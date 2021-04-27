import pygame
import json
import colorama

from time import time


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
        with open("map/RocketFunlandMap.json") as map_json:
            map_dict = json.load(map_json)
        self.tile_height = map_dict["tileheight"]
        self.tile_width = map_dict["tilewidth"]
        self.map_height = map_dict["height"]
        self.map_width = map_dict["width"]
        self.map_placment_list = map_dict["layers"][0]["data"]

        self.tile_scaling = self.SW / (self.tile_width * self.map_width)
        self.y_offset = self.SH / (self.tile_height * self.map_height * self.tile_scaling)
        self.tile_offset = int((self.map_height - self.y_offset * self.map_height) / 2 + 1)  # +1 to fill rounding gaps

        self.tile_table = self.load_tile_table("map/Tilemap.png", self.tile_height, self.tile_width, self.tile_scaling)

        self.map = []
        element = 0
        line = 0
        for tile in self.map_placment_list:
            if element == 0:
                self.map.append([tile - 1])
            else:
                self.map[line].append(tile - 1)  # -1 because latter used as index
            if element == self.map_width - 1:
                line += 1
                element = 0
            else:
                element += 1

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
    def load_tile_table(filename, width, height, scale):
        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_y in range(0, int(image_height / height)):
            for tile_x in range(0, int(image_width / width)):
                rect = (tile_x * width, tile_y * height, width, height)
                tile_table.append(
                    pygame.transform.scale(image.subsurface(rect),
                                           (int(width * scale + 1),  # +1 to fill rounding gaps
                                            int(height * scale + 1))  # +1 to fill rounding gaps
                                           )
                )
        return tile_table

    def screen_update(self):
        start_time = time()
        # fill screen
        self.screen.fill(self.background_color)
        # draw map
        y_pos = 0
        for y_list in self.map:
            x_pos = 0
            for tile in self.map[self.map.index(y_list)]:
                if y_pos >= self.tile_offset:
                    self.screen.blit(self.tile_table[tile],
                                     (x_pos * self.tile_height * self.tile_scaling,
                                      (y_pos - self.tile_offset) * self.tile_width * self.tile_scaling))
                x_pos += 1
            y_pos += 1

        # update screen
        pygame.display.update()
        if time() - start_time > 1 / self.tick_rate:
            print(f'{colorama.Fore.RED}::performance warning::{colorama.Style.RESET_ALL} screen update time: {time() - start_time}')

    def game_loop(self):
        while self.running:
            # get mouse position
            mouse = pygame.mouse.get_pos()

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
                    self.tile_scaling = self.SW / (self.tile_width * self.map_width)
                    self.tile_table = self.load_tile_table("map/Tilemap.png", self.tile_height, self.tile_width,
                                                           self.tile_scaling)
                    self.y_offset = self.SH / (self.tile_height * self.map_height * self.tile_scaling)
                    self.tile_offset = int((self.map_height - self.y_offset * self.map_height) / 2 + 1)
            if time() - start_time > 1 / self.tick_rate:
                print(f'{colorama.Fore.RED}::performance warning::{colorama.Style.RESET_ALL} event handling time: {time() - start_time}')

            self.screen_update()

            if time() - start_time > 1 / self.tick_rate:
                print(f'{colorama.Fore.RED}::performance warning::{colorama.Style.RESET_ALL} game loop time: {time() - start_time}')
            # tick
            self.screen_clock.tick(self.tick_rate)
