import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

#表示部分をこの関数で記入
def display():
    glClearColor(1., 1., 1., 1.) # 消去色指定
    glClear(GL_COLOR_BUFFER_BIT) # 画面消去

    "ここに描画に関するプログラムコードを入れる "

    glFlush() #画面出力

if __name__ == "__main__":
    glutInit(sys.argv) #ライブラリの初期化
    glutInitWindowSize(400, 400) #ウィンドウサイズを指定
    glutCreateWindow(sys.argv[0]) #ウィンドウを作成
    glutDisplayFunc(display) #表示関数を指定
    glutMainLoop() #イベント待ち