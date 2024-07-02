import pygame
import sys
import numpy as np
import time
from environment import Environment

pygame.init()

width, height = 600, 600
rows, cols = 6, 6
cell_size = width // cols

black = (0, 0, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mapa 6x6')

def draw_grid():
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

def draw_map(env, state):
    for row in range(env.rows):
        for col in range(env.cols):
            rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
            color = tuple(env.grid_colors[row, col])
            pygame.draw.rect(screen, color, rect)
            if (row, col) == state:
                pygame.draw.rect(screen, (0, 255, 0), rect)  # Green for robot
            pygame.draw.rect(screen, black, rect, 1)

def main():
    q_table = np.load("q_table.npy")
    
    def choose_action(state):
        row, col = state
        return np.argmax(q_table[row, col])
    
    env = Environment()
    
    state = env.reset()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        action = choose_action(state)
        next_state, reward, done = env.step(action)
        state = next_state

        screen.fill(black)
        draw_grid()
        draw_map(env, state)
        pygame.display.flip()

        if done:
            time.sleep(2)
            state = env.reset()

        time.sleep(0.5)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
