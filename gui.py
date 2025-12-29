import pygame
import sys
import time
import copy
import math
from Game import Game
from Play import Play

# Couleurs cohérentes
BG_DARK = (235, 220, 195)
BG_LIGHT = (245, 235, 215)
WOOD_MAIN = (120, 81, 45)
WOOD_DARK = (80, 54, 30)
WOOD_LIGHT = (160, 108, 60)
STONE = (200, 200, 200)
GOLD = (218, 165, 32)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (46, 125, 50)
RED = (198, 40, 40)
BLUE = (33, 150, 243)

class MancalaGUI:
    def __init__(self):
        pygame.init()
        self.width = 1400
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mancala - Minimax Alpha-Beta")
        self.clock = pygame.time.Clock()
        
        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)
        
        # Load background image
        try:
            self.background = pygame.image.load('table.jpg')
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except:
            self.background = None
        
        self.game_mode = None
        self.player_side = None
        self.game = None
        self.play = None
        self.current_player = None
        self.selected_pit = None
        self.game_over = False
    
    def draw_rounded_rect(self, x, y, w, h, color, radius=20):
        """Dessine un rectangle bien arrondi"""
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, color, rect, border_radius=radius)
    
    def draw_3d_button(self, x, y, w, h, text, color, hover=False):
        """Dessine un bouton 3D"""
        # Ombre
        shadow_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 80), (0, 0, w, h), border_radius=20)
        self.screen.blit(shadow_surf, (x + 5, y + 5))
        
        # Bouton
        btn_color = tuple(min(c + 40, 255) for c in color) if hover else color
        self.draw_rounded_rect(x, y, w, h, btn_color, 20)
        pygame.draw.rect(self.screen, WHITE, (x, y, w, h), 3, border_radius=20)
        
        # Texte
        text_surf = self.font_medium.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=(x + w//2, y + h//2))
        self.screen.blit(text_surf, text_rect)
        
        return pygame.Rect(x, y, w, h)
    
    def draw_stone(self, x, y, size):
        """Dessine une pierre"""
        pygame.draw.circle(self.screen, (180, 180, 180), (x + 1, y + 1), size)
        pygame.draw.circle(self.screen, STONE, (x, y), size)
        pygame.draw.circle(self.screen, (240, 240, 240), (x - size//4, y - size//4), size//5)
    
    def draw_pit(self, x, y, width, height, stones, label, highlight=False):
        """Dessine une fosse avec pierres"""
        # Ombre
        shadow_surf = pygame.Surface((width + 6, height + 6), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 60), (0, 0, width + 6, height + 6))
        self.screen.blit(shadow_surf, (x + 2, y + 2))
        
        # Fosse
        color = GOLD if highlight else WOOD_DARK
        pygame.draw.ellipse(self.screen, color, (x, y, width, height))
        pygame.draw.ellipse(self.screen, WOOD_LIGHT, (x, y, width, height), 4)
        
        # Label
        label_surf = self.font_medium.render(label, True, GOLD)
        self.screen.blit(label_surf, (x + width//2 - label_surf.get_width()//2, y - 35))
        
        # Nombre
        count_surf = self.font_small.render(str(stones), True, WHITE)
        self.screen.blit(count_surf, (x + width//2 - count_surf.get_width()//2, y + height + 15))
        
        # Pierres
        if stones > 0:
            stone_size = 7 if stones > 12 else 9
            max_display = min(stones, 12)
            
            for i in range(max_display):
                angle = (i / max_display) * 6.28
                radius = min(width, height) * 0.25
                stone_x = x + width//2 + int(radius * math.cos(angle))
                stone_y = y + height//2 + int(radius * math.sin(angle))
                self.draw_stone(stone_x, stone_y, stone_size)
    
    def draw_store(self, x, y, width, height, stones, player_name, score):
        """Dessine un magasin avec score"""
        # Ombre
        shadow_surf = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 80), (0, 0, width + 10, height + 10), border_radius=30)
        self.screen.blit(shadow_surf, (x + 4, y + 4))
        
        # Magasin
        self.draw_rounded_rect(x, y, width, height, WOOD_MAIN, 30)
        pygame.draw.rect(self.screen, WOOD_LIGHT, (x, y, width, height), 5, border_radius=30)
        
        # Nom
        name_surf = self.font_small.render(player_name, True, GOLD)
        self.screen.blit(name_surf, (x + width//2 - name_surf.get_width()//2, y - 40))
        
        # Score
        score_surf = self.font_large.render(str(score), True, WHITE)
        self.screen.blit(score_surf, (x + width//2 - score_surf.get_width()//2, y + 20))
        
        # Pierres
        if stones > 0:
            max_display = min(stones, 20)
            cols = 4
            stone_size = 8
            
            for i in range(max_display):
                row = i // cols
                col = i % cols
                stone_x = x + 25 + col * 28
                stone_y = y + 90 + row * 28
                self.draw_stone(stone_x, stone_y, stone_size)
    
    def draw_board(self):
        """Dessine le plateau complet"""
        # Background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BG_DARK)
        
        # Titre
        title = self.font_large.render("MANCALA", True, WOOD_DARK)
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 30))
        
        # Sous-titre mode de jeu
        if self.game_mode == 'cvc':
            mode_text = "COMPUTER 1 VS COMPUTER 2"
        else:
            mode_text = "HUMAN VS COMPUTER"
        mode_surf = self.font_medium.render(mode_text, True, WOOD_DARK)
        self.screen.blit(mode_surf, (self.width//2 - mode_surf.get_width()//2, 95))
        
        # Board
        board_x = 100
        board_y = 200
        board_width = 1200
        board_height = 400
        
        # Ombre board
        shadow_surf = pygame.Surface((board_width + 12, board_height + 12), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 100), (0, 0, board_width + 12, board_height + 12), border_radius=35)
        self.screen.blit(shadow_surf, (board_x + 6, board_y + 6))
        
        # Board en bois
        self.draw_rounded_rect(board_x, board_y, board_width, board_height, WOOD_MAIN, 35)
        pygame.draw.rect(self.screen, WOOD_DARK, (board_x, board_y, board_width, board_height), 6, border_radius=35)
        
        # Fosses Player 2 (G-L) - en haut
        pit_width = 120
        pit_height = 80
        pit_spacing = 135
        start_x = board_x + 180
        top_y = board_y + 50
        
        for i, pit in enumerate(['L', 'K', 'J', 'I', 'H', 'G']):
            highlight = (self.selected_pit == pit)
            self.draw_pit(start_x + i * pit_spacing, top_y, pit_width, pit_height, 
                         self.game.state.board[pit], pit, highlight)
        
        # Fosses Player 1 (A-F) - en bas
        bottom_y = board_y + 270
        for i, pit in enumerate(['A', 'B', 'C', 'D', 'E', 'F']):
            highlight = (self.selected_pit == pit)
            self.draw_pit(start_x + i * pit_spacing, bottom_y, pit_width, pit_height,
                         self.game.state.board[pit], pit, highlight)
        
        # Magasins
        store_width = 120
        store_height = 300
        
        # Magasin Player 1 (droite) - dans le plateau côté droit
        if self.game_mode == 'cvc':
            player1_name = "COMPUTER 1"
        else:
            player1_name = "HUMAN" if self.game.playerSide['HUMAN'] == 'player1' else "COMPUTER"
        self.draw_store(board_x + board_width - store_width - 50, board_y + 50, store_width, store_height,
                       self.game.state.board['1'], player1_name, self.game.state.board['1'])
        
        # Magasin Player 2 (gauche) - dans le plateau côté gauche
        if self.game_mode == 'cvc':
            player2_name = "COMPUTER 2"
        else:
            player2_name = "HUMAN" if self.game.playerSide['HUMAN'] == 'player2' else "COMPUTER"
        self.draw_store(board_x + 20, board_y + 50, store_width, store_height,
                       self.game.state.board['2'], player2_name, self.game.state.board['2'])
        
        # Indicateur de tour
        if not self.game_over:
            if self.game_mode == 'cvc':
                turn_text = f"Tour: {'COMPUTER 1' if self.current_player == 'player1' else 'COMPUTER 2'}"
                turn_color = BLUE if self.current_player == 'player1' else RED
            else:
                turn_text = f"Tour: {'HUMAN' if self.current_player == self.game.playerSide['HUMAN'] else 'COMPUTER'}"
                turn_color = GREEN if self.current_player == self.game.playerSide['HUMAN'] else RED
            turn_surf = self.font_medium.render(turn_text, True, turn_color)
            self.screen.blit(turn_surf, (self.width//2 - turn_surf.get_width()//2, 680))
        
        # Bouton Quit
        quit_btn_w = 150
        quit_btn_h = 50
        quit_btn_x = self.width - quit_btn_w - 30
        quit_btn_y = 30
        self.quit_button_rect = pygame.Rect(quit_btn_x, quit_btn_y, quit_btn_w, quit_btn_h)
        
        mouse_pos = pygame.mouse.get_pos()
        self.draw_3d_button(quit_btn_x, quit_btn_y, quit_btn_w, quit_btn_h,
                           "QUIT", RED,
                           self.quit_button_rect.collidepoint(mouse_pos))
    
    def show_menu(self):
        """Menu principal"""
        running = True
        
        while running:
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill(BG_DARK)
            
            # Titre
            title = self.font_large.render("WELCOME TO MANCALA", True, WOOD_DARK)
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 100))
            
            # Boutons
            mouse_pos = pygame.mouse.get_pos()
            
            btn_y = 280
            btn_spacing = 100
            btn_w = 500
            btn_h = 75
            btn_x = self.width//2 - btn_w//2
            
            hvh_rect = self.draw_3d_button(btn_x, btn_y, btn_w, btn_h, 
                                          "Human vs Computer", BLUE,
                                          pygame.Rect(btn_x, btn_y, btn_w, btn_h).collidepoint(mouse_pos))
            
            cvc_rect = self.draw_3d_button(btn_x, btn_y + btn_spacing, btn_w, btn_h,
                                          "Computer vs Computer", GREEN,
                                          pygame.Rect(btn_x, btn_y + btn_spacing, btn_w, btn_h).collidepoint(mouse_pos))
            
            rules_rect = self.draw_3d_button(btn_x, btn_y + btn_spacing * 2, btn_w, btn_h,
                                           "Rules", WOOD_MAIN,
                                           pygame.Rect(btn_x, btn_y + btn_spacing * 2, btn_w, btn_h).collidepoint(mouse_pos))
            
            quit_rect = self.draw_3d_button(btn_x, btn_y + btn_spacing * 3, btn_w, btn_h,
                                           "Quit", RED,
                                           pygame.Rect(btn_x, btn_y + btn_spacing * 3, btn_w, btn_h).collidepoint(mouse_pos))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hvh_rect.collidepoint(event.pos):
                        self.game_mode = 'hvh'
                        return self.choose_player_side()
                    elif cvc_rect.collidepoint(event.pos):
                        self.game_mode = 'cvc'
                        return self.start_game()
                    elif rules_rect.collidepoint(event.pos):
                        self.show_rules()
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            
            self.clock.tick(60)
    
    def choose_player_side(self):
        """Choix du côté du joueur"""
        running = True
        
        while running:
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill(BG_DARK)
            
            title = self.font_large.render("Choose Your Side", True, WOOD_DARK)
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 100))
            
            mouse_pos = pygame.mouse.get_pos()
            
            btn_y = 300
            btn_w = 450
            btn_h = 100
            
            p1_x = self.width//2 - btn_w - 50
            p2_x = self.width//2 + 50
            
            p1_rect = self.draw_3d_button(p1_x, btn_y, btn_w, btn_h,
                                         "Player 1 (A-F)", BLUE,
                                         pygame.Rect(p1_x, btn_y, btn_w, btn_h).collidepoint(mouse_pos))
            
            p2_rect = self.draw_3d_button(p2_x, btn_y, btn_w, btn_h,
                                         "Player 2 (G-L)", RED,
                                         pygame.Rect(p2_x, btn_y, btn_w, btn_h).collidepoint(mouse_pos))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if p1_rect.collidepoint(event.pos):
                        self.player_side = 'player1'
                        return self.start_game()
                    elif p2_rect.collidepoint(event.pos):
                        self.player_side = 'player2'
                        return self.start_game()
            
            self.clock.tick(60)
    
    def start_game(self):
        """Initialise le jeu"""
        if self.game_mode == 'hvh':
            player_sides = {'HUMAN': self.player_side, 
                           'COMPUTER': 'player2' if self.player_side == 'player1' else 'player1'}
        else:
            player_sides = {'COMPUTER': 'player1', 'HUMAN': 'player2'}
        
        self.game = Game(player_sides)
        self.play = Play(self.game, depth=6, heuristic='basic')
        self.current_player = 'player1'
        self.game_over = False
        self.run_game()
    
    def show_game_over(self):
        """Affiche l'écran Game Over"""
        winner, score_w, score_l = self.game.findWinner()
        
        popup_w = 600
        popup_h = 400
        popup_x = self.width//2 - popup_w//2
        popup_y = self.height//2 - popup_h//2
        
        # Fond semi-transparent
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Popup
        shadow_surf = pygame.Surface((popup_w + 12, popup_h + 12), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 120), (0, 0, popup_w + 12, popup_h + 12), border_radius=35)
        self.screen.blit(shadow_surf, (popup_x + 6, popup_y + 6))
        
        self.draw_rounded_rect(popup_x, popup_y, popup_w, popup_h, WOOD_MAIN, 35)
        pygame.draw.rect(self.screen, GOLD, (popup_x, popup_y, popup_w, popup_h), 6, border_radius=35)
        
        # Texte
        y_offset = popup_y + 50
        
        title = self.font_large.render("GAME OVER", True, RED)
        self.screen.blit(title, (popup_x + popup_w//2 - title.get_width()//2, y_offset))
        
        y_offset += 100
        
        if winner == 'DRAW':
            result = self.font_medium.render(f"Draw! {score_w} - {score_l}", True, WHITE)
            self.screen.blit(result, (popup_x + popup_w//2 - result.get_width()//2, y_offset))
        else:
            # Display COMPUTER 1 or COMPUTER 2 in CvC mode
            if self.game_mode == 'cvc':
                if winner == 'COMPUTER':
                    winner_text = "COMPUTER 1"
                elif winner == 'HUMAN':
                    winner_text = "COMPUTER 2"
                else:
                    winner_text = winner
            else:
                winner_text = winner
            
            result = self.font_medium.render(f"Winner: {winner_text}", True, GOLD)
            self.screen.blit(result, (popup_x + popup_w//2 - result.get_width()//2, y_offset))
            
            y_offset += 60
            score = self.font_medium.render(f"Score: {score_w} - {score_l}", True, WHITE)
            self.screen.blit(score, (popup_x + popup_w//2 - score.get_width()//2, y_offset))
        
        y_offset += 80
        prompt = self.font_small.render("Click to return to menu", True, WHITE)
        self.screen.blit(prompt, (popup_x + popup_w//2 - prompt.get_width()//2, y_offset))
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    waiting = False
    
    def get_clicked_pit(self, pos):
        """Retourne la fosse cliquée"""
        board_x = 100
        board_y = 200
        pit_width = 120
        pit_height = 80
        pit_spacing = 135
        start_x = board_x + 180
        
        # Player 2 pits (haut)
        top_y = board_y + 50
        for i, pit in enumerate(['L', 'K', 'J', 'I', 'H', 'G']):
            pit_rect = pygame.Rect(start_x + i * pit_spacing, top_y, pit_width, pit_height)
            if pit_rect.collidepoint(pos):
                return pit
        
        # Player 1 pits (bas)
        bottom_y = board_y + 270
        for i, pit in enumerate(['A', 'B', 'C', 'D', 'E', 'F']):
            pit_rect = pygame.Rect(start_x + i * pit_spacing, bottom_y, pit_width, pit_height)
            if pit_rect.collidepoint(pos):
                return pit
        
        return None
    
    def show_rules(self):
        """Affiche les règles du jeu"""
        running = True
        
        rules = [
            "MANCALA RULES:",
            "",
            "1. Each player controls 6 pits (A-F or G-L) and one store",
            "",
            "2. Players take turns picking a pit and distributing stones",
            "   counterclockwise, one stone per pit",
            "",
            "3. Skip the opponent's store when distributing",
            "",
            "4. CAPTURE: If your last stone lands in an empty pit on your",
            "   side and the opposite pit has stones, capture both",
            "",
            "5. Game ends when one side is empty. Player with most",
            "   stones in their store wins",
            "",
            "6. AI uses Minimax Alpha-Beta Pruning algorithm"
        ]
        
        while running:
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill(BG_DARK)
            
            # Semi-transparent overlay
            overlay = pygame.Surface((900, 600), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (120, 81, 45, 240), (0, 0, 900, 600), border_radius=30)
            self.screen.blit(overlay, (250, 100))
            
            # Border
            pygame.draw.rect(self.screen, GOLD, (250, 100, 900, 600), 5, border_radius=30)
            
            # Rules text
            y_offset = 130
            for line in rules:
                if line.startswith("MANCALA RULES:"):
                    text_surf = self.font_large.render(line, True, WOOD_DARK)
                elif line == "":
                    y_offset += 10
                    continue
                else:
                    text_surf = self.font_small.render(line, True, WHITE)
                
                self.screen.blit(text_surf, (280, y_offset))
                y_offset += 40
            
            # Back button
            btn_w = 300
            btn_h = 60
            btn_x = self.width//2 - btn_w//2
            btn_y = 630
            
            mouse_pos = pygame.mouse.get_pos()
            back_rect = self.draw_3d_button(btn_x, btn_y, btn_w, btn_h,
                                           "Back to Menu", WOOD_MAIN,
                                           pygame.Rect(btn_x, btn_y, btn_w, btn_h).collidepoint(mouse_pos))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(event.pos):
                        return
            
            self.clock.tick(60)
    
    def run_game(self):
        """Boucle principale du jeu"""
        running = True
        
        while running and not self.game.gameOver():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check quit button
                    if hasattr(self, 'quit_button_rect') and self.quit_button_rect.collidepoint(event.pos):
                        return
                    
                    if self.game_mode == 'hvh' and self.current_player == self.game.playerSide['HUMAN']:
                        pit = self.get_clicked_pit(event.pos)
                        moves = self.game.state.possibleMoves(self.game.playerSide['HUMAN'])
                        
                        if pit and pit in moves:
                            self.selected_pit = pit
                            self.draw_board()
                            pygame.display.flip()
                            pygame.time.wait(300)
                            
                            self.game.state.doMove(self.game.playerSide['HUMAN'], pit)
                            self.current_player = 'player2' if self.current_player == 'player1' else 'player1'
                            self.selected_pit = None
            
            # Computer turns
            if self.game_mode == 'hvh' and self.current_player == self.game.playerSide['COMPUTER']:
                self.draw_board()
                pygame.display.flip()
                pygame.time.wait(700)
                
                value, pit = self.play.MinimaxAlphaBetaPruning(
                    self.game, Game.MAX, 6, float('-inf'), float('inf')
                )
                
                if pit:
                    self.selected_pit = pit
                    self.draw_board()
                    pygame.display.flip()
                    pygame.time.wait(700)
                    
                    self.game.state.doMove(self.game.playerSide['COMPUTER'], pit)
                    self.current_player = 'player2' if self.current_player == 'player1' else 'player1'
                    self.selected_pit = None
            
            elif self.game_mode == 'cvc':
                self.draw_board()
                pygame.display.flip()
                pygame.time.wait(1000)
                
                if self.current_player == 'player1':
                    play_ai = Play(self.game, depth=7, heuristic='advanced')
                    value, pit = play_ai.MinimaxAlphaBetaPruning(
                        self.game, Game.MAX, 7, float('-inf'), float('inf')
                    )
                else:
                    # Computer 2 avec rôles inversés pour utiliser MAX aussi
                    play_ai = Play(self.game, depth=7, heuristic='basic')
                    temp_game = Game({'COMPUTER': 'player2', 'HUMAN': 'player1'})
                    temp_game.state = copy.deepcopy(self.game.state)
                    value, pit = play_ai.MinimaxAlphaBetaPruning(
                        temp_game, Game.MAX, 7, float('-inf'), float('inf')
                    )
                
                if pit:
                    self.selected_pit = pit
                    self.draw_board()
                    pygame.display.flip()
                    pygame.time.wait(700)
                    
                    self.game.state.doMove(self.current_player, pit)
                    self.current_player = 'player2' if self.current_player == 'player1' else 'player1'
                    self.selected_pit = None
            
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)
        
        if self.game.gameOver():
            self.game_over = True
            self.draw_board()
            pygame.display.flip()
            pygame.time.wait(1000)
            self.show_game_over()
            self.show_menu()
    
    def run(self):
        """Lance l'application"""
        self.show_menu()

if __name__ == "__main__":
    gui = MancalaGUI()
    gui.run()
