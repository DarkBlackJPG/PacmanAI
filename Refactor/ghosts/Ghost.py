import os
import pygame
import math
import random
import time

from Refactor.enums import GhostStates
from Refactor.enums import EntityDirection
import Refactor.entity as entity

lib_path = os.path.dirname(__file__)


def calculate_euclidian_tile_dist(x, y):
    return round(math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2), 2)


class Ghost(entity.Entity.Entity):
    __DIRECTIONS = {(0, -1): 0, (-1, 0): 1, (0, 1): 2, (1, 0): 3}

    def __init__(self, context, speed=1):
        super().__init__(context, speed)
        self.image = None
        self.game_begun = False
        self.image_size = super().get_game_context().tile_width
        self.frightened_image_path = os.path.abspath(os.path.join(lib_path, '../resources/vulnerable.png'))
        self.dead_image_path = os.path.abspath(os.path.join(lib_path, '../resources/dead.png'))
        self.frightened_image = pygame.transform.scale(pygame.image.load(self.frightened_image_path),
                                                       (self.image_size, self.image_size))
        self.dead_image = pygame.transform.scale(pygame.image.load(self.dead_image_path),
                                                 (self.image_size, self.image_size))
        self.board_definition = super().get_game_context().board_definition
        self.screen = super().get_game_context().get_screen()
        self.speed = speed
        self.tile_width = super().get_game_context().tile_width
        self.tile_height = super().get_game_context().tile_height
        #
        self.LEFT = 0
        self.RIGHT = 1
        self.UP = 2
        self.DOWN = 3
        self.direction_priorities = [self.UP, self.LEFT, self.DOWN, self.RIGHT]
        self.direction = self.RIGHT
        self.directions = [False, False, False, False]
        #
        self.rect = None
        self.state = GhostStates.IN_HOUSE
        #
        self.target = (0, 0)
        self.target_color = (255, 255, 255)
        #
        self.previous_tile = (0, 0)
        self.next_tile = (0, 0)
        self.target = (15, 11)
        #
        self.state_index = 0
        self.state_times = [0,  # Potencijalno je ovo na nivou game-a
                            7000,
                            20000,
                            7000,
                            20000,
                            5000,
                            20000,
                            5000,
                            0]
        #
        self.begin_state_time = pygame.time.get_ticks()  # in_house is the first state

    def calculate_center_for_tile(self, x, y):
        return int(x * self.tile_width + self.tile_width / 2), int(y * self.tile_height + self.tile_height / 2)

    def check_center_is_in_tile(self, tile_x, tile_y):
        return self.rect.centerx == tile_x * self.tile_width + self.tile_width / 2 and \
            self.rect.centery == tile_y * self.tile_height + self.tile_height / 2

    def trigger_frightened(self):
        self.state = GhostStates.FRIGHTENED
        self.image = self.frightened_image
        pass

    def trigger_dead(self):
        self.state = GhostStates.EATEN
        self.image = self.dead_image
        pass

    def trigger_standard(self):
        # If killed, we want him to go to the house
        if self.state == GhostStates.EATEN:
            return
        # TODO kako ovo?
        if self.state_index % 2:
            self.state = GhostStates.CHASE
        else:
            self.state = GhostStates.SCATTER

        self.image = self.standard_image
        pass

    def wiggle_factor(self, modulo, factor):
        return factor * 0.38 <= modulo <= factor * 0.62

    def update_directions(self):
        tile_x, tile_y = self.get_entity_current_tile()
        self.directions = [False, False, False, False]
        if tile_x + 1 > 29 or tile_x < 0:
            self.directions = [True, True, False, False]
            return

        if (self.board_definition[tile_y - 1][tile_x] < 3 or self.board_definition[tile_y - 1][
            tile_x] == 9) and 12 <= self.rect.centerx % self.tile_width <= 18:
            self.directions[self.UP] = True
        if (self.board_definition[tile_y + 1][tile_x] < 3) \
                and 12 <= self.rect.centerx % self.tile_width <= 18 \
                or (self.board_definition[tile_y + 1][tile_x] == 9 and self.state == GhostStates.EATEN):
            self.directions[self.DOWN] = True
        if (self.board_definition[tile_y][tile_x - 1] < 3 or self.board_definition[tile_y - 1][
            tile_x] == 9) and 12 <= self.rect.centery % self.tile_height <= 18:
            self.directions[self.LEFT] = True
        if (self.board_definition[tile_y][tile_x + 1] < 3 or self.board_definition[tile_y - 1][
            tile_x] == 9) and 12 <= self.rect.centery % self.tile_height <= 18:
            self.directions[self.RIGHT] = True

    def update(self):
        self.update_directions()
        self.draw_directions()
        self.draw_target(self.target_color)
        self.draw_line_to_target(self.target_color)

        if self.state == GhostStates.IN_HOUSE:
            self.in_house()
        elif self.state == GhostStates.SCATTER:
            self.scatter_master()
        elif self.state == GhostStates.CHASE:
            self.chase_master()
        elif self.state == GhostStates.FRIGHTENED:
            self.frightened()
        elif self.state == GhostStates.EATEN:
            self.eaten()

        if not super().get_game_context().is_game_paused():
            self.move()

    def in_house(self):
        if self.state == GhostStates.IN_HOUSE:
            self.get_next_tile()
            tile_x, tile_y = self.get_entity_current_tile()
            if tile_y < 13 and not self.game_begun:
                self.state = GhostStates.SCATTER
                self.state_index += 1
                self.game_begun = True
                self.begin_state_time = pygame.time.get_ticks()
            elif tile_y < 13 and self.game_begun:
                if self.state_index % 2:
                    self.state = GhostStates.CHASE
                else:
                    self.state = GhostStates.SCATTER
        pass

    def scatter_master(self):
        if self.state == GhostStates.SCATTER:
            self.get_next_tile()
            self.scatter()
            if self.state_times[self.state_index] != 0 and pygame.time.get_ticks() - self.begin_state_time >= \
                    self.state_times[self.state_index]:
                self.turn_180_deg()
                self.state_index += 1
                self.state = GhostStates.CHASE
                self.begin_state_time = pygame.time.get_ticks()
        pass

    def scatter(self):
        pass

    def turn_180_deg(self):
        tile_x, tile_y = self.get_entity_current_tile()
        if self.direction == EntityDirection.RIGHT and self.directions[self.LEFT]:
            self.direction = self.LEFT
            self.next_tile = (tile_x - 1, tile_y)
        elif self.direction == EntityDirection.LEFT and self.directions[self.RIGHT]:
            self.direction = self.RIGHT
            self.next_tile = (tile_x + 1, tile_y)
        elif self.direction == EntityDirection.UP and self.directions[self.DOWN]:
            self.direction = EntityDirection.DOWN
            self.next_tile = (tile_x, tile_y + 1)
        elif self.direction == EntityDirection.DOWN and self.directions[self.UP]:
            self.direction = EntityDirection.UP
            self.next_tile = (tile_x, tile_y - 1)
        self.previous_tile = (0, 0)
        self.update_directions()

    def chase_master(self):
        if self.state == GhostStates.CHASE:
            self.get_next_tile()
            self.chase()
            if self.state_times[self.state_index] != 0 and pygame.time.get_ticks() - self.begin_state_time >= \
                    self.state_times[self.state_index]:
                self.turn_180_deg()
                self.state_index += 1
                self.state = GhostStates.SCATTER
                self.begin_state_time = pygame.time.get_ticks()
        pass

    def chase(self):
        pass

    def frightened(self):
        if self.state == GhostStates.FRIGHTENED:
            self.get_next_random_tile()
        pass

    def eaten(self):
        if self.state == GhostStates.EATEN:
            tile_x, tile_y = self.get_entity_current_tile()
            if tile_x == 15 and tile_y == 14:
                self.state = GhostStates.IN_HOUSE
                self.image = self.standard_image
                self.target = (0, 0)
                return
            self.target = (15, 14)
            self.get_next_tile()
        pass

    def draw_directions(self):
        if super().get_game_context().debug_show_debug_data():
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
        if super().get_game_context().debug_show_debug_data():
            pygame.draw.circle(self.screen, color,
                               (self.target[0] * self.tile_width, self.target[1] * self.tile_height), 5)

    def draw_line_to_target(self, color):
        if super().get_game_context().debug_show_debug_data():
            pygame.draw.line(self.screen, color, self.rect.center,
                             (self.target[0] * self.tile_width, self.target[1] * self.tile_height), 2)

    def get_next_tile(self):
        # if at the target tile
        if self.calculate_center_for_tile(self.next_tile[0], self.next_tile[1]) == (
                self.rect.centerx, self.rect.centery):
            tile_x, tile_y = self.get_entity_current_tile()
            best_distance = 1000
            best_direction = (0, 0)
            if self.directions[self.UP]:
                temp_dist = calculate_euclidian_tile_dist((tile_x, tile_y - 1), self.target)
                if temp_dist < best_distance and self.previous_tile != (tile_x, tile_y - 1):
                    best_distance = temp_dist
                    best_direction = (0, -1)

            if self.directions[self.LEFT]:
                temp_dist = calculate_euclidian_tile_dist((tile_x - 1, tile_y), self.target)
                if temp_dist < best_distance and self.previous_tile != (tile_x - 1, tile_y):
                    best_distance = temp_dist
                    best_direction = (-1, 0)

            if self.directions[self.DOWN]:
                temp_dist = calculate_euclidian_tile_dist((tile_x, tile_y + 1), self.target)
                if temp_dist < best_distance and self.previous_tile != (tile_x, tile_y + 1):
                    best_distance = temp_dist
                    best_direction = (0, 1)

            if self.directions[self.RIGHT]:
                temp_dist = calculate_euclidian_tile_dist((tile_x + 1, tile_y), self.target)
                if temp_dist < best_distance and self.previous_tile != (tile_x + 1, tile_y):
                    best_direction = (1, 0)

            self.previous_tile = self.next_tile
            self.next_tile = (best_direction[0] + self.next_tile[0], best_direction[1] + self.next_tile[1])

    def can_go_through_portal(self):
        if self.rect.left > super().get_game_context().get_screen_width():
            self.rect.left = -super().get_game_context().get_tile_width()
            self.next_tile = (1, 15)
            return True
        elif self.rect.left < -super().get_game_context().get_tile_width():
            self.rect.left = super().get_game_context().get_screen_width() - super().get_game_context().get_tile_width()
            self.next_tile = (29, 15)
            return True
        return False

    def move(self):
        loc_x, loc_y = self.calculate_center_for_tile(self.next_tile[0], self.next_tile[1])
        entity_x, entity_y = self.rect.center

        if self.can_go_through_portal():
            return

        if entity_x == loc_x and entity_y == loc_y:  # need to update next_tile
            return

        # Diagonal traversal not possible, next_tile is always one step away
        if entity_x < loc_x:
            self.rect.centerx += self.speed

        if entity_x > loc_x:
            self.rect.centerx -= self.speed

        if entity_y > loc_y:
            self.rect.centery -= self.speed

        if entity_y < loc_y:
            self.rect.centery += self.speed

    def get_next_random_tile(self):
        # if at the target tile
        if self.calculate_center_for_tile(self.next_tile[0], self.next_tile[1]) == (
                self.rect.centerx, self.rect.centery):
            rand = random.Random()
            rand.seed(time.time())
            tile_x, tile_y = self.get_entity_current_tile()

            # create a list of directions in random order
            directions = [self.UP, self.LEFT, self.DOWN, self.RIGHT]
            rand.shuffle(directions)
            best_direction = None
            # iterate over all directions until a valid tile is found
            for direction in directions:
                if direction == self.UP and self.directions[self.UP]:
                    if self.previous_tile != (tile_x, tile_y - 1):
                        best_direction = (0, -1)
                        break
                elif direction == self.LEFT and self.directions[self.LEFT]:
                    if self.previous_tile != (tile_x - 1, tile_y):
                        best_direction = (-1, 0)
                        break
                elif direction == self.DOWN and self.directions[self.DOWN]:
                    if self.previous_tile != (tile_x, tile_y + 1):
                        best_direction = (0, 1)
                        break
                elif direction == self.RIGHT and self.directions[self.RIGHT]:
                    if self.previous_tile != (tile_x + 1, tile_y):
                        best_direction = (1, 0)
                        break

            self.previous_tile = self.next_tile
            if best_direction is None:
                raise Exception("No valid direction found")
            self.next_tile = (best_direction[0] + self.next_tile[0], best_direction[1] + self.next_tile[1])
