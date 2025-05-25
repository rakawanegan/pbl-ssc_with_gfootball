from gfootball.scenarios import *

def build_scenario(builder):
	builder.config().game_duration = 3000
	builder.config().right_team_difficulty = 0.6
	builder.config().deterministic = False
	builder.config().deterministic = True
	builder.SetBallPosition(0.0, 0.0)
	if builder.EpisodeNumber() % 2 == 0:
		first_team = Team.e_Left
		second_team = Team.e_Right
	else:
		first_team = Team.e_Right
		second_team = Team.e_Left
	builder.SetTeam(first_team)
	builder.AddPlayer(-0.870476, 0.001976, e_PlayerRole_GK)
	builder.AddPlayer(-0.150286, 0.107100, e_PlayerRole_RM)
	builder.AddPlayer(0.006286, 0.113524, e_PlayerRole_CF)
	builder.AddPlayer(-0.185333, 0.290047, e_PlayerRole_CF)
	builder.AddPlayer(-0.097905, -0.190729, e_PlayerRole_LM)
	builder.AddPlayer(-0.397714, -0.006671, e_PlayerRole_CB)
	builder.AddPlayer(-0.206857, 0.013094, e_PlayerRole_DM)
	builder.AddPlayer(-0.002286, -0.109941, e_PlayerRole_DM)
	builder.AddPlayer(-0.308952, -0.141071, e_PlayerRole_LB)
	builder.AddPlayer(-0.400381, 0.150088, e_PlayerRole_CB)
	builder.AddPlayer(-0.383238, 0.294000, e_PlayerRole_RB)
	builder.SetTeam(second_team)
	builder.AddPlayer(-0.100000, -0.214076, e_PlayerRole_RB)
	builder.AddPlayer(-0.356762, -0.094747, e_PlayerRole_CB)
	builder.AddPlayer(0.008000, 0.002841, e_PlayerRole_DM)
	builder.AddPlayer(-0.000762, -0.357000, e_PlayerRole_CF)
	builder.AddPlayer(-0.064000, 0.059912, e_PlayerRole_LM)
	builder.AddPlayer(-0.174286, -0.015812, e_PlayerRole_RM)
	builder.AddPlayer(-0.242286, 0.160712, e_PlayerRole_LB)
	builder.AddPlayer(-0.005905, 0.235447, e_PlayerRole_CF)
	builder.AddPlayer(-0.761143, -0.005559, e_PlayerRole_GK)
	builder.AddPlayer(-0.005333, -0.263118, e_PlayerRole_CF)
	builder.AddPlayer(-0.349905, 0.027671, e_PlayerRole_CB)
