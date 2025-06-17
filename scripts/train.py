import gym
from stable_baselines3 import PPO
from gfootball.env import create_environment

# 環境生成
env = create_environment(
    env_name="11_vs_11_stochastic",  # シナリオ
    representation="simple115",  # 入力情報
    render=False,
)

# モデル定義
model = PPO(
    policy="MlpPolicy",
    env=env,
    verbose=1,
    learning_rate=2.5e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
)

# 学習実行（例：1万ステップ）
model.learn(total_timesteps=10_000)

# 学習後の評価
env = create_environment(
    env_name="11_vs_11_stochastic",
    write_full_episode_dumps=True,  # 全エピソードのトレースを出力
    write_goal_dumps=True,  # ゴール前 200 フレームのトレースも出力
    tracesdir="./logs",  # トレースの出力先ディレクトリ
    write_video=True,  # 動画不要なら False（True にすると AVI も同時出力）
    render=False,
)
obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()

env.close()
