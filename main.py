import queue
import sys

from PyQt5.QtCore import QThread, QCoreApplication, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
import can
from can.interfaces.vector import VectorBus, xldefine, get_channel_configs, VectorBusParams, VectorCanParams, \
    VectorCanFdParams
from udsoncan import NegativeResponseException, TimeoutException, UnexpectedResponseException, InvalidResponseException, \
    services, Request, Response
# from udsoncan.services import *

from UDS_Client_UI import Ui_MainWindow
import isotp

from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
import udsoncan.configs


class CANbusThread(QThread):
    def __init__(self):
        super().__init__()


class MainWindows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.vectorConfigs = []

        self.channel_choose = 0
        self.appName = 'UDS Client'
        self.vectorChannelCanParams = None
        self.is_run = False

        self.refresh_ui()
        self.init()

    def set_canParams(self):
        can_params = VectorCanParams(
            bitrate=5000,
            sjw=1,
            tseg1=1,
            tseg2=1,
            sam=1,
            output_mode=xldefine.XL_OutputMode.XL_OUTPUT_MODE_NORMAL,
            can_op_mode=xldefine.XL_CANFD_BusParams_CanOpMode.XL_BUS_PARAMS_CANOPMODE_CAN20
        )
        canfd_params = VectorCanFdParams(
            bitrate=5000,
            data_bitrate=20000,
            sjw_abr=1,
            tseg1_abr=1,
            tseg2_abr=1,
            sam_abr=1,
            sjw_dbr=1,
            tseg1_dbr=1,
            tseg2_dbr=1,
            output_mode=xldefine.XL_OutputMode.XL_OUTPUT_MODE_NORMAL,
            can_op_mode=xldefine.XL_CANFD_BusParams_CanOpMode.XL_BUS_PARAMS_CANOPMODE_CANFD
        )

        self.vectorChannelCanParams = VectorBusParams(
            bus_type=xldefine.XL_BusTypes.XL_BUS_TYPE_CAN,
            can=can_params,
            canfd=canfd_params
        )

    def init(self):
        self.send_queue = queue.Queue()
        self.rec_queue = queue.Queue()
        self.pushButton_start.clicked.connect(self.run_bus)
        self.comboBox_channel.activated.connect(self.update_channel_cfg_ui)
        self.pushButton_send.clicked.connect(self.send_uds)

        self.set_canParams()

    def refresh_ui(self):
        self.refresh_drive();
        self.update_channel_lists_ui()
        # 重新加载后将channel_choose复位
        self.channel_choose = 0
        self.update_channel_cfg_ui()

    def refresh_drive(self):
        self.__vectorAvailableConfigs = get_channel_configs()
        self.vectorConfigs.clear()
        for channel_list in self.__vectorAvailableConfigs:
            self.vectorConfigs.append({
                'name': channel_list.name,
                'transceiver_name': channel_list.transceiver_name,
                'channel index': channel_list.channel_index,
                'serial_number': channel_list.serial_number,
                'is_on_bus': channel_list.is_on_bus,
                'is_support_canfd': bool(channel_list.channel_capabilities.value & \
                                      xldefine.XL_ChannelCapabilities.XL_CHANNEL_FLAG_CANFD_BOSCH_SUPPORT.value),
                'can_op_mode':channel_list.bus_params.can.can_op_mode
                                         })


    def update_channel_lists_ui(self):
        self.comboBox_channel.clear()
        for channel in self.vectorConfigs:
            self.comboBox_channel.addItem(str(channel["name"]) +
                                          ' ' +
                                          str(channel['transceiver_name']) +
                                          ' ' +
                                          str(channel['serial_number']))

    def update_channel_cfg_ui(self):
        self.channel_choose = self.comboBox_channel.currentIndex()
        if self.vectorConfigs[self.channel_choose]['is_on_bus']:
            if self.vectorConfigs[self.channel_choose]['can_op_mode'] & xldefine.XL_CANFD_BusParams_CanOpMode.XL_BUS_PARAMS_CANOPMODE_CAN20:
                self.checkBox_bustype.setChecked(False)
                self.checkBox_bustype.setDisabled(True)
            elif self.vectorConfigs[self.channel_choose]['can_op_mode'] & xldefine.XL_CANFD_BusParams_CanOpMode.XL_BUS_PARAMS_CANOPMODE_CANFD:
                self.checkBox_bustype.setChecked(True)
                self.checkBox_bustype.setDisabled(True)
        else:
            if self.vectorConfigs[self.channel_choose]['is_support_canfd']:
                self.checkBox_bustype.setChecked(True)
            else:
                self.checkBox_bustype.setChecked(False)
                self.checkBox_bustype.setDisabled(True)

    def run_bus(self):
        if self.is_run:
            self.canudsthread.stop_thread()
            self.send_queue.empty()
            self.conn.close()
            self.stack.stop()
            self.notifier.stop()
            self.canbus.shutdown()

            self.is_run = False

            self.pushButton_start.setText('Start')

            self.comboBox_channel.setDisabled(False)
            self.pushButton_send.setDisabled(True)
        else:
            self.connect_vector_can_interfaces()
            self.create_uds_client(self.canbus)

    def connect_vector_can_interfaces(self):

        VectorBus.set_application_config(
            app_name=self.appName,
            app_channel=self.channel_choose,
            hw_type=self.__vectorAvailableConfigs[self.channel_choose].hw_type,
            hw_index=self.__vectorAvailableConfigs[self.channel_choose].hw_index,
            hw_channel=self.__vectorAvailableConfigs[self.channel_choose].hw_channel
        )
        if self.checkBox_bustype.isChecked():
            busParams_dict=self.vectorChannelCanParams.canfd._asdict()
        else:
            busParams_dict=self.vectorChannelCanParams.can._asdict()

        if self.__vectorAvailableConfigs[self.channel_choose].is_on_bus:
            self.canbus = VectorBus(
                channel=self.channel_choose,
                app_name=self.appName,
                fd=self.checkBox_bustype.isChecked())
        else:
            self.canbus = VectorBus(
                channel=self.channel_choose,
                app_name=self.appName,
                fd=self.checkBox_bustype.isChecked(),
                **busParams_dict)

    def create_uds_client(self,bus):
        # tp_addr = isotp.Address(isotp.AddressingMode.Normal_29bits, txid=0x18DA05F1, rxid=0x18DAF105,
        #                         functional_id=0x18DB33F1)
        tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=0x123, rxid=0x124,
                                functional_id=0x125)


        isotpparams = {
            'blocking_send': False,
            'stmin': 32,
            # Will request the sender to wait 32ms between consecutive frame. 0-127ms or 100-900ns with values from 0xF1-0xF9
            'blocksize': 8,
            # Request the sender to send 8 consecutives frames before sending a new flow control message
            'wftmax': 0,  # Number of wait frame allowed before triggering an error
            'tx_data_length': 8,  # Link layer (CAN layer) works with 8 byte payload (CAN 2.0)
            # Minimum length of CAN messages. When different from None, messages are padded to meet this length. Works with CAN 2.0 and CAN FD.
            'tx_data_min_length': None,
            'tx_padding': 0,  # Will pad all transmitted CAN messages with byte 0x00.
            'rx_flowcontrol_timeout': 1000,
            # Triggers a timeout if a flow control is awaited for more than 1000 milliseconds
            'rx_consecutive_frame_timeout': 1000,
            # Triggers a timeout if a consecutive frame is awaited for more than 1000 milliseconds
            'override_receiver_stmin': 0,
            # When sending, respect the stmin requirement of the receiver. If set to True, go as fast as possible.
            'max_frame_size': 4095,  # Limit the size of receive frame.
            'can_fd': self.checkBox_bustype.isChecked(),  # Does not set the can_fd flag on the output CAN messages
            'bitrate_switch': False,  # Does not set the bitrate_switch flag on the output CAN messages
            'rate_limit_enable': False,  # Disable the rate limiter
            'rate_limit_max_bitrate': 1000000,
            # Ignored when rate_limit_enable=False. Sets the max bitrate when rate_limit_enable=True
            'rate_limit_window_size': 0.2,
            # Ignored when rate_limit_enable=False. Sets the averaging window size for bitrate calculation when rate_limit_enable=True
            'listen_mode': False,  # Does not use the listen_mode which prevent transmission.
        }

        uds_config = udsoncan.configs.default_client_config.copy()

        self.notifier = can.Notifier(bus, [])  # Add a debug listener that print all messages
        # stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)              # isotp v1.x has no notifier support
        self.stack = isotp.NotifierBasedCanStack(bus=bus, notifier=self.notifier, address=tp_addr,
                                            params=isotpparams)  # Network/Transport layer (IsoTP protocol). Register a new listenenr
        self.conn = PythonIsoTpConnection(self.stack)  # interface between Application and Transport layer
        # with Client(conn, config=uds_config) as client:  # Application layer (UDS protocol)
        #     client.change_session(1)
        # conn.close()
        # stack.stop()





        self.canudsthread=canUDSClientThread(conn=self.conn,send_queue=self.send_queue)
        self.canudsthread.start()

        self.is_run=True

        self.pushButton_start.setText('Stop')

        self.comboBox_channel.setDisabled(True)
        self.pushButton_send.setDisabled(False)


    def send_uds(self):
        self.send_queue.put(1)

