import pygame
import OriginalGame.entity as entity


class Fruit(entity.Entity.Entity):
    def __init__(self, context):
        super().__init__(context, 0)
        self.image_size = 35
        self.screen = self.context.get_screen()
        self.tile_width = self.context.get_tile_width()
        self.tile_height = self.context.get_tile_height()
        pass

    def get_points(self):
        pass


class Cherry(Fruit):
    def __init__(self, context):
        super().__init__(context)
        self.points = 100
        self.image = pygame.transform.scale(pygame.image.load(f'resources/cherry.png'),
                                            (self.image_size, self.image_size))
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (-100, -100)
        pass

    def get_points(self):
        return self.points


class Strawberry(Fruit):
    def __init__(self, context):
        super().__init__(context)
        self.points = 300
        self.image = pygame.transform.scale(pygame.image.load(f'resources/strawberry.png'),
                                            (self.image_size, self.image_size))
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (-100, -100)
        pass

    def get_points(self):
        return self.points


class Apple(Fruit):
    def __init__(self, context):
        super().__init__(context)
        self.points = 700
        self.image = pygame.transform.scale(pygame.image.load(f'resources/apple.png'),
                                            (self.image_size, self.image_size))
        self.rect = self.image.get_bounding_rect()
        self.rect.center = (-100, -100)
        pass

    def get_points(self):
        return self.points
