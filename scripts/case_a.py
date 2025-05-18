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
from src.real_data import make_scenario_from_real_data


def main():
    # 環境生成
    p_scenario = './scenarios/from_real_soccer_data.py'
    env_dict = dict(
        representation="simple115",  # 入力情報
        render=True,
        write_video=False,        # 動画保存を有効化
    )

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
    tracking_df = tracking_df.merge(
        player_df[["ホームアウェイF", "選手背番号", "ポジション"]],
        left_on=["HA", "No"],
        right_on=["ホームアウェイF", "選手背番号"],
        how="left"
    )

    # 特定フレームのデータ抽出
    ini_frame = int(tracking_df.loc[tracking_df['No'] == 0, "Frame"].iloc[0])
    tracking_framedf = tracking_df.loc[tracking_df["Frame"] == ini_frame]

    scenario_file = make_scenario_from_real_data(tracking_framedf)

    with open(p_scenario, "w", encoding="utf-8") as f:
        f.write(scenario_file)

    env = create_environment_with_custom_environment(p_scenario, **env_dict)

    obs = env.reset()
    done = False
    while not done:
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        env.render()
    env.close()


if __name__ == "__main__":
    main()