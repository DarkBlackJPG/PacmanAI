import pygame

import Refactor.PacmanGame as PacmanGame


class Entity(pygame.sprite.Sprite):
    def __init__(self,
                 context: PacmanGame,
                 speed=1):
        super().__init__()
        self._game_context = context
        self.speed = speed
        self.screen = self._game_context.get_screen()
        self.tile_width, self.tile_height = self._game_context.get_tile_width_and_height()
        self.rect = None

    def wiggle_factor(self, modulo, factor):
        return factor * 0.38 <= modulo <= factor * 0.62

    def get_game_context(self):
        return self._game_context

    def get_entity_current_tile(self, error_x=0, error_y=0):
        center_x, center_y = self.rect.center
        return (center_x + error_x) // self.tile_width, (error_y + center_y) // self.tile_height
