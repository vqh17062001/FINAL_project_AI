import pygame
import sys
import numpy as np
from board import GoBoard

class GoGameUI:
    """
    UI for the Go game.
    """
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BOARD_COLOR = (219, 176, 102)
    LINE_COLOR = (0, 0, 0)
    TEXT_COLOR = (0, 0, 0)
    HIGHLIGHT_COLOR = (255, 0, 0, 128)
    
    def __init__(self, board_size=19, fullscreen=False):
        """
        Initialize the UI.
        
        Args:
            board_size (int): Size of the board (9, 13, or 19)
            fullscreen (bool): Whether to run in fullscreen mode
        """
        pygame.init()
        self.board_size = board_size
        self.fullscreen = fullscreen
        
        # Get screen info for adaptive sizing
        screen_info = pygame.display.Info()
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        
        # Set cell size and margins adaptively
        if fullscreen:
            # Adapt cell size to screen resolution (leaving space for info panel)
            board_area_width = self.screen_width - 350  # reserve space for info panel
            board_area_height = self.screen_height
            
            # Determine cell size based on the smaller dimension
            max_cell_size = min(
                board_area_width / (board_size + 2),  # +2 for margins
                board_area_height / (board_size + 2)
            )
            self.cell_size = int(max_cell_size)
            self.margin = self.cell_size
        else:
            # Điều chỉnh kích thước mặc định dựa trên kích thước bàn cờ
            if board_size == 9:
                # Tăng kích thước ô cho bàn cờ 9x9
                self.cell_size = 50  # Tăng từ 30 lên 50
                self.margin = 50     # Tăng margin cho bàn cờ nhỏ
            elif board_size == 13:
                self.cell_size = 40
                self.margin = 45
            else:  # 19x19
                self.cell_size = 30
                self.margin = 40
        
        self.stone_radius = self.cell_size // 2 - 2
        
        # Calculate window size based on board size
        self.info_panel_width = 350
        self.window_width = (self.board_size + 1) * self.cell_size + 2 * self.margin + self.info_panel_width
        self.window_height = max(650, (self.board_size + 1) * self.cell_size + 2 * self.margin)
        
        if fullscreen:
            self.window_width = self.screen_width
            self.window_height = self.screen_height
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        
        pygame.display.set_caption("Go Game")
        
        # Create fonts - size based on cell size
        self.font_size = max(14, self.cell_size // 2)
        self.title_font_size = max(18, self.cell_size // 2 + 4)
        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.title_font = pygame.font.SysFont('Arial', self.title_font_size, bold=True)
        
        # Create board
        self.board = GoBoard(board_size)
        
        # Game state
        self.running = True
        self.game_over = False
        self.agents = []
        self.current_agent_index = 0
        self.auto_play = False
        self.delay = 500  # milliseconds
        self.last_move = None
        
        # Initialize UI components
        self.update_ui_components()
    
    def update_ui_components(self):
        """Update UI component sizes and positions based on current window size"""
        # UI state
        self.info_panel_rect = pygame.Rect(
            self.window_width - self.info_panel_width,
            0,
            self.info_panel_width,
            self.window_height
        )
        
        # Buttons
        self.button_height = max(30, self.cell_size // 1.5)
        self.button_width = max(120, self.info_panel_width // 2 - 30)
        self.button_margin = max(10, self.cell_size // 3)
        
        self.size_9_button = pygame.Rect(
            self.info_panel_rect.x + self.button_margin,
            self.button_margin,
            self.button_width,
            self.button_height
        )
        
        self.size_13_button = pygame.Rect(
            self.info_panel_rect.x + self.button_width + 2 * self.button_margin,
            self.button_margin,
            self.button_width,
            self.button_height
        )
        
        self.size_19_button = pygame.Rect(
            self.info_panel_rect.x + self.button_margin,
            self.button_margin + self.button_height + self.button_margin,
            self.button_width,
            self.button_height
        )
        
        self.autoplay_button = pygame.Rect(
            self.info_panel_rect.x + self.button_width + 2 * self.button_margin,
            self.button_margin + self.button_height + self.button_margin,
            self.button_width,
            self.button_height
        )
        
        self.reset_button = pygame.Rect(
            self.info_panel_rect.x + self.button_margin,
            self.button_margin + 2 * self.button_height + 2 * self.button_margin,
            self.button_width,
            self.button_height
        )
        
        self.pass_button = pygame.Rect(
            self.info_panel_rect.x + self.button_width + 2 * self.button_margin,
            self.button_margin + 2 * self.button_height + 2 * self.button_margin,
            self.button_width,
            self.button_height
        )
        
        # Add fullscreen toggle button
        self.fullscreen_button = pygame.Rect(
            self.info_panel_rect.x + self.button_margin,
            self.button_margin + 3 * self.button_height + 3 * self.button_margin,
            self.button_width,
            self.button_height
        )
    
    def set_agents(self, agent1, agent2):
        """
        Set the agents for the game.
        
        Args:
            agent1: First agent (Black)
            agent2: Second agent (White)
        """
        self.agents = [agent1, agent2]
    
    def reset_game(self, new_size=None):
        """
        Reset the game.
        
        Args:
            new_size (int, optional): New board size
        """
        if new_size is not None and new_size != self.board_size:
            self.board_size = new_size
            
            # Recalculate cell size if in fullscreen mode
            if self.fullscreen:
                board_area_width = self.screen_width - 350
                board_area_height = self.screen_height
                max_cell_size = min(
                    board_area_width / (self.board_size + 2),
                    board_area_height / (self.board_size + 2)
                )
                self.cell_size = int(max_cell_size)
                self.margin = self.cell_size
                self.stone_radius = self.cell_size // 2 - 2
            else:
                # Điều chỉnh kích thước mặc định dựa trên kích thước bàn cờ
                if new_size == 9:
                    # Tăng kích thước ô cho bàn cờ 9x9
                    self.cell_size = 50  # Tăng từ 30 lên 50
                    self.margin = 50     # Tăng margin cho bàn cờ nhỏ
                elif new_size == 13:
                    self.cell_size = 40
                    self.margin = 45
                else:  # 19x19
                    self.cell_size = 30
                    self.margin = 40
                
                self.stone_radius = self.cell_size // 2 - 2
                self.window_width = (self.board_size + 1) * self.cell_size + 2 * self.margin + self.info_panel_width
                self.window_height = max(650, (self.board_size + 1) * self.cell_size + 2 * self.margin)
                self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
            
            # Update UI components based on new sizes
            self.update_ui_components()
        
        self.board = GoBoard(self.board_size)
        self.game_over = False
        self.current_agent_index = 0
        self.last_move = None
        
        # Reset agents' metrics
        for agent in self.agents:
            agent.reset_metrics()
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.fullscreen = not self.fullscreen
        
        # Get screen info
        screen_info = pygame.display.Info()
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        
        if self.fullscreen:
            # Switch to fullscreen
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.window_width = self.screen_width
            self.window_height = self.screen_height
            
            # Adapt cell size to screen resolution
            board_area_width = self.screen_width - 350
            board_area_height = self.screen_height
            max_cell_size = min(
                board_area_width / (self.board_size + 2),
                board_area_height / (self.board_size + 2)
            )
            self.cell_size = int(max_cell_size)
            self.margin = self.cell_size
            self.stone_radius = self.cell_size // 2 - 2
        else:
            # Switch to windowed mode with adaptive sizes based on board size
            if self.board_size == 9:
                # Tăng kích thước ô cho bàn cờ 9x9
                self.cell_size = 50
                self.margin = 50
            elif self.board_size == 13:
                self.cell_size = 40
                self.margin = 45
            else:  # 19x19
                self.cell_size = 30
                self.margin = 40
            
            self.stone_radius = self.cell_size // 2 - 2
            
            self.window_width = (self.board_size + 1) * self.cell_size + 2 * self.margin + self.info_panel_width
            self.window_height = max(650, (self.board_size + 1) * self.cell_size + 2 * self.margin)
            self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        
        # Update font sizes based on cell size
        self.font_size = max(14, self.cell_size // 2)
        self.title_font_size = max(18, self.cell_size // 2 + 4)
        self.font = pygame.font.SysFont('Arial', self.font_size)
        self.title_font = pygame.font.SysFont('Arial', self.title_font_size, bold=True)
        
        # Update UI components with new dimensions
        self.update_ui_components()
    
    def handle_resize(self, size):
        """
        Handle window resize event.
        
        Args:
            size (tuple): New window size (width, height)
        """
        if not self.fullscreen:
            self.window_width, self.window_height = size
            
            # Adjust cell size based on new window dimensions
            board_area_width = self.window_width - self.info_panel_width - 2 * self.margin
            board_area_height = self.window_height - 2 * self.margin
            max_cell_size = min(
                board_area_width / (self.board_size + 1),
                board_area_height / (self.board_size + 1)
            )
            self.cell_size = max(15, int(max_cell_size))  # Ensure minimum size
            self.stone_radius = self.cell_size // 2 - 2
            
            # Update font sizes
            self.font_size = max(14, self.cell_size // 2)
            self.title_font_size = max(18, self.cell_size // 2 + 4)
            self.font = pygame.font.SysFont('Arial', self.font_size)
            self.title_font = pygame.font.SysFont('Arial', self.title_font_size, bold=True)
            
            # Update UI components with new dimensions
            self.update_ui_components()
    
    def board_coords_to_screen(self, x, y):
        """
        Convert board coordinates to screen coordinates.
        
        Args:
            x (int): Board x-coordinate
            y (int): Board y-coordinate
            
        Returns:
            tuple: Screen coordinates (x, y)
        """
        return (
            self.margin + self.cell_size + x * self.cell_size,
            self.margin + self.cell_size + y * self.cell_size
        )
    
    def screen_coords_to_board(self, x, y):
        """
        Convert screen coordinates to board coordinates.
        
        Args:
            x (int): Screen x-coordinate
            y (int): Screen y-coordinate
            
        Returns:
            tuple: Board coordinates (x, y) or None if invalid
        """
        # Calculate the position on the board
        board_x = round((x - self.margin - self.cell_size) / self.cell_size)
        board_y = round((y - self.margin - self.cell_size) / self.cell_size)
        
        # Check if the position is valid
        if 0 <= board_x < self.board_size and 0 <= board_y < self.board_size:
            return (board_x, board_y)
        
        return None
    
    def draw_board(self):
        """Draw the Go board."""
        # Draw board background
        pygame.draw.rect(self.window, self.BOARD_COLOR, (
            self.margin,
            self.margin,
            (self.board_size + 1) * self.cell_size,
            (self.board_size + 1) * self.cell_size
        ))
        
        # Draw grid lines
        for i in range(self.board_size):
            # Horizontal lines
            pygame.draw.line(
                self.window,
                self.LINE_COLOR,
                self.board_coords_to_screen(0, i),
                self.board_coords_to_screen(self.board_size - 1, i),
                max(1, self.cell_size // 15)  # Scale line thickness
            )
            
            # Vertical lines
            pygame.draw.line(
                self.window,
                self.LINE_COLOR,
                self.board_coords_to_screen(i, 0),
                self.board_coords_to_screen(i, self.board_size - 1),
                max(1, self.cell_size // 15)  # Scale line thickness
            )
        
        # Draw star points (hoshi)
        if self.board_size == 19:
            star_points = [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]
        elif self.board_size == 13:
            star_points = [(3, 3), (3, 9), (6, 6), (9, 3), (9, 9)]
        elif self.board_size == 9:
            star_points = [(2, 2), (2, 6), (4, 4), (6, 2), (6, 6)]
        
        star_radius = max(3, self.cell_size // 10)
        for x, y in star_points:
            screen_x, screen_y = self.board_coords_to_screen(x, y)
            pygame.draw.circle(self.window, self.BLACK, (screen_x, screen_y), star_radius)
        
        # Draw the stones
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board.board[x, y] != GoBoard.EMPTY:
                    screen_x, screen_y = self.board_coords_to_screen(x, y)
                    color = self.BLACK if self.board.board[x, y] == GoBoard.BLACK else self.WHITE
                    pygame.draw.circle(self.window, color, (screen_x, screen_y), self.stone_radius)
                    
                    # Draw a border for white stones
                    if self.board.board[x, y] == GoBoard.WHITE:
                        border_width = max(1, self.cell_size // 20)
                        pygame.draw.circle(self.window, self.BLACK, (screen_x, screen_y), self.stone_radius, border_width)
        
        # Highlight the last move
        if self.last_move is not None and self.last_move != (-1, -1):
            x, y = self.last_move
            screen_x, screen_y = self.board_coords_to_screen(x, y)
            
            # Create a transparent surface for the highlight
            highlight_surface = pygame.Surface((self.stone_radius * 2, self.stone_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(highlight_surface, self.HIGHLIGHT_COLOR, (self.stone_radius, self.stone_radius), self.stone_radius)
            
            # Blit the highlight surface onto the window
            self.window.blit(highlight_surface, (screen_x - self.stone_radius, screen_y - self.stone_radius))
    
    def draw_info_panel(self):
        """Draw the information panel."""
        # Draw panel background
        pygame.draw.rect(self.window, (240, 240, 240), self.info_panel_rect)
        pygame.draw.line(self.window, self.BLACK, (self.info_panel_rect.x, 0), (self.info_panel_rect.x, self.window_height), 2)
        
        # Draw board size buttons
        pygame.draw.rect(self.window, (200, 200, 200), self.size_9_button)
        pygame.draw.rect(self.window, (200, 200, 200), self.size_13_button)
        pygame.draw.rect(self.window, (200, 200, 200), self.size_19_button)
        
        size_9_text = self.font.render("9x9 Board", True, self.BLACK)
        size_13_text = self.font.render("13x13 Board", True, self.BLACK)
        size_19_text = self.font.render("19x19 Board", True, self.BLACK)
        
        # Center text on buttons
        self.window.blit(size_9_text, (
            self.size_9_button.x + (self.size_9_button.width - size_9_text.get_width()) // 2,
            self.size_9_button.y + (self.size_9_button.height - size_9_text.get_height()) // 2
        ))
        self.window.blit(size_13_text, (
            self.size_13_button.x + (self.size_13_button.width - size_13_text.get_width()) // 2,
            self.size_13_button.y + (self.size_13_button.height - size_13_text.get_height()) // 2
        ))
        self.window.blit(size_19_text, (
            self.size_19_button.x + (self.size_19_button.width - size_19_text.get_width()) // 2,
            self.size_19_button.y + (self.size_19_button.height - size_19_text.get_height()) // 2
        ))
        
        # Draw autoplay button
        pygame.draw.rect(self.window, (200, 200, 200), self.autoplay_button)
        autoplay_text = self.font.render("Autoplay: " + ("ON" if self.auto_play else "OFF"), True, self.BLACK)
        self.window.blit(autoplay_text, (
            self.autoplay_button.x + (self.autoplay_button.width - autoplay_text.get_width()) // 2,
            self.autoplay_button.y + (self.autoplay_button.height - autoplay_text.get_height()) // 2
        ))
        
        # Draw reset button
        pygame.draw.rect(self.window, (200, 200, 200), self.reset_button)
        reset_text = self.font.render("Reset Game", True, self.BLACK)
        self.window.blit(reset_text, (
            self.reset_button.x + (self.reset_button.width - reset_text.get_width()) // 2,
            self.reset_button.y + (self.reset_button.height - reset_text.get_height()) // 2
        ))
        
        # Draw pass button
        pygame.draw.rect(self.window, (200, 200, 200), self.pass_button)
        pass_text = self.font.render("Pass", True, self.BLACK)
        self.window.blit(pass_text, (
            self.pass_button.x + (self.pass_button.width - pass_text.get_width()) // 2,
            self.pass_button.y + (self.pass_button.height - pass_text.get_height()) // 2
        ))
        
        # Draw fullscreen toggle button
        pygame.draw.rect(self.window, (200, 200, 200), self.fullscreen_button)
        fullscreen_text = self.font.render("Fullscreen: " + ("ON" if self.fullscreen else "OFF"), True, self.BLACK)
        self.window.blit(fullscreen_text, (
            self.fullscreen_button.x + (self.fullscreen_button.width - fullscreen_text.get_width()) // 2,
            self.fullscreen_button.y + (self.fullscreen_button.height - fullscreen_text.get_height()) // 2
        ))
        
        # Draw game information
        y_offset = self.fullscreen_button.y + self.fullscreen_button.height + self.button_margin + 20
        
        # Current player
        current_player_text = self.title_font.render("Current Player:", True, self.BLACK)
        self.window.blit(current_player_text, (self.info_panel_rect.x + 10, y_offset))
        y_offset += self.title_font_size + 10
        
        player_color = "Black" if self.board.current_player == GoBoard.BLACK else "White"
        player_name = self.agents[self.current_agent_index].name if self.agents else player_color
        player_text = self.font.render(f"{player_color}: {player_name}", True, self.BLACK)
        self.window.blit(player_text, (self.info_panel_rect.x + 20, y_offset))
        y_offset += self.font_size + 10
        
        # Game status
        status_text = self.title_font.render("Game Status:", True, self.BLACK)
        self.window.blit(status_text, (self.info_panel_rect.x + 10, y_offset))
        y_offset += self.title_font_size + 10
        
        if self.game_over:
            winner = self.board.get_winner()
            if winner == GoBoard.BLACK:
                status = "Black wins!"
            elif winner == GoBoard.WHITE:
                status = "White wins!"
            else:
                status = "Draw!"
            
            black_score, white_score = self.board.get_score()
            score_status = f"Black: {black_score:.1f}, White: {white_score:.1f}"
        else:
            status = "In progress"
            score_status = ""
        
        game_status_text = self.font.render(status, True, self.BLACK)
        self.window.blit(game_status_text, (self.info_panel_rect.x + 20, y_offset))
        y_offset += self.font_size + 5
        
        if score_status:
            score_text = self.font.render(score_status, True, self.BLACK)
            self.window.blit(score_text, (self.info_panel_rect.x + 20, y_offset))
            y_offset += self.font_size + 10
        
        # Hiển thị một số thông tin về số quân trên bàn cờ ngay cả khi đang chơi
        if not self.game_over:
            stone_count = self.board.count_stones()
            current_score_text = self.font.render(
                f"Stones: B: {stone_count[GoBoard.BLACK]}, W: {stone_count[GoBoard.WHITE]}", 
                True, self.BLACK
            )
            self.window.blit(current_score_text, (self.info_panel_rect.x + 20, y_offset))
            y_offset += self.font_size + 10
        
        # Agent information
        y_offset += 10
        agents_text = self.title_font.render("Agents:", True, self.BLACK)
        self.window.blit(agents_text, (self.info_panel_rect.x + 10, y_offset))
        y_offset += self.title_font_size + 10
        
        # Đảm bảo có đủ không gian hiển thị thông tin agent (đặc biệt quan trọng cho bàn cờ 9x9)
        if len(self.agents) > 0:
            # Tính toán không gian còn lại
            remaining_space = self.window_height - y_offset - 20
            space_per_agent = remaining_space / len(self.agents)
            
            # Điều chỉnh không gian hiển thị
            compact_mode = space_per_agent < 90  # Nếu không gian quá ít, hiển thị dưới dạng compact
            
            for i, agent in enumerate(self.agents):
                color = "Black" if i == 0 else "White"
                agent_text = self.font.render(f"{color}: {agent.name}", True, self.BLACK)
                self.window.blit(agent_text, (self.info_panel_rect.x + 20, y_offset))
                
                if compact_mode:
                    # Hiển thị thông tin thời gian và bộ nhớ trên cùng một dòng
                    y_offset += self.font_size + 5
                    
                    # Cập nhật để hiển thị tổng bộ nhớ thay vì bộ nhớ trung bình
                    combined_text = self.font.render(
                        f"Time: {agent.get_average_time():.2f}s | Mem: {agent.get_total_memory():.2f}MB", 
                        True, self.BLACK
                    )
                    self.window.blit(combined_text, (self.info_panel_rect.x + 20, y_offset))
                    y_offset += self.font_size + 10
                else:
                    y_offset += self.font_size + 5
                    
                    time_text = self.font.render(f"Avg Time: {agent.get_average_time():.4f}s", True, self.BLACK)
                    self.window.blit(time_text, (self.info_panel_rect.x + 20, y_offset))
                    y_offset += self.font_size + 5
                    
                    # Cập nhật để hiển thị tổng bộ nhớ thay vì bộ nhớ trung bình
                    memory_text = self.font.render(f"Total Memory: {agent.get_total_memory():.2f}MB", True, self.BLACK)
                    self.window.blit(memory_text, (self.info_panel_rect.x + 20, y_offset))
                    y_offset += self.font_size + 15
    
    def handle_click(self, pos):
        """
        Handle mouse clicks.
        
        Args:
            pos (tuple): Mouse position (x, y)
        """
        x, y = pos
        
        # Check if the click is on the board
        if x < self.info_panel_rect.x:
            board_pos = self.screen_coords_to_board(x, y)
            if board_pos and not self.game_over:
                if self.agents and self.board.current_player == self.agents[self.current_agent_index].color:
                    # If it's an agent's turn and autoplay is off, don't allow manual moves
                    if not self.auto_play:
                        print("Cannot make manual moves for AI agent")
                else:
                    self.make_move(board_pos)
        else:
            # Check if a button was clicked
            if self.size_9_button.collidepoint(pos):
                self.reset_game(9)
            elif self.size_13_button.collidepoint(pos):
                self.reset_game(13)
            elif self.size_19_button.collidepoint(pos):
                self.reset_game(19)
            elif self.autoplay_button.collidepoint(pos):
                self.auto_play = not self.auto_play
            elif self.reset_button.collidepoint(pos):
                self.reset_game()
            elif self.pass_button.collidepoint(pos) and not self.game_over:
                self.make_move((-1, -1))  # Pass
            elif self.fullscreen_button.collidepoint(pos):
                self.toggle_fullscreen()
    
    def make_move(self, pos):
        """
        Make a move at the given position.
        
        Args:
            pos (tuple): Board position (x, y)
        """
        if self.board.play_move(*pos):
            self.last_move = pos
            
            # Check if the game is over
            if self.board.is_game_over():
                self.game_over = True
                print("Game over!")
                winner = self.board.get_winner()
                if winner == GoBoard.BLACK:
                    print("Black wins!")
                elif winner == GoBoard.WHITE:
                    print("White wins!")
                else:
                    print("Draw!")
            else:
                # Switch to the next player
                self.current_agent_index = 1 - self.current_agent_index
    
    def agent_move(self):
        """Make a move for the current agent."""
        if not self.game_over and self.agents and self.board.current_player == self.agents[self.current_agent_index].color:
            agent = self.agents[self.current_agent_index]
            move = agent.get_move(self.board)
            
            if move:
                self.make_move(move)
    
    def run(self):
        """Run the UI loop."""
        clock = pygame.time.Clock()
        last_agent_move_time = 0
        
        while self.running:
            current_time = pygame.time.get_ticks()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:  # Use F key as shortcut for fullscreen toggle
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE and self.fullscreen:
                        # ESC exits fullscreen mode
                        self.fullscreen = False
                        self.toggle_fullscreen()
                elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
                    # Handle window resize
                    self.handle_resize(event.size)
            
            # Agent moves in autoplay mode
            if self.auto_play and not self.game_over and self.agents:
                if current_time - last_agent_move_time > self.delay:
                    self.agent_move()
                    last_agent_move_time = current_time
            
            # Draw the game
            self.window.fill((255, 255, 255))
            self.draw_board()
            self.draw_info_panel()
            
            # Update the display
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()