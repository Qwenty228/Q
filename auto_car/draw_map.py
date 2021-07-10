import pygame as pg
import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

N_SIZE = 30
WIN_SIZE = (800, 500)
HM_EPISODES = 10000
WALL_PENALTY = 5

epsilon = 0.5
EPS_DECAY = 0.9998
GOAL_REWARD = 50

SHOW_EVERY = 1

start_q_table = "qtable-car.pickle" #'qtable-car-1621268045.pickle' # or existing q table filename

LEARNING_RATE = 0.5
DISCOUNT = 0.9





if start_q_table is None:
    q_table = {}
    for x1 in range(-N_SIZE, N_SIZE + 1):
        for y1 in range(-N_SIZE, N_SIZE + 1):
            q_table[(x1, y1)] = [np.random.uniform(-5, 0) for i in range(3)]


else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)



def draw_map():
    pg.init()
    SURFACE = pg.display.set_mode(WIN_SIZE)
    CLOCK = pg.time.Clock()
    FPS = 60
    run = True
    once = False
    shape_list = []
    car_rect = (100, 100, 10, 15)
    wall_list = []
    finish_line = []
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    shape_list = []
                    finish_line = []
                    wall_list = []
                    once = False
                if event.key == pg.K_c:
                    car_rect = (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 10, 15)
                if event.key == pg.K_s:
                    with open("map.pickle", "wb") as f:
                        pickle.dump((shape_list, finish_line, car_rect), f)
                if event.key == pg.K_o:
                    with open('map.pickle', "rb") as f:
                        data = pickle.load(f)
                    shape_list = data[0]
                    finish_line = data[1]
                    car_rect = data[2]
                  
                    
        if pg.mouse.get_pressed()[0]:
            if len(wall_list) > 1:
                if pg.mouse.get_pos() not in wall_list:
                    wall_list.append(pg.mouse.get_pos())
                   
            else:
                wall_list.append(pg.mouse.get_pos())
        else:
            if wall_list not in shape_list and wall_list != []:
                shape_list.append(wall_list[:])
            wall_list = []

        if pg.mouse.get_pressed()[2] and not once:
            if len(finish_line) > 1:
                if pg.mouse.get_pos() not in finish_line:
                    finish_line.append(pg.mouse.get_pos())
                   
            else:
                finish_line.append(pg.mouse.get_pos())
        else:
            if len(finish_line) > 1:
                once = True
        

        SURFACE.fill('azure')
        if len(wall_list) > 1:
            pg.draw.lines(SURFACE, (0,0,0),False, wall_list, 2)
        for wall in shape_list:
            if len(wall) > 1:
                pg.draw.lines(SURFACE, (0,0,0),False, wall, 2)
        if len(finish_line) > 1:
            pg.draw.lines(SURFACE, (255,0,0),False, finish_line, 2)
        pg.draw.rect(SURFACE, (0,255,0), pg.Rect(car_rect))
        pg.display.update()
        CLOCK.tick(FPS)


    return shape_list, finish_line, car_rect

