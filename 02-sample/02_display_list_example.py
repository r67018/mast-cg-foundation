import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# ディスプレイリストの学習
# 星を描画する描画命令一式を、ディスプレイリストとして作成しておき
# 必要な時に、その命令を呼び出す
ID_DRAW_STAR=1 #  glNewList 関数で使用する識別ID。値は何でも構わない

#表示部分をこの関数で記入
def display():
    glClearColor (1., 1., 1., 1.)  # 消去色指定
    glClear(GL_COLOR_BUFFER_BIT)       # 画面と奥行き情報を初期化

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glColor3d(1., 0., 0.)
    glTranslated(0.5, 0, 0)
    glCallList(ID_DRAW_STAR)
    glLoadIdentity()

    glColor3d(0., 1., 0.)
    glTranslated(0, 0.5, 0)
    glCallList(ID_DRAW_STAR)
    glLoadIdentity()

    glColor3d(0., 0., 1.)
    glTranslated(-0.5, 0, 0)
    glCallList(ID_DRAW_STAR)

    glutSwapBuffers() # バッファの入れ替え
    
#一定時間ごとに呼び出される関数
def timer(value):

    glutPostRedisplay() # 再描画命令
    glutTimerFunc(100 , timer , 0) # 100ミリ秒後に自身を実行する
    
# ディスプレイリストを作成する
def buildDisplayList():
    glNewList(ID_DRAW_STAR,GL_COMPILE)

    r0 = 0.15 # 星の内径
    r1 = 0.4 # 星の外径
    glBegin(GL_TRIANGLES)
    for i in range(5): # 5つの三角形で星を表現する
        deg = i * 72
        glVertex3d(r0 * math.cos( (deg - 36) * math.pi / 180.), r0 * math.sin( (deg - 36) * math.pi / 180.), 0)  # 内側の頂点
        glVertex3d(r1 * math.cos( deg * math.pi / 180.), r1 * math.sin( deg * math.pi / 180.), 0)  # 外側の頂点
        glVertex3d(r0 * math.cos( (deg + 36) * math.pi / 180.), r0 * math.sin( (deg + 36) * math.pi / 180.) ,0)  # 内側の頂点
    glEnd()               

    glEndList()

if __name__ == "__main__":
    glutInit(sys.argv) #ライブラリの初期化
    glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE)
    glutInitWindowSize(400, 400) #ウィンドウサイズを指定
    glutCreateWindow(sys.argv[0]) #ウィンドウを作成
    timer(0) #timer関数の実行
    glutDisplayFunc(display) #表示関数を指定
    buildDisplayList()
    glutMainLoop() #イベント待ち