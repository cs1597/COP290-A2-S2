from settings import *
from level import Level, MazeLevel
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from overworld import Overworld
from data import Data

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pygame Platformer')
        self.clock = pygame.time.Clock()
        self.import_assets()
        # data contains the ui elements like health, score, etc
        self.data=Data(self)
        # have just made it none for now, beacue needed on the front page
        self.tmx_maps = {0: load_pygame(join('..', 'data', 'levels', 'forest_deer_rescue_maze.tmx')),
                         1: load_pygame(join('..', 'data', 'levels', 'forest_2.tmx')),
                         2: load_pygame(join('..', 'data', 'tundra','levels', 'platformer.tmx'))
                         }
        self.tmx_overworld = load_pygame(join('..', 'data', 'overworld', 'overworld.tmx'))
        # self.current_stage = MazeLevel(self.tmx_maps[3], self.level_frames)
        self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames)
        
    # def switch_stage(self,target,unlock=0):
    #     if target=='level':
    #         self.current_stage=Level()
    #     else: 
    #         self.current_stage = Overworld()

    def import_assets(self):
        self.level_frames = {
            'items' : import_sub_folders('..', 'graphics', 'items'),
            'effects' : import_sub_folders('..', 'graphics', 'effects'),
            'player' : import_sub_folders('..', 'graphics', 'player'),
            'maze_player' : import_sub_folders('..', 'graphics', 'maze_player'),
            'spikes' : import_folder('..', 'graphics', 'enemies', 'floor_spikes'),
            'helicopter' : import_folder('..', 'graphics', 'levels', 'tundra', 'helicopter'),
            'boat' : import_folder('..', 'graphics', 'levels', 'tundra', 'boat'),
            'gunner' : import_folder('..', 'graphics', 'enemies', 'gunner'),
            'bullet' : import_folder('..', 'graphics', 'enemies', 'bullet'),
            'elephant' : import_folder('..', 'graphics', 'animals', 'elephant'),
            'penguin' : import_folder('..', 'graphics', 'animals', 'penguin'),
            'overworld_char' : import_sub_folders('..', 'graphics', 'overworld_character'),
            'level_icon': import_folder('..', 'graphics', 'overworld_map', 'point_loc'),
        }
        self.overworld_frames = {
            'point_loc' : import_folder('..', 'graphics', 'overworld_map', 'point_loc'),
            'icon': import_sub_folders('..', 'graphics', 'overworld_character'),
        }
        
    def run(self):
        while True:
            dt =self.clock.tick(100) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.current_stage.run(dt)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()