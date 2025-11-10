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

# Bスプラインの次数
g_Degree = 3

# ノットベクトル
# この配列の値を変更することで基底関数が変化する。その結果として形が変わる。
# 下の例では、一定間隔で値が変化するので、「一様Bスプライン曲線」となる
# g_NotVector = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 課題(2)では次のノットベクトルを変更する
# g_NotVector = [0, 0, 0, 0, 1, 1, 1, 1]

g_NotVector = list(range(0, 20))

# 基底関数 N{i,n}(t)の値を計算する
def getBaseN(i, n, t):
    if n == 0:
        # n が 0 の時だけ t の値に応じて 0 または 1 を返す
        if g_NotVector[i] <= t < g_NotVector[i + 1]:
            return 1.0
        return 0.0
    else:
        # 係数を計算するときに、ノットが重なる（分母がゼロとなる）ときには、その項を無視する

        ####
        # ここにコードを追加する
        ####

        denom1 = g_NotVector[i+n] - g_NotVector[i]
        if denom1 > 0:
            term1 = (t-g_NotVector[i]) / (g_NotVector[i+n]-g_NotVector[i]) * getBaseN(i, n-1, t)
        else:
            term1 = 0.

        denom2 = g_NotVector[i+n+1]-g_NotVector[i+1]
        if denom2 > 0:
            term2 = (g_NotVector[i+n+1]-t) / (g_NotVector[i+n+1]-g_NotVector[i+1]) * getBaseN(i+1, n-1, t)
        else:
            term2 = 0.

        return term1 + term2


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

    # ここにBスプライン曲線を描画するプログラムコードを入れる
    # ヒント1: 3次Bスプラインの場合は制御点を4つ入れるまでは何も描けない
    # ヒント2: パラメータtの値の取り得る範囲に注意

    n = g_Degree
    if len(g_ControlPoints) >= n + 1:
        t_start = g_NotVector[n]
        t_end = g_NotVector[len(g_ControlPoints)]

        glColor3d(0., 0., 0.)
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)

        for t in np.linspace(t_start, t_end-0.0001, 100):
            p = np.array([0., 0.])
            for i in range(len(g_ControlPoints)):
                N = getBaseN(i, n, t)
                p += N * g_ControlPoints[i]
            glVertex2dv(p)
        glEnd()

        # セグメントの境界点を描画
        glPointSize(8)
        glColor3d(0., 0., 1.)
        glBegin(GL_POINTS)
        for t_knot in range(int(t_start), int(t_end)):
            if t_knot >= t_start and t_knot < t_end:
                p = np.array([0., 0.])
                for i in range(len(g_ControlPoints)):
                    N = getBaseN(i, n, t_knot)
                    p += N * g_ControlPoints[i]
                glVertex2dv(p)
        glEnd()

        # 法線ベクトルの描画
        glColor3d(0., 0., 1.)
        glLineWidth(1)
        normal_length = 30.0  # 法線ベクトルの長さ

        num_normals = 100  # 法線を表示する数
        glBegin(GL_LINES)
        for t in np.linspace(t_start, t_end-0.0001, num_normals):
            # 現在の点を計算
            p = np.array([0., 0.])
            for i in range(len(g_ControlPoints)):
                N = getBaseN(i, n, t)
                p += N * g_ControlPoints[i]

            # 接線ベクトルを近似計算
            delta_t = 0.01
            p_next = np.array([0., 0.])
            for i in range(len(g_ControlPoints)):
                N_next = getBaseN(i, n, min(t + delta_t, t_end - 0.0001))
                p_next += N_next * g_ControlPoints[i]

            # 接線ベクトル
            tangent = p_next - p
            tangent_norm = np.linalg.norm(tangent)

            if tangent_norm > 1e-6:  # ゼロ除算を避ける
                # 接線を正規化
                tangent = tangent / tangent_norm

                # 90度回転
                normal = np.array([-tangent[1], tangent[0]])

                p_end = p + normal * normal_length
                glVertex2dv(p)
                glVertex2dv(p_end)
        glEnd()

    # 基底関数のグラフを描画
    if len(g_ControlPoints) >= g_Degree + 1:
        graph_height = 150  # グラフの高さ
        graph_y_offset = g_WindowHeight - graph_height  # グラフの開始Y座標
        graph_x_margin = 50
        graph_width = g_WindowWidth - 2 * graph_x_margin

        # グラフのの背景
        glColor3d(0.95, 0.95, 0.95)
        glBegin(GL_QUADS)
        glVertex2d(graph_x_margin, graph_y_offset)
        glVertex2d(g_WindowWidth - graph_x_margin, graph_y_offset)
        glVertex2d(g_WindowWidth - graph_x_margin, g_WindowHeight - 10)
        glVertex2d(graph_x_margin, g_WindowHeight - 10)
        glEnd()

        # 軸
        glColor3d(0., 0., 0.)
        glLineWidth(1)
        glBegin(GL_LINES)
        # 横軸
        glVertex2d(graph_x_margin, g_WindowHeight - 10)
        glVertex2d(g_WindowWidth - graph_x_margin, g_WindowHeight - 10)
        # 縦軸
        glVertex2d(graph_x_margin, graph_y_offset)
        glVertex2d(graph_x_margin, g_WindowHeight - 10)
        glEnd()

        t_start = g_NotVector[g_Degree]
        t_end = g_NotVector[len(g_ControlPoints)]
        t_range = t_end - t_start

        if t_range > 0:
            # 基底関数の色
            colors = [
                (1.0, 0.0, 0.0),  # 赤
                (0.0, 0.7, 0.0),  # 緑
                (0.0, 0.0, 1.0),  # 青
                (1.0, 0.5, 0.0),  # オレンジ
                (0.5, 0.0, 0.5),  # 紫
                (0.0, 0.7, 0.7),  # シアン
                (1.0, 0.0, 1.0),  # マゼンタ
            ]

            for i in range(len(g_ControlPoints)):
                color = colors[i % len(colors)]
                glColor3d(*color)
                glLineWidth(2)
                glBegin(GL_LINE_STRIP)

                for t in np.linspace(t_start, t_end - 0.0001, 200):
                    N = getBaseN(i, g_Degree, t)
                    # tの値を画面のx座標に変換
                    x = graph_x_margin + (t - t_start) / t_range * graph_width
                    # Nの値を画面のy座標に変換
                    y = g_WindowHeight - 10 - N * (graph_height - 20)
                    glVertex2d(x, y)

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
            # ノット数を増やせばいくらでも制御点を追加できるが、今回はノットベクトルが固定されているので
            # いくらでも追加できるわけではない
            if len(g_ControlPoints) < len(g_NotVector) - (g_Degree + 1):
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
