import pygame
import OriginalGame.PacmanGame as PacmanGame
import OriginalGame.entity as entity
import OriginalGame.enums.State as State
import OriginalGame.enums.Direction as Direction
import random
import time
import math


class Ghost(entity.Entity.Entity):
    def calculate_center_for_tile(self, x, y):
        return int(x * self.tile_width + self.tile_width / 2), int(y * self.tile_height + self.tile_height / 2)

    def check_center_is_in_tile(self, tile_x, tile_y):
        return self.rect.centerx == tile_x * self.tile_width + self.tile_width / 2 and \
            self.rect.centery == tile_y * self.tile_height + self.tile_height / 2

    def trigger_frightened(self):
        self.state = State.State.FRIGHTENED
        self.image = self.frightened_image
        pass

    def trigger_dead(self):
        self.state = State.State.EATEN
        self.image = self.dead_image
        pass

    def trigger_standard(self):
        # If killed, we want him to go to the house
        if self.state == State.State.EATEN:
            return
        # TODO kako ovo?
        if self.state_index % 2:
            self.state = State.State.CHASE
        else:
            self.state = State.State.SCATTER

        self.image = self.standard_image
        pass

    def __init__(self, context, speed):
        super().__init__(context, speed)
        self.game_begun = False
        self.image_size = 35
        self.frightened_image_path = f'resources/vulnerable.png'
        self.standard_image = None
        self.dead_image_path = f'resources/dead.png'
        self.frightened_image = pygame.transform.scale(pygame.image.load(self.frightened_image_path),
                                                       (self.image_size, self.image_size))
        self.dead_image = pygame.transform.scale(pygame.image.load(self.dead_image_path),
                                                 (self.image_size, self.image_size))
        self.context = context
        self.board_definition = self.context.board_definition
        self.screen = self.context.screen
        self.speed = speed
        self.tile_width = self.context.tile_width
        self.tile_height = self.context.tile_height
        #
        self.LEFT = 0
        self.RIGHT = 1
        self.UP = 2
        self.DOWN = 3
        self.direction_priorities = [self.UP, self.LEFT, self.DOWN, self.RIGHT]
        self.direction = self.RIGHT
        self.directions = [False, False, False, False]
        #
        self.rect: pygame.Rect = None
        self.state = State.State.IN_HOUSE
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
                or (self.board_definition[tile_y + 1][tile_x] == 9 and self.state == State.State.EATEN):
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

        if self.state == State.State.IN_HOUSE:
            self.in_house()
        elif self.state == State.State.SCATTER:
            self.scatter_master()
        elif self.state == State.State.CHASE:
            self.chase_master()
        elif self.state == State.State.FRIGHTENED:
            self.frightened()
        elif self.state == State.State.EATEN:
            self.eaten()

        if not self.context.pause:
            self.move()

    def in_house(self):
        if self.state == State.State.IN_HOUSE:
            self.get_next_tile()
            tile_x, tile_y = self.get_entity_current_tile()
            if tile_y < 13 and not self.game_begun:
                self.state = State.State.SCATTER
                self.state_index += 1
                self.game_begun = True
                self.begin_state_time = pygame.time.get_ticks()
            elif tile_y < 13 and self.game_begun:
                if self.state_index % 2:
                    self.state = State.State.CHASE
                else:
                    self.state = State.State.SCATTER
        pass

    def scatter_master(self):
        if self.state == State.State.SCATTER:
            self.get_next_tile()
            self.scatter()
            if self.state_times[self.state_index] != 0 and pygame.time.get_ticks() - self.begin_state_time >= \
                    self.state_times[self.state_index]:
                self.turn_180_deg()
                self.state_index += 1
                self.state = State.State.CHASE
                self.begin_state_time = pygame.time.get_ticks()
        pass

    def scatter(self):
        pass

    def turn_180_deg(self):
        tile_x, tile_y = self.get_entity_current_tile()
        if self.direction == Direction.Direction.RIGHT and self.directions[self.LEFT]:
            self.direction = self.LEFT
            self.next_tile = (tile_x - 1, tile_y)
        elif self.direction == Direction.Direction.LEFT and self.directions[self.RIGHT]:
            self.direction = self.RIGHT
            self.next_tile = (tile_x + 1, tile_y)
        elif self.direction == Direction.Direction.UP and self.directions[self.DOWN]:
            self.direction = Direction.Direction.DOWN
            self.next_tile = (tile_x, tile_y + 1)
        elif self.direction == Direction.Direction.DOWN and self.directions[self.UP]:
            self.direction = Direction.Direction.UP
            self.next_tile = (tile_x, tile_y - 1)
        self.previous_tile = (0, 0)
        self.update_directions()

    def chase_master(self):
        if self.state == State.State.CHASE:
            self.get_next_tile()
            self.chase()
            if self.state_times[self.state_index] != 0 and pygame.time.get_ticks() - self.begin_state_time >= \
                    self.state_times[self.state_index]:
                self.turn_180_deg()
                self.state_index += 1
                self.state = State.State.SCATTER
                self.begin_state_time = pygame.time.get_ticks()
        pass

    def chase(self):
        pass

    def frightened(self):
        if self.state == State.State.FRIGHTENED:
            self.get_next_random_tile()
        pass

    def eaten(self):
        if self.state == State.State.EATEN:
            tile_x, tile_y = self.get_entity_current_tile()
            if tile_x == 15 and tile_y == 14:
                self.state = State.State.IN_HOUSE
                self.image = self.standard_image
                self.target = (0, 0)
                return
            self.target = (15, 14)
            self.get_next_tile()
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

    def get_next_tile(self):
        # if at the target tile
        if self.calculate_center_for_tile(self.next_tile[0], self.next_tile[1]) == (
                self.rect.centerx, self.rect.centery):
            tile_x, tile_y = self.get_entity_current_tile()
            best_distance = 1000
            best_direction = (0, 0)
            if self.directions[self.UP]:
                temp_dist = PacmanGame.calculate_euclidian_tile_dist((tile_x, tile_y - 1), self.target)
                if temp_dist < best_distance and self.previous_tile != (tile_x, tile_y - 1):
                    best_distance = temp_dist
                    best_direction = (0, -1)

            if self.directions[self.LEFT]:
                temp_dist = PacmanGame.calculate_euclidian_tile_dist((tile_x - 1, tile_y), self.target)
                if temp_dist < best_distance and self.previous_tile != (tile_x - 1, tile_y):
                    best_distance = temp_dist
                    best_direction = (-1, 0)

            if self.directions[self.DOWN]:
                temp_dist = PacmanGame.calculate_euclidian_tile_dist((tile_x, tile_y + 1), self.target)
                if temp_dist < best_distance and self.previous_tile != (tile_x, tile_y + 1):
                    best_distance = temp_dist
                    best_direction = (0, 1)

            if self.directions[self.RIGHT]:
                temp_dist = PacmanGame.calculate_euclidian_tile_dist((tile_x + 1, tile_y), self.target)
                if temp_dist < best_distance and self.previous_tile != (tile_x + 1, tile_y):
                    best_direction = (1, 0)

            self.previous_tile = self.next_tile
            self.next_tile = (best_direction[0] + self.next_tile[0], best_direction[1] + self.next_tile[1])

    def move(self):
        loc_x, loc_y = self.calculate_center_for_tile(self.next_tile[0], self.next_tile[1])
        entity_x, entity_y = self.rect.center
        if self.rect.left > 900:
            self.rect.left = -40
            self.next_tile = (1, 15)
            return
        elif self.rect.left < -50:
            self.rect.left = 890
            self.next_tile = (29, 15)
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
            # TODO Nije efikasno u picku materinu ahahaha
            # TODO Sta kad udju u portaL?
            while True:
                dir = int(rand.randrange(0, 4, 1))

                if dir == self.UP and self.directions[self.UP]:
                    if self.previous_tile != (tile_x, tile_y - 1):
                        best_direction = (0, -1)
                        break

                if dir == self.LEFT and self.directions[self.LEFT]:
                    if self.previous_tile != (tile_x - 1, tile_y):
                        best_direction = (-1, 0)
                        break

                if dir == self.DOWN and self.directions[self.DOWN]:
                    if self.previous_tile != (tile_x, tile_y + 1):
                        best_direction = (0, 1)
                        break

                if dir == self.RIGHT and self.directions[self.RIGHT]:
                    if self.previous_tile != (tile_x + 1, tile_y):
                        best_direction = (1, 0)
                        break

            self.previous_tile = self.next_tile
            self.next_tile = (best_direction[0] + self.next_tile[0], best_direction[1] + self.next_tile[1])
        pass


class Pinky(Ghost):
    def __init__(self, context, speed=2):
        super().__init__(context, speed)
        self.image_path = f'resources/pinky.png'
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
        self.image_path = f'resources/inky.png'
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
        self.image_path = f'resources/clyde.png'
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
        self.image_path = f'resources/blinky.png'
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
