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

    def display_board(self):
        # Display the current state of the board
        print(self.board)

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

    # Example to get neighbors of a cell
    ex_row, ex_col = 5, 5
    ex_neighbors = game_board.get_neighbors(ex_row, ex_col)
    print("Neighbors of cell ({}, {}):".format(ex_row, ex_col))
    for direc, (n_row, n_col) in ex_neighbors.items():
        print(f"{direc}: ({n_row}, {n_col})")