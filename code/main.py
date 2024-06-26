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
import time

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Call Of The Wild')
        self.clock = pygame.time.Clock()
        self.import_assets()
        
        self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui =UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.stage_state = 'overworld'
        self.first_time = True

        self.clock = pygame.time.Clock()
        # Define paths to your images
        self.start_images = [
            join('..', 'graphics', 'cutscene_images', '0.png'),
            join('..', 'graphics', 'cutscene_images', '1.png'),
            join('..', 'graphics', 'cutscene_images', '2.png'),
            join('..', 'graphics', 'cutscene_images', '3.png'),
            join('..', 'graphics', 'cutscene_images', '4.png')
        ]

        self.defeat_images = [
            join('..', 'graphics', 'cutscene_images', '5.png'),
            join('..', 'graphics', 'cutscene_images', '6.png'),
        ]
        
        self.victory_images = [
            join('..', 'graphics', 'cutscene_images', '7.png'),
            join('..', 'graphics', 'cutscene_images', '8.png'),
            join('..', 'graphics', 'cutscene_images', '9.png'),
        ]
        
        self.penguin_images = [join('..', 'graphics', 'cutscene_images', '11.png')]
        self.elephant_images = [join('..', 'graphics', 'cutscene_images', '10.png')]
        # Corresponding scripts for each image
        self.start_scripts = [
            "In the enchanted realm of Wildhaven, where every leaf and stone tells a story...",
            "A land of harmony, where diverse terrains cradle the world's most magical creatures....",
            "But shadows loom as poachers invade, threatening the peace of this pristine paradise...",
            "Amid relics of adventures past, young Eli uncovers a destiny foretold in his grandfather's diary",
            "With courage his shield, Eli steps into the dawn, the Guardian of Wildhaven's legacy reborn...."
        ]

        self.defeat_scripts = [
            "In the shadowed silence of the forest, Eli faces his toughest moment yet.",
            "Rise again, Eli. The forest calls, your journey awaits, with a renewed spirit."
        ]
        
        self.victory_scripts = [
            "As the sun shines anew over Wildhaven, Eli and his furry friends revel in the joy of freedom.",
            "Nature's balance is restored, thanks to the bravery of one young guardian.",
            "Eli pledges to continue watching over Wildhaven. The journey never truly ends...."
        ]
        
        self.penguin_scripts = ["Ice shatters, the cage opens, and warmth returns to the heart"]
        self.elephant_scripts = ["Reunited, the forest breathes a sigh of relief, the elephant's trumpet a song of joy"]
        
        self.ow_htp = [
            "This is the OVERWORLD.",
            "Use W, A, S, D to navigate the player",
            "The map consists of four regions, each with two levels",
            "To enter a level, reach to the level location and press the ENTER key",
            "Locked levels are displayed in Black and White while the unlocked levels are in color",
            "Collect coins and diamonds to buy lives and unlock levels. Press B to enter shop",
            "To go back to the main menu, press ESC"
        ]
        
        self.level_htp = [
            "This is a level.",
            "Use A, D to navigate the player. Use S to fall through platforms",
            "Use SPACE to jump and X to attack",
            "There are two types of levels: Maze and Rescue",
            "Reach the other end of the Maze level and retrieve the key",
            "Find and rescue the caged animal in the Rescue level"
        ]
        
        self.tmx_maps = {
                         8: load_pygame(join('..', 'data', 'levels', 'desert_level.tmx')),
                         7: load_pygame(join('..', 'data', 'levels', 'desert_maze.tmx')),
                         6: load_pygame(join('..', 'data', 'levels', 'forest_new_vel.tmx')),
                         5: load_pygame(join('..', 'data', 'levels', 'forest_maze_2.tmx')),
                         4: load_pygame(join('..', 'data', 'levels', 'forest_2.tmx')),
                         3: load_pygame(join('..', 'data', 'levels', 'maze_1.tmx')),
                         2: load_pygame(join('..', 'data', 'tundra','levels', 'platformer.tmx')),
                         1: load_pygame(join('..', 'data', 'levels', 'ice_maze.tmx')),
                         }
        
        self.tmx_overworld = load_pygame(join('..', 'data', 'overworld', 'overworld.tmx'))
        self.current_stage = Overworld(self.tmx_overworld, self.overworld_frames, self.data, self.switch_stage)
        # self.bgm_1 = pygame.mixer.Sound(join('..', 'audio', 'ow_bgm.wav'))
        # self.bgm_1.set_volume(0.6)
        self.click = False
        self.level_bgm = pygame.mixer.Sound(join('..', 'audio', 'level_bgm.mp3'))
        self.ow_bgm = pygame.mixer.Sound(join('..', 'audio', 'ow_bgm.mp3'))
        self.start_cs_bgm = pygame.mixer.Sound(join('..', 'audio', 'start_cs.mp3'))
        self.level_bgm.set_volume(0.6)
        self.ow_bgm.set_volume(0.6)
        self.start_cs_bgm.set_volume(0.6)

    def get_font(self,size):
        return pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), size)
        
    def check_skip(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
        return False

    def fade_in(self, image, speed=10, htp = False):
        for alpha in range(0, 255, speed):
            self.display_surface.fill((0, 0, 0))
            image.set_alpha(alpha)
            if htp:
                self.display_surface.blit(image, (265, 270))
            else:
                self.display_surface.blit(image, ((WINDOW_WIDTH-900)/2, WINDOW_HEIGHT/10))
            pygame.display.update()
            self.clock.tick(30)
            if self.check_skip():
                return True
        return False

    def display_text_animation(self, text, pos):
        font = self.get_font(35)
        text_surface = font.render('', True, pygame.Color('white'))
        for i in range(len(text)):
            next_text = text[:i+1]
            text_surface = font.render(next_text, True, pygame.Color('white'))
            self.display_surface.blit(text_surface, pos)
            pygame.display.update()
            self.clock.tick(20)
            if self.check_skip():
                return True
        return False

    def opening_cutscene(self):
        pygame.mixer.stop()
        self.start_cs_bgm.play(-1)
        for idx, image_path in enumerate(self.start_images):
            image = pygame.image.load(image_path).convert_alpha()
            if self.fade_in(image):
                break
            if self.display_text_animation(self.start_scripts[idx], (40, 30)):
                break
            time.sleep(1.5) 

        pygame.mixer.stop()
        self.ow_bgm.play(-1)
        self.run()
        
    def how_to_play(self):
        background_image_1 = pygame.image.load(join('..', 'graphics', 'how_to_play','overworld.png'))
        background_image_2 = pygame.image.load(join('..', 'graphics', 'how_to_play','level.png'))
        
        if self.fade_in(background_image_1, htp = True):
            return
        for idx, text in enumerate(self.ow_htp):
            if self.display_text_animation(text, (40, 32*(idx+1))):
                break
            time.sleep(1)
        if self.fade_in(background_image_2, htp = True):
            return
        for idx, text in enumerate(self.level_htp):
            if self.display_text_animation(text, (40, 32*(idx+1))):
                break
            time.sleep(1)
        
        pygame.mixer.stop()
        self.main_menu()
        
    def victory(self):
        for idx, image_path in enumerate(self.victory_images):
            image = pygame.image.load(image_path).convert_alpha()
            if self.fade_in(image):
                break
            if self.display_text_animation(self.victory_scripts[idx], (40, 30)):
                break
            time.sleep(1.5) 
        
        self.first_time = True
        pygame.mixer.stop()
        self.main_menu()

    def defeat(self):
        for idx, image_path in enumerate(self.defeat_images):
            image = pygame.image.load(image_path).convert_alpha()
            if self.fade_in(image):
                break
            if self.display_text_animation(self.defeat_scripts[idx], (40, 30)):
                break
            time.sleep(1.5) 
        pygame.mixer.stop()
            
    def penguin(self):
        for idx, image_path in enumerate(self.penguin_images):
            image = pygame.image.load(image_path).convert_alpha()
            if self.fade_in(image):
                break
            if self.display_text_animation(self.penguin_scripts[idx], (40, 30)):
                break
            time.sleep(1.5)
        
    def elephant(self):
        for idx, image_path in enumerate(self.elephant_images):
            image = pygame.image.load(image_path).convert_alpha()
            if self.fade_in(image):
                break
            if self.display_text_animation(self.elephant_scripts[idx], (40, 30)):
                break
            time.sleep(1.5)
        
    def defeat(self):
        for idx, image_path in enumerate(self.defeat_images):
            image = pygame.image.load(image_path).convert_alpha()
            if self.fade_in(image):
                break
            if self.display_text_animation(self.defeat_scripts[idx], (40, 30)):
                break
            time.sleep(1.5) 
        
        self.first_time = True
        self.main_menu()
       
    def switch_stage(self, target, unlock = 0):
        pygame.mixer.stop()
        if target == 'level':
            self.level_bgm.play(-1)
            self.stage_state = 'level'
            self.data.level_health = 3
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
        else:
            self.ow_bgm.play(-1)
            if unlock == 9:
                self.victory()
            if unlock == 3:
                self.penguin()
            if unlock == 5:
                self.elephant()
            if unlock > 0:
                self.data.unlocked_level = unlock
                self.data.health = self.data.health
            else:
                self.data.health -= 1
                if self.data.health == 0:
                    self.defeat()
            self.stage_state = 'overworld'
            print(self.data.health)
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
            'camel': import_folder('..', 'graphics', 'animals', 'camel'),
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
        
    def skip_level(self):
        if self.data.diamonds >= 50:
            self.data.diamonds -= 50 
            self.data.unlocked_level += 1
            self.display_text_animation("Yayy! Next level unlocked!!", (440, 30))
        else:
            self.display_text_animation("You don't have enough diamonds!", (420, 30))
        time.sleep(1)
        
    def buy_lives(self):
        if self.data.coins >= 100:
            self.data.coins -= 100 
            self.data.health += 1
            self.display_text_animation("Yayy! One life added!!", (440, 30))
        else:
            self.display_text_animation("You don't have enough coins!", (420, 30))
        time.sleep(1)


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
                            pygame.mixer.stop()
                            self.main_menu()
                    if event.key == pygame.K_b:
                        if self.stage_state == 'overworld':
                            self.shop()
                            
            coins_text = self.get_font(30).render("COINS: "+str(self.data.coins), True, "#ffffff")
            coins_rect = coins_text.get_rect(topleft=(10, 40))
            diamonds_text = self.get_font(30).render("DIAMONDS: "+str(self.data.diamonds), True, "#ffffff")
            diamonds_rect = diamonds_text.get_rect(topleft=(10, 65))
            self.current_stage.run(dt)
            self.display_surface.blit(coins_text, coins_rect)
            self.display_surface.blit(diamonds_text, diamonds_rect)
            self.ui.update(dt)
            pygame.display.update()
            
    def main_menu(self):
        self.ow_bgm.play(-1)
        background_image = pygame.image.load(join('..', 'graphics', 'backgrounds','main.png'))
        while True:
            self.display_surface.blit(background_image, (0, 0))

            pointer = pygame.mouse.get_pos()

            main_menu_text = self.get_font(75).render("MAIN MENU", True, "#1e6b1d")
            main_menu_rect = main_menu_text.get_rect(center=(640, 150))

            continue_button = Button(image=pygame.image.load(join('..', 'graphics', 'buttons', 'menu_button.png')), pos=(640, 275), 
                                text_input="CONTINUE", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")
            play_button = Button(image=pygame.image.load(join('..', 'graphics', 'buttons', 'menu_button.png')), pos=(640, 400), 
                                text_input="NEW GAME", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")
            options_button = Button(image=pygame.image.load(join('..', 'graphics', 'buttons', 'menu_button.png')), pos=(640, 525), 
                                text_input="HOW TO PLAY", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image=pygame.image.load(join('..', 'graphics', 'buttons', 'menu_button.png')), pos=(640, 650), 
                                text_input="QUIT", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")

            self.display_surface.blit(main_menu_text, main_menu_rect)

            for button in [continue_button,play_button, options_button, quit_button]:
                button.changeColor(pointer)
                button.update(self.display_surface)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.checkForInput(pointer):
                        if self.first_time:
                            self.display_text_animation("Please start a NEW GAME!!", (480, 30))
                            time.sleep(1)
                        else:
                            self.run()
                    if play_button.checkForInput(pointer):
                        self.first_time = False
                        self.data.health = 5
                        self.data.coins = 0
                        self.data.diamonds = 0
                        self.data.unlocked_level = 1
                        self.data.current_level = 1
                        self.opening_cutscene()
                    if options_button.checkForInput(pointer):
                        self.how_to_play()
                    if quit_button.checkForInput(pointer):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            
    def shop(self):
        background_image = pygame.image.load(join('..', 'graphics', 'backgrounds','shop.png'))
        sprite_image = pygame.image.load(join('..', 'graphics', 'items','gold','0.png')) 
        sprite_text_25 = self.get_font(25).render("100x", True, "#ffffff")
        sprite_rect = sprite_image.get_rect(center=(790, 350))
        sprite_rect_25 = sprite_image.get_rect(center=(758, 355))
        sprite_image_diamond = pygame.image.load(join('..', 'graphics', 'items','diamond','0.png')) 
        sprite_text_50 = self.get_font(25).render("50x", True, "#ffffff")
        sprite_rect_diamond = sprite_image.get_rect(center=(790, 470))
        sprite_rect_50 = sprite_image.get_rect(center=(762, 475))
        while True:
            self.display_surface.blit(background_image, (0, 0))

            pointer = pygame.mouse.get_pos()

            main_menu_text = self.get_font(75).render("SHOP", True, "#b68f40")
            main_menu_rect = main_menu_text.get_rect(center=(640, 170))

            self.display_surface.blit(main_menu_text, main_menu_rect)
            

            play_button = Button(image=pygame.image.load(join('..', 'graphics', 'buttons', 'menu_button.png')), pos=(640, 350), 
                                text_input="BUY LIVES", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")
            options_button = Button(image=pygame.image.load(join('..', 'graphics', 'buttons', 'menu_button.png')), pos=(640, 475), 
                                text_input="SKIP LEVEL", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image=pygame.image.load(join('..', 'graphics', 'buttons', 'menu_button.png')), pos=(640, 600), 
                                text_input="BACK", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")


            for button in [play_button, options_button, quit_button]:
                button.changeColor(pointer)
                button.update(self.display_surface)

            self.display_surface.blit(sprite_image, sprite_rect)
            self.display_surface.blit(sprite_text_25, sprite_rect_25)
            self.display_surface.blit(sprite_image_diamond, sprite_rect_diamond)
            self.display_surface.blit(sprite_text_50, sprite_rect_50)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(pointer):
                        self.buy_lives()
                    if options_button.checkForInput(pointer):
                        self.skip_level()
                    if quit_button.checkForInput(pointer):
                        self.run()

            pygame.display.update()
   
    def cover(self):
        background_image = pygame.image.load(join('..', 'graphics', 'backgrounds','cover.png'))
        while True:
            self.display_surface.blit(background_image, (0, 0))
            main_menu_text = self.get_font(120).render("CALL OF THE WILD", True, "#000000")
            main_menu_rect = main_menu_text.get_rect(center=(640, 140))
            
            txt_menu_text = self.get_font(25).render("PRESS SPACE TO CONTINUE", True, "#1addeb")
            txt_menu_rect = txt_menu_text.get_rect(center=(1150, 980))
            
            self.display_surface.blit(main_menu_text, main_menu_rect)
            self.display_surface.blit(txt_menu_text, txt_menu_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.main_menu()
                    
            pygame.display.update()

def main():
    game = Game()
    game.cover()
    
main()
