import Fruit
import pygame
import os

lib_path = os.path.dirname(__file__)


class Strawberry(Fruit):
    def __init__(self, context):
        super().__init__(context)
        self.points = 300
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.abspath(os.path.join(lib_path, '../resources/strawberry.png'))),
            (self.image_size, self.image_size))
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (-100, -100)
        pass

    def get_points(self):
        return self.points
