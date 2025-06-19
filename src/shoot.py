import numpy as np
import gfootball.env as football_env
from gfootball.env import config as gfootball_config

class ShootDetector:
    """
    simple115形式の観測を入力として、シュートが打たれたかを判別するクラスである。
    前回の観測を保持し、ボールの位置、速度、プレイヤー、ゴール両端に基づいてシュートを検出する。
    オウンゴールへのシュートは検出しない。
    """

    def __init__(self):
        """
        コンストラクタ。
        """
        self.previous_obs = None

        # ゴールポストのY座標 (Google Footballの標準ゴール幅を考慮)
        self.goal_y_upper = 0.2
        self.goal_y_lower = -0.2

        # ゴールのX座標
        self.left_goal_x = -1.0
        self.right_goal_x = 1.0

        # シュート検出を限定するX座標の範囲
        self.shoot_detect_range_x = 0.3
        self.left_shoot_max_x = self.left_goal_x + self.shoot_detect_range_x  # 左ゴールから右方向へ
        self.right_shoot_min_x = self.right_goal_x - self.shoot_detect_range_x # 右ゴールから左方向へ

    def update(self, current_obs: dict) -> bool:
        """
        現在の観測を更新し、シュートが打たれたかを判別する。

        Args:
            current_obs (dict): simple115形式の現在の観測。

        Returns:
            bool: シュートが打たれたと判断された場合にTrue、それ以外はFalseである。
        """
        if self.previous_obs is None:
            self.previous_obs = current_obs
            return False

        is_shot = self._detect_shot(current_obs, self.previous_obs)
        self.previous_obs = current_obs
        return is_shot

    def _detect_shot(self, current_obs: dict, prev_obs: dict) -> bool:
        """
        前後の観測を比較してシュートを検出する内部メソッドである。
        """
        current_ball_pos = np.array(current_obs['ball'])
        current_ball_vel = np.array(current_obs['ball_direction'])

        # 1. ボール保持プレイヤーとチームの特定
        ball_owned_team = current_obs['ball_owned_team']
        ball_owned_player_idx = current_obs['ball_owned_player']

        if ball_owned_team == -1 or ball_owned_player_idx == -1:
            return False # シュートはボール保持者がいる状態で発生すると仮定する

        # 2. ボールの初期位置が指定範囲内にあるかを確認
        ball_x, ball_y = current_ball_pos[0], current_ball_pos[1]

        if ball_owned_team == 0: # 左チーム (右ゴールへシュート)
            if ball_x < self.right_shoot_min_x: # 右ゴールに対するシュート範囲外
                return False
        else: # 右チーム (左ゴールへシュート)
            if ball_x > self.left_shoot_max_x: # 左ゴールに対するシュート範囲外
                return False

        # 3. ゴール方向の判定 (オウンゴール除外)
        # ボールが自ゴールに向かっているかを確認
        if (ball_owned_team == 0 and current_ball_vel[0] < 0) or \
           (ball_owned_team == 1 and current_ball_vel[0] > 0):
            return False # 自ゴールに向かっている場合、オウンゴールへのシュートとみなし検出しない

        # 4. ボールからゴール両端への「視野角」判定 (2D平面での判定)
        if ball_owned_team == 0: # 左チームのシュート (右ゴールへ向かう)
            target_goal_x = self.right_goal_x
        else: # 右チームのシュート (左ゴールへ向かう)
            target_goal_x = self.left_goal_x

        # ボールが既に目標ゴールを通過している場合はシュートとしない
        if (ball_owned_team == 0 and ball_x > target_goal_x) or \
           (ball_owned_team == 1 and ball_x < target_goal_x):
            return False 

        # ボールが進む方向のY座標を予測 (単純な線形予測)
        if current_ball_vel[0] == 0:
            return False # X方向への速度がない場合、ゴールには進まない

        time_to_reach_goal_x = (target_goal_x - ball_x) / current_ball_vel[0]
        
        if time_to_reach_goal_x < 0:
            return False

        predicted_ball_y_at_goal_x = ball_y + current_ball_vel[1] * time_to_reach_goal_x

        # 予測されたY座標がゴールの範囲内にあるか
        if self.goal_y_lower <= predicted_ball_y_at_goal_x <= self.goal_y_upper:
            return True # すべての条件を満たした場合、シュートと判断する

        return False