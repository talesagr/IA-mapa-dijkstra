import numpy as np
import random

class Environment:
    def __init__(self):
        self.rows = 6
        self.cols = 6
        self.state = (0, 5)
        self.presents = { (1, 2), (3, 2), (4, 5) }
        self.zombies =  { (1, 0), (1, 4), (3, 3), (5, 0), (5,4) }
        self.walls = {(2, 3), (3, 4), (3, 5)}
        self.exit = (5, 5)
        self.collected_presents = set()
        self.present_value = 10
        self.exit_value = 100
        self.move_penalty = -1
        self.revisit_penalty = -5
        self.visited = set()
        self.grid_colors = np.full((self.rows, self.cols, 3), (255, 255, 255))

        for present in self.presents:
            self.grid_colors[present] = (255, 255, 0)
        for zombie in self.zombies:
            self.grid_colors[zombie] = (255, 0, 0)
        for wall in self.walls:
            self.grid_colors[wall] = (128, 128, 128)
        self.grid_colors[self.exit] = (0, 0, 255)

    def reset(self):
        self.state = (0, 0)
        self.collected_presents = set()
        self.visited = set()
        self.grid_colors = np.full((self.rows, self.cols, 3), (255, 255, 255))

        for present in self.presents:
            self.grid_colors[present] = (255, 255, 0)
        for zombie in self.zombies:
            self.grid_colors[zombie] = (255, 0, 0)
        for wall in self.walls:
            self.grid_colors[wall] = (128, 128, 128)
        self.grid_colors[self.exit] = (0, 0, 255)

        return self.state

    def is_terminal(self, state):
        return state == self.exit and len(self.collected_presents) >= len(self.presents) // 2

    def get_next_state(self, state, action):
        row, col = state
        if action == 0:   
            row = max(0, row - 1)
        elif action == 1: 
            col = min(self.cols - 1, col + 1)
        elif action == 2: 
            row = min(self.rows - 1, row + 1)
        elif action == 3: 
            col = max(0, col - 1)
        return (row, col)

    def get_reward(self, state):
        if state in self.zombies:
            return -10
        elif state in self.collected_presents:
            return self.move_penalty
        elif state in self.presents:
            return self.present_value
        elif state == self.exit:
            if len(self.collected_presents) >= len(self.presents) // 2:
                return self.exit_value
            else:
                return -10
        else:
            return self.move_penalty

    def step(self, action):
        next_state = self.get_next_state(self.state, action)
        if next_state in self.walls:
            next_state = self.state  
        reward = self.get_reward(next_state)
        if next_state in self.visited:
            reward += self.revisit_penalty 
        if next_state in self.presents and next_state not in self.collected_presents:
            self.collected_presents.add(next_state)
            self.grid_colors[next_state] = (200, 200, 200)  # Change color to grey when present is collected
        self.visited.add(next_state)
        self.state = next_state
        if next_state in self.zombies or next_state == self.exit:
            done = True
        else:
            done = False
        return next_state, reward, done
