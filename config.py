# config.py
"""
Configuration options for the CRT Terminal.
Edit these values to customize the look and feel.
"""

# Color schemes (choose 'green', 'amber', or 'blue')
COLOR_SCHEME = 'green'

COLOR_PRESETS = {
    'green': {
        'bg': (10, 20, 10),
        'text': (80, 255, 80),
        'glow': (80, 255, 80, 80),
    },
    'amber': {
        'bg': (30, 20, 10),
        'text': (255, 200, 80),
        'glow': (255, 200, 80, 80),
    },
    'blue': {
        'bg': (10, 20, 30),
        'text': (80, 200, 255),
        'glow': (80, 200, 255, 80),
    },
}

# Font settings
FONT_NAME = 'Assets/PerfectDOSVGA437.ttf'  # Place your retro font in assets/
FONT_SIZE = 24

# Text speed (characters per second, or 0 for instant)
TEXT_SPEED = 0  # 0 = instant, >0 = typing effect

# Effects toggles
ENABLE_SCANLINES = True
ENABLE_NOISE = False
ENABLE_GLOW = False
ENABLE_WARP = False
ENABLE_FLICKER = False
ENABLE_JITTER = False

# Glitch effect toggle
GLITCHY_TEXT = True
GLITCH_CHANCE = 0.05

# CRT effect parameters
SCANLINE_OPACITY = 64  # 0-255
NOISE_OPACITY = 0     # 0-255
GLOW_RADIUS = 0        # px
JITTER_AMOUNT = 0      # px
FLICKER_INTENSITY = 0.0  # 0-1 

# Corruption effect toggle and settings
ENABLE_CORRUPTION = True
CORRUPTION_CHANCE = 0.012  # Probability per frame to trigger corruption
CORRUPTION_DURATION = 0.75  # Seconds corruption lasts
CORRUPTION_INTENSITY = 0.6  # 0-1, how many blocks to corrupt
CORRUPTION_BLOCK_SIZE = 80  # px 