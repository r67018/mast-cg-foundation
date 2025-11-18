import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

vertices = []
faces = []
normals = []

# マウスドラッグ用の変数
last_x, last_y = 0, 0
rotation_x, rotation_y = 0, 0

# ズーム用の変数
zoom_factor = -5.0

# 頂点の表示フラグ
show_vertices = True

# 辺の表示フラグ
show_edges = False

# 面の表示フラグ
show_faces = True

# 面の表示方法
normal_visualization = True


# OBJファイルを読み込む関数
def load_obj(filename):
    global vertices, faces, normals
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):  # 頂点情報
                parts = line.split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '):  # 面情報
                parts = line.split()
                face = []
                for part in parts[1:]:
                    face.append(int(part.split('/')[0]) - 1)  # 頂点インデックスは1から始まるので-1
                faces.append(face)

    # 法線ベクトルを計算
    calculate_normals()

# 法線を計算する関数（フラットシェーディング用）
def calculate_normals():
    global normals
    for face in faces:
        v1 = np.array(vertices[face[1]]) - np.array(vertices[face[0]])
        v2 = np.array(vertices[face[2]]) - np.array(vertices[face[0]])
        normal = np.cross(v1, v2)
        normal = normal / np.linalg.norm(normal)  # 正規化
        normals.append(normal)

# 頂点の正規化を行う関数
def normalize_vertices():
    global vertices
    vertices = np.array(vertices)

    # 各座標軸(x, y, z)の最大値と最小値を取得
    min_vals = vertices.min(axis=0)
    max_vals = vertices.max(axis=0)

    # 中心点を計算
    center = (max_vals + min_vals) / 2.0

    # 最大幅を計算
    max_extent = (max_vals - min_vals).max()

    # 頂点を中心に移動し、最大幅が1になるようにスケーリング
    vertices = (vertices - center) / max_extent

# 3Dモデルを描画する関数
def display():
    global rotation_x, rotation_y, zoom_factor, show_vertices, show_edges, show_faces, normal_visualization
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # 光源の設定（回転前に光源を固定）
    light_position = [1.0, 1.0, 1.0, 0.0]  # 左上から光が当たるように設定
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # カメラの位置をズームに応じて調整
    glTranslatef(0.0, 0.0, zoom_factor)

    # モデルの回転
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)


    # 頂点の表示
    if show_vertices:
        glDisable(GL_LIGHTING)  
        glColor3f(0.0, 0.0, 0.0)
        glPointSize(3)        
        glBegin(GL_POINTS)
        for v in vertices:
            glVertex3fv(v)
        glEnd()


    # 面の描画
    if show_faces:
        if normal_visualization:
            glDisable(GL_LIGHTING)  
        else:
            glEnable(GL_LIGHTING)  

        glEnable(GL_POLYGON_OFFSET_FILL)  # ポリゴンオフセットを有効化
        glPolygonOffset(1.0, 1.0)  # オフセット量を設定
        for i, face in enumerate(faces):
            glNormal3fv(normals[i])  # 面ごとの法線を設定
            glColor3f(normals[i][0] * 0.5 + 0.5, normals[i][1] * 0.5 + 0.5, normals[i][2] * 0.5 + 0.5)
            glBegin(GL_POLYGON)
            for vertex in face:
                glVertex3fv(vertices[vertex])
            glEnd()
        glDisable(GL_POLYGON_OFFSET_FILL)  # ポリゴンオフセットを無効化
        glDisable(GL_LIGHTING)  # 面描画が終わったら照明をオフ

    # 辺の表示
    if show_edges:
        glDisable(GL_LIGHTING)  # 照明をオフにする
        glColor3f(0.0, 0.0, 0.0)  # 黒色
        glLineWidth(1.0)
        glBegin(GL_LINES)
        for face in faces:
            for i in range(len(face)):
                v1 = vertices[face[i]]
                v2 = vertices[face[(i + 1) % len(face)]]
                glVertex3fv(v1)
                glVertex3fv(v2)
        glEnd()

    glutSwapBuffers()

# 画面のリサイズに対応する関数
def resizeWindow(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# キーボード入力の処理
def keyboard(key, x, y):
    global show_edges, show_faces, normal_visualization, show_vertices
    if key == b'q' or key == b'\033':  # 'q' or ESCで終了
        sys.exit()
    elif key == b'v':  # 'e'キーで辺の表示を切り替え
        show_vertices = not show_vertices
        glutPostRedisplay()
    elif key == b'e':  # 'e'キーで辺の表示を切り替え
        show_edges = not show_edges
        glutPostRedisplay()
    elif key == b'f':  # 'f'キーで面の表示を切り替え
        show_faces = not show_faces
        glutPostRedisplay()
    elif key == b'n':  # 'n'キーでnormal visualizationを切り替え
        normal_visualization = not normal_visualization
        glutPostRedisplay()

# マウスドラッグでの回転操作を処理する関数
def mouse_motion(x, y):
    global last_x, last_y, rotation_x, rotation_y
    dx = x - last_x
    dy = y - last_y
    rotation_x += dy * 0.5
    rotation_y += dx * 0.5
    last_x, last_y = x, y
    glutPostRedisplay()

# マウスクリックイベントを処理する関数
def mouse(button, state, x, y):
    global last_x, last_y
    if state == GLUT_DOWN:
        last_x, last_y = x, y

# マウスホイールでズームを操作する関数
def mouse_wheel(button, direction, x, y):
    global zoom_factor
    if direction > 0:
        zoom_factor += 0.5  # ズームイン
    else:
        zoom_factor -= 0.5  # ズームアウト
    glutPostRedisplay()

# OpenGLの初期化
def initOpenGL():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)  # 法線の自動正規化
    glEnable(GL_LIGHTING)  # ライティングを有効化
    glEnable(GL_LIGHT0)

    # 背景を白に設定
    glClearColor(1.0, 1.0, 1.0, 1.0)

# メインプログラム
def main(filename):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"OBJ Model Viewer")
    glutDisplayFunc(display)
    glutReshapeFunc(resizeWindow)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(mouse_motion)  # マウスドラッグを検知
    glutMouseWheelFunc(mouse_wheel)  # マウスホイールによるズームを検知

    initOpenGL()
    load_obj(filename)  # OBJファイルの読み込み
    normalize_vertices()  # 頂点の正規化

    glutMainLoop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python obj_view.py <obj_file>")
        print("Keyboard controls:")
        print("  'q' or ESC  : Quit the program")
        print("  'v'         : Toggle vertex display (on/off)")
        print("  'e'         : Toggle edge display (on/off)")
        print("  'f'         : Toggle face display (on/off)")
        print("  'n'         : Toggle normal visualization (on/off)")
        print("Mouse controls:")
        print("  Left-drag   : Rotate the object")
        print("  Scroll wheel: Zoom in/out")
        sys.exit(1)
    main(sys.argv[1])
