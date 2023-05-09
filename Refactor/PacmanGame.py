import math
import random
import time
import copy
import pygame
import os
import numpy as np

import Refactor.enums as Enums

from pygame.event import Event

from Refactor.board import board
from Refactor.pacman import Pacman
from Refactor.ghosts import Pinky
from Refactor.ghosts import Blinky
from Refactor.ghosts import Clyde
from Refactor.ghosts import Inky

DEBUG_PARAMETERS = {
    "show_debug_data": True,
    "show_game_grid": False
}

LIB_PATH = os.path.dirname(__file__)


class PacmanGame:
    _pellet_color = 'beige'
    _number_of_rows = 32
    _number_of_columns = 30
    _number_of_small_pellets = 240
    _number_of_powerups = 4
    _small_pellet_score = 10
    _powerup_score = 50
    _ghost_eat_score = [200, 400, 800, 1600]
    _wall_color = (65, 107, 186)
    _circle_color = 'beige'
    _ghost_wall_color = 'white'
    _fruit_spawn_points = [
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

    __pygame_direction_map = {
        pygame.K_LEFT: Enums.EntityDirection.LEFT,
        pygame.K_RIGHT: Enums.EntityDirection.RIGHT,
        pygame.K_UP: Enums.EntityDirection.UP,
        pygame.K_DOWN: Enums.EntityDirection.DOWN,
    }
    __draw_functions = {
        1: pygame.draw.circle,
        2: pygame.draw.circle,
        3: pygame.draw.line,
        4: pygame.draw.line,
        5: pygame.draw.arc,
        6: pygame.draw.arc,
        7: pygame.draw.arc,
        8: pygame.draw.arc,
        9: pygame.draw.line,
    }

    def __init__(self,
                 render_method: Enums.RenderType = Enums.RenderType.HUMAN,
                 input_type: Enums.InputType = Enums.InputType.HUMAN,
                 fps=60,
                 screen_width=900,
                 screen_height=900,
                 screen_footer_height=50,
                 skip_timers=False):
        self.__pacman_speed = 1
        self._score = 0
        self.__external_input_request = None
        self.__render_method = render_method
        self.__input_type = input_type
        self.__fps = fps
        self._footer_height = screen_footer_height
        self._skip_timers = skip_timers
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height + screen_footer_height
        self.__number_of_pellets = self._number_of_small_pellets
        self.__number_of_powerups = self._number_of_powerups

        self.tile_height = screen_height // PacmanGame._number_of_rows
        self.tile_width = screen_width // PacmanGame._number_of_columns

        self.small_pellet_size = int(self.tile_width * 0.1)
        self.large_pellet_size = int(self.tile_width * 0.25)
        self.wall_width = int(self.tile_width * 0.15)

        self.board_definition = copy.deepcopy(board.board_definition)
        self.center_cache = {(j, i): self.calculate_center(j, i) for i in range(len(self.board_definition)) for j in
                             range(len(self.board_definition[i]))}
        self.vertical_cache = {(j, i): self.calculate_vertical(j, i) for i in range(len(self.board_definition)) for j in
                               range(len(self.board_definition[i])) if self.board_definition[i][j] == 3}
        self.horizontal_cache = {(j, i): self.calculate_horizontal(j, i) for i in range(len(self.board_definition)) for
                                 j in range(len(self.board_definition[i])) if
                                 self.board_definition[i][j] == 4 or self.board_definition[i][j] == 9}
        self.upper_right_arc_cache = {(j, i): self.calculate_upper_right_arc(j, i) for i in
                                      range(len(self.board_definition)) for j in range(len(self.board_definition[i])) if
                                      self.board_definition[i][j] == 5}
        self.upper_left_arc_cache = {(j, i): self.calculate_upper_left_arc(j, i) for i in
                                     range(len(self.board_definition)) for j in range(len(self.board_definition[i])) if
                                     self.board_definition[i][j] == 6}
        self.bottom_left_arc_cache = {(j, i): self.calculate_bottom_left_arc(j, i) for i in
                                      range(len(self.board_definition)) for j in range(len(self.board_definition[i])) if
                                      self.board_definition[i][j] == 7}
        self.bottom_right_arc_cache = {(j, i): self.calculate_bottom_right_arc(j, i) for i in
                                       range(len(self.board_definition)) for j in range(len(self.board_definition[i]))
                                       if self.board_definition[i][j] == 8}

        self.__run_game = False
        self.__pause = False
        self.__powerup_timer = None

        self.__pacman_group = pygame.sprite.Group()
        self.__ghost_group = pygame.sprite.Group()
        self.__fruit_group = pygame.sprite.Group()

        pygame.init()
        pygame.font.init()
        self._font = pygame.font.Font(os.path.abspath(os.path.join(LIB_PATH, 'resources/joystix.otf')), 20)
        self._screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])

        self.pacman = Pacman(self, speed=self.__pacman_speed)
        self.pinky = Pinky(self)
        self.blinky = Blinky(self)
        self.inky = Inky(self)
        self.clyde = Clyde(self)
        self.__pacman_group.add(self.pacman)
        self.__ghost_group.add(self.pinky)
        self.__ghost_group.add(self.blinky)
        self.__ghost_group.add(self.clyde)
        self.__ghost_group.add(self.inky)

    def get_screen(self):
        return self._screen

    def get_screen_width(self):
        return self.SCREEN_WIDTH

    def get_screen_height(self):
        return self.SCREEN_HEIGHT

    def get_number_of_small_pellets(self):
        return self._number_of_small_pellets

    def get_number_of_powerups(self):
        return self._number_of_powerups

    def get_tile_width_and_height(self):
        return self.tile_width, self.tile_height

    def get_tile_width(self):
        return self.tile_width

    def get_tile_height(self):
        return self.tile_height

    def update(self):
        if self.__run_game:
            pygame.quit()
            return

        self.__draw_walls()
        self.__handle_events()
        self.__update_entities()
        self.__draw_entities()

        return self.__render()

    def is_game_paused(self):
        return self.__pause

    def __render(self):
        if self.__render_method == Enums.RenderType.HUMAN:
            pygame.display.flip()
            return None
        elif self.__render_method == Enums.RenderType.RGB_ARRAY:
            return np.transpose(np.array(pygame.surfarray.pixels3d(self._screen)), axes=(1, 0, 2))

    def __handle_events(self):
        event_handlers = {
            pygame.QUIT: self.__handle_quit_event,
            pygame.KEYDOWN: self.__handle_key_down_event,
        }
        events = pygame.event.get()
        for event in events:
            event_type = event.type
            if event_type in event_handlers:
                event_handlers[event_type](event)
            elif self.__input_type == Enums.InputType.MACHINE:
                self.handle_external_input()

    def handle_external_input(self):
        if self.__external_input_request is not None:
            # self.pacman.change_facing_direction(self.external_input_request)
            self.external_input_request = None

    def __handle_quit_event(self, event: Event):
        self.__run_game = False

    def small_pellet_eaten(self):
        self.__number_of_pellets -= 1
        self._score += self._small_pellet_score

    def power_pellet_eaten(self):
        self.__number_of_powerups -= 1
        self._score += self._powerup_score
    def powerup(self):
        self.power_pellet_eaten()
        # self.ghost_eat_index = 0
        # self.blinky.trigger_frightened()
        # self.inky.trigger_frightened()
        # self.clyde.trigger_frightened()
        # self.pinky.trigger_frightened()
        # self.powerup_timer = pygame.time.get_ticks()
    def __handle_key_down_event(self, event: Event):
        direction = PacmanGame.__pygame_direction_map.get(event.key, Enums.EntityDirection.RIGHT)
        if event.key == pygame.K_SPACE:
            self.pause = not self.__pause
        self.pacman.change_facing_direction(direction)

    def debug_draw_gridline(self):
        return DEBUG_PARAMETERS['show_game_grid']

    def debug_show_debug_data(self):
        return DEBUG_PARAMETERS['show_debug_data']
    def __update_entities(self):
        self.__pacman_group.update()
        self.__ghost_group.update()
        self.__fruit_group.update()

    def __draw_entities(self):
        self.__pacman_group.draw(self._screen)
        self.__ghost_group.draw(self._screen)
        pass

    def __draw_walls(self):
        self._screen.fill('black')
        for i in range(len(self.board_definition)):
            for j in range(len(self.board_definition[i])):
                board_element = self.board_definition[i][j]
                if board_element in PacmanGame.__draw_functions:
                    if board_element == 1:
                        PacmanGame.__draw_functions[board_element](self._screen, PacmanGame._pellet_color,
                                                                   self.center_cache[(j, i)],
                                                                   self.small_pellet_size)
                    elif board_element == 2:
                        PacmanGame.__draw_functions[board_element](self._screen, PacmanGame._pellet_color,
                                                                   self.center_cache[(j, i)],
                                                                   self.large_pellet_size)
                    elif board_element == 3:
                        begin, end = self.vertical_cache[(j, i)]
                        PacmanGame.__draw_functions[board_element](self._screen, PacmanGame._wall_color, begin, end,
                                                                   self.wall_width)
                    elif board_element == 4:
                        begin, end = self.horizontal_cache[(j, i)]
                        PacmanGame.__draw_functions[board_element](self._screen, PacmanGame._wall_color, begin, end,
                                                                   self.wall_width)
                    elif board_element == 5:
                        rect, arc_begin, arc_end = self.upper_right_arc_cache[(j, i)]
                        PacmanGame.__draw_functions[board_element](self._screen, PacmanGame._wall_color, rect,
                                                                   arc_begin, arc_end,
                                                                   self.wall_width)
                    elif board_element == 6:
                        rect, arc_begin, arc_end = self.upper_left_arc_cache[(j, i)]
                        PacmanGame.__draw_functions[board_element](self._screen, PacmanGame._wall_color, rect,
                                                                   arc_begin, arc_end, self.wall_width)
                    elif board_element == 7:
                        rect, arc_begin, arc_end = self.bottom_left_arc_cache[(j, i)]
                        PacmanGame.__draw_functions[board_element](self._screen, PacmanGame._wall_color, rect,
                                                                   arc_begin, arc_end, self.wall_width)
                    elif board_element == 8:
                        rect, arc_begin, arc_end = self.bottom_right_arc_cache[(j, i)]
                        PacmanGame.__draw_functions[board_element](self._screen, PacmanGame._wall_color, rect,
                                                                   arc_begin, arc_end, self.wall_width)
                    elif board_element == 9:
                        begin, end = self.horizontal_cache[(j, i)]
                        PacmanGame.__draw_functions[board_element](self._screen, PacmanGame._ghost_wall_color, begin,
                                                                   end)

        if DEBUG_PARAMETERS['show_game_grid']:
            for x in range(0, self.SCREEN_WIDTH, self.tile_width):
                for y in range(0, self.SCREEN_HEIGHT, self.tile_height):
                    rect = pygame.Rect(x, y, self.tile_width, self.tile_height)
                    pygame.draw.rect(self._screen, 'white', rect, 1)

    def calculate_vertical(self, x, y):
        x_repositioned = x * self.tile_width + 0.5 * self.tile_width
        y_repositioned = y * self.tile_height
        return [x_repositioned, y_repositioned], [x_repositioned, y_repositioned + self.tile_height]

    def calculate_horizontal(self, x, y):
        x_repositioned = x * self.tile_width
        y_repositioned = y * self.tile_height + 0.5 * self.tile_height
        return [x_repositioned, y_repositioned], [x_repositioned + self.tile_width, y_repositioned]

    def calculate_upper_left_arc(self, x, y):
        x_repositioned = x * self.tile_width + 0.5 * (self.tile_width - self.wall_width) + 1
        y_repositioned = y * self.tile_height + 0.5 * (self.tile_height - self.wall_width) + 1
        rect = pygame.Rect(x_repositioned, y_repositioned, self.tile_width, self.tile_height)
        begin_angle = math.pi / 2
        end_angle = math.pi
        return rect, begin_angle, end_angle

    def calculate_bottom_left_arc(self, x, y):
        x_repositioned = x * self.tile_width + 0.5 * (self.tile_width - self.wall_width) + 1
        y_repositioned = y * self.tile_height - 0.5 * (self.tile_height - self.wall_width) + 1
        rect = pygame.Rect(x_repositioned, y_repositioned, self.tile_width, self.tile_height)
        begin_angle = math.pi
        end_angle = 3 * math.pi / 2
        return rect, begin_angle, end_angle

    def calculate_upper_right_arc(self, x, y):
        x_repositioned = x * self.tile_width - 0.5 * (self.tile_width - self.wall_width) + 1
        y_repositioned = y * self.tile_height + 0.5 * (self.tile_height - self.wall_width) + 1
        rect = pygame.Rect(x_repositioned, y_repositioned, self.tile_width, self.tile_height)
        begin_angle = 0
        end_angle = math.pi / 2
        return rect, begin_angle, end_angle

    def calculate_bottom_right_arc(self, x, y):
        x_repositioned = x * self.tile_width - 0.5 * (self.tile_width - self.wall_width) + 1
        y_repositioned = y * self.tile_height - 0.5 * (self.tile_height - self.wall_width) + 1
        rect = pygame.Rect(x_repositioned, y_repositioned, self.tile_width, self.tile_height)
        begin_angle = 3 * math.pi / 2
        end_angle = 0
        return rect, begin_angle, end_angle

    def calculate_center(self, x, y):
        return x * self.tile_width + (0.5 * self.tile_height), y * self.tile_height + (0.5 * self.tile_width)


if __name__ == '__main__':
    p = PacmanGame()
    while True:
        p.update()
