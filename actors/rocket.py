import pygame
import math


def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))


def length(v):
  return math.sqrt(dotproduct(v, v))


def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


class Rocket:
    def __init__(self, position, direction, parent):
        self.image_inital = pygame.image.load("textures/Rocket.png")
        self.image = self.image_inital
        self.image_size_x, self.image_size_y = self.image_inital.get_size()
        self.position = position
        position_x = position[0]
        position_y = position[1]
        self.boundary_rect = pygame.Rect((position_x, position_y), (self.image_size_x, self.image_size_y))
        self.scaling(parent.tile_scaling)
        self.image = pygame.transform.rotate(self.image, angle(self.position, (1, 1)))  # TODO fix rotation
        v = 2
        self.velocity_x = direction[0] * v
        self.velocity_y = direction[1] * v

    def scaling(self, scale):
        self.image = pygame.transform.scale(self.image_inital,
                                            (int(self.image_size_x * scale + 1),
                                                    int(self.image_size_y * scale + 1))
                                            )
        self.boundary_rect = pygame.Rect(self.boundary_rect.x,
                                         self.boundary_rect.y,
                                         self.image.get_size()[0],
                                         self.image.get_size()[1]
                                         )
