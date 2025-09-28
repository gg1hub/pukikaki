import pygame
import os

class SoundManager:
    def __init__(self):
        self.enabled = True
        self.volume = 0.7
        self.sounds = {}
        self.music_playing = False
        
        # Initialize pygame mixer if not already done
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        except pygame.error as e:
            print(f"Warning: Could not initialize sound system: {e}")
            self.enabled = False
            
        if self.enabled:
            self.create_procedural_sounds()
        else:
            # Create empty sound dictionary for silent mode
            self.sounds = {
                'eat': None,
                'game_over': None,
                'menu_select': None,
                'menu_navigate': None
            }
        
    def create_procedural_sounds(self):
        """Create simple procedural sounds using pygame"""
        # Food pickup sound - short beep
        self.sounds['eat'] = self.create_beep(440, 0.1)
        
        # Game over sound - descending tone
        self.sounds['game_over'] = self.create_descending_tone(440, 220, 0.5)
        
        # Menu select sound
        self.sounds['menu_select'] = self.create_beep(660, 0.05)
        
        # Menu navigate sound
        self.sounds['menu_navigate'] = self.create_beep(550, 0.03)
        
    def create_beep(self, frequency, duration):
        """Create a simple beep sound"""
        try:
            import numpy as np
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
            # Create numpy array for better performance and compatibility
            arr = np.zeros((frames, 2), dtype=np.int16)
            
            for i in range(frames):
                time_point = float(i) / sample_rate
                # Sine wave with fade out
                amplitude = 4096 * (1 - time_point / duration)
                wave = amplitude * pygame.math.Vector2(1, 0).rotate(frequency * time_point * 360).y
                arr[i] = [int(wave), int(wave)]
                
            sound = pygame.sndarray.make_sound(arr)
            return sound
        except ImportError:
            # Fallback without numpy - create empty sound
            try:
                # Create minimal silent sound as fallback
                import array
                sample_rate = 22050
                frames = int(0.1 * sample_rate)  # Short silent sound
                arr = array.array('h', [0] * (frames * 2))
                sound = pygame.sndarray.make_sound(arr)
                return sound
            except:
                # Ultimate fallback - return None
                return None
        
    def create_descending_tone(self, start_freq, end_freq, duration):
        """Create a descending tone"""
        try:
            import numpy as np
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
            # Create numpy array
            arr = np.zeros((frames, 2), dtype=np.int16)
            
            for i in range(frames):
                time_point = float(i) / sample_rate
                progress = time_point / duration
                
                # Linear frequency interpolation
                frequency = start_freq + (end_freq - start_freq) * progress
                
                # Fade out amplitude
                amplitude = 4096 * (1 - progress)
                
                wave = amplitude * pygame.math.Vector2(1, 0).rotate(frequency * time_point * 360).y
                arr[i] = [int(wave), int(wave)]
                
            sound = pygame.sndarray.make_sound(arr)
            return sound
        except ImportError:
            # Fallback without numpy - create silent sound
            try:
                import array
                sample_rate = 22050
                frames = int(0.1 * sample_rate)  # Short silent sound
                arr = array.array('h', [0] * (frames * 2))
                sound = pygame.sndarray.make_sound(arr)
                return sound
            except:
                return None
        
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if not self.enabled or sound_name not in self.sounds:
            return
        
        sound = self.sounds[sound_name]
        if sound is None:  # Sound creation failed
            return
            
        try:
            sound.set_volume(self.volume)
            sound.play()
        except Exception as e:
            print(f"Error playing sound {sound_name}: {e}")
            
    def set_volume(self, volume):
        """Set the master volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.enabled = not self.enabled
        return self.enabled
        
    def is_sound_enabled(self):
        """Check if sound is enabled"""
        return self.enabled
        
    def play_background_music(self):
        """Start background music (simple ambient tone)"""
        if not self.enabled or self.music_playing:
            return
            
        try:
            # Create ambient background sound
            ambient_sound = self.create_ambient_sound()
            pygame.mixer.music.load(ambient_sound)
            pygame.mixer.music.set_volume(self.volume * 0.3)
            pygame.mixer.music.play(-1)  # Loop infinitely
            self.music_playing = True
        except Exception as e:
            print(f"Error playing background music: {e}")
            
    def stop_background_music(self):
        """Stop background music"""
        try:
            pygame.mixer.music.stop()
            self.music_playing = False
        except Exception as e:
            print(f"Error stopping background music: {e}")
            
    def create_ambient_sound(self):
        """Create a simple ambient sound file"""
        # This is a placeholder - in a real implementation,
        # you might want to use actual music files
        # For now, we'll just use silence
        import tempfile
        import wave
        
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        
        # Create a short silent wav file for ambient music placeholder
        with wave.open(temp_file.name, 'wb') as wav_file:
            wav_file.setnchannels(2)
            wav_file.setsampwidth(2)
            wav_file.setframerate(22050)
            
            # Write 1 second of silence
            silence = b'\x00' * (22050 * 2 * 2)  # 1 sec, 2 channels, 2 bytes per sample
            wav_file.writeframes(silence)
            
        return temp_file.name