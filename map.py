#         course: ICS3U1 2019
#       exercise: Culminating Activity
#           date: 2019-12-06
# student number: 340926187
#           name: Brandon Ly
#    description: Two players (Mr Chun & Mr Pileggi) running around the school
#                 collecting food for the food drive.

# map and camera classes

import pygame
from settings import *


class Map:
    """
    class to contain the map reader
    """

    def __init__(self, filename):
        """
        initializes and reads the map based of the text
        file at the filename parameter
        """
        self.data = []
        with open(filename, 'rt') as level:
            for line in level:
                self.data.append(line.strip())

        self.tileWidth = len(self.data[0])
        self.tileHeight = len(self.data)
        self.width = self.tileWidth * tileSize
        self.height = self.tileHeight * tileSize


class Camera:
    """
    class to contain the games camera
    """

    def __init__(self, cam_width, cam_height, camNum):
        """
        initializes a camera based on the cam_width
        and cam_height parameters
        """
        self.camera = pygame.Rect(0, 0, width/2, height)
        self.width = cam_width
        self.height = cam_height

    def apply(self, entity):
        """
        returns the camera movement to the entity parameter
        """
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        """
        updates the camera based on the target parameter's movement
        """
        x = -target.rect.x + int(width / 4)
        y = -target.rect.y + int(height / 2)

        # camera limits
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - width/2), x)
        y = max(-(self.height - height), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)
