# Computer Graphics Foundation

このプロジェクトは、NixとPoetryを使用した再現可能な開発環境で、OpenGLを使ったコンピュータグラフィックスの基礎を学ぶためのものです。

## 環境構築

### 前提条件

- Nix（Flakesが有効になっていること）
- X11ディスプレイサーバー（Linuxの場合）

### 開発環境の起動

```bash
$ nix develop
```

これにより、Python 3.13とPyOpenGL、必要なシステムライブラリがすべて含まれた開発環境に入ります。
環境変数`PYOPENGL_PLATFORM=glx`が自動的に設定され、01/以下のすべてのサンプルプログラムが変更なしで動作します。

## サンプルプログラムの実行

`01/`ディレクトリには、OpenGLの基礎を学ぶためのサンプルプログラムが含まれています。

```bash
# 開発環境に入る
$ nix develop

# シンプルなウィンドウを表示
$ python 01/01_simple_window.py

# 線を描画
$ python 01/02_draw_lines.py

# 三角形を描画
$ python 01/03_draw_triangle.py

# 図形を描画
$ python 01/04_draw_figures.py

# forループを使った描画
$ python 01/05_for_loop.py

# 円を描画
$ python 01/06_draw_circle.py

# キーボードとマウスのイベント処理
# （左クリックで点を追加、右クリックで削除、qキーで終了）
$ python 01/07_key_and_mouse.py
```

## 依存関係

このプロジェクトは以下のライブラリを使用しています：

- Python 3.13
- PyOpenGL 3.1.9
- PyOpenGL-accelerate 3.1.9
- freeglut（システムライブラリ）
- libGL、libGLU（OpenGLライブラリ）

## トラブルシューティング

### ディスプレイエラーが発生する場合

X11ディスプレイサーバーが起動していることを確認してください。WSL2を使用している場合は、X serverソフトウェア（VcXsrv、X410など）が必要です。

```bash
# DISPLAY環境変数を確認
$ echo $DISPLAY
```

### OpenGLのバージョンを確認

```bash
$ nix develop --command python -c "import OpenGL; print('OpenGL version:', OpenGL.__version__)"
```

## 技術的な詳細

- `flake.nix`で`PYOPENGL_PLATFORM=glx`環境変数を設定することで、PyOpenGLがGLXプラットフォームを使用するようになります
- これにより、01/以下のPythonファイルを一切変更することなく、すべてのサンプルが動作します
- `LD_LIBRARY_PATH`も自動的に設定され、必要なOpenGLライブラリが読み込まれます
