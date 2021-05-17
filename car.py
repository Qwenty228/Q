# my shitty take

import pygame as pg
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

SIZE = (400, 800)
N_SIZE = 10
WIN_SIZE = (400, 400)
HM_EPISODES = 2500
ENEMY_PENALTY = 5
MOVE_PENALTY = 0.2

epsilon = 0.0
EPS_DECAY = 0.9998

SHOW_EVERY = 100

start_q_table = 'qtable-car-1621268045.pickle' # or existing q table filename

LEARNING_RATE = 0.5
DISCOUNT = 1


class box:
    def __init__(self,rect):
        self.rect = pg.Rect(rect)
        self.color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        self.vel = 0

    def action(self, choice):
        if choice == 0:
            self.move(x=4)
        elif choice == 1:
            self.move(x=-4)
        elif choice == 2:
            self.move(x=0)

    def __sub__(self, other):
        return (((self.rect.x + self.rect.w)/2 - (other.rect.x + other.rect.w)/2)*N_SIZE//WIN_SIZE[0],
         (self.rect.y - other.rect.y)*N_SIZE//WIN_SIZE[1] if WIN_SIZE[1] >= (self.rect.y - other.rect.y) > 0 else N_SIZE + 1 )

    def move(self, x=False):
        if not x:
            self.vel = np.random.randint(-5, 6)
        else:
            self.vel = x

        self.rect.x += self.vel
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIN_SIZE[0] - self.rect.w:
            self.rect.x = WIN_SIZE[0] - self.rect.w
   

if start_q_table is None:
    q_table = {}
    for x1 in range(-N_SIZE, N_SIZE):
        for y1 in range(0, N_SIZE + 2):
            for x2 in range(-N_SIZE, N_SIZE):
                for y2 in range(0, N_SIZE + 2):
                    q_table[((x1, y1),(x2, y2))] = [np.random.uniform(-5, 0) for i in range(3)]


else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)






episode_rewards = []
for episode in range(HM_EPISODES):
    GOAL = {'REWARD':15,
        'rect':pg.Rect(0, -SIZE[1] + 100, SIZE[0], 10),
        'COLOR':'firebrick'}

    pg.init()
    SURFACE = pg.display.set_mode(WIN_SIZE)
    CLOCK = pg.time.Clock()
    FPS = 60
    pg.display.set_caption('Car!')


    player = box((np.random.randint(0, WIN_SIZE[0]-50), 340, 25, 50))
    wall1 = box((np.random.randint(0, WIN_SIZE[0]-50), np.random.randint(-200,0), np.random.randint(50,150), 50))
    wall2 = box((np.random.randint(0, WIN_SIZE[0]-50), np.random.randint(-450,-250), np.random.randint(50,150), 50))
    wall3 = box((np.random.randint(0, WIN_SIZE[0]-50), np.random.randint(-700,-500), np.random.randint(50,150), 50))
    wall_list = [wall1, wall2, wall3]
    bottom = 0
    done = False

    if episode % SHOW_EVERY == 0:
        print(f'on # {episode}, epsilon: {epsilon}')
        print(f' {SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}')
        show = True
    else:
        show = False

    episode_reward = 0
    while not done: # main loop
        if bottom < SIZE[1]: 
            bottom += 10
            GOAL['rect'].y += 10
            for i in wall_list:
                i.rect.y += 10
        else:
            if player.rect.y + player.rect.h/2 > GOAL['rect'].y:
                player.rect.y -= 10
            
        
        nearest = wall_list[np.argmin([(player - x)[1] for x in wall_list])]
        sec_near = [x for x in wall_list if N_SIZE + 1 > (player - x)[1] >= (player - nearest)[1]]
        sec_near = nearest if len(sec_near) == 0 else sec_near[1-len(sec_near)] 
        obs = (player - nearest, player - sec_near)
        if np.random.random() > epsilon:
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 3)

        player.action(action)
        
        if nearest.rect.x - player.rect.w <= player.rect.x < nearest.rect.x + nearest.rect.w  and nearest.rect.y < player.rect.y <= nearest.rect.y + nearest.rect.h :
           reward = -ENEMY_PENALTY
        elif player.rect.y + player.rect.h/2 <= GOAL['rect'].y:
            reward = GOAL['REWARD']
        elif player.vel == 0:
            reward = 0
        else:
            reward = -MOVE_PENALTY

        new_obs = (player - nearest, player - sec_near)
        max_future_q = np.max(q_table[new_obs])
        current_q = q_table[obs][action]

        if reward == GOAL['REWARD']:
            new_q = GOAL['REWARD']
        elif reward == -ENEMY_PENALTY:
            new_q = -ENEMY_PENALTY
        else:
            new_q = (1 - LEARNING_RATE)* current_q + LEARNING_RATE*(reward + DISCOUNT*max_future_q)
        
        q_table[obs][action] = new_q

        if show:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
            SURFACE.fill('azure')

            for i in wall_list:
                pg.draw.rect(SURFACE, i.color, i.rect)
            pg.draw.rect(SURFACE, GOAL['COLOR'], GOAL['rect'])
            pg.draw.rect(SURFACE, 'dodgerblue', player.rect)
            pg.display.update()
            CLOCK.tick(FPS)
        episode_reward += reward
        if reward == GOAL['REWARD'] or reward == -ENEMY_PENALTY:
            done = True

    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"Reward {SHOW_EVERY} moving average")
plt.xlabel("episode #")
plt.show()

with open("qtable-car-1621268045.pickle", "wb") as f:
    pickle.dump(q_table, f)