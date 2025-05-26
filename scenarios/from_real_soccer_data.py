from gfootball.scenarios import *

def build_scenario(builder):
	builder.config().game_duration = 3000
	builder.config().right_team_difficulty = 1.0
	builder.config().left_team_difficulty = 1.0
	builder.config().deterministic = False
	builder.config().end_episode_on_score = True
	builder.SetBallPosition(-0.1024761904761905, -0.2848588235294117)
	if builder.EpisodeNumber() % 2 == 0:
		first_team = Team.e_Left
		second_team = Team.e_Right
	else:
		first_team = Team.e_Right
		second_team = Team.e_Left
	builder.SetTeam(first_team)
	builder.AddPlayer(-0.669333, 0.046200, e_PlayerRole_GK)
	builder.AddPlayer(-0.220952, -0.060653, e_PlayerRole_LB)
	builder.AddPlayer(0.278476, 0.331553, e_PlayerRole_RB)
	builder.AddPlayer(0.288952, -0.168247, e_PlayerRole_LM)
	builder.AddPlayer(0.015810, 0.159971, e_PlayerRole_RM)
	builder.AddPlayer(0.333714, 0.178871, e_PlayerRole_CF)
	builder.AddPlayer(0.234286, 0.218524, e_PlayerRole_CF)
	builder.AddPlayer(-0.210095, 0.083135, e_PlayerRole_CB)
	builder.AddPlayer(-0.112571, 0.244094, e_PlayerRole_DM)
	builder.AddPlayer(0.010667, 0.034588, e_PlayerRole_DM)
	builder.AddPlayer(-0.196762, 0.252247, e_PlayerRole_CB)
	builder.SetTeam(second_team)
	builder.AddPlayer(-0.764571, -0.036688, e_PlayerRole_GK)
	builder.AddPlayer(-0.347810, 0.071153, e_PlayerRole_LB)
	builder.AddPlayer(-0.164571, -0.315124, e_PlayerRole_RB)
	builder.AddPlayer(-0.087810, -0.209012, e_PlayerRole_LM)
	builder.AddPlayer(0.023619, -0.095735, e_PlayerRole_RM)
	builder.AddPlayer(-0.141524, -0.291406, e_PlayerRole_CF)
	builder.AddPlayer(0.001333, 0.114882, e_PlayerRole_CF)
	builder.AddPlayer(0.130667, -0.064729, e_PlayerRole_CF)
	builder.AddPlayer(-0.332000, -0.148976, e_PlayerRole_CB)
	builder.AddPlayer(0.102476, -0.284859, e_PlayerRole_DM)
	builder.AddPlayer(-0.336571, -0.031871, e_PlayerRole_CB)
