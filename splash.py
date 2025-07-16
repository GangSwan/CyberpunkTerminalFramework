import pygame
import time
import random
from config import GLITCHY_TEXT, GLITCH_CHANCE, ENABLE_CORRUPTION, CORRUPTION_CHANCE, CORRUPTION_DURATION, CORRUPTION_INTENSITY, CORRUPTION_BLOCK_SIZE
from effects import apply_text_glitch, corrupt_surface

class SplashScreen:
    """
    Animated splash/boot screen for the CRT terminal.
    Shows a fake BIOS/boot sequence with typewriter text, flicker, and a progress bar.
    """
    def __init__(self, screen, font, colors, duration=6.0):
        self.screen = screen
        self.font = font
        self.colors = colors
        self.duration = duration
        self.boot_lines = [
            "CYBERPUNK SYSTEMS BIOS v3.2",
            "Copyright (C) 2045 Night City",
            "",
            "Memory Test: 16384K OK",
            "Detecting Devices...",
            "  IDE0: Quantum Fireball 512MB",
            "  IDE1: Not Detected",
            "  SCSI: Arasaka Cyberdeck v2.1",
            "",
            "Booting..."
        ]
        self.progress_bar_length = 32
        self.bg_color = self.colors['bg']
        self.text_color = self.colors['text']

    def show_logo_intro(self, logo_path="Assets/logo.png", intro_duration=2.8):
        clock = pygame.time.Clock()
        w, h = self.screen.get_size()
        # Load logo
        try:
            logo = pygame.image.load(logo_path).convert_alpha()
        except Exception:
            logo = None
        if logo:
            max_w, max_h = w // 2, h // 3
            scale = min(max_w / logo.get_width(), max_h / logo.get_height(), 1.0)
            logo = pygame.transform.smoothscale(logo, (int(logo.get_width()*scale), int(logo.get_height()*scale)))
        start_time = time.time()
        running = True
        dot_states = [".", "..", "..."]
        wipe_duration = 0.7
        # Corruption effect state for splash
        corruption_active = False
        corruption_end_time = 0.0
        while running:
            now = time.time()
            elapsed = now - start_time
            # --- Corruption logic ---
            if ENABLE_CORRUPTION:
                if not corruption_active and random.random() < CORRUPTION_CHANCE:
                    corruption_active = True
                    corruption_end_time = now + CORRUPTION_DURATION
                if corruption_active and now > corruption_end_time:
                    corruption_active = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            self.screen.fill(self.bg_color)
            # --- Screen wipe animation ---
            if logo:
                logo_x = (w - logo.get_width()) // 2
                logo_y = h // 4
                offset_x = random.randint(-1, 1)
                offset_y = random.randint(-1, 1)
                logo_surf = logo.copy()
                if random.random() < 0.07:
                    arr = pygame.surfarray.pixels3d(logo_surf)
                    arr[:, :, :] = 255 - arr[:, :, :]
                    del arr  # Unlock the surface!
                temp_surf = pygame.Surface(logo_surf.get_size(), pygame.SRCALPHA)
                temp_surf.fill(self.bg_color)
                temp_surf.blit(logo_surf, (0, 0))
                # Apply corruption to logo if active
                if corruption_active:
                    temp_surf = corrupt_surface(temp_surf, intensity=CORRUPTION_INTENSITY, block_size=CORRUPTION_BLOCK_SIZE)
                # Wipe reveal
                if elapsed < wipe_duration:
                    wipe_height = int(logo_surf.get_height() * (elapsed / wipe_duration))
                    if wipe_height > 0:
                        logo_crop = temp_surf.subsurface((0, 0, temp_surf.get_width(), wipe_height)).copy()
                        self.screen.blit(logo_crop, (logo_x + offset_x, logo_y + offset_y))
                else:
                    self.screen.blit(temp_surf, (logo_x + offset_x, logo_y + offset_y))
            # Animated text at bottom
            dots = dot_states[int((elapsed * 2) % 3)]
            base_text = f"parsing memory fragments{dots}"
            if GLITCHY_TEXT:
                base_text = apply_text_glitch(base_text, GLITCH_CHANCE)
            text_surf = self.font.render(base_text, True, self.text_color)
            self.screen.blit(text_surf, ((w - text_surf.get_width()) // 2, h - self.font.get_height() - 40))
            pygame.display.flip()
            clock.tick(60)
            if elapsed > intro_duration:
                running = False

    def show_press_enter_screen(self):
        clock = pygame.time.Clock()
        w, h = self.screen.get_size()
        waiting = True
        prompt = "press enter to continue"
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            self.screen.fill(self.bg_color)
            surf = self.font.render(prompt, True, self.text_color)
            self.screen.blit(surf, ((w - surf.get_width()) // 2, (h - surf.get_height()) // 2))
            pygame.display.flip()
            clock.tick(60)

    def run(self):
        clock = pygame.time.Clock()
        start_time = time.time()
        fade = 0
        fade_in_time = 0.7
        line_delay = 0.32
        progress_time = 2.2
        lines_shown = 0
        progress = 0
        w, h = self.screen.get_size()
        margin = 32
        bar_y = h // 2 + 80
        running = True
        while running:
            now = time.time()
            elapsed = now - start_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            self.screen.fill(self.bg_color)
            # Fade in
            if elapsed < fade_in_time:
                fade = int(255 * (1 - elapsed / fade_in_time))
            else:
                fade = 0
            # Typewriter lines
            lines_shown = min(int((elapsed - fade_in_time) / line_delay), len(self.boot_lines))
            y = h // 2 - 100
            for i in range(lines_shown):
                line = self.boot_lines[i]
                # Glitch effect
                if GLITCHY_TEXT:
                    line = apply_text_glitch(line, GLITCH_CHANCE)
                # Flicker effect
                if random.random() < 0.07:
                    color = (self.text_color[0], self.text_color[1], self.text_color[2], 180)
                else:
                    color = self.text_color
                surf = self.font.render(line, True, color)
                self.screen.blit(surf, (margin, y))
                y += self.font.get_height() + 4
            # Progress bar
            if elapsed > fade_in_time + line_delay * len(self.boot_lines):
                progress = min(1.0, (elapsed - (fade_in_time + line_delay * len(self.boot_lines))) / progress_time)
                bar_w = int(self.progress_bar_length * progress)
                bar_str = '[' + '=' * bar_w + ' ' * (self.progress_bar_length - bar_w) + ']'
                surf = self.font.render(bar_str, True, self.text_color)
                self.screen.blit(surf, (margin, bar_y))
            # Fade overlay
            if fade > 0:
                overlay = pygame.Surface((w, h))
                overlay.set_alpha(fade)
                overlay.fill(self.bg_color)
                self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            clock.tick(60)
            # End after duration
            if elapsed > self.duration:
                running = False 