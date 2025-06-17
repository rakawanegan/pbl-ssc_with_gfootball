def make_player_df_from_playdf(playdf):
    play_df = playdf.copy()
    # ホームアウェイF	1:ホームチーム　2:アウェイチーム
    # ポジションID	1:GK　2:DF　3:MF　4:FW　0:不明選手or選手のプレーではないもの

    position_dict = {
        1: "GK",
        2: "DF",
        3: "MF",
        4: "FW",
    }
    player_df = (
        play_df[["ホームアウェイF", "選手背番号", "ポジションID", "選手名"]]
        .dropna()
        .drop_duplicates()
        .sort_values(["ホームアウェイF", "ポジションID"])
    )
    player_df["選手背番号"] = player_df["選手背番号"].map(int)
    player_df["ポジション"] = player_df["ポジションID"].map(position_dict)
    player_df = player_df.reset_index(drop=True)
    return player_df


def norm_xy_to_gfootball(x, y):
    # GFootball の座標範囲
    gfootball_x_min, gfootball_x_max = -1.0, 1.0
    gfootball_y_min, gfootball_y_max = -0.42, 0.42

    # データスタジアムの座標範囲
    datastudium_x_min, datastudium_x_max = -5250.0, 5250.0
    datastudium_y_min, datastudium_y_max = -3400.0, 3400.0

    # 線形変換
    norm_x = ((x - datastudium_x_min) / (datastudium_x_max - datastudium_x_min)) * (
        gfootball_x_max - gfootball_x_min
    ) + gfootball_x_min
    norm_y = ((y - datastudium_y_min) / (datastudium_y_max - datastudium_y_min)) * (
        gfootball_y_max - gfootball_y_min
    ) + gfootball_y_min

    return norm_x, norm_y


def find_nearest(
    value_list: list[float | int], target_value: float | int
) -> float | int | None:
    if not value_list:
        return None
    nearest_value = min(value_list, key=lambda x: abs(x - target_value))
    return nearest_value
