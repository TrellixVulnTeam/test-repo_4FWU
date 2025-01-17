import sys
import os
from time import strftime, gmtime
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickWindow
from PyQt6.QtCore import QObject, pyqtSignal
import threading
from time import sleep

curr_time = strftime("%H:%M:%S", gmtime())


class Backend(QObject):
    def __init__(self):
        QObject.__init__(self)

    updated = pyqtSignal(str, arguments=['updater'])

    def updater(self, curr_time):
        self.upated.emit(curr_time)

    def bootUp(self):
        t_thread = threading.Thread(target=self.bootUp)
        t_thread.daemon = True
        t_thread.start()

    def _bootUP(self):
        while True:
            curr_time = strftime("%H:%M:%S", gmtime())
            print(curr_time)
            self.updater(curr_time)
            sleep(0.1)


QQuickWindow.setSceneGraphBackend('software')
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('./UI/main.qml')
back_end = Backend()
engine.rootObjects()[0].setProperty('backend', back_end)
engine.rootObjects()[0].setProperty('currTime', curr_time)
back_end.bootUp()
sys.exit(app.exec())
