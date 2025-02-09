import pygame
import random
from settings import TILE_SIZE

class Fruit:
    def __init__(self, grid):
        self.image = pygame.image.load('assets/fruit.png')
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.grid = grid
        self.position = self.random_position()

    def random_position(self):
        while True:
            x = random.randint(0, len(self.grid[0]) - 1)
            y = random.randint(0, len(self.grid) - 1)
            if self.grid[y][x] == '_':
                return (x, y)

    def draw(self, screen):
        screen.blit(self.image, (self.position[0] * TILE_SIZE, self.position[1] * TILE_SIZE))

    def relocate(self):
        self.position = None
