import pandas as pd


def assosiate_player_detail_role(player_df, init_frame_tracking_df):
    player_df = player_df.copy()
    init_frame_tracking_df = init_frame_tracking_df.copy()

    tempdf = init_frame_tracking_df.merge(
        player_df[["ホームアウェイF", "選手背番号", "ポジション", "ポジションID", "選手名"]],
        left_on=["HA", "No"],
        right_on=["ホームアウェイF", "選手背番号"],
        how="left"
    )
    tempdf = tempdf.loc[tempdf["HA"] != 0]

    new_row = list()
    for ha, ha_df in tempdf.groupby("HA"):
        for pos, pos_df in ha_df.groupby("ポジション"):
            if pos == "DF" and len(pos_df) == 4:
                pos_df.loc[pos_df["Y"].idxmax(), "ポジション"] = "LB"
                pos_df.loc[pos_df["Y"].idxmin(), "ポジション"] = "RB"

            elif pos == "MF" and len(pos_df) >= 3:
                pos_df.loc[pos_df["Y"].idxmax(), "ポジション"] = "LM"
                pos_df.loc[pos_df["Y"].idxmin(), "ポジション"] = "RM"

            new_row.append(pos_df)
    new_df = pd.concat(new_row, ignore_index=True)
    new_player_df = new_df[["ホームアウェイF", "選手背番号", "ポジションID", "選手名", "ポジション"]]
    new_player_df[[ "ホームアウェイF", "選手背番号", "ポジションID"]] = new_player_df[[ "ホームアウェイF", "選手背番号", "ポジションID"]].map(int)
    return new_player_df


def make_scenario_from_real_data(tracking_framedf):
    tracking_framedf = tracking_framedf.copy()

    position_to_gfootball_role_dict ={
    "GK": "e_PlayerRole_GK",

    'DF': "e_PlayerRole_CB",  # DF は GFootball では CB として扱う
    'CB': "e_PlayerRole_CB",
    'LB': "e_PlayerRole_LB",
    'RB': "e_PlayerRole_RB",

    'MF': "e_PlayerRole_DM",  # MF は GFootball では DM として扱う
    "CM": "e_PlayerRole_CM",
    "LM": "e_PlayerRole_LM",
    "RM": "e_PlayerRole_RM",
    "AM": "e_PlayerRole_AM",

    'FW': "e_PlayerRole_CF",  # FW は GFootball では CF として扱う
    "CF": "e_PlayerRole_CF",
    }
    tracking_framedf["gfootball_role"] = tracking_framedf["ポジション"].map(position_to_gfootball_role_dict)

    ball_point_x, ball_point_y = map(float, tracking_framedf.loc[tracking_framedf["HA"] == 0, ["norm_X", "norm_Y"]].values.flatten())
    # GFootballではシナリオのロールの登場順番が揃っている必要がある（GK→*B→*M→*F）.
    position_order = ['GK', 'CB', 'LB', 'RB', 'DM', 'CM', 'LM', 'RM', 'AM', 'CF', 'LF', 'RF', 'FW']
    tracking_framedf['ポジション'] = pd.Categorical(
        tracking_framedf['ポジション'],
        categories=position_order,
        ordered=True
    )
    tracking_framedf = tracking_framedf.sort_values("ポジション")

    # 元のAwayteam (HA == 2) が新しいHometeam (first_team) になる
    hometeams = list()
    # GFootballでは first_team の座標系として Y を反転する想定 (元のコードの HA == 1 に対する処理)
    tracking_framedf.loc[tracking_framedf["HA"] == 2, "norm_Y"] *= -1
    for _, row in tracking_framedf.loc[tracking_framedf["HA"] == 2].iterrows():
        hometeams.append(f'\tbuilder.AddPlayer({row["norm_X"]:.6f}, {row["norm_Y"]:.6f}, {row["gfootball_role"]})')
    hometeams = "\n".join(hometeams)

    # 元のHometeam (HA == 1) が新しいAwayteam (second_team) になる
    awayteams = list()
    # GFootballでは second_team の座標系として X を反転する想定 (元のコードの HA == 2 に対する処理)
    tracking_framedf.loc[tracking_framedf["HA"] == 1, "norm_X"] *= -1
    for _, row in tracking_framedf.loc[tracking_framedf["HA"] == 1].iterrows():
        awayteams.append(f'\tbuilder.AddPlayer({row["norm_X"]:.6f}, {row["norm_Y"]:.6f}, {row["gfootball_role"]})')
    awayteams = "\n".join(awayteams)

    return (
    "from gfootball.scenarios import *\n\n"
    "def build_scenario(builder):\n"
    "\tbuilder.config().game_duration = 3000\n"
    "\tbuilder.config().right_team_difficulty = 1.0\n"
    "\tbuilder.config().left_team_difficulty = 1.0\n"
    "\tbuilder.config().deterministic = False\n"
    # "\tbuilder.config().offsides = False\n"
    "\tbuilder.config().end_episode_on_score = True\n"
    # "\tbuilder.config().end_episode_on_out_of_play = True\n"
    # "\tbuilder.config().end_episode_on_possession_change = True\n"
    f"\tbuilder.SetBallPosition({ball_point_x}, {ball_point_y})\n"
    "\tif builder.EpisodeNumber() % 2 == 0:\n"
    "\t\tfirst_team = Team.e_Left\n"
    "\t\tsecond_team = Team.e_Right\n"
    "\telse:\n"
    "\t\tfirst_team = Team.e_Right\n"
    "\t\tsecond_team = Team.e_Left\n"
    "\tbuilder.SetTeam(first_team)\n"
    f"{hometeams}\n"
    "\tbuilder.SetTeam(second_team)\n"
    f"{awayteams}\n"
    )