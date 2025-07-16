import pygame
import random
import numpy as np
import string

# --- Scanlines ---
def apply_scanlines(surface, opacity=32, spacing=2):
    """
    Draws horizontal scanlines over the surface.
    """
    w, h = surface.get_size()
    scanline = pygame.Surface((w, spacing), pygame.SRCALPHA)
    scanline.fill((0, 0, 0, opacity))
    for y in range(0, h, spacing*2):
        surface.blit(scanline, (0, y))

# --- Noise/Grain ---
def apply_noise(surface, opacity=32):
    """
    Overlays random noise (grain) on the surface.
    """
    arr = np.random.randint(0, 255, (surface.get_height(), surface.get_width()), dtype=np.uint8)
    noise = pygame.surfarray.make_surface(np.stack([arr]*3, axis=-1))
    noise.set_alpha(opacity)
    surface.blit(noise, (0, 0))

# --- Glow/Bloom ---
def apply_glow(surface, color, radius=8):
    """
    Simulates phosphor glow by blurring a copy of the surface and tinting it.
    """
    glow = pygame.transform.smoothscale(surface, (surface.get_width()//2, surface.get_height()//2))
    glow = pygame.transform.smoothscale(glow, surface.get_size())
    glow.set_alpha(80)
    tint = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    tint.fill(color)
    glow.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    surface.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

# --- Jitter ---
def jitter_rect(rect, amount=1):
    """
    Returns a new rect with slight horizontal jitter.
    """
    dx = random.randint(-amount, amount)
    return rect.move(dx, 0)

# --- Flicker ---
def flicker_alpha(base_alpha, intensity=0.15):
    """
    Returns a slightly randomized alpha for flicker effect.
    """
    return max(0, min(255, int(base_alpha * (1.0 + random.uniform(-intensity, intensity)))))

def apply_text_glitch(text, glitch_chance=0.15, charset=None):
    """
    Returns a new string where each character has a chance to be replaced by a random symbol.
    glitch_chance: probability (0-1) that a character is replaced.
    charset: string of possible glitch characters (defaults to ASCII symbols).
    """
    if charset is None:
        charset = string.ascii_letters + string.digits + "!@#$%^&*()_+-=~[]{}|;:',.<>?/\\"
    glitched = []
    for c in text:
        if c != ' ' and random.random() < glitch_chance:
            glitched.append(random.choice(charset))
        else:
            glitched.append(c)
    return ''.join(glitched)

def apply_moving_scanlines(surface, opacity=32, spacing=2, offset_x=0, offset_y=0):
    """
    Draws diagonal scanlines over the surface, moving by (offset_x, offset_y).
    """
    w, h = surface.get_size()
    scanline = pygame.Surface((w, spacing), pygame.SRCALPHA)
    scanline.fill((0, 0, 0, opacity))
    # Diagonal movement: shift both x and y
    for y in range(-spacing*2, h, spacing*2):
        x_offset = int((y + offset_y) * offset_x / (h if h else 1))  # proportional diagonal
        surface.blit(scanline, (x_offset, y + offset_y))

def corrupt_surface(surface, intensity=0.2, block_size=32):
    """
    Randomly shifts horizontal bands or blocks of the surface for a corruption effect.
    intensity: 0-1, how many blocks to corrupt.
    block_size: size of each block in pixels.
    """
    w, h = surface.get_size()
    corrupted = surface.copy()
    num_blocks = int(h * intensity // block_size)
    for _ in range(num_blocks):
        y = random.randint(0, h - block_size)
        x_shift = random.randint(-w // 8, w // 8)
        rect = pygame.Rect(0, y, w, block_size)
        band = surface.subsurface(rect).copy()
        corrupted.blit(band, (x_shift, y))
    return corrupted 