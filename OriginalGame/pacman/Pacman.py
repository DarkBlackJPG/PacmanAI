import pygame
import OriginalGame.PacmanGame as PacmanGame
import OriginalGame.entity as entity
import OriginalGame.enums.Direction as Direction
import os


lib_path = os.path.dirname(__file__)


class Pacman(entity.Entity.Entity):
    def __init__(self, context: PacmanGame, speed=10):
        super().__init__(context, speed)
        self.context = context
        self.image_size = 40
        self.turn_error = 21
        self.error = 15
        self.original_image = pygame.transform.scale(pygame.image.load(os.path.abspath(os.path.join(lib_path, '../resources/pacman.png'))),
                                                     (self.image_size, self.image_size))
        self.image = self.original_image
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (430, 685)
        self.screen = self.context.get_screen()
        self.direction = Direction.Direction.RIGHT
        self.direction_request = Direction.Direction.RIGHT
        self.tile_width = self.context.get_tile_width()
        self.tile_height = self.context.get_tile_height()

    def update(self):
        if self.direction == Direction.Direction.UP:
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == Direction.Direction.DOWN:
            self.image = pygame.transform.rotate(self.original_image, 270)
        elif self.direction == Direction.Direction.LEFT:
            self.image = pygame.transform.flip(self.original_image, True, False)
        elif self.direction == Direction.Direction.RIGHT:
            self.image = self.original_image

        if not self.context.pause:
            self.move()

    def change_facing_direction(self, direction: Direction.Direction = None):
        if direction is not None:
            self.direction_request = direction

    def move(self):
        tile_x, tile_y = self.get_entity_current_tile()

        if 30 > tile_x >= 0 and self.context.board_definition[tile_y][tile_x] < 3:
            if self.context.board_definition[tile_y][tile_x] == 2:
                self.context.powerup()
            elif self.context.board_definition[tile_y][tile_x] == 1:
                self.context.small_pellet_eaten()

            self.context.board_definition[tile_y][tile_x] = 0

        if self.direction != self.direction_request:
            if self.direction_request == Direction.Direction.LEFT:
                tile_x_t, tile_y_t = self.get_entity_current_tile(-self.turn_error, 0)
                if self.valid_move(tile_x_t, tile_y_t) and 12 <= self.rect.centery % self.tile_height <= 18:
                    self.rect.centerx -= self.speed
                    self.direction = self.direction_request

            elif self.direction_request == Direction.Direction.RIGHT:
                tile_x_t, tile_y_t = self.get_entity_current_tile(self.turn_error, 0)
                if self.valid_move(tile_x_t, tile_y_t) and 12 <= self.rect.centery % self.tile_height <= 18:
                    self.rect.centerx += self.speed
                    self.direction = self.direction_request

            elif self.direction_request == Direction.Direction.UP:
                tile_x_t, tile_y_t = self.get_entity_current_tile(0, -self.turn_error)
                if self.valid_move(tile_x_t, tile_y_t) and 12 <= self.rect.centerx % self.tile_width <= 18:
                    self.rect.centery -= self.speed
                    self.direction = self.direction_request

            elif self.direction_request == Direction.Direction.DOWN:
                tile_x_t, tile_y_t = self.get_entity_current_tile(0, self.turn_error)
                if self.valid_move(tile_x_t, tile_y_t) and 12 <= self.rect.centerx % self.tile_width <= 18:
                    self.rect.centery += self.speed
                    self.direction = self.direction_request

        if self.direction == Direction.Direction.LEFT:
            tile_x_t, tile_y_t = self.get_entity_current_tile(-self.error, 0)
            if self.valid_move(tile_x_t, tile_y_t):
                self.rect.centerx -= self.speed
        elif self.direction == Direction.Direction.RIGHT:
            tile_x_t, tile_y_t = self.get_entity_current_tile(self.error, 0)
            if self.valid_move(tile_x_t, tile_y_t):
                self.rect.centerx += self.speed
        elif self.direction == Direction.Direction.UP:
            tile_x_t, tile_y_t = self.get_entity_current_tile(0, -self.error)
            if self.valid_move(tile_x_t, tile_y_t):
                self.rect.centery -= self.speed
        elif self.direction == Direction.Direction.DOWN:
            tile_x_t, tile_y_t = self.get_entity_current_tile(0, self.error)
            if self.valid_move(tile_x_t, tile_y_t):
                self.rect.centery += self.speed

        if self.rect.left > 900:
            self.rect.left = -47
        elif self.rect.left < -50:
            self.rect.left = 897

    def valid_move(self, tile_x, tile_y):
        if tile_x < 0 or tile_x > len(self.context.board_definition[0]) - 1 and (
                self.direction == Direction.Direction.LEFT
                or self.direction == Direction.Direction.RIGHT
                or self.direction_request == Direction.Direction.LEFT
                or self.direction_request == Direction.Direction.RIGHT):
            return True
        if self.context.board_definition[tile_y][tile_x] < 3:
            return True

        return False
