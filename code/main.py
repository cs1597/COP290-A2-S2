from settings import *
from level import Level, MazeLevel
from data import Data
from ui import UI
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from overworld import Overworld
from button import Button
from data import Data

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pygame Platformer')
        self.clock = pygame.time.Clock()
        self.import_assets()
        
        self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui =UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.stage_state = 'overworld'
        
        self.tmx_maps = {
                         1: load_pygame(join('..', 'data', 'levels', 'desert_maze.tmx')),
                         6: load_pygame(join('..', 'data', 'levels', 'forest_2.tmx')),
                         2: load_pygame(join('..', 'data', 'levels', 'maze_1.tmx')),
                         4: load_pygame(join('..', 'data', 'tundra','levels', 'platformer.tmx')),
                         5: load_pygame(join('..', 'data', 'levels', 'ice_maze.tmx')),
                         }
        self.tmx_overworld = load_pygame(join('..', 'data', 'overworld', 'overworld.tmx'))
        # self.current_stage = Level(self.tmx_maps[1], self.level_frames, self.data, self.switch_stage)
        self.current_stage = Overworld(self.tmx_overworld, self.overworld_frames, self.data, self.switch_stage)
        self.click = False
        
    def get_font(self,size):
        return pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), size)
       
    def switch_stage(self, target, unlock = 0):
        if target == 'level':
            self.stage_state = 'level'
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
        else:
            if unlock > 0:
                self.data.unlocked_level = unlock
            else:
                self.data.health += 1
            self.stage_state = 'overworld'
            self.current_stage = Overworld(self.tmx_overworld, self.overworld_frames, self.data, self.switch_stage)
        
    def import_assets(self):
        self.level_frames = {
            'items' : import_sub_folders('..', 'graphics', 'items'),
            'effects' : import_sub_folders('..', 'graphics', 'effects'),
            'player' : import_sub_folders('..', 'graphics', 'player'),
            'maze_player' : import_sub_folders('..', 'graphics', 'maze_player'),
            'spikes' : import_folder('..', 'graphics', 'enemies', 'floor_spikes'),
            'helicopter' : import_folder('..', 'graphics', 'levels', 'tundra', 'helicopter'),
            'boat' : import_folder('..', 'graphics', 'levels', 'tundra', 'boat'),
            'gunner' : import_sub_folders('..', 'graphics', 'enemies', 'gunner'),
            'bullet' : import_folder('..', 'graphics', 'enemies', 'bullet'),
            'elephant' : import_folder('..', 'graphics', 'animals', 'elephant'),
            'penguin' : import_folder('..', 'graphics', 'animals', 'penguin'),
            'polar bear': import_folder('..', 'graphics', 'animals', 'polar bear'),
            'overworld_char' : import_sub_folders('..', 'graphics', 'overworld_character'),
            'level_icon': import_folder('..', 'graphics', 'overworld_map', 'point_loc'),
        }
        self.overworld_frames = {
            'point_loc' : import_folder('..', 'graphics', 'overworld_map', 'point_loc'),
            'icon': import_sub_folders('..', 'graphics', 'overworld_character'),
        }
        self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'coin' : import_folder(join('..', 'graphics', 'ui', 'coin')),
            'heart' : import_folder(join('..', 'graphics', 'ui', 'heart'))
        }
        self.audio_files = {
            'coin' : pygame.mixer.Sound(join('..', 'audio', 'coin.wav')),
            'damage' : pygame.mixer.Sound(join('..', 'audio', 'damage.wav')),
            'hit' : pygame.mixer.Sound(join('..', 'audio', 'hit.wav')),
            'attack' : pygame.mixer.Sound(join('..', 'audio', 'attack.wav')),
            }
        self.bgm_1 = pygame.mixer.Sound(join('..', 'audio', 'bgm2.mp3'))
        self.bgm_1.set_volume(0.6)
        self.bgm_1.play(-1)
        
    def run(self):
        while True:
            dt =self.clock.tick(100) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.stage_state == 'overworld':
                            self.main_menu()
                            
            coins_text = self.get_font(25).render("COINS: "+str(self.data.coins), True, "#ffffff")
            coins_rect = coins_text.get_rect(topleft=(10, 30))
            diamonds_text = self.get_font(25).render("DIAMONDS: "+str(self.data.diamonds), True, "#ffffff")
            diamonds_rect = diamonds_text.get_rect(topleft=(10, 51))
            self.current_stage.run(dt)
            self.display_surface.blit(coins_text, coins_rect)
            self.display_surface.blit(diamonds_text, diamonds_rect)
            self.ui.update(dt)
            pygame.display.update()
            
    def main_menu(self):
        while True:
            self.display_surface.fill((255,255,0))

            pointer = pygame.mouse.get_pos()

            main_menu_text = self.get_font(75).render("MAIN MENU", True, "#b68f40")
            main_menu_rect = main_menu_text.get_rect(center=(640, 200))

            play_button = Button(image=pygame.image.load(join('..', 'graphics', 'buttons', 'menu_button.png')), pos=(640, 350), 
                                text_input="NEW GAME", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")
            options_button = Button(image=pygame.image.load(join('..', 'graphics', 'buttons', 'menu_button.png')), pos=(640, 475), 
                                text_input="SETTINGS", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image=pygame.image.load(join('..', 'graphics', 'buttons', 'menu_button.png')), pos=(640, 600), 
                                text_input="QUIT", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")

            self.display_surface.blit(main_menu_text, main_menu_rect)

            for button in [play_button, options_button, quit_button]:
                button.changeColor(pointer)
                button.update(self.display_surface)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(pointer):
                        self.run()
                    if options_button.checkForInput(pointer):
                        # options()
                        pass
                    if quit_button.checkForInput(pointer):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            
    def start_scene(self):
        font = pygame.font.SysFont(None, 36)
        text = "Gradually Displayed Text"
        text_surface = font.render(text, True, (255, 255, 255))

        # Initial position of the text
        text_x = -text_surface.get_width()  # Start off-self.display_surface to the left
        text_y = WINDOW_HEIGHT // 2 - text_surface.get_height() // 2

        # Main game loop
        running = True
        index = 0  # Index to gradually display text
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
    
    # Clear the self.display_surface
            self.display_surface.fill((0, 0, 0))
    
            # Render the text gradually, letter by letter
            partial_text = text[:index]
            partial_surface = font.render(partial_text, True, (255, 255, 255))
            
            # Blit the partial text onto the self.display_surface
            self.display_surface.blit(partial_surface, (text_x, text_y))
            
            # Update the display
            pygame.display.flip()
            
            # Cap the frame rate
            clock.tick(10)  # Adjust speed as needed

            # Exit loop when all text is displayed
            if index < len(text):
                index += 1

            # Exit loop when all text is displayed
            if index >= len(text):
                pygame.time.delay(2000)  # Wait for a few seconds before quitting
                running = False
                
            
if __name__ == '__main__':
    game = Game()
    game.start_scene()