class canUDSClientThread(QThread):
    def __init__(self, conn,send_queue):
        super().__init__()
        self.conn=conn
        self.send_queue=send_queue
        self.stop_flag=0;

    def run(self):
        self.conn.open()
        # client=Client(conn=self.conn, config=self.config,request_timeout=2)
        while True:
            try:
                if self.stop_flag==1:
                    break
                data = self.send_queue.get(block=True, timeout=1)  # 设置超时时间，例如 1 秒

                req = Request(services.ECUReset, subfunction=1)
                self.conn.send(req.get_payload())
                payload = self.conn.wait_frame(timeout=1)
                print(payload)
                if payload==None:
                    print('None')
                else:
                    try:
                        response = Response.from_payload(payload)
                        print(response.code)
                        if response.service == services.ECUReset and response.code == Response.Code.PositiveResponse and response.data == b'\x01':
                            print('Success!')
                        else:
                            print('Reset failed')
                    except Exception as e:
                        print(e)



            except queue.Empty:
                # 处理队列为空的情况，例如打印日志或进行其他操作
                print("队列为空，等待数据...")
    def stop_thread(self):
        self.stop_flag=1

















if __name__ == "__main__":
    # 高dpi
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    w = MainWindows()
    w.show()
    sys.exit(app.exec_())
