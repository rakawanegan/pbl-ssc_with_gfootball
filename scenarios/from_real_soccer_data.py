from gfootball.scenarios import *

def build_scenario(builder):
	builder.config().game_duration = 200
	builder.config().right_team_difficulty = 1.0
	builder.config().left_team_difficulty = 1.0
	builder.config().deterministic = False
	builder.config().end_episode_on_score = True
	builder.config().end_episode_on_out_of_play = True
	builder.SetBallPosition(-0.5689523809523809, -0.17182941176470595)
	first_team = Team.e_Left
	second_team = Team.e_Right
	builder.SetTeam(first_team)
	builder.AddPlayer(-0.924381, 0.029029, e_PlayerRole_GK)
	builder.AddPlayer(-0.622667, 0.247059, e_PlayerRole_LB)
	builder.AddPlayer(-0.311619, -0.169235, e_PlayerRole_RB)
	builder.AddPlayer(-0.240762, 0.288441, e_PlayerRole_LM)
	builder.AddPlayer(-0.381714, 0.182700, e_PlayerRole_RM)
	builder.AddPlayer(-0.019048, 0.182082, e_PlayerRole_CF)
	builder.AddPlayer(-0.013714, -0.169359, e_PlayerRole_CF)
	builder.AddPlayer(-0.624952, 0.128965, e_PlayerRole_CB)
	builder.AddPlayer(-0.568952, 0.171829, e_PlayerRole_DM)
	builder.AddPlayer(-0.062095, 0.100800, e_PlayerRole_DM)
	builder.AddPlayer(-0.617143, -0.051018, e_PlayerRole_CB)
	builder.SetTeam(second_team)
	builder.AddPlayer(-0.595619, 0.036935, e_PlayerRole_GK)
	builder.AddPlayer(0.317524, 0.361818, e_PlayerRole_LB)
	builder.AddPlayer(-0.064000, -0.151941, e_PlayerRole_RB)
	builder.AddPlayer(0.063810, 0.188259, e_PlayerRole_LM)
	builder.AddPlayer(0.280762, 0.141565, e_PlayerRole_RM)
	builder.AddPlayer(0.470667, -0.087953, e_PlayerRole_CF)
	builder.AddPlayer(0.600381, 0.297088, e_PlayerRole_CF)
	builder.AddPlayer(0.559238, 0.181465, e_PlayerRole_CF)
	builder.AddPlayer(-0.120381, 0.075106, e_PlayerRole_CB)
	builder.AddPlayer(0.573524, 0.089312, e_PlayerRole_DM)
	builder.AddPlayer(-0.094286, 0.223465, e_PlayerRole_CB)
