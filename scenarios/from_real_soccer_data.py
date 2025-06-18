from gfootball.scenarios import *

def build_scenario(builder):
	builder.config().game_duration = 750
	builder.config().right_team_difficulty = 1.0
	builder.config().left_team_difficulty = 1.0
	builder.config().deterministic = False
	builder.config().end_episode_on_score = True
	builder.SetBallPosition(1.0, 0.42)
	if builder.EpisodeNumber() % 2 == 0:
		first_team = Team.e_Left
		second_team = Team.e_Right
	else:
		first_team = Team.e_Right
		second_team = Team.e_Left
	builder.SetTeam(first_team)
	builder.AddPlayer(-0.031429, -0.000000, e_PlayerRole_GK)
	builder.AddPlayer(0.961524, -0.399494, e_PlayerRole_LB)
	builder.AddPlayer(0.476952, -0.027424, e_PlayerRole_RB)
	builder.AddPlayer(0.597143, -0.159724, e_PlayerRole_LM)
	builder.AddPlayer(0.665143, 0.049535, e_PlayerRole_RM)
	builder.AddPlayer(0.886667, 0.002224, e_PlayerRole_CF)
	builder.AddPlayer(0.828571, -0.058553, e_PlayerRole_CF)
	builder.AddPlayer(0.797714, 0.058553, e_PlayerRole_CB)
	builder.AddPlayer(0.888381, -0.025447, e_PlayerRole_DM)
	builder.AddPlayer(0.834286, -0.030388, e_PlayerRole_DM)
	builder.AddPlayer(0.796190, 0.010994, e_PlayerRole_CB)
	builder.SetTeam(second_team)
	builder.AddPlayer(-0.959429, -0.010006, e_PlayerRole_GK)
	builder.AddPlayer(-0.845333, -0.017294, e_PlayerRole_LB)
	builder.AddPlayer(-0.840762, 0.005559, e_PlayerRole_RB)
	builder.AddPlayer(-0.897333, 0.022359, e_PlayerRole_LM)
	builder.AddPlayer(-0.820381, -0.053365, e_PlayerRole_RM)
	builder.AddPlayer(-0.934095, 0.067447, e_PlayerRole_CF)
	builder.AddPlayer(-0.769143, 0.117724, e_PlayerRole_CF)
	builder.AddPlayer(-0.914667, 0.032859, e_PlayerRole_CF)
	builder.AddPlayer(-0.846857, 0.044471, e_PlayerRole_CB)
	builder.AddPlayer(-0.741905, -0.049906, e_PlayerRole_DM)
	builder.AddPlayer(-0.908952, 0.013218, e_PlayerRole_CB)
