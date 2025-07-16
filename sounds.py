import pygame
import os
import random

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.enabled = True
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound files from the Assets/sounds directory."""
        sound_dir = "Assets/sounds/"
        if os.path.exists(sound_dir):
            for file in os.listdir(sound_dir):
                if file.endswith(('.wav', '.ogg', '.mp3')):
                    name = file.split('.')[0]
                    try:
                        self.sounds[name] = pygame.mixer.Sound(os.path.join(sound_dir, file))
                        print(f"Loaded sound: {name}")
                    except Exception as e:
                        print(f"Failed to load sound {name}: {e}")
        else:
            print(f"Sound directory {sound_dir} not found")
    
    def play(self, sound_name):
        """Play a specific sound by name."""
        if self.enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Failed to play sound {sound_name}: {e}")
    
    def play_random_keypress(self):
        """Play a random keypress sound from the available options."""
        keypress_sounds = ['Keypress1', 'KeyPress2', 'KeyPress3']
        available_sounds = [s for s in keypress_sounds if s in self.sounds]
        
        if available_sounds:
            random_sound = random.choice(available_sounds)
            self.play(random_sound)
    
    def play_startup(self):
        """Play the computer startup sound."""
        self.play('ComputerStart')
    
    def toggle_sound(self):
        """Toggle sound on/off."""
        self.enabled = not self.enabled
        print(f"Sound {'enabled' if self.enabled else 'disabled'}") 