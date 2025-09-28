import pygame
import math
from enum import Enum
from .config import *

class MenuState(Enum):
    MAIN_MENU = 0
    SETTINGS = 1
    HIGH_SCORES = 2
    GAME = 3
    CREDITS = 4

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        self.click_animation = 0
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.click_animation = 0.3
                if self.action:
                    return self.action()
        return None
        
    def update(self, dt):
        if self.click_animation > 0:
            self.click_animation -= dt * 3
            if self.click_animation < 0:
                self.click_animation = 0
                
    def draw(self, screen, font):
        # Button color based on state
        if self.click_animation > 0:
            color = BLUE
        elif self.hovered:
            color = LIGHT_GRAY
        else:
            color = GRAY
            
        # Draw button with slight animation
        offset = int(self.click_animation * 3)
        draw_rect = self.rect.copy()
        draw_rect.x += offset
        draw_rect.y += offset
        
        pygame.draw.rect(screen, color, draw_rect)
        pygame.draw.rect(screen, WHITE, draw_rect, 2)
        
        # Draw text
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=draw_rect.center)
        screen.blit(text_surface, text_rect)

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def add_particle(self, x, y, vx, vy, color, life):
        self.particles.append({
            'x': x, 'y': y, 'vx': vx, 'vy': vy,
            'color': color, 'life': life, 'max_life': life
        })
        
    def update(self, dt):
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['life'] -= dt
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def draw(self, screen):
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            color = (*particle['color'][:3], alpha)
            
            # Create surface for alpha blending
            surf = pygame.Surface((4, 4), pygame.SRCALPHA)
            surf.fill(color)
            screen.blit(surf, (int(particle['x']), int(particle['y'])))

