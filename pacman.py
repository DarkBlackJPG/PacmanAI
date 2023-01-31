import math

import pygame

import board
from board import board_definition
from enum import Enum


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
        self.tile_width = (self.WIDTH // 30)
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.run = True
        self.board_definition = board_definition
        self.wall_width = 5
        self.pacman = Pacman(self, 20)

    def update(self):
        if not self.run:
            pygame.quit()
            return

        self.timer.tick(self.fps)
        self.screen.fill('black')

        self.draw_board()
        self.pacman.update()

        self.handle_events()

        pygame.display.flip()

    def calculate_center(self, x, y):
        return x * self.tile_width + (0.5 * self.tile_height), y * self.tile_height + (0.5 * self.tile_width)

    def draw_board(self):
        for i in range(len(self.board_definition)):
            for j in range(len(self.board_definition[i])):
                board_element = board_definition[i][j]
                if board_element == 1:
                    pygame.draw.circle(self.screen, 'beige', self.calculate_center(j, i), 4)
                    pass
                elif board_element == 2:
                    pygame.draw.circle(self.screen, 'beige', self.calculate_center(j, i), 10)
                    pass
                elif board_element == 3:
                    begin, end = self.calculate_vertical(j, i)
                    pygame.draw.line(self.screen, (65, 107, 186), begin, end, self.wall_width)
                    pass
                elif board_element == 4:
                    begin, end = self.calculate_horizontal(j, i)
                    pygame.draw.line(self.screen, (65, 107, 186), begin, end, self.wall_width)
                    pass
                elif board_element == 5:
                    rect, arc_begin, arc_end = self.calculate_upper_right_arc(j, i)
                    pygame.draw.arc(self.screen, (65, 107, 186), rect, arc_begin, arc_end, self.wall_width)
                    pass
                elif board_element == 6:
                    rect, arc_begin, arc_end = self.calculate_upper_left_arc(j, i)
                    pygame.draw.arc(self.screen, (65, 107, 186), rect, arc_begin, arc_end, self.wall_width)
                    pass
                elif board_element == 7:
                    rect, arc_begin, arc_end = self.calculate_bottom_left_arc(j, i)
                    pygame.draw.arc(self.screen, (65, 107, 186), rect, arc_begin, arc_end, self.wall_width)
                    pass
                elif board_element == 8:
                    rect, arc_begin, arc_end = self.calculate_bottom_right_arc(j, i)
                    pygame.draw.arc(self.screen, (65, 107, 186), rect, arc_begin, arc_end, self.wall_width)
                    pass
                elif board_element == 9:
                    begin, end = self.calculate_horizontal(j, i)
                    pygame.draw.line(self.screen, 'white', begin, end)
                    pass
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



class Pacman:

    def __init__(self, context: PacmanGame, speed=2):
        self.context = context
        self.image_size = 40
        self.error = 20
        self.image = pygame.transform.scale(pygame.image.load(f'pacman.png'), (self.image_size, self.image_size))
        self.pos_x = 430
        self.pos_y = 665
        self.screen = self.context.get_screen()
        self.direction = Direction.RIGHT
        self.speed = speed
        self.tile_width = self.context.get_tile_width()
        self.tile_height = self.context.get_tile_height()

    def update(self):
        self.draw()
        self.move()

    def draw(self):
        if self.direction == Direction.UP:
            self.screen.blit(pygame.transform.rotate(self.image, 90), (self.pos_x, self.pos_y))
        elif self.direction == Direction.DOWN:
            self.screen.blit(pygame.transform.rotate(self.image, 270), (self.pos_x, self.pos_y))
        elif self.direction == Direction.LEFT:
            self.screen.blit(pygame.transform.flip(self.image, True, False), (self.pos_x, self.pos_y))
        elif self.direction == Direction.RIGHT:
            self.screen.blit(self.image, (self.pos_x, self.pos_y))

    def change_facing_direction(self, direction: Direction = None):
        if direction is not None and self.valid_move(direction):
            self.direction = direction

    def move(self):
        tile_x, tile_y = self.get_tiles()
        if board_definition[tile_y][tile_x] < 3:
            board_definition[tile_y][tile_x] = 0;
        if self.direction == Direction.LEFT and self.valid_move(Direction.LEFT):
            self.pos_x -= self.speed
        elif self.direction == Direction.RIGHT and self.valid_move(Direction.RIGHT):
            self.pos_x += self.speed
        elif self.direction == Direction.UP and self.valid_move(Direction.UP):
            self.pos_y -= self.speed
        elif self.direction == Direction.DOWN and self.valid_move(Direction.DOWN):
            self.pos_y += self.speed
        pass

    def check_collision(self):
        center_x, center_y = self.get_center()
        if center_x // 30 < 29:
            if self.direction == Direction.RIGHT and board.board_definition[center_y // self.tile_height][
                (center_x - self.error) // self.tile_width] < 3:
                return True
            if self.direction == Direction.LEFT and board.board_definition[center_y // self.tile_height][
                (center_x - self.error) // self.tile_width] < 3:
                return True
            if self.direction == Direction.UP and board.board_definition[center_y // self.tile_height][
                (center_x - self.error) // self.tile_width] < 3:
                return True
            if self.direction == Direction.DOWN and board.board_definition[center_y // self.tile_height][
                (center_x - self.error) // self.tile_width] < 3:
                return True
        else:
            pass
        pass

    def get_center(self):
        return self.pos_x + (self.image_size // 2) + 1, self.pos_y + (self.image_size // 2) + 1

    def valid_move(self, next_direction):
        if next_direction == Direction.LEFT:
            tile_x, tile_y = self.get_tiles(-self.error, 0)
            if board_definition[tile_y][tile_x] > 2:
                return False

        elif next_direction == Direction.RIGHT:
            tile_x, tile_y = self.get_tiles(self.error, 0)
            if board_definition[tile_y][tile_x] > 2:
                return False

        elif next_direction == Direction.UP:
            tile_x, tile_y = self.get_tiles(0, -self.error)
            if board_definition[tile_y][tile_x] > 2:
                return False

        elif next_direction == Direction.DOWN:
            tile_x, tile_y = self.get_tiles(0, self.error)
            if board_definition[tile_y][tile_x] > 2:
                return False

        return True

    def get_tiles(self, error_x=0, error_y=0):
        center_x, center_y = self.get_center()
        return (center_x + error_x) // self.tile_width, (error_y + center_y) // self.tile_height


if __name__ == '__main__':
    game = PacmanGame()
    while game.run:
        game.update()
