import numpy as np
import random
from environment import Environment

class QLearningAgent:
    def __init__(self, env, alpha=0.10, gamma=0.7, epsilon=0.1, epsilon_decay=0.995, epsilon_min=0.01):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.q_table = np.zeros((env.rows, env.cols, 4))

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, 3)  # Ação aleatória
        else:
            row, col = state
            return np.argmax(self.q_table[row, col])  # Melhor ação baseada na Q-table

    def update_q_value(self, state, action, reward, next_state, done):
        row, col = state
        next_row, next_col = next_state
        best_next_action = np.argmax(self.q_table[next_row, next_col])
        td_target = reward + (self.gamma * self.q_table[next_row, next_col, best_next_action] * (1 - done))
        self.q_table[row, col, action] += self.alpha * (td_target - self.q_table[row, col, action])

    def train(self, episodes, max_steps_per_episode=100):
        rewards = []
        for episode in range(episodes):
            total_reward = 0
            state = self.env.reset()
            for step in range(max_steps_per_episode):
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.update_q_value(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward
                if done:
                    break
            rewards.append(total_reward)
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
            if episode % 1000 == 0:
                print(f"Episode {episode}, Total Reward: {total_reward}")

    def save_q_table(self, file_path):
        np.save(file_path, self.q_table)

    def load_q_table(self, file_path):
        self.q_table = np.load(file_path)

if __name__ == "__main__":
    env = Environment()
    agent = QLearningAgent(env)
    agent.train(20000)

    agent.save_q_table("q_table.npy")

    print("Treinamento concluído e Q-table salva!")
