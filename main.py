import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from can.interfaces.vector import VectorBus
from UDS_Client_UI import Ui_MainWindow


class MainWindows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__vectorConfigs=[]
        self.refresh_drive()

    def refresh_drive(self):
        self.vectorAvailableConfigs = VectorBus._detect_available_configs()
        self.comboBox_channel.clear()
        for channel_list in self.vectorAvailableConfigs:
            self.comboBox_channel.addItem(str(channel_list['vector_channel_config'].name) +
                                  ' ' +
                                  str(channel_list['vector_channel_config'].transceiver_name) +
                                  ' ' +
                                  str(channel_list['vector_channel_config'].serial_number))
            self.__vectorConfigs.append({'name':channel_list['vector_channel_config'].name,
                                         'transceiver_name':channel_list['vector_channel_config'].transceiver_name,
                                         'serial_number':channel_list['vector_channel_config'].serial_number,
                                         'is_on_bus':channel_list['vector_channel_config'].is_on_bus,
                                         })








if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    w = MainWindows()
    w.show()
    sys.exit(app.exec_())
