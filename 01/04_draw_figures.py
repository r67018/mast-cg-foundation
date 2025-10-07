import os
os.environ['PYOPENGL_PLATFORM'] = 'glx'

import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

#表示部分をこの関数で記入
def display():
    glClearColor(1., 1., 1., 1.) # 消去色指定
    glClear(GL_COLOR_BUFFER_BIT)

    # 1つ目の図形
    glColor3d(1., 0.5, 0.)   # 色指定(R,G,B)で0～1まで
    glBegin(GL_QUADS)     # 描画するものを指定
    glVertex2d(-0.3,  0.) # 頂点位置の指定(1つめ)
    glVertex2d(-0.3, -0.4) # 頂点位置の指定(2つめ)
    glVertex2d( 0.3, -0.4) # 頂点位置の指定(3つめ)
    glVertex2d( 0.3,  0.) # 頂点位置の指定(4つめ)
    glEnd()

    # 2つ目の図形
    glColor3d(0., 1., 0.)   # 色指定(R,G,B)で0～1まで
    glBegin(GL_TRIANGLES)      # 描画するものを指定
    glVertex2d( 0., 0.9) # 頂点位置の指定(1つめ)
    glVertex2d(-0.7, 0.) # 頂点位置の指定(2つめ)
    glVertex2d( 0.7, 0.) # 頂点位置の指定(3つめ)
    glEnd()

    glFlush() # 画面出力

if __name__ == "__main__":
    glutInit(sys.argv) #ライブラリの初期化
    glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE) #ディスプレイモードを指定
    glutInitWindowSize(400, 400) #ウィンドウサイズを指定
    glutCreateWindow(b"Draw Figures") #ウィンドウを作成
    glutDisplayFunc(display) #表示関数を指定
    glutMainLoop() #イベント待ち