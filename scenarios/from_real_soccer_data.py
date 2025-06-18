from gfootball.scenarios import *

def build_scenario(builder):
	builder.config().game_duration = 750
	builder.config().right_team_difficulty = 1.0
	builder.config().left_team_difficulty = 1.0
	builder.config().deterministic = False
	builder.config().end_episode_on_score = True
	builder.config().end_episode_on_out_of_play = True
	builder.config().end_episode_on_possession_change = True
	builder.SetBallPosition(0.8615238095238096, 0.02075294117647053)
	if builder.EpisodeNumber() % 2 == 0:
		first_team = Team.e_Left
		second_team = Team.e_Right
	else:
		first_team = Team.e_Right
		second_team = Team.e_Left
	builder.SetTeam(first_team)
	builder.AddPlayer(-0.023429, 0.000247, e_PlayerRole_GK)
	builder.AddPlayer(0.927810, -0.380841, e_PlayerRole_LB)
	builder.AddPlayer(0.479048, -0.028412, e_PlayerRole_RB)
	builder.AddPlayer(0.589333, -0.149965, e_PlayerRole_LM)
	builder.AddPlayer(0.654857, 0.041629, e_PlayerRole_RM)
	builder.AddPlayer(0.861524, -0.020753, e_PlayerRole_CF)
	builder.AddPlayer(0.871048, -0.076959, e_PlayerRole_CF)
	builder.AddPlayer(0.880381, 0.066706, e_PlayerRole_CB)
	builder.AddPlayer(0.894095, -0.058182, e_PlayerRole_DM)
	builder.AddPlayer(0.887429, -0.065841, e_PlayerRole_DM)
	builder.AddPlayer(0.846857, -0.026188, e_PlayerRole_CB)
	builder.SetTeam(second_team)
	builder.AddPlayer(-0.977524, 0.022853, e_PlayerRole_GK)
	builder.AddPlayer(-0.836000, 0.013465, e_PlayerRole_LB)
	builder.AddPlayer(-0.888190, 0.060776, e_PlayerRole_RB)
	builder.AddPlayer(-0.903238, 0.054971, e_PlayerRole_LM)
	builder.AddPlayer(-0.825143, -0.044841, e_PlayerRole_RM)
	builder.AddPlayer(-0.908952, 0.082765, e_PlayerRole_CF)
	builder.AddPlayer(-0.754095, 0.118465, e_PlayerRole_CF)
	builder.AddPlayer(-0.905333, 0.054600, e_PlayerRole_CF)
	builder.AddPlayer(-0.883619, 0.077947, e_PlayerRole_CB)
	builder.AddPlayer(-0.727048, -0.038541, e_PlayerRole_DM)
	builder.AddPlayer(-0.891429, -0.008894, e_PlayerRole_CB)
