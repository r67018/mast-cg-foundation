import os

import sys
import math
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

# コッホ曲線を描画する関数
def koch_curve(x1, y1, x2, y2, level):
    if level == 0:
        # levelが0の時は直線を描画
        glVertex2d(x1, y1)
        glVertex2d(x2, y2)
    else:
        # 線分を3等分する点を計算
        dx = x2 - x1
        dy = y2 - y1

        # 1/3の点
        px1 = x1 + dx / 3
        py1 = y1 + dy / 3

        # 2/3の点
        px2 = x1 + 2 * dx / 3
        py2 = y1 + 2 * dy / 3

        # 正三角形の頂点を計算
        # px1からpx2へのベクトル
        vx = px2 - px1
        vy = py2 - py1

        # 60度回転して正三角形の頂点を求める
        # 左回りに60度回転
        cos60 = math.cos(math.pi / 3)
        sin60 = math.sin(math.pi / 3)

        # 60度を時計回りに回転させ、外側に突起が出るようにする
        qx = px1 + vx * cos60 + vy * sin60
        qy = py1 - vx * sin60 + vy * cos60

        # 再帰的に4つの線分を描画
        koch_curve(x1, y1, px1, py1, level - 1)
        koch_curve(px1, py1, qx, qy, level - 1)
        koch_curve(qx, qy, px2, py2, level - 1)
        koch_curve(px2, py2, x2, y2, level - 1)

#表示部分をこの関数で記入
def display():
    glClearColor(1., 1., 1., 1.) # 消去色指定
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3d(0., 0., 1.)   # 色指定(R,G,B)で0～1まで
    glBegin(GL_LINES)      # 描画するものを指定

    # コッホ曲線を描画
    # 正三角形の頂点を計算
    size = 0.6
    # 下の頂点
    x1 = 0.0
    y1 = -size * math.sqrt(3) / 3
    # 右上の頂点
    x2 = size / 2
    y2 = size * math.sqrt(3) / 6
    # 左上の頂点
    x3 = -size / 2
    y3 = size * math.sqrt(3) / 6

    # 3辺それぞれにコッホ曲線を適用
    level = 2 # 詳細度
    koch_curve(x1, y1, x2, y2, level) # 下→右上
    koch_curve(x2, y2, x3, y3, level) # 右上→左上
    koch_curve(x3, y3, x1, y1, level) # 左上→下

    glEnd()

    glFlush() #画面出力

if __name__ == "__main__":
    glutInit(sys.argv) #ライブラリの初期化
    glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE) #ディスプレイモードを指定
    glutInitWindowSize(400, 400) #ウィンドウサイズを指定
    glutCreateWindow(b"Koch Snowflake") #ウィンドウを作成
    glutDisplayFunc(display) #表示関数を指定
    glutMainLoop() #イベント待ち

