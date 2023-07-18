import pyxel

class Room:
    def __init__(self, objects):
        self.objects = objects
        self.types = []
        self.keys = [1] * 3
        self.doors = [1] * 3
        self.doors_state = [8] * 3
        self.button_state = [0] * 3
        self.spawn_x = 0
        self.spawn_y = 0

    def collision(self, x, y):
        if x // 8 > 15 or y // 8 > 15:
            return 0

        object_on = self.objects[x // 8][y // 8]
        object_below = self.objects[x // 8][y // 8 - 1]

        type_on = -1
        type_below = -1

        if object_on in [17, 20, 23]:
            type_on = [17, 20, 23].index(object_on)

        if object_below in [17, 20, 23]:
            type_below = [17, 20, 23].index(object_below)

        if type_on != -1 and self.doors[type_on] == 1:
            return 1
        elif type_below != -1 and self.doors[type_below] == 1:
            return 1
        elif object_on in [13, 14, 15, 16]:
            return 2
        elif object_on in [26, 27]:
            return 3
        elif 1 <= object_on <= 12:
            return 1
        else:
            return 0

    def update_room(self, player_x, player_y):
        for i in range(3):
            if self.button_state[i] != 0:
                self.button_state[i] -= 1

        for x, line in enumerate(self.objects):
            for y, tile in enumerate(line):
                if tile in [17, 20, 23]:
                    door_index = [17, 20, 23].index(tile)
                    if self.keys[door_index] == 0 or self.button_state[door_index] != 0:
                        self.doors[door_index] = 0
                    else:
                        self.doors[door_index] = 1
                elif tile in [18, 21, 24]:
                    button_index = [18, 21, 24].index(tile)
                    button_x = x * 8
                    button_y = y * 8

                    if button_x - 4 <= player_x <= button_x + 4 and button_y == player_y:
                        self.button_state[button_index] = 150
                    elif button_x - 5 <= player_x <= button_x + 5 and button_y - 1 <= player_y <= button_y and self.button_state[button_index] <= 2:
                        self.button_state[button_index] = 2
                    elif button_x - 6 <= player_x <= button_x + 6 and button_y - 2 < player_y <= button_y and self.button_state[button_index] <= 1:
                        self.button_state[button_index] = 1

                elif tile in [19, 22, 25]:
                    key_index = [19, 22, 25].index(tile)
                    key_x = x * 8
                    key_y = y * 8

                    if not (player_x + 7 < key_x or key_x + 7 < player_x or player_y + 7 < key_y or key_y + 7 < player_y):
                        self.keys[key_index] = 0

        for i in range(3):
            if self.doors[i] == 0 and self.doors_state[i] > 0:
                self.doors_state[i] -= 1
            elif self.doors[i] == 1 and self.doors_state[i] < 8:
                self.doors_state[i] += 1

    def draw_room(self):
        for x, line in enumerate(self.objects):
            for y, tile in enumerate(line):
                tile_mapping = {
                    1: (48, 8),
                    2: (48, 0),
                    3: (56, 0),
                    4: (56, 8),
                    5: (16, 16),
                    6: (24, 16),
                    7: (16, 24),
                    8: (24, 24),
                    9: (32, 16),
                    10: (40, 16),
                    11: (32, 24),
                    12: (40, 24),
                    13: (0, 16),
                    14: (8, 16),
                    15: (0, 24),
                    16: (8, 24)
                }
                door_mapping = {
                    17: [(32, 32), (32, 40)],
                    20: [(40, 32), (40, 40)],
                    23: [(48, 32), (48, 40)]
                }
                button_mapping = {
                    18: (24, 40),
                    21: (16, 32),
                    24: (16, 40)
                }
                key_mapping = {
                    19: (56, 32),
                    22: (56, 40),
                    25: (56, 48)
                }

                if tile in tile_mapping:
                    pyxel.blt(x * 8, y * 8, 0, *tile_mapping[tile], 8, 8, 0)

                elif tile in door_mapping:
                    door_index = [17, 20, 23].index(tile)

                    pyxel.blt(x * 8, y * 8, 0, 32 + 8 * (door_index), 40 - self.doors_state[door_index], 8, self.doors_state[door_index], 0)
                    pyxel.blt(x * 8, y * 8 + 16 - self.doors_state[door_index], 0, 32 + 8 * (door_index), 40, 8, self.doors_state[door_index], 0)

                elif tile in button_mapping:
                    button_index = [18, 21, 24].index(tile)

                    if self.button_state[button_index] == 0:
                        pyxel.blt(x * 8, y * 8, 0, *button_mapping[tile], 8, 8, 0)
                    elif self.button_state[button_index] == 1:
                        pyxel.blt(x * 8, y * 8 + 1, 0, *button_mapping[tile], 8, 7, 0)
                    elif self.button_state[button_index] == 2:
                        pyxel.blt(x * 8, y * 8 + self.button_state[button_index], 0, *button_mapping[tile], 8, 6, 0)

                elif tile in key_mapping:
                    key_index = [19, 22, 25].index(tile)

                    if self.keys[key_index] == 1:
                        pyxel.blt(x * 8, y * 8, 0, *key_mapping[tile], 8, 8, 0)
                    else:
                        pyxel.blt(x * 8, y * 8, 0, 0, 0, 8, 8, 0)

                elif tile == 26:
                    pyxel.blt(x * 8, y * 8, 0, 0, 40, 8, 8, 0)
                    pyxel.blt(x * 8 + 8, y * 8, 0, 8, 40, 8, 8, 0)
                    pyxel.blt(x * 8, y * 8 - 8, 0, 0, 32, 8, 8, 0)
                    pyxel.blt(x * 8 + 8, y * 8 - 8, 0, 8, 32, 8, 8, 0)