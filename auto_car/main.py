from draw_map import *


class car:
    def __init__(self,rect):
        self.rect = pg.Rect(rect)
        self.cal_rect = self.rect
        self.sen_rect = pg.Rect((self.rect[0] - 20, self.rect[1] - 20, rect[2] + 40, rect[3] + 40))
        self.color = (69,96,69)#(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        self.angle = 0
        self.mag = 2

    def action(self, choice):
        if choice == 0:
            self.move(ang=-5)
        elif choice == 1:
            self.move(ang=5)
        elif choice == 2:
            self.move(ang = 0)

    def __sub__(self, other):
        return ((self.rect.centerx - other[0])//2, (self.rect.centery - other[1])//2)

    def move(self, ang=0):
        self.angle += ang
        
        
   
    def draw(self, surface):
        position = (int(self.rect.x), int(self.rect.y))
        self.sen_rect = pg.Rect((position[0] - 40, position[1] - 40,  80, 80))
        #pg.draw.rect(surface, (0,0,255), self.sen_rect)
        self.rect.x += np.around(np.cos(np.radians(self.angle)), decimals=5)*self.mag
        self.rect.y += np.around(np.sin(np.radians(self.angle)), decimals=5)*self.mag
        
       
        rotation_offset_center = (0, 0)
        nRenderRatio = 1 #2/4/8
        sw = self.rect[2]+abs(rotation_offset_center[0])*2
        sh = self.rect[3]+abs(rotation_offset_center[1])*2
        surfcenterx = sw//2
        surfcentery = sh//2
        s = pg.Surface( (sw*nRenderRatio,sh*nRenderRatio) )
        s = s.convert_alpha()
        s.fill((0,0,0,0))
        rw2=self.rect[2]//2 # halfwidth of rectangle
        rh2=self.rect[3]//2
        pg.draw.rect( s, self.color, ((surfcenterx-rw2-rotation_offset_center[0])*nRenderRatio,(surfcentery-rh2-rotation_offset_center[1])*nRenderRatio,self.rect[2]*nRenderRatio,self.rect[3]*nRenderRatio), border_radius=0)
        s = pg.transform.rotate( s, 90-self.angle )    
        self.cal_rect = pg.Rect((self.rect.x, self.rect.y, s.get_width(), s.get_height()))  
        if nRenderRatio != 1: 
            s = pg.transform.smoothscale(s,(s.get_width()//nRenderRatio,s.get_height()//nRenderRatio))
        incfromrotw = (s.get_width()-sw)//2
        incfromroth = (s.get_height()-sh)//2
        self.width, self.height = s.get_width(), s.get_height()
        surface.blit( s, (position[0] - self.rect[2]/2 -surfcenterx+rotation_offset_center[0]+rw2-incfromrotw,
            position[1] - self.rect[3]/2-surfcentery+rotation_offset_center[1]+rh2-incfromroth) )
        
    

ALL_WALL, GOAL, CAR_RECT = draw_map()


episode_rewards = []
for episode in range(HM_EPISODES):
    pg.init()
    SURFACE = pg.display.set_mode(WIN_SIZE)
    CLOCK = pg.time.Clock()
    FPS = 60
    pg.display.set_caption('self driving car!')


    player = car(CAR_RECT)
    done = False

    if episode % SHOW_EVERY == 0:
        print(f'on # {episode}, epsilon: {epsilon}')
        print(f' {SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}')
        show = True
    else:
        show = False

    episode_reward = 0
    while not done: # main loop
        for point in [j for sub in ALL_WALL for j in sub]:
            if player.sen_rect.collidepoint(point):
                obs = player - point
                if np.random.random() > epsilon:
                    action = np.argmax(q_table[obs])
                else:
                    action = np.random.randint(0, 3)
                #print(action)
                player.action(action)
        
        if player.rect.x < 0 or player.rect.x > WIN_SIZE[0] - player.rect.w:
            reward = -WALL_PENALTY 
        elif player.rect.y < 0 or player.rect.y + player.rect.w > WIN_SIZE[1]:
            reward = -WALL_PENALTY
        else:
            reward = 0
        for point in [j for sub in ALL_WALL for j in sub]:
            if player.cal_rect.collidepoint(point):
                reward = -WALL_PENALTY
        for point in GOAL:
            if  player.cal_rect.collidepoint(point):
                reward = GOAL_REWARD
      
        for point in [j for sub in ALL_WALL for j in sub]:
            if player.sen_rect.collidepoint(point):
                new_obs = player - point
                max_future_q = np.max(q_table[new_obs])
                current_q = q_table[obs][action]
        

                if reward == GOAL_REWARD:
                    new_q = GOAL_REWARD
                elif reward == -WALL_PENALTY:
                    new_q = -WALL_PENALTY
                else:
                    new_q = (1 - LEARNING_RATE)* current_q + LEARNING_RATE*(reward + DISCOUNT*max_future_q)
                
                q_table[obs][action] = new_q

        if show:
            
            #player.action(choice=np.random.randint(0,3))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
            '''keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                player.action(0)        
            if keys[pg.K_d]:
                player.action(1)   
            if keys[pg.K_w]:
                player.action(2)   '''
                    
            SURFACE.fill('azure')

            for walls in ALL_WALL:
                pg.draw.lines(SURFACE, (0,0,0), False, walls)
            pg.draw.lines(SURFACE, (255,0,0), False, GOAL)
            player.draw(SURFACE)
            pg.display.update()
            CLOCK.tick(FPS)
        episode_reward += reward
        if reward == GOAL_REWARD or reward == -WALL_PENALTY:
            done = True
    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY

#moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

'''plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"Reward {SHOW_EVERY} moving average")
plt.xlabel("episode #")
plt.show()'''

with open("qtable-car.pickle", "wb") as f:
    pickle.dump(q_table, f)
