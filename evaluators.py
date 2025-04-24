from board import GoBoard

class StoneCountEvaluator:
    """
    Evaluation function based on counting stones on the board.
    Evaluates a board state by looking at the difference between the number of stones.
    """
    
    def __init__(self, player_color):
        """
        Initialize the evaluator.
        
        Args:
            player_color (int): The color of the player (GoBoard.BLACK or GoBoard.WHITE)
        """
        self.player_color = player_color
        self.opponent_color = GoBoard.WHITE if player_color == GoBoard.BLACK else GoBoard.BLACK
    
    def evaluate(self, board):
        """
        Evaluate the board state.
        
        Args:
            board (GoBoard): The board to evaluate
            
        Returns:
            float: The evaluation score (higher is better for the player)
        """
        stone_count = board.count_stones()
        
        # Calculate total stones for each player
        player_stones = stone_count[self.player_color]
        opponent_stones = stone_count[self.opponent_color]
        
        # Add captured stones to the score
        player_stones += board.captured_stones[self.player_color]
        opponent_stones += board.captured_stones[self.opponent_color]
        
        # Return the difference - higher is better for the player
        return player_stones - opponent_stones

class LibertyCountEvaluator:
    """
    Evaluation function based on counting liberties of stones.
    Evaluates a board state by looking at the total liberties of each player's stones.
    More liberties means more flexibility and stronger positions.
    """
    
    def __init__(self, player_color):
        """
        Initialize the evaluator.
        
        Args:
            player_color (int): The color of the player (GoBoard.BLACK or GoBoard.WHITE)
        """
        self.player_color = player_color
        self.opponent_color = GoBoard.WHITE if player_color == GoBoard.BLACK else GoBoard.BLACK
    
    def evaluate(self, board):
        """
        Evaluate the board state.
        
        Args:
            board (GoBoard): The board to evaluate
            
        Returns:
            float: The evaluation score (higher is better for the player)
        """
        player_liberties = 0
        opponent_liberties = 0
        
        # Count liberties for each group
        counted_groups = set()
        
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x, y] != GoBoard.EMPTY and (x, y) not in counted_groups:
                    # Get the group and its liberties
                    group = board.get_group(x, y)
                    liberties = len(board.get_liberties(x, y))
                    
                    # Add the point to the counted groups
                    counted_groups.update(group)
                    
                    # Add liberties to the appropriate counter
                    if board.board[x, y] == self.player_color:
                        player_liberties += liberties
                    else:
                        opponent_liberties += liberties
        
        # Consider captured stones in the evaluation
        player_captures = board.captured_stones[self.player_color]
        opponent_captures = board.captured_stones[self.opponent_color]
        
        # Return the weighted combination of liberties and captures
        # The formula gives higher value to liberties (mobility) and captured stones
        return (player_liberties - opponent_liberties) + 3 * (player_captures - opponent_captures)

class TerritoryEvaluator:
    """
    Additional evaluation function that considers territory control.
    This can be combined with other evaluators for more sophisticated agents.
    """
    
    def __init__(self, player_color):
        """
        Initialize the evaluator.
        
        Args:
            player_color (int): The color of the player (GoBoard.BLACK or GoBoard.WHITE)
        """
        self.player_color = player_color
        self.opponent_color = GoBoard.WHITE if player_color == GoBoard.BLACK else GoBoard.BLACK
    
    def evaluate(self, board):
        """
        Evaluate the board state based on territory.
        
        Args:
            board (GoBoard): The board to evaluate
            
        Returns:
            float: The evaluation score (higher is better for the player)
        """
        # Get territory for each player
        territory = board.count_territory()
        
        # Return the territory difference
        return territory[self.player_color] - territory[self.opponent_color]