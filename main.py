from game_board import GameBoard
from player import Player

def main_game_loop():
    # Initialize the game board
    board = GameBoard()

    # Create players
    player1 = Player(0, board)  # Assuming 0 is black
    player2 = Player(1, board)  # Assuming 1 is white

    # Decide the depth of the Minimax algorithm if using AI
    minimax_depth = 3

    # Game loop
    current_player = player1
    while not board.is_game_over():
        print("Current board:")
        board.display_board()

        # Decide if using AI or human player for the move
        if isinstance(current_player, Player):  # If AI
            print(f"Player {current_player.color}'s turn (AI):")
            move = current_player.best_move(minimax_depth)
            if move:
                move.apply(board)
            else:
                print("No valid moves available. Skipping turn.")
        else:
            # Assume human player implementation or another type of player
            pass

        # Check if the game has ended
        if board.is_game_over():
            break

        # Switch players
        current_player = player2 if current_player == player1 else player1

    # Determine the winner
    if board.out[0] >= 6:
        print("Game Over! Player 0 (Black) wins!")
    elif board.out[1] >= 6:
        print("Game Over! Player 1 (White) wins!")
    else:
        print("Game Over! It's a draw!")

    # Display final board
    print("Final board:")
    board.display_board()

if __name__ == "__main__":
    main_game_loop()
