import pygame
import sys
import time
import random
from config import COLOR_SCHEME, COLOR_PRESETS, FONT_NAME, FONT_SIZE, TEXT_SPEED, \
    ENABLE_SCANLINES, ENABLE_NOISE, ENABLE_GLOW, ENABLE_WARP, ENABLE_FLICKER, ENABLE_JITTER, \
    SCANLINE_OPACITY, NOISE_OPACITY, GLOW_RADIUS, JITTER_AMOUNT, FLICKER_INTENSITY, \
    GLITCHY_TEXT, GLITCH_CHANCE, \
    ENABLE_CORRUPTION, CORRUPTION_CHANCE, CORRUPTION_DURATION, CORRUPTION_INTENSITY, CORRUPTION_BLOCK_SIZE
from effects import apply_scanlines, apply_noise, apply_glow, jitter_rect, flicker_alpha, apply_text_glitch, corrupt_surface
from commands import CommandHandler
from splash import SplashScreen
from sounds import SoundManager

class Terminal:
    """
    CRT Terminal main class. Handles UI, input, output, and effects.
    """
    def __init__(self, width=960, height=600, screen=None):
        pygame.init()
        pygame.display.set_caption("Cyberpunk CRT Terminal")
        if screen is not None:
            self.screen = screen
        else:
            self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.colors = COLOR_PRESETS[COLOR_SCHEME]
        self.input_line = ''
        self.output_lines = []
        self.max_lines = 100
        self.command_handler = CommandHandler()
        self.typing_buffer = []
        self.typing_index = 0
        self.typing_time = 0
        self.sim_delay = 0.2  # Simulated command delay (seconds)
        self.running = True
        self.prompt = '> '
        self.scroll_offset = 0
        self.line_height = self.font.get_height() + 2
        self.margin = 16
        # Corruption effect state
        self.corruption_active = False
        self.corruption_end_time = 0.0
        # Sound manager
        self.sound_manager = SoundManager()

    def add_output(self, text, flicker=False):
        """
        Adds text (or list of lines) to output history.
        """
        if isinstance(text, str):
            lines = text.split('\n')
        else:
            lines = text
        for line in lines:
            self.output_lines.append({'text': line, 'flicker': flicker})
        if len(self.output_lines) > self.max_lines:
            self.output_lines = self.output_lines[-self.max_lines:]
        self.scroll_offset = 0

    def handle_command(self, line):
        self.add_output(self.prompt + line, flicker=True)
        time.sleep(self.sim_delay)  # Simulated delay
        output = self.command_handler.handle(line)
        self.add_output(output)
        if line.strip().lower() == 'exit':
            self.running = False

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                # Only reset display mode if we own the screen
                if not hasattr(self, '_external_screen'):
                    self.screen = pygame.display.set_mode(event.size, pygame.FULLSCREEN)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_BACKSPACE:
                    self.input_line = self.input_line[:-1]
                    self.sound_manager.play_random_keypress()
                elif event.key == pygame.K_RETURN:
                    line = self.input_line.strip()
                    if line:
                        self.handle_command(line)
                    self.input_line = ''
                elif event.key == pygame.K_UP:
                    self.scroll_offset = min(self.scroll_offset + 1, max(0, len(self.output_lines) - 1))
                elif event.key == pygame.K_DOWN:
                    self.scroll_offset = max(self.scroll_offset - 1, 0)
                elif event.key < 256:
                    self.input_line += event.unicode
                    self.sound_manager.play_random_keypress()

    def draw(self):
        self.screen.fill(self.colors['bg'])
        w, h = self.screen.get_size()
        # --- Draw everything to a framebuffer first ---
        framebuffer = pygame.Surface((w, h))
        framebuffer.fill(self.colors['bg'])
        # Draw output lines (scrollable)
        lines_to_show = (h - self.line_height - self.margin*2) // self.line_height
        start = max(0, len(self.output_lines) - lines_to_show - self.scroll_offset)
        end = len(self.output_lines) - self.scroll_offset
        y = self.margin
        for i in range(lines_to_show):
            line_idx = start + i
            if line_idx < end:
                line = self.output_lines[line_idx]
                text = line['text']
                flicker = line.get('flicker', False) and ENABLE_FLICKER
                # Apply glitch effect
                if GLITCHY_TEXT:
                    text = apply_text_glitch(text, GLITCH_CHANCE)
            else:
                text = ''
                flicker = False
            color = self.colors['text']
            alpha = flicker_alpha(255, FLICKER_INTENSITY) if flicker else 255
            surf = self.font.render(text, True, color)
            if alpha < 255:
                surf.set_alpha(alpha)
            rect = surf.get_rect(topleft=(self.margin, y))
            framebuffer.blit(surf, rect)
            y += self.line_height
        # Draw input line
        input_text = self.prompt + self.input_line
        input_surf = self.font.render(input_text, True, self.colors['text'])
        framebuffer.blit(input_surf, (self.margin, h - self.line_height - self.margin))
        # --- Effects (apply to framebuffer only) ---
        if ENABLE_GLOW:
            apply_glow(framebuffer, self.colors['glow'], max(4, GLOW_RADIUS // 2))
        # Classic horizontal scanlines
        if ENABLE_SCANLINES:
            apply_scanlines(framebuffer, SCANLINE_OPACITY, spacing=4)
        if ENABLE_NOISE:
            apply_noise(framebuffer, max(16, NOISE_OPACITY // 2))
        # --- Corruption effect ---
        now = pygame.time.get_ticks() / 1000.0
        if ENABLE_CORRUPTION:
            if not self.corruption_active and random.random() < CORRUPTION_CHANCE:
                self.corruption_active = True
                self.corruption_end_time = now + CORRUPTION_DURATION
            if self.corruption_active:
                framebuffer = corrupt_surface(framebuffer, intensity=CORRUPTION_INTENSITY, block_size=CORRUPTION_BLOCK_SIZE)
                if now > self.corruption_end_time:
                    self.corruption_active = False
        # Blit framebuffer to screen
        self.screen.blit(framebuffer, (0, 0))

if __name__ == '__main__':
    # Initialize pygame and create window
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    # Initialize sound manager
    from sounds import SoundManager
    sound_manager = SoundManager()
    
    # Show splash/boot screen
    from config import COLOR_PRESETS, COLOR_SCHEME, FONT_NAME, FONT_SIZE
    font = pygame.font.Font(FONT_NAME, FONT_SIZE)
    colors = COLOR_PRESETS[COLOR_SCHEME]
    splash = SplashScreen(screen, font, colors)
    
    # Show press enter screen and play startup sound when Enter is pressed
    splash.show_press_enter_screen(sound_manager)
    splash.show_logo_intro()
    splash.run()
    
    # Then launch the terminal, reusing the same screen
    term = Terminal(screen=screen)
    term.add_output("CYBERPUNK RED TERMINAL ONLINE.")
    term.add_output("Type 'help' for commands.")
    term.run() 