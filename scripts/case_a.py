"""
あるプレーが結果に与える影響を、該当プレー実行時と非実行時で比較
"""
import os
import gym
from stable_baselines3 import PPO

import sys;sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.scenario import create_environment_with_custom_environment


# 環境生成
p_scenario = './scenarios/from_real_soccer_data.py'
env_dict = dict(
    representation="simple115",  # 入力情報
    render=True,
    write_video=True,        # 動画保存を有効化
)
env = create_environment_with_custom_environment(p_scenario, **env_dict)

obs = env.reset()
done = False
while not done:
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    env.render()
env.close()
