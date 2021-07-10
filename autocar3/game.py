
import pygame as pg
from enum import Enum
from collections import namedtuple
import numpy as np
from draw_map import draw_map
import os
from car import Car
from Lib import map_range, Vector



pg.init()
#font = pg.font.Font('arial.ttf', 25)
font = pg.font.SysFont('arial', 25)



Point = namedtuple('Point', 'x, y')
FOLDER = 'data'
SPEED = 120


class Game:

    def __init__(self, w=1200, h=640):
        self.w = w
        self.h = h
        # init display
        self.display = pg.display.set_mode((self.w, self.h))
        
        self.clock = pg.time.Clock()
        self.pos, self.goal = draw_map()
        self.reset()


    def reset(self):
        # init game state
        
        self.car = Car(self.pos)
        self.map = pg.image.load(os.path.join((FOLDER), 'map.png'))
        self.head = Point(self.w/2, self.h/2)
        self.score = 0
        self.frame_iteration = 0
        pg.display.set_caption(f'Car3 frame = {self.frame_iteration}')



    def play_step(self, action):
        self.frame_iteration += 1
        pg.display.set_caption(f'Car3 frame = {self.frame_iteration}')
        # 1. collect user input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            
        
        # 2. move
        self._move(action) # update the head
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() :
            game_over = True
            reward = -10 + map_range(self.frame_iteration, 0, 1000, 0, 5)
            
            return reward, game_over, self.score
        if self.frame_iteration > 1000:
            game_over = True
            reward = -15
            
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.car.goal:
            self.score += 1
            reward = 10
            game_over = True
        
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self):
        return not self.car.is_alive


    def _update_ui(self):
        self.display.fill('white')
        self.display.blit(self.map,(0,0))
        self.car.update(self.map)
        self.car.draw(self.display)
        #text = font.render("Score: " + str(self.score), True, WHITE)
        #self.display.blit(text, [0, 0])
        pg.display.flip()


    def _move(self, action):
        self.car.action(np.argmax(action) + 1)


