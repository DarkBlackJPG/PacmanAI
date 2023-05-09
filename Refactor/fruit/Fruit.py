import pygame
import Refactor.entity as entity
import os

lib_path = os.path.dirname(__file__)


class Fruit(entity.Entity.Entity):
    def __init__(self, context):
        super().__init__(context, 0)
        self.image_size = 35
        self.screen = super().get_game_context().get_screen()
        self.tile_width = super().get_game_context().get_tile_width()
        self.tile_height = super().get_game_context().get_tile_height()
        pass

    def get_points(self):
        raise NotImplementedError("Subclass must implement abstract method")