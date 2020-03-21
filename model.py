# -*- coding:utf-8 -*-
from draw import *


class Model:
    def draw(self):
        pass

    def move(self, direction):
        pass


class Building(Model):
    def __init__(self, floors=1, rooms=1, floor_thickness=0.3, room_length=10.0,
                 room_width=5.0, room_height=5.0, wall_thickness=0.10, rotate=0, pos_x=0.0, pos_y=0.0, pos_z=0.0):
        self.show = True
        self.enable = True
        self.floors = floors
        self.rooms = rooms
        self.floor_thickness = floor_thickness
        self.room_size = [room_length, room_width, room_height]
        self.wall_thickness = wall_thickness

        self.rotate = rotate
        self.position = [pos_x, pos_y, pos_z]

    def move(self, direction):
        speed = 0.4
        if self.enable and direction in ['up', 'down', 'forward', 'back', 'left', 'right']:
            if direction == 'up':
                self.position[1] += speed
            elif direction == 'down':
                self.position[1] -= speed
            elif direction == 'forward':
                self.position[2] -= speed
            elif direction == 'back':
                self.position[2] += speed
            elif direction == 'left':
                self.position[0] -= speed
            elif direction == 'right':
                self.position[0] += speed

    def draw(self, mode=''):
        # 绘制房间
        # glDepthMask(GL_FALSE)
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(self.rotate, 0, 1, 0)
        for i in range(self.floors):
            for j in range(self.rooms):
                if self.rooms % 2 == 0:
                    pos_x = (self.room_size[0] / 2 + self.wall_thickness) * pow(-1, j) * (
                                2 * (j // 2) + 1)
                else:
                    pos_x = (self.room_size[0] + 2 * self.wall_thickness) * pow(-1, j + 1) * (
                                (j + 1) // 2)
                pos_y = (self.room_size[2] + self.floor_thickness) * i
                draw_wall(position=[pos_x, pos_y, 0], size=self.room_size, thickness=self.wall_thickness)
            floor_height = self.room_size[2] + (self.room_size[2] + self.floor_thickness) * i
            floor_length = self.rooms * (self.room_size[0] + 2 * self.wall_thickness)
            floor_width = self.room_size[1] + 2 * self.wall_thickness
            draw_floor(position=[0, floor_height, 0], length=floor_length, width=floor_width,
                       thickness=self.floor_thickness)

        glPopMatrix()
        # glDepthMask(GL_TRUE)


class Source(Model):
    FREQS = [5000, 2400]       # 发射频段
    DAMPING = [20, 25]         # 衰减补偿
    SPAN = [0.5, 0.75]         # 波间隔
    WAVE_BY_POWER = [4, 2]     # 波数与发射功率之比

    def __init__(self, power=15, source_type=0, pos_x=0.0, pos_y=1.0, pos_z=0.0):
        self.show = True
        self.enable = True
        self.freq = self.FREQS[source_type]
        self.power = power
        self.type = source_type
        self.position = [pos_x, pos_y, pos_z]
        self.wave = self.WAVE_BY_POWER[source_type] * power
        self.span = self.SPAN[source_type]
        self.damping = self.DAMPING[source_type]

    def freq_change(self, source_type):
        self.type = source_type
        self.freq = self.FREQS[source_type]
        self.wave = self.WAVE_BY_POWER[source_type] * self.power
        self.span = self.SPAN[source_type]
        self.damping = self.DAMPING[source_type]

    def damp(self, r):
        """
        衰减值(dBm)
        :param r: 传播半径
        """
        return self.damping + 32.45 + 20 * np.log10(self.freq) + 20 * np.log10(r / 1000)

    def move(self, direction):
        speed = 0.4
        if self.enable and direction in ['up', 'down', 'forward', 'back', 'left', 'right']:
            if direction == 'up':
                self.position[1] += speed
            elif direction == 'down':
                self.position[1] -= speed
            elif direction == 'forward':
                self.position[2] -= speed
            elif direction == 'back':
                self.position[2] += speed
            elif direction == 'left':
                self.position[0] -= speed
            elif direction == 'right':
                self.position[0] += speed

    def draw(self):
        glDepthMask(GL_FALSE)
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        # r = 0.01
        for i in range(self.wave):
            r = (i + 1) * self.span
            s = self.power - self.damp(r)
            alpha = np.power(10, (s + 50) / 20) / 8
            if s > -50:
                glColor4f(0.75, 0, 0, alpha)
            elif -50 > s > -70:
                glColor4f(0.75 + (-s - 50) / 80, 0, 0, alpha)
            elif -70 > s > -80:  # 红到黄
                glColor4f(1, (-s - 70) / 10, 0, alpha)
            elif -80 > s > -90:  # 黄到绿
                glColor4f(1 - (-s - 80) / 10, 1, 0, alpha)
            else:
                # r += (-s) / 200
                break
            # r += (-s) / 200
            glutWireSphere(r, 32, 32)
            # sphere = gluNewQuadric()
            # gluSphere(sphere, r, 16, 16)

        glPopMatrix()
        glDepthMask(GL_TRUE)
