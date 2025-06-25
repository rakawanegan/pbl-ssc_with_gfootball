from gfootball.scenarios import *

def build_scenario(builder):
	builder.config().game_duration = 200
	builder.config().right_team_difficulty = 1.0
	builder.config().left_team_difficulty = 1.0
	builder.config().deterministic = False
	builder.config().end_episode_on_score = True
	builder.config().end_episode_on_out_of_play = True
	builder.SetBallPosition(0.5784761904761904, -0.2837470588235294)
	first_team = Team.e_Left
	second_team = Team.e_Right
	builder.SetTeam(first_team)
	builder.AddPlayer(-0.537905, -0.031500, e_PlayerRole_GK)
	builder.AddPlayer(0.578476, 0.283747, e_PlayerRole_LB)
	builder.AddPlayer(0.474286, -0.061147, e_PlayerRole_RB)
	builder.AddPlayer(0.720000, 0.073376, e_PlayerRole_LM)
	builder.AddPlayer(0.751429, 0.020876, e_PlayerRole_RM)
	builder.AddPlayer(0.480571, -0.031624, e_PlayerRole_CF)
	builder.AddPlayer(0.722095, -0.152806, e_PlayerRole_CF)
	builder.AddPlayer(0.013333, -0.006424, e_PlayerRole_CB)
	builder.AddPlayer(0.241905, 0.057935, e_PlayerRole_DM)
	builder.AddPlayer(0.747238, 0.103765, e_PlayerRole_DM)
	builder.AddPlayer(0.032952, -0.169482, e_PlayerRole_CB)
	builder.SetTeam(second_team)
	builder.AddPlayer(-0.938667, 0.011118, e_PlayerRole_GK)
	builder.AddPlayer(-0.743238, 0.124888, e_PlayerRole_LB)
	builder.AddPlayer(-0.737714, -0.108829, e_PlayerRole_RB)
	builder.AddPlayer(-0.620571, 0.087953, e_PlayerRole_LM)
	builder.AddPlayer(-0.665714, 0.027918, e_PlayerRole_RM)
	builder.AddPlayer(-0.522286, -0.098453, e_PlayerRole_CF)
	builder.AddPlayer(-0.579619, 0.228653, e_PlayerRole_CF)
	builder.AddPlayer(-0.060000, -0.186653, e_PlayerRole_CF)
	builder.AddPlayer(-0.747619, -0.001359, e_PlayerRole_CB)
	builder.AddPlayer(-0.342286, -0.021988, e_PlayerRole_DM)
	builder.AddPlayer(-0.776571, 0.047065, e_PlayerRole_CB)
