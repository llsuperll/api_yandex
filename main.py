import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from window_ui import Ui_Window
import requests


class Window(Ui_Window, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.map_zoom = 8
        self.map_ll = [37.977751, 55.757718]
        self.map_l = "map"
        self.delta = 0.1
        self.refresh_map()
        self.button_sat.clicked.connect(self.set_sat)
        self.button_scheme.clicked.connect(self.set_map)
        self.button_hybrid.clicked.connect(self.set_hybrid)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.map_zoom < 17:
            self.map_zoom += 1
        if event.key() == Qt.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
        if event.key() == Qt.Key_W:
            self.map_ll[1] += self.delta
        if event.key() == Qt.Key_S:
            self.map_ll[1] -= self.delta
        if event.key() == Qt.Key_A:
            self.map_ll[0] -= self.delta
        if event.key() == Qt.Key_D:
            self.map_ll[0] += self.delta
        self.refresh_map()

    def set_map(self):
        self.map_l = "map"
        self.refresh_map()

    def set_sat(self):
        self.map_l = "sat"
        self.refresh_map()

    def set_hybrid(self):
        self.map_l = "skl"
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": ",".join(map(str, self.map_ll)),
            "l": self.map_l,
            "z": self.map_zoom
        }
        response = requests.get(self.api_server, params=map_params)
        if not response:
            print(f"Ошибка выполнения запроса: Http статус: {response.status_code}"
                  f"({response.reason})")
        with open("tmp.png", mode="wb") as tmp:
            tmp.write(response.content)

        pixmap = QPixmap()
        pixmap.load("tmp.png")
        self.label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
