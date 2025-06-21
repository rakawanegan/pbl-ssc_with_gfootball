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
    
    # raw_obsの構造:
    # 'left_team': (11, 2) の座標配列
    # 'right_team': (11, 2) の座標配列
    # 'ball': (3,) の座標 (x, y, z)
    # 'left_team_direction': (11, 2) の速度ベクトル配列
    # 'right_team_direction': (11, 2) の速度ベクトル配列
    # 'ball_direction': (3,) の速度ベクトル
    
    # ホームチーム（左チーム）
    for i, (pos, direction) in enumerate(zip(raw_obs['left_team'], raw_obs['left_team_direction'])):
        if np.all(pos == -1): continue # 無効なプレイヤーはスキップ
        speed = np.linalg.norm(direction)
        records.append({
            'HA': 1, 'SysTarget': i + 1, 'No': i + 1,
            'X': pos[0], 'Y': pos[1], 'Speed': speed
        })

    # アウェイチーム（右チーム）
    for i, (pos, direction) in enumerate(zip(raw_obs['right_team'], raw_obs['right_team_direction'])):
        if np.all(pos == -1): continue
        speed = np.linalg.norm(direction)
        records.append({
            'HA': 2, 'SysTarget': 11 + i + 1, 'No': i + 1,
            'X': pos[0], 'Y': pos[1], 'Speed': speed
        })
        
    # ボール
    ball_pos = raw_obs['ball']
    ball_dir = raw_obs['ball_direction']
    ball_speed = np.linalg.norm(ball_dir)
    records.append({
        'HA': 0, 'SysTarget': 99, 'No': 0,
        'X': ball_pos[0], 'Y': ball_pos[1], 'Speed': ball_speed
    })
    
    return records


@hydra.main(version_base=None, config_path="conf", config_name="case_a")
def main(cfg):
    output_dir = HydraConfig.get().runtime.output_dir
    if cfg.debug:
        cfg.n_iter = 1
        cfg.n_sub_iter = 1
    else:
        defeat_excess_logger()
    # 環境生成
    p_scenario = "./scenarios/base_scenario.py"
    env_dict = dict(
        representation="simple115",  # 入力情報
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

    plot_gfootball_scenario_with_roles(p_scenario, output_dir)

    env = create_environment_with_custom_environment(p_scenario, **env_dict)

    if cfg.render:
        env.render()
    env.reset()
    done = False
    step_count = 0
    tracking_data_records = []
    while not done:
        _, _, done, info = env.step([])
        step_count += 1

        # 環境から"raw"形式の完全な観測を取得
        raw_obs = env.unwrapped.observation()

        # 抽出したデータを、求めるCSV形式のレコードに追加
        extracted_records = extract_data_from_raw(raw_obs[0] if isinstance(raw_obs, list) else raw_obs)

        for record in extracted_records:
            record['GameID'] = 0
            record['Frame'] = step_count
            tracking_data_records.append(record)

        if cfg.render:
            env.render()

    env.close()

    # 全シミュレーションステップのデータをDataFrameに変換
    df_tracking = pd.DataFrame(tracking_data_records)

    # CSVファイルとして保存
    output_dir
    output_filename = f'simulated_tracking_data.csv'
    df_tracking.to_csv(
        os.path.join(output_dir, output_filename),
        index=False,
        encoding="utf-8"
    )


if __name__ == "__main__":
    main()
