# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np

from draw import *


class GLWindow(QOpenGLWidget):
    VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 1000.0])  # 视景体的left/right/bottom/top/near/far六个面
    SCALE_K = np.array([1.0, 1.0, 1.0])         # 模型缩放比例
    EYE = np.array([0.0, 5.0, 10.0])            # 眼睛的位置（默认z轴的正方向）
    LOOK_AT = np.array([0.0, 0.0, 0.0])         # 瞄准方向的参考点（默认在坐标原点）
    EYE_UP = np.array([0.0, 4.0, 0.0])          # 定义对观察者而言的上方（默认y轴的正方向）
    WIN_W, WIN_H = 960, 680                     # 保存窗口宽度和高度的变量
    LEFT_IS_DOWNED = False                      # 鼠标左键被按下
    MOUSE_X, MOUSE_Y = 0, 0                     # 考察鼠标位移量时保存的起始位置
    dx, dy, dz = 0, 0, 0                        # 观察点平移偏移量

    building_x_changed = pyqtSignal(float)      # 建筑位置变化
    building_z_changed = pyqtSignal(float)

    source_x_changed = pyqtSignal(float)        # 自定义wifi位置变化的信号
    source_y_changed = pyqtSignal(float)
    source_z_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        super(GLWindow, self).__init__(parent)
        self.DIST, self.PHI, self.THETA = self.get_posture()  # 眼睛与观察目标之间的距离、仰角、方位角
        self.zoom = 0
        self.buildings = []
        self.sources = []
        self.active_building = -1
        self.active_source = -1
        # self.grabKeyboard()

    def initializeGL(self):
        glClearColor(0, 0, 0, 1.0)
        glEnable(GL_DEPTH_TEST)     # 开启深度测试，实现遮挡关系
        glDepthFunc(GL_LEQUAL)      # 设置深度测试函数,GL_LEQUAL只是选项之一

        glutInit()
        display_mode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
        glutInitDisplayMode(display_mode)

    def get_posture(self):
        dist = np.sqrt(np.power((self.EYE-self.LOOK_AT), 2).sum())
        if dist > 0:
            # 仰角和方向角
            phi = np.arcsin((self.EYE[1]-self.LOOK_AT[1])/dist)
            theta = np.arcsin((self.EYE[0]-self.LOOK_AT[0])/(dist*np.cos(phi)))
        else:
            phi = 0.0
            theta = 0.0
        return dist, phi, theta

    def paintGL(self):
        # 设置透明显示
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # 清除屏幕及深度缓存
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 设置投影（透视投影）
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width = self.WIN_W
        height = self.WIN_H
        view = self.VIEW
        if width > height:
            glFrustum(view[0] * width / height, view[1] * width / height, view[2], view[3], view[4], view[5])
        else:
            glFrustum(view[0], view[1], view[2] * height / width, view[3] * height / width, view[4], view[5])

        # 设置模型视图
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # 几何变换
        scale = self.SCALE_K
        glScale(scale[0], scale[1], scale[2])
        # 设置视点
        eye = self.EYE
        eye_up = self.EYE_UP
        look_at = self.LOOK_AT
        gluLookAt(
            eye[0], eye[1], eye[2],
            look_at[0], look_at[1], look_at[2],
            eye_up[0], eye_up[1], eye_up[2]
        )
        # 设置视口
        glViewport(0, 0, width, height)
        # 平移
        glTranslatef(self.dx, self.dy, self.dz)

        # 绘制地面
        draw_land(100)
        # 绘制房间
        for building in self.buildings:
            if building.show:
                building.draw()
        # 绘制信号强度球面
        for source in self.sources:
            if source.show:
                source.draw()

        # 切换缓冲区，以显示绘制内容
        # glutSwapBuffers()

    def resizeGL(self, width, height):
        self.WIN_W, self.WIN_H = width, height
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.MOUSE_X, self.MOUSE_Y = e.x(), e.y()
            self.LEFT_IS_DOWNED = True

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.LEFT_IS_DOWNED = False

    def mouseMoveEvent(self, e):
        if self.LEFT_IS_DOWNED:
            dx = self.MOUSE_X - e.x()
            dy = e.y() - self.MOUSE_Y
            self.MOUSE_X, self.MOUSE_Y = e.x(), e.y()

            self.PHI += 2 * np.pi * dy / self.WIN_H
            self.PHI %= 2 * np.pi
            self.THETA += 2 * np.pi * dx / self.WIN_W
            self.THETA %= 2 * np.pi
            r = self.DIST * np.cos(self.PHI)

            self.EYE[1] = self.DIST * np.sin(self.PHI)
            self.EYE[0] = r * np.sin(self.THETA)
            self.EYE[2] = r * np.cos(self.THETA)

            if 0.5 * np.pi < self.PHI < 1.5 * np.pi:
                self.EYE_UP[1] = -1.0
            else:
                self.EYE_UP[1] = 1.0

            self.update()

    def wheelEvent(self, e):
        if e.angleDelta().y() >= 120 and self.zoom > -15:
            self.EYE = self.LOOK_AT + (self.EYE - self.LOOK_AT) * 0.95
            self.DIST, self.PHI, self.THETA = self.get_posture()
            self.zoom -= 1
            self.update()
        elif e.angleDelta().y() <= -120 and self.zoom < 20:
            self.EYE = self.LOOK_AT + (self.EYE - self.LOOK_AT) / 0.95
            self.DIST, self.PHI, self.THETA = self.get_posture()
            self.zoom += 1
            self.update()

    def keyPressEvent(self, e):
        key = e.key()
        mod = e.modifiers()
        speed = 0.4
        if key in [Qt.Key_W, Qt.Key_A, Qt.Key_S, Qt.Key_D, Qt.Key_Space, Qt.Key_C]:
            if key == Qt.Key_W:
                self.dz += speed
            elif key == Qt.Key_S:
                self.dz -= speed
            elif key == Qt.Key_A:
                self.dx += speed
            elif key == Qt.Key_D:
                self.dx -= speed
            elif key == Qt.Key_Space:
                self.dy -= speed
            elif key == Qt.Key_C:
                self.dy += speed
            self.update()
        if self.active_source >= 0:
            active = self.active_source
            if key in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
                if mod == Qt.ControlModifier:
                    if key == Qt.Key_Up:
                        self.sources[active].move('up')
                        self.source_y_changed.emit(self.sources[active].position[1])    # 传递当前位置信号
                    elif key == Qt.Key_Down:
                        self.sources[active].move('down')
                        self.source_y_changed.emit(self.sources[active].position[1])
                else:
                    if key == Qt.Key_Up:
                        self.sources[active].move('forward')
                        self.source_z_changed.emit(self.sources[active].position[2])
                    elif key == Qt.Key_Down:
                        self.sources[active].move('back')
                        self.source_z_changed.emit(self.sources[active].position[2])
                    elif key == Qt.Key_Left:
                        self.sources[active].move('left')
                        self.source_x_changed.emit(self.sources[active].position[0])
                    elif key == Qt.Key_Right:
                        self.sources[active].move('right')
                        self.source_x_changed.emit(self.sources[active].position[0])
                self.update()
        elif self.active_building >= 0:
            active = self.active_building
            if key in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
                if key == Qt.Key_Up:
                    self.buildings[active].move('forward')
                    self.building_z_changed.emit(self.buildings[active].position[2])
                elif key == Qt.Key_Down:
                    self.buildings[active].move('back')
                    self.building_z_changed.emit(self.buildings[active].position[2])
                elif key == Qt.Key_Left:
                    self.buildings[active].move('left')
                    self.building_x_changed.emit(self.buildings[active].position[0])
                elif key == Qt.Key_Right:
                    self.buildings[active].move('right')
                    self.building_x_changed.emit(self.buildings[active].position[0])


