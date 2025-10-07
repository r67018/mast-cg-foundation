import os
os.environ['PYOPENGL_PLATFORM'] = 'glx'

import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

#表示部分をこの関数で記入
def display():
    glClearColor(1., 1., 1., 1.) # 消去色指定
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3d(0., 0., 0.)   # 色指定(R,G,B)で0～1まで
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        x = math.cos(i * 3.14159 /180.)
        y = math.sin(i * 3.14159 /180.)
        glVertex2d(x * 0.6, y * 0.6)
    glEnd()

    glFlush() #画面出力

if __name__ == "__main__":
    glutInit(sys.argv) #ライブラリの初期化
    glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE) #ディスプレイモードを指定
    glutInitWindowSize(400, 400) #ウィンドウサイズを指定
    glutCreateWindow(b"Draw Circle") #ウィンドウを作成
    glutDisplayFunc(display) #表示関数を指定
    glutMainLoop() #イベント待ち