import pygame
import random
from enum import Enum
from .config import *

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        # Start in the center
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        
        self.body = [(start_x, start_y)]
        for i in range(1, INITIAL_SNAKE_LENGTH):
            self.body.append((start_x - i, start_y))
            
        self.direction = Direction.RIGHT
        self.grow_pending = False
        
    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        self.body.insert(0, new_head)
        
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False
            
    def grow(self):
        self.grow_pending = True
        
    def change_direction(self, new_direction):
        # Prevent snake from going backwards into itself
        if len(self.body) > 1:
            current_dx, current_dy = self.direction.value
            new_dx, new_dy = new_direction.value
            if (current_dx, current_dy) != (-new_dx, -new_dy):
                self.direction = new_direction
        else:
            self.direction = new_direction
            
    def check_collision(self):
        head_x, head_y = self.body[0]
        
        # Check wall collision
        if (head_x < 0 or head_x >= GRID_WIDTH or 
            head_y < 0 or head_y >= GRID_HEIGHT):
            return True
            
        # Check self collision
        if (head_x, head_y) in self.body[1:]:
            return True
            
        return False
        
    def draw(self, screen):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if i == 0:  # Head
                pygame.draw.rect(screen, DARK_GREEN, rect)
                pygame.draw.rect(screen, GREEN, rect, 2)
                # Draw eyes
                eye_size = GRID_SIZE // 6
                if self.direction == Direction.UP:
                    eye1_pos = (x * GRID_SIZE + GRID_SIZE//4, y * GRID_SIZE + GRID_SIZE//4)
                    eye2_pos = (x * GRID_SIZE + 3*GRID_SIZE//4, y * GRID_SIZE + GRID_SIZE//4)
                elif self.direction == Direction.DOWN:
                    eye1_pos = (x * GRID_SIZE + GRID_SIZE//4, y * GRID_SIZE + 3*GRID_SIZE//4)
                    eye2_pos = (x * GRID_SIZE + 3*GRID_SIZE//4, y * GRID_SIZE + 3*GRID_SIZE//4)
                elif self.direction == Direction.LEFT:
                    eye1_pos = (x * GRID_SIZE + GRID_SIZE//4, y * GRID_SIZE + GRID_SIZE//4)
                    eye2_pos = (x * GRID_SIZE + GRID_SIZE//4, y * GRID_SIZE + 3*GRID_SIZE//4)
                else:  # RIGHT
                    eye1_pos = (x * GRID_SIZE + 3*GRID_SIZE//4, y * GRID_SIZE + GRID_SIZE//4)
                    eye2_pos = (x * GRID_SIZE + 3*GRID_SIZE//4, y * GRID_SIZE + 3*GRID_SIZE//4)
                
                pygame.draw.circle(screen, WHITE, eye1_pos, eye_size)
                pygame.draw.circle(screen, WHITE, eye2_pos, eye_size)
            else:  # Body
                pygame.draw.rect(screen, GREEN, rect)
                pygame.draw.rect(screen, DARK_GREEN, rect, 1)

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)
        self.animation_time = 0
        
    def generate_position(self, snake_body):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_body:
                return (x, y)
                
    def draw(self, screen, dt):
        self.animation_time += dt
        x, y = self.position
        
        # Pulsing animation
        pulse = abs(pygame.math.Vector2.from_polar((1, self.animation_time * 200)).y) * 0.1 + 0.9
        size = int(GRID_SIZE * pulse)
        
        rect = pygame.Rect(
            x * GRID_SIZE + (GRID_SIZE - size) // 2,
            y * GRID_SIZE + (GRID_SIZE - size) // 2,
            size, size
        )
        pygame.draw.ellipse(screen, RED, rect)
        pygame.draw.ellipse(screen, YELLOW, rect, 2)
        
class GameEngine:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False
        self.paused = False
        
    def reset(self):
        self.snake.reset()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False
        self.paused = False
        
    def update(self, dt):
        if self.game_over or self.paused:
            return
            
        self.snake.move()
        
        # Check collision with walls or self
        if self.snake.check_collision():
            self.game_over = True
            return
            
        # Check collision with food
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.score += 10
            self.food = Food(self.snake.body)
            
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.snake.change_direction(Direction.UP)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.snake.change_direction(Direction.DOWN)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.snake.change_direction(Direction.LEFT)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.snake.change_direction(Direction.RIGHT)
            elif event.key == pygame.K_SPACE:
                if self.game_over:
                    self.reset()
                else:
                    self.paused = not self.paused
                    
    def draw(self, screen, dt):
        screen.fill(BLACK)
        
        # Draw grid (optional)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))
            
        self.food.draw(screen, dt)
        self.snake.draw(screen)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw game over or pause overlay
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            font_big = pygame.font.Font(None, 72)
            game_over_text = font_big.render("GAME OVER", True, RED)
            restart_text = font.render("Press SPACE to restart", True, WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            
            screen.blit(game_over_text, game_over_rect)
            screen.blit(restart_text, restart_rect)
            
        elif self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            font_big = pygame.font.Font(None, 72)
            pause_text = font_big.render("PAUSED", True, WHITE)
            resume_text = font.render("Press SPACE to resume", True, WHITE)
            
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
            resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
            
            screen.blit(pause_text, pause_rect)
            screen.blit(resume_text, resume_rect)