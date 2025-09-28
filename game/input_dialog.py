import pygame
from .config import *

class InputDialog:
    def __init__(self, prompt, max_length=15):
        self.prompt = prompt
        self.text = ""
        self.max_length = max_length
        self.active = True
        self.cursor_visible = True
        self.cursor_timer = 0
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Dialog dimensions
        self.width = 400
        self.height = 200
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
        
    def handle_event(self, event):
        if not self.active:
            return None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Return the entered text (or "Player" if empty)
                result = self.text.strip() if self.text.strip() else "Player"
                self.active = False
                return result
            elif event.key == pygame.K_ESCAPE:
                # Cancel dialog
                self.active = False
                return None
            elif event.key == pygame.K_BACKSPACE:
                # Remove last character
                self.text = self.text[:-1]
            else:
                # Add character if it's printable and within limit
                if len(self.text) < self.max_length:
                    char = event.unicode
                    if char.isprintable():
                        self.text += char
                        
        return "continue"
        
    def update(self, dt):
        # Update cursor blinking
        self.cursor_timer += dt
        if self.cursor_timer >= 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
            
    def draw(self, screen):
        if not self.active:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Draw dialog box
        dialog_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, GRAY, dialog_rect)
        pygame.draw.rect(screen, WHITE, dialog_rect, 3)
        
        # Draw prompt
        prompt_text = self.font.render(self.prompt, True, WHITE)
        prompt_rect = prompt_text.get_rect(center=(self.x + self.width//2, self.y + 40))
        screen.blit(prompt_text, prompt_rect)
        
        # Draw input box
        input_box = pygame.Rect(self.x + 20, self.y + 80, self.width - 40, 40)
        pygame.draw.rect(screen, WHITE, input_box)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        
        # Draw text
        display_text = self.text
        if self.cursor_visible:
            display_text += "|"
            
        text_surface = self.font.render(display_text, True, BLACK)
        text_rect = text_surface.get_rect(left=input_box.left + 5, centery=input_box.centery)
        
        # Clip text to fit in input box
        clipped_surface = text_surface.subsurface((0, 0, min(text_surface.get_width(), input_box.width - 10), text_surface.get_height()))
        screen.blit(clipped_surface, text_rect)
        
        # Draw instructions
        instruction_text = self.small_font.render("Press ENTER to confirm, ESC to cancel", True, LIGHT_GRAY)
        instruction_rect = instruction_text.get_rect(center=(self.x + self.width//2, self.y + 160))
        screen.blit(instruction_text, instruction_rect)