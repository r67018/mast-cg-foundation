import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# ディスプレイリストの学習
# 星を描画する描画命令一式を、ディスプレイリストとして作成しておき
# 必要な時に、その命令を呼び出す
ID_DRAW_CIRCLE = 1
ID_DRAW_MOUNTAIN = 2
ID_DRAW_BG = 3
ID_DRAW_SUN_RAYS = 4
ID_DRAW_STAR = 5

rotateAngle = 0

#表示部分をこの関数で記入
def display():
    glClearColor (1., 1., 1., 1.)  # 消去色指定
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # 空
    glPushMatrix()
    glColor3d(0.4, 0.6, 1)
    glRotated(rotateAngle - 90, 0, 0, 1)
    glCallList(ID_DRAW_BG)
    glPopMatrix()
    # 夜空
    glPushMatrix()
    glColor3d(0.05, 0.05, 0.2)
    glRotated(rotateAngle - 270, 0, 0, 1)
    glCallList(ID_DRAW_BG)
    glPopMatrix()

    # 太陽
    scale = (rotateAngle - 180) * 2 % 360 / 360
    glPushMatrix()
    glColor3d(1, 0.2, 0)
    glRotated(rotateAngle, 0, 0, 1)
    glTranslated(0.7, 0, 0)
    glScaled(scale, scale, 1)
    glCallList(ID_DRAW_CIRCLE)
    # 太陽の光線
    glRotate(rotateAngle * 2, 0, 0, 1)
    glCallList(ID_DRAW_SUN_RAYS)
    glPopMatrix()

    # 月
    glPushMatrix()
    glColor3d(1, 1, 0)
    glRotated(rotateAngle + 180, 0, 0, 1)
    glTranslated(0.7, 0, 0)
    glCallList(ID_DRAW_CIRCLE)

    # 星
    random.seed(0)
    for i in range(20):
        glPushMatrix()
        dx = random.uniform(-1.0, 1.0)
        dy = random.uniform(-1.0, 1.0)
        glTranslated(dx, dy, 0)
        glScaled(0.2, 0.2, 0)
        glCallList(ID_DRAW_STAR)
        glPopMatrix()
    glPopMatrix()

    # 山
    glPushMatrix()
    glColor3d(0, 1, 0)
    glCallList(ID_DRAW_MOUNTAIN)
    glPopMatrix()

    glutSwapBuffers() # バッファの入れ替え
    
#一定時間ごとに呼び出される関数
def timer(value):
    global rotateAngle
    rotateAngle += 5 # 回転角度の更新
    glutPostRedisplay() # 再描画命令
    glutTimerFunc(100 , timer , 0) # 100ミリ秒後に自身を実行する
    
# ディスプレイリストを作成する
def buildDisplayList():
    # 円
    glNewList(ID_DRAW_CIRCLE, GL_COMPILE)

    r = 0.2 # 半径
    num_lines = 50
    glBegin(GL_TRIANGLE_FAN)
    for i in range(num_lines):
        angle = i * 2.0 * math.pi / num_lines
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        glVertex2f(x, y)
    glEnd()
    glEndList()

    glNewList(ID_DRAW_SUN_RAYS, GL_COMPILE)
    num_rays = 12
    ray_length = 0.2
    glLineWidth(3.0)
    glBegin(GL_LINES)
    for i in range(num_rays):
        angle = i * 2.0 * math.pi / num_rays
        
        x_start = r * math.cos(angle)
        y_start = r * math.sin(angle)
        
        x_end = (r + ray_length) * math.cos(angle)
        y_end = (r + ray_length) * math.sin(angle)
        
        glVertex2f(x_start, y_start)
        glVertex2f(x_end, y_end)
    glEnd()
    glLineWidth(1.0)
    glEndList()

    # 山
    glNewList(ID_DRAW_MOUNTAIN, GL_COMPILE)
    glBegin(GL_POLYGON)
    glVertex2f(-1.0, -1.0) 
    # 山の頂点
    glVertex2f(-1.0, 0)
    glVertex2f(-0.7, 0.2)
    glVertex2f(-0.5, -0.2)
    glVertex2f(-0.3, 0.3)
    glVertex2f(0.0, 0)
    glVertex2f(0.3, 0.4)
    glVertex2f(0.6, 0.1)
    glVertex2f(0.9, 0.2)
    glVertex2f(1.0, 0)
    # 画面下端の右端
    glVertex2f(1.0, -1.0)
    glEnd()
    glEndList()

    # 星
    glNewList(ID_DRAW_STAR, GL_COMPILE)
    glBegin(GL_QUADS)
    glVertex2f(0.1, 0)
    glVertex2f(0, 0.1)
    glVertex2f(-0.1, 0)
    glVertex2f(0, -0.1)
    glEnd()
    glEndList()

    glNewList(ID_DRAW_BG, GL_COMPILE)
    glBegin(GL_QUADS)
    glVertex2f(-1.5, 0)
    glVertex2f(1.5, 0)
    glVertex2f(1.5, 1.5)
    glVertex2f(-1.5, 1.5)
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


