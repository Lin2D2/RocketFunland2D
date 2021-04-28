import pygame


class Player:
    def __init__(self, image_path, position, parent):
        self.player_image_inital = pygame.image.load(image_path)
        self.player_image = self.player_image_inital
        self.player_image_size_x, self.player_image_size_y = self.player_image.get_size()
        self.position_x = position[0] + (parent.tile_width / 2 - self.player_image_size_x / 2)
        self.position_y = position[1] - (parent.tile_height + 1) * parent.tile_scaling
        self.boundary = pygame.Rect(self.position_x,
                                    self.position_y,
                                    self.player_image.get_size()[0],
                                    self.player_image.get_size()[1]
                                    )
        self.velocity_x = 0
        self.velocity_y = 0
        self.HP = 100
        self.scaling(parent.tile_scaling)

    def set_position(self, x, y):
        self.position_x = x
        self.position_y = y
        # TODO make better
        self.boundary = pygame.Rect(self.position_x,
                                    self.position_y,
                                    self.player_image.get_size()[0],
                                    self.player_image.get_size()[1]
                                    )

    def move(self, x_v, y_v):
        self.position_x += x_v
        self.position_y += y_v
        # TODO make better
        self.boundary = pygame.Rect(self.position_x,
                                    self.position_y,
                                    self.player_image.get_size()[0],
                                    self.player_image.get_size()[1]
                                    )

    def scaling(self, scale):
        self.player_image = pygame.transform.scale(self.player_image_inital,
                                                   (int(self.player_image_size_x * scale + 1),
                                                    int(self.player_image_size_y * scale + 1))
                                                   )
        self.boundary = pygame.Rect(self.position_x,
                                    self.position_y,
                                    self.player_image.get_size()[0],
                                    self.player_image.get_size()[1]
                                    )
