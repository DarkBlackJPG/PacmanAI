import pygame
import OriginalGame.PacmanGame as PacmanGame
import OriginalGame.entity as entity
import OriginalGame.enums.State as State
import OriginalGame.enums.Direction as Direction
import random
import time
import math
import os






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
        pacman_tile = self.context.pacman.get_entity_current_tile()
        pacman_direction = self.context.pacman.direction
        if pacman_direction == Direction.Direction.UP:
            pacman_tile = (pacman_tile[0] - 4, pacman_tile[1] - 4)
        elif pacman_direction == Direction.Direction.DOWN:
            pacman_tile = (pacman_tile[0], pacman_tile[1] + 4)
        elif pacman_direction == Direction.Direction.LEFT:
            pacman_tile = (pacman_tile[0] - 4, pacman_tile[1])
        elif pacman_direction == Direction.Direction.RIGHT:
            pacman_tile = (pacman_tile[0] + 4, pacman_tile[1])

        self.target = pacman_tile


class Inky(Ghost):
    def __init__(self, context, speed=2):
        super().__init__(context, speed)
        self.image_path = os.path.abspath(os.path.join(lib_path, '../resources/inky.png'))
        self.standard_image = pygame.transform.scale(pygame.image.load(self.image_path),
                                                     (self.image_size, self.image_size))
        self.image = self.standard_image
        self.rect = self.image.get_bounding_rect()
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
        pacman_tile = self.context.pacman.get_entity_current_tile()
        blinky_tile = self.context.blinky.get_entity_current_tile()
        pacman_direction = self.context.pacman.direction
        if pacman_direction == Direction.Direction.UP:
            pacman_tile = (pacman_tile[0] - 2, pacman_tile[1] - 2)
        elif pacman_direction == Direction.Direction.DOWN:
            pacman_tile = (pacman_tile[0], pacman_tile[1] + 2)
        elif pacman_direction == Direction.Direction.LEFT:
            pacman_tile = (pacman_tile[0] - 2, pacman_tile[1])
        elif pacman_direction == Direction.Direction.RIGHT:
            pacman_tile = (pacman_tile[0] + 2, pacman_tile[1])
        (dx, dy) = (int(math.fabs(pacman_tile[0] - blinky_tile[0])), int(math.fabs(pacman_tile[1] - blinky_tile[1])))
        self.target = (int(math.fabs(pacman_tile[0] - dx)), int(math.fabs(pacman_tile[1] - dy)))


class Clyde(Ghost):
    def __init__(self, context, speed=2):
        super().__init__(context, speed)
        self.image_path = os.path.abspath(os.path.join(lib_path, '../resources/clyde.png'))
        self.standard_image = pygame.transform.scale(pygame.image.load(self.image_path),
                                                     (self.image_size, self.image_size))
        self.image = self.standard_image
        self.rect = self.image.get_bounding_rect()
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
        pacman_tile = self.context.pacman.get_entity_current_tile()
        tile_x, tile_y = self.get_entity_current_tile()
        if int(math.fabs(tile_x - pacman_tile[0])) <= 8 and int(math.fabs(tile_y - pacman_tile[1])) <= 8:
            self.target = self.context.pacman.get_entity_current_tile()
        else:
            self.target = (29, 1)


class Blinky(Ghost):
    def __init__(self, context, speed=2):
        super().__init__(context, speed)
        self.image_path = os.path.abspath(os.path.join(lib_path, '../resources/blinky.png'))
        self.standard_image = pygame.transform.scale(pygame.image.load(self.image_path),
                                                     (self.image_size, self.image_size))
        self.image = self.standard_image
        self.rect = self.image.get_bounding_rect()
        self.previous_tile = (17, 16)
        self.next_tile = (17, 16)
        self.target_color = (255, 0, 0)
        self.scatter_target = (29, 1)
        self.rect.center = self.calculate_center_for_tile(self.previous_tile[0], self.previous_tile[1])

    def update(self):
        super().update()

    def scatter(self):
        if self.context.number_of_small_pellets + self.context.number_of_powerups <= 20:
            self.target = self.context.pacman.get_entity_current_tile()
            return
        self.target = self.scatter_target

    def chase(self):
        self.target = self.context.pacman.get_entity_current_tile()