class MenuManager:
    def __init__(self, score_manager):
        self.state = MenuState.MAIN_MENU
        self.font_large = pygame.font.Font(None, MENU_FONT_SIZE)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, SMALL_FONT_SIZE)
        self.score_manager = score_manager
        self.particles = ParticleSystem()
        self.background_time = 0
        self.fade_alpha = 255
        self.transition_speed = 300
        
        self.setup_buttons()
        
    def setup_buttons(self):
        center_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2 - 50
        
        self.main_buttons = [
            Button(center_x - BUTTON_WIDTH//2, start_y, BUTTON_WIDTH, BUTTON_HEIGHT, 
                   "New Game", lambda: MenuState.GAME),
            Button(center_x - BUTTON_WIDTH//2, start_y + 70, BUTTON_WIDTH, BUTTON_HEIGHT, 
                   "High Scores", lambda: MenuState.HIGH_SCORES),
            Button(center_x - BUTTON_WIDTH//2, start_y + 140, BUTTON_WIDTH, BUTTON_HEIGHT, 
                   "Settings", lambda: MenuState.SETTINGS),
            Button(center_x - BUTTON_WIDTH//2, start_y + 210, BUTTON_WIDTH, BUTTON_HEIGHT, 
                   "Credits", lambda: MenuState.CREDITS),
            Button(center_x - BUTTON_WIDTH//2, start_y + 280, BUTTON_WIDTH, BUTTON_HEIGHT, 
                   "Exit", lambda: "exit")
        ]
        
        self.back_button = Button(50, SCREEN_HEIGHT - 80, 100, 40, "Back", 
                                  lambda: MenuState.MAIN_MENU)
        
    def handle_event(self, event):
        if self.state == MenuState.MAIN_MENU:
            for button in self.main_buttons:
                result = button.handle_event(event)
                if result:
                    if result == "exit":
                        return "exit"
                    else:
                        self.state = result
                        self.fade_alpha = 255
                        return None
        else:
            result = self.back_button.handle_event(event)
            if result:
                self.state = result
                self.fade_alpha = 255
                
        return None
        
    def update(self, dt):
        # Update background animation
        self.background_time += dt
        
        # Update fade transition
        if self.fade_alpha > 0:
            self.fade_alpha -= self.transition_speed * dt
            if self.fade_alpha < 0:
                self.fade_alpha = 0
                
        # Update particles
        if self.state == MenuState.MAIN_MENU:
            # Add background particles
            if len(self.particles.particles) < 50:
                import random
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                vx = random.randint(-50, 50)
                vy = random.randint(-50, 50)
                color = random.choice([GREEN, BLUE, YELLOW, WHITE])
                self.particles.add_particle(x, y, vx, vy, color, 3.0)
                
        self.particles.update(dt)
        
        # Update buttons
        if self.state == MenuState.MAIN_MENU:
            for button in self.main_buttons:
                button.update(dt)
        else:
            self.back_button.update(dt)
            
        return self.state
        
    def draw_animated_background(self, screen):
        # Animated grid background
        offset = (self.background_time * 20) % (GRID_SIZE * 2)
        
        for x in range(-GRID_SIZE, SCREEN_WIDTH + GRID_SIZE, GRID_SIZE * 2):
            alpha = int(30 + 20 * math.sin(self.background_time + x * 0.01))
            color = (*DARK_GREEN, alpha)
            pygame.draw.line(screen, DARK_GREEN, 
                           (x + offset, 0), (x + offset, SCREEN_HEIGHT))
                           
        for y in range(-GRID_SIZE, SCREEN_HEIGHT + GRID_SIZE, GRID_SIZE * 2):
            alpha = int(30 + 20 * math.sin(self.background_time + y * 0.01))
            pygame.draw.line(screen, DARK_GREEN, 
                           (0, y + offset), (SCREEN_WIDTH, y + offset))
        
    def draw(self, screen):
        screen.fill(BLACK)
        self.draw_animated_background(screen)
        self.particles.draw(screen)
        
        if self.state == MenuState.MAIN_MENU:
            self.draw_main_menu(screen)
        elif self.state == MenuState.HIGH_SCORES:
            self.draw_high_scores(screen)
        elif self.state == MenuState.SETTINGS:
            self.draw_settings(screen)
        elif self.state == MenuState.CREDITS:
            self.draw_credits(screen)
            
        # Draw fade transition
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.set_alpha(int(self.fade_alpha))
            fade_surface.fill(BLACK)
            screen.blit(fade_surface, (0, 0))
            
    def draw_main_menu(self, screen):
        # Title with animation
        title_bounce = math.sin(self.background_time * 2) * 10
        title_text = self.font_large.render("SNAKE GAME", True, GREEN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150 + title_bounce))
        
        # Title shadow
        shadow_text = self.font_large.render("SNAKE GAME", True, DARK_GREEN)
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH//2 + 3, 153 + title_bounce))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)
        
        # Draw buttons
        for button in self.main_buttons:
            button.draw(screen, self.font_medium)
            
    def draw_high_scores(self, screen):
        title_text = self.font_large.render("HIGH SCORES", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title_text, title_rect)
        
        scores = self.score_manager.get_high_scores()
        
        for i, score in enumerate(scores[:10]):
            score_text = self.font_medium.render(
                f"{i+1:2d}. {score['name']:<15} {score['score']:>6d}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 180 + i * 35))
            screen.blit(score_text, score_rect)
            
        if not scores:
            no_scores_text = self.font_medium.render("No high scores yet!", True, GRAY)
            no_scores_rect = no_scores_text.get_rect(center=(SCREEN_WIDTH//2, 300))
            screen.blit(no_scores_text, no_scores_rect)
            
        self.back_button.draw(screen, self.font_small)
        
    def draw_settings(self, screen):
        title_text = self.font_large.render("SETTINGS", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title_text, title_rect)
        
        # Settings options (placeholder)
        settings_text = [
            "Game Speed: Normal",
            "Sound: On",
            "Grid: Visible",
            "Controls: Arrow Keys / WASD"
        ]
        
        for i, text in enumerate(settings_text):
            setting_text = self.font_medium.render(text, True, WHITE)
            setting_rect = setting_text.get_rect(center=(SCREEN_WIDTH//2, 200 + i * 50))
            screen.blit(setting_text, setting_rect)
            
        self.back_button.draw(screen, self.font_small)
        
    def draw_credits(self, screen):
        title_text = self.font_large.render("CREDITS", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title_text, title_rect)
        
        credits_text = [
            "Snake Game",
            "",
            "Created with Python & Pygame",
            "",
            "Controls:",
            "Arrow Keys or WASD - Move",
            "Space - Pause/Restart",
            "ESC - Main Menu",
            "",
            "Have fun!"
        ]
        
        for i, text in enumerate(credits_text):
            if text:
                color = GREEN if text in ["Snake Game", "Have fun!"] else WHITE
                credit_text = self.font_small.render(text, True, color)
                credit_rect = credit_text.get_rect(center=(SCREEN_WIDTH//2, 180 + i * 25))
                screen.blit(credit_text, credit_rect)
                
        self.back_button.draw(screen, self.font_small)