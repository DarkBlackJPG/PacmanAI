import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, context, speed=100):
        super().__init__()
        self.context = context
        self.original_speed = speed
        self.speed = self.original_speed
        self.screen = self.context.screen
        self.tile_width = 0
        self.tile_height = 0
        self.rect: pygame.Rect = None

    def update_speed(self, dt):
        self.speed = self.original_speed * dt

    def get_entity_current_tile(self, error_x=0, error_y=0):
        center_x, center_y = self.rect.center
        if self.context.debug:
            pygame.draw.circle(self.screen, 'cyan', ((center_x + error_x), (error_y + center_y)), 3)
        return (center_x + error_x) // self.tile_width, (error_y + center_y) // self.tile_height

