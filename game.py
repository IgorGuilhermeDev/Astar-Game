import pygame
import random
from settings import WIDTH, HEIGHT, TILE_SIZE, FPS, GRID_WIDTH, GRID_HEIGHT
from astar import astar_search
from player import Player
from enemy import Enemy
from fruit import Fruit
from enum import Enum

class GameState(Enum):
    RUNNING = 1
    GAME_OVER = 2
    GAME_OVER_WIN = 3

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player(0, 0)
        self.enemy = Enemy(5, 5)  
        self.grid, self.goal_pos = self.generate_random_grid(GRID_WIDTH, GRID_HEIGHT)
        self.fruit = Fruit(self.grid)
        self.path = []
        self.path_index = 0
        self.state = GameState.RUNNING

        
        self.goal_image = pygame.image.load('assets/goal.png')
        self.goal_image = pygame.transform.scale(self.goal_image, (TILE_SIZE, TILE_SIZE))
        self.block_image = pygame.image.load('assets/block.png')
        self.block_image = pygame.transform.scale(self.block_image, (TILE_SIZE, TILE_SIZE))

        
        self.button_width = 200
        self.button_height = 50
        self.button_spacing = 20
        self.restart_button = pygame.Rect((WIDTH - self.button_width) // 2, (HEIGHT - self.button_height * 2 - self.button_spacing) // 2, self.button_width, self.button_height)
        self.quit_button = pygame.Rect((WIDTH - self.button_width) // 2, (HEIGHT - self.button_height * 2 - self.button_spacing) // 2 + self.button_height + self.button_spacing, self.button_width, self.button_height)

    def generate_random_grid(self, width, height):
        while True:
            grid = [['_' for _ in range(width)] for _ in range(height)]
            num_blocks = random.randint(20, 40)  
            for _ in range(num_blocks):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                if (x, y) not in [(0, 0), (5, 5)]:
                    grid[y][x] = 'B'

                
            corners = [(0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)]
            corners.remove((0, 0))

    
            goal_position = random.choice(corners)
            grid[goal_position[1]][goal_position[0]] = 'o'

    
            if astar_search((0, 0), (goal_position[1], goal_position[0]), grid):
                return grid, goal_position

    def draw_grid(self):
        for x in range(0, WIDTH, TILE_SIZE):
            for y in range(0, HEIGHT, TILE_SIZE):
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def draw_elements(self):
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col == 'B':
                    self.screen.blit(self.block_image, (x * TILE_SIZE, y * TILE_SIZE))
                elif (x, y) == self.goal_pos:
                    self.screen.blit(self.goal_image, (x * TILE_SIZE, y * TILE_SIZE))
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        if self.fruit.position:
            self.fruit.draw(self.screen)

    def display_restart_screen(self, message):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 54)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (0, 255, 0), self.restart_button)
        pygame.draw.rect(self.screen, (255, 0, 0), self.quit_button)

        small_font = pygame.font.Font(None, 50)
        restart_text = small_font.render("Restart", True, (0, 0, 0))
        quit_text = small_font.render("Quit", True, (0, 0, 0))

        self.screen.blit(restart_text, (self.restart_button.x + (self.button_width - restart_text.get_width()) // 2, self.restart_button.y + 10))
        self.screen.blit(quit_text, (self.quit_button.x + (self.button_width - quit_text.get_width()) // 2, self.quit_button.y + 10))


    def restart_game(self):
        self.grid, self.goal_pos = self.generate_random_grid(GRID_WIDTH, GRID_HEIGHT)
        self.player = Player(0, 0)
        self.enemy = Enemy(5, 5)
        self.fruit = Fruit(self.grid)
        self.path = []
        self.path_index = 0
        self.state = GameState.RUNNING

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if (self.state == GameState.GAME_OVER or self.state == GameState.GAME_OVER_WIN) and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_button.collidepoint(event.pos):
                        self.restart_game()
                    elif self.quit_button.collidepoint(event.pos):
                        pygame.quit()
                        return

            if self.state == GameState.RUNNING:
                self.screen.fill((0, 0, 0))
                self.draw_grid()
                self.draw_elements()

                if self.player.path_needs_recalculation:
                    self.path = astar_search((self.player.y, self.player.x), (self.goal_pos[1], self.goal_pos[0]), self.grid, True)
                    self.player.path_needs_recalculation = False
                    self.path_index = 0

                if not self.path:
                    self.path = astar_search((self.player.y, self.player.x), (self.goal_pos[1], self.goal_pos[0]), self.grid)
                    self.path_index = 0

                if self.path and self.path_index < len(self.path):
                    next_step = self.path[self.path_index]
                    if (self.grid[next_step[0]][next_step[1]] != 'B' or self.player.can_pass_through_blocks):
                        if (next_step[1], next_step[0]) == (self.enemy.x, self.enemy.y):
                            self.state = GameState.GAME_OVER
                            
                    self.player.move_to(next_step[1], next_step[0])
                    self.path_index += 1
                    self.player.check_collision_with_fruit(self.fruit)
                    self.enemy.move(self.grid)

                
                else:
                    self.state = GameState.GAME_OVER_WIN

                if (self.player.x, self.player.y) == (self.enemy.x, self.enemy.y):
                    self.state = GameState.GAME_OVER

            elif self.state == GameState.GAME_OVER:
                self.display_restart_screen("Capitão pátria te matou :(")
            elif self.state == GameState.GAME_OVER_WIN:                
                self.display_restart_screen("Chegou no Ryan !")

            pygame.display.flip()
            self.clock.tick(FPS // 10)  
