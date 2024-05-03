from game_board import GameBoard
from player import Player

def main_game_loop():
    # Initialize the game board
    board = GameBoard()

    # Create players and choose strategy
    strategy_black = input("Choose strategy for Player Black ('minimax' or 'random'): ")
    strategy_white = input("Choose strategy for Player White ('minimax' or 'random'): ")
    player_black = Player(0, board, strategy=strategy_black)  # Black player
    player_white = Player(1, board, strategy=strategy_white)  # White player

    # Decide the depth of the Minimax algorithm if using AI
    minimax_depth = 2

    # Game loop
    current_player = player_black
    while not board.is_game_over():
        print("Current board:")
        board.display_board()

        # Get player name for display
        player_name = "Player Black" if current_player.color == 0 else "Player White"

        # Decide and apply move
        print(f"{player_name}'s turn:")
        move = current_player.choose_move(minimax_depth)
        if move:
            move.apply(board)
            board.update_out_counts()
            print(f"{player_name} played move from {move.marbles} to {move.direction}")
        else:
            print("No valid moves available. Skipping turn.")

        # Check if the game has ended
        if board.is_game_over():
            break

        # Switch players
        current_player = player_white if current_player == player_black else player_black

    # Determine the winner
    if board.out[0] >= 6:
        print("Game Over! Player Black wins!")
    elif board.out[1] >= 6:
        print("Game Over! Player White wins!")
    else:
        print("Game Over! It's a draw!")

    # Display final board
    print("Final board:")
    board.display_board()

if __name__ == "__main__":
    main_game_loop()