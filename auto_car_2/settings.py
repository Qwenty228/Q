import pygame as pg
import numpy as np
import math
import os
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

N_SIZE = 20
WIN_SIZE = (800, 500)
HM_EPISODES = 500
WALL_PENALTY = 5

epsilon = 0.4
EPS_DECAY = 0.98
GOAL_REWARD = 50

SHOW_EVERY = 1

start_q_table =  "qtable-car.pickle" #"qtable-car.pickle" #'qtable-car-1621268045.pickle' # or existing q table filename

LEARNING_RATE = 0.2
DISCOUNT = 0.95

FOLDER = 'data'

CAR_IMG = pg.transform.scale(pg.image.load(os.path.join((FOLDER), 'car.png')), (40,40))



if start_q_table is None:
    q_table = {}
    for d1 in range(0, N_SIZE + 1):
        for d2 in range(0, N_SIZE + 1):
            for d3 in range(0, N_SIZE + 1):
                for ang in range(-N_SIZE, N_SIZE + 1):
                    q_table[(d1, d2, d3, ang)] = [np.random.uniform(-5, 0) for i in range(3)]


else:
    with open(os.path.join((FOLDER),start_q_table), "rb") as f:
        q_table = pickle.load(f)

