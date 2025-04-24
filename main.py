import argparse
import time
from board import GoBoard
from agents import StoneCountAgent, LibertyCountAgent, RandomAgent
from evaluators import StoneCountEvaluator, LibertyCountEvaluator
from game_analytics import GameAnalytics
from ui import GoGameUI

def agent_vs_agent(black_agent, white_agent, board_size=19, num_games=10, ui_enabled=True, analytics=None, fullscreen=False):
    """
    Run a series of games between two agents and collect statistics.
    
    Args:
        black_agent: Agent playing as black
        white_agent: Agent playing as white
        board_size (int): Size of the board
        num_games (int): Number of games to play
        ui_enabled (bool): Whether to enable the UI
        analytics (GameAnalytics, optional): Analytics object to record results
        fullscreen (bool): Whether to run the UI in fullscreen mode
    
    Returns:
        GameAnalytics: Analytics object with game results
    """
    if analytics is None:
        analytics = GameAnalytics()
    
    # Start with UI if enabled
    if ui_enabled:
        ui = GoGameUI(board_size, fullscreen)
        ui.set_agents(black_agent, white_agent)
        ui.auto_play = True
        ui.delay = 100  # Make the game play faster
        ui.run()
        
        # Record the result of the UI game
        winner = ui.board.get_winner()
        analytics.record_game_result(winner, [black_agent, white_agent])
        
        # Subtract 1 from num_games since we've played one game in the UI
        num_games -= 1
    
    # Play the remaining games without UI
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

def main():
    """Main function to run the Go game."""
    parser = argparse.ArgumentParser(description="Go Game with AI agents")
    parser.add_argument("--board-size", type=int, default=9, choices=[9, 13, 19], help="Board size (9, 13, or 19)")
    parser.add_argument("--num-games", type=int, default=10, help="Number of games to play")
    parser.add_argument("--depth", type=int, default=2, help="Search depth for agents")
    parser.add_argument("--no-ui", action="store_true", help="Disable UI and run games in console only")
    parser.add_argument("--plot", action="store_true", help="Plot analytics after games")
    parser.add_argument("--save-plots", type=str, help="Directory to save plot images")
    parser.add_argument("--fullscreen", action="store_true", help="Run the game in fullscreen mode")
    args = parser.parse_args()
    
    # Create agents
    black_agent = StoneCountAgent(GoBoard.BLACK, args.depth)
    white_agent = LibertyCountAgent(GoBoard.WHITE, args.depth)
    
    # Create analytics
    analytics = GameAnalytics()
    
    # Run the games
    analytics = agent_vs_agent(
        black_agent,
        white_agent,
        board_size=args.board_size,
        num_games=args.num_games,
        ui_enabled=not args.no_ui,
        analytics=analytics,
        fullscreen=args.fullscreen
    )
    
    # Print summary
    analytics.print_summary()
    
    # Plot results if requested
    if args.plot or args.save_plots:
        analytics.plot_metrics(args.save_plots)

if __name__ == "__main__":
    main()