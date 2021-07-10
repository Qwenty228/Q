from settings import *

def draw_map():
    pg.init()
    SURFACE = pg.display.set_mode(WIN_SIZE)
    CLOCK = pg.time.Clock()
    FPS = 60
    run = True
    once = False
    shape_list = []
    car_pos = (100, 100)
    wall_list = []
    finish_line = []
    food = []
    inv = 0
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                SURFACE.fill('azure')
                pg.draw.lines(SURFACE, (255,0,0),False, finish_line, 20)
                for wall in shape_list:
                    pg.draw.lines(SURFACE, (0,0,0),False, wall, 10)
                for n in food:
                    pg.draw.circle(SURFACE,( 255, 255, 0), n, 40)
                pg.image.save(SURFACE, os.path.join(FOLDER, "map.png"))
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    shape_list = []
                    finish_line = []
                    wall_list = []
                    food = []
                    once = False
                if event.key == pg.K_c:
                    car_pos = (pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                if event.key == pg.K_s:
                    with open(os.path.join((FOLDER), "map.pickle"), "wb") as f:
                        pickle.dump((shape_list, finish_line, car_pos, food), f)
                if event.key == pg.K_o:
                    with open(os.path.join((FOLDER), 'map.pickle'), "rb") as f:
                        data = pickle.load(f)
                    shape_list = data[0]
                    finish_line = data[1]
                    car_pos = data[2]
                    food = data[3]
                if event.key == pg.K_t:
                    inv += 1
                    if inv> 1: inv = 0
                  
                    
        if pg.mouse.get_pressed()[0]:
            if inv ==0:
                if len(wall_list) > 1:
                    if pg.mouse.get_pos() not in wall_list:
                        wall_list.append(pg.mouse.get_pos())
                    
                else:
                    wall_list.append(pg.mouse.get_pos())
            else:
                food.append(pg.mouse.get_pos())
        else:
            if inv ==0:
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
        if len(finish_line) > 1:
            pg.draw.lines(SURFACE, (255,0,0),False, finish_line, 20)
        if len(wall_list) > 1:
            pg.draw.lines(SURFACE, (0,0,0),False, wall_list, 10)
        for wall in shape_list:
            if len(wall) > 1:
                pg.draw.lines(SURFACE, (0,0,0),False, wall, 10)
        if len(food) > 0:
            for n in food:
                pg.draw.circle(SURFACE,( 255, 255, 0), n, 40)
        SURFACE.blit(CAR_IMG, car_pos)
        pg.display.update()
        CLOCK.tick(FPS)

    
    return car_pos