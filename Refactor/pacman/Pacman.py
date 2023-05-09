import pygame
import Refactor.PacmanGame as PacmanGame
import math
import Refactor.entity as entity
from Refactor.enums import EntityDirection
from Refactor.enums import RenderType
from Refactor.enums import InputType
import os

lib_path = os.path.dirname(__file__)


class Pacman(entity.Entity.Entity):
    def __init__(self, context: PacmanGame, start_position=(15, 25), speed=1):
        super().__init__(context, speed)
        self.tile_width = super().get_game_context().get_tile_width()
        self.tile_height = super().get_game_context().get_tile_height()
        self.image_size = self.tile_width
        self.turn_error = math.floor(self.image_size * 0.55)
        self.error = math.floor(self.image_size * 0.49)
        self.original_image = pygame.transform.scale(
            pygame.image.load(os.path.abspath(os.path.join(lib_path, '../resources/pacman.png'))),
            (self.image_size, self.image_size))
        self.image = self.original_image
        self.rect = self.image.get_bounding_rect()
        self.start_position = start_position
        self.rect.center = (self.tile_width * start_position[0], self.tile_height * start_position[1] - self.image_size * 0.5)
        self.screen = super().get_game_context().get_screen()
        self.direction = EntityDirection.RIGHT
        self.direction_request = EntityDirection.RIGHT

    def update(self):
        if self.direction == EntityDirection.UP:
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == EntityDirection.DOWN:
            self.image = pygame.transform.rotate(self.original_image, 270)
        elif self.direction == EntityDirection.LEFT:
            self.image = pygame.transform.flip(self.original_image, True, False)
        elif self.direction == EntityDirection.RIGHT:
            self.image = self.original_image
        #
        # if not self.context.pause:
        self.move()

    def change_facing_direction(self, direction: EntityDirection = None):
        if direction is not None:
            self.direction_request = direction

    def move(self):
        tile_x, tile_y = self.get_entity_current_tile()

        if 30 > tile_x >= 0 and super().get_game_context().board_definition[tile_y][tile_x] < 3:
            if super().get_game_context().board_definition[tile_y][tile_x] == 2:
                super().get_game_context().powerup()
            elif super().get_game_context().board_definition[tile_y][tile_x] == 1:
                super().get_game_context().small_pellet_eaten()

            super().get_game_context().board_definition[tile_y][tile_x] = 0

        if self.direction != self.direction_request:
            if self.direction_request == EntityDirection.LEFT:
                tile_x_t, tile_y_t = self.get_entity_current_tile(-self.turn_error, 0)
                if self.valid_move(tile_x_t, tile_y_t) and self.wiggle_factor(self.rect.centery % self.tile_height, self.tile_height):
                    self.rect.centerx -= self.speed
                    self.direction = self.direction_request

            elif self.direction_request == EntityDirection.RIGHT:
                tile_x_t, tile_y_t = self.get_entity_current_tile(self.turn_error, 0)
                if self.valid_move(tile_x_t, tile_y_t) and self.wiggle_factor(self.rect.centery % self.tile_height, self.tile_height):
                    self.rect.centerx += self.speed
                    self.direction = self.direction_request

            elif self.direction_request == EntityDirection.UP:
                tile_x_t, tile_y_t = self.get_entity_current_tile(0, -self.turn_error)
                if self.valid_move(tile_x_t, tile_y_t) and self.wiggle_factor(self.rect.centerx % self.tile_width, self.tile_width):
                    self.rect.centery -= self.speed
                    self.direction = self.direction_request

            elif self.direction_request == EntityDirection.DOWN:
                tile_x_t, tile_y_t = self.get_entity_current_tile(0, self.turn_error)
                if self.valid_move(tile_x_t, tile_y_t) and self.wiggle_factor(self.rect.centerx % self.tile_width, self.tile_width):
                    self.rect.centery += self.speed
                    self.direction = self.direction_request

        if self.direction == EntityDirection.LEFT:
            tile_x_t, tile_y_t = self.get_entity_current_tile(-self.error, 0)
            if self.valid_move(tile_x_t, tile_y_t):
                self.rect.centerx -= self.speed
        elif self.direction == EntityDirection.RIGHT:
            tile_x_t, tile_y_t = self.get_entity_current_tile(self.error, 0)
            if self.valid_move(tile_x_t, tile_y_t):
                self.rect.centerx += self.speed
        elif self.direction == EntityDirection.UP:
            tile_x_t, tile_y_t = self.get_entity_current_tile(0, -self.error)
            if self.valid_move(tile_x_t, tile_y_t):
                self.rect.centery -= self.speed
        elif self.direction == EntityDirection.DOWN:
            tile_x_t, tile_y_t = self.get_entity_current_tile(0, self.error)
            if self.valid_move(tile_x_t, tile_y_t):
                self.rect.centery += self.speed

        # if self.rect.left > 900:
        #     self.rect.left = -47
        # elif self.rect.left < -50:
        #     self.rect.left = 897


    def valid_move(self, tile_x, tile_y):
        if tile_x < 0 or tile_x > len(super().get_game_context().board_definition[0]) - 1 and self.direction in (
                EntityDirection.LEFT, EntityDirection.RIGHT, self.direction_request):
            return True
        if super().get_game_context().board_definition[tile_y][tile_x] >= 3:
            return False
        return True

