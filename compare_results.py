
from random import randint
from random import seed
from isolation import Board
from game_agent import MinimaxPlayer
from game_agent import AlphaBetaPlayer
from sample_players import RandomPlayer
from sample_players import GreedyPlayer


def initialize_board(player1, player2, height, width):
	game = Board(player1, player2)
	i1=randint(0, height-1)
	j1=randint(0, width-1)
	i2 = i1
	j2 = j1
	while((i1 == i2) and (j1 == j2)):
		i2=randint(0, height-1)
		j2=randint(0, width-1)
	game.apply_move((i1, j1))
	game.apply_move((i2, j2))
	return game

if __name__ == "__main__":
	seed(312)
	player1 = RandomPlayer()
	player2 = MinimaxPlayer(search_depth=1, timeout=10.)
	height = 7
	width = 7
	player1_wins=0
	total = 100
	for i in range(total):
		game = initialize_board(player1, player2, height, width)
		#assert(player1 == game.active_player)
		print i
		print("\nOld state:\n{}".format(game.to_string()))

		winner, history, outcome = game.play(time_limit=150)
		print 
		if ((winner == player1) and (outcome == "illegal move")):
			player1_wins+=1

		# print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
    	#print(game.to_string())
     	#print("Move history:\n{!s}".format(history))

 	print "\n results: "
 	print  player1_wins
