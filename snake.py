import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# * This is the classic game known as Snake. This project has given me a better understanding of pygame as well as a little bit of lambda functions, OOP and tkinter.

# TODO: Add sounds, give player the option to change the size of the board, and look into adding fun powerups that give the snake various abilities (extra lives, invincibility, etc.)

# Each individual piece of the snake is a cube object


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows   # this is the height/width of each cube
        i = self.pos[0]             # this is the current row
        j = self.pos[1]             # current column

        # this draws the rectangles in their appropriate locations
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        if eyes:                # if the eyes parameter is true, this function draws the eyes on the head of the snake
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

# The entire snake is represented in the snake class. Cube objects are part of the snake object.


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        # this is the head of the snake, which is always at the front
        self.head = cube(pos)
        self.body.append(self.head)  # this adds the head to the body list
        # dirnx and dirny represent the direction the snake is facing.
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # if the close window button is pressed, pygame quits
                pygame.quit()

            keys = pygame.key.get_pressed()   # gets the state of all pressed keys

            for key in keys:                  # when looping through the pressed keys, -1 indicates left, 1 indicates right, 1 indicates down, and -1 indicates up
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # loops through every cube in the snake's body
        for i, c in enumerate(self.body):
            # this stores the cube's position on the grid
            p = c.pos[:]
            if p in self.turns:
                # if the cube's current position is at a spot we turned, this gets the direction it should turn
                turn = self.turns[p]
                # this actually moves the cube in that direction
                c.move(turn[0], turn[1])
                # if this is the last cube in the body, it is removed from the dict
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:  # if the cube hasn't reached a turning point, the if/elif conditions below check whether it has hit the edge of the screen. If so, we make it appear on the opposite side.
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:       # if none of the above conditions apply, it continues moving in the current direction
                    c.move(c.dirnx, c.dirny)

    # the reset function resets the snake so we can replay
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # the code below which side to add the cube to
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        # the cube's direction is then set to the direction of the snake
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                # for the first cube in the list, the head, eyes need to be drawn. Adding true as the argument tells the draw function to draw eyes
                c.draw(surface, True)
            else:
                # else, it will simply draw a normal cube
                c.draw(surface)

# this function actually draws the grid on the screen


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows      # gives the distance between lines

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        # this draws the vertical lines
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        # this draws the horizontal lines
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

# redrawWindow updates the display


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))  # fills the screen in with a solid black colour
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)  # draws in the grid lines
    pygame.display.update()        # updates the screen

# randomSnack simply draws the snack on a random part of the grid


def randomSnack(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # this ensures that the snack doesn't spawn inside the snake's body
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)

# this is the message box that pops up when the game is lost


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500     # width of the screen
    rows = 20       # rows on the screen
    # this is the screen/surface being worked on
    win = pygame.display.set_mode((width, width))
    # this creates & gives the snake a red color and starts it in the exact middle (10,10)
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()   # this creates the clock

    while flag:
        # this sets a delay of 50 milliseconds before the loop continues
        pygame.time.delay(50)
        # this ensures the snake doesn't move faster than 10fps.
        clock.tick(10)
        s.move()
        # checks if the head collides with the snack, if so it adds a new cube to the end of the snake
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(
                0, 255, 0))   # creates a new snack object

        # this checks if the snake has collided with itself, if so, it ends the game
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10, 10))
                break

        redrawWindow(win)


main()
