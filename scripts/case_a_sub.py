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
        representation="extracted",  # 入力情報
        render=True,  # 画面表示
        stacked=False,
        logdir="./logs",  # ログディレクトリ
        write_video=False,        # 動画保存
    )

    env = create_environment_with_custom_environment(p_scenario, **env_dict)

    obs = env.reset()
    done = False
    while not done:
        action = env.action_space.sample()
        print(f"[info] {action=}")
        obs, reward, done, info = env.step(action)
        print(f"[info] {info=}")
        env.render()
        print(f"[info] rendered")
    env.close()


if __name__ == "__main__":
    main()