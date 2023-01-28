import pygame

class PacmanGame:
    def __init__(self):
        pygame.init()
        self.WIDTH = 900
        self.HEIGHT = 950
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.run = True

    def update(self):
        if not self.run:
            pygame.quit()
            return

        self.timer.tick()
        self.screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
        pygame.display.flip()


if __name__ == '__main__':
    game = PacmanGame()
    while game.run:
        game.update()