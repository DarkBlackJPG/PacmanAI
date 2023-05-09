from .Ghost import Ghost
import pygame
import os

from Refactor.enums import EntityDirection

lib_path = os.path.dirname(__file__)


class Pinky(Ghost):
    def __init__(self, context, speed=2):
        super().__init__(context, speed)
        self.image_path = os.path.abspath(os.path.join(lib_path, '../resources/pinky.png'))
        self.standard_image = pygame.transform.scale(pygame.image.load(self.image_path),
                                                     (self.image_size, self.image_size))
        self.image = self.standard_image
        self.rect = self.image.get_bounding_rect()
        self.image = self.image.subsurface(self.rect)
        self.current_tile = (12, 14)
        self.next_tile = (12, 14)
        self.scatter_target = (0, 0)
        self.target_color = (255, 184, 255)
        self.rect.center = self.calculate_center_for_tile(self.current_tile[0], self.current_tile[1])

    def update(self):
        super().update()

    def scatter(self):
        self.target = self.scatter_target

    def chase(self):
        pacman_tile = super().get_game_context().pacman.get_entity_current_tile()
        pacman_direction = super().get_game_context().pacman.direction
        if pacman_direction == EntityDirection.UP:
            pacman_tile = (pacman_tile[0] - 4, pacman_tile[1] - 4)
        elif pacman_direction == EntityDirection.DOWN:
            pacman_tile = (pacman_tile[0], pacman_tile[1] + 4)
        elif pacman_direction == EntityDirection.LEFT:
            pacman_tile = (pacman_tile[0] - 4, pacman_tile[1])
        elif pacman_direction == EntityDirection.RIGHT:
            pacman_tile = (pacman_tile[0] + 4, pacman_tile[1])

        self.target = pacman_tile
