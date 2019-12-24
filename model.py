# -*- coding:utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


class GLWindow:

    IS_PERSPECTIVE = True   # 透视投影
    VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 1000.0])  # 视景体的left/right/bottom/top/near/far六个面
    SCALE_K = np.array([1.0, 1.0, 1.0])     # 模型缩放比例
    EYE = np.array([0.0, 0.0, 4.0])         # 眼睛的位置（默认z轴的正方向）
    LOOK_AT = np.array([0.0, 0.0, 0.0])     # 瞄准方向的参考点（默认在坐标原点）
    EYE_UP = np.array([0.0, 4.0, 0.0])      # 定义对观察者而言的上方（默认y轴的正方向）
    WIN_W, WIN_H = 640, 480                 # 保存窗口宽度和高度的变量
    LEFT_IS_DOWNED = False                  # 鼠标左键被按下
    MOUSE_X, MOUSE_Y = 0, 0                 # 考察鼠标位移量时保存的起始位置
    dx, dy, dz = 0, 0, 0                    # 平移偏移量

    def __init__(self):
        self.DIST, self.PHI, self.THETA = self.getposture()  # 眼睛与观察目标之间的距离、仰角、方位角

    def init(self):
        glClearColor(0.4, 0.8, 1.0, 1.0)

        glEnable(GL_DEPTH_TEST)     # 开启深度测试，实现遮挡关系
        glDepthFunc(GL_LEQUAL)      # 设置深度测试函数,GL_LEQUAL只是选项之一

    def getposture(self):
        dist = np.sqrt(np.power((self.EYE-self.LOOK_AT), 2).sum())
        if dist > 0:
            # 仰角和方向角
            phi = np.arcsin((self.EYE[1]-self.LOOK_AT[1])/dist)
            theta = np.arcsin((self.EYE[0]-self.LOOK_AT[0])/(dist*np.cos(phi)))
        else:
            phi = 0.0
            theta = 0.0
        return dist, phi, theta

    def draw(self):
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
            if self.IS_PERSPECTIVE:
                glFrustum(view[0] * width / height, view[1] * width / height, view[2], view[3], view[4], view[5])
            else:
                glOrtho(view[0] * width / height, view[1] * width / height, view[2], view[3], view[4], view[5])
        else:
            if self.IS_PERSPECTIVE:
                glFrustum(view[0], view[1], view[2] * height / width, view[3] * height / width, view[4], view[5])
            else:
                glOrtho(view[0], view[1], view[2] * height / width, view[3] * height / width, view[4], view[5])

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

        # 绘制坐标系
        '''
        xyz_depth = 2.0
        glBegin(GL_LINES)
        glColor4f(0.0, 0.0, 0.0, 1.0)
        glVertex3f(-xyz_depth, 0.0, 0.0)
        glVertex3f(xyz_depth, 0.0, 0.0)
        glColor4f(0.0, 0.0, 0.0, 1.0)
        glVertex3f(0.0, -xyz_depth, 0.0)
        glVertex3f(0.0, xyz_depth, 0.0)
        glColor4f(0.0, 0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, -xyz_depth)
        glVertex3f(0.0, 0.0, xyz_depth)
        glEnd()'''

        sqare = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
        room_length = 10.0
        room_width = 7.0
        land = 100.0
        # 绘制后面
        glBegin(GL_QUADS)
        for i in range(4):
            glColor4f(0.75, 0.75, 0.75, 1.0)
            glVertex3f(sqare[i][0]*room_length, sqare[i][1]*5.0, -room_width)
        glEnd()

        # 绘制左侧、顶面、右侧
        glBegin(GL_QUAD_STRIP)
        for i in range(4):
            glColor4f(0.75, 0.75, 0.75, 1.0)
            glVertex3f(sqare[i][0] * room_length, sqare[i][1] * 5.0, room_width)
            glColor4f(0.75, 0.75, 0.75, 1.0)
            glVertex3f(sqare[i][0] * room_length, sqare[i][1] * 5.0, -room_width)
        glEnd()

        # 绘制底面
        glBegin(GL_POLYGON)
        for i in range(4):
            glColor4f(0.75, 0.56, 0.375, 1.0)
            glVertex3f(sqare[i][0]*land, -5.0, sqare[i][1]*land)
        glEnd()

        # 绘制点
        glDepthMask(GL_FALSE)
        glPointSize(5.0)
        glBegin(GL_POINTS)
        glColor4f(1.0, 0.0, 0.0, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glEnd()
        glDepthMask(GL_TRUE)

        # 切换缓冲区，以显示绘制内容
        glutSwapBuffers()

    # 事件
    def reshape(self, width, height):
        self.WIN_W, self.WIN_H = width, height
        glutPostRedisplay()

    def mouse_click(self, button, state, x, y):
        self.MOUSE_X, self.MOUSE_Y = x, y
        if button == GLUT_LEFT_BUTTON:
            self.LEFT_IS_DOWNED = state == GLUT_DOWN
        elif button == 3:
            self.EYE = self.LOOK_AT + (self.EYE - self.LOOK_AT) * 0.95
            self.DIST, self.PHI, self.THETA = self.getposture()
            glutPostRedisplay()
        elif button == 4:
            self.EYE = self.LOOK_AT + (self.EYE - self.LOOK_AT) / 0.95
            self.DIST, self.PHI, self.THETA = self.getposture()
            glutPostRedisplay()
        '''
        elif button == 3:
            self.SCALE_K *= 1.05
            glutPostRedisplay()
        elif button == 4:
            self.SCALE_K *= 0.95
            glutPostRedisplay()'''

    def mouse_motion(self, x, y):
        if self.LEFT_IS_DOWNED:
            dx = self.MOUSE_X - x
            dy = y - self.MOUSE_Y
            self.MOUSE_X, self.MOUSE_Y = x, y

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

            glutPostRedisplay()

    def keydown(self, key, x, y):
        speed = 0.4
        if key in [b'a', b'd', b'y', b'Y', b'w', b's']:
            if key == b'd':  # 瞄准参考点 x 减小
                self.dx -= speed
            elif key == b'a':  # 瞄准参考 x 增大
                self.dx += speed
            elif key == b'y':  # 瞄准参考点 y 减小
                self.LOOK_AT[1] -= speed
            elif key == b'Y':  # 瞄准参考点 y 增大
                self.LOOK_AT[1] += speed
            elif key == b's':  # 瞄准参考点 z 减小
                self.dz -= speed
            elif key == b'w':  # 瞄准参考点 z 增大
                self.dz += speed

            self.DIST, self.PHI, self.THETA = self.getposture()
            glutPostRedisplay()
        '''
        elif key == b'\r':  # 回车键，视点前进
            self.EYE = self.LOOK_AT + (self.EYE - self.LOOK_AT) * 0.9
            self.DIST, self.PHI, self.THETA = self.getposture()
            glutPostRedisplay()
        elif key == b'\x08':  # 退格键，视点后退
            self.EYE = self.LOOK_AT + (self.EYE - self.LOOK_AT) * 1.1
            self.DIST, self.PHI, self.THETA = self.getposture()
            glutPostRedisplay()
        elif key == b' ':  # 空格键，切换投影模式
            self.IS_PERSPECTIVE = not self.IS_PERSPECTIVE
            glutPostRedisplay()'''


if __name__ == "__main__":
    glwindow = GLWindow()

    glutInit()
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
    glutInitDisplayMode(displayMode)

    glutInitWindowSize(glwindow.WIN_W, glwindow.WIN_H)
    glutCreateWindow('Triangle')

    glwindow.init()
    glutDisplayFunc(glwindow.draw)
    glutReshapeFunc(glwindow.reshape)  # 注册响应窗口改变的函数reshape()
    glutMouseFunc(glwindow.mouse_click)  # 注册响应鼠标点击的函数
    glutMotionFunc(glwindow.mouse_motion)  # 注册响应鼠标拖拽的函数
    glutKeyboardFunc(glwindow.keydown)  # 注册键盘输入的函数keydown()
    glutMainLoop()
