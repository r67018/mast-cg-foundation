import os
os.environ['PYOPENGL_PLATFORM'] = 'glx'

import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = [] #描画対象の頂点を格納するリスト
w, h = 400, 400

#表示部分をこの関数で記入
def display():
    glClearColor(1., 1., 1., 1.) # 消去色指定
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3d(1., 0., 0.)   # 色指定(R,G,B)で0～1まで
    glPointSize(10.0)       # 大きさを指定
    glBegin(GL_POINTS)      # 描画するものを指定
    for v in vertices:
        glVertex2d(v[0],v[1]) # 頂点位置の指定(1つめ)
    glEnd()
    glFlush() #画面出力

def keyboard(key, x, y):
    if key==b'q':
        glutLeaveMainLoop()# キーボードの[q]が押されたときの処理（GLUTのイベントループを終了）

def mouse(button, state, x, y):
    w, h = glutGet(GLUT_WINDOW_WIDTH),glutGet(GLUT_WINDOW_HEIGHT) #ウィンドウサイズを取得
    x_, y_ = (x-(w/2))/(w/2), -(y-(h/2))/(h/2) #x,yはピクセル座標なので-1~1になるように正規化

    if button==GLUT_LEFT_BUTTON and state==GLUT_DOWN: #左クリックで押したとき
        vertices.append([x_,y_]) #リストに描画対象の座標(_x, _y)を追加
    if button==GLUT_RIGHT_BUTTON and state==GLUT_DOWN: #右クリックで押したとき
        if vertices: #リストの中が空じゃなければ
            vertices.pop() #リストの最後の要素を削除

if __name__ == "__main__":
    glutInit(sys.argv) #ライブラリの初期化
    glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE) #ディスプレイモードを指定
    glutInitWindowSize(w, h) #ウィンドウサイズを指定
    glutCreateWindow(b"Key and Mouse") #ウィンドウを作成
    glutDisplayFunc(display) #表示関数を指定
    glutKeyboardFunc(keyboard) #キーボード関数の登録
    glutMouseFunc(mouse) #マウス関数の登録
    glutMainLoop() #イベント待ち