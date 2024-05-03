import random
from game_board import GameBoard
from move import Move, InvalidMoveError
import numpy as np
from itertools import combinations


class Player:
    def __init__(self, color, board, strategy='minimax'):
        self.color = color  # Player's color (0 for black, 1 for white)
        self.board = board  # Reference to the game board
        self.strategy = strategy  # Strategy can be 'minimax' or 'random'

    def choose_move(self, depth=3):
        """
        Choose a move based on the specified strategy.
        """
        if self.strategy == 'minimax':
            return self.best_move(depth)
        elif self.strategy == 'random':
            return self.random_move()
        else:
            raise ValueError("Unsupported strategy specified")

    def find_all_marbles(self):
        """Retrieve all positions of this player's marbles on the board."""
        return [(i, j) for i in range(self.board.board.shape[0])
                for j in range(self.board.board.shape[1])
                if self.board.board[i][j] == self.color]

    def random_move(self):
        """Generate and apply a random valid move from all possible moves."""
        all_possible_moves = self.generate_all_possible_moves()
        if not all_possible_moves:
            print("No valid moves available.")
            return False  # No valid moves to make

        # Select a random move from the list of all valid moves
        random_move = random.choice(all_possible_moves)
        return random_move

    def generate_all_possible_moves(self):
        """Generate all valid moves for the current player.
        >>> board = GameBoard()
        >>> player_white = Player(1, board)
        >>> moves = player_white.generate_all_possible_moves()
        >>> print(len(moves))
        44
        """
        all_moves = []
        marbles = self.find_all_marbles()
        directions = list(self.board.DIRECTIONS.keys())

        # Generate all single and group moves
        for num_marbles in range(1, 4):  # From 1 marble up to 3 marbles
            for marble_group in combinations(marbles, num_marbles):
                for direction in directions:
                    move = Move(list(marble_group), direction)
                    try:
                        if move.is_valid(self.board):
                            all_moves.append(move)
                            #print(move.marbles, move.direction)
                    except InvalidMoveError:
                        continue

        return all_moves

    def minimax(self, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.board.is_game_over():
            return self.board.evaluate_board(self.color)

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in self.generate_all_possible_moves():
                # Save a copy of the board
                board_copy = np.copy(self.board.board)

                # Simulate the move
                move.apply(self.board)  # Assume move.apply() modifies the board directly
                eval = self.minimax(depth - 1, alpha, beta, False)

                # Restore the board from the copy
                self.board.board = board_copy

                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            opponent_color = 1 if self.color == 0 else 0
            opponent = Player(opponent_color, self.board)
            for move in opponent.generate_all_possible_moves():
                # Save a copy of the board
                board_copy = np.copy(self.board.board)

                # Simulate the move
                move.apply(self.board)  # Assume move.apply() modifies the board directly
                eval = self.minimax(depth - 1, alpha, beta, True)

                # Restore the board from the copy
                self.board.board = board_copy

                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def best_move(self, depth):
        best_score = float('-inf') if self.color == 1 else float('inf')
        best_move = None
        for move in self.generate_all_possible_moves():
            # Save a copy of the board
            board_copy = np.copy(self.board.board)

            # Simulate the move
            move.apply(self.board)  # Assume move.apply() modifies the board directly
            score = self.minimax(depth - 1, float('-inf'), float('inf'), False)

            # Restore the board from the copy
            self.board.board = board_copy

            # Update the best move and score
            if (self.color == 1 and score > best_score) or (self.color == 0 and score < best_score):
                best_score = score
                best_move = move

        return best_move