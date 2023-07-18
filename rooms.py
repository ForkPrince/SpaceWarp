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
        if object_on == 17:
            type_on = 0
        elif object_on == 20:
            type_on = 1
        elif object_on == 23:
            type_on = 2

        type_below = -1
        if object_below == 17:
            type_below = 0
        elif object_below == 20:
            type_below = 1
        elif object_below == 23:
            type_below = 2

        if object_on == 17 or object_on == 20 or object_on == 23:
            if type_on != -1 and (self.doors[type_on] == 1):
                return 1
        elif object_below == 17 or object_below == 20 or object_below == 23:
            if type_below != -1 and (self.doors[type_below] == 1):
                return 1
        elif object_on == 13 or object_on == 14 or object_on == 15 or object_on == 16:
            return 2
        elif object_on == 26 or object_on == 27:
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
                if tile == 17:
                    if self.keys[0] == 0 or self.button_state[0] != 0:
                        self.doors[0] = 0
                    else:
                        self.doors[0] = 1
                elif tile == 18:
                    if x * 8 - 4 <= player_x <= x * 8 + 4 and y * 8 == player_y:
                        self.button_state[0] = 150
                    elif x * 8 - 5 <= player_x <= x * 8 + 5 and y * 8 - 1 <= player_y <= y * 8 and self.button_state[0] <= 2:
                        self.button_state[0] = 2
                    elif x * 8 - 6 <= player_x <= x * 8 + 6 and y * 8 - 2 < player_y <= y * 8 and self.button_state[0] <= 1:
                        self.button_state[0] = 1
                elif tile == 19:
                    if (not(player_x + 7 < x * 8 or x * 8 + 7 < player_x or player_y + 7 < y * 8 or y * 8 + 7 < player_y)):
                        self.keys[0] = 0

                elif tile == 20:
                    if self.keys[1] == 0 or self.button_state[1] != 0:
                        self.doors[1] = 0
                    else:
                        self.doors[1] = 1
                elif tile == 21:
                    if x * 8 - 4 <= player_x <= x * 8 + 4 and y * 8 == player_y:
                        self.button_state[1] = 150
                    elif x * 8 - 5 <= player_x <= x * 8 + 5 and y * 8 - 1 <= player_y <= y * 8 and self.button_state[1] <= 2:
                        self.button_state[1] = 2
                    elif x * 8 - 6 <= player_x <= x * 8 + 6 and y * 8 - 2 < player_y <= y * 8 and self.button_state[1] <= 1:
                        self.button_state[1] = 1
                elif tile == 22:
                    if (not(player_x + 7 < x * 8 or x * 8 + 7 < player_x or player_y + 7 < y * 8 or y * 8 + 7 < player_y)):
                        self.keys[1] = 0

                elif tile == 23:
                    if self.keys[2] == 0 or self.button_state[2] != 0:
                        self.doors[2] = 0
                    else:
                        self.doors[2] = 1
                elif tile == 24:
                    if x * 8 - 4 <= player_x <= x * 8 + 4 and y * 8 == player_y:
                        self.button_state[2] = 150
                    elif x * 8 - 5 <= player_x <= x * 8 + 5 and y * 8 - 1 <= player_y <= y * 8 and self.button_state[2] <= 2:
                        self.button_state[2] = 2
                    elif x * 8 - 6 <= player_x <= x * 8 + 6 and y * 8 - 2 < player_y <= y * 8 and self.button_state[2] <= 1:
                        self.button_state[2] = 1
                elif tile == 25:
                    if (not(player_x + 7 < x * 8 or x * 8 + 7 < player_x or player_y + 7 < y * 8 or y * 8 + 7 < player_y)):
                        self.keys[2] = 0

        for i in range(3):
            if self.doors[i] == 0 and self.doors_state[i] > 0:
                self.doors_state[i] -= 1
            elif self.doors[i] == 1 and self.doors_state[i] < 8:
                self.doors_state[i] += 1

    def draw_room(self):
        for x, line in enumerate(self.objects):
            for y, tile in enumerate(line):
                if tile == 1:
                    pyxel.blt(x * 8, y * 8, 0, 48, 8, 8, 8, 0)
                elif tile == 2:
                    pyxel.blt(x * 8, y * 8, 0, 48, 0, 8, 8, 0)
                elif tile == 3:
                    pyxel.blt(x * 8, y * 8, 0, 56, 0, 8, 8, 0)
                elif tile == 4:
                    pyxel.blt(x * 8, y * 8, 0, 56, 8, 8, 8, 0)
                elif tile == 5:
                    pyxel.blt(x * 8, y * 8, 0, 16, 16, 8, 8, 0)
                elif tile == 6:
                    pyxel.blt(x * 8, y * 8, 0, 24, 16, 8, 8, 0)
                elif tile == 7:
                    pyxel.blt(x * 8, y * 8, 0, 16, 24, 8, 8, 0)
                elif tile == 8:
                    pyxel.blt(x * 8, y * 8, 0, 24, 24, 8, 8, 0)
                elif tile == 9:
                    pyxel.blt(x * 8, y * 8, 0, 32, 16, 8, 8, 0)
                elif tile == 10:
                    pyxel.blt(x * 8, y * 8, 0, 40, 16, 8, 8, 0)
                elif tile == 11:
                    pyxel.blt(x * 8, y * 8, 0, 32, 24, 8, 8, 0)
                elif tile == 12:
                    pyxel.blt(x * 8, y * 8, 0, 40, 24, 8, 8, 0)

                elif tile == 13:
                    pyxel.blt(x * 8, y * 8, 0, 0, 16, 8, 8, 0)
                elif tile == 14:
                    pyxel.blt(x * 8, y * 8, 0, 8, 16, 8, 8, 0)
                elif tile == 15:
                    pyxel.blt(x * 8, y * 8, 0, 0, 24, 8, 8, 0)
                elif tile == 16:
                    pyxel.blt(x * 8, y * 8, 0, 8, 24, 8, 8, 0)

                elif tile == 17:
                    pyxel.blt(x * 8, y * 8 + self.doors_state[0] - 8, 0, 32, 32, 8, 8, 0)
                    pyxel.blt(x * 8, y * 8 + 16 - self.doors_state[0], 0, 32, 40, 8, 8, 0)
                elif tile == 18:
                    if self.button_state[0] == 0:
                        pyxel.blt(x * 8, y * 8, 0, 24, 40, 8, 8, 0)
                    elif self.button_state[0] == 1:
                        pyxel.blt(x * 8, y * 8 + 1, 0, 24, 40, 8, 7, 0)
                    elif self.button_state[0] == 2:
                        pyxel.blt(x * 8, y * 8 + 2, 0, 24, 40, 8, 6, 0)
                elif tile == 19:
                    if self.keys[0] == 1:
                        pyxel.blt(x * 8, y * 8, 0, 56, 32, 8, 8, 0)
                    else:
                        pyxel.blt(x * 8, y * 8, 0, 0, 0, 8, 8, 0)

                elif tile == 20:
                    pyxel.blt(x * 8, y * 8 + self.doors_state[1] - 8, 0, 40, 32, 8, 8, 0)
                    pyxel.blt(x * 8, y * 8 + 16 - self.doors_state[1], 0, 40, 40, 8, 8, 0)
                elif tile == 21:
                    if self.button_state[1] == 0:
                        pyxel.blt(x * 8, y * 8, 0, 16, 32, 8, 8, 0)
                    elif self.button_state[1] == 1:
                        pyxel.blt(x * 8, y * 8 + 1, 0, 16, 32, 8, 7, 0)
                    elif self.button_state[1] == 2:
                        pyxel.blt(x * 8, y * 8 + 2, 0, 16, 32, 8, 6, 0)
                elif tile == 22:
                    if self.keys[1] == 1:
                        pyxel.blt(x * 8, y * 8, 0, 56, 40, 8, 8, 0)
                    else:
                        pyxel.blt(x * 8, y * 8, 0, 0, 0, 8, 8, 0)

                elif tile == 23:
                    pyxel.blt(x * 8, y * 8 + self.doors_state[2] - 8, 0, 48, 32, 8, 8, 0)
                    pyxel.blt(x * 8, y * 8 + 16 - self.doors_state[2], 0, 48, 40, 8, 8, 0)
                elif tile == 24:
                    if self.button_state[2] == 0:
                        pyxel.blt(x * 8, y * 8, 0, 16, 40, 8, 8, 0)
                    elif self.button_state[2] == 1:
                        pyxel.blt(x * 8, y * 8 + 1, 0, 16, 40, 8, 7, 0)
                    elif self.button_state[2] == 2:
                        pyxel.blt(x * 8, y * 8 + 2, 0, 16, 40, 8, 6, 0)
                elif tile == 25:
                    if self.keys[2] == 1:
                        pyxel.blt(x * 8, y * 8, 0, 56, 48, 8, 8, 0)
                    else:
                        pyxel.blt(x * 8, y * 8, 0, 0, 0, 8, 8, 0)

                elif tile == 26:
                    pyxel.blt(x * 8, y * 8, 0, 0, 40, 8, 8, 0)
                    pyxel.blt(x * 8 + 8, y * 8, 0, 8, 40, 8, 8, 0)
                    pyxel.blt(x * 8, y * 8 - 8, 0, 0, 32, 8, 8, 0)
                    pyxel.blt(x * 8 + 8, y * 8 - 8, 0, 8, 32, 8, 8, 0)