import OriginalGame.PacmanGame as PacmanGame
import OriginalGame.pacman.Pacman as Pacman
from enum import Enum
import pygame
import numpy as np
import copy


class PacmanGameGym(PacmanGame.PacmanGame):
    directions_API = [
        Pacman.Direction.Direction.LEFT,
        Pacman.Direction.Direction.UP,
        Pacman.Direction.Direction.RIGHT,
        Pacman.Direction.Direction.DOWN,
        None,
    ]

    def __init__(self, external_inputs=False, fps=60, render_type: PacmanGame.RenderType = PacmanGame.RenderType.HUMAN):
        super().__init__(external_inputs=external_inputs, render_method=render_type)
        self.fps = fps
        self.__dead_reward = -200
        self.__pacman_eaten_reward = -100
        self.done = False
        self.pacman_lives = 1
        self.reward = 0
        self.wall_width = 7
        self.small_pellet_size = 6
        self.large_pellet_size = 14

    def ghost_eaten(self):
        super().ghost_eaten()
        self.reward = self.ghost_eat_scores[self.ghost_eat_index - 1]  # In superclass index is + 1

    def eat_fruit(self, fruit):
        super().eat_fruit(fruit)
        self.reward = fruit.get_points()

    def small_pellet_eaten(self):
        super().small_pellet_eaten()
        self.reward = self.small_pellet_score

    def power_pellet_eaten(self):
        super().power_pellet_eaten()
        self.reward = self.power_pellet_score

    def pacman_dead(self):
        if self.pacman_lives == 0:
            self.done = True

        # Soft Reset
        del self.pacman
        del self.inky
        del self.pinky
        del self.clyde
        del self.blinky
        self.pacman_lives -= 1

        self.reward = self.__pacman_eaten_reward if self.pacman_lives > 0 else self.__dead_reward

        if self.pacman_lives == 0:
            self.done = True
            self.full_reset()
            return

        self.reset_objects()

    def get_reward(self):
        return self.reward

    def reset_state(self):
        self.reward = 0

    def full_reset(self):
        super().full_reset()
        self.done = False

    def get_board_rgb_array(self):
        return self.rgb_array()
