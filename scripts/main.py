from gfootball.env import config, football_env

cfg = config.Config({
    'level': '11_vs_11_stochastic',
    'render': True,       # 画面表示を有効化
    'real_time': True,     # 人間観察用にスローダウン
    'write_video': True,        # 動画保存を有効化
    'dump_frequency': 1,         # 1エピソードごとにダンプ
})
env = football_env.FootballEnv(cfg)

obs = env.reset()
done = False
while not done:
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    env.render()
env.close()
