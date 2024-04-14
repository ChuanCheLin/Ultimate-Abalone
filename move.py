from game_board import GameBoard


class InvalidMoveError(Exception):
    """Custom exception class for invalid moves."""
    pass


class Move:
    def __init__(self, marbles, direction):
        self.marbles = self.sort_marbles(marbles, direction)  # A list of tuples representing the marbles' positions to be moved
        print(self.marbles)
        self.direction = direction

    def sort_marbles(self, marbles, direction):
        delta_row, delta_col = GameBoard.DIRECTIONS[direction]

        # Adjust sorting based on direction dynamics
        if delta_row != 0 and delta_col != 0:  # Diagonal movement
            return sorted(marbles, key=lambda x: (x[0] * delta_row, x[1] * delta_col))
        elif delta_row != 0:  # Vertical movement only
            return sorted(marbles, key=lambda x: x[0] * delta_row)
        else:  # Horizontal movement only
            return sorted(marbles, key=lambda x: x[1] * delta_col)

    def get_destination(self, game_board):
        """Get the destination positions for the marbles being moved."""
        destinations = []
        for marble in self.marbles:
            delta_row, delta_col = GameBoard.DIRECTIONS[self.direction]
            destination = (marble[0] + delta_row, marble[1] + delta_col)
            if not self._is_on_board(destination, game_board):
                return None  # One of the marbles would move off the board
            destinations.append(destination)
        return destinations

    def is_valid(self, game_board):
        """Check if the move is valid based on the game rules."""
        if not self.marbles:
            raise InvalidMoveError("No marbles selected for the move.")

        if len(self.marbles) > 3:
            raise InvalidMoveError("Cannot move more than three marbles at a time.")

        if self.direction not in GameBoard.DIRECTIONS:
            raise InvalidMoveError(f"Invalid direction: {self.direction}")

        destinations = self.get_destination(game_board)
        if not destinations:
            raise InvalidMoveError("Invalid move: One or more marbles would be moved off the board.")

        # Check for side-step move
        is_side_step = all(
            marble[0] - self.marbles[0][0] == marble[1] - self.marbles[0][1]
            for marble in self.marbles
        )
        if is_side_step:
            if not all(game_board.board[dest] == -1 for dest in destinations):
                raise InvalidMoveError("Invalid side-step: Destination positions are not all empty.")
        else:
            # Check for in-line move
            if any(game_board.board[marble] != game_board.board[self.marbles[0]] for marble in self.marbles):
                raise InvalidMoveError("Invalid in-line move: Not all marbles belong to the same player.")

            # Checking contiguity in is_valid method
            delta_row, delta_col = GameBoard.DIRECTIONS[self.direction]
            for i in range(len(self.marbles) - 1):
                expected_next_marble = (self.marbles[i][0] + delta_row, self.marbles[i][1] + delta_col)
                if expected_next_marble != self.marbles[i + 1]:
                    raise InvalidMoveError("Invalid in-line move: Marbles are not contiguous.")

            player_marble_count = len(self.marbles)
            opponent_marble_count = 0
            current_position = self.marbles[-1]

            while True:
                current_position = self.get_destination(game_board)[0]
                if not self._is_on_board(current_position, game_board):
                    break  # Reached the end of the board, or an empty space

                current_marble = game_board.board[current_position]
                if current_marble == -1 or current_marble == -2:
                    break  # Reached an empty space or the edge of the board
                if current_marble != game_board.board[self.marbles[0]]:
                    opponent_marble_count += 1
                    if opponent_marble_count >= player_marble_count:
                        raise InvalidMoveError("Invalid push: Numerical superiority not met for pushing.")
                else:
                    # Found a marble belonging to the player, so no push possible
                    if opponent_marble_count > 0:
                        raise InvalidMoveError(
                            "Invalid push: Friendly marble encountered before pushing all opponent marbles.")
                    break

        return True

    def apply(self, game_board):
        """Apply the move to the board."""
        if not self.is_valid(game_board):
            return False  # Invalid move

        destinations = self.get_destination(game_board)
        if not destinations:
            return False  # Invalid destinations

        # We need to ensure that marbles are moved without losing any during the update.
        # Start by moving marbles from the last to the first in the list to avoid overwriting
        # any marble that still needs to be moved.

        # Create temporary storage to hold new positions
        new_positions = {}
        for marble, destination in zip(self.marbles, destinations):
            new_positions[destination] = game_board.board[marble]

        # Now, apply the new positions to the board and clear the original positions
        for marble in self.marbles:
            game_board.board[marble] = -1  # Clear original position

        for destination, value in new_positions.items():
            game_board.board[destination] = value  # Set new position

        return True

    @staticmethod
    def _is_on_board(pos, game_board):
        """Check if a position is on the board."""
        rows, cols = game_board.board.shape
        return 0 <= pos[0] < rows and 0 <= pos[1] < cols and game_board.board[pos] != -2


# Example usage
if __name__ == '__main__':
    board = GameBoard()
    board.display_board()

    # Attempt an in-line move with two white marbles
    move = Move(marbles=[(1, 5), (2, 4)], direction='DOWN_LEFT')
    try:
        if move.apply(board):
            print("Move applied successfully.")
    except InvalidMoveError as e:
        print(f"Move was invalid: {e}")

    board.display_board()
