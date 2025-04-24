import argparse
import os
from board import GoBoard
from agents import StoneCountAgent, LibertyCountAgent, RandomAgent
from game_analytics import GameAnalytics
import matplotlib.pyplot as plt
import numpy as np
import time

def run_tournament(board_sizes=[9, 13, 19], num_games=10, depth=2, save_dir=None):
    """
    Run a tournament between agents on different board sizes.
    
    Args:
        board_sizes (list): List of board sizes to test
        num_games (int): Number of games to play for each configuration
        depth (int): Search depth for agents
        save_dir (str, optional): Directory to save plot images
    """
    # Create save directory if needed
    if save_dir is not None:
        os.makedirs(save_dir, exist_ok=True)
    
    # Tournament results
    results = {
        'stone_count_wins': [],
        'liberty_count_wins': [],
        'draws': [],
        'stone_count_time': [],
        'liberty_count_time': [],
        'stone_count_memory': [],
        'liberty_count_memory': []
    }
    
    # Run tournament for each board size
    for board_size in board_sizes:
        print(f"\n=== Running tournament on {board_size}x{board_size} board ===")
        
        # Create agents
        stone_count_black = StoneCountAgent(GoBoard.BLACK, depth)
        liberty_count_white = LibertyCountAgent(GoBoard.WHITE, depth)
        
        # Play games
        print(f"Playing {num_games} games: Stone Count (Black) vs Liberty Count (White)")
        analytics1 = play_games(stone_count_black, liberty_count_white, board_size, num_games)
        
        # Switch colors and play games again
        print(f"Playing {num_games} games: Liberty Count (Black) vs Stone Count (White)")
        liberty_count_black = LibertyCountAgent(GoBoard.BLACK, depth)
        stone_count_white = StoneCountAgent(GoBoard.WHITE, depth)
        analytics2 = play_games(liberty_count_black, stone_count_white, board_size, num_games)
        
        # Combine results
        stone_count_wins = (
            analytics1.results['wins'].get('Stone Count Agent', 0) +
            analytics2.results['wins'].get('Stone Count Agent', 0)
        )
        liberty_count_wins = (
            analytics1.results['wins'].get('Liberty Count Agent', 0) +
            analytics2.results['wins'].get('Liberty Count Agent', 0)
        )
        
        # Get time and memory usage
        stone_count_time = (
            np.mean(analytics1.results['times'].get('Stone Count Agent', [0])) +
            np.mean(analytics2.results['times'].get('Stone Count Agent', [0]))
        ) / 2
        
        liberty_count_time = (
            np.mean(analytics1.results['times'].get('Liberty Count Agent', [0])) +
            np.mean(analytics2.results['times'].get('Liberty Count Agent', [0]))
        ) / 2
        
        stone_count_memory = (
            np.mean(analytics1.results['memory'].get('Stone Count Agent', [0])) +
            np.mean(analytics2.results['memory'].get('Stone Count Agent', [0]))
        ) / 2
        
        liberty_count_memory = (
            np.mean(analytics1.results['memory'].get('Liberty Count Agent', [0])) +
            np.mean(analytics2.results['memory'].get('Liberty Count Agent', [0]))
        ) / 2
        
        # Calculate draws
        total_games = analytics1.results['total_games'] + analytics2.results['total_games']
        draws = total_games - stone_count_wins - liberty_count_wins
        
        # Store results
        results['stone_count_wins'].append(stone_count_wins)
        results['liberty_count_wins'].append(liberty_count_wins)
        results['draws'].append(draws)
        results['stone_count_time'].append(stone_count_time)
        results['liberty_count_time'].append(liberty_count_time)
        results['stone_count_memory'].append(stone_count_memory)
        results['liberty_count_memory'].append(liberty_count_memory)
        
        # Print tournament summary for this board size
        print(f"\n=== Tournament Results for {board_size}x{board_size} board ===")
        print(f"Total Games: {total_games}")
        print(f"Stone Count Agent wins: {stone_count_wins} ({stone_count_wins/total_games:.2%})")
        print(f"Liberty Count Agent wins: {liberty_count_wins} ({liberty_count_wins/total_games:.2%})")
        print(f"Draws: {draws} ({draws/total_games:.2%})")
        print(f"Average time per move:")
        print(f"  Stone Count Agent: {stone_count_time:.4f} seconds")
        print(f"  Liberty Count Agent: {liberty_count_time:.4f} seconds")
        print(f"Average memory usage per move:")
        print(f"  Stone Count Agent: {stone_count_memory:.2f} MB")
        print(f"  Liberty Count Agent: {liberty_count_memory:.2f} MB")
    
    # Plot tournament results
    plot_tournament_results(board_sizes, results, save_dir)

