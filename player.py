import pygame


class Player:
    def __init__(self, image_path, position, parent):
        self.player_image_inital = pygame.image.load(image_path)
        self.player_image = self.player_image_inital
        self.player_image_size_x, self.player_image_size_y = self.player_image.get_size()
        position_x = position[0] + (parent.tile_width / 2 - self.player_image_size_x / 2)
        position_y = position[1] - (parent.tile_height + 1) * parent.tile_scaling
        self.boundary_rect = pygame.Rect(position_x,
                                         position_y,
                                         self.player_image.get_size()[0],
                                         self.player_image.get_size()[1]
                                         )
        self.velocity_x = 0
        self.reduce_velocity_x = True
        self.velocity_y = 0
        self.in_air = False
        self.HP = 100
        self.scaling(parent.tile_scaling)

    def move(self, x_v, y_v):
        self.boundary_rect.x += x_v
        self.boundary_rect.y += y_v

    def scaling(self, scale):
        self.player_image = pygame.transform.scale(self.player_image_inital,
                                                   (int(self.player_image_size_x * scale + 1),
                                                    int(self.player_image_size_y * scale + 1))
                                                   )
        self.boundary_rect = pygame.Rect(self.boundary_rect.x,
                                         self.boundary_rect.y,
                                         self.player_image.get_size()[0],
                                         self.player_image.get_size()[1]
                                         )
