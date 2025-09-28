import json
import os
from datetime import datetime
from .config import SCORES_FILE

class ScoreManager:
    def __init__(self):
        self.scores = []
        self.ensure_data_dir()
        self.load_scores()
        
    def ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        data_dir = os.path.dirname(SCORES_FILE)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
    def load_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(SCORES_FILE):
                with open(SCORES_FILE, 'r') as f:
                    self.scores = json.load(f)
        except Exception as e:
            print(f"Error loading scores: {e}")
            self.scores = []
            
    def save_scores(self):
        """Save high scores to file"""
        try:
            with open(SCORES_FILE, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except Exception as e:
            print(f"Error saving scores: {e}")
            
    def add_score(self, player_name, score):
        """Add a new score to the high score list"""
        new_score = {
            'name': player_name.strip()[:15],  # Limit name length
            'score': score,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.scores.append(new_score)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Keep only top 10 scores
        self.scores = self.scores[:10]
        
        self.save_scores()
        
        # Return the rank (1-based)
        for i, score_entry in enumerate(self.scores):
            if (score_entry['name'] == new_score['name'] and 
                score_entry['score'] == new_score['score'] and
                score_entry['date'] == new_score['date']):
                return i + 1
                
        return None
        
    def get_high_scores(self):
        """Get the current high score list"""
        return self.scores.copy()
        
    def is_high_score(self, score):
        """Check if a score qualifies as a high score"""
        if len(self.scores) < 10:
            return True
        return score > self.scores[-1]['score']
        
    def get_rank(self, score):
        """Get the rank a score would have"""
        rank = 1
        for high_score in self.scores:
            if score > high_score['score']:
                break
            rank += 1
        return rank