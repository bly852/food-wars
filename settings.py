#         course: ICS3U1 2019
#       exercise: Culminating Activity
#           date: 2019-12-06
# student number: 340926187
#           name: Brandon Ly
#    description: Two players (Mr Chun & Mr Pileggi) running around the school
#                 collecting food for the food drive.

# game variables and settings

import os

# colours
blue = (66, 144, 245)
red = (247, 59, 49)
green = (62, 247, 49)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)
lightgrey = (100, 100, 100)


# game options
width, height = 1280, 720
fps = 120  # fps limit
title = 'Food Wars'
time_limit = 60  # game time limit in seconds
gui_accent_colour = green


# tiles
tileSize = 32
gridWidth = width / tileSize
gridHeight = height / tileSize


# player settings
player_speed = 500
spawn_chance = 1 # percentage chance of player spawn on a tile sprite


# folders | loads the paths to the game folders
game_folder = os.path.dirname(__file__)
image_folder = os.path.join(game_folder, 'images')
food_folder = os.path.join(image_folder, 'food')
map_folder = os.path.join(game_folder, 'maps')
font_folder = os.path.join(game_folder, 'fonts')
map = 'tdss.txt'

# images
player1_image = 'hitman1_hold.png'
player2_image = 'manBlue_hold.png'
floor_image = 'brick_floor32x32.png'
wall_image = 'mask_32x_0.png'
food_images = ['baconcheeseburger1.png', 'bakedziti1.png', 'beanbun1.png', 'blackdragonroll1.png', 'newyorkstrip1.png', 'supreme1.png', 'wedgesalad1.png']
student_images = ['blue_student.png', 'green_student.png', 'orange_student.png', 'pink_student.png', 'red_student.png', 'yellow_student.png', ]


# food settings
food_spawn_rate = 30  # lower number = more food
food_spawn_timer = 0.1  # seconds between food spawn


# text settings
default_font = 'Segoe UI.ttf'
default_font_bold = 'Segoe_UI_Bold.ttf'
