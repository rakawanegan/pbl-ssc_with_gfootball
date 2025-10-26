"""
あるプレーが結果に与える影響を、該当プレー実行時と非実行時で比較
"""
import os
import sys
import gym
import numpy as np
import pandas as pd
import hydra
from hydra.core.hydra_config import HydraConfig
import swifter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.util import make_player_df_from_playdf, norm_xy_to_gfootball, find_nearest
from src.scenario import create_environment_with_custom_environment
from src.real_data import make_scenario_from_real_data, assosiate_player_detail_role
from src.visualization import plot_gfootball_scenario_with_roles
from src.shoot import ShootDetector


def defeat_excess_logger():
    """
    gfootballのログ出力を抑制する
    """
    import logging
    import warnings
    import pandas as pd
    from pandas.errors import SettingWithCopyWarning

    absl_logger = logging.getLogger("absl")
    absl_logger.setLevel(logging.WARNING)
    warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
    warnings.simplefilter(action="ignore", category=FutureWarning)


def extract_data_from_raw(raw_obs):
    """
    "raw"観測辞書からトラッキングデータを抽出する。
    """
    records = []

    # ホームチーム（左チーム）
    for i, (pos, direction) in enumerate(
        zip(raw_obs["left_team"], raw_obs["left_team_direction"])
    ):
        if np.all(pos == -1):
            continue
        speed = np.linalg.norm(direction)
        records.append(
            {
                "HA": 1,
                "SysTarget": i + 1,
                "No": i + 1,
                "X": pos[0],
                "Y": pos[1],
                "Speed": speed,
            }
        )

    # アウェイチーム（右チーム）
    for i, (pos, direction) in enumerate(
        zip(raw_obs["right_team"], raw_obs["right_team_direction"])
    ):
        if np.all(pos == -1):
            continue
        speed = np.linalg.norm(direction)
        records.append(
            {
                "HA": 2,
                "SysTarget": 11 + i + 1,
                "No": i + 1,
                "X": pos[0],
                "Y": pos[1],
                "Speed": speed,
            }
        )

    # ボール
    ball_pos = raw_obs["ball"]
    ball_dir = raw_obs["ball_direction"]
    ball_speed = np.linalg.norm(ball_dir)
    records.append(
        {
            "HA": 0,
            "SysTarget": 99,
            "No": 0,
            "X": ball_pos[0],
            "Y": ball_pos[1],
            "Speed": ball_speed,
        }
    )

    return records


# simple115 形式における主要なインデックス定義
BALL_X = 0
BALL_Y = 1
BALL_Z = 2
BALL_VEL_X = 3
BALL_VEL_Y = 4
BALL_VEL_Z = 5
BALL_OWNED_TEAM = 6  # 0: left, 1: right, -1: none
BALL_OWNED_PLAYER = 7


def convert_raw_to_simple115_array(raw_obs_dict):
    """
    raw 形式の観測辞書から、ShootDetector が要求する
    simple115 形式の numpy.ndarray (115,) を構築する。
    ボール関連の情報のみを移し、他はゼロで埋める。
    """
    simple115_array = np.zeros(115, dtype=np.float32)

    if raw_obs_dict is None:
        return simple115_array

    # ボール座標
    if "ball" in raw_obs_dict:
        simple115_array[BALL_X] = raw_obs_dict["ball"][0]
        simple115_array[BALL_Y] = raw_obs_dict["ball"][1]
        simple115_array[BALL_Z] = raw_obs_dict["ball"][2]

    # ボール速度
    if "ball_direction" in raw_obs_dict:
        simple115_array[BALL_VEL_X] = raw_obs_dict["ball_direction"][0]
        simple115_array[BALL_VEL_Y] = raw_obs_dict["ball_direction"][1]
        simple115_array[BALL_VEL_Z] = raw_obs_dict["ball_direction"][2]

    # ボール所有権
    if "ball_owned_team" in raw_obs_dict:
        simple115_array[BALL_OWNED_TEAM] = raw_obs_dict["ball_owned_team"]
    if "ball_owned_player" in raw_obs_dict:
        simple115_array[BALL_OWNED_PLAYER] = raw_obs_dict["ball_owned_player"]

    return simple115_array


