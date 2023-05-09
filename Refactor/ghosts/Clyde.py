from .Ghost import Ghost
import pygame
import os
import math

from Refactor.enums import EntityDirection

lib_path = os.path.dirname(__file__)


class Clyde(Ghost):
    def __init__(self, context, speed=2):
        super().__init__(context, speed)
        self.image_path = os.path.abspath(os.path.join(lib_path, '../resources/clyde.png'))
        self.standard_image = pygame.transform.scale(pygame.image.load(self.image_path),
                                                     (self.image_size, self.image_size))
        self.image = self.standard_image
        self.rect = self.image.get_bounding_rect()
        self.image = self.image.subsurface(self.rect)
        self.previous_tile = (12, 16)
        self.next_tile = (12, 16)
        self.target_color = (255, 182, 82)
        self.scatter_target = (1, 32)
        self.rect.center = self.calculate_center_for_tile(self.previous_tile[0], self.previous_tile[1])

    def update(self):
        super().update()
        pass

    def scatter(self):
        self.target = self.scatter_target

    def chase(self):
        pacman_tile = super().get_game_context().pacman.get_entity_current_tile()
        tile_x, tile_y = self.get_entity_current_tile()
        if int(math.fabs(tile_x - pacman_tile[0])) <= 8 and int(math.fabs(tile_y - pacman_tile[1])) <= 8:
            self.target = super().get_game_context().pacman.get_entity_current_tile()
        else:
            self.target = (29, 1)
