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

WINDOWWIDTH = 640
WINDOWHEIGHT = 480

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

   snake = []
   snake_start_pos = random.choice(grid)
 
   food = []
   food_start_pos = random.choice(grid)

   FPSCLOCK = pygame.time.Clock()
   pygame.display.set_caption('python-python!')
   BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
   food.append(food_start_pos)
   snake.append(snake_start_pos)
   direction = random.choice((UP, DOWN, LEFT, RIGHT))
   new_direction = direction
   snake_crashed = False

   while True == True: #main game loop
       DISPLAYSURF.fill(BLACK)
       draw_food(food)
       check_for_quit()
       new_direction = change_direction(new_direction)
       snake = refresh_snake(snake, new_direction)
       snake_crashed = detect_crash(snake)
       if snake_crashed == True:
           quit()
       snake_eating(snake, food, new_direction)
       pygame.display.update()
       FPSCLOCK.tick(12)

def quit():
    pygame.quit()
    sys.exit()

def check_for_quit():
    for event in pygame.event.get(QUIT):
        quit()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            quit()
        pygame.event.post(event)

def change_direction(direction):
    for event in pygame.event.get():
        if event.type == KEYUP: # this is here so that KEYDOWN events are handled. otherwise,
                                # they will eventually render the snake unresponsive, and
                                # it will crash into a wall as the gamer looks on in anguish.
            pygame.event.post(event)
    for event in pygame.event.get(KEYUP):
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

def add_snake_tail(old_snake_head, move_dir):
    if move_dir == UP:
        new_snake_tail = (old_snake_head[0], old_snake_head[1]-MOVESPEED-1)
    elif move_dir == DOWN:
        new_snake_tail = (old_snake_head[0], old_snake_head[1]+MOVESPEED+1)
    elif move_dir == LEFT:
        new_snake_tail = (old_snake_head[0]-MOVESPEED-1, old_snake_head[1])
    elif move_dir == RIGHT:
        new_snake_tail = (old_snake_head[0]+MOVESPEED+1, old_snake_head[1])
    return new_snake_tail



def refresh_snake(snake, direction):
    new_snake_head = add_snake_head(snake[-1], direction)
    snake.append(new_snake_head)
    snake.remove(snake[0])
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
        if i[0] >= COLUMNS or i[0] <= 0 or i[1] >= ROWS or i[1] <= 0:
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
           snake_lengthen(snake, direction)
           food.append(random.choice(grid))

def snake_lengthen(snake, direction):
    new_snake_tail = add_snake_tail(snake[0], direction)
    snake.insert(0,new_snake_tail)
    draw_snake(snake)


def draw_snake(snake):
    for i in snake:
        pygame.draw.rect(DISPLAYSURF, YELLOW, (i[0] *CELLSIZE, i[1] * CELLSIZE, CELLSIZE, CELLSIZE))

def draw_food(food):
    for i in food:
        pygame.draw.rect(DISPLAYSURF, GREEN, (i[0] *CELLSIZE, i[1] * CELLSIZE, CELLSIZE, CELLSIZE))

main()
