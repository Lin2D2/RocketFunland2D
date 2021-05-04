import pygame
import json
import colorama
import random
import math

from time import time
from actors.player import Player
from actors.rocket import Rocket


class Game:
    def __init__(self):
        pygame.init()
        colorama.init()
        self.running = True

        # Color
        self.color_red = pygame.Color("red")
        self.color_white = pygame.Color("white")
        self.color_black = pygame.Color("black")
        self.darkslate_gray = pygame.Color("darkslategray1")
        self.color_green = pygame.Color("green")
        self.color_yellow = pygame.Color("yellow")

        # clock
        self.screen_clock = pygame.time.Clock()
        self.tick_rate = 60

        # screen
        self.screen = pygame.display.set_mode([1080, 720], pygame.RESIZABLE)
        self.SW = self.screen.get_width()
        self.SH = self.screen.get_height()
        self.background_color = self.color_black

        # Tile and Map
        with open("textures/RocketFunlandMap.json") as map_json:
            map_dict = json.load(map_json)
        self.tile_height = map_dict["tileheight"]
        self.tile_width = map_dict["tilewidth"]
        self.map_height = map_dict["height"]
        self.map_width = map_dict["width"]
        self.map_placment_list = map_dict["layers"][0]["data"]

        self.non_collision_tile = [0]  # maybe find better solution

        self.map = []
        self.spawn_tiles = []
        element = 0
        line = 0
        for tile in self.map_placment_list:
            if element == 0:
                self.map.append([tile - 1])
            else:
                self.map[line].append(tile - 1)  # -1 because latter used as index
            # spawn points
            if tile - 1 == 1:
                self.spawn_tiles.append((element, line))

            if element == self.map_width - 1:
                line += 1
                element = 0
            else:
                element += 1

        # textures collisions
        self.map_collison = []
        for y_pos, row in enumerate(self.map):
            for x_pos, tile in enumerate(row):
                if tile not in self.non_collision_tile:
                    if y_pos > 0:
                        if self.map[y_pos - 1][x_pos] in self.non_collision_tile \
                                and (x_pos, y_pos) not in self.map_collison:
                            self.map_collison.append((x_pos, y_pos))
                    if y_pos < self.map_height - 1:
                        if self.map[y_pos + 1][x_pos] in self.non_collision_tile \
                                and (x_pos, y_pos) not in self.map_collison:
                            self.map_collison.append((x_pos, y_pos))
                    if x_pos > 0:
                        if self.map[y_pos][x_pos - 1] in self.non_collision_tile \
                                and (x_pos, y_pos) not in self.map_collison:
                            self.map_collison.append((x_pos, y_pos))
                    if x_pos < self.map_width - 1:
                        if self.map[y_pos][x_pos + 1] in self.non_collision_tile \
                                and (x_pos, y_pos) not in self.map_collison:
                            self.map_collison.append((x_pos, y_pos))

        # scaling of th map
        self.importend_tile_height = 13
        self.importend_tile_width = 23
        self.importend_tile_pixel_height = self.importend_tile_height * self.tile_height
        self.importend_tile_pixel_width = self.importend_tile_width * self.tile_width
        self.scaled_tile_size = 0
        self.tile_scaling = 0
        self.x_offset = 0
        self.y_offset = 0
        self.tile_table = []
        self.map_collison_rects_reduced = []
        self.change_scalling(start=True)

        # # debugging draw textures to console
        # for row in self.map:
        #     row_list = []
        #     for e in row:
        #         if e < 10:
        #             row_list.append("0" + str(e))
        #         else:
        #             row_list.append(str(e))
        #     print(row_list)

        # Player
        self.spawn_position = self.spawn_tiles[random.randint(0, 3)]
        self.spawn_position = (self.spawn_position[0] * self.scaled_tile_size + self.x_offset / 2 -
                               (self.map_width - self.importend_tile_width) * self.scaled_tile_size / 2,
                               self.spawn_position[1] * self.scaled_tile_size + self.y_offset / 2 -
                               (self.map_height - self.importend_tile_height + 2) * self.scaled_tile_size / 2)
        self.player = Player((self.spawn_position[0], self.spawn_position[1]), self)

        self.rockets = []

        # Buttons
        #

    def start(self):
        self.screen.fill(self.background_color)
        pygame.display.update()
        try:
            self.game_loop()
        except pygame.error as error:
            print(f'error: {error}')

    @staticmethod
    def load_tile_table(file_path, width, height, scaled_tile_size):
        texture = pygame.image.load(file_path).convert()
        texture_width, texture_height = texture.get_size()
        tile_table = []
        for tile_y in range(0, int(texture_height / height)):
            for tile_x in range(0, int(texture_width / width)):
                rect = (tile_x * width, tile_y * height, width, height)
                tile_table.append(
                    pygame.transform.scale(texture.subsurface(rect),
                                           (scaled_tile_size, scaled_tile_size)))
        return tile_table

    def change_scalling(self, start=False):
        # scaling
        scale_height = self.SH / self.importend_tile_pixel_height
        scale_width = self.SW / self.importend_tile_pixel_width
        if scale_width < scale_height:
            self.scaled_tile_size = int(scale_width * self.tile_width)
            self.tile_scaling = scale_width
        else:
            self.scaled_tile_size = int(scale_height * self.tile_height)
            self.tile_scaling = scale_height
        self.x_offset = self.SW - self.importend_tile_width * self.scaled_tile_size
        self.y_offset = self.SH - self.importend_tile_height * self.scaled_tile_size
        if not start:
            # Player
            self.spawn_position = self.spawn_tiles[random.randint(0, 3)]
            self.spawn_position = (self.spawn_position[0] * self.scaled_tile_size + self.x_offset / 2 -
                                   (self.map_width - self.importend_tile_width) * self.scaled_tile_size / 2,
                                   self.spawn_position[1] * self.scaled_tile_size + self.y_offset / 2 -
                                   (self.map_height - self.importend_tile_height + 2) * self.scaled_tile_size / 2)
            self.player = Player((self.spawn_position[0], self.spawn_position[1]), self)
        # Tile map
        self.tile_table = self.load_tile_table("textures/RocketFunlandTilemap.png", self.tile_height, self.tile_width,
                                               self.scaled_tile_size)
        map_collison_rects = []
        for pos in self.map_collison:
            map_collison_rects.append(pygame.Rect(
                (pos[0] * self.scaled_tile_size + self.x_offset / 2 -
                 (self.map_width - self.importend_tile_width) * self.scaled_tile_size / 2,
                 pos[1] * self.scaled_tile_size + self.y_offset / 2 -
                 (self.map_height - self.importend_tile_height + 2) * self.scaled_tile_size / 2),
                (self.scaled_tile_size, self.scaled_tile_size)))

        self.map_collison_rects_reduced = map_collison_rects
        looking = True
        index = 0
        while looking:
            if index < len(self.map_collison_rects_reduced) - 1:
                item = self.map_collison_rects_reduced[index]
                # next_item = self.map_collison_rects_reduced[index + 1]
                found = False
                for next_item in self.map_collison_rects_reduced:
                    if item.x == next_item.x and next_item.y - (item.y + item.h) == 0:
                        item.h += next_item.h
                        self.map_collison_rects_reduced.remove(next_item)
                        found = True
                        break
                    if item.y == next_item.y and next_item.x - (item.x + item.w) == 0:
                        item.w += next_item.w
                        self.map_collison_rects_reduced.remove(next_item)
                        found = True
                        break
                if not found:
                    index += 1
            else:
                looking = False

    def game_update(self):
        start_time = time()
        # fill screen
        self.screen.fill(self.background_color)
        # TODO fix uneaven movment, faster to the left then to the right
        # gravity and friction
        if self.player.velocity_y < 2.5 * self.tile_scaling:
            self.player.velocity_y += .05 * self.tile_scaling
        if self.player.velocity_x != 0:
            if round(self.player.velocity_x, 2) > 0 and self.player.reduce_velocity_x:
                self.player.velocity_x -= .1 * self.tile_scaling
            if round(self.player.velocity_x, 2) < 0 and self.player.reduce_velocity_x:
                self.player.velocity_x += .1 * self.tile_scaling
            if round(self.player.velocity_x, 2) == 0:
                self.player.reduce_velocity_x = False
                self.player.reduce_velocity_x = 0

        # draw textures  # TODO only draw tiles with movment
        for y_pos, y_list in enumerate(self.map):
            for x_pos, tile in enumerate(y_list):
                self.screen.blit(self.tile_table[tile],
                                 (x_pos * self.scaled_tile_size + self.x_offset / 2 -
                                  (self.map_width - self.importend_tile_width) * self.scaled_tile_size / 2,
                                  y_pos * self.scaled_tile_size + self.y_offset / 2 -
                                  (self.map_height - self.importend_tile_height + 2) * self.scaled_tile_size / 2))
        # for index, rect in enumerate(self.map_collison_rects_reduced):
        #     if index % 2 == 0:
        #         pygame.draw.rect(self.screen, self.color_red, rect)
        #     else:
        #         pygame.draw.rect(self.screen, self.color_yellow, rect)

        # handle player
        # player collision detection and movement
        self.player.boundary_rect.x += self.player.velocity_x
        for tile in self.map_collison_rects_reduced:
            if self.player.boundary_rect.colliderect(tile):
                if self.player.velocity_x > 0:
                    self.player.boundary_rect.right = tile.left
                else:
                    self.player.boundary_rect.left = tile.right
                self.player.velocity_x = 0
        self.player.boundary_rect.y += self.player.velocity_y
        for tile in self.map_collison_rects_reduced:
            if self.player.boundary_rect.colliderect(tile):
                if self.player.velocity_y > 0:
                    self.player.boundary_rect.bottom = tile.top
                    self.player.in_air = False
                else:
                    self.player.boundary_rect.top = tile.bottom
                self.player.velocity_y = 0

        # detect if player fallen of overhang
        if not self.player.in_air:
            self.player.boundary_rect.y += 1
            test = False
            for tile in self.map_collison_rects_reduced:
                if self.player.boundary_rect.colliderect(tile):
                    test = True
            self.player.boundary_rect.y += -1
            if not test:
                self.player.in_air = True
        # draw player
        self.screen.blit(self.player.image, (self.player.boundary_rect.x, self.player.boundary_rect.y))

        # handle rockets
        rockets = self.rockets.copy()
        rockets.reverse()
        for rocket in rockets:
            # player collision detection and movement
            rocket.boundary_rect.x += rocket.velocity_x
            rocket.boundary_rect.y += rocket.velocity_y
            if rocket.boundary_rect.collidelist(self.map_collison_rects_reduced) != -1:
                # TODO explosion
                self.rockets.remove(rocket)

            # draw rocket
            self.screen.blit(rocket.image, (rocket.boundary_rect.x, rocket.boundary_rect.y))

        # update screen
        pygame.display.update()  # TODO only draw tiles with movment -> maybe pass in list of colliding tiles
        if time() - start_time > 1 / self.tick_rate:
            print(
                f'{colorama.Fore.RED}::performance warning::{colorama.Style.RESET_ALL} screen update time: {time() - start_time}')

    def game_loop(self):
        while self.running:
            # get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # event handling
            start_time = time()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print("Quiting...")
                    self.running = False
                    pygame.quit()
                if event.type == pygame.VIDEORESIZE:
                    self.SW, self.SH = pygame.display.get_window_size()
                    if self.SH < 500:
                        self.SH = 500
                        pygame.display.set_mode((self.SW, self.SH), pygame.RESIZABLE)
                    if self.SW < 805:
                        self.SW = 805
                        pygame.display.set_mode((self.SW, self.SH), pygame.RESIZABLE)
                    self.change_scalling()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.reduce_velocity_x = False
                        self.player.velocity_x = -1.5 * self.tile_scaling
                    if event.key == pygame.K_RIGHT:
                        self.player.reduce_velocity_x = False
                        self.player.velocity_x = 1.5 * self.tile_scaling
                    if event.key == pygame.K_UP and self.player.in_air is False:
                        self.player.velocity_y = -3.5 * self.tile_scaling
                        self.player.in_air = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.reduce_velocity_x = True
                    if event.key == pygame.K_RIGHT:
                        self.player.reduce_velocity_x = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    left_mouse_button, middle_mouse_button, right_mouse_button = pygame.mouse.get_pressed(3)
                    if left_mouse_button:
                        player_x = self.player.boundary_rect.x
                        player_y = self.player.boundary_rect.y
                        direction_x = mouse_x - player_x
                        direction_y = mouse_y - player_y
                        direction_length = math.sqrt(direction_x * direction_x + direction_y * direction_y)
                        direction_x /= direction_length
                        direction_y /= direction_length
                        self.rockets.append(
                            Rocket((player_x, player_y), (direction_x, direction_y), self)
                        )

            if time() - start_time > 1 / self.tick_rate:
                print(
                    f'{colorama.Fore.RED}::performance warning::{colorama.Style.RESET_ALL} event handling time: {time() - start_time}')

            self.game_update()

            if time() - start_time > 1 / self.tick_rate:
                print(
                    f'{colorama.Fore.RED}::performance warning::{colorama.Style.RESET_ALL} game loop time: {time() - start_time}')
            # tick
            self.screen_clock.tick(self.tick_rate)
