import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60

# Colors - Professional palette
DARK_BLUE = (13, 27, 42)
NAVY = (27, 38, 59)
GOLD = (255, 195, 0)
LIGHT_GOLD = (255, 215, 77)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (189, 195, 199)
LIGHT_GRAY = (236, 240, 241)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
BLUE = (52, 152, 219)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)

# Word pairs
WORD_PAIRS = [
    ("clean the garage", "garajı temizlemek"),
    ("clean up", "temizlemek"),
    ("cook", "yemek pişirmek"),
    ("do errands", "günlük işler yapmak"),
    ("do the ironing", "ütü yapmak"),
    ("do the laundry", "çamaşırları yıkamak"),
    ("dry the dishes", "bulaşıkları kurulamak"),
    ("dust the furniture", "mobilyaların tozunu almak"),
    ("empty the dishwasher", "bulaşık makinesini boşaltmak"),
    ("feed the cat", "kediyi beslemek"),
    ("go shopping", "alışveriş yapmak"),
    ("load the dishwasher", "bulaşık makinesini doldurmak"),
    ("make the bed", "yatağı toplamak"),
    ("mop the floor", "yeri paspaslamak"),
    ("prepare meals", "yemek hazırlamak"),
    ("set the table", "masayı kurmak"),
    ("take care of the garden", "bahçe ile ilgilenmek"),
    ("take out the garbage", "çöpü dışarı çıkartmak"),
    ("tidy up the room", "odayı toplamak"),
    ("vacuum the floor", "yeri süpürmek"),
    ("walk the dog", "köpeği yürüyüşe çıkarmak"),
    ("wash the dishes", "bulaşıkları yıkamak"),
    ("wash the car", "arabayı yıkamak")
]

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, text_color=WHITE, font_size=28):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = color
        self.color = color
        self.text_color = text_color
        self.hover = False
        self.font = pygame.font.Font(None, font_size)
        self.disabled = False
        
    def draw(self, screen):
        color = self.color
        if self.hover and not self.disabled:
            # Lighten color on hover
            color = tuple(min(c + 30, 255) for c in self.base_color)
            
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=12)
        
        # Draw text with word wrap
        words = self.text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.font.size(test_line)[0] <= self.rect.width - 20:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        total_height = len(lines) * self.font.get_height()
        y_offset = self.rect.centery - total_height // 2
        
        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, y_offset + self.font.get_height() // 2))
            screen.blit(text_surface, text_rect)
            y_offset += self.font.get_height()
        
    def check_hover(self, pos):
        self.hover = self.rect.collidepoint(pos) and not self.disabled
        return self.hover
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) and not self.disabled

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chores Master - Ev Isleri Ustasi")
        self.clock = pygame.time.Clock()
        
        # Load sounds and images with proper path handling
        import os
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        sounds_path = os.path.join(base_path, 'sounds')
        
        try:
            self.correct_sound = pygame.mixer.Sound(os.path.join(sounds_path, "correct.mp3"))
            self.wrong_sound = pygame.mixer.Sound(os.path.join(sounds_path, "wrong.mp3"))
            self.thinking_sound = pygame.mixer.Sound(os.path.join(sounds_path, "thinking.mp3"))
            
            # Set volume to avoid overlapping chaos
            self.correct_sound.set_volume(0.5)
            self.wrong_sound.set_volume(0.5)
            self.thinking_sound.set_volume(0.3)
        except Exception as e:
            print(f"Sound loading error: {e}")
            self.correct_sound = None
            self.wrong_sound = None
            self.thinking_sound = None
        
        # Load logo
        try:
            logo_path = os.path.join(base_path, "logo.png")
            self.logo = pygame.image.load(logo_path)
            # Scale logo to reasonable size (max 150x150)
            logo_width, logo_height = self.logo.get_size()
            max_size = 150
            if logo_width > max_size or logo_height > max_size:
                scale_factor = min(max_size / logo_width, max_size / logo_height)
                new_width = int(logo_width * scale_factor)
                new_height = int(logo_height * scale_factor)
                self.logo = pygame.transform.scale(self.logo, (new_width, new_height))
        except Exception as e:
            print(f"Logo loading error: {e}")
            self.logo = None
        
        self.state = "MENU"  # MENU, GAME, GAME_OVER
        self.game_mode = None
        self.total_score = 0
        self.last_sound_time = 0
        
    def play_sound(self, sound):
        # Prevent sound overlap - only play if 200ms passed since last sound
        current_time = pygame.time.get_ticks()
        if sound and (current_time - self.last_sound_time) > 200:
            pygame.mixer.stop()  # Stop any currently playing sound
            sound.play()
            self.last_sound_time = current_time
    
    def draw_gradient_background(self, color1, color2):
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
    
    def draw_menu(self):
        self.draw_gradient_background(DARK_BLUE, NAVY)
        
        # Logo at top
        if self.logo:
            logo_x = WIDTH // 2 - self.logo.get_width() // 2
            logo_y = 20
            self.screen.blit(self.logo, (logo_x, logo_y))
            title_y = logo_y + self.logo.get_height() + 10
        else:
            title_y = 50
        
        # Title with shadow
        title_font = pygame.font.Font(None, 80)
        shadow = title_font.render("CHORES MASTER", True, BLACK)
        title = title_font.render("CHORES MASTER", True, GOLD)
        self.screen.blit(shadow, (WIDTH // 2 - title.get_width() // 2 + 3, title_y + 3))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, title_y))
        
        subtitle_font = pygame.font.Font(None, 36)
        subtitle = subtitle_font.render("Ev Isleri Kelime Oyunu", True, LIGHT_GOLD)
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, title_y + 70))
        
        # Game mode buttons
        button_width = 500
        button_height = 100
        start_y = title_y + 140
        spacing = 120
        
        modes = [
            ("KIM MILYONER OLMAK ISTER", "quiz", BLUE, "Coktan secmeli sorular - Suresiz"),
            ("HIZLI YANITLA", "speed", RED, "30 saniyede kac kelime bilirsin? - Sureli"),
            ("KELIME ESLESTIRME", "match", GREEN, "Ingilizce-Turkce eslestir - Suresiz"),
            ("ZAMANA KARSI", "timed", ORANGE, "60 saniyede tum kelimeleri bul - Sureli")
        ]
        
        self.menu_buttons = []
        for i, (text, mode, color, desc) in enumerate(modes):
            btn = Button(WIDTH // 2 - button_width // 2, start_y + i * spacing, 
                        button_width, button_height, text, color, WHITE, 32)
            btn.mode = mode
            self.menu_buttons.append(btn)
            
            # Description
            desc_font = pygame.font.Font(None, 24)
            desc_surface = desc_font.render(desc, True, GRAY)
            self.screen.blit(desc_surface, 
                           (WIDTH // 2 - desc_surface.get_width() // 2, 
                            start_y + i * spacing + button_height + 5))
        
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.menu_buttons:
            btn.check_hover(mouse_pos)
            btn.draw(self.screen)
        
        # Credits at bottom
        credits_y = HEIGHT - 60
        
        # Developer info
        dev_font = pygame.font.Font(None, 32)
        dev_text = dev_font.render("CeZeC Dev", True, GOLD)
        self.screen.blit(dev_text, (WIDTH // 2 - dev_text.get_width() // 2, credits_y))
        
        # Programmer info
        prog_font = pygame.font.Font(None, 24)
        prog_text = prog_font.render("Programmer: Cesur", True, LIGHT_GOLD)
        self.screen.blit(prog_text, (WIDTH // 2 - prog_text.get_width() // 2, credits_y + 30))
    
    def start_game(self, mode):
        self.game_mode = mode
        self.state = "GAME"
        
        if mode == "quiz":
            self.quiz_game = QuizGame(self)
        elif mode == "speed":
            self.speed_game = SpeedGame(self)
        elif mode == "match":
            self.match_game = MatchGame(self)
        elif mode == "timed":
            self.timed_game = TimedGame(self)
    
    def run(self):
        running = True
        
        while running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.state == "MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for btn in self.menu_buttons:
                            if btn.is_clicked(mouse_pos):
                                self.play_sound(self.thinking_sound)
                                self.start_game(btn.mode)
                
                elif self.state == "GAME":
                    if self.game_mode == "quiz":
                        self.quiz_game.handle_event(event)
                    elif self.game_mode == "speed":
                        self.speed_game.handle_event(event)
                    elif self.game_mode == "match":
                        self.match_game.handle_event(event)
                    elif self.game_mode == "timed":
                        self.timed_game.handle_event(event)
            
            # Draw
            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "GAME":
                if self.game_mode == "quiz":
                    self.quiz_game.update()
                    self.quiz_game.draw()
                elif self.game_mode == "speed":
                    self.speed_game.update()
                    self.speed_game.draw()
                elif self.game_mode == "match":
                    self.match_game.update()
                    self.match_game.draw()
                elif self.game_mode == "timed":
                    self.timed_game.update()
                    self.timed_game.draw()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

class QuizGame:
    """Kim Milyoner Olmak Ister tarzi oyun"""
    def __init__(self, game):
        self.game = game
        self.score = 0
        self.question_num = 0
        self.total_questions = 15
        self.current_question = None
        self.options = []
        self.selected_option = None
        self.feedback_timer = 0
        self.feedback_message = ""
        self.is_correct = False
        self.used_pairs = []
        self.game_over = False
        self.prize_ladder = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 
                            64000, 125000, 250000, 500000, 1000000]
        self.generate_question()
        
    def generate_question(self):
        if self.question_num >= self.total_questions:
            return
        
        available_pairs = [p for p in WORD_PAIRS if p not in self.used_pairs]
        if not available_pairs:
            available_pairs = WORD_PAIRS.copy()
            self.used_pairs = []
        
        correct_pair = random.choice(available_pairs)
        self.used_pairs.append(correct_pair)
        
        # Random direction
        if random.choice([True, False]):
            self.current_question = correct_pair[0]
            correct_answer = correct_pair[1]
            wrong_answers = [p[1] for p in WORD_PAIRS if p != correct_pair]
        else:
            self.current_question = correct_pair[1]
            correct_answer = correct_pair[0]
            wrong_answers = [p[0] for p in WORD_PAIRS if p != correct_pair]
        
        wrong_answers = random.sample(wrong_answers, 3)
        self.options = [correct_answer] + wrong_answers
        random.shuffle(self.options)
        self.correct_answer = correct_answer
        
        # Create option buttons
        self.option_buttons = []
        button_width = 500
        button_height = 70
        start_x = WIDTH // 2 - button_width // 2
        start_y = 350
        
        colors = [BLUE, GREEN, ORANGE, PURPLE]
        labels = ["A:", "B:", "C:", "D:"]
        
        for i, (option, color, label) in enumerate(zip(self.options, colors, labels)):
            btn = Button(start_x, start_y + i * 90, button_width, button_height,
                        f"{label} {option}", color, WHITE, 26)
            btn.answer = option
            self.option_buttons.append(btn)
        
        self.selected_option = None
        self.feedback_timer = 0
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.feedback_timer == 0 and not self.game_over:
                for btn in self.option_buttons:
                    if btn.is_clicked(mouse_pos):
                        self.selected_option = btn
                        self.check_answer(btn.answer)
                        break
            
            # Back button
            if hasattr(self, 'back_button') and self.back_button.is_clicked(mouse_pos):
                self.game.state = "MENU"
    
    def check_answer(self, answer):
        if answer == self.correct_answer:
            self.is_correct = True
            self.score = self.prize_ladder[self.question_num]
            self.feedback_message = "DOGRU!"
            self.game.play_sound(self.game.correct_sound)
            self.question_num += 1
        else:
            self.is_correct = False
            self.feedback_message = f"YANLIS! Dogru cevap: {self.correct_answer}"
            self.game.play_sound(self.game.wrong_sound)
            self.game_over = True  # Game ends on wrong answer
        
        self.feedback_timer = 120
    
    def update(self):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            if self.feedback_timer == 0:
                if self.is_correct and self.question_num < self.total_questions and not self.game_over:
                    self.generate_question()
    
    def draw(self):
        self.game.draw_gradient_background(DARK_BLUE, NAVY)
        
        # Header
        header_font = pygame.font.Font(None, 48)
        header = header_font.render("KIM MILYONER OLMAK ISTER?", True, GOLD)
        self.game.screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 30))
        
        # Question number and prize
        info_font = pygame.font.Font(None, 32)
        question_text = info_font.render(f"Soru {self.question_num + 1}/{self.total_questions}", True, WHITE)
        prize_text = info_font.render(f"Odul: TL{self.prize_ladder[min(self.question_num, 14)]:,}", True, GOLD)
        self.game.screen.blit(question_text, (50, 100))
        self.game.screen.blit(prize_text, (WIDTH - prize_text.get_width() - 50, 100))
        
        # Current score
        score_text = info_font.render(f"Kazanilan: TL{self.score:,}", True, GREEN)
        self.game.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 100))
        
        if self.feedback_timer == 0 and self.question_num < self.total_questions and not self.game_over:
            # Question
            question_font = pygame.font.Font(None, 42)
            question_surface = question_font.render(self.current_question, True, WHITE)
            question_rect = pygame.Rect(WIDTH // 2 - 550, 200, 1100, 100)
            pygame.draw.rect(self.game.screen, NAVY, question_rect, border_radius=15)
            pygame.draw.rect(self.game.screen, GOLD, question_rect, 3, border_radius=15)
            self.game.screen.blit(question_surface, 
                                (WIDTH // 2 - question_surface.get_width() // 2, 235))
            
            # Options
            mouse_pos = pygame.mouse.get_pos()
            for btn in self.option_buttons:
                btn.check_hover(mouse_pos)
                btn.draw(self.game.screen)
            
            # Back button at bottom
            self.back_button = Button(50, HEIGHT - 70, 200, 50, "Ana Menuye Don", GRAY, WHITE, 24)
            self.back_button.check_hover(mouse_pos)
            self.back_button.draw(self.game.screen)
        
        elif self.feedback_timer > 0:
            # Feedback
            feedback_font = pygame.font.Font(None, 56)
            color = GREEN if self.is_correct else RED
            feedback = feedback_font.render(self.feedback_message, True, color)
            self.game.screen.blit(feedback, (WIDTH // 2 - feedback.get_width() // 2, 400))
        
        else:
            # Game over
            game_over_font = pygame.font.Font(None, 64)
            if self.question_num >= self.total_questions:
                message = "TEBRIKLER! MILYONER OLDUNUZ!"
                color = GOLD
            else:
                message = "OYUN BITTI!"
                color = RED
            
            game_over = game_over_font.render(message, True, color)
            self.game.screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, 300))
            
            final_score_font = pygame.font.Font(None, 48)
            final_score = final_score_font.render(f"Kazandiginiz Para: TL{self.score:,}", True, WHITE)
            self.game.screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 400))
            
            # Back button
            self.back_button = Button(WIDTH // 2 - 150, 500, 300, 60, "Ana Menuye Don", BLUE)
            mouse_pos = pygame.mouse.get_pos()
            self.back_button.check_hover(mouse_pos)
            self.back_button.draw(self.game.screen)


class SpeedGame:
    """30 saniyede hizli cevaplama oyunu - SURELI"""
    def __init__(self, game):
        self.game = game
        self.score = 0
        self.time_limit = 30
        self.start_time = time.time()
        self.current_question = None
        self.input_text = ""
        self.feedback_timer = 0
        self.feedback_message = ""
        self.is_correct = False
        self.used_pairs = []
        self.questions_answered = 0
        self.generate_question()
        
    def generate_question(self):
        available_pairs = [p for p in WORD_PAIRS if p not in self.used_pairs]
        if not available_pairs:
            available_pairs = WORD_PAIRS.copy()
            self.used_pairs = []
        
        correct_pair = random.choice(available_pairs)
        self.used_pairs.append(correct_pair)
        
        # Random direction
        if random.choice([True, False]):
            self.current_question = correct_pair[0]
            self.correct_answer = correct_pair[1]
        else:
            self.current_question = correct_pair[1]
            self.correct_answer = correct_pair[0]
        
        self.input_text = ""
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.input_text and self.feedback_timer == 0 and not self.is_time_up():
                self.check_answer()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.unicode.isprintable() and len(self.input_text) < 50:
                self.input_text += event.unicode
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if hasattr(self, 'back_button') and self.back_button.is_clicked(mouse_pos):
                self.game.state = "MENU"
    
    def check_answer(self):
        if self.input_text.lower().strip() == self.correct_answer.lower().strip():
            self.is_correct = True
            self.score += 10
            self.questions_answered += 1
            self.feedback_message = "DOGRU! +10 puan"
            self.game.play_sound(self.game.correct_sound)
        else:
            self.is_correct = False
            self.feedback_message = f"YANLIS! Dogru: {self.correct_answer}"
            self.game.play_sound(self.game.wrong_sound)
        
        self.feedback_timer = 60
    
    def update(self):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            if self.feedback_timer == 0 and not self.is_time_up():
                self.generate_question()
    
    def is_time_up(self):
        return time.time() - self.start_time >= self.time_limit
    
    def get_remaining_time(self):
        return max(0, self.time_limit - (time.time() - self.start_time))
    
    def draw(self):
        self.game.draw_gradient_background(RED, DARK_BLUE)
        
        # Header
        header_font = pygame.font.Font(None, 56)
        header = header_font.render("HIZLI YANITLA", True, GOLD)
        self.game.screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 30))
        
        # Timer
        remaining = self.get_remaining_time()
        timer_font = pygame.font.Font(None, 72)
        timer_color = RED if remaining < 10 else WHITE
        timer_text = timer_font.render(f"{int(remaining)}s", True, timer_color)
        self.game.screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 100))
        
        # Score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Puan: {self.score} | Cevaplanan: {self.questions_answered}", True, GOLD)
        self.game.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 180))
        
        # Back button at top
        mouse_pos = pygame.mouse.get_pos()
        self.back_button = Button(50, 30, 200, 50, "Ana Menuye Don", GRAY, WHITE, 24)
        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(self.game.screen)
        
        if not self.is_time_up() and self.feedback_timer == 0:
            # Question
            question_font = pygame.font.Font(None, 48)
            question_surface = question_font.render(self.current_question, True, WHITE)
            question_rect = pygame.Rect(WIDTH // 2 - 550, 250, 1100, 100)
            pygame.draw.rect(self.game.screen, NAVY, question_rect, border_radius=15)
            pygame.draw.rect(self.game.screen, GOLD, question_rect, 3, border_radius=15)
            self.game.screen.blit(question_surface, 
                                (WIDTH // 2 - question_surface.get_width() // 2, 285))
            
            # Input box
            input_rect = pygame.Rect(WIDTH // 2 - 400, 400, 800, 80)
            pygame.draw.rect(self.game.screen, WHITE, input_rect, border_radius=12)
            pygame.draw.rect(self.game.screen, GOLD, input_rect, 4, border_radius=12)
            
            input_font = pygame.font.Font(None, 42)
            input_surface = input_font.render(self.input_text, True, BLACK)
            self.game.screen.blit(input_surface, (input_rect.x + 20, input_rect.y + 25))
            
            # Hint
            hint_font = pygame.font.Font(None, 28)
            hint = hint_font.render("Cevabi yazip ENTER'a basin", True, GRAY)
            self.game.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 500))
        
        elif self.feedback_timer > 0:
            # Feedback
            feedback_font = pygame.font.Font(None, 48)
            color = GREEN if self.is_correct else RED
            feedback = feedback_font.render(self.feedback_message, True, color)
            self.game.screen.blit(feedback, (WIDTH // 2 - feedback.get_width() // 2, 400))
        
        else:
            # Game over
            game_over_font = pygame.font.Font(None, 64)
            game_over = game_over_font.render("SURE BITTI!", True, RED)
            self.game.screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, 300))
            
            final_score_font = pygame.font.Font(None, 48)
            final_score = final_score_font.render(f"Toplam Puan: {self.score}", True, WHITE)
            self.game.screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 380))
            
            answered = final_score_font.render(f"Cevaplanan Soru: {self.questions_answered}", True, GOLD)
            self.game.screen.blit(answered, (WIDTH // 2 - answered.get_width() // 2, 440))
            
            # Back button
            back_btn = Button(WIDTH // 2 - 150, 520, 300, 60, "Ana Menuye Don", BLUE)
            back_btn.check_hover(mouse_pos)
            back_btn.draw(self.game.screen)
            self.back_button = back_btn

class MatchGame:
    """Klasik eslestirme oyunu - SURESIZ"""
    def __init__(self, game):
        self.game = game
        self.score = 0
        self.selected_pairs = random.sample(WORD_PAIRS, 8)
        
        # Create buttons
        self.english_buttons = []
        self.turkish_buttons = []
        
        english_words = [pair[0] for pair in self.selected_pairs]
        turkish_words = [pair[1] for pair in self.selected_pairs]
        random.shuffle(turkish_words)
        
        button_width = 450
        button_height = 65
        
        for i, word in enumerate(english_words):
            btn = Button(50, 180 + i * 75, button_width, button_height, word, BLUE, WHITE, 24)
            btn.matched = False
            btn.word = word
            self.english_buttons.append(btn)
            
        for i, word in enumerate(turkish_words):
            btn = Button(700, 180 + i * 75, button_width, button_height, word, GREEN, WHITE, 24)
            btn.matched = False
            btn.word = word
            self.turkish_buttons.append(btn)
        
        self.selected_english = None
        self.selected_turkish = None
        self.feedback_timer = 0
        self.feedback_message = ""
        self.is_correct = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.feedback_timer == 0 and not self.check_win():
                # Check English buttons
                for btn in self.english_buttons:
                    if btn.is_clicked(mouse_pos) and not btn.matched:
                        if self.selected_english == btn:
                            self.selected_english = None
                        else:
                            self.selected_english = btn
                            self.game.play_sound(self.game.thinking_sound)
                
                # Check Turkish buttons
                for btn in self.turkish_buttons:
                    if btn.is_clicked(mouse_pos) and not btn.matched:
                        if self.selected_turkish == btn:
                            self.selected_turkish = None
                        else:
                            self.selected_turkish = btn
                            self.game.play_sound(self.game.thinking_sound)
                            
                        if self.selected_english and self.selected_turkish:
                            self.check_match()
            
            # Back button
            if hasattr(self, 'back_button') and self.back_button.is_clicked(mouse_pos):
                self.game.state = "MENU"
    
    def check_match(self):
        eng_word = self.selected_english.word
        tur_word = self.selected_turkish.word
        
        correct_match = False
        for pair in self.selected_pairs:
            if pair[0] == eng_word and pair[1] == tur_word:
                correct_match = True
                break
        
        if correct_match:
            self.selected_english.matched = True
            self.selected_turkish.matched = True
            self.selected_english.disabled = True
            self.selected_turkish.disabled = True
            self.score += 10
            self.feedback_message = "MUKEMMEL!"
            self.is_correct = True
            self.game.play_sound(self.game.correct_sound)
        else:
            self.feedback_message = "TEKRAR DENE!"
            self.is_correct = False
            self.game.play_sound(self.game.wrong_sound)
            
        self.feedback_timer = 60
        self.selected_english = None
        self.selected_turkish = None
    
    def check_win(self):
        return all(btn.matched for btn in self.english_buttons)
    
    def update(self):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
    
    def draw(self):
        self.game.draw_gradient_background(DARK_BLUE, NAVY)
        
        # Header
        header_font = pygame.font.Font(None, 56)
        header = header_font.render("KELIME ESLESTIRME", True, GOLD)
        self.game.screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 30))
        
        # Score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Puan: {self.score}", True, GOLD)
        self.game.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 100))
        
        # Instructions
        inst_font = pygame.font.Font(None, 24)
        inst = inst_font.render("Ingilizce ve Turkce kelimeleri eslestirin", True, GRAY)
        self.game.screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, 140))
        
        # Back button at top
        mouse_pos = pygame.mouse.get_pos()
        self.back_button = Button(50, 30, 200, 50, "Ana Menuye Don", GRAY, WHITE, 24)
        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(self.game.screen)
        
        if not self.check_win():
            # Draw buttons
            for btn in self.english_buttons:
                if btn == self.selected_english:
                    btn.color = ORANGE
                elif btn.matched:
                    btn.color = GREEN
                else:
                    btn.color = BLUE
                btn.check_hover(mouse_pos)
                btn.draw(self.game.screen)
                
            for btn in self.turkish_buttons:
                if btn == self.selected_turkish:
                    btn.color = ORANGE
                elif btn.matched:
                    btn.color = GREEN
                else:
                    btn.color = PURPLE
                btn.check_hover(mouse_pos)
                btn.draw(self.game.screen)
            
            # Feedback message
            if self.feedback_timer > 0:
                feedback_font = pygame.font.Font(None, 48)
                color = GREEN if self.is_correct else RED
                feedback = feedback_font.render(self.feedback_message, True, color)
                self.game.screen.blit(feedback, (WIDTH // 2 - feedback.get_width() // 2, HEIGHT - 80))
        
        else:
            # Win message
            win_font = pygame.font.Font(None, 64)
            win_text = win_font.render("TEBRIKLER!", True, GOLD)
            self.game.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 400))
            
            final_score_font = pygame.font.Font(None, 48)
            final_score = final_score_font.render(f"Toplam Puan: {self.score}", True, WHITE)
            self.game.screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 480))
            
            # Back button
            back_btn = Button(WIDTH // 2 - 150, 560, 300, 60, "Ana Menuye Don", BLUE)
            back_btn.check_hover(mouse_pos)
            back_btn.draw(self.game.screen)
            self.back_button = back_btn

class TimedGame:
    """60 saniyede tum kelimeleri bulma oyunu - SURELI"""
    def __init__(self, game):
        self.game = game
        self.score = 0
        self.time_limit = 60
        self.start_time = time.time()
        self.total_words = 10
        self.found_words = []
        self.current_word = None
        self.options = []
        self.feedback_timer = 0
        self.feedback_message = ""
        self.is_correct = False
        self.used_pairs = []
        self.generate_question()
        
    def generate_question(self):
        if len(self.found_words) >= self.total_words:
            return
        
        available_pairs = [p for p in WORD_PAIRS if p not in self.used_pairs]
        if not available_pairs:
            available_pairs = WORD_PAIRS.copy()
            self.used_pairs = []
        
        correct_pair = random.choice(available_pairs)
        self.used_pairs.append(correct_pair)
        
        # Random direction
        if random.choice([True, False]):
            self.current_word = correct_pair[0]
            correct_answer = correct_pair[1]
            wrong_answers = [p[1] for p in WORD_PAIRS if p != correct_pair]
        else:
            self.current_word = correct_pair[1]
            correct_answer = correct_pair[0]
            wrong_answers = [p[0] for p in WORD_PAIRS if p != correct_pair]
        
        wrong_answers = random.sample(wrong_answers, 3)
        self.options = [correct_answer] + wrong_answers
        random.shuffle(self.options)
        self.correct_answer = correct_answer
        
        # Create option buttons
        self.option_buttons = []
        button_width = 500
        button_height = 70
        
        colors = [BLUE, GREEN, ORANGE, PURPLE]
        
        for i, (option, color) in enumerate(zip(self.options, colors)):
            x = 100 if i < 2 else 600
            y = 400 if i % 2 == 0 else 490
            btn = Button(x, y, button_width, button_height, option, color, WHITE, 26)
            btn.answer = option
            self.option_buttons.append(btn)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.feedback_timer == 0 and not self.is_time_up() and len(self.found_words) < self.total_words:
                for btn in self.option_buttons:
                    if btn.is_clicked(mouse_pos):
                        self.check_answer(btn.answer)
                        break
            
            # Back button
            if hasattr(self, 'back_button') and self.back_button.is_clicked(mouse_pos):
                self.game.state = "MENU"
    
    def check_answer(self, answer):
        if answer == self.correct_answer:
            self.is_correct = True
            self.score += 10
            self.found_words.append(self.current_word)
            self.feedback_message = f"DOGRU! {len(self.found_words)}/{self.total_words}"
            self.game.play_sound(self.game.correct_sound)
        else:
            self.is_correct = False
            self.feedback_message = "YANLIS!"
            self.game.play_sound(self.game.wrong_sound)
        
        self.feedback_timer = 45
    
    def update(self):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            if self.feedback_timer == 0 and not self.is_time_up() and len(self.found_words) < self.total_words:
                self.generate_question()
    
    def is_time_up(self):
        return time.time() - self.start_time >= self.time_limit
    
    def get_remaining_time(self):
        return max(0, self.time_limit - (time.time() - self.start_time))
    
    def draw(self):
        self.game.draw_gradient_background(ORANGE, DARK_BLUE)
        
        # Header
        header_font = pygame.font.Font(None, 56)
        header = header_font.render("ZAMANA KARSI", True, GOLD)
        self.game.screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 30))
        
        # Timer and progress
        remaining = self.get_remaining_time()
        timer_font = pygame.font.Font(None, 64)
        timer_color = RED if remaining < 15 else WHITE
        timer_text = timer_font.render(f"{int(remaining)}s", True, timer_color)
        self.game.screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 100))
        
        # Progress
        progress_font = pygame.font.Font(None, 36)
        progress_text = progress_font.render(f"Ilerleme: {len(self.found_words)}/{self.total_words}", True, GOLD)
        self.game.screen.blit(progress_text, (WIDTH // 2 - progress_text.get_width() // 2, 180))
        
        # Score
        score_text = progress_font.render(f"Puan: {self.score}", True, WHITE)
        self.game.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 220))
        
        # Back button at top
        mouse_pos = pygame.mouse.get_pos()
        self.back_button = Button(50, 30, 200, 50, "Ana Menuye Don", GRAY, WHITE, 24)
        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(self.game.screen)
        
        if not self.is_time_up() and len(self.found_words) < self.total_words and self.feedback_timer == 0:
            # Question
            question_font = pygame.font.Font(None, 48)
            question_surface = question_font.render(self.current_word, True, WHITE)
            question_rect = pygame.Rect(WIDTH // 2 - 550, 280, 1100, 90)
            pygame.draw.rect(self.game.screen, NAVY, question_rect, border_radius=15)
            pygame.draw.rect(self.game.screen, GOLD, question_rect, 3, border_radius=15)
            self.game.screen.blit(question_surface, 
                                (WIDTH // 2 - question_surface.get_width() // 2, 310))
            
            # Options
            for btn in self.option_buttons:
                btn.check_hover(mouse_pos)
                btn.draw(self.game.screen)
        
        elif self.feedback_timer > 0:
            # Feedback
            feedback_font = pygame.font.Font(None, 56)
            color = GREEN if self.is_correct else RED
            feedback = feedback_font.render(self.feedback_message, True, color)
            self.game.screen.blit(feedback, (WIDTH // 2 - feedback.get_width() // 2, 450))
        
        else:
            # Game over
            game_over_font = pygame.font.Font(None, 64)
            if len(self.found_words) >= self.total_words:
                message = "TEBRIKLER! KAZANDIN!"
                color = GOLD
            else:
                message = "SURE BITTI!"
                color = RED
            
            game_over = game_over_font.render(message, True, color)
            self.game.screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, 350))
            
            final_score_font = pygame.font.Font(None, 48)
            final_score = final_score_font.render(f"Toplam Puan: {self.score}", True, WHITE)
            self.game.screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 430))
            
            found = final_score_font.render(f"Bulunan Kelime: {len(self.found_words)}/{self.total_words}", True, GOLD)
            self.game.screen.blit(found, (WIDTH // 2 - found.get_width() // 2, 490))
            
            # Back button
            back_btn = Button(WIDTH // 2 - 150, 560, 300, 60, "Ana Menuye Don", BLUE)
            back_btn.check_hover(mouse_pos)
            back_btn.draw(self.game.screen)
            self.back_button = back_btn

if __name__ == "__main__":
    game = Game()
    game.run()
