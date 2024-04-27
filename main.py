import pyxel, json, copy, math
from player import Player
from rooms import Room
from menu import Menu
from pygame import mixer

mixer.music.load("ressources/bgm.mp3")

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

import numpy as np

def rotate(array):
    array_np = np.array(array)

    rotated = np.rot90(array_np, k=0, axes=(0,1))

    return rotated.tolist()

class App:
    def __init__(self):
        self.gamestate = 0
        self.menu = Menu()
        mixer.music.play()

        pyxel.init(128, 128, title='SpaceWarp')
        pyxel.load("ressources/assets.pyxres")
        pyxel.run(self.update, self.draw)
        
    def load_mask(self):
        tilemap = pyxel.tilemaps[self.difficulty + 1]

        tile_mapping = {
            (6, 1): 1,
            (6, 0): 2,
            (7, 0): 3,
            (7, 1): 4,
            (2, 2): 5,
            (3, 2): 6,
            (2, 3): 7,
            (3, 3): 8,
            (4, 2): 9,
            (5, 2): 10,
            (4, 3): 11,
            (5, 3): 12,
            (0, 4): 26,
            (0, 5): 27,
            (1, 4): 28,
            (1, 5): 29,
            (3, 5): 18,
            (2, 4): 21,
            (2, 5): 24,
            (7, 4): 19,
            (7, 5): 22,
            (7, 6): 25,
            (4, 5): 0,
            (5, 5): 0,
            (6, 5): 0,
            (4, 4): 17,
            (5, 4): 20,
            (6, 4): 23,
            (0, 2): 13,
            (0, 3): 15,
            (1, 2): 14,
            (1, 3): 16,
            (6, 2): 30,
            (6, 3): 31,
            (7, 2): 32,
            (7, 3): 33,
            (4, 0): 34,
            (4, 1): 35,
            (5, 0): 36,
            (5, 1): 37,
            (0, 1): 38,
            (3, 4): 39,
            (0, 6): 40,
            (0, 7): 41,
            (1, 6): 42,
            (1, 7): 43,
            (2, 6): 44,
            (2, 7): 45,
            (3, 6): 46,
            (3, 7): 47,
            (4, 6): 48,
            (4, 7): 49,
            (5, 6): 50,
            (5, 7): 51,
            (6, 6): 52,
            (6, 7): 53,
            (7, 7): 55
        }

        self.rooms = [[0] * 16] * 16

        for level in range(16):
            room = [[0] * 16 for _ in range(16)]

            offset = 16 * level

            for x in range(16):
                for y in range(16):
                    tile = tilemap.pget(x + offset, y)

                    tile_type = 0 if tile == (0, 0) else 2

                    if tile in tile_mapping:
                        tile_index = tile_mapping[tile]

                        tile_type = tile_index

                    room[x][y] = tile_type

            room = rotate(room)
            self.rooms[level] = Room(room)

    def update(self):
        if self.gamestate == 0:
            self.gamestate = self.menu.update_menu()
            if self.gamestate == 1:
                self.difficulty = self.menu.difficulty
                self.load_mask()
                self.rooms[0].spawn_x, self.rooms[0].spawn_y = 0, 112
                self.enter_room_state = copy.deepcopy(self.rooms[0])
                self.start_frame = pyxel.frame_count
                self.end_frame = 0
                self.player = Player(0, 112, 0)
                self.current_screen = 0
            return
        if self.gamestate == 2:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_Z) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A):
                self.gamestate = 0
            return
        self.player.move(self.rooms[self.current_screen], self.current_screen, self.difficulty)
        self.update_screen_position()
        self.rooms[self.current_screen].update_room(self.player.x, self.player.y)
        
        if self.player.alive == 0 or pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
            self.player.reset(self.rooms[self.current_screen].spawn_x, self.rooms[self.current_screen].spawn_y)
            self.player.alive = 1
            self.rooms[self.current_screen] = copy.deepcopy(self.enter_room_state)
        
        if self.player.win == 1:
            self.gamestate = 2
            self.end_frame = pyxel.frame_count
            self.total_time = str(round_half_up((self.end_frame - self.start_frame)/30, 2))
            self.end_anim_frame = 0

    def update_screen_position(self):
        if self.player.x == 124:
            self.current_screen += 1
            self.player.x -= 128
            self.rooms[self.current_screen].spawn_x = self.player.x + 4
            self.rooms[self.current_screen].spawn_y = self.player.y
            self.enter_room_state = copy.deepcopy(self.rooms[self.current_screen])
        elif self.player.x == -5 and self.current_screen != 0:
            self.current_screen -= 1
            self.player.x += 128
            self.rooms[self.current_screen].spawn_x = self.player.x - 4
            self.rooms[self.current_screen].spawn_y = self.player.y
            self.enter_room_state = copy.deepcopy(self.rooms[self.current_screen])


    def draw(self):
        if not mixer.music.get_busy():
            mixer.music.play()
        if self.gamestate == 0:
            pyxel.cls(0)
            self.menu.draw_menu()
        elif self.gamestate == 1:
            pyxel.cls(0)
            self.rooms[self.current_screen].draw_room()
            self.player.draw_player()

            #! Debug Mode
            if self.menu.debug == 1 and (pyxel.btnp(pyxel.KEY_LEFTBRACKET) or pyxel.btnp(pyxel.KEY_RIGHTBRACKET)):
                if pyxel.btnp(pyxel.KEY_LEFTBRACKET):
                    self.current_screen = (self.current_screen - 1) % len(self.rooms)
                if pyxel.btnp(pyxel.KEY_RIGHTBRACKET):
                    self.current_screen = (self.current_screen + 1) % len(self.rooms)

                if self.current_screen == 1 or self.current_screen == 3:
                    self.rooms[self.current_screen].spawn_x = 0
                    self.rooms[self.current_screen].spawn_y = 112
                elif self.current_screen == 2:
                    self.rooms[self.current_screen].spawn_x = 0
                    self.rooms[self.current_screen].spawn_y = 48

                self.enter_room_state = copy.deepcopy(self.rooms[self.current_screen])
                self.player.alive = 0

        elif self.gamestate == 2:
            pyxel.cls(0)
            if self.end_anim_frame < 72:
                pyxel.bltm(0, 0, 0, 128, 0, 128, 64)
                pyxel.blt(88, 48 - self.end_anim_frame, 0, 0, 32, 16, 16)
                pyxel.blt(92, 64 - self.end_anim_frame, 0, 8, 16, 8, 8)
                pyxel.bltm(0, 64, 0, 128, 64, 128, 64)
                self.end_anim_frame += 1        
            else:
                pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
                pyxel.text(48, 48, "You win!", 7)
                pyxel.text(40, 56, "Time: " + self.total_time + "s", 7)
                pyxel.text(42, 72, "Difficulty:", 7)
                pyxel.text(48, 80, str(self.menu.options[1][self.difficulty]), 0)

App()