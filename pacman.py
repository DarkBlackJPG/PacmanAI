import math

import pygame
from board import board_definition


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

    def update(self):
        if not self.run:
            pygame.quit()
            return

        self.timer.tick()
        self.screen.fill('black')
        self.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
        pygame.display.flip()

    def calculate_center(self, x, y):
        return x * self.tile_width + (0.5 * self.tile_height), y * self.tile_height + (0.5 * self.tile_width)

    def draw(self):
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


if __name__ == '__main__':
    game = PacmanGame()
    while game.run:
        game.update()
