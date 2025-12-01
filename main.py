import sys
import math
from pathlib import Path
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie, QTransform, QCursor
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QDesktopWidget

ASSETS_DIR = Path(__file__).parent / "assets"
WALK_FILENAME = "cat_walk.gif"

UPDATE_INTERVAL_MS = 30
SPEED = 4.4
CLICK_THROUGH = False


class CatFollower(QWidget):
    def __init__(self):
        super().__init__(None, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        if CLICK_THROUGH:
            self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.label = QLabel(self)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.label.setScaledContents(True)

        self.facing_right = True

        path = ASSETS_DIR / WALK_FILENAME
        self.movie = QMovie(str(path))
        self.movie.frameChanged.connect(self.on_movie_frame)
        self.movie.start()

        self.resize(self.movie.currentPixmap().size())
        self.label.resize(self.size())

        screen = QDesktopWidget().availableGeometry()
        self.pos_f = (20.0, float(screen.height() - self.height() - 20))
        self.move(int(self.pos_f[0]), int(self.pos_f[1]))

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(UPDATE_INTERVAL_MS)

    def on_movie_frame(self):
        pm = self.movie.currentPixmap()
        if pm.isNull():
            return
        if not self.facing_right:
            pm = pm.transformed(QTransform().scale(-1, 1))
        self.label.setPixmap(pm)

    def update_position(self):
        cur = QCursor.pos()

        target_x = cur.x() - self.width() / 2
        target_y = cur.y() - self.height() / 2

        cat_x, cat_y = self.pos_f
        dx = target_x - cat_x
        dy = target_y - cat_y
        dist = math.hypot(dx, dy)

        if dist > 1:
            nx = dx / dist
            ny = dy / dist

            new_facing = dx > 0
            if new_facing != self.facing_right:
                self.facing_right = new_facing
                self.on_movie_frame()

            cat_x += nx * SPEED
            cat_y += ny * SPEED
            self.pos_f = (cat_x, cat_y)
            self.move(int(cat_x), int(cat_y))

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            QApplication.instance().quit()


def main():
    app = QApplication(sys.argv)
    w = CatFollower()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
