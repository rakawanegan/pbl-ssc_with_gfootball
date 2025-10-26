import numpy as np

# simple115 形式における主要なインデックス定義
BALL_X = 0
BALL_Y = 1
BALL_Z = 2
BALL_VEL_X = 3
BALL_VEL_Y = 4
BALL_VEL_Z = 5
BALL_OWNED_TEAM = 6  # 0: left, 1: right, -1: none
BALL_OWNED_PLAYER = 7


class ShootDetector:
    """
    simple115形式 (np.ndarray) の観測を入力として、シュートが打たれたかを判別するクラスである。
    前回の観測を保持し、ボールの位置、方向、ゴール両端への線形予測に基づいてシュートを検出する。
    オウンゴール（自ゴールに向かうキック）は検出しない。
    """

    def __init__(self):
        """
        コンストラクタ。
        """
        self.previous_obs = None
        self.last_shoot_info = None  # シュートが検出された際の座標と方向を保持する

        # ゴールポストのY座標 (Google Footballの標準ゴール幅を考慮)
        self.goal_y_upper = 0.044
        self.goal_y_lower = -0.044

        # ゴールのX座標
        self.left_goal_x = -1.0
        self.right_goal_x = 1.0

        # シュート検出を限定するX座標の範囲
        self.shoot_detect_range_x = 0.5
        self.left_shoot_max_x = (
            self.left_goal_x + self.shoot_detect_range_x
        )  # 左ゴールから右方向へ
        self.right_shoot_min_x = (
            self.right_goal_x - self.shoot_detect_range_x
        )  # 右ゴールから左方向へ

    def update(self, current_obs: np.ndarray) -> bool:
        """
        現在の観測を更新し、シュートが打たれたかを判別する。

        Args:
            current_obs (np.ndarray): simple115形式 (115,) の現在の観測。

        Returns:
            bool: シュートが打たれたと判断された場合にTrue、それ以外はFalseである。
        """
        
        # ### 修正: 入力形式のバリデーション ###
        if not isinstance(current_obs, np.ndarray) or current_obs.shape != (115,):
            raise ValueError("入力は (115,) 形状の simple115 形式 numpy.ndarray である必要があります。")

        if self.previous_obs is None:
            self.previous_obs = current_obs
            return False

        is_shoot = self._detect_shoot(current_obs, self.previous_obs)
        if is_shoot:
            # シュート検出時に座標と方向を保存
            self.last_shoot_info = {
                "coordinates": current_obs[BALL_X : BALL_Z + 1].tolist(),
                "direction": current_obs[BALL_VEL_X : BALL_VEL_Z + 1].tolist(),
            }
        else:
            self.last_shoot_info = None  # シュートが検出されなかった場合はリセット

        self.previous_obs = current_obs
        return is_shoot

    def _detect_shoot(self, current_obs: np.ndarray, prev_obs: np.ndarray) -> bool:
        """
        前後の観測を比較してシュートを検出する内部メソッドである。
        """
        
        # 1. simple115 インデックスから状態を取得
        ball_x = current_obs[BALL_X]
        ball_y = current_obs[BALL_Y]
        ball_vel_x = current_obs[BALL_VEL_X]
        ball_vel_y = current_obs[BALL_VEL_Y]
        
        current_ball_owned_team = int(current_obs[BALL_OWNED_TEAM])

        # 2. シュート実行チームの特定
        # キック直後にルーズボール(-1)になる可能性があるため、
        # 現在(-1)なら、直前(prev_obs)に保持していたチームをキッカーとみなす
        if current_ball_owned_team == -1:
            shooter_team = int(prev_obs[BALL_OWNED_TEAM])
        else:
            shooter_team = current_ball_owned_team
            
        if shooter_team == -1: # 直前もルーズボールならキックではない
             return False 

        # 3. ボールの初期位置が指定範囲内にあるかを確認
        if shooter_team == 0:  # 左チーム (右ゴールへシュート)
            if ball_x < self.right_shoot_min_x:  # 右ゴールに対するシュート範囲外
                return False
        else:  # 右チーム (左ゴールへシュート)
            if ball_x > self.left_shoot_max_x:  # 左ゴールに対するシュート範囲外
                return False

        # 4. オウンゴール方向の判定 (要求仕様)
        # 左チーム(0)が撃つ場合、X速度(vel_x)は正(> 0)でなければならない
        if shooter_team == 0 and ball_vel_x <= 0:
            return False  # 自ゴール方向(または静止)
        # 右チーム(1)が撃つ場合、X速度(vel_x)は負(< 0)でなければならない
        if shooter_team == 1 and ball_vel_x >= 0:
            return False  # 自ゴール方向(または静止)

        # 5. ゴール枠への線形予測 (オウンゴール方向は 4. で除外済み)
        if shooter_team == 0:  # 左チーム -> 右ゴール
            target_goal_x = self.right_goal_x
        else:  # 右チーム -> 左ゴール
            target_goal_x = self.left_goal_x

        # X方向の速度は 4. で 0 でないことが保証されている
        time_to_reach_goal_x = (target_goal_x - ball_x) / ball_vel_x

        # 予測時間が負になるケース（ゴールラインを過ぎてから撃つなど）を除外
        if time_to_reach_goal_x < 0:
            return False

        # ゴールライン到達時のY座標を予測
        predicted_ball_y_at_goal_x = ball_y + ball_vel_y * time_to_reach_goal_x

        # 予測されたY座標がゴールの範囲内にあるか
        if self.goal_y_lower <= predicted_ball_y_at_goal_x <= self.goal_y_upper:
            return True  # すべての条件を満たした場合、シュートと判断する

        return False

    def dump_shoot_info(self) -> dict:
        """
        最後にシュートが検出された際のボールの座標と方向を返す。
        シュートが検出されていない場合はNoneを返す。

        Returns:
            dict: シュートが打たれた際のボールの座標 [x, y, z] および方向 [vx, vy, vz] の辞書。
                  シュートが検出されていない場合はNone。
        """
        return self.last_shoot_info