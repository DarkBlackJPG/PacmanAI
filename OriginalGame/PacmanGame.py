import math
import random
import time
import copy
import pygame
import os
import numpy as np
from enum import Enum

from OriginalGame.pacman import Pacman
from OriginalGame.board import board
from OriginalGame.fruit import Fruit
from OriginalGame.ghosts import Ghosts


DEBUG = False
GRID = False

lib_path = os.path.dirname(__file__)

class RenderType(Enum):
    HUMAN = 0
    RGB_ARRAY = 1


class PacmanGame:
    def __init__(self, render_method: RenderType = RenderType.HUMAN, external_inputs=False, fps=60):
        pygame.init()
        self.small_pellet_size = 4
        self.large_pellet_size = 10
        self.pacman_lives = 3
        self.WIDTH = 400
        self.HEIGHT = 400
        self.num_of_rows = 32
        self.num_of_cols = 30
        self.wall_color = (65, 107, 186)
        self.circle_color = 'beige'
        self.ghost_wall_color = 'white'
        self.wall_color = (65, 107, 186)
        self.external_input_request = None
        self.board_definition = copy.deepcopy(board.board_definition)
        self.power_pellet_time = 10_000

        self._render_method = render_method

        pygame.font.init()
        self.font = pygame.font.Font(os.path.abspath(os.path.join(lib_path, 'resources/joystix.otf')), 20)

        self.external_inputs = external_inputs

        # self.tile_height = ((self.HEIGHT - 50) // 32)
        self.tile_height = (self.HEIGHT // self.num_of_rows)
        self.tile_width = (self.WIDTH // self.num_of_cols)

        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.timer = pygame.time.Clock()
        self.fps = fps
        self.score = 0

        self.run = True

        self.wall_width = 5
        self.debug = DEBUG
        self.pacman = Pacman.Pacman(self)
        self.pacman_group = pygame.sprite.Group()
        self.pacman_group.add(self.pacman)
        self.ghost_group = pygame.sprite.Group()
        self.pinky = Ghosts.Pinky(self)
        self.inky = Ghosts.Inky(self)
        self.clyde = Ghosts.Clyde(self)
        self.blinky = Ghosts.Blinky(self)
        self.ghost_group.add(self.pinky)
        self.ghost_group.add(self.inky)
        self.ghost_group.add(self.clyde)
        self.ghost_group.add(self.blinky)
        self.pause = False
        self.powerup_timer = None
        self.fruit_spawn_points = [
            (10, 12),
            (10, 13),
            (10, 14),
            (10, 15),
            (10, 16),
            (10, 17),
            (10, 18),
            (11, 18),
            (12, 18),
            (13, 18),
            (14, 18),
            (15, 18),
            (16, 18),
            (17, 18),
            (18, 18),
            (19, 18),
            (19, 17),
            (19, 16),
            (19, 15),
            (19, 14),
            (19, 13),
            (19, 12),
            (18, 12),
            (17, 12),
            (16, 12),
            (15, 12),
            (14, 12),
            (13, 12),
            (12, 12),
            (11, 12),
        ]
        self.fruits = [Fruit.Apple(self), Fruit.Strawberry(self), Fruit.Cherry(self)]

        self.fruit_group = pygame.sprite.Group()
        self.fruit_group.add(self.fruits[0])
        self.fruit_group.add(self.fruits[1])
        self.fruit_group.add(self.fruits[2])

        self.number_of_small_pellets = 240
        self.number_of_powerups = 4

        self.small_pellet_score = 10
        self.power_pellet_score = 50
        self.ghost_eat_index = 0
        self.ghost_eat_scores = [200, 400, 800, 1600]

        self.fruit_spawned = False
        self.spawned_fruit_index = 0
        self.fruit_spawned_begin = None
        self.fruit_spawned_timeout = 10 * 1000

        self.fruit_random_spawn_timer = 0
        self.fruit_spawn_timer = 0

        self.score_text = self.font.render('SCORE: 0', False, (255, 255, 255))

    def pacman_dead(self):
        # Soft Reset
        del self.pacman
        del self.inky
        del self.pinky
        del self.clyde
        del self.blinky
        self.pacman_lives -= 1

        if self.pacman_lives == 0:
            self.full_reset()
            return

        self.reset_objects()

    def reset_objects(self):
        self.pacman = Pacman.Pacman(self)
        self.pacman_group = pygame.sprite.Group()
        self.ghost_group = pygame.sprite.Group()
        self.pinky = Ghosts.Pinky(self)
        self.inky = Ghosts.Inky(self)
        self.clyde = Ghosts.Clyde(self)
        self.blinky = Ghosts.Blinky(self)
        self.pacman_group.add(self.pacman)
        self.ghost_group.add(self.pinky)
        self.ghost_group.add(self.inky)
        self.ghost_group.add(self.clyde)
        self.ghost_group.add(self.blinky)

    def ghost_eaten(self):
        self.score += self.ghost_eat_scores[self.ghost_eat_index]
        self.ghost_eat_index += 1
        self.score_text = self.font.render(f'SCORE: {self.score}', False, (255, 255, 255))

    def fruit_spawn(self):
        if not self.fruit_spawned \
                and self.number_of_small_pellets + self.number_of_powerups <= 122 \
                and pygame.time.get_ticks() - self.fruit_spawn_timer >= self.fruit_random_spawn_timer:
            rng = random.Random()
            rng.seed(time.time())

            self.fruit_spawned = True
            self.fruit_spawned_begin = pygame.time.get_ticks()

            self.spawned_fruit_index = rng.randrange(0, 3)
            spawn_point_index = rng.randrange(0, len(self.fruit_spawn_points))
            spawn_point = self.fruit_spawn_points[spawn_point_index]
            self.fruits[self.spawned_fruit_index].rect.center = self.calculate_center(spawn_point[0], spawn_point[1])

    def eat_fruit(self, fruit):
        self.score += fruit.get_points()
        self.score_text = self.font.render(f'SCORE: {self.score}', False, (255, 255, 255))
        self.remove_fruit_reset()

    def remove_fruit_reset(self):
        rng = random.Random()
        rng.seed(time.time())
        self.fruit_spawned = False
        self.fruit_random_spawn_timer = rng.randrange(20000, 50000, 1)
        self.fruit_spawn_timer = pygame.time.get_ticks()
        self.fruits[self.spawned_fruit_index].rect.center = (-100, -100)

    def should_despawn_fruit(self):
        if self.fruit_spawned \
                and pygame.time.get_ticks() - self.fruit_spawned_begin >= self.fruit_spawned_timeout:
            self.remove_fruit_reset()

    def small_pellet_eaten(self):
        self.number_of_small_pellets -= 1
        self.score += self.small_pellet_score

        self.score_text = self.font.render(f'SCORE: {self.score}', False, (255, 255, 255))

    def power_pellet_eaten(self):
        self.number_of_powerups -= 1
        self.score += self.power_pellet_score
        self.score_text = self.font.render(f'SCORE: {self.score}', False, (255, 255, 255))

    def _prepare_screen(self):
        self.screen.fill('black')
        self.draw_board()
        self.ghost_group.draw(self.screen)
        self.pacman_group.draw(self.screen)
        self.fruit_group.draw(self.screen)

    def _fruit_handle(self):
        self.should_despawn_fruit()
        self.fruit_spawn()

    def _entities_update(self):
        self.pacman_group.update()
        self.ghost_group.update()

    def _check_collisions(self):
        self._check_ghost_collisions()
        self._check_fruit_collisions()

    def update(self):
        if not self.run:
            pygame.quit()
            return

        self._prepare_screen()

        self.handle_powerup()

        self._fruit_handle()

        self._entities_update()

        self._check_collisions()

        self.handle_events()

        self._render()

    def rgb_array(self):
        return np.transpose(
            np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
        )

    def _render(self):
        if self._render_method == RenderType.HUMAN:
            pygame.display.flip()

    def calculate_center(self, x, y):
        return x * self.tile_width + (0.5 * self.tile_height), y * self.tile_height + (0.5 * self.tile_width)

    def draw_board(self):
        self.screen.blit(self.score_text, (45, 920))
        for i in range(len(self.board_definition)):
            for j in range(len(self.board_definition[i])):
                board_element = self.board_definition[i][j]
                if board_element == 1:
                    pygame.draw.circle(self.screen, self.circle_color, self.calculate_center(j, i),
                                       self.small_pellet_size)

                elif board_element == 2:
                    pygame.draw.circle(self.screen, self.circle_color, self.calculate_center(j, i),
                                       self.large_pellet_size)

                elif board_element == 3:
                    begin, end = self.calculate_vertical(j, i)
                    pygame.draw.line(self.screen, self.wall_color, begin, end, self.wall_width)

                elif board_element == 4:
                    begin, end = self.calculate_horizontal(j, i)
                    pygame.draw.line(self.screen, self.wall_color, begin, end, self.wall_width)

                elif board_element == 5:
                    rect, arc_begin, arc_end = self.calculate_upper_right_arc(j, i)
                    pygame.draw.arc(self.screen, self.wall_color, rect, arc_begin, arc_end, self.wall_width)

                elif board_element == 6:
                    rect, arc_begin, arc_end = self.calculate_upper_left_arc(j, i)
                    pygame.draw.arc(self.screen, self.wall_color, rect, arc_begin, arc_end, self.wall_width)

                elif board_element == 7:
                    rect, arc_begin, arc_end = self.calculate_bottom_left_arc(j, i)
                    pygame.draw.arc(self.screen, self.wall_color, rect, arc_begin, arc_end, self.wall_width)

                elif board_element == 8:
                    rect, arc_begin, arc_end = self.calculate_bottom_right_arc(j, i)
                    pygame.draw.arc(self.screen, self.wall_color, rect, arc_begin, arc_end, self.wall_width)

                elif board_element == 9:
                    begin, end = self.calculate_horizontal(j, i)
                    pygame.draw.line(self.screen, self.ghost_wall_color, begin, end)

        for i in range(self.pacman_lives):
            offset = i * 45
            self.screen.blit(pygame.transform.scale(self.pacman.original_image, (30, 30)), (700 + offset, 915))

        if self.debug and GRID:
            for x in range(0, self.WIDTH, self.tile_width):
                for y in range(0, self.HEIGHT, self.tile_height):
                    rect = pygame.Rect(x, y, self.tile_width, self.tile_height)
                    pygame.draw.rect(self.screen, 'white', rect, 1)

    def calculate_vertical(self, x, y):
        x_repositioned = x * self.tile_width + self.tile_width * 0.5
        y_repositioned = y * self.tile_height
        return [x_repositioned, y_repositioned], [x_repositioned, y_repositioned + self.tile_height]

    def calculate_horizontal(self, x, y):
        x_repositioned = x * self.tile_width
        y_repositioned = y * self.tile_height + self.tile_height * 0.5
        return [x_repositioned, y_repositioned], [x_repositioned + self.tile_width, y_repositioned]

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
            elif self.external_input_request is not None and self.external_inputs:
                self.handle_external_input()

    def handle_player_input(self, event):
        direction = Pacman.Direction.Direction.RIGHT
        if event.key == pygame.K_LEFT:
            direction = Pacman.Direction.Direction.LEFT
        elif event.key == pygame.K_RIGHT:
            direction = Pacman.Direction.Direction.RIGHT
        elif event.key == pygame.K_UP:
            direction = Pacman.Direction.Direction.UP
        elif event.key == pygame.K_DOWN:
            direction = Pacman.Direction.Direction.DOWN
        elif event.key == pygame.K_SPACE:
            self.pause = not self.pause
        self.pacman.change_facing_direction(direction)

    def get_screen(self):
        return self.screen

    def get_tile_width(self):
        return self.tile_width

    def get_tile_height(self):
        return self.tile_height

    def powerup(self):
        self.power_pellet_eaten()
        self.ghost_eat_index = 0
        self.blinky.trigger_frightened()
        self.inky.trigger_frightened()
        self.clyde.trigger_frightened()
        self.pinky.trigger_frightened()
        self.powerup_timer = pygame.time.get_ticks()

    def handle_powerup(self):
        if self.powerup_timer is not None:
            end = pygame.time.get_ticks()
            if end - self.powerup_timer >= self.power_pellet_time:
                self.inky.trigger_standard()
                self.blinky.trigger_standard()
                self.clyde.trigger_standard()
                self.pinky.trigger_standard()
                self.powerup_timer = None
                self.ghost_eat_index = 0

    def full_reset(self):
        self.pacman_lives = 3

        self.reset_objects()

        self.pause = False
        self.powerup_timer = None

        self.number_of_small_pellets = 240
        self.number_of_powerups = 4

        self.fruit_spawned = False
        self.spawned_fruit_index = 0
        self.fruit_spawned_begin = None
        self.fruit_spawned_timeout = 10 * 1000

        self.fruit_random_spawn_timer = 0
        self.fruit_spawn_timer = 0

        self.score_text = self.font.render('SCORE: 0', False, (255, 255, 255))
        self.score = 0
        self.board_definition = copy.deepcopy(board.board_definition)

    def external_input(self, direction):
        self.external_input_request = direction

    def handle_external_input(self):
        if self.external_input_request is not None:
            self.pacman.change_facing_direction(self.external_input_request)
            self.external_input_request = None

    def _check_ghost_collisions(self):
        ghost = pygame.sprite.spritecollideany(self.pacman, self.ghost_group)
        if ghost:
            if ghost.state == Ghosts.State.State.FRIGHTENED:
                self.ghost_eaten()
                ghost.trigger_dead()

            elif not ghost.state == Ghosts.State.State.EATEN:
                self.pacman_dead()

    def _check_fruit_collisions(self):
        fruit = pygame.sprite.spritecollideany(self.pacman, self.fruit_group)
        if fruit:
            self.eat_fruit(fruit)


def calculate_euclidian_tile_dist(x, y):
    return round(math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2), 2)


if __name__ == '__main__':
    game = PacmanGame(fps=999999)
    while game.run:
        game.update()
