# Copyright 2016 Zara Zaimeche

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#Python Python! It's snake, in python!

import sys, random, pygame
from pygame.locals import *
from colours import *
try:
    from snakeconf import *
except:
    from samplesnakeconf import *

savefile = open(SAVEFILE, 'r')

high_score = 0

high_score = savefile.read()
high_score = int(high_score)


WINDOWWIDTH = WIDTH
WINDOWHEIGHT = HEIGHT

CELLSIZE = 10

COLUMNS = WINDOWWIDTH / CELLSIZE
ROWS = WINDOWHEIGHT / CELLSIZE

MOVESPEED = 1

pygame.init()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

grid = []

for row in range(1, ROWS):
    for column in range (1, COLUMNS):
        coordinate = (column, row)
        grid.append(coordinate)

# each coordinate will correspond to one cell in the grid; we will multiply by
# 10 because we are terrible people who also use the royal 'we' for no reason

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
new_direction = ''


def main():

   score = 0

   snake = []
   center_of_screen = (COLUMNS/2, ROWS/2)
   snake_start_pos = center_of_screen
 
   food = []
   food_start_pos = random.choice(grid)

   FPSCLOCK = pygame.time.Clock()
   pygame.display.set_caption('python-python!')
   try:
       BASICFONT = pygame.font.Font('/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansCondensed.ttf', 16)
   except:
       BASICFONT = pygame.font.Font('freesansbold.ttf', 16)

   try:
       SHADOWFONT = pygame.font.Font('/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansCondensed.ttf', 16) #3Dish
   except:
       SHADOWFONT = pygame.font.Font('freesansbold.ttf', 16)


   food.append(food_start_pos)
   snake.append(snake_start_pos)
   direction = random.choice((UP, DOWN, LEFT, RIGHT))
   snake_crashed = False
   counter = 0
   
   if MUSIC != "":
       pygame.mixer.music.load(MUSIC)
       pygame.mixer.music.play(-1, 0.0)

   while True == True: #main game loop
       snake_lengthen = False
       score = (len(snake) - 1) * 100 # '-1' since it starts at 1
       score_surf = BASICFONT.render('Score: %d' % score, 1, BRIGHTRED)
       shadow_surf = SHADOWFONT.render('Score: %d' % score, 1, ORANGE)
       score_rect = score_surf.get_rect()
       score_rect.topleft = (10, 10)
       shadow_rect = shadow_surf.get_rect()
       shadow_rect.topleft = (11, 9)

       if score < high_score:
           high_score_surf = BASICFONT.render('High score: %d' % high_score, 1, BLUE)
       else: #duplicated, but so we're not reading from file a lot
           high_score_surf = BASICFONT.render('High score: %d' % score, 1, BLUE)

       high_score_rect = high_score_surf.get_rect()
       high_score_rect.topleft = (150, 10)

       DISPLAYSURF.fill(BLACK)
       DISPLAYSURF.blit(shadow_surf, shadow_rect)
       DISPLAYSURF.blit(score_surf, score_rect)
       DISPLAYSURF.blit(high_score_surf, high_score_rect)

       draw_food(food)
       check_for_quit(score, high_score)
       direction = change_direction(direction)
       snake = refresh_snake(snake, direction, snake_lengthen)
       snake_crashed = detect_crash(snake)
       if snake_crashed == True:
           draw_snake(snake)
           quit(score, high_score)
       snake_eating(snake, food, direction)
       pygame.display.update()
       FPSCLOCK.tick(FPS)

def quit(score, high_score):
    if score > high_score:
        score = str(score) #file.write() requires string
        savefile = open(SAVEFILE, 'w')
        savefile.write(score)
    pygame.quit()
    sys.exit()

def check_for_quit(score, high_score):
    for event in pygame.event.get(QUIT):
        quit(score, high_score)
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            quit(score, high_score)
        pygame.event.post(event)

