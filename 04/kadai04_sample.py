import sys
import numpy as np
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

# 制御点を格納する配列
g_ControlPoints = []

# ウィンドウサイズを保持する
g_WindowWidth = 512
g_WindowHeight = 512

#表示部分をこの関数で記入
def display():
    glClearColor(1., 1., 1., 1.) # 消去色指定
    glClear(GL_COLOR_BUFFER_BIT)

	# 制御点の描画
    glPointSize(5)
    glColor3d(0., 0., 0.)
    glBegin(GL_POINTS)
    for point in g_ControlPoints:
        glVertex2dv(point)    
    glEnd()

    # 制御点を結ぶ線分の描画
    glColor3d(1., 0., 0.)   
    glLineWidth(1)
    glBegin(GL_LINE_STRIP)
    for point in g_ControlPoints:
        glVertex2dv(point)    
    glEnd()

	# ベジェ曲線の描画
    glColor3d(0., 0., 0.)
    glLineWidth(2)
    # 【ここにベジェ曲線を描画するためのコードを記述する】
    glBegin(GL_LINE_STRIP)
    num_lines = (len(g_ControlPoints) - 1) // 3
    for i in range(0, num_lines):
        p = g_ControlPoints[i*3:i*3+4]
        for t in np.linspace(0.0, 1.0, 100):
            pt = (1-t)**3*p[0] + 3*t*(1-t)**2*p[1] + 3*t**2*(1-t)*p[2] + t**3*p[3]
            glVertex2dv(pt)
    glEnd()

    # 法線ベクトルを描画
    glColor3d(0., 0., 1.)
    glLineWidth(1)
    glBegin(GL_LINES)
    for i in range(0, num_lines):
        p = g_ControlPoints[i*3:i*3+4]
        for t in np.linspace(0.0, 1.0, 100):
            pt = (1-t)**3*p[0] + 3*t*(1-t)**2*p[1] + 3*t**2*(1-t)*p[2] + t**3*p[3]
            dpt = -3*(1-t)**2*p[0] + (9*t**2 - 12*t + 3)*p[1] + (-9*t**2 + 6*t)*p[2] + 3*t**2*p[3]
            n = np.array([-dpt[1], dpt[0]])
            n_normalized = n / np.linalg.norm(n)

            d2pt = 6*(1-t)*p[0] + (18*t - 12)*p[1] + (-18*t + 6)*p[2] + 6*t*p[3]
            det = dpt[0]*d2pt[1] - dpt[1]*d2pt[0]
            k = abs(det) / abs(np.linalg.norm(dpt)**3)

            glVertex2dv(pt)
            glVertex2dv(pt + n_normalized * k * 10000)
    glEnd()

    glFlush() #画面出力

# ウィンドウのサイズが変更されたときの処理
def resize(w, h):
    if h > 0:
        glViewport(0, 0, w, h)
        g_WindowWidth = w
        g_WindowHeight = h
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # ウィンドウ内の座標系設定
        # マウスクリックの座標と描画座標が一致するような正投影
        glOrtho(0, w, h, 0, -10, 10)
        glMatrixMode(GL_MODELVIEW)


# マウスクリックのイベント処理
def mouse(button, state, x, y):
    if state == GLUT_DOWN: 
        # 左ボタンだったらクリックした位置に制御点を置く
        if button == GLUT_LEFT_BUTTON:
            g_ControlPoints.append(np.array([x, y]))
            
        # 右ボタンだったら末尾の制御点を削除
        if button == GLUT_RIGHT_BUTTON:
            if g_ControlPoints:
                g_ControlPoints.pop()
    
    glutPostRedisplay()   

# キーが押されたときのイベント処理
def keyboard(key, x, y): 
    if key==b'q':
        pass
    elif key==b'Q':
        pass
    elif key==b'\x1b':
        exit() #b'\x1b'は ESC の ASCII コード
    
    glutPostRedisplay()

def init():
    # アンチエイリアスを有効にする
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

if __name__ == "__main__":
    glutInit(sys.argv) #ライブラリの初期化
    glutInitWindowSize(g_WindowWidth, g_WindowHeight) #ウィンドウサイズを指定
    glutCreateWindow(sys.argv[0]) #ウィンドウを作成
    glutDisplayFunc(display) #表示関数を指定
    glutReshapeFunc(resize) # ウィンドウサイズが変更されたときの関数を指定
    glutMouseFunc(mouse) # マウス関数を指定
    glutKeyboardFunc(keyboard) # キーボード関数を指定
    init() # 初期設定を行う
    glutMainLoop() #イベント待ち
