# Configuration file for Snake Game
import pygame

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 150, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
YELLOW = (255, 255, 0)

# Game settings
SNAKE_SPEED = 8
INITIAL_SNAKE_LENGTH = 3

# File paths
SCORES_FILE = "data/scores.json"
SETTINGS_FILE = "data/settings.json"

# Menu settings
MENU_FONT_SIZE = 48
SMALL_FONT_SIZE = 24
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Animation settings
FADE_SPEED = 5
ANIMATION_SPEED = 0.1