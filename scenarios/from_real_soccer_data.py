from gfootball.scenarios import *

def build_scenario(builder):
	builder.config().game_duration = 3000
	builder.config().right_team_difficulty = 1.0
	builder.config().left_team_difficulty = 1.0
	builder.config().deterministic = False
	builder.config().end_episode_on_score = True
	builder.SetBallPosition(-0.06171428571428572, -0.31685294117647056)
	if builder.EpisodeNumber() % 2 == 0:
		first_team = Team.e_Left
		second_team = Team.e_Right
	else:
		first_team = Team.e_Right
		second_team = Team.e_Left
	builder.SetTeam(first_team)
	builder.AddPlayer(-0.731238, 0.098329, e_PlayerRole_GK)
	builder.AddPlayer(-0.193524, -0.212471, e_PlayerRole_LB)
	builder.AddPlayer(-0.061714, 0.316853, e_PlayerRole_RB)
	builder.AddPlayer(0.323238, -0.105618, e_PlayerRole_LM)
	builder.AddPlayer(0.098857, 0.196906, e_PlayerRole_RM)
	builder.AddPlayer(0.272381, 0.039159, e_PlayerRole_CF)
	builder.AddPlayer(0.276952, 0.169729, e_PlayerRole_CF)
	builder.AddPlayer(-0.429905, 0.050276, e_PlayerRole_CB)
	builder.AddPlayer(-0.151810, 0.103641, e_PlayerRole_DM)
	builder.AddPlayer(0.276762, -0.144035, e_PlayerRole_DM)
	builder.AddPlayer(-0.177333, 0.266824, e_PlayerRole_CB)
	builder.SetTeam(second_team)
	builder.AddPlayer(-0.678857, -0.036688, e_PlayerRole_GK)
	builder.AddPlayer(-0.321714, 0.085606, e_PlayerRole_LB)
	builder.AddPlayer(-0.239619, -0.280412, e_PlayerRole_RB)
	builder.AddPlayer(-0.133905, -0.059418, e_PlayerRole_LM)
	builder.AddPlayer(-0.029143, -0.201353, e_PlayerRole_RM)
	builder.AddPlayer(0.042857, -0.324635, e_PlayerRole_CF)
	builder.AddPlayer(-0.022476, 0.094747, e_PlayerRole_CF)
	builder.AddPlayer(0.194286, -0.261018, e_PlayerRole_CF)
	builder.AddPlayer(-0.322095, -0.142800, e_PlayerRole_CB)
	builder.AddPlayer(0.126667, -0.192953, e_PlayerRole_DM)
	builder.AddPlayer(-0.337524, -0.045582, e_PlayerRole_CB)