def get_team_name(team_id):
    """ チームID (0, 1, -1) を文字列に変換する """
    if team_id == 0:
        return "Left"
    if team_id == 1:
        return "Right"
    return "None"


@hydra.main(version_base=None, config_path="conf", config_name="case_a")
def main(cfg):
    output_dir = HydraConfig.get().runtime.output_dir
    if cfg.debug:
        cfg.n_iter = 1
        cfg.n_sub_iter = 1
    else:
        defeat_excess_logger()

    # CSVファイルの保存先ディレクトリを作成する
    save_dir = "simulated_data"
    os.makedirs(save_dir, exist_ok=True)

    # cfg.n_iterの回数だけシミュレーションを繰り返す
    for i in range(cfg.n_iter):
        print(f"----- Simulation loop: {i+1}/{cfg.n_iter} -----")
        # 環境生成
        p_scenario = "./scenarios/base_scenario.py"
        env_dict = dict(
            representation="simple115",
            stacked=False,
            number_of_left_players_agent_controls=0,
            number_of_right_players_agent_controls=0,
            players="",
        )

        if cfg.render:
            env_dict["render"] = True
            env_dict["real_time"] = True

        if cfg.dump:
            env_dict["dump_full_episodes"] = True

        if i == 0:  # 初回のみシナリオをプロットする
            plot_gfootball_scenario_with_roles(p_scenario, output_dir)

        env = create_environment_with_custom_environment(p_scenario, **env_dict)

        if cfg.render:
            env.render()

        env.reset()
        done = False
        step_count = 0
        tracking_data_records = []

        # イベント検出器とログの初期化
        shoot_detector = ShootDetector()
        event_log_records = []
        current_score = [0, 0]  # 現在のスコアを追跡

        # ループ初回比較のため、リセット直後の観測で検出器と状態を初期化
        raw_obs_list_init = env.unwrapped.observation()
        raw_obs_init = (
            raw_obs_list_init[0]
            if isinstance(raw_obs_list_init, list)
            else raw_obs_list_init
        )
        simple_obs_array_init = convert_raw_to_simple115_array(raw_obs_init)
        shoot_detector.update(
            simple_obs_array_init
        )  # 最初の 'previous_obs' として設定

        # ボール所有権の追跡用変数
        prev_ball_owned_team = raw_obs_init.get("ball_owned_team", -1)
        # ルーズボールになる直前の所有者情報を保持する
        last_owner_before_loose = {
            "team": prev_ball_owned_team,
            "player": raw_obs_init.get("ball_owned_player", -1),
        }

        while not done:
            _, _, done, info = env.step([])
            step_count += 1

            # raw_obs を取得 (リスト対応)
            raw_obs_list = env.unwrapped.observation()
            raw_obs = (
                raw_obs_list[0]
                if isinstance(raw_obs_list, list)
                else raw_obs_list
            )

            if not raw_obs:
                continue

            # raw_obs から simple115 形式の配列を自作
            simple_obs_array = convert_raw_to_simple115_array(raw_obs)

            # 現在のボール所有権
            current_ball_owned_team = raw_obs.get("ball_owned_team", -1)
            current_ball_owned_player = raw_obs.get("ball_owned_player", -1)

            # --- イベント検出ロジック ---

            # 1. 「シュート」イベントの検出 (自作した simple115 配列を使用)
            is_shoot = shoot_detector.update(simple_obs_array)

            if is_shoot:
                shoot_info = shoot_detector.dump_shoot_info()
                # シュートはルーズボールになる直前のプレイヤーが実行したとみなす
                shooter_team_int = last_owner_before_loose["team"]
                shooter_player_idx = last_owner_before_loose["player"]

                event_log_records.append(
                    {
                        "GameID": i,
                        "Frame": step_count,
                        "Event": "Shot_Attempt",
                        "Team": get_team_name(shooter_team_int),
                        "Player": shooter_player_idx,
                        "X": shoot_info["coordinates"][0],
                        "Y": shoot_info["coordinates"][1],
                        "Speed": np.linalg.norm(shoot_info["direction"]),
                    }
                )

            # 2. 「ゴール」イベントの検出 (info を使用)
            new_score = info.get("score", current_score)
            goal_team = None
            if new_score[0] > current_score[0]:
                goal_team = "Left"
            elif new_score[1] > current_score[1]:
                goal_team = "Right"

            if goal_team:
                event_log_records.append(
                    {
                        "GameID": i,
                        "Frame": step_count,
                        "Event": "Goal",
                        "Team": goal_team,
                        "Player": -1,  # infoからだけではキッカーは不明
                        "X": raw_obs["ball"][0],
                        "Y": raw_obs["ball"][1],
                        "Speed": np.linalg.norm(raw_obs["ball_direction"]),
                    }
                )
            current_score = new_score  # スコアを更新

            # 3. 「パス（成功）」と「ボールロスト」の検出
            # ボールがルーズボールでなくなり、所有権が確定した瞬間(prev=-1, current!=-1)に判定
            if current_ball_owned_team != -1 and prev_ball_owned_team == -1:

                # 3a. 「パス（成功）」
                # ルーズボール直前の所有者とチームが同じで、プレイヤーが異なる
                if (
                    last_owner_before_loose["team"] == current_ball_owned_team
                    and last_owner_before_loose["player"]
                    != current_ball_owned_player
                    and last_owner_before_loose["player"] != -1
                ):
                    event_log_records.append(
                        {
                            "GameID": i,
                            "Frame": step_count,
                            "Event": "Pass_Success",
                            "Team": get_team_name(current_ball_owned_team),
                            "Player": last_owner_before_loose["player"],  # パサー
                            "X": raw_obs["ball"][0],
                            "Y": raw_obs["ball"][1],
                            "Speed": np.linalg.norm(
                                raw_obs["ball_direction"]
                            ),
                        }
                    )

                # 3b. 「ボールロスト」
                # ルーズボール直前の所有者とチームが異なる
                elif (
                    last_owner_before_loose["team"] != -1
                    and last_owner_before_loose["team"]
                    != current_ball_owned_team
                ):
                    event_log_records.append(
                        {
                            "GameID": i,
                            "Frame": step_count,
                            "Event": "Possession_Lost",
                            "Team": get_team_name(
                                last_owner_before_loose["team"]
                            ),  # 失ったチーム
                            "Player": last_owner_before_loose[
                                "player"
                            ],  # 失ったプレイヤー
                            "X": raw_obs["ball"][0],
                            "Y": raw_obs["ball"][1],
                            "Speed": np.linalg.norm(
                                raw_obs["ball_direction"]
                            ),
                        }
                    )

            # --- 既存のトラッキングデータ抽出 (raw形式を使用) ---
            extracted_records = extract_data_from_raw(raw_obs)
            for record in extracted_records:
                record["GameID"] = i  # GameIDをループのインデックスに設定
                record["Frame"] = step_count
                tracking_data_records.append(record)

            if cfg.render:
                env.render()

            # --- 状態の更新 ---
            # ボールがルーズボールでない場合、「ルーズボールになる直前の所有者」情報を更新
            if current_ball_owned_team != -1:
                last_owner_before_loose = {
                    "team": current_ball_owned_team,
                    "player": current_ball_owned_player,
                }

            prev_ball_owned_team = current_ball_owned_team

        env.close()

        # 全シミュレーションステップのデータをDataFrameに変換
        df_tracking = pd.DataFrame(tracking_data_records)

        # CSVファイルとして連番で保存
        output_filename = os.path.join(
            save_dir, f"simulated_tracking_data_{i}.csv"
        )
        df_tracking.to_csv(output_filename, index=False, encoding="utf-8")
        print(f"Successfully saved tracking data to: {output_filename}")

        # イベントログの保存
        if event_log_records:  # ログがある場合のみ保存
            df_events = pd.DataFrame(event_log_records)
            event_output_filename = os.path.join(
                save_dir, f"simulated_event_data_{i}.csv"
            )
            df_events.to_csv(
                event_output_filename, index=False, encoding="utf-8"
            )
            print(f"Successfully saved event data to: {event_output_filename}")
        else:
            print("No events were detected in this simulation.")


if __name__ == "__main__":
    main()