import pygame


class Player:
    def __init__(self, position, parent):
        self.image_inital = pygame.image.load("textures/Player.png")
        self.image = self.image_inital
        self.image_size_x, self.image_size_y = self.image.get_size()
        position_x = position[0] + (parent.tile_width / 2 - self.image_size_x / 2)
        position_y = position[1] - (parent.tile_height + 1) * parent.tile_scaling
        self.boundary_rect = pygame.Rect(position_x,
                                         position_y,
                                         self.image.get_size()[0],
                                         self.image.get_size()[1]
                                         )
        self.velocity_x = 0
        self.reduce_velocity_x = True
        self.velocity_y = 0
        self.in_air = False
        self.HP = 100
        self.scaling(parent.tile_scaling)

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
