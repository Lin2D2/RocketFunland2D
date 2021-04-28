import pygame


class Player:
    def __init__(self, image_path, position, parent):
        self.player_image_inital = pygame.image.load(image_path)
        self.player_image = self.player_image_inital
        self.player_image_size_x, self.player_image_size_y = self.player_image.get_size()
        self.boundary = self.player_image.get_rect()
        self.position = (position[0]+(parent.tile_width/2-self.player_image_size_x/2),
                         position[1] - (parent.tile_height + 1) * parent.tile_scaling)
        self.velocity = tuple()
        self.HP = 100
        self.scaling(parent.tile_scaling)

    def scaling(self, scale):
        self.player_image = pygame.transform.scale(self.player_image_inital,
                                                   (int(self.player_image_size_x * scale + 1),
                                                    int(self.player_image_size_y * scale + 1))
                                                   )
