import random
from game_board import GameBoard
from move import Move, InvalidMoveError
import numpy as np


class Player:
    def __init__(self, color, board):
        self.color = color  # Player's color (0 for black, 1 for white)
        self.board = board  # Reference to the game board

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
        marbles, direction = random_move.marbles, random_move.direction

        try:
            move = Move(marbles, direction)
            if move.apply(self.board):
                print(f"Move successful: {marbles} moved {direction}")
                return True
        except InvalidMoveError as e:
            print(f"Failed to apply the move: {e}")
            return False

        return False

    def generate_all_possible_moves(self):
        """Generate all valid moves for the current player."""
        all_moves = []
        marbles = self.find_all_marbles()
        directions = list(GameBoard.DIRECTIONS.keys())

        # Check moves for single marbles and combinations of 2 or 3 marbles if possible
        for marble in marbles:
            for direction in directions:
                # Check individual marble moves
                try:
                    move = Move([marble], direction)
                    if move.is_valid(self.board):
                        all_moves.append(move)
                except InvalidMoveError:
                    continue  # If the move is not valid, skip it

        # Check combinations of marbles (2 and 3 combinations)
        if len(marbles) > 1:
            from itertools import combinations
            for num_marbles in [2, 3]:  # Consider pairs and triplets of marbles
                for marble_group in combinations(marbles, num_marbles):
                    for direction in directions:
                        try:
                            move = Move(list(marble_group), direction)
                            if move.is_valid(self.board):
                                all_moves.append(move)
                        except InvalidMoveError:
                            continue  # If the move is not valid, skip it

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

# Example usage
if __name__ == '__main__':
    board = GameBoard()  # Create an instance of the GameBoard
    player_white = Player(1, board)  # Player 1, usually white marbles
    player_black = Player(0, board)  # Player 0, usually black marbles

    move_count = 0
    total_moves = 20

    print("Initial Board:")
    board.display_board()  # Display initial setup

    while move_count < total_moves:
        if move_count % 2 == 0:
            print(f"\nMove {move_count + 1} by Player Black:")
            if not player_black.random_move():  # Player black tries to make a move
                print("No valid moves available for Player Black.")
                break
        else:
            print(f"\nMove {move_count + 1} by Player White:")
            if not player_white.random_move():  # Player white tries to make a move
                print("No valid moves available for Player White.")
                break

        board.display_board()  # Display the board after each move
        move_count += 1
        if board.out[0] >= 6:
            print("White win")
            break
        elif board.out[1] >= 6:
            print("Black win")
            break
