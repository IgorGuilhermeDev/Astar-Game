import pygame
from settings import TILE_SIZE

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('assets/player.png')
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.can_pass_through_blocks = False
        self.path_needs_recalculation = False

    def draw(self, screen):
        screen.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def check_collision_with_fruit(self, fruit):
        if (self.x, self.y) == fruit.position:
            self.can_pass_through_blocks = True
            fruit.relocate()
            self.path_needs_recalculation = True
