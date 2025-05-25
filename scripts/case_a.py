"""
あるプレーが結果に与える影響を、該当プレー実行時と非実行時で比較
"""
import os
import gym
import pandas as pd
import swifter
from stable_baselines3 import PPO

import sys;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.util import make_player_df_from_playdf, norm_xy_to_gfootball
from src.scenario import create_environment_with_custom_environment
from src.real_data import make_scenario_from_real_data, assosiate_player_detail_role


def main():
    # 環境生成
    render = False  # 画面表示
    dump = False  # ログ出力
    p_scenario = './scenarios/from_real_soccer_data.py'
    env_dict = dict(
        representation="simple115",  # 入力情報
        stacked=False,
        number_of_left_players_agent_controls=0,
        number_of_right_players_agent_controls=0,
        players = "",
    )

    if render:
        env_dict["render"] = True
        env_dict["real_time"] = True

    if dump:
        env_dict["dump_full_episodes"] = True

    data_dir = 'data/unofficial/2023041506'
    p_play = os.path.join(data_dir, 'play.csv')
    p_tracking = os.path.join(data_dir, 'tracking.csv')
    play_df = pd.read_csv(p_play, encoding='ansi')
    tracking_df = pd.read_csv(p_tracking)

    player_df = make_player_df_from_playdf(play_df)
    tracking_df[["norm_X", "norm_Y"]] = tracking_df.swifter.apply(
        lambda row: pd.Series(norm_xy_to_gfootball(row["X"], row["Y"])),
        axis=1
    )

    ini_frame = int(tracking_df.loc[tracking_df['No'] == 0, "Frame"].iloc[0])
    tracking_framedf = tracking_df.loc[tracking_df["Frame"] == ini_frame]
    player_df = assosiate_player_detail_role(player_df, tracking_framedf)

    tracking_df = tracking_df.merge(
        player_df[["ホームアウェイF", "選手背番号", "ポジション"]],
        left_on=["HA", "No"],
        right_on=["ホームアウェイF", "選手背番号"],
        how="left"
    )

    # 特定フレームのデータ抽出
    target_frame = int(tracking_df.loc[tracking_df['No'] == 0, "Frame"].sample(1).iloc[0])
    tracking_framedf = tracking_df.loc[tracking_df["Frame"] == target_frame]

    scenario_file = make_scenario_from_real_data(tracking_framedf)

    with open(p_scenario, "w", encoding="utf-8") as f:
        f.write(scenario_file)

    max_iter = 100
    results = list()
    for n_iter in range(max_iter):
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
        winner = "Home" if info["score_reward"] == 1 else "Away" if info["score_reward"] == -1 else "Draw"
        print(f"[info] Iteration {n_iter + 1}/{max_iter}: Winner is {winner}")
        results.append(winner)

    print(f"[info] {max_iter} iterations completed.")
    print(f"[info] Results of Winning rate: {results.count('Home') / max_iter * 100:.2f}% Home, {results.count('Away') / max_iter * 100:.2f}% Away, {results.count('Draw') / max_iter * 100:.2f}% Draw")


if __name__ == "__main__":
    main()