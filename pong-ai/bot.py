import pygame as pg

import pandas as pd
import numpy as np

from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

###################### MODEL ######################

# KNeighborsRegressor and StandardScaler were used after analysis in data-analysis.ipynb

play_data = pd.read_csv('game_data.csv')
play_data.drop_duplicates()

bot = KNeighborsRegressor(n_neighbors = 3)
scaler = StandardScaler()

X = play_data[[play_data.columns[0], play_data.columns[1], play_data.columns[2], play_data.columns[3]]]
y = play_data[play_data.columns[4]]

X = scaler.fit_transform(X)

bot.fit(X, y)

###################### GAME ######################

# constants

WIDTH = 1200
HEIGHT = 600
BORDER = 20
VELOCITY = 1

# my colours

bg_colour = pg.color.Color('black')  # background colour
fg_colour = pg.color.Color('green')  # foreground colour
ball_colour = pg.color.Color('green')  # ball colour
paddle_colour = pg.color.Color('green')  # paddle colour

# temp variables
running = True

# screen for the game
screen = pg.display.set_mode((WIDTH, HEIGHT))

# refresh function
def refresh():
    pg.display.flip()

# classes

class Ball:

    # radius of the ball
    RADIUS = 20

    # positions
    X = 0
    Y = 0

    # velocities
    velX = 0
    velY = 0

    # constructor
    def __init__(self, x, y, velX_ = 1, velY_ = 1):

        # positions

        self.X = x
        self.Y = y

        # velocities

        self.velX = velX_
        self.velY = velY_


    # shows the ball

    def show(self, surface = screen, colour = ball_colour):
        pg.draw.circle(surface, colour, (self.X, self.Y), Ball.RADIUS)

    # updates the position

    def update(self):
        newX = self.X + self.velX
        newY = self.Y + self.velY

        # checks if paddle has hit ball
        if newX > WIDTH - BORDER and paddle.Y < newY < paddle.Y + paddle.HEIGHT:
            self.velX = -self.velX
        else:
            pass

        # collisions with walls

        if newX < BORDER + self.RADIUS:
            self.velX = -self.velX
        elif newY < BORDER + self.RADIUS or newY > HEIGHT - BORDER - self.RADIUS:
            self.velY = -self.velY
        else:
            self.show(colour = bg_colour)

            self.X += self.velX
            self.Y += self.velY

            self.show(colour = ball_colour)


class Paddle:

    # dimensions

    WIDTH = 20
    HEIGHT = 200

    # positions
    Y = 0
    
    # constructor
    def __init__(self, y):
        self.Y = y

    # shows the paddle
    def show(self, surface = screen, colour = paddle_colour):
        pg.draw.rect(screen, colour, pg.Rect((WIDTH - self.WIDTH, int(self.Y)), ((self.HEIGHT // 2), self.HEIGHT)))

    # updates the position based on mouse position
    def update(self, newY = pg.mouse.get_pos()[1]):
        self.show(colour = bg_colour)
        self.Y = newY
        self.show(colour = paddle_colour)


# objects

ball = Ball(WIDTH - Ball.RADIUS, HEIGHT // 2, -VELOCITY, -VELOCITY)
paddle = Paddle(HEIGHT // 2)

# main

# draws borders

pg.draw.rect(screen, fg_colour, pg.Rect((0, 0), (WIDTH, BORDER)))
pg.draw.rect(screen, fg_colour, pg.Rect((0, 0), (BORDER, HEIGHT)))
pg.draw.rect(screen, fg_colour, pg.Rect((0, HEIGHT - BORDER), (WIDTH, BORDER)))

# keeps the window open until process is ended
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # predicts paddle.Y with current data
    predicted_Y = bot.predict(scaler.transform([[ball.X, ball.Y, ball.velX, ball.velY]]))

    ball.update()
    paddle.update(newY = predicted_Y)

    refresh()

pg.quit()

