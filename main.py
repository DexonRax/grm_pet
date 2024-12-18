from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QMovie
import sys
import random

class DesktopPet(QMainWindow):
    def __init__(self, character):
        super().__init__()
        self.character = character
        self.animations = ["idle", "move_left", "move_right", "dance"]
        self.animationId = 0
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.setFixedSize(200, 200)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 200, 200)
        self.movie = QMovie(self.get_animation_path())

        self.movie.setScaledSize(QSize(200, 200))
        self.label.setMovie(self.movie)
        self.movie.start()

        self.setMouseTracking(True)

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.change_animation)
        self.animation_timer.start(random.randint(5000, 7000))

        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_window)
        self.move_timer.start(30)
        self.move_direction_x = 0
        self.move_direction_y = 0
        self.move_speed = 2

    def get_animation_path(self):
        return f"{self.character}/{self.animations[self.animationId]}.gif"

    def change_animation(self):
        self.animationId = random.randint(0, len(self.animations)-1)#(self.animationId + 1) % len(self.animations)
        self.movie.stop()
        self.movie = QMovie(self.get_animation_path())
        self.movie.setScaledSize(QSize(200, 200))
        self.label.setMovie(self.movie)
        self.movie.start()

        if self.animations[self.animationId] == "move_left":
            self.move_direction_x = random.uniform(-1.0, -0.1)
            self.move_direction_y = random.uniform(-1.0, 1.0)
        elif self.animations[self.animationId] == "move_right":
            self.move_direction_x = random.uniform(0.1, 1.0)
            self.move_direction_y = random.uniform(-1.0, 1.0)
        else:
            self.move_direction_x = 0
            self.move_direction_y = 0

    def move_window(self):
        if self.move_direction_x != 0:
            self.move(self.x() + int(self.move_direction_x * self.move_speed), int(self.y() + self.move_direction_y * self.move_speed))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet("eduardo")
    pet.show()
    sys.exit(app.exec_())
