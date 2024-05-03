import numpy as np


class GameBoard:
    # Class attribute for the directions
    DIRECTIONS = {
        'LEFT': (0, -1),
        'RIGHT': (0, 1),
        'UP_LEFT': (-1, 0),
        'UP_RIGHT': (-1, 1),
        'DOWN_LEFT': (1, -1),
        'DOWN_RIGHT': (1, 0)
    }

    WEIGHTS = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0],
        [0, 0, 0, 0, 1, 2, 3, 3, 2, 1, 0],
        [0, 0, 0, 1, 2, 3, 4, 3, 2, 1, 0],
        [0, 0, 1, 2, 3, 4, 4, 3, 2, 1, 0],
        [0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0],
        [0, 1, 2, 3, 4, 4, 3, 2, 1, 0, 0],
        [0, 1, 2, 3, 4, 3, 2, 1, 0, 0, 0],
        [0, 1, 2, 3, 3, 2, 1, 0, 0, 0, 0],
        [0, 1, 2, 3, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])

    def __init__(self):
        # Initialize the board
        # -1 stands for empty, -2 stands for void
        # 0 stands for black, 1 stands for white
        self.board = np.array([
            [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
            [-2, -2, -2, -2, -2,  1,  1,  1,  1,  1, -2],
            [-2, -2, -2, -2,  1,  1,  1,  1,  1,  1, -2],
            [-2, -2, -2, -1, -1,  1,  1,  1, -1, -1, -2],
            [-2, -2, -1, -1, -1, -1, -1, -1, -1, -1, -2],
            [-2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2],
            [-2, -1, -1, -1, -1, -1, -1, -1, -1, -2, -2],
            [-2, -1, -1,  0,  0,  0, -1, -1, -2, -2, -2],
            [-2,  0,  0,  0,  0,  0,  0, -2, -2, -2, -2],
            [-2,  0,  0,  0,  0,  0, -2, -2, -2, -2, -2],
            [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2]
        ])
        self.out = [0, 0] # [Black, White] The number of abalones are push out of board.

    def update_out_counts(self):
        """Updates the count of marbles pushed out of the board by checking the current board state."""
        # Initialize counts for black and white marbles
        count_black = 0
        count_white = 0

        # Counting the marbles based on the typical board values for black (0) and white (1)
        for row in self.board:
            for cell in row:
                if cell == 0:
                    count_black += 1
                elif cell == 1:
                    count_white += 1

        # Update the out counts based on the total marbles minus the ones on the board
        # Assuming the total starting marbles per player were initially known, adjust accordingly
        total_marbles_per_player = 14  # Change this based on your game's initial settings
        self.out[0] = total_marbles_per_player - count_black  # Black marbles pushed out
        self.out[1] = total_marbles_per_player - count_white

    def is_game_over(self):
        """
        Check if the game is over based on the number of marbles each player has pushed out.

        Returns:
        bool: True if the game is over (if any player has pushed out a sufficient number of marbles), otherwise False.
        """
        # Assuming the game ends when a player pushes out 6 or more marbles
        # This threshold can be adjusted according to your game's rules
        winning_count = 6
        if self.out[0] >= winning_count or self.out[1] >= winning_count:
            return True
        return False

    # def simulate_move(self, move):
    #     """
    #     Simulate a move on the board, and return the necessary information to undo it.
    #
    #     Args:
    #     move (Move): The move to simulate.
    #
    #     Returns:
    #     tuple: A tuple containing the original positions and their values, and the destination positions.
    #     """
    #     original_positions = {marble: self.board[marble] for marble in move.marbles}
    #     move.apply(self)  # Apply the move to change the board
    #     # print("Board after simulate:", self.display_board())
    #     return original_positions, move.marbles  # Store original positions and their states to revert later

    # def undo_move(self, original_positions, marbles):
    #     """
    #     Undo a move using the original positions and values.
    #
    #     Args:
    #     original_positions (dict): A dictionary of positions (tuple) and their original values (int).
    #     marbles (list): The list of marbles moved.
    #     """
    #     # Reset the board positions to their original state
    #     for position, value in original_positions.items():
    #         self.board[position] = value
    #
    #     # Clear the new positions where marbles were moved to
    #     for marble in marbles:
    #         self.board[marble] = -1  # Assuming -1 is the value for an empty space
    #
    #     # print("Board after undo:", self.display_board())

    #TODO: The Heuristic Function
    def evaluate_board(self, player_color):
        """
        Evaluate the game board from the perspective of the given player,
        taking positional strength into consideration.

        Args:
        player_color (int): The color of the player for whom to evaluate the board,
                            where 0 represents black and 1 represents white.

        Returns:
        int: The evaluation score, where a positive score is good for the player_color.
        """
        score = 0

        # # Evaluate positional strength and marbles on the board
        # for i in range(self.board.shape[0]):
        #     for j in range(self.board.shape[1]):
        #         if self.board[i][j] == 0:  # Black marble
        #             score_black += self.WEIGHTS[i][j]
        #         elif self.board[i][j] == 1:  # White marble
        #             score_white += self.WEIGHTS[i][j]

        # Add score for marbles pushed off the board
        # Assuming pushing off a marble scores an additional 10 points
        self.update_out_counts()
        score -= self.out[1] * 10  # Score for black based on white marbles pushed out
        score += self.out[0] * 10  # Score for white based on black marbles pushed out

        return score

    def display_board(self):
        # Display the current state of the board in a hexagonal shape
        board_representation = ""
        # Determine the maximum number of spaces needed at the beginning of the top row
        max_offset = len(self.board) - 1
        for i, row in enumerate(self.board):
            # Calculate the offset for the current row to center the hexagon
            offset = abs(i - max_offset // 2)
            # Add leading spaces to stagger the rows and create a hexagonal effect
            board_representation += " " * offset
            for cell in row:
                if cell == -2:  # Void space
                    continue  # Skip void spaces, they are just placeholders
                elif cell == -1:  # Empty space
                    board_representation += ". "  # Display dot and space
                elif cell == 0:  # Black marble
                    board_representation += "B "  # Display 'B' and space
                elif cell == 1:  # White marble
                    board_representation += "W "  # Display 'W' and space
            board_representation += "\n"
            # print(board_representation)
        print(board_representation.rstrip())  # Strip the last newline for clean output
        # Display the count of abalones pushed out of the board
        print("Abalones out of board - Black: {}, White: {}".format(self.out[0], self.out[1]))

    def get_neighbors(self, row, col):
        """Get the neighboring cells of a given cell at (row, col)."""
        neighbors = {}
        for direction, (d_row, d_col) in GameBoard.DIRECTIONS.items():
            neighbor_row, neighbor_col = row + d_row, col + d_col
            # Check if the neighbor is within the bounds of the board
            if (0 <= neighbor_row < self.board.shape[0] and
                    0 <= neighbor_col < self.board.shape[1]):
                neighbors[direction] = (neighbor_row, neighbor_col)
        return neighbors


# Example usage
if __name__ == "__main__":
    game_board = GameBoard()
    game_board.display_board()