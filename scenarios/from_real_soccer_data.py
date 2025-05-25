from gfootball.scenarios import *

def build_scenario(builder):
	builder.config().game_duration = 3000
	builder.config().right_team_difficulty = 0.6
	builder.config().deterministic = False
	builder.config().deterministic = True
	builder.SetBallPosition(-0.807047619047619, -0.15552352941176467)
	if builder.EpisodeNumber() % 2 == 0:
		first_team = Team.e_Left
		second_team = Team.e_Right
	else:
		first_team = Team.e_Right
		second_team = Team.e_Left
	builder.SetTeam(first_team)
	builder.AddPlayer(-0.897714, 0.155894, e_PlayerRole_GK)
	builder.AddPlayer(-0.406286, -0.232235, e_PlayerRole_LB)
	builder.AddPlayer(-0.538667, 0.319694, e_PlayerRole_RB)
	builder.AddPlayer(0.000190, -0.321176, e_PlayerRole_LM)
	builder.AddPlayer(-0.241905, -0.039529, e_PlayerRole_RM)
	builder.AddPlayer(0.084762, -0.058924, e_PlayerRole_CF)
	builder.AddPlayer(0.078667, 0.286218, e_PlayerRole_CF)
	builder.AddPlayer(-0.496000, -0.050400, e_PlayerRole_CB)
	builder.AddPlayer(-0.393905, 0.205924, e_PlayerRole_DM)
	builder.AddPlayer(-0.057524, -0.039653, e_PlayerRole_DM)
	builder.AddPlayer(-0.487619, 0.133041, e_PlayerRole_CB)
	builder.SetTeam(second_team)
	builder.AddPlayer(-0.564000, -0.042124, e_PlayerRole_GK)
	builder.AddPlayer(-0.040952, 0.142059, e_PlayerRole_LB)
	builder.AddPlayer(-0.053905, -0.261882, e_PlayerRole_RB)
	builder.AddPlayer(0.173524, -0.220253, e_PlayerRole_LM)
	builder.AddPlayer(0.076571, -0.046818, e_PlayerRole_RM)
	builder.AddPlayer(0.496000, -0.296100, e_PlayerRole_CF)
	builder.AddPlayer(0.277524, 0.146259, e_PlayerRole_CF)
	builder.AddPlayer(0.440190, -0.174053, e_PlayerRole_CF)
	builder.AddPlayer(-0.057143, -0.118218, e_PlayerRole_CB)
	builder.AddPlayer(0.759238, -0.174424, e_PlayerRole_DM)
	builder.AddPlayer(-0.104571, 0.007659, e_PlayerRole_CB)
