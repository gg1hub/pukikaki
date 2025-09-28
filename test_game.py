#!/usr/bin/env python3
"""
Snake Game Test Suite
Tests all game functionality without requiring a display.
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import pygame
        print("✅ pygame imported")
        
        from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, SNAKE_SPEED
        print("✅ game.config imported")
        
        from game.snake import Snake, Food, GameEngine, Direction
        print("✅ game.snake imported")
        
        from game.menu import MenuManager, MenuState
        print("✅ game.menu imported")
        
        from game.score_manager import ScoreManager
        print("✅ game.score_manager imported")
        
        from game.sound_manager import SoundManager
        print("✅ game.sound_manager imported")
        
        from game.input_dialog import InputDialog
        print("✅ game.input_dialog imported")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_game_logic():
    """Test game logic without display"""
    print("\n🧪 Testing game logic...")
    
    try:
        # Initialize pygame without display
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        import pygame
        pygame.init()
        
        from game.snake import Snake, GameEngine, Direction
        
        # Test snake creation
        snake = Snake()
        initial_length = len(snake.body)
        print(f"✅ Snake created with {initial_length} segments")
        
        # Test snake movement
        old_head = snake.body[0]
        snake.move()
        new_head = snake.body[0]
        assert old_head != new_head, "Snake should move"
        print("✅ Snake movement works")
        
        # Test snake growth
        snake.grow()
        snake.move()
        assert len(snake.body) > initial_length, "Snake should grow"
        print("✅ Snake growth works")
        
        # Test direction change
        snake.change_direction(Direction.UP)
        assert snake.direction == Direction.UP, "Direction should change"
        print("✅ Direction change works")
        
        # Test game engine
        engine = GameEngine()
        initial_score = engine.score
        print(f"✅ GameEngine created with score {initial_score}")
        
        return True
    except Exception as e:
        print(f"❌ Game logic test failed: {e}")
        return False

def test_score_system():
    """Test score management system"""
    print("\n🧪 Testing score system...")
    
    try:
        from game.score_manager import ScoreManager
        
        # Create score manager
        score_mgr = ScoreManager()
        print("✅ ScoreManager created")
        
        # Test adding scores
        initial_count = len(score_mgr.get_high_scores())
        score_mgr.add_score("TestPlayer", 150)
        score_mgr.add_score("TestPlayer2", 200)
        
        scores = score_mgr.get_high_scores()
        assert len(scores) >= 2, "Scores should be added"
        assert scores[0]['score'] >= scores[1]['score'], "Scores should be sorted"
        print("✅ Score addition and sorting works")
        
        # Test high score detection
        assert score_mgr.is_high_score(1000), "High score should be detected"
        print("✅ High score detection works")
        
        return True
    except Exception as e:
        print(f"❌ Score system test failed: {e}")
        return False

def test_sound_system():
    """Test sound system (without actually playing sounds)"""
    print("\n🧪 Testing sound system...")
    
    try:
        from game.sound_manager import SoundManager
        
        # Create sound manager
        sound_mgr = SoundManager()
        print("✅ SoundManager created")
        
        # Test sound playing (should not crash even if no audio)
        sound_mgr.play_sound('eat')
        sound_mgr.play_sound('game_over')
        print("✅ Sound playing works")
        
        # Test volume control
        sound_mgr.set_volume(0.5)
        assert sound_mgr.volume == 0.5, "Volume should be set"
        print("✅ Volume control works")
        
        # Test sound toggle
        enabled = sound_mgr.toggle_sound()
        print(f"✅ Sound toggle works (enabled: {enabled})")
        
        return True
    except Exception as e:
        print(f"❌ Sound system test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 SNAKE GAME TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Game Logic Test", test_game_logic),
        ("Score System Test", test_score_system),
        ("Sound System Test", test_sound_system),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED\n")
            else:
                print(f"❌ {test_name} FAILED\n")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}\n")
    
    print("=" * 60)
    print(f"🏁 TEST RESULTS: {passed}/{total} PASSED")
    print("=" * 60)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Game is ready to play!")
        return True
    else:
        print("⚠️  Some tests failed. Check the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)