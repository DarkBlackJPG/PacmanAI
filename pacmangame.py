import math
import pprint

import pygame

import board
from board import board_definition
from enum import Enum

DEBUG = True
GRID = False


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class PacmanGame:
    def __init__(self):
        pygame.init()
        self.WIDTH = 900
        self.HEIGHT = 950
        self.tile_height = ((self.HEIGHT - 50) // 32)
        self.wall_color = (65, 107, 186)
        self.circle_color = 'beige'
        self.ghost_wall_color = 'white'
        self.wall_color = (65, 107, 186)
        self.tile_width = (self.WIDTH // 30)
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.run = True
        self.board_definition = board_definition
        self.wall_width = 5
        self.pacman_group = pygame.sprite.Group()
        self.pacman = Pacman(self)
        self.pacman_group.add(self.pacman)
        self.debug = DEBUG
        self.ghost_group = pygame.sprite.Group()
        self.pinky = Pinky(self)
        self.inky = Inky(self, 0.0)
        self.clyde = Clyde(self, 0.0)
        self.blinky = Blinky(self, 0.0)
        self.ghost_group.add(self.pinky)
        self.ghost_group.add(self.inky)
        self.ghost_group.add(self.clyde)
        self.ghost_group.add(self.blinky)

    def update(self):
        if not self.run:
            pygame.quit()
            return

        self.timer.tick(self.fps)
        self.screen.fill('black')

        self.draw_board()
        self.ghost_group.draw(self.screen)
        self.pacman_group.draw(self.screen)

        self.pacman_group.update()
        self.ghost_group.update()

        if pygame.sprite.spritecollideany(self.pacman, self.ghost_group):
            print('Booya')

        self.handle_events()

        pygame.display.flip()

    def calculate_center(self, x, y):
        return x * self.tile_width + (0.5 * self.tile_height), y * self.tile_height + (0.5 * self.tile_width)

    def draw_board(self):
        for i in range(len(self.board_definition)):
            for j in range(len(self.board_definition[i])):
                board_element = board_definition[i][j]
                if board_element == 1:
                    pygame.draw.circle(self.screen, self.circle_color, self.calculate_center(j, i), 4)
                    pass
                elif board_element == 2:
                    pygame.draw.circle(self.screen, self.circle_color, self.calculate_center(j, i), 10)
                    pass
                elif board_element == 3:
                    begin, end = self.calculate_vertical(j, i)
                    pygame.draw.line(self.screen, self.wall_color, begin, end, self.wall_width)
                    pass
                elif board_element == 4:
                    begin, end = self.calculate_horizontal(j, i)
                    pygame.draw.line(self.screen, self.wall_color, begin, end, self.wall_width)
                    pass
                elif board_element == 5:
                    rect, arc_begin, arc_end = self.calculate_upper_right_arc(j, i)
                    pygame.draw.arc(self.screen, self.wall_color, rect, arc_begin, arc_end, self.wall_width)
                    pass
                elif board_element == 6:
                    rect, arc_begin, arc_end = self.calculate_upper_left_arc(j, i)
                    pygame.draw.arc(self.screen, self.wall_color, rect, arc_begin, arc_end, self.wall_width)
                    pass
                elif board_element == 7:
                    rect, arc_begin, arc_end = self.calculate_bottom_left_arc(j, i)
                    pygame.draw.arc(self.screen, self.wall_color, rect, arc_begin, arc_end, self.wall_width)
                    pass
                elif board_element == 8:
                    rect, arc_begin, arc_end = self.calculate_bottom_right_arc(j, i)
                    pygame.draw.arc(self.screen, self.wall_color, rect, arc_begin, arc_end, self.wall_width)
                    pass
                elif board_element == 9:
                    begin, end = self.calculate_horizontal(j, i)
                    pygame.draw.line(self.screen, self.ghost_wall_color, begin, end)
                    pass
        if self.debug and GRID:
            blckW = self.tile_width  # Set the size of the grid block
            blckH = self.tile_height  # Set the size of the grid block
            for x in range(0, self.WIDTH, blckW):
                for y in range(0, self.HEIGHT, blckH):
                    rect = pygame.Rect(x, y, blckW, blckH)
                    pygame.draw.rect(self.screen, 'white', rect, 1)
        pass

    def calculate_vertical(self, x, y):
        x_repositioned = x * self.tile_width + self.tile_width * 0.5
        y_repositioned = y * self.tile_height
        return [x_repositioned, y_repositioned], [x_repositioned, y_repositioned + self.tile_height]

    def calculate_horizontal(self, x, y):
        x_repositioned = x * self.tile_width
        y_repositioned = y * self.tile_height + self.tile_height * 0.5
        return [x_repositioned, y_repositioned], [x_repositioned + self.tile_width, y_repositioned]
        pass

    def calculate_upper_left_arc(self, x, y):
        x_repositioned = x * self.tile_width + (self.wall_width * 0.5) + self.wall_width + 6
        y_repositioned = y * self.tile_height + (self.tile_height * 0.5) - 1.5
        rect = pygame.Rect(x_repositioned, y_repositioned, self.tile_width + 5, self.tile_height + 5)
        begin_angle = math.pi / 2
        end_angle = math.pi
        return rect, begin_angle, end_angle

    def calculate_bottom_left_arc(self, x, y):
        x_repositioned = x * self.tile_width + (self.wall_width * 0.5) + self.wall_width + 6
        y_repositioned = y * self.tile_height - (self.tile_height * 0.5) - 1.5
        rect = pygame.Rect(x_repositioned, y_repositioned, self.tile_width + 5, self.tile_height + 5)
        begin_angle = math.pi
        end_angle = 3 * math.pi / 2
        return rect, begin_angle, end_angle

    def calculate_upper_right_arc(self, x, y):
        x_repositioned = x * self.tile_width - (self.wall_width * 0.5) - 15 + 1
        y_repositioned = y * self.tile_height + (self.tile_height * 0.5) - 1.5
        rect = pygame.Rect(x_repositioned, y_repositioned, self.tile_width + 5, self.tile_height + 5)
        begin_angle = 0
        end_angle = math.pi / 2
        return rect, begin_angle, end_angle

    def calculate_bottom_right_arc(self, x, y):
        x_repositioned = x * self.tile_width - 15 - 2
        y_repositioned = y * self.tile_height - 15 - 1.5
        rect = pygame.Rect(x_repositioned, y_repositioned, self.tile_width + 5, self.tile_height + 5)
        begin_angle = 3 * math.pi / 2
        end_angle = 0
        return rect, begin_angle, end_angle

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                self.handle_player_input(event)
        pass

    def handle_player_input(self, event):
        direction = Direction.RIGHT
        if event.key == pygame.K_LEFT:
            direction = Direction.LEFT
        elif event.key == pygame.K_RIGHT:
            direction = Direction.RIGHT
        elif event.key == pygame.K_UP:
            direction = Direction.UP
        elif event.key == pygame.K_DOWN:
            direction = Direction.DOWN
        self.pacman.change_facing_direction(direction)
        pass

    def get_screen(self):
        return self.screen

    def get_tile_width(self):
        return self.tile_width

    def get_tile_height(self):
        return self.tile_height


class Entity(pygame.sprite.Sprite):
    def __init__(self, context: PacmanGame, speed=2):
        super().__init__()
        self.context = context
        self.speed = speed
        self.screen = self.context.screen
        self.tile_width = 0
        self.tile_height = 0
        self.rect: pygame.Rect = None

    def get_tiles(self, error_x=0, error_y=0):
        center_x, center_y = self.rect.center
        if self.context.debug:
            pygame.draw.circle(self.screen, 'cyan', ((center_x + error_x), (error_y + center_y)), 3)
        return (center_x + error_x) // self.tile_width, (error_y + center_y) // self.tile_height


class Pacman(Entity):
    def __init__(self, context: PacmanGame, speed=2):
        super().__init__(context, speed)
        self.context = context
        self.image_size = 40
        self.turn_error = 21
        self.error = 15
        self.original_image = pygame.transform.scale(pygame.image.load(f'pacman.png'),
                                                     (self.image_size, self.image_size))
        self.image = self.original_image
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (430, 685)
        self.screen = self.context.get_screen()
        self.direction = Direction.RIGHT
        self.direction_request = Direction.RIGHT
        self.speed = speed
        self.tile_width = self.context.get_tile_width()
        self.tile_height = self.context.get_tile_height()

    def update(self):
        if self.direction == Direction.UP:
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == Direction.DOWN:
            self.image = pygame.transform.rotate(self.original_image, 270)
        elif self.direction == Direction.LEFT:
            self.image = pygame.transform.flip(self.original_image, True, False)
        elif self.direction == Direction.RIGHT:
            self.image = self.original_image
        self.move()

    def change_facing_direction(self, direction: Direction = None):
        if direction is not None:
            self.direction_request = direction

    def move(self):
        tile_x, tile_y = self.get_tiles()

        if 30 > tile_x >= 0 and board_definition[tile_y][tile_x] < 3:
            board_definition[tile_y][tile_x] = 0

        if self.direction != self.direction_request:
            if self.direction_request == Direction.LEFT:
                tile_x_t, tile_y_t = self.get_tiles(-self.turn_error, 0)
                if self.valid_move(tile_x_t, tile_y_t) and 12 <= self.rect.centery % self.tile_height <= 18:
                    self.rect.centerx -= self.speed
                    self.direction = self.direction_request

            elif self.direction_request == Direction.RIGHT:
                tile_x_t, tile_y_t = self.get_tiles(self.turn_error, 0)
                if self.valid_move(tile_x_t, tile_y_t) and 12 <= self.rect.centery % self.tile_height <= 18:
                    self.rect.centerx += self.speed
                    self.direction = self.direction_request

            elif self.direction_request == Direction.UP:
                tile_x_t, tile_y_t = self.get_tiles(0, -self.turn_error)
                if self.valid_move(tile_x_t, tile_y_t) and 12 <= self.rect.centerx % self.tile_width <= 18:
                    self.rect.centery -= self.speed
                    self.direction = self.direction_request

            elif self.direction_request == Direction.DOWN:
                tile_x_t, tile_y_t = self.get_tiles(0, self.turn_error)
                if self.valid_move(tile_x_t, tile_y_t) and 12 <= self.rect.centerx % self.tile_width <= 18:
                    self.rect.centery += self.speed
                    self.direction = self.direction_request

        if self.direction == Direction.LEFT:
            tile_x_t, tile_y_t = self.get_tiles(-self.error, 0)
            if self.valid_move(tile_x_t, tile_y_t):
                self.rect.centerx -= self.speed
        elif self.direction == Direction.RIGHT:
            tile_x_t, tile_y_t = self.get_tiles(self.error, 0)
            if self.valid_move(tile_x_t, tile_y_t):
                self.rect.centerx += self.speed
        elif self.direction == Direction.UP:
            tile_x_t, tile_y_t = self.get_tiles(0, -self.error)
            if self.valid_move(tile_x_t, tile_y_t):
                self.rect.centery -= self.speed
        elif self.direction == Direction.DOWN:
            tile_x_t, tile_y_t = self.get_tiles(0, self.error)
            if self.valid_move(tile_x_t, tile_y_t):
                self.rect.centery += self.speed

        if self.rect.left > 900:
            self.rect.left = -47
        elif self.rect.left < -50:
            self.rect.left = 897

    def valid_move(self, tile_x, tile_y):
        if tile_x < 0 or tile_x > len(board_definition[0]) - 1 and (
                self.direction == Direction.LEFT or self.direction == Direction.RIGHT or self.direction_request == Direction.LEFT or self.direction_request == Direction.RIGHT):
            return True
        if board_definition[tile_y][tile_x] < 3:
            return True

        return False


class State(Enum):
    SCATTER = 0
    CHASE = 1
    FRIGHTENED = 2
    EATEN = 3


def calculate_euclidian_tile_dist(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)


class Ghost(Entity):
    def __init__(self, context: PacmanGame, speed):
        super().__init__(context, speed)
        self.LEFT = 0
        self.RIGHT = 1
        self.UP = 2
        self.DOWN = 3
        self.previous_turn = self.RIGHT
        self.direction = self.RIGHT
        self.image_size = 35
        self.rect: pygame.Rect = None
        self.directions = [False, False, False, False]
        self.direction_priorities = [self.UP, self.LEFT, self.DOWN, self.RIGHT]
        self.context = context
        self.screen = self.context.screen
        self.speed = speed
        self.tile_width = self.context.tile_width
        self.tile_height = self.context.tile_height
        self.state = State.SCATTER
        self.target = (0, 0)
        self.target_color = (255, 255, 255)

    def update_directions(self):
        tile_x, tile_y = self.get_tiles()
        self.directions = [False, False, False, False]
        if board_definition[tile_y - 1][tile_x] < 3 or board_definition[tile_y - 1][tile_x] == 9:
            self.directions[self.UP] = True
        if board_definition[tile_y + 1][tile_x] < 3 or board_definition[tile_y - 1][tile_x] == 9:
            self.directions[self.DOWN] = True
        if board_definition[tile_y][tile_x - 1] < 3 or board_definition[tile_y - 1][tile_x] == 9:
            self.directions[self.LEFT] = True
        if board_definition[tile_y][tile_x + 1] < 3 or board_definition[tile_y - 1][tile_x] == 9:
            self.directions[self.RIGHT] = True

    def update(self):
        self.update_directions()
        self.draw_directions()
        self.draw_target(self.target_color)
        self.draw_line_to_target(self.target_color)

        if self.state == State.SCATTER:
            self.scatter()
        elif self.state == State.CHASE:
            self.chase()
        elif self.state == State.FRIGHTENED:
            self.frightened()
        elif self.state == State.EATEN:
            self.eaten()

        best_direction = self.get_best_direction()
        self.move(best_direction)

    def scatter(self):
        pass

    def chase(self):
        pass

    def frightened(self):
        pass

    def eaten(self):
        pass

    def draw_directions(self):
        if self.context.debug:
            if self.directions[self.LEFT]:
                pygame.draw.circle(self.screen, 'green', (self.rect.centerx - self.tile_width, self.rect.centery), 3)
                pass
            else:
                pygame.draw.circle(self.screen, 'red', (self.rect.centerx - self.tile_width, self.rect.centery), 3)

            if self.directions[self.RIGHT]:
                pygame.draw.circle(self.screen, 'green', (self.rect.centerx + self.tile_width, self.rect.centery), 3)
                pass
            else:
                pygame.draw.circle(self.screen, 'red', (self.rect.centerx + self.tile_width, self.rect.centery), 3)

            if self.directions[self.UP]:
                pygame.draw.circle(self.screen, 'green', (self.rect.centerx, self.rect.centery - self.tile_height), 3)
                pass
            else:
                pygame.draw.circle(self.screen, 'red', (self.rect.centerx, self.rect.centery - self.tile_height), 3)

            if self.directions[self.DOWN]:
                pygame.draw.circle(self.screen, 'green', (self.rect.centerx, self.rect.centery + self.tile_height), 3)
                pass
            else:
                pygame.draw.circle(self.screen, 'red', (self.rect.centerx, self.rect.centery + self.tile_height), 3)

    def draw_target(self, color):
        if self.context.debug:
            pygame.draw.circle(self.screen, color,
                               (self.target[0] * self.tile_width, self.target[1] * self.tile_height), 5)

    def draw_line_to_target(self, color):
        if self.context.debug:
            pygame.draw.line(self.screen, color, self.rect.center,
                             (self.target[0] * self.tile_width, self.target[1] * self.tile_height), 2)

    def get_best_direction(self):
        tile_x, tile_y = self.get_tiles()
        best_distance = 1000
        best_direction = self.direction

        if self.directions[self.UP]:
            temp_dist = calculate_euclidian_tile_dist((tile_x, tile_y - 1), self.target)
            if temp_dist < best_distance:
                best_distance = temp_dist
                if self.previous_turn != self.UP:
                    best_direction = self.UP

        if self.directions[self.LEFT]:
            temp_dist = calculate_euclidian_tile_dist((tile_x - 1, tile_y), self.target)
            if temp_dist < best_distance:
                best_distance = temp_dist
                if self.previous_turn != self.LEFT:
                    best_direction = self.LEFT

        if self.directions[self.DOWN]:
            temp_dist = calculate_euclidian_tile_dist((tile_x, tile_y + 1), self.target)
            if temp_dist < best_distance:
                best_distance = temp_dist
                if self.previous_turn != self.DOWN:
                    best_direction = self.DOWN

        if self.directions[self.RIGHT]:
            temp_dist = calculate_euclidian_tile_dist((tile_x + 1, tile_y), self.target)
            if temp_dist < best_distance:
                if self.previous_turn != self.RIGHT:
                    best_direction = self.RIGHT

        return best_direction

    def move(self, best_direction):
        if best_direction == self.UP:
            if self.direction != self.UP:
                self.previous_turn = self.direction
                self.direction = self.UP
            self.rect.centery -= self.speed

        elif best_direction == self.LEFT:
            if self.direction != self.LEFT:
                self.previous_turn = self.direction
                self.direction = self.LEFT
            self.rect.centerx -= self.speed

        elif best_direction == self.DOWN:
            if self.direction != self.DOWN:
                self.previous_turn = self.direction
                self.direction = self.DOWN
            self.rect.centery += self.speed

        elif best_direction == self.RIGHT:
            if self.direction != self.RIGHT:
                self.previous_turn = self.direction
                self.direction = self.RIGHT
            self.rect.centerx += self.speed


class Pinky(Ghost):
    def __init__(self, context: PacmanGame, speed=2):
        super().__init__(context, speed)
        self.image_path = f'pinky.png'
        self.image = pygame.transform.scale(pygame.image.load(self.image_path), (self.image_size, self.image_size))
        self.rect = self.image.get_bounding_rect()
        self.image = self.image.subsurface(self.rect)
        self.rect.center = (400, 410)
        self.scatter_target = (1, 1)
        self.target = (15, 12)
        self.target_color = (255, 184, 255)

    def update(self):
        super().update()
        pass


class Inky(Ghost):
    def __init__(self, context: PacmanGame, speed=2):
        super().__init__(context, speed)
        self.image_path = f'inky.png'
        self.image = pygame.transform.scale(pygame.image.load(self.image_path), (self.image_size, self.image_size))
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (400, 460)
        self.target_color = (0, 255, 255)
        self.scatter_target = (29, 32)
        self.target = (29, 32)

    def update(self):
        # super().update()

        pass


class Clyde(Ghost):
    def __init__(self, context: PacmanGame, speed=2):
        super().__init__(context, speed)
        self.image_path = f'clyde.png'
        self.image = pygame.transform.scale(pygame.image.load(self.image_path), (self.image_size, self.image_size))
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (450, 410)
        self.target_color = (255, 182, 82)
        self.scatter_target = (29, 1)
        self.target = (29, 1)

    def update(self):
        # super().update()
        pass


class Blinky(Ghost):
    def __init__(self, context: PacmanGame, speed=2):
        super().__init__(context, speed)
        self.image_path = f'blinky.png'
        self.image = pygame.transform.scale(pygame.image.load(self.image_path), (self.image_size, self.image_size))
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (500, 460)
        self.target_color = (255, 0, 0)
        self.scatter_target = (1, 32)
        self.target = (1, 32)

    def update(self):
        # super().update()
        pass


if __name__ == '__main__':
    game = PacmanGame()
    while game.run:
        game.update()
