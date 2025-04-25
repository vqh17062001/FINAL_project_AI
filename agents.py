import time
import random
import psutil
import os
from copy import deepcopy

class GoAgent:
    """
    Base class for AI agents playing Go.
    """
    
    def __init__(self, color, evaluator, search_depth=2, name="GoAgent"):
        """
        Initialize the agent.
        
        Args:
            color (int): The color of the agent (GoBoard.BLACK or GoBoard.WHITE)
            evaluator: The evaluation function to use
            search_depth (int): The search depth for the minimax algorithm
            name (str): The name of the agent
        """
        self.color = color
        self.evaluator = evaluator
        self.search_depth = search_depth
        self.name = name
        
        # Performance metrics
        self.total_moves = 0
        self.total_time = 0
        self.total_memory = 0
    
    def get_move(self, board):
        """
        Get the best move for the current board state.
        
        Args:
            board: The current board state
            
        Returns:
            tuple: The chosen move (x, y)
        """
        # Track time and memory usage
        start_time = time.time()
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Get the move
        move = self._get_move(board)
        
        # Update performance metrics
        end_time = time.time()
        end_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        self.total_moves += 1
        self.total_time += (end_time - start_time)
        
        # Đảm bảo chỉ cộng giá trị dương vào total_memory
        memory_used = max(0, end_memory - start_memory)
        self.total_memory += memory_used
        
        return move
    
    def _get_move(self, board):
        """
        Abstract method to be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_average_time(self):
        """Get average time per move in seconds."""
        if self.total_moves == 0:
            return 0
        return self.total_time / self.total_moves
    
    def get_average_memory(self):
        """Get average memory usage per move in MB."""
        if self.total_moves == 0:
            return 0
        return self.total_memory / self.total_moves
    
    def get_total_memory(self):
        """Get total memory usage in MB."""
        return self.total_memory
    
    def reset_metrics(self):
        """Reset performance metrics."""
        self.total_moves = 0
        self.total_time = 0
        self.total_memory = 0

class MinimaxAgent(GoAgent):
    """
    Go agent using the Minimax algorithm with Alpha-Beta pruning.
    """
    
    def __init__(self, color, evaluator, search_depth=2, name="MinimaxAgent"):
        """
        Initialize the Minimax agent.
        
        Args:
            color (int): The color of the agent (GoBoard.BLACK or GoBoard.WHITE)
            evaluator: The evaluation function to use
            search_depth (int): The search depth for the minimax algorithm
            name (str): The name of the agent
        """
        super().__init__(color, evaluator, search_depth, name)
    
    def _get_move(self, board):
        """
        Get the best move using the Minimax algorithm with Alpha-Beta pruning.
        
        Args:
            board: The current board state
            
        Returns:
            tuple: The chosen move (x, y)
        """
        # Check if it's this agent's turn
        if board.current_player != self.color:
            return None
        
        # Get valid moves
        valid_moves = board.get_valid_moves()
        
        # If no valid moves, pass
        if not valid_moves:
            return (-1, -1)  # Pass
        
        # Shuffle moves to add variety to gameplay
        random.shuffle(valid_moves)
        
        # Use Alpha-Beta search to find the best move
        best_score = float('-inf')
        best_move = None
        
        for move in valid_moves:
            # Make a deep copy of the board
            board_copy = deepcopy(board)
            
            # Make the move
            x, y = move
            board_copy.play_move(x, y)
            
            # Get the score for this move
            score = self._min_value(board_copy, 1, float('-inf'), float('inf'))
            
            # Update the best move if needed
            if score > best_score:
                best_score = score
                best_move = move
        
        # If we couldn't find a good move, just play randomly
        if best_move is None and valid_moves:
            best_move = random.choice(valid_moves)
        
        return best_move
    
    def _max_value(self, board, depth, alpha, beta):
        """
        Maximizing function for the Minimax algorithm.
        
        Args:
            board: The current board state
            depth: The current depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            
        Returns:
            float: The best score for the maximizing player
        """
        # Check if the game is over or we've reached the maximum depth
        if board.is_game_over() or depth >= self.search_depth:
            return self.evaluator.evaluate(board)
        
        # Get valid moves
        valid_moves = board.get_valid_moves()
        
        # If no valid moves, pass
        if not valid_moves:
            board_copy = deepcopy(board)
            board_copy.play_move(-1, -1)  # Pass
            return self._min_value(board_copy, depth + 1, alpha, beta)
        
        # Initialize the best score
        best_score = float('-inf')
        
        # Try each move
        for move in valid_moves:
            # Make a deep copy of the board
            board_copy = deepcopy(board)
            
            # Make the move
            x, y = move
            board_copy.play_move(x, y)
            
            # Get the score for this move
            score = self._min_value(board_copy, depth + 1, alpha, beta)
            
            # Update the best score
            best_score = max(best_score, score)
            
            # Alpha-Beta pruning
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        
        return best_score
    
    def _min_value(self, board, depth, alpha, beta):
        """
        Minimizing function for the Minimax algorithm.
        
        Args:
            board: The current board state
            depth: The current depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            
        Returns:
            float: The best score for the minimizing player
        """
        # Check if the game is over or we've reached the maximum depth
        if board.is_game_over() or depth >= self.search_depth:
            return self.evaluator.evaluate(board)
        
        # Get valid moves
        valid_moves = board.get_valid_moves()
        
        # If no valid moves, pass
        if not valid_moves:
            board_copy = deepcopy(board)
            board_copy.play_move(-1, -1)  # Pass
            return self._max_value(board_copy, depth + 1, alpha, beta)
        
        # Initialize the best score
        best_score = float('inf')
        
        # Try each move
        for move in valid_moves:
            # Make a deep copy of the board
            board_copy = deepcopy(board)
            
            # Make the move
            x, y = move
            board_copy.play_move(x, y)
            
            # Get the score for this move
            score = self._max_value(board_copy, depth + 1, alpha, beta)
            
            # Update the best score
            best_score = min(best_score, score)
            
            # Alpha-Beta pruning
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        
        return best_score

class RandomAgent(GoAgent):
    """
    Go agent that plays random moves.
    Useful for testing.
    """
    
    def __init__(self, color, name="RandomAgent"):
        """
        Initialize the random agent.
        
        Args:
            color (int): The color of the agent (GoBoard.BLACK or GoBoard.WHITE)
            name (str): The name of the agent
        """
        # Pass a dummy evaluator
        super().__init__(color, None, 0, name)
    
    def _get_move(self, board):
        """
        Get a random move.
        
        Args:
            board: The current board state
            
        Returns:
            tuple: The chosen move (x, y)
        """
        # Check if it's this agent's turn
        if board.current_player != self.color:
            return None
        
        # Get valid moves
        valid_moves = board.get_valid_moves()
        
        # If no valid moves, pass
        if not valid_moves:
            return (-1, -1)  # Pass
        
        # Choose a random move
        return random.choice(valid_moves)

class StoneCountAgent(MinimaxAgent):
    """
    Go agent using the Minimax algorithm with Stone Count evaluation.
    """
    
    def __init__(self, color, search_depth=2):
        """
        Initialize the Stone Count agent.
        
        Args:
            color (int): The color of the agent (GoBoard.BLACK or GoBoard.WHITE)
            search_depth (int): The search depth for the minimax algorithm
        """
        from evaluators import StoneCountEvaluator
        evaluator = StoneCountEvaluator(color)
        super().__init__(color, evaluator, search_depth, "Stone Count Agent")

class LibertyCountAgent(MinimaxAgent):
    """
    Go agent using the Minimax algorithm with Liberty Count evaluation.
    """
    
    def __init__(self, color, search_depth=2):
        """
        Initialize the Liberty Count agent.
        
        Args:
            color (int): The color of the agent (GoBoard.BLACK or GoBoard.WHITE)
            search_depth (int): The search depth for the minimax algorithm
        """
        from evaluators import LibertyCountEvaluator
        evaluator = LibertyCountEvaluator(color)
        super().__init__(color, evaluator, search_depth, "Liberty Count Agent")