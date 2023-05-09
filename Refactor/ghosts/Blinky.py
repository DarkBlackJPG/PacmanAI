from .Ghost import Ghost
import pygame
import os
import math

from Refactor.enums import EntityDirection

lib_path = os.path.dirname(__file__)


class Blinky(Ghost):
    def __init__(self, context, speed=2):
        super().__init__(context, speed)
        self.image_path = os.path.abspath(os.path.join(lib_path, '../resources/blinky.png'))
        self.standard_image = pygame.transform.scale(pygame.image.load(self.image_path),
                                                     (self.image_size, self.image_size))
        self.image = self.standard_image
        self.rect = self.image.get_bounding_rect()
        self.image = self.image.subsurface(self.rect)
        self.previous_tile = (17, 16)
        self.next_tile = (17, 16)
        self.target_color = (255, 0, 0)
        self.scatter_target = (29, 1)
        self.rect.center = self.calculate_center_for_tile(self.previous_tile[0], self.previous_tile[1])

    def update(self):
        super().update()

    def scatter(self):
        if super().get_game_context().get_number_of_small_pellets() + super().get_game_context().get_number_of_powerups() <= 20:
            self.target = super().get_game_context().pacman.get_entity_current_tile()
            return
        self.target = self.scatter_target

    def chase(self):
        self.target = super().get_game_context().pacman.get_entity_current_tile()
