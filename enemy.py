import pygame
from settings import TILE_SIZE

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('assets/enemy.png')
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.direction = 1

    def move(self, grid):
        next_y = self.y + self.direction
        if next_y < 0 or next_y >= len(grid) or grid[next_y][self.x] == 'B':
            self.direction *= -1
        else:
            self.y += self.direction

    def draw(self, screen):
        screen.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))
