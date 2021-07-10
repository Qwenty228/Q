import math
import pygame as pg
import os


FOLDER = 'data'
CAR_IMG = pg.transform.scale(pg.image.load(os.path.join((FOLDER), 'car.png')), (40,40))
WIN_SIZE = (1200, 640)

class Car:
    def __init__(self, pos):
        self.img = CAR_IMG
        self.rotate_surface = self.img
        self.size = self.img.get_rect()
        self.pos = [pos[0], pos[1]]
        self.angle = 0
        self.speed = 0
        self.center = [self.pos[0] + self.size[2]//2, self.pos[1] + self.size[3]//2]
        self.radars = []
        self.radars_for_draw = []
        self.is_alive = True
        self.goal = False
        self.distance = 0
        self.time_spent = 0
        self.food = False

    def draw(self, screen):
        screen.blit(self.rotate_surface, self.pos)
        self.draw_radar(screen)

    def draw_radar(self, screen):
        for r in self.radars:
            pos, dist = r
            pg.draw.line(screen, (0, 255, 0), self.center, pos, 1)
            pg.draw.circle(screen, (0, 255, 0), pos, 5)

    def check_collision(self, map):
        self.is_alive = True
        for p in self.four_points:
            if int(p[0]) >= WIN_SIZE[0] - 5 or int(p[0]) <= 5 or int(p[1]) >= WIN_SIZE[1] - 5 or int(p[1]) < 5:
                self.is_alive = False
                break
            if map.get_at((int(p[0]), int(p[1]))) == (0, 0, 0, 255):
                self.is_alive = False
                break
            if map.get_at((int(p[0]), int(p[1]))) == (255, 0, 0, 255):
                self.goal = True
                break
            if map.get_at((int(p[0]), int(p[1]))) == (255, 255, 0, 255):
                self.food = True
                break
    def check_radar(self, degree, map):
        len = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        while not map.get_at((x, y)) == (0, 0, 0, 255) and len < 500 and x < WIN_SIZE[0] - 5 and x > 5 and y < WIN_SIZE[1] - 5 and y > 5:
            len += 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)
        

        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def update(self, map):
        #check speed
        self.speed = 8

        #check position
        self.rotate_surface = self.rot_center(self.img, self.angle)
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        if self.pos[0] < 20:
            self.pos[0] = 20
        elif self.pos[0] > WIN_SIZE[0] - self.size[2]:
            self.pos[0] = WIN_SIZE[0] - self.size[2]

        self.distance += self.speed
        self.time_spent += 1
        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        if self.pos[1] < 20:
            self.pos[1] = 20
        elif self.pos[1] > WIN_SIZE[1] - 20:
            self.pos[1] = WIN_SIZE[1] - 20

        # caculate 4 collision points
        self.center = [self.pos[0] + self.size[2]//2, self.pos[1] + self.size[3]//2]
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * self.size[2]//2, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * self.size[3]//2]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * self.size[2]//2, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * self.size[3]//2]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * self.size[2]//2, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * self.size[3]//2]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * self.size[2]//2, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * self.size[3]//2]
        self.four_points = [left_top, right_top, left_bottom, right_bottom]

        self.check_collision(map)
        self.radars.clear()
        for d in range(-120, 120, 30):
            self.check_radar(d, map)

    def get_data(self):
        radars = self.radars
        ret = [0,0,0,0,0,0,0,0]
        for i, r in enumerate(radars):
            ret[i] = int(r[1] // 25)

        return ret, (self.angle % 360)//90

    def get_alive(self):
        return self.is_alive

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def action(self, choice=3):
        if choice == 1:
            self.angle -= 8
        elif choice == 2:
            self.angle += 8
        elif choice == 3:
            self.angle += 0