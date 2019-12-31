# -*- coding:utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

from draw import *


class GLWindow(QOpenGLWindow):
    VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 1000.0])  # 视景体的left/right/bottom/top/near/far六个面
    SCALE_K = np.array([1.0, 1.0, 1.0])         # 模型缩放比例
    EYE = np.array([0.0, 5.0, 20.0])            # 眼睛的位置（默认z轴的正方向）
    LOOK_AT = np.array([0.0, 0.0, 0.0])         # 瞄准方向的参考点（默认在坐标原点）
    EYE_UP = np.array([0.0, 4.0, 0.0])          # 定义对观察者而言的上方（默认y轴的正方向）
    WIN_W, WIN_H = 960, 680                     # 保存窗口宽度和高度的变量
    LEFT_IS_DOWNED = False                      # 鼠标左键被按下
    MOUSE_X, MOUSE_Y = 0, 0                     # 考察鼠标位移量时保存的起始位置
    dx, dy, dz = 0, 0, 0                        # 观察点平移偏移量
    wifi_x, wifi_y, wifi_z = 0, 3, 0            # wifi位置

    def __init__(self, parent=None):
        super(GLWindow, self).__init__(parent)
        self.DIST, self.PHI, self.THETA = self.get_posture()  # 眼睛与观察目标之间的距离、仰角、方位角
        self.floors = 1
        self.sources = [1]
        self.power = 15             # 发射功率默认15dBm,31.6mW
        self.wifi_type = 0
        self.freqs = [5000, 2400]   # 发射频率默认5GHz
        self.damping = [20, 25]     # 衰减补偿值
        self.span = [0.2, 0.3]      # 波间隔
        # self.wave = [10*self.power, 5*self.power]      # 波数量
        self.wave_by_power = [10, 5]  # 波数量与发射功率之比

    def initializeGL(self):
        glClearColor(0, 0, 0, 1.0)
        glEnable(GL_DEPTH_TEST)     # 开启深度测试，实现遮挡关系
        glDepthFunc(GL_LEQUAL)      # 设置深度测试函数,GL_LEQUAL只是选项之一

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

        sqare = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
        color_wall = [0.9, 0.9, 0.9]
        color_land = [0.9, 0.9, 0.9]
        room_size = [20.0, 10.0, 6.0]
        land = 100.0

        # 绘制地面
        glBegin(GL_POLYGON)
        for i in range(4):
            glColor4f(color_land[0], color_land[1], color_land[2], 1.0)
            glVertex3f(sqare[i][0] * land, 0, sqare[i][1] * land)
        glEnd()

        # 绘制房间
        for i in range(self.floors):
            draw_wall(position=[0, 7 * i, 0], size=room_size, thickness=0.5)
            draw_wall(position=[21, 7 * i, 0], size=room_size, thickness=0.5)
            draw_wall(position=[-21, 7 * i, 0], size=room_size, thickness=0.5)
            draw_floor(position=[0, 6 + 7 * i, 0], length=63, width=11, thickness=1)

        # 绘制信号强度球面
        for wifi in self.sources:
            glPushMatrix()
            glTranslatef(self.wifi_x, self.wifi_y, self.wifi_z)
            # r = 0.01
            for i in range(self.wave_by_power[self.wifi_type] * self.power):
                r = (i + 1) * self.span[self.wifi_type]
                s = self.power - self.damp(self.freqs[self.wifi_type], r)
                alpha = np.power(10, (s + 50) / 20) / 5
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

        # 切换缓冲区，以显示绘制内容
        # glutSwapBuffers()

    # 衰减dBm
    def damp(self, freq, r):
        return self.damping[self.wifi_type] + 32.45 + 20 * np.log10(freq) + 20 * np.log10(r / 1000)

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
        if e.angleDelta().y() >= 120:
            self.EYE = self.LOOK_AT + (self.EYE - self.LOOK_AT) * 0.95
            self.DIST, self.PHI, self.THETA = self.get_posture()
            self.update()
        elif e.angleDelta().y() <= -120:
            self.EYE = self.LOOK_AT + (self.EYE - self.LOOK_AT) / 0.95
            self.DIST, self.PHI, self.THETA = self.get_posture()
            self.update()

    def keyPressEvent(self, e):
        pass


if __name__ == '__main__':
    glutInit()
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
    glutInitDisplayMode(displayMode)
    
    app = QApplication(sys.argv)
    glwindow = GLWindow()
    glwindow.setGeometry(200, 200, 960, 680)
    glwindow.show()
    sys.exit(app.exec_())
