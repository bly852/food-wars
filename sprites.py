#         course: ICS3U1 2019
#       exercise: Culminating Activity
#           date: 2019-12-06
# student number: 340926187
#           name: Brandon Ly
#    description: Two players (Mr Chun & Mr Pileggi) running around the school
#                 collecting food for the food drive.

# sprite classes

import pygame
import random
import math
import os
from settings import *


class Player(pygame.sprite.Sprite):
    """
    player class that contains all data and functions related to the player
    """

    def __init__(self, game, x, y, playerNum):
        """
        initalizes a player sprite when an instance is created in the game
        parameter, at the x and y paramters, and with the player number
        """
        self.playerNum = playerNum
        self.groups = game.all_sprites, game.players
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # image selection for each player
        if self.playerNum == 1:
            self.image = pygame.transform.rotate(self.game.player1_image, 90)
        else:
            self.image = pygame.transform.rotate(self.game.player2_image, 90)
        self.rect = self.image.get_rect()

        # setting the players base movement velocity
        self.velX, self.velY = 0, 0

        # setting the players position on the grid
        self.x = x * tileSize - tileSize
        self.y = y * tileSize - tileSize

        # players starting score
        self.score = 0

        # if joysticks are connected, enable joystick controls for the player
        self.joystick_count = pygame.joystick.get_count()
        if self.joystick_count > 0:
            self.joystick_enabled = True
        else:
            self.joystick_enabled = False

    def get_keys(self):
        """
        checks for all keys pressed and changes the players velocity on that
        axis to the player speed varaiable
        """
        self.velX, self.velY = 0, 0
        keys = pygame.key.get_pressed()

        # player 1 controls
        if self.playerNum == 1:
            if keys[pygame.K_a]:
                self.velX = -player_speed
            if keys[pygame.K_d]:
                self.velX = player_speed
            if keys[pygame.K_w]:
                self.velY = -player_speed
            if keys[pygame.K_s]:
                self.velY = player_speed

        # player 2 controls
        else:
            if keys[pygame.K_LEFT]:
                self.velX = -player_speed
            if keys[pygame.K_RIGHT]:
                self.velX = player_speed
            if keys[pygame.K_UP]:
                self.velY = -player_speed
            if keys[pygame.K_DOWN]:
                self.velY = player_speed

        # if moving diagonally reduce the speed
        if self.velX > 0 and self.velY > 0:
            self.velX = player_speed * 0.701
            self.velY = player_speed * 0.701
        elif self.velX < 0 and self.velY < 0:
            self.velX = player_speed * -0.701
            self.velY = player_speed * -0.701

    def get_joystick_axis(self):
        """
        changes the velocity of the character in the x and y based on joystick
        input
        """
        # joystick controls for two seperate controllers
        if self.joystick_count == 2:
            # joystick control for player 1
            if self.playerNum == 1:
                # joystick initialization
                joystick = pygame.joystick.Joystick(1)
                joystick.init()

                # different joystick settings for Xbox controllers
                if joystick.get_name() == 'Xbox Wireless Controller' or 'Controller (Xbox One For Windows)':
                # checks for axis movement and changes velX and velY
                    if round(joystick.get_axis(0)) != 0 or round(joystick.get_axis(1)) != 0:
                        self.velX += joystick.get_axis(0) * player_speed
                        self.velY += joystick.get_axis(1) * player_speed
                else:
                    if round(joystick.get_axis(1)) != 0 or round(joystick.get_axis(0)) != 0:
                        self.velX += joystick.get_axis(1) * player_speed
                        self.velY -= joystick.get_axis(0) * player_speed

            # joystick control for player 2
            elif self.playerNum == 2:
                # joystick initialization
                joystick = pygame.joystick.Joystick(0)
                joystick.init()

                # Different joystick settings for Xbox controllers
                if joystick.get_name() == 'Xbox Wireless Controller' or 'Controller (Xbox One For Windows)':
                # checks for axis movement and changes velX and velY
                    if round(joystick.get_axis(0)) != 0 or round(joystick.get_axis(1)) != 0:
                        self.velX += joystick.get_axis(0) * player_speed
                        self.velY += joystick.get_axis(1) * player_speed
                else:
                    if round(joystick.get_axis(1)) != 0 or round(joystick.get_axis(0)) != 0:
                        self.velX += joystick.get_axis(1) * player_speed
                        self.velY -= joystick.get_axis(0) * player_speed
        # joystick controls for a single controller
        elif self.joystick_count == 1:
            # joystick control for player 1
            if self.playerNum == 1:
                # joystick initialization
                joystick = pygame.joystick.Joystick(0)
                joystick.init()

                # different joystick settings for Xbox controllers
                if joystick.get_name() == 'Xbox Wireless Controller' or 'Controller (Xbox One For Windows)':
                # checks for axis movement and changes velX and velY
                    if round(joystick.get_axis(0)) != 0 or round(joystick.get_axis(1)) != 0:
                        self.velX += joystick.get_axis(0) * player_speed
                        self.velY += joystick.get_axis(1) * player_speed
                else:
                    if round(joystick.get_axis(1)) != 0 or round(joystick.get_axis(0)) != 0:
                        self.velX += joystick.get_axis(1) * player_speed
                        self.velY -= joystick.get_axis(0) * player_speed

            # joystick control for player 2
            elif self.playerNum == 2:
                # joystick initialization
                joystick = pygame.joystick.Joystick(0)
                joystick.init()

                # different joystick settings for Xbox controllers
                if joystick.get_name() == 'Xbox Wireless Controller' or 'Controller (Xbox One For Windows)':
                # checks for axis movement and changes velX and velY
                    if round(joystick.get_axis(4)) != 0 or round(joystick.get_axis(3)) != 0:
                        self.velX += joystick.get_axis(4) * player_speed
                        self.velY += joystick.get_axis(3) * player_speed
                else:
                    if round(joystick.get_axis(1)) != 0 or round(joystick.get_axis(0)) != 0:
                        self.velX += joystick.get_axis(2) * player_speed
                        self.velY -= joystick.get_axis(3) * player_speed

    def direction(self):
        """
        rotates the player sprite based on the current direction and new
        direction
        """
        # player 1 rotation
        if self.playerNum == 1:
            if self.velX > 100:
                if self.velY < -100:
                    self.image = pygame.transform.rotate(self.game.player1_image, 45)
                elif self.velY > 100:
                    self.image = pygame.transform.rotate(self.game.player1_image, -45)
                else:
                    self.image = pygame.transform.rotate(self.game.player1_image, 0)
            elif self.velX < -100:
                if self.velY < -100:
                    self.image = pygame.transform.rotate(self.game.player1_image, 135)
                elif self.velY > 100:
                    self.image = pygame.transform.rotate(self.game.player1_image, -135)
                else:
                    self.image = pygame.transform.rotate(self.game.player1_image, 180)
            else:
                if self.velY < -100:
                    self.image = pygame.transform.rotate(self.game.player1_image, 90)
                elif self.velY > 100:
                    self.image = pygame.transform.rotate(self.game.player1_image, -90)
        # player 2 rotation
        else:
            if self.velX > 100:
                if self.velY < -100:
                    self.image = pygame.transform.rotate(self.game.player2_image, 45)
                elif self.velY > 100:
                    self.image = pygame.transform.rotate(self.game.player2_image, -45)
                else:
                    self.image = pygame.transform.rotate(self.game.player2_image, 0)
            elif self.velX < -100:
                if self.velY < -100:
                    self.image = pygame.transform.rotate(self.game.player2_image, 135)
                elif self.velY > 100:
                    self.image = pygame.transform.rotate(self.game.player2_image, -135)
                else:
                    self.image = pygame.transform.rotate(self.game.player2_image, 180)
            else:
                if self.velY < -100:
                    self.image = pygame.transform.rotate(self.game.player2_image, 90)
                elif self.velY > 100:
                    self.image = pygame.transform.rotate(self.game.player2_image, -90)

    def wall_collision(self, axis):
        """
        checks for player collision with the all wall sprites on the axis
        given and prevents player movement onto it
        """
        if axis == 'x':
            collides = pygame.sprite.spritecollide(self, self.game.walls, False)
            if collides:
                if self.velX > 0:
                    self.x = collides[0].rect.left - self.rect.width
                if self.velX < 0:
                    self.x = collides[0].rect.right
                self.velX = 0
                self.rect.x = self.x
        if axis == 'y':
            collides = pygame.sprite.spritecollide(self, self.game.walls, False)
            if collides:
                if self.velY > 0:
                    self.y = collides[0].rect.top - self.rect.height
                if self.velY < 0:
                    self.y = collides[0].rect.bottom
                self.velY = 0
                self.rect.y = self.y

    def player_collision(self, axis):
        """
        checks for player collision with the all wall sprites on the axis
        given and prevents player movement onto it
        """
        # checks for player 1 collision to player 2
        if self.playerNum == 1:
            if axis == 'x':
                if self.rect.colliderect(self.game.player2):
                    if self.velX > 0:
                        self.x = self.game.player2.rect.left - self.rect.width
                    if self.velX < 0:
                        self.x = self.game.player2.rect.right
                    self.velX = 0
                    self.rect.x = self.x
            if axis == 'y':
                if self.rect.colliderect(self.game.player2):
                    if self.velY > 0:
                        self.y = self.game.player2.rect.top - self.rect.height
                    if self.velY < 0:
                        self.y = self.game.player2.rect.bottom
                    self.velY = 0
                    self.rect.y = self.y
        # checks for player 2 collision to player 1
        else:
            if axis == 'x':
                if self.rect.colliderect(self.game.player1):
                    if self.velX > 0:
                        self.x = self.game.player1.rect.left - self.rect.width
                    if self.velX < 0:
                        self.x = self.game.player1.rect.right
                    self.velX = 0
                    self.rect.x = self.x
            if axis == 'y':
                if self.rect.colliderect(self.game.player1):
                    if self.velY > 0:
                        self.y = self.game.player1.rect.top - self.rect.height
                    if self.velY < 0:
                        self.y = self.game.player1.rect.bottom
                    self.velY = 0
                    self.rect.y = self.y

    def food_collision(self):
        """
        checks for player collision with all food sprites killing any sprites it comes collides with and adding 1 to the players score value
        """
        collides = pygame.sprite.spritecollide(self, self.game.food, True)
        if collides:
            self.score += 1

    def update(self):
        """
        updates the players position
        """
        self.get_keys()
        if self.joystick_enabled == True:
            self.get_joystick_axis()
        self.direction()
        self.x += self.velX * self.game.dt
        self.y += self.velY * self.game.dt
        self.rect.x = self.x
        self.wall_collision('x')
        self.player_collision('x')
        self.rect.y = self.y
        self.wall_collision('y')
        self.player_collision('y')
        self.food_collision()


