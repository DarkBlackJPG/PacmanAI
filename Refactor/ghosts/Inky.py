from .Ghost import Ghost
import pygame
import os
import math
from Refactor.enums import EntityDirection

lib_path = os.path.dirname(__file__)


class Inky(Ghost):
    def __init__(self, context, speed=2):
        super().__init__(context, speed)
        self.image_path = os.path.abspath(os.path.join(lib_path, '../resources/inky.png'))
        self.standard_image = pygame.transform.scale(pygame.image.load(self.image_path),
                                                     (self.image_size, self.image_size))
        self.image = self.standard_image
        self.rect = self.image.get_bounding_rect()
        self.image = self.image.subsurface(self.rect)
        self.previous_tile = (17, 14)
        self.next_tile = (17, 14)
        self.target_color = (0, 255, 255)
        self.scatter_target = (29, 32)
        self.rect.center = self.calculate_center_for_tile(self.previous_tile[0], self.previous_tile[1])

    def update(self):
        super().update()

    def scatter(self):
        self.target = self.scatter_target

    def chase(self):
        pacman_tile = super().get_game_context().pacman.get_entity_current_tile()
        blinky_tile = super().get_game_context().blinky.get_entity_current_tile()
        pacman_direction = super().get_game_context().pacman.direction
        if pacman_direction == EntityDirection.UP:
            pacman_tile = (pacman_tile[0] - 2, pacman_tile[1] - 2)
        elif pacman_direction == EntityDirection.DOWN:
            pacman_tile = (pacman_tile[0], pacman_tile[1] + 2)
        elif pacman_direction == EntityDirection.LEFT:
            pacman_tile = (pacman_tile[0] - 2, pacman_tile[1])
        elif pacman_direction == EntityDirection.RIGHT:
            pacman_tile = (pacman_tile[0] + 2, pacman_tile[1])
        (dx, dy) = (int(math.fabs(pacman_tile[0] - blinky_tile[0])), int(math.fabs(pacman_tile[1] - blinky_tile[1])))
        self.target = (int(math.fabs(pacman_tile[0] - dx)), int(math.fabs(pacman_tile[1] - dy)))
