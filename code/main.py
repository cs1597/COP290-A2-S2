from settings import *
from level import Level
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
        
        self.tmx_maps = {0: load_pygame(join('..', 'data', 'tundra', 'levels', 'platform.tmx'))}
        self.current_stage = Level(self.tmx_maps[0], self.level_frames)
        
    def import_assets(self):
        self.level_frames = {
            'items' : import_sub_folders('..', 'graphics', 'items'),
            'effects' : import_sub_folders('..', 'graphics', 'effects'),
            'player' : import_sub_folders('..', 'graphics', 'player'),
            'spikes' : import_folder('..', 'graphics', 'enemies', 'floor_spikes'),
            'helicopter' : import_folder('..', 'graphics', 'levels', 'tundra', 'helicopter'),
            'gunner' : import_folder('..', 'graphics', 'enemies', 'gunner'),
            'bullet' : import_folder('..', 'graphics', 'enemies', 'bullet')
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