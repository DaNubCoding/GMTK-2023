import pygame

VEC = pygame.math.Vector2

FPS = 144
WIN_WIDTH, WIN_HEIGHT = WIN_SIZE = 512, 384
WIDTH, HEIGHT = SIZE = WIN_WIDTH // 4, WIN_HEIGHT // 4
HSIZE = (WIDTH // 2, HEIGHT // 2)
SKY_COLOR = (135, 206, 250)
GROUND_COLOR = (110, 67, 37)
GRAVITY = 90

pygame.font.init()
ENERGY_FONT = pygame.font.Font("res/fonts/PixgamerRegular-OVD6A.ttf", 16)
MAIN_FONT = pygame.font.Font("res/fonts/slkscr.ttf", 9)