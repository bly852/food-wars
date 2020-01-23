#         course: ICS3U1 2019
#       exercise: Culminating Activity
#           date: 2019-12-06
# student number: 340926187
#           name: Brandon Ly
#    description: Two players (Mr Chun & Mr Pileggi) running around the school
#                 collecting food for the food drive.

# main game script

import pygame
import random
import sys
import time
from pygame.locals import *
from settings import *
from sprites import *
from os import path
from map import *


class Game:
    """
    Game class that contains the entire game
    """

    def __init__(self):
        """
        initialize pygame window when an instance is created
        """
        # initalizes pygame window and name
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("{}".format(title))

        # joystick initialization
        pygame.joystick.init()
        # returns the count of joysticks plugged in

        # initialize player cameras
        self.canvas = pygame.Surface((width, height))
        self.player1_rect = pygame.Rect(0, 0, width / 2, height)
        self.player2_rect = pygame.Rect(width / 2, 0, width / 2, height)
        self.player1_cam = self.canvas.subsurface(self.player1_rect)
        self.player2_cam = self.canvas.subsurface(self.player2_rect)

        # creates a clock to track FPS
        self.fpsClock = pygame.time.Clock()

        # loads game assets
        self.data_loader()

    def data_loader(self):
        """
        loads game assets from folders into memory
        """
        # setting image varaiables
        self.map = Map(path.join(map_folder, 'tdss.txt'))
        self.floor_image = pygame.image.load(path.join(image_folder, floor_image)).convert_alpha()
        self.wall_image = pygame.image.load(path.join(image_folder, wall_image)).convert_alpha()
        self.player1_image = pygame.image.load(path.join(image_folder, player1_image)).convert_alpha()
        self.player2_image = pygame.image.load(path.join(image_folder, player2_image)).convert_alpha()

        # Game over darkening layer
        self.game_over = pygame.image.load(path.join(image_folder, 'Transparent Grey Layer.png')).convert_alpha()

    def draw_text(self, text, font_name, size, colour, x, y, align="topleft"):
        """
        renders and blits the text with a specified font, size, colour, x and
        y coordinate, and alignment in the rectangle
        """
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()

        # text alignment within rect
        if align == "topleft":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)

        # blit text to the screen
        self.screen.blit(text_surface, text_rect)

    def new(self):
        """
        initializes a new game resetting cameras and sprite groups
        """

        # tells the game it is no longer at the spash screen
        self.splashscreen = False

        # sprite groups to organize all sprites
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.students = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.food = pygame.sprite.Group()

        # initializes the camera for the player
        self.camera1 = Camera(self.map.width, self.map.height, 1)
        self.camera2 = Camera(self.map.width, self.map.height, 2)

        # generates walls and floors
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'X':
                    Wall(self, col, row)
                elif tile == '.':
                    Floor(self, col, row)

        # generates initial food sprites
        for x in range((self.map.tileWidth * self.map.tileHeight) // food_spawn_rate):
            Food(self, random.randint(0, self.map.tileWidth),
                 random.randint(0, self.map.tileHeight))

        # generates player sprites
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Floor(self, col, row)
                    self.player1 = Player(self, col, row, 1)
                elif tile == "2":
                    Floor(self, col, row)
                    self.player2 = Player(self, col, row, 2)

    def run(self):
        """
        main game loop
        """
        self.playing = True
        self.elapsed_time = 0
        self.foodTimer = 0
        while self.playing:
            self.dt = self.fpsClock.tick(fps) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        """
        quits pygame and closes the window
        """
        pygame.quit()
        sys.exit()

    def update(self):
        """
        part of the game loop - updates sprites
        """
        self.all_sprites.update()
        self.camera1.update(self.player1)
        self.camera2.update(self.player2)

    def draw(self):
        """
        part of the game loop - draws the new sprite positions and text to the
        screen
        """
        # updates window caption with current FPS
        pygame.display.set_caption(
            "{} | FPS: {:.0f}".format(title, self.fpsClock.get_fps()))

        # wipes both cameras and fills with light grey
        self.player1_cam.fill(lightgrey)
        self.player2_cam.fill(lightgrey)

        # blit all sprites to each players camera
        for sprite in self.all_sprites:
            self.player1_cam.blit(sprite.image, self.camera1.apply(sprite))
        for sprite in self.all_sprites:
            self.player2_cam.blit(sprite.image, self.camera2.apply(sprite))

        # blits both players views onto the main screen
        self.screen.blit(self.player1_cam, (0, 0))
        self.screen.blit(self.player2_cam, (width / 2, 0))

        # draws the screen border
        pygame.draw.rect(self.screen, gui_accent_colour,
                         (0, 0, width, height), 3)

        # draws the GUI base layer
        pygame.draw.line(self.screen, gui_accent_colour,
                         (width / 2, 0), (width / 2, height), 14)
        pygame.draw.rect(self.screen, gui_accent_colour, ((width / 4) - (width / 12) - 2, 0, width - (width / 4) - (width / 12) + 4, 37))
        pygame.draw.line(self.screen, black, (width / 2, 2), (width / 2, height), 10)
        pygame.draw.rect(self.screen, black, ((width / 4) - (width / 12), 2, width - (width / 4) - (width / 12), 33))

        # draws time left to the screen
        self.draw_text('{} seconds left'.format(time_limit - (int(self.elapsed_time))), default_font_bold, 25, white, width / 2, 17, align='center')

        # draws player score to the screen
        self.draw_text('Score: {}'.format(self.player1.score), default_font_bold, 25, white, width / 4, 17, align='center')
        self.draw_text('Score: {}'.format(self.player2.score), default_font_bold, 25, white, width - (width / 4), 17, align='center')

        # flip render to the screen
        pygame.display.flip()

    def events(self):
        """
        part of the game loop - checks for events
        """
        # adds delta time every frame to check
        self.elapsed_time += self.dt
        if self.elapsed_time >= time_limit:
            self.playing = False

        # adds delta time every frame to check how much time has passed since a new food sprite has been spawned
        self.foodTimer += self.dt

        # generates new food sprites based on timer if the amount of food sprites is less than amount of initial food sprites
        if len(self.food) < (self.map.tileWidth * self.map.tileHeight) // food_spawn_rate:
            if self.foodTimer > food_spawn_timer:
                Food(self, random.randint(0, self.map.tileWidth),
                     random.randint(0, self.map.tileHeight))
                self.foodTimer = 0

        # checks for events to exit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.playing = False

    def show_start_screen(self):
        """
        shows the games start screen
        """
        # sets the screen as black
        self.screen.fill(black)

        # draws splash screen text
        self.draw_text('FOOD WARS', default_font_bold, 100, white, width // 2, height // 2 - 100, align='center')
        self.draw_text('WASD to move Mr. Pileggi (Player 1)', default_font_bold, 25, white, width // 2, height // 2 + 25, align='center')
        self.draw_text('Arrow Keys to move Mr. Chun (Player 2)', default_font_bold, 25, white, width // 2, height // 2 + 50, align='center')
        self.draw_text('Pickup food to get points', default_font_bold, 25, white, width // 2, height // 2 + 100, align='center')
        self.draw_text('Press any key to start', default_font_bold, 50, white, width // 2, height // 2 + 175, align='center')

        self.splashscreen = True

        # flips final screen to display
        pygame.display.flip()
        self.wait_for_key()

    def show_game_over(self):
        """
        shows the game over screen with option to play again or quit
        """
        # draws the final screen
        self.draw()

        # covers the final screen in a transparent grey layer
        self.screen.blit(self.game_over, (0, 0))

        # draws the game over screen text
        self.draw_text('GAME OVER', default_font_bold, 100, white, width // 2, height // 2 - 100, align='center')
        if self.player1.score > self.player2.score:
            self.draw_text('Player 1 Wins!', default_font_bold, 50, white, width // 2, height // 2 + 75, align='center')
        elif self.player1.score < self.player2.score:
            self.draw_text('Player 2 Wins!', default_font_bold, 50, white, width // 2, height // 2 + 75, align='center')
        else:
            self.draw_text('It was a tie!', default_font_bold, 50, white, width // 2, height // 2 + 75, align='center')
        self.draw_text('Press Escape to quit the game', default_font_bold, 25, white, width // 2, height // 2 + 150, align='center')
        self.draw_text('Press any other key to play again', default_font_bold, 25, white, width // 2, height // 2 + 175, align='center')

        pygame.display.flip() # flips final screen to the display
        self.wait_for_key() # runs the loop

    def wait_for_key(self):
        """
        game loop that waits at the game over screen
        """
        start_time = time.time()
        pygame.event.clear()
        waiting = True
        while waiting:
            self.fpsClock.tick(fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    waiting = False
                    self.quit()
                # timer to prevent accidental instant replay
                if time.time() - start_time >= 1:
                    # if escape is pressed quit the game, otherwise start a new game
                    if event.type == KEYDOWN:
                        if self.splashscreen == True:
                            waiting = False
                        else:
                            if event.key == K_ESCAPE:
                                self.quit()
                            else:
                                waiting = False


game = Game() # creates an instance of the game
game.show_start_screen() # runs the start screen with instructions
while True:
    game.new() # generates a new level
    game.run() # runs the game loop
    game.show_game_over() # show the game over screen with option to play again
