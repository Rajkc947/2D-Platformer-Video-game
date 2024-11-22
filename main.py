import pygame
import asyncio
import sys
from settings import * 
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import * 
from data import Data
from debug import debug
from ui import UI
import button  
from overworld import Overworld

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer Game')
        self.clock = pygame.time.Clock()

        # Game state variables
        self.game_paused = False  # Is the game paused?
        self.menu_state = "main_menu"  # Start with the main menu state
        
        # Load assets and initialize game components
        self.import_assets()
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.tmx_maps = {0: load_pygame(join('data', 'levels', 'omni.tmx')), 1: load_pygame(join( 'data', 'levels', '1.tmx')),
			2: load_pygame(join( 'data', 'levels', '2.tmx')),
			3: load_pygame(join( 'data', 'levels', '3.tmx')),
			4: load_pygame(join( 'data', 'levels', '4.tmx')),
			5: load_pygame(join( 'data', 'levels', '5.tmx')),
        }
        self.tmx_overworld = load_pygame(join( 'data', 'overworld', 'overworld.tmx'))
        self.current_stage = Level(self.tmx_maps[0], self.level_frames, self.audio_files, self.data, self.switch_stage)

        # Load button images
        self.start_img = pygame.image.load("images/button_start.png").convert_alpha()
        self.start_click_sound = pygame.mixer.Sound("audio/button_click.wav")
        self.options_img = pygame.image.load("images/button_options.png").convert_alpha()
        self.quit_img = pygame.image.load("images/button_quit.png").convert_alpha()

        self.resume_img = pygame.image.load("images/button_resume.png").convert_alpha()  # Resume button for pause menu
        self.quit_pause_img = pygame.image.load("images/button_quit.png").convert_alpha()  # Quit button for pause menu

        self.retry_img = pygame.image.load("images/button_retry.png").convert_alpha()  # Retry button for game over menu
        self.menu_background = pygame.image.load("images/menu_background.png").convert()
        self.pause_background = pygame.image.load("images/pause_background.png").convert()
        self.credits = pygame.image.load("images/credits.png").convert()
        self.back_img = pygame.image.load("images/button_back.png").convert_alpha()

        # Get button dimensions
        start_button_width = self.start_img.get_width() * 1  # Scale factor is 1
        start_button_height = self.start_img.get_height() * 1

        options_button_width = self.options_img.get_width() * 1
        options_button_height = self.options_img.get_height() * 1

        quit_button_width = self.quit_img.get_width() * 1
        quit_button_height = self.quit_img.get_height() * 1

        back_button_width = self.back_img.get_width()
        back_button_height = self.back_img.get_height()

        # Calculate centered positions
        self.start_button = button.Button((1280 - start_button_width) // 2, (720 - start_button_height) // 2 - 50, self.start_img, 1)
        self.options_button = button.Button((1280 - options_button_width) // 2, (720 - options_button_height) // 2 + 50, self.options_img, 1)
        self.quit_button = button.Button((1280 - quit_button_width) // 2, (720 - quit_button_height) // 2 + 150, self.quit_img, 1)

        # Create buttons for pause menu
        self.resume_button = button.Button((1280 - start_button_width) // 2, (720 - start_button_height) // 2 - 50, self.resume_img, 1)
        self.quit_pause_button = button.Button((1280 - quit_button_width) // 2, (720 - quit_button_height) // 2 + 50, self.quit_pause_img, 1)

        # Calculate the position for the back button
        self.back_button = button.Button((1280 - back_button_width) // 2, (720 - back_button_height) // 2 + 250, self.back_img, 1)
     

    def switch_stage(self, target, unlock=0):
        """Switch between levels or handle game over."""
        if target == 'level':
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
            self.data.coins= 0
        else:
            if unlock>0:
                self.data.unlocked_level=1
            if unlock>1:
                self.data.unlocked_level=2
            if unlock>2:
                self.data.unlocked_level=3
            if unlock>3:
                self.data.unlocked_level=4
            if unlock>4:
                self.data.unlocked_level=5
            if unlock>5:
                self.data.unlocked_level=6
            else:
                self.data.health -=0
            self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)

    def import_assets(self):
        """Import all necessary assets."""
        # Import game assets
        self.level_frames = {
      'flag': import_folder('graphics', 'level', 'flag'),
			'saw': import_folder('graphics', 'enemies', 'saw', 'animation'),
			'floor_spike': import_folder('graphics','enemies', 'floor_spikes'),
			'palms': import_sub_folders('graphics', 'level', 'palms'),
			'candle': import_folder('graphics','level', 'candle'),
			'window': import_folder('graphics','level', 'window'),
			'big_chain': import_folder('graphics','level', 'big_chains'),
			'small_chain': import_folder('graphics','level', 'small_chains'),
			'candle_light': import_folder('graphics','level', 'candle light'),
			'player': import_sub_folders('graphics','player'),
			'saw': import_folder('graphics', 'enemies', 'saw', 'animation'),
			'saw_chain': import_image('graphics', 'enemies', 'saw', 'saw_chain'),
			'helicopter': import_folder('graphics', 'level', 'helicopter'),
			'boat': import_folder('graphics', 'objects', 'boat'),
			'spike': import_image('graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
			'spike_chain': import_image('graphics', 'enemies', 'spike_ball', 'spiked_chain'),
			'tooth': import_folder('graphics','enemies', 'tooth', 'run'),
			'shell': import_sub_folders('graphics','enemies', 'shell'),
			'pearl': import_image('graphics', 'enemies', 'bullets', 'pearl'),
			'items': import_sub_folders('graphics', 'items'),
			'particle': import_folder('graphics', 'effects', 'particle'),
			'water_top': import_folder('graphics', 'level', 'water', 'top'),
			'water_body': import_image('graphics', 'level', 'water', 'body'),
			'bg_tiles': import_folder_dict('graphics', 'level', 'bg', 'tiles'),
			'cloud_small': import_folder('graphics','level', 'clouds', 'small'),
			'cloud_large': import_image('graphics','level', 'clouds', 'large_cloud'),
        }
        
        self.font = pygame.font.Font(join('graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart': import_folder('graphics', 'ui', 'heart'), 
            'coin': import_image('graphics', 'ui', 'coin')
        }
        self.overworld_frames = {
			'palms': import_folder( 'graphics', 'overworld', 'palm'),
			'water': import_folder( 'graphics', 'overworld', 'water'),
			'path': import_folder_dict( 'graphics', 'overworld', 'path'),
			'icon': import_sub_folders( 'graphics', 'overworld', 'icon'),
		}
        self.audio_files = {
      'coin': pygame.mixer.Sound(join('audio', 'coin.wav')),
			'attack': pygame.mixer.Sound(join('audio', 'attack.wav')),
			'jump': pygame.mixer.Sound(join('audio', 'jump.wav')), 
			'damage': pygame.mixer.Sound(join('audio', 'damage.wav')),
			'pearl': pygame.mixer.Sound(join('audio', 'pearl.wav')),
        }
        pygame.mixer.music.load(join('audio', 'starlight_city.mp3'))  # Load the music file
        pygame.mixer.music.set_volume(0.5)  # Set initial volume
        pygame.mixer.music.play(-1)  # Play the music in a loop

    def check_game_over(self):
             """Check if the player's health is 0 and restart the game at the main menu."""
             if self.data.health <= 0:
                 # Reset health and other game-related variables
                 self.data.health = 5  # Reset to the starting health
                 self.data.current_level = 0  # Reset to the first level
                 self.data.coins = 0
                 self.data.unlocked_level = 0

                 # Reset the level to the starting state
                 self.current_stage = Level(self.tmx_maps[self.data.current_level], 
                                       self.level_frames, self.audio_files, self.data, self.switch_stage)
            
                # Go back to the main menu
                 self.menu_state = 'main_menu'



    def handle_pause_menu(self):
      """Handle the rendering of the pause menu."""
      if self.game_paused:
        # Draw pause menu background
        self.display_surface.blit(self.pause_background, (0, 0))  # Draw the background at (0, 0)

        # Draw and check the pause menu buttons
        if self.resume_button.draw(self.display_surface):
            self.game_paused = False  # Resume the game
        if self.quit_pause_button.draw(self.display_surface):
            pygame.quit()
            sys.exit()

    def handle_main_menu(self):
         self.display_surface.blit(self.menu_background, (0, 0))  # Draw the background at (0, 0)

         # Draw buttons for the main menu
         if self.start_button.draw(self.display_surface):
            # Reset the game state when starting a new game
            self.data.health = 5  # Reset health
            self.data.current_level = 0  # Reset to the first level
            self.data.coins = 0
            self.data.unlocked_level = 0

            # Reinitialize the level to make sure the player starts at the initial position
            self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)

            self.menu_state = 'playing'  # Start the game
         if self.options_button.draw(self.display_surface):
             self.menu_state = 'options_menu'  # Switch to the options menu

         if self.quit_button.draw(self.display_surface):
            pygame.quit()
            sys.exit()

    def handle_options_menu(self):
    # Draw the options image
       self.display_surface.blit(self.credits, (0, 0))  # Display the options/credits image

    # Draw the "Back" button
       if self.back_button.draw(self.display_surface):  # Reusing the 'quit' button as 'back'
        self.menu_state = 'main_menu'  # Go back to the main menu


    async def run(self):
        """Main game loop."""
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Toggle pause with ESCAPE key when playing
                if event.type == pygame.KEYDOWN and self.menu_state == 'playing':
                    if event.key == pygame.K_ESCAPE:
                        self.game_paused = not self.game_paused
                      
                            

            if self.menu_state == 'main_menu':
                # Show start menu
                self.handle_main_menu()
            elif self.game_paused:
                # Show pause menu
                self.handle_pause_menu()
            elif self.menu_state == 'options_menu':  # Handle the options menu
                self.handle_options_menu()
            else:
                # Main game logic
                self.check_game_over()
                self.current_stage.run(dt)
                self.ui.update(dt)

            pygame.display.update()

            await asyncio.sleep(0)

if __name__ == '__main__':
    game = Game()
    asyncio.run(game.run())
