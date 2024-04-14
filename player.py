import random
from game_board import GameBoard
from move import Move, InvalidMoveError


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
        """Generate and apply a random valid move."""
        marbles = self.find_all_marbles()
        directions = list(GameBoard.DIRECTIONS.keys())

        # Try up to 100 times to find a valid move
        for _ in range(100):
            random_marbles = random.sample(marbles, k=min(len(marbles), random.randint(1, 3)))  # Select 1-3 marbles
            random_direction = random.choice(directions)

            try:
                move = Move(random_marbles, random_direction)
                if move.apply(self.board):
                    print(f"Move successful: {random_marbles} moved {random_direction}")
                    return True
            except InvalidMoveError as e:
                continue  # If the move was invalid, try again
        print("Failed to make a valid move after 100 attempts.")
        return False


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
