# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *

from UI.draw import *
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class GLWindow(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWindow, self).__init__(parent)

    def initializeGL(self):
        glutInit()
        '''displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
        glutInitDisplayMode(displayMode)'''
        # glutCreateWindow('Triangle')

        glClearColor(0, 0, 0, 1.0)
        glEnable(GL_DEPTH_TEST)     # 开启深度测试，实现遮挡关系
        glDepthFunc(GL_LEQUAL)      # 设置深度测试函数,GL_LEQUAL只是选项之一

    def paintGL(self):
        # glutWireSphere(2, 16, 16)
        glPointSize(20)
        glColor4f(1, 1, 1, 1)
        glVertex3f(0, 0, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GLWindow()
    window.show()
    sys.exit(app.exec_())
