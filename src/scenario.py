import os
import shutil
import importlib.util

from gfootball.env import config
from gfootball.env import football_env

def create_environment_with_custom_environment(custom_scenario_path, **kwargs):
    """
    指定されたカスタムシナリオを GFootball ライブラリ内に一時的にコピーし、
    create_environment を呼び出して環境を作成後、シナリオを削除する。
    
    Parameters:
        custom_scenario_path (str): カスタムシナリオファイルのフルパス
        **kwargs: create_environment に渡す他の引数

    Returns:
        gym.Env: 作成された環境
    """
    if not os.path.isfile(custom_scenario_path):
        raise FileNotFoundError(f"指定されたファイルが存在しません: {custom_scenario_path}")
    
    # GFootballのscenariosディレクトリを特定
    gfootball_spec = importlib.util.find_spec("gfootball")
    if gfootball_spec is None or gfootball_spec.submodule_search_locations is None:
        raise ImportError("gfootball ライブラリが見つかりませんでした。")

    gfootball_path = gfootball_spec.submodule_search_locations[0]
    scenarios_dir = os.path.join(gfootball_path, "scenarios")
    if not os.path.isdir(scenarios_dir):
        raise FileNotFoundError(f"GFootballのscenariosディレクトリが見つかりません: {scenarios_dir}")

    # カスタムファイル名
    scenario_filename = os.path.basename(custom_scenario_path)
    temp_scenario_path = os.path.join(scenarios_dir, scenario_filename)

    try:
        # シナリオをコピー
        shutil.copyfile(custom_scenario_path, temp_scenario_path)

        # env_name をファイル名から推測（例: "custom_scenario.py" → "custom_scenario"）
        env_name = os.path.splitext(scenario_filename)[0]

        # 環境を作成
        cfg_values = kwargs.copy()
        cfg_values['action_set'] = 'default'
        cfg_values['level'] = env_name  # シナリオ名をレベルとして設定
        cfg = config.Config(cfg_values)
        env = football_env.FootballEnv(cfg)
        return env

    finally:
        # シナリオを削除
        if os.path.isfile(temp_scenario_path):
            os.remove(temp_scenario_path)