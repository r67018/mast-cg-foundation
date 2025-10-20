import os

import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

#表示部分をこの関数で記入
def display():
    glClearColor(1., 1., 1., 1.) # 消去色指定
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3d(0., 0., 1.)   # 色指定(R,G,B)で0～1まで
    glBegin(GL_LINE_STRIP)      # 描画するものを指定
    l = 1
    for _ in range(10):
        glVertex2d(l, l)
        glVertex2d(l, -l)
        glVertex2d(-l, -l)
        glVertex2d(-l, l - 0.1)
        l -= 0.1
    glEnd()

    glFlush() #画面出力

if __name__ == "__main__":
    glutInit(sys.argv) #ライブラリの初期化
    glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE) #ディスプレイモードを指定
    glutInitWindowSize(400, 400) #ウィンドウサイズを指定
    glutCreateWindow(b"Draw Lines") #ウィンドウを作成
    glutDisplayFunc(display) #表示関数を指定
    glutMainLoop() #イベント待ち