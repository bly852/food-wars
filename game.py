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
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("{}".format(title))

        # joystick initialization
        pygame.joystick.init()
        # returns the count of joysticks plugged in

        # initialize player cameras
        self.canvas = pygame.Surface((self.screen_width, self.screen_height))
        self.player1_rect = pygame.Rect(0, 0, self.screen_width / 2, self.screen_height)
        self.player2_rect = pygame.Rect(self.screen_width / 2, 0, self.screen_width / 2, self.screen_height)
        self.player1_cam = self.canvas.subsurface(self.player1_rect)
        self.player2_cam = self.canvas.subsurface(self.player2_rect)

        # creates a clock to track FPS
        self.fpsClock = pygame.time.Clock()
        self.dt = self.fpsClock.tick(fps) / 1000
        self.elapsed_time = 0

        # loads game assets
        self.data_loader()

    def data_loader(self):
        """
        loads game assets from folders into memory
        """
        # setting image varaiables
        self.map = Map(path.join(map_folder, map))
        self.floor_image = pygame.image.load(path.join(image_folder, floor_image)).convert_alpha()
        self.wall_image = pygame.image.load(path.join(image_folder, wall_image)).convert_alpha()
        self.player1_image = pygame.image.load(path.join(image_folder, player1_image)).convert_alpha()
        self.player2_image = pygame.image.load(path.join(image_folder, player2_image)).convert_alpha()
        self.default_font_bold = path.join(font_folder, default_font_bold)

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
        # sprite groups to organize all sprites
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.students = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.floor = pygame.sprite.Group()
        self.food = pygame.sprite.Group()

        # initializes the camera for the player
        self.camera1 = Camera(self.map.width, self.map.height, 1, self.screen_width, self.screen_height)
        self.camera2 = Camera(self.map.width, self.map.height, 2, self.screen_width, self.screen_height)

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

        # spawns players at a random spot on the map
        while len(self.players) < 2:
            for row, tiles in enumerate(self.map.data):
                 for col, tile in enumerate(tiles):
                     if tile == '.':
                         if len(self.players) == 2:
                             break
                         elif len(self.players) < 1:
                             if random.randint(spawn_chance, 10000) == 1:
                                 self.player1 = Player(self, col, row, 1)
                         else:
                             if random.randint(spawn_chance, 10000) == 2:
                                 self.player2 = Player(self, col, row, 2)

    def run(self):
        """
        main game loop
        """
        self.splashscreen = False # Tells the game it is no longer at splash screen
        self.playing = True
        self.elapsed_time = 0
        self.foodTimer = 0
        while self.playing:
            self.dt = self.fpsClock.tick(fps) / 1000
            self.events()
            self.update()
            self.draw()
            pygame.display.flip()

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
        self.screen.blit(self.player2_cam, (self.screen_width / 2, 0))

        # draws the screen border
        pygame.draw.rect(self.screen, gui_accent_colour,
                         (0, 0, self.screen_width, self.screen_height), 3)

        # draws the GUI base layer
        pygame.draw.line(self.screen, gui_accent_colour,
                         (self.screen_width / 2, 0), (self.screen_width / 2, self.screen_height), 14)
        pygame.draw.rect(self.screen, gui_accent_colour, ((self.screen_width / 4) - (self.screen_width / 12) - 2, 0, self.screen_width - (self.screen_width / 4) - (self.screen_width / 12) + 4, 37))
        pygame.draw.line(self.screen, black, (self.screen_width / 2, 2), (self.screen_width / 2, self.screen_height), 10)
        pygame.draw.rect(self.screen, black, ((self.screen_width / 4) - (self.screen_width / 12), 2, self.screen_width - (self.screen_width / 4) - (self.screen_width / 12), 33))

        # updates window caption with current FPS
        pygame.display.set_caption(
            "{} | FPS: {:.0f}".format(title, self.fpsClock.get_fps()))

        # draws time left to the screen
        time_left = round((time_limit - self.elapsed_time), 2)
        # draws Times up when the timer is finished
        if time_left <= 0:
            self.draw_text("Time's Up!", self.default_font_bold, 25, red, self.screen_width / 2, 17, align='center')
        # draws the timer in red when it is under 10
        elif time_left < 10:
            # adds a 0 to the end of the time when less than 3 digits (e.g. 1.3)
            if len(str(time_left)) == 3:
                time_left = str(time_left) + '0'
            self.draw_text('{} seconds left'.format(time_left), self.default_font_bold, 25, red, self.screen_width / 2, 17, align='center')
        # draws the timer to the nearest tenth decimal
        else:
            self.draw_text('{} seconds left'.format(round(time_left, 1)), self.default_font_bold, 25, white, self.screen_width / 2, 17, align='center')

        # draws player score to the screen
        self.draw_text('Score: {}'.format(self.player1.score), self.default_font_bold, 25, white, self.screen_width / 4, 17, align='center')
        self.draw_text('Score: {}'.format(self.player2.score), self.default_font_bold, 25, white, self.screen_width - (self.screen_width / 4), 17, align='center')

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
        # tells the game rest of the game that it is at splashscreen
        self.splashscreen = True

        # creates a new game instance and fills the background with it
        self.new()
        self.draw()

        # covers the screen in a transparent grey layer
        self.screen.blit(self.game_over, (0, 0))

        waiting = True
        self.click = False
        while waiting:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                else:
                    self.click = False

            mx, my = pygame.mouse.get_pos()

            # draws splash screen buttons
            play_button = pygame.Rect(self.screen_width/2 - self.screen_width/16, self.screen_height/2 - 150, self.screen_width/8, self.screen_height/16)
            quit_button = pygame.Rect(self.screen_width/2 - self.screen_width/16, self.screen_height/2 + 150, self.screen_width/8, self.screen_height/16)
            if play_button.collidepoint((mx, my)):
                if self.click:
                    waiting = False
                else:
                    pygame.draw.rect(self.screen, black, play_button)
                    self.draw_text("Play", self.default_font_bold, 40, white, self.screen_width/2, self.screen_height/2 - 135, align="center")
            else:
                pygame.draw.rect(self.screen, white, play_button)
                self.draw_text("Play", self.default_font_bold, 40, black, self.screen_width/2, self.screen_height/2 - 135, align="center")
            if quit_button.collidepoint((mx, my)):
                if self.click:
                    self.quit()
                else:
                    pygame.draw.rect(self.screen, black, quit_button)
                    self.draw_text("Quit", self.default_font_bold, 40, white, self.screen_width/2, self.screen_height/2 + 170, align="center")
            else:
                pygame.draw.rect(self.screen, white, quit_button)
                self.draw_text("Quit", self.default_font_bold, 40, black, self.screen_width/2, self.screen_height/2 + 170, align="center")

            self.fpsClock.tick(fps)
            pygame.display.flip()

    def show_game_over(self):
        """
        shows the game over screen with option to play again or quit
        """
        # draws the final screen
        self.draw()

        # covers the final screen in a transparent grey layer
        self.screen.blit(self.game_over, (0, 0))

        # draws the game over screen text
        self.draw_text('GAME OVER', self.default_font_bold, 100, white, self.screen_width // 2, self.screen_height // 2 - 100, align='center')
        if self.player1.score > self.player2.score:
            self.draw_text('Player 1 Wins!', self.default_font_bold, 50, white, self.screen_width // 2, self.screen_height // 2 + 75, align='center')
        elif self.player1.score < self.player2.score:
            self.draw_text('Player 2 Wins!', self.default_font_bold, 50, white, self.screen_width // 2, self.screen_height // 2 + 75, align='center')
        elif self.player1.score == self.player2.score:
            self.draw_text('It was a tie!', self.default_font_bold, 50, white, self.screen_width // 2, self.screen_height // 2 + 75, align='center')
        else:
            self.draw_text('Did you even try?', self.default_font_bold, 50, white, self.screen_width // 2, self.screen_height // 2 + 75, align='center')


        waiting = True
        main_menu = False
        self.click = False
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                else:
                    self.click = False

            mx, my = pygame.mouse.get_pos()

            # draws splash screen buttons
            play_button = pygame.Rect(self.screen_width/2 - self.screen_width/16, self.screen_height/2 + 140, self.screen_width/8, self.screen_height/24)
            main_menu_button = pygame.Rect(self.screen_width/2 - self.screen_width/16, self.screen_height/2 + 170, self.screen_width/8, self.screen_height/24)

            if play_button.collidepoint((mx, my)):
                if self.click:
                    waiting = False
                else:
                    pygame.draw.rect(self.screen, black, play_button)
                    self.draw_text('Play Again', self.default_font_bold, 25, white, self.screen_width // 2, self.screen_height // 2 + 150, align='center')
            else:
                pygame.draw.rect(self.screen, white, play_button)
                self.draw_text('Play Again', self.default_font_bold, 25, black, self.screen_width // 2, self.screen_height // 2 + 150, align='center')

            if main_menu_button.collidepoint((mx, my)):
                if self.click:
                    main_menu = True
                    waiting = False
                else:
                    pygame.draw.rect(self.screen, black, main_menu_button)
                    self.draw_text('Main Menu', self.default_font_bold, 25, white, self.screen_width // 2, self.screen_height // 2 + 180, align='center')
            else:
                pygame.draw.rect(self.screen, white, main_menu_button)
                self.draw_text('Main Menu', self.default_font_bold, 25, black, self.screen_width // 2, self.screen_height // 2 + 180, align='center')




            self.fpsClock.tick(fps)
            pygame.display.flip()

        if main_menu:
            self.show_start_screen()

    def countdown(self):
        start_time = time.time()
        counting = True
        self.update()
        while counting:
            self.draw()
            self.screen.blit(self.game_over, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()

            if time.time() - start_time <= 1:
                # player 1 countdown
                self.draw_text('3', self.default_font_bold, 250, white, self.screen_width/4, self.screen_height/2, align='center')

                # player 2 countdown
                self.draw_text('3', self.default_font_bold, 250, white, self.screen_width-(self.screen_width/4), self.screen_height/2, align='center')

            elif time.time() - start_time <=2:
                # player 1 countdown
                self.draw_text('2', self.default_font_bold, 250, white, self.screen_width/4, self.screen_height/2, align='center')

                # player 2 countdown
                self.draw_text('2', self.default_font_bold, 250, white, self.screen_width-(self.screen_width/4), self.screen_height/2, align='center')

            elif time.time() - start_time <=3:
                # player 1 countdown
                self.draw_text('1', self.default_font_bold, 250, white, self.screen_width/4, self.screen_height/2, align='center')

                # player 2 countdown
                self.draw_text('1', self.default_font_bold, 250, white, self.screen_width-(self.screen_width/4), self.screen_height/2, align='center')

            elif time.time() - start_time >=3:
                counting = False
            pygame.display.flip()


game = Game() # creates an instance of the game
game.show_start_screen() # runs the start screen with instructions
while True:
    game.new() # generates a new level
    game.countdown() # runs countdown timer before game starts
    game.run() # runs the game loop
    game.show_game_over() # show the game over screen with option to play again