def play_games(black_agent, white_agent, board_size, num_games):
    """
    Play a series of games between two agents without UI.
    
    Args:
        black_agent: Agent playing as black
        white_agent: Agent playing as white
        board_size (int): Size of the board
        num_games (int): Number of games to play
    
    Returns:
        GameAnalytics: Analytics object with game results
    """
    analytics = GameAnalytics()
    
    for i in range(num_games):
        board = GoBoard(board_size)
        
        # Reset agents for the new game
        black_agent.reset_metrics()
        white_agent.reset_metrics()
        
        # Play the game
        while not board.is_game_over():
            if board.current_player == GoBoard.BLACK:
                move = black_agent.get_move(board)
            else:
                move = white_agent.get_move(board)
            
            if move:
                board.play_move(*move)
        
        # Record the result
        winner = board.get_winner()
        analytics.record_game_result(winner, [black_agent, white_agent])
        
        # Print progress
        print(f"Game {i+1}/{num_games} completed")
    
    return analytics

def plot_tournament_results(board_sizes, results, save_dir=None):
    """
    Plot tournament results.
    
    Args:
        board_sizes (list): List of board sizes
        results (dict): Tournament results
        save_dir (str, optional): Directory to save plot images
    """
    # Convert board sizes to strings for plotting
    board_size_labels = [f"{size}x{size}" for size in board_sizes]
    
    # Plot win rates
    plt.figure(figsize=(12, 6))
    bar_width = 0.25
    index = np.arange(len(board_sizes))
    
    # Calculate total games for each board size
    total_games = [s + l + d for s, l, d in zip(
        results['stone_count_wins'],
        results['liberty_count_wins'],
        results['draws']
    )]
    
    # Calculate win rates
    stone_count_win_rates = [s / t for s, t in zip(results['stone_count_wins'], total_games)]
    liberty_count_win_rates = [l / t for l, t in zip(results['liberty_count_wins'], total_games)]
    draw_rates = [d / t for d, t in zip(results['draws'], total_games)]
    
    # Plot bars
    plt.bar(index - bar_width, stone_count_win_rates, bar_width, label='Stone Count Agent')
    plt.bar(index, liberty_count_win_rates, bar_width, label='Liberty Count Agent')
    plt.bar(index + bar_width, draw_rates, bar_width, label='Draws')
    
    plt.xlabel('Board Size')
    plt.ylabel('Win Rate')
    plt.title('Agent Win Rates by Board Size')
    plt.xticks(index, board_size_labels)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    if save_dir:
        plt.savefig(os.path.join(save_dir, 'win_rates_by_board_size.png'))
    else:
        plt.show()
    
    # Plot time
    plt.figure(figsize=(12, 6))
    plt.bar(index - bar_width/2, results['stone_count_time'], bar_width, label='Stone Count Agent')
    plt.bar(index + bar_width/2, results['liberty_count_time'], bar_width, label='Liberty Count Agent')
    
    plt.xlabel('Board Size')
    plt.ylabel('Average Time per Move (seconds)')
    plt.title('Agent Performance: Time per Move')
    plt.xticks(index, board_size_labels)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    if save_dir:
        plt.savefig(os.path.join(save_dir, 'time_by_board_size.png'))
    else:
        plt.show()
    
    # Plot memory
    plt.figure(figsize=(12, 6))
    plt.bar(index - bar_width/2, results['stone_count_memory'], bar_width, label='Stone Count Agent')
    plt.bar(index + bar_width/2, results['liberty_count_memory'], bar_width, label='Liberty Count Agent')
    
    plt.xlabel('Board Size')
    plt.ylabel('Average Memory Usage per Move (MB)')
    plt.title('Agent Performance: Memory Usage')
    plt.xticks(index, board_size_labels)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    if save_dir:
        plt.savefig(os.path.join(save_dir, 'memory_by_board_size.png'))
        plt.close()
    else:
        plt.show()

def main():
    """Main function to run the tournament."""
    parser = argparse.ArgumentParser(description="Go Agent Tournament")
    parser.add_argument("--board-sizes", type=int, nargs="+", default=[9, 13, 19], help="Board sizes to test")
    parser.add_argument("--num-games", type=int, default=5, help="Number of games to play for each configuration")
    parser.add_argument("--depth", type=int, default=2, help="Search depth for agents")
    parser.add_argument("--save-dir", type=str, help="Directory to save plot images")
    args = parser.parse_args()
    
    # Validate board sizes
    board_sizes = [s for s in args.board_sizes if s in [9, 13, 19]]
    if not board_sizes:
        board_sizes = [9]
        print("Warning: Invalid board sizes. Using default size 9.")
    
    start_time = time.time()
    
    # Run the tournament
    run_tournament(
        board_sizes=board_sizes,
        num_games=args.num_games,
        depth=args.depth,
        save_dir=args.save_dir
    )
    
    total_time = time.time() - start_time
    print(f"\nTournament completed in {total_time:.2f} seconds")

if __name__ == "__main__":
    main()