class Building:
    def __init__(self, floors=1, rooms=1, floor_thickness=0.3, room_length=10.0,
                 room_width=5.0, room_height=5.0, wall_thickness=0.10, pos_x=0.0, pos_z=0.0):
        self.show = True
        self.enable = True
        self.floors = floors
        self.rooms = rooms
        self.floor_thickness = floor_thickness
        self.room_size = [room_length, room_width, room_height]
        self.wall_thickness = wall_thickness
        self.position = [pos_x, 0.0, pos_z]

    def move(self, direction):
        speed = 0.4
        if self.enable and direction in ['forward', 'back', 'left', 'right']:
            if direction == 'forward':
                self.position[2] -= speed
            elif direction == 'back':
                self.position[2] += speed
            elif direction == 'left':
                self.position[0] -= speed
            elif direction == 'right':
                self.position[0] += speed

    def draw(self):
        # 绘制房间
        glDepthMask(GL_FALSE)
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
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
            draw_floor(position=[0, floor_height, 0], length=floor_length, width=floor_width, thickness=self.floor_thickness)

        glPopMatrix()
        glDepthMask(GL_TRUE)


class Source:
    FREQS = [5000, 2400]        # 发射频段
    DAMPING = [20, 25]          # 衰减补偿
    SPAN = [0.5, 0.75]           # 波间隔
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
        # 衰减值(dBm)
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
            # glutWireSphere(r, 32, 32)
            sphere = gluNewQuadric()
            gluSphere(sphere, r, 16, 16)

        glPopMatrix()
        glDepthMask(GL_TRUE)


if __name__ == '__main__':
    glutInit()
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
    glutInitDisplayMode(displayMode)

    app = QApplication(sys.argv)

    building = Building(floors=5, rooms=5, floor_thickness=1, room_length=12, room_width=6, room_height=5, wall_thickness=0.2)
    glwindow = GLWindow(building)
    source = Source()
    glwindow.sources.append(source)
    source2 = Source(pos_x=10)
    glwindow.sources.append(source2)

    glwindow.setGeometry(200, 200, 960, 680)
    glwindow.show()
    sys.exit(app.exec_())
