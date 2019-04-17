"""This file contains the MiniMax and alpha beta pruning algorithms.
"""
import random
from random import randint

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    """
    # we start using the open_move_score defined in sample players
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))

    raise NotImplementedError




class IsolationPlayer:
    """Base class for minimax and alphabeta agents 
    """
    def __init__(self, search_depth=5, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """depth-limited minimax search algorithm 
        """

        # TODO: finish this function!
        # Defining nested functions
        def maximum_val_level(game, depth):
            # verify time constraint
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            # initialize score to -inf
            score = float('-inf')
            # get the legal moves of the level
            level_legal_moves = game.get_legal_moves()
            # return score of it is final level
            if depth == 0 or len(level_legal_moves) == 0:
                return self.score(game, self)

            # iterate over all possible moves and get the min score from next level
            for move in level_legal_moves:
                # get the new board after the move
                game_subbranch = game.forecast_move(move)
                # get the score from the nex level whivh is a min level
                new_score = minimum_val_level(game_subbranch, depth - 1)
                # if the new score is higher the the prev score update score
                score = max(score, new_score)
            return score

        def minimum_val_level(game, depth):          
            # verify time constraint
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # get the legal moves of the level
            level_legal_moves = game.get_legal_moves()
            # return score of it is final level
            if depth == 0 or len(level_legal_moves) == 0:
                return self.score(game, self)
            # initialize score to -inf
            score = float('inf')
            # iterate over all possible moves and get the max score from next level
            for move in level_legal_moves:
                # get the new board after the move
                game_subbranch = game.forecast_move(move)
                # get the score from the nex level whivh is a min level
                new_score = maximum_val_level(game_subbranch, depth - 1)
                # if the new score is lower the the prev score update score
                score = min(score, new_score)
            return score

        # verify time constraint
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # initialize score to -inf
        score = float('-inf')
        # initialize best move to (-1, -1)
        best_move = (-1,-1)        
        # get the legal moves of the level
        level_legal_moves = game.get_legal_moves()
        # chosing the best move randomly if there are possible moves
        if level_legal_moves:
            _, best_move = max([(self.score(game.forecast_move(m), self), m) for m in level_legal_moves])
        # we start with a max level
        # iterate over all possible moves and get the min score from next level and recursively alternating between max and min levels
        for move in level_legal_moves:
            game_subbranch = game.forecast_move(move)
            new_score = minimum_val_level(game_subbranch, depth-1)
            # if the new score is higher the the prev score update score and best move
            if new_score > score:
                best_move = move
                score = new_score

        return best_move
        raise NotImplementedError


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        """
        self.time_left = time_left

        # TODO: finish this function!
        best_move = (-1,-1)
        level_legal_moves = game.get_legal_moves()
        if level_legal_moves:
            _, best_move = max([(self.score(game.forecast_move(m), self), m) for m in level_legal_moves])

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.alphabeta(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed
        return best_move
        

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """depth-limited minimax search with alpha-beta pruning 
        """


        def level_max_value_alpha_beta(game, depth, alpha, beta):
            # verify time constraint
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

            # get the legal moves of the level
            level_legal_moves = game.get_legal_moves()

            # return score of it is final level
            if depth == 0 or len(level_legal_moves) == 0:
                return self.score(game, self)

            # initialize score
            score = float('-inf')
            # iterate over possible moves
            for move in level_legal_moves:
                game_subbranch = game.forecast_move(move)
                # alternate recursive calling
                new_score = level_min_value_alpha_beta(game_subbranch, depth - 1, alpha, beta)
                # update score
                score = max(score, new_score)
                # beta stopping criteria
                if score >= beta:
                    return score
                # update alpha
                alpha = max(alpha, score)
            return score

        def level_min_value_alpha_beta(game, depth, alpha, beta):
            # verify time constraint
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            # get the legal moves of the level
            level_legal_moves = game.get_legal_moves()
            # return score of it is final level or terminal state
            if depth == 0 or len(level_legal_moves) == 0:
                return self.score(game, self)
            # initialize score
            score = float('inf')
            # iterate over possible moves 
            for move in level_legal_moves:
                game_subbranch = game.forecast_move(move)
                # alternate recursive calling
                new_score = level_max_value_alpha_beta(game_subbranch, depth - 1, alpha, beta)
                # update score
                score = min(score, new_score)
                # alpha stopping criteria
                if score <= alpha:
                    return score
                # update beta
                beta = min(beta, score)
            return score

        #initialize best move
        best_move = (-1,-1)
        # get possible moves
        level_legal_moves = game.get_legal_moves()
        # associate randome move to best move
        if level_legal_moves:
            _, best_move = max([(self.score(game.forecast_move(m), self), m) for m in level_legal_moves])
        # initialize score
        score = float('-inf')
        # iterate over posible moves ( max level )
        for move in level_legal_moves:
            game_subbranch = game.forecast_move(move)
            # alternate recursive calling
            new_score = level_min_value_alpha_beta(game_subbranch, depth-1, alpha, beta)
            # update score and best move
            if new_score >= score:
                score = new_score
                best_move = move
            # beta stopping criteria
            if new_score >= beta:
                return best_move
            # update alpha
            alpha = max(alpha, new_score)
        return best_move


        # TODO: finish this function!
        raise NotImplementedError
