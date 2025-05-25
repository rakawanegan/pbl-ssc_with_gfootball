from gfootball.scenarios import *

def build_scenario(builder):
	builder.config().game_duration = 3000
	builder.config().right_team_difficulty = 1.0
	builder.config().left_team_difficulty = 1.0
	builder.config().deterministic = False
	builder.config().end_episode_on_score = True
	builder.config().deterministic = True
	builder.SetBallPosition(-0.9055238095238095, 0.20765294117647054)
	if builder.EpisodeNumber() % 2 == 0:
		first_team = Team.e_Left
		second_team = Team.e_Right
	else:
		first_team = Team.e_Right
		second_team = Team.e_Left
	builder.SetTeam(first_team)
	builder.AddPlayer(-0.965524, -0.065841, e_PlayerRole_GK)
	builder.AddPlayer(-0.837524, -0.198882, e_PlayerRole_LB)
	builder.AddPlayer(-0.519048, 0.080418, e_PlayerRole_RB)
	builder.AddPlayer(0.065143, -0.349959, e_PlayerRole_LM)
	builder.AddPlayer(-0.478476, -0.055712, e_PlayerRole_RM)
	builder.AddPlayer(0.122667, -0.185541, e_PlayerRole_CF)
	builder.AddPlayer(-0.088952, 0.119576, e_PlayerRole_CF)
	builder.AddPlayer(-0.939048, -0.203082, e_PlayerRole_CB)
	builder.AddPlayer(-0.481714, -0.226059, e_PlayerRole_DM)
	builder.AddPlayer(-0.140952, -0.067818, e_PlayerRole_DM)
	builder.AddPlayer(-0.676190, -0.014576, e_PlayerRole_CB)
	builder.SetTeam(second_team)
	builder.AddPlayer(-0.531048, -0.039529, e_PlayerRole_GK)
	builder.AddPlayer(-0.068952, 0.304994, e_PlayerRole_LB)
	builder.AddPlayer(0.132762, -0.195547, e_PlayerRole_RB)
	builder.AddPlayer(0.185714, 0.092771, e_PlayerRole_LM)
	builder.AddPlayer(0.279238, 0.236682, e_PlayerRole_RM)
	builder.AddPlayer(0.925333, 0.199624, e_PlayerRole_CF)
	builder.AddPlayer(0.732571, 0.290047, e_PlayerRole_CF)
	builder.AddPlayer(0.533714, 0.032241, e_PlayerRole_CF)
	builder.AddPlayer(-0.113333, -0.053735, e_PlayerRole_CB)
	builder.AddPlayer(0.401524, -0.061641, e_PlayerRole_DM)
	builder.AddPlayer(-0.075429, 0.156882, e_PlayerRole_CB)
