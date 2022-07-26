#!/usr/bin/env python3

import sys
import random
import socket
from threading import Thread
from PySide6 import QtCore, QtWidgets, QtGui

import myconstants

class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        self.button_save = QtWidgets.QPushButton('Save File')

        self.text = QtWidgets.QTextEdit('Your question will appear here...')
        self.text.setReadOnly(True)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button_save)

        self.button_save.clicked.connect(self.savefile)

        print('creating thread')
        self.thread = DownloadThread(self)

    @QtCore.Slot(bytes)
    def update_text(self, file):
        print('received data in main thread: \n', file)
        self.text.clear()
        self.text.setPlainText(file.decode('utf-8'))

    @QtCore.Slot()
    def clear(self):
        self.text.clear()

    @QtCore.Slot()
    def savefile(self):
        ret = QtWidgets.QFileDialog.getSaveFileName(self, 'Select Directory')
        filename = ret[0]
        print(f'writing {filename}')
        f = open(filename, 'ab+')
        f.write(self.text.toPlainText().encode('utf-8'))
        f.write(b'\n')

class Communicate(QtCore.QObject):
    signal_file = QtCore.Signal(bytes)

class DownloadThread(QtCore.QThread):

    data_downloaded = QtCore.Signal(str)

    def __init__(self, parent=None, file='question'):
        print('inside DownloadThread.__init__')
        super(DownloadThread, self).__init__(parent)
        print('inited')
        self.signals = Communicate()
        # connect the signal to the main thread slots
        self.signals.signal_file.connect(parent.update_text)
        print('connected')

        self.port = myconstants.PORT
        self.file = file    # File to save question in
        self.start()

    def run(self):
        self.start_server()

    def start_server(self):
        self.create_socket(self.port)
        while True:
            print('listening...')
            (clientsock, addr) = self.sock.accept()
            print('connection accepted:', addr)
            contents = self.recvfile(clientsock)
            self.signals.signal_file.emit(contents)
            print('emitted contents: ', contents)

    def create_socket(self, port):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('', self.port))
            self.sock.listen(1)
            print('socket created:', self.sock)
        except Exception as arg:
            print(f'error creating socket: {arg}\nexiting...')
            sys.exit(1)

    def recvfile(self, clientsock):
        buf = clientsock.recv(myconstants.BUFFSIZE)
        ret = buf
        while len(buf) != 0:
            print(f'received {len(buf)} bytes')
            buf = clientsock.recv(myconstants.BUFFSIZE)
            ret += buf
        print('connection closed')
        return ret

    def setfile(self, file):
        self.file = file
        print('updated filename to', self.file)

    def getfile(self):
        return self.file

def main():
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    app.exec()

if __name__ == '__main__':
    main()
