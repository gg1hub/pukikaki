#!/usr/bin/env python3
"""
Snake Game - Main Application
A complete Snake game with menus, high scores, animations, and sound effects.
"""

import pygame
import sys
import os
from game.config import *
from game.snake import GameEngine
from game.menu import MenuManager, MenuState
from game.score_manager import ScoreManager
from game.sound_manager import SoundManager
from game.input_dialog import InputDialog

class SnakeGame:
    def __init__(self):
        pygame.init()
        
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        
        # Set up clock
        self.clock = pygame.time.Clock()
        
        # Initialize game components
        self.score_manager = ScoreManager()
        self.sound_manager = SoundManager()
        self.menu_manager = MenuManager(self.score_manager)
        self.game_engine = GameEngine()
        
        # Game state
        self.current_state = MenuState.MAIN_MENU
        self.running = True
        self.game_timer = 0
        self.input_dialog = None
        
        # Try to set icon (if available)
        try:
            icon_path = "assets/icon.png"
            if os.path.exists(icon_path):
                icon = pygame.image.load(icon_path)
                pygame.display.set_icon(icon)
        except:
            pass  # Icon not found or couldn't load
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
                
            # Handle input dialog events
            if self.input_dialog and self.input_dialog.active:
                result = self.input_dialog.handle_event(event)
                if result == "continue":
                    continue
                elif result:  # Player name entered
                    rank = self.score_manager.add_score(result, self.game_engine.score)
                    self.sound_manager.play_sound('menu_select')
                    self.input_dialog = None
                    self.current_state = MenuState.HIGH_SCORES
                    self.menu_manager.state = MenuState.HIGH_SCORES
                else:  # Dialog cancelled
                    self.input_dialog = None
                    self.current_state = MenuState.MAIN_MENU
                    self.menu_manager.state = MenuState.MAIN_MENU
                continue
                
            # Global key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_state == MenuState.GAME:
                        self.current_state = MenuState.MAIN_MENU
                        self.menu_manager.state = MenuState.MAIN_MENU
                        self.sound_manager.play_sound('menu_select')
                    elif self.current_state != MenuState.MAIN_MENU:
                        self.current_state = MenuState.MAIN_MENU
                        self.menu_manager.state = MenuState.MAIN_MENU
                        self.sound_manager.play_sound('menu_select')
                        
            # Handle menu events
            if self.current_state != MenuState.GAME:
                # Mouse hover sound for buttons
                if event.type == pygame.MOUSEMOTION:
                    # This is a simplified check - in a real implementation
                    # you might want to track when hover state changes
                    pass
                    
                result = self.menu_manager.handle_event(event)
                if result == "exit":
                    self.running = False
                    return
                elif result == MenuState.GAME:
                    self.start_new_game()
                    self.sound_manager.play_sound('menu_select')
                    
            # Handle game events
            elif self.current_state == MenuState.GAME:
                self.game_engine.handle_input(event)
                
    def start_new_game(self):
        """Start a new game"""
        self.current_state = MenuState.GAME
        self.game_engine.reset()
        self.game_timer = 0
        
    def update(self, dt):
        """Update game state"""
        if self.input_dialog and self.input_dialog.active:
            self.input_dialog.update(dt)
            return
            
        # Update menu
        if self.current_state != MenuState.GAME:
            menu_state = self.menu_manager.update(dt)
            if menu_state == MenuState.GAME and self.current_state != MenuState.GAME:
                self.start_new_game()
        
        # Update game
        elif self.current_state == MenuState.GAME:
            self.game_timer += dt
            
            # Update game at fixed intervals
            if self.game_timer >= 1.0 / SNAKE_SPEED:
                old_score = self.game_engine.score
                self.game_engine.update(dt)
                
                # Check for score increase (food eaten)
                if self.game_engine.score > old_score:
                    self.sound_manager.play_sound('eat')
                
                # Check for game over
                if self.game_engine.game_over:
                    self.sound_manager.play_sound('game_over')
                    
                    # Check for high score
                    if self.score_manager.is_high_score(self.game_engine.score):
                        self.input_dialog = InputDialog("New High Score! Enter your name:")
                    
                self.game_timer = 0
                
    def draw(self, dt):
        """Draw everything"""
        if self.current_state == MenuState.GAME:
            self.game_engine.draw(self.screen, dt)
        else:
            self.menu_manager.draw(self.screen)
            
        # Draw input dialog on top if active
        if self.input_dialog and self.input_dialog.active:
            self.input_dialog.draw(self.screen)
            
        pygame.display.flip()
        
    def run(self):
        """Main game loop"""
        print("Starting Snake Game...")
        
        try:
            while self.running:
                dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
                
                self.handle_events()
                if not self.running:
                    break
                    
                self.update(dt)
                self.draw(dt)
                
        except KeyboardInterrupt:
            print("Game interrupted by user")
        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up...")
        pygame.quit()
        
def main():
    """Entry point for the game"""
    # Check if pygame is available
    try:
        import pygame
    except ImportError:
        print("Pygame is not installed!")
        print("Please run: pip install pygame")
        return 1
        
    # Check if we can initialize pygame
    try:
        pygame.init()
        pygame.quit()
    except Exception as e:
        print(f"Could not initialize pygame: {e}")
        return 1
        
    # Run the game
    game = SnakeGame()
    game.run()
    return 0

if __name__ == "__main__":
    sys.exit(main())