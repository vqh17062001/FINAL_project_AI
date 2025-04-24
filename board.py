import numpy as np

class GoBoard:
    """
    Representation of the Go board with game rules implementation.
    """
    
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    
    def __init__(self, size=19):
        """
        Initialize a Go board with the given size.
        
        Args:
            size (int): Board size (9, 13, or 19)
        """
        if size not in [9, 13, 19]:
            raise ValueError("Board size must be 9, 13, or 19")
        
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.current_player = self.BLACK
        self.ko_point = None
        self.move_history = []
        self.captured_stones = {self.BLACK: 0, self.WHITE: 0}
        self.pass_count = 0
    
    def reset(self):
        """Reset the board to the initial state."""
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.current_player = self.BLACK
        self.ko_point = None
        self.move_history = []
        self.captured_stones = {self.BLACK: 0, self.WHITE: 0}
        self.pass_count = 0
    
    def is_on_board(self, x, y):
        """Check if the coordinates are within the board."""
        return 0 <= x < self.size and 0 <= y < self.size
    
    def get_adjacent_points(self, x, y):
        """Get adjacent points (up, right, down, left)."""
        adjacent = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if self.is_on_board(nx, ny):
                adjacent.append((nx, ny))
        return adjacent
    
    def get_group(self, x, y):
        """Get all stones in the connected group at (x, y)."""
        if not self.is_on_board(x, y) or self.board[x, y] == self.EMPTY:
            return set()
        
        color = self.board[x, y]
        group = set([(x, y)])
        frontier = [(x, y)]
        
        while frontier:
            stone_x, stone_y = frontier.pop()
            for nx, ny in self.get_adjacent_points(stone_x, stone_y):
                if self.board[nx, ny] == color and (nx, ny) not in group:
                    group.add((nx, ny))
                    frontier.append((nx, ny))
        
        return group
    
    def get_liberties(self, x, y):
        """Get all liberties of the stone group at (x, y)."""
        if not self.is_on_board(x, y) or self.board[x, y] == self.EMPTY:
            return set()
        
        group = self.get_group(x, y)
        liberties = set()
        
        for stone_x, stone_y in group:
            for nx, ny in self.get_adjacent_points(stone_x, stone_y):
                if self.board[nx, ny] == self.EMPTY:
                    liberties.add((nx, ny))
        
        return liberties
    
    def count_liberties(self, x, y):
        """Count the number of liberties of the stone group at (x, y)."""
        return len(self.get_liberties(x, y))
    
    def remove_group(self, x, y):
        """Remove a group of stones from the board and return the number removed."""
        group = self.get_group(x, y)
        for stone_x, stone_y in group:
            self.board[stone_x, stone_y] = self.EMPTY
        return len(group)
    
    def would_be_suicide(self, x, y, color):
        """Check if placing a stone at (x, y) would be suicide."""
        # Make a copy of the board to simulate the move
        board_copy = self.board.copy()
        board_copy[x, y] = color
        
        # Check if the placed stone would have liberties
        if self._has_liberties_in_copy(board_copy, x, y):
            return False
        
        # Check if the move would capture any opponent stones
        opponent = self.WHITE if color == self.BLACK else self.BLACK
        for nx, ny in self.get_adjacent_points(x, y):
            if board_copy[nx, ny] == opponent:
                if not self._has_liberties_in_copy(board_copy, nx, ny):
                    return False  # Capturing opponent's stones, not suicide
        
        return True  # The move would be suicide
    
    def _has_liberties_in_copy(self, board_copy, x, y):
        """Check if a stone in the board copy has liberties."""
        if board_copy[x, y] == self.EMPTY:
            return False
        
        color = board_copy[x, y]
        visited = set([(x, y)])
        frontier = [(x, y)]
        
        while frontier:
            stone_x, stone_y = frontier.pop()
            for nx, ny in self.get_adjacent_points(stone_x, stone_y):
                if board_copy[nx, ny] == self.EMPTY:
                    return True  # Found a liberty
                if board_copy[nx, ny] == color and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    frontier.append((nx, ny))
        
        return False  # No liberties found
    
    def is_ko(self, x, y):
        """Check if the move would violate the ko rule."""
        return self.ko_point == (x, y)
    
    def is_valid_move(self, x, y):
        """Check if placing a stone at (x, y) is a valid move."""
        # Check if the point is on the board
        if not self.is_on_board(x, y):
            return False
        
        # Check if the point is empty
        if self.board[x, y] != self.EMPTY:
            return False
        
        # Check for ko rule
        if self.is_ko(x, y):
            return False
        
        # Check for suicide rule
        if self.would_be_suicide(x, y, self.current_player):
            return False
        
        return True
    
    def get_valid_moves(self):
        """Get all valid moves for the current player."""
        valid_moves = []
        for x in range(self.size):
            for y in range(self.size):
                if self.is_valid_move(x, y):
                    valid_moves.append((x, y))
        return valid_moves
    
    def play_move(self, x, y):
        """Play a move at the given coordinates."""
        # Handle passing
        if x == -1 and y == -1:
            self.pass_count += 1
            self.move_history.append((-1, -1))
            self.current_player = self.WHITE if self.current_player == self.BLACK else self.BLACK
            self.ko_point = None
            return True
        
        # Reset pass count when a player places a stone
        self.pass_count = 0
        
        # Check if the move is valid
        if not self.is_valid_move(x, y):
            return False
        
        # Place the stone
        self.board[x, y] = self.current_player
        self.move_history.append((x, y))
        
        # Check for captures
        opponent = self.WHITE if self.current_player == self.BLACK else self.BLACK
        captured_stones = 0
        potential_ko_point = None
        
        for nx, ny in self.get_adjacent_points(x, y):
            if self.board[nx, ny] == opponent:
                if self.count_liberties(nx, ny) == 0:
                    # If we capture only one stone, it might lead to a ko
                    group = self.get_group(nx, ny)
                    if len(group) == 1:
                        potential_ko_point = next(iter(group))
                    
                    captured = self.remove_group(nx, ny)
                    captured_stones += captured
                    self.captured_stones[self.current_player] += captured
        
        # Ko rule detection
        if captured_stones == 1 and potential_ko_point is not None:
            # Check if the move captured exactly one stone and if placing back would capture
            # the stone just played (ko situation)
            px, py = potential_ko_point
            self.ko_point = (px, py) if self.count_liberties(x, y) == 1 else None
        else:
            self.ko_point = None
        
        # Switch player
        self.current_player = self.WHITE if self.current_player == self.BLACK else self.BLACK
        
        return True
    
    def is_game_over(self):
        """
        Check if the game is over.
        Game ends when:
        1. Two consecutive passes
        2. One player has a significant advantage (more than 60% of the board)
        3. The game has gone on for too long (>150 moves for 19x19, scaled for other sizes)
        """
        # Condition 1: Two consecutive passes
        if self.pass_count >= 2:
            return True
        
        # Condition 2: Check for overwhelming advantage
        stone_count = self.count_stones()
        black_count = stone_count[self.BLACK]
        white_count = stone_count[self.WHITE]
        total_stones = black_count + white_count
        
        # If the board is at least 1/3 filled and one player has more than 60% of the stones
        if total_stones >= (self.size * self.size) / 3:
            if black_count > 0 and white_count > 0:  # Ensure both players have some stones
                black_percentage = black_count / total_stones
                white_percentage = white_count / total_stones
                
                # If one player has overwhelming advantage (>60% of stones)
                if black_percentage > 0.60 or white_percentage > 0.60:
                    
                    # Additionally check territory control for a more accurate assessment
                    territory = self.count_territory()
                    black_territory = territory[self.BLACK]
                    white_territory = territory[self.WHITE]
                    
                    # If the player also controls significant territory or has a large territory advantage
                    if (black_percentage > 0.60 and black_territory > white_territory * 1.5) or \
                       (white_percentage > 0.60 and white_territory > black_territory * 1.5):
                        return True
        
        # Condition 3: Game has gone on for too long
        max_moves = self.size * self.size // 2  # Roughly half the board size is a reasonable max
        if len(self.move_history) > max_moves:
            return True
            
        return False
    
    def count_stones(self):
        """Count the number of stones of each color on the board."""
        black_count = np.sum(self.board == self.BLACK)
        white_count = np.sum(self.board == self.WHITE)
        return {self.BLACK: black_count, self.WHITE: white_count}
    
    def count_territory(self):
        """Estimate territory for each color (simple implementation)."""
        territory = {self.BLACK: 0, self.WHITE: 0}
        visited = set()
        
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x, y] == self.EMPTY and (x, y) not in visited:
                    region = set()
                    frontier = [(x, y)]
                    border_colors = set()
                    
                    # Find the connected empty region and its border colors
                    while frontier:
                        px, py = frontier.pop()
                        if (px, py) in visited:
                            continue
                        
                        visited.add((px, py))
                        region.add((px, py))
                        
                        for nx, ny in self.get_adjacent_points(px, py):
                            if self.board[nx, ny] == self.EMPTY and (nx, ny) not in visited:
                                frontier.append((nx, ny))
                            elif self.board[nx, ny] != self.EMPTY:
                                border_colors.add(self.board[nx, ny])
                    
                    # If the region is surrounded by only one color, it's that color's territory
                    if len(border_colors) == 1:
                        color = border_colors.pop()
                        territory[color] += len(region)
        
        return territory
    
    def get_score(self, komi=6.5):
        """
        Calculate the score using area scoring method.
        
        Args:
            komi (float): Points added to White's score to compensate for Black's first-move advantage
        
        Returns:
            tuple: (black_score, white_score)
        """
        stone_count = self.count_stones()
        territory = self.count_territory()
        
        black_score = stone_count[self.BLACK] + territory[self.BLACK]
        white_score = stone_count[self.WHITE] + territory[self.WHITE] + komi
        
        return black_score, white_score
    
    def get_winner(self, komi=6.5):
        """
        Determine the winner of the game.
        
        Returns:
            int: BLACK for black winner, WHITE for white winner, EMPTY for draw
        """
        black_score, white_score = self.get_score(komi)
        
        if black_score > white_score:
            return self.BLACK
        elif white_score > black_score:
            return self.WHITE
        else:
            return self.EMPTY  # Draw
    
    def get_board_state(self):
        """Get the current board state."""
        return self.board.copy()
    
    def __str__(self):
        """String representation of the board."""
        result = "  "
        for i in range(self.size):
            result += chr(65 + i if i < 8 else 66 + i) + " "  # Skip 'I'
        result += "\n"
        
        for i in range(self.size):
            result += f"{self.size - i:2d} "
            for j in range(self.size):
                if self.board[i, j] == self.EMPTY:
                    result += ". "
                elif self.board[i, j] == self.BLACK:
                    result += "● "
                else:
                    result += "○ "
            result += f"{self.size - i}\n"
        
        result += "  "
        for i in range(self.size):
            result += chr(65 + i if i < 8 else 66 + i) + " "
        
        return result