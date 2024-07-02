import numpy as np
from environment import Environment
from q_learning import QLearningAgent

if __name__ == "__main__":
    env = Environment()
    agent = QLearningAgent(env)
    agent.train(120000)

    agent.save_q_table("q_table.npy")
    
    print("Treinamento concluído e Q-table salva!")
