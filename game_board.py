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