class Student(pygame.sprite.Sprite):
    """
    class to contain all the data for student AI sprites
    """
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.students
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pygame.image.load(os.path.join(image_folder, (random.choice(student_images))))

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tileSize
        self.rect.y = y * tileSize


class Wall(pygame.sprite.Sprite):
    """
    class to contain all the data for wall sprites
    """

    def __init__(self, game, x, y):
        """
        initalizes a wall sprite when an instance is create in the game
        parameter, at the x and y paramters
        """
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tileSize
        self.rect.y = y * tileSize


class Floor(pygame.sprite.Sprite):
    """
    class to contain all the data for floor sprites
    """

    def __init__(self, game, x, y):
        """
        initalizes a floor sprite when an instance is created in the game
        parameter, at the x and y paramters
        """
        self.groups = game.all_sprites, game.floor
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.floor_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tileSize
        self.rect.y = y * tileSize


class Food(pygame.sprite.Sprite):
    """
    class to contain all the data for food sprites
    """

    def __init__(self, game, x, y):
        """
        initalizes a food sprite when an instance is created in the game
        parameter, at the x and y paramters
        """
        self.groups = game.all_sprites, game.food
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # picks random image for the sprite
        self.image = pygame.image.load(os.path.join(food_folder, (random.choice(food_images)))).convert_alpha()

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tileSize
        self.rect.y = y * tileSize

        # checks if the sprite is allowed to spawn in the x and y
        self.spawnable = False
        collided = pygame.sprite.spritecollide(self, self.game.floor, False)
        for sprite in collided:
            if self.x == sprite.x and self.y == sprite.y:
                self.spawnable = True
        if self.spawnable == False:
            self.kill()
