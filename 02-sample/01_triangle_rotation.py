import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

rotateAngle = 0 # 回転角度を記録しておく変数

#表示部分をこの関数で記入
def display():
    glClearColor (1., 1., 1., 1.)  # 消去色指定
    glClear(GL_COLOR_BUFFER_BIT)       # 画面と奥行き情報を初期化

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotated(rotateAngle, 0, 0, 1)

    glColor3d(1., 0., 0.)   # 色指定(R,G,B)で0～1まで
    glBegin(GL_TRIANGLES)
    glVertex3d(0,     0, 0) 
    glVertex3d(0.5,   0, 0) 
    glVertex3d(0.5, 0.5, 0) 
    glEnd()                               

    glutSwapBuffers() # バッファの入れ替え
    
#一定時間ごとに呼び出される関数
def timer(value):
    global rotateAngle
    rotateAngle+=1 # 回転角度の更新

    glutPostRedisplay() # 再描画命令
    glutTimerFunc(100 , timer , 0) # 100ミリ秒後に自身を実行する


if __name__ == "__main__":
    glutInit(sys.argv) #ライブラリの初期化
    glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE)
    glutInitWindowSize(400, 400) #ウィンドウサイズを指定
    glutCreateWindow(sys.argv[0]) #ウィンドウを作成
    timer(0) #timer関数の実行
    glutDisplayFunc(display) #表示関数を指定
    glutMainLoop() #イベント待ち