from settings import *
from level import Level, MazeLevel
from data import Data
from ui import UI
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *

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
        self.tmx_maps = {
            0: load_pygame(join('..', 'data', 'tundra', 'levels', 'platformer.tmx')),
            1: load_pygame(join('..', 'data', 'levels', 'forest_2.tmx'))}
        self.current_stage = Level(self.tmx_maps[0], self.level_frames, self.data)
        
        self.click = False
       
    def switch_stage(self, target, unlock = 0):
        if target == 'level':
            pass
        else:
            # self.current_stage = 
            pass
        
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
            'penguin' : import_folder('..', 'graphics', 'animals', 'penguin')
        }
        self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'coin' : import_folder(join('..', 'graphics', 'ui', 'coin')),
            'heart' : import_folder(join('..', 'graphics', 'ui', 'heart'))
        }
        
    # def draw_text(self, text, font, color, surface, x, y):
    #     textobj = font.render(text, 1, color)
    #     textrect = textobj.get_rect()
    #     textrect.topleft = (x,y)
    #     surface.blit(textobj, textrect)
        
        
    # def pause_menu(self):
    #     while True:
    #         self.display_surface.fill((0,0,0))
    #         print(92834)
    #         # self.draw_text('Paused', self.font, (255,255,255), self.display_surface, 40, 40)
            
    #         mx, my = pygame.mouse.get_pos()
            
    #         button_1 = pygame.Rect(50, 200, 200, 50)
    #         button_2 = pygame.Rect(50, 300, 200, 50)
    #         if button_1.collidepoint((mx, my)):
    #             if self.click:
    #                 break
    #         if button_2.collidepoint((mx, my)):
    #             if self.click:
    #                 pass
    #         pygame.draw.rect(self.display_surface, (255,255,0), button_1)
    #         pygame.draw.rect(self.display_surface, (255,255,0), button_2)
        
    def run(self):
        while True:
            # self.click = False
            dt =self.clock.tick(100) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_ESCAPE:
                #         self.pause_menu()

            self.current_stage.run(dt)
            self.ui.update(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()