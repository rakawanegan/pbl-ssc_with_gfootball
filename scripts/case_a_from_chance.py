"""
あるプレーが結果に与える影響を、該当プレー実行時と非実行時で比較
"""
import os
import gym
import pandas as pd
import hydra
from hydra.core.hydra_config import HydraConfig
import swifter
# from stable_baselines3 import PPO

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.util import make_player_df_from_playdf, norm_xy_to_gfootball, find_nearest
from src.scenario import create_environment_with_custom_environment
from src.real_data import make_scenario_from_real_data, assosiate_player_detail_role
from src.visualization import plot_gfootball_scenario_with_roles


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


@hydra.main(version_base=None, config_path="conf", config_name="case_a")
def main(cfg):
    output_dir = HydraConfig.get().runtime.output_dir
    if not cfg.debug:
        defeat_excess_logger()
    # 環境生成
    render = False  # 画面表示
    dump = False  # ログ出力
    p_scenario = "./scenarios/from_real_soccer_data.py"
    env_dict = dict(
        representation="simple115",  # 入力情報
        stacked=False,
        number_of_left_players_agent_controls=0,
        number_of_right_players_agent_controls=0,
        players="",
    )

    if render:
        env_dict["render"] = True
        env_dict["real_time"] = True

    if dump:
        env_dict["dump_full_episodes"] = True

    data_dir = "data/unofficial/2023041506"
    p_play = os.path.join(data_dir, "play.csv")
    p_tracking = os.path.join(data_dir, "tracking.csv")
    play_df = pd.read_csv(p_play, encoding="ansi")
    tracking_df = pd.read_csv(p_tracking)

    player_df = make_player_df_from_playdf(play_df)
    tracking_df[["norm_X", "norm_Y"]] = tracking_df.swifter.apply(
        lambda row: pd.Series(norm_xy_to_gfootball(row["X"], row["Y"])), axis=1
    )

    ini_frame = int(tracking_df.loc[tracking_df["No"] == 0, "Frame"].iloc[0])
    tracking_framedf = tracking_df.loc[tracking_df["Frame"] == ini_frame]
    player_df = assosiate_player_detail_role(player_df, tracking_framedf)

    tracking_df = tracking_df.merge(
        player_df[["ホームアウェイF", "選手背番号", "ポジション"]],
        left_on=["HA", "No"],
        right_on=["ホームアウェイF", "選手背番号"],
        how="left",
    )

    # 特定フレームのデータ抽出
    buff_frame = cfg.buf_time * cfg.fps
    target_frame = cfg.data.frame_id - buff_frame
    contain_ball_frames = (
        tracking_df.loc[tracking_df["No"] == 0, "Frame"].unique().tolist()
    )
    approx_target_frame = find_nearest(contain_ball_frames, target_frame)
    if cfg.debug:
        print(f"[debug] Target frame: {target_frame}")
        print(f"[debug] Approximate target frame: {approx_target_frame}")
    tracking_framedf = tracking_df.loc[tracking_df["Frame"] == approx_target_frame]

    scenario_file = make_scenario_from_real_data(tracking_framedf, cfg)

    with open(p_scenario, "w", encoding="utf-8") as f:
        f.write(scenario_file)

    plot_gfootball_scenario_with_roles(p_scenario, output_dir)
    # シミュレーションの実行

    results = list()
    sub_results = list()
    for _ in range(cfg.n_iter):
        for n_iter in range(cfg.n_sub_iter):
            env = create_environment_with_custom_environment(p_scenario, **env_dict)

            if render:
                env.render()
            env.reset()
            done = False
            while not done:
                action = env.action_space.sample()
                obs, reward, done, info = env.step([])
                if render:
                    env.render()
            env.close()

            # home is left team, away is right team. if home team wins, score_reward is 1
            winner = (
                "Home"
                if info["score_reward"] == 1
                else "Away"
                if info["score_reward"] == -1
                else "Draw"
            )

            if cfg.debug:
                print(f"[debug] Iteration {n_iter + 1}/{cfg.n_iter}: Winner is {winner}")
            sub_results.append(winner)
        chance_team_winning_percentage = sub_results.count(cfg.data.which_chance) / cfg.n_sub_iter * 100
        results.append({
            "chance_team": chance_team_winning_percentage,
        })

        if cfg.debug:
            print(f"[debug] {cfg.n_sub_iter} iterations completed.")
        print(
            f"[info] Results: frame={cfg.data.frame_id}, chance team={cfg.data.which_chance}"
        )
        print(
            f"[info] Results of Winning rate: {chance_team_winning_percentage:.2f}% Chance Team, "
        )
        sub_results.clear()

    # export results to CSV
    results_df = pd.DataFrame({
        "frame_id": [cfg.data.frame_id] * len(results),
        "chance_team": [cfg.data.which_chance] * len(results),
        "chance_team_winning_percentage": [r["chance_team"] for r in results],
        "n_iter": [cfg.n_iter] * len(results),
        "n_sub_iter": [cfg.n_sub_iter] * len(results),
    })
    print(f'[info] chance_team_winning_percentage: {results_df["chance_team_winning_percentage"].mean():.2f}%')
    results_csv_path = os.path.join(output_dir, f"results_{cfg.data.frame_id}.csv")
    results_df.to_csv(results_csv_path, index=False, encoding="utf-8")


if __name__ == "__main__":
    main()
