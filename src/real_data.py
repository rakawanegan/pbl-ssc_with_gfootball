def make_scenario_from_real_data(tracking_framedf):
    tracking_framedf = tracking_framedf.copy()

    position_to_gfootball_role_dict ={
    "GK": "e_PlayerRole_GK",
    'DF': "e_PlayerRole_CB ",
    'MF': "e_PlayerRole_DM ",
    'FW': "e_PlayerRole_CF ",
    }
    tracking_framedf["gfootball_role"] = tracking_framedf["ポジション"].map(position_to_gfootball_role_dict)

    ball_point_x, ball_point_y = map(float, tracking_framedf.loc[tracking_framedf["HA"] == 0, ["norm_X", "norm_Y"]].values.flatten())

    # GFootballでは自陣営→敵陣営の座標系のため、ファーストチームの座標系は反転する必要がある。
    hometeams = list()
    tracking_framedf.loc[tracking_framedf["HA"] == 1, "norm_Y"] *= -1
    for _, row in tracking_framedf.loc[tracking_framedf["HA"] == 1].iterrows():
        hometeams.append(f'\tbuilder.AddPlayer({row["norm_X"]:.6f}, {row["norm_Y"]:.6f}, {row["gfootball_role"]})')
    hometeams = "\n".join(hometeams)

    awayteams = list()
    tracking_framedf.loc[tracking_framedf["HA"] == 2, "norm_X"] *= -1
    for _, row in tracking_framedf.loc[tracking_framedf["HA"] == 2].iterrows():
        awayteams.append(f'\tbuilder.AddPlayer({row["norm_X"]:.6f}, {row["norm_Y"]:.6f}, {row["gfootball_role"]})')
    awayteams = "\n".join(awayteams)

    return (
    "from gfootball.scenarios import *\n\n"
    "def build_scenario(builder):\n"
    "\tbuilder.config().game_duration = 3000\n"
    "\tbuilder.config().right_team_difficulty = 1.0\n"
    "\tbuilder.config().left_team_difficulty = 1.0\n"
    "\tbuilder.config().deterministic = False\n"
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