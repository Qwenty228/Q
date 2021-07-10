import torch
import numpy as np
from collections import deque
from model import QTrainer, Linear_QNet
from game import Game
import random
import os

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
PATH = './model/model.pth' if os.path.isdir('./model/model3.pth') else None


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(9, 256, 3, PATH)
        self.trainer = QTrainer(self.model, learning_rate=LR, gamma=self.gamma)
        self.reward = 0

    def get_state(self, game):
        state = [
            # nearest Danger
            game.car.get_data()[0][0],
            game.car.get_data()[0][1],
            game.car.get_data()[0][2],
            game.car.get_data()[0][3],
            game.car.get_data()[0][4],
            game.car.get_data()[0][5],
            game.car.get_data()[0][6],
            game.car.get_data()[0][7],
      
            # angle
            game.car.get_data()[1],

            


            
            ]
        '''# goal location
            game.goal[0] < game.car.pos[0],  # food left
            game.goal[0] > game.car.pos[0],  # food right
            game.goal[1] < game.car.pos[1],  # food up
            game.goal[1] > game.car.pos[1]  # food down'''

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)


    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
        if done:
            self.reward += reward//10 if reward > 0 else 0

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        
        self.epsilon = 10 - self.reward
        final_move = [0,0,0]
        if np.random.randint(0, 200) < self.epsilon:
            move = np.random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()
    while True:
        # get old state
        state_old = agent.get_state(game)
        #print(state_old)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record, f'reward {reward} and {agent.reward}' )

            '''plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)'''


if __name__ == '__main__':
    train()