#!/usr/bin/env python3

import sys
import random
import socket
import subprocess
from threading import Thread
from PySide6 import QtCore, QtWidgets, QtGui

import myconstants

class MyWidget(QtWidgets.QWidget):

    @QtCore.Slot()
    def set_list(self):
        ret = QtWidgets.QFileDialog.getOpenFileName(self, 'Select File')
        self.listfile = ret[0]
        print(f"system list file: '{self.listfile}'")

    @QtCore.Slot()
    def set_qdir(self):
        ret = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.qdir = ret
        print(f"question dir: '{self.qdir}'")

    @QtCore.Slot()
    def set_logfile(self):
        ret = QtWidgets.QFileDialog.getSaveFileName(self, 'Select Log file')
        self.logfile = ret[0]
        print(f"logfile: '{self.logfile}'")

    def handle_stdout(self):
        print('handling output')
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode('utf8')
        self.text.append(stdout)
        print(stdout)
        print('handled output')

    def handle_stderr(self):
        print('handling stderr')
        data = self.p.readAllStandardError()
        print(bytes(data))
        stderr = bytes(data).strip().decode('utf8')
        self.text.setTextColor(QtGui.QColor(255, 0, 0))
        self.text.append(stderr)
        self.text.setTextColor(QtGui.QColor(0, 0, 0))

    def handle_state(self, state):
        if state == QtCore.QProcess.Starting:
            self.text.append(f"System List: '{self.listfile}'\n" +
                             f"Question Directory: '{self.qdir}'\n" +
                             f"Log File: '{self.logfile}'\n")
            print('Starting')
            self.text.append('Starting\n'
                             '========')

    def proc_finished(self):
        self.text.append('\n========\n'
                         'Finished')
        self.p = None

    @QtCore.Slot()
    def runclient(self):
        if self.p is None:
            self.p = QtCore.QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.proc_finished)
            cmd = ['./client.py', '-v', '-l', self.listfile, '-q', self.qdir,
                   '-L', self.logfile]
            print('cmd:', cmd)
            self.text.append('command: ' + ' '.join(cmd))
            self.p.start('python3', cmd)

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)

        self.choose_list = QtWidgets.QPushButton('Choose System List')
        self.choose_qdir = QtWidgets.QPushButton('Choose Question Directory')
        self.choose_logf = QtWidgets.QPushButton('Choose Log File')
        self.send        = QtWidgets.QPushButton('Send')

        self.text = QtWidgets.QTextEdit('')
        self.text.setReadOnly(True)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.choose_list)
        self.layout.addWidget(self.choose_qdir)
        self.layout.addWidget(self.choose_logf)
        self.layout.addWidget(self.send)

        self.choose_list.clicked.connect(self.set_list)
        self.choose_qdir.clicked.connect(self.set_qdir)
        self.choose_logf.clicked.connect(self.set_logfile)
        self.send.clicked.connect(self.runclient)

        self.listfile = myconstants.LISTFILE
        self.qdir = myconstants.QDIR
        self.logfile = myconstants.LOGFILE

        # To run process
        self.p = None

def main():
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(350, 350)
    widget.show()
    app.exec()

if __name__ == '__main__':
    main()