def change_direction(direction):
    for event in pygame.event.get():
        if event.type == KEYDOWN: # this is here so that KEYUP events are handled. otherwise,
                                # they will eventually render the snake unresponsive, and
                                # it will crash into a wall as the gamer looks on in anguish.
            pygame.event.post(event)
    for event in pygame.event.get(KEYDOWN):
        if event.key == K_LEFT and direction is not RIGHT: #now snake can't go back on itself
            direction = LEFT
        elif event.key == K_RIGHT and direction is not LEFT:
            direction = RIGHT
        elif event.key == K_UP and direction is not DOWN:
            direction = UP
        elif event.key == K_DOWN and direction is not UP:
            direction = DOWN
    return direction

def add_snake_head(old_snake_head, move_dir):
    if move_dir == UP:
        new_snake_head = (old_snake_head[0], old_snake_head[1]-MOVESPEED)
    elif move_dir == DOWN:
        new_snake_head = (old_snake_head[0], old_snake_head[1]+MOVESPEED)
    elif move_dir == LEFT:
        new_snake_head = (old_snake_head[0]-MOVESPEED, old_snake_head[1])
    elif move_dir == RIGHT:
        new_snake_head = (old_snake_head[0]+MOVESPEED, old_snake_head[1])
    return new_snake_head

def refresh_snake(snake, direction, snake_lengthen):
    new_snake_head = add_snake_head(snake[-1], direction)
    snake.append(new_snake_head)
    if snake_lengthen == False:
        snake.remove(snake[0])
    else:
        snake_lengthen = False
    draw_snake(snake)
    return snake

def check_duplicates(snake):
    snake_copy = snake[:]
    for i in snake_copy:
        value = i
        snake_copy.remove(i)
        if value in snake_copy:
            duplicates = True
            return duplicates
    duplicates = False
    return duplicates

def check_for_wall(snake):
    for i in snake:
        if i[0] >= COLUMNS or i[0] < 0 or i[1] >= ROWS or i[1] < 0:
            wall_in_snake = True
            return wall_in_snake
    wall_in_snake = False
    return wall_in_snake

def detect_crash(snake):
    duplicate_in_snake = check_duplicates(snake)
    wall_in_snake = check_for_wall(snake)
    if duplicate_in_snake or wall_in_snake:
        snake_crashed = True
    else:
        snake_crashed = False
    return snake_crashed

def snake_eating(snake, food, direction):
   for i in food:
       if i in snake:
           food.remove(food[0])
           snake_lengthen = True
           refresh_snake(snake, direction, snake_lengthen)
           food.append(random.choice(grid))


def draw_snake(snake):
    for i in snake:
        pygame.draw.ellipse(DISPLAYSURF, YELLOW, (i[0] *CELLSIZE, i[1] * CELLSIZE, CELLSIZE+1, CELLSIZE+1))
        pygame.draw.ellipse(DISPLAYSURF, BRIGHTYELLOW, (i[0] *CELLSIZE, i[1] * CELLSIZE, CELLSIZE-1, CELLSIZE-1))
        pygame.draw.ellipse(DISPLAYSURF, PALEYELLOW, (i[0] *CELLSIZE, i[1] * CELLSIZE, CELLSIZE-4, CELLSIZE-4))


def draw_food(food):
    for i in food:
        pygame.draw.ellipse(DISPLAYSURF, GREEN, ((i[0] *CELLSIZE), (i[1] * CELLSIZE), CELLSIZE+2, CELLSIZE+2))
        pygame.draw.ellipse(DISPLAYSURF, BRIGHTGREEN, (i[0] *CELLSIZE, i[1] * CELLSIZE, CELLSIZE, CELLSIZE))
        pygame.draw.ellipse(DISPLAYSURF, PALEGREEN, (i[0] *CELLSIZE, i[1] * CELLSIZE, CELLSIZE-4, CELLSIZE-4))



main()
