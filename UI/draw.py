# -*- coding:utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

color_land = [0.9, 0.9, 0.9]
color_wall = [0.5, 0.5, 0.5]
color_floor = [0.3, 0.3, 0.3]
quad = [[-1, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]]
sqare = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
wall_alpha = 0.6


def draw_wall(position, size, thickness):
    # position为底面中心位置[x, y, z]，size[length, width, height]，墙厚度thickness
    # 绘制内墙正面
    glDepthMask(GL_FALSE)
    glBegin(GL_QUADS)
    glColor4f(color_wall[0], color_wall[1], color_wall[2], wall_alpha)
    glVertex3f(position[0] + size[0] / 2, position[1], position[2] + size[1] / 2)
    glVertex3f(position[0] + size[0] / 2, position[1] + size[2], position[2] + size[1] / 2)
    glVertex3f(position[0] - size[0] / 2, position[1] + size[2], position[2] + size[1] / 2)
    glVertex3f(position[0] - size[0] / 2, position[1], position[2] + size[1] / 2)
    glEnd()
    glDepthMask(GL_TRUE)
    # 绘制外墙正面
    glDepthMask(GL_FALSE)
    glBegin(GL_QUADS)
    glColor4f(color_wall[0], color_wall[1], color_wall[2], wall_alpha)
    glVertex3f(position[0] + size[0] / 2 + thickness, position[1], position[2] + size[1] / 2 + thickness)
    glVertex3f(position[0] + size[0] / 2 + thickness, position[1] + size[2], position[2] + size[1] / 2 + thickness)
    glVertex3f(position[0] - size[0] / 2 - thickness, position[1] + size[2], position[2] + size[1] / 2 + thickness)
    glVertex3f(position[0] - size[0] / 2 - thickness, position[1], position[2] + size[1] / 2 + thickness)
    glEnd()
    glDepthMask(GL_TRUE)

    # 绘制内墙左侧、后侧、右侧
    glBegin(GL_QUAD_STRIP)
    glColor4f(color_wall[0], color_wall[1], color_wall[2], 1.0)
    for i in range(4):
        glVertex3f(position[0] + quad[i][0] * size[0] / 2, position[1], position[2] + quad[i][1] * size[1] / 2)
        glVertex3f(position[0] + quad[i][0] * size[0] / 2, position[1] + size[2], position[2] + quad[i][1] * size[1] / 2)
    glEnd()
    # 绘制外墙
    glBegin(GL_QUAD_STRIP)
    glColor4f(color_wall[0], color_wall[1], color_wall[2], 1.0)
    for i in range(4):
        glVertex3f(position[0] + quad[i][0] * (size[0] / 2 + thickness), position[1],
                   position[2] + quad[i][1] * (size[1] / 2 + thickness))
        glVertex3f(position[0] + quad[i][0] * (size[0] / 2 + thickness), position[1] + size[2],
                   position[2] + quad[i][1] * (size[1] / 2 + thickness))
    glEnd()


def draw_floor(position, length, width, thickness):
    # 绘制侧面
    glBegin(GL_QUAD_STRIP)
    glColor4f(color_floor[0], color_floor[1], color_floor[2], 1.0)
    for i in range(5):
        glVertex3f(position[0] + quad[i][0] * length / 2, position[1], position[2] + quad[i][1] * width / 2)
        glVertex3f(position[0] + quad[i][0] * length / 2, position[1] + thickness, position[2] + quad[i][1] * width / 2)
    glEnd()

    # 绘制上下底面
    glBegin(GL_QUADS)
    glColor4f(color_floor[0], color_floor[1], color_floor[2], 1.0)
    glVertex3f(position[0] + length / 2, position[1], position[2] + width / 2)
    glVertex3f(position[0] - length / 2, position[1], position[2] + width / 2)
    glVertex3f(position[0] - length / 2, position[1], position[2] - width / 2)
    glVertex3f(position[0] + length / 2, position[1], position[2] - width / 2)

    glVertex3f(position[0] + length / 2, position[1] + thickness, position[2] + width / 2)
    glVertex3f(position[0] - length / 2, position[1] + thickness, position[2] + width / 2)
    glVertex3f(position[0] - length / 2, position[1] + thickness, position[2] - width / 2)
    glVertex3f(position[0] + length / 2, position[1] + thickness, position[2] - width / 2)
    glEnd()


def draw_land(length):
    # 绘制地面
    glBegin(GL_POLYGON)
    for i in range(4):
        glColor4f(color_land[0], color_land[1], color_land[2], 1.0)
        glVertex3f(sqare[i][0] * length, 0, sqare[i][1] * length)
    glEnd()
