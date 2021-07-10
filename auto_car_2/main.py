from settings import *
from car import Car
from draw_map import draw_map



car_pos = draw_map()

episode_rewards = []

for episode in range(HM_EPISODES):
    player = Car(car_pos)
    MAP = pg.image.load(os.path.join((FOLDER), 'map.png'))
    done = False
    pg.init()
    SURFACE = pg.display.set_mode(WIN_SIZE)
    CLOCK = pg.time.Clock()
    FPS = 60
    pg.display.set_caption('self driving car!')
    if episode % SHOW_EVERY == 0:
        print(f'on # {episode}, epsilon: {epsilon}')
        print(f' {SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}')
    episode_reward = 0
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            #keys = pg.key.get_pressed()
            '''if keys[pg.K_a]:
                player.angle -= 3
            if keys[pg.K_d]:
                player.angle += 3'''

        SURFACE.blit(MAP, (0, 0))
        player.update(MAP)  
        if player.get_alive():
            player.draw(SURFACE)

        obs = (player.get_data())
        if np.random.random() > epsilon:
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 3)

        player.action(action)
        
        if not player.get_alive():
            reward = -WALL_PENALTY
        elif player.goal:
            reward = GOAL_REWARD 
        elif player.food:
            reward = 0.1
        else:
            reward = 0.5**(abs(obs[0]-obs[2]))

        print(0.5**abs(obs[0]-obs[2]), obs)

        new_obs = (player.get_data())
        max_future_q = np.max(q_table[new_obs])
    
        current_q = q_table[obs][action]

        
        new_q = (1 - LEARNING_RATE)* current_q + LEARNING_RATE*(reward + DISCOUNT*max_future_q)
        
       
        q_table[obs][action] = new_q
        
        
        pg.display.update()
        CLOCK.tick(FPS)
        episode_reward += reward
        if reward == GOAL_REWARD or reward == -WALL_PENALTY:
            done = True
    

    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"Reward {SHOW_EVERY} moving average")
plt.xlabel("episode #")
plt.show()

 
with open(os.path.join((FOLDER),"qtable-car.pickle"), "wb") as f:
    pickle.dump(q_table, f)
