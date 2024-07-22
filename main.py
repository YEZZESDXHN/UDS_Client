import queue
import sys
import ctypes
from PyQt5.QtCore import QThread, QCoreApplication, Qt, pyqtSignal, QRegExp, QStringListModel
from PyQt5.QtGui import QTextCursor, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow
import can
from can.interfaces.vector import VectorBus, xldefine, get_channel_configs, VectorBusParams, VectorCanParams, \
    VectorCanFdParams
from udsoncan import NegativeResponseException, TimeoutException, UnexpectedResponseException, InvalidResponseException, \
    services, Request,  DidCodec, ConfigError

from UDS_Client_UI import Ui_MainWindow
import isotp

from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
import udsoncan.configs
import configparser

class MainWindows(QMainWindow, Ui_MainWindow):
    sig_dll_path = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.vectorConfigs = []
        self.dll_path=None
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
            bitrate=500000,
            data_bitrate=2000000,
            sjw_abr=16,
            tseg1_abr=63,
            tseg2_abr=16,
            sam_abr=1,
            sjw_dbr=4,
            tseg1_dbr=15,
            tseg2_dbr=4,
            output_mode=xldefine.XL_OutputMode.XL_OUTPUT_MODE_NORMAL,
            can_op_mode=xldefine.XL_CANFD_BusParams_CanOpMode.XL_BUS_PARAMS_CANOPMODE_CANFD
        )

        self.vectorChannelCanParams = VectorBusParams(
            bus_type=xldefine.XL_BusTypes.XL_BUS_TYPE_CAN,
            can=can_params,
            canfd=canfd_params
        )

    def read_ecu_config(self):
        config = configparser.ConfigParser()
        config.read('./ECUConfig/DIDList.ini')
        ecu_data = {}
        for ecu_name in config.sections():
            if ":" not in ecu_name:  # 只处理 ECU 名称，不处理子项
                AddressingMode=None
                try:
                    AddressingMode=int(config[ecu_name]["AddressingMode"])
                except:
                    AddressingMode=0
                try:
                    uds_on_can_request_id=config[ecu_name]["uds_on_can_request_id"]
                except:
                    uds_on_can_request_id=0x701
                try:
                    uds_on_can_response_id=config[ecu_name]["uds_on_can_response_id"]
                except:
                    uds_on_can_response_id=0x702
                try:
                    uds_on_can_function_id=config[ecu_name]["uds_on_can_function_id"]
                except:
                    uds_on_can_function_id=0x7df



                ecu_data[ecu_name] = {}
                # 读取 ECU 基本信息
                ecu_data[ecu_name]["AddressingMode"] = AddressingMode
                ecu_data[ecu_name]["uds_on_can_request_id"] = uds_on_can_request_id
                ecu_data[ecu_name]["uds_on_can_response_id"] = uds_on_can_response_id
                ecu_data[ecu_name]["uds_on_can_function_id"] = uds_on_can_function_id

                # 读取 dll 信息
                try:
                    dll=config[f"{ecu_name}:dll"]["dll"]
                except:
                    dll=None
                ecu_data[ecu_name]["dll"] = dll

                # 读取 ReadDataByIdentifier 信息
                ecu_data[ecu_name]["ReadDataByIdentifier"] = {}
                try:
                    for key, value in config.items(f"{ecu_name}:ReadDataByIdentifier"):
                        ecu_data[ecu_name]["ReadDataByIdentifier"][key] = value
                except:
                    pass
                # 读取 DIDs 信息
                ecu_data[ecu_name]["DIDs"] = {}
                try:
                    for key, value in config.items(f"{ecu_name}:DIDs"):
                        ecu_data[ecu_name]["DIDs"][key] = value
                except:
                    pass


        return ecu_data

    def set_ecu_diag_id(self):
        ecu_name=self.comboBox_eculist.currentText()
        self.lineEdit_requestid.setText(self.ecus[ecu_name]['uds_on_can_request_id'])
        self.lineEdit_responseid.setText(self.ecus[ecu_name]['uds_on_can_response_id'])
        self.lineEdit_functionid.setText(self.ecus[ecu_name]['uds_on_can_function_id'])
        self.set_did_list()
        self.dll_path=self.ecus[ecu_name]['dll']
        self.sig_dll_path.emit(self.ecus[ecu_name]['dll'])

    def set_did_list(self):
        model = QStringListModel()  # 在循环外创建 QStringListModel

        ecu_name = self.comboBox_eculist.currentText()

        string_list = []  # 创建一个空列表存储所有 did
        for did in self.ecus[ecu_name]['DIDs']:
            string_list.append(did)  # 将 did 添加到列表中

        model.setStringList(string_list)  # 将所有 did 设置给 model

        self.listView_dids.setModel(model)

    def init(self):

        try:
            self.ecus=self.read_ecu_config()
            self.comboBox_eculist.clear()
            for ecu in self.ecus.keys():
                self.comboBox_eculist.addItem(ecu)

            self.set_ecu_diag_id()




        except:
            self.comboBox_eculist.setDisabled(True)
            self.ecus=None

        self.send_queue = queue.Queue()
        self.rec_queue = queue.Queue()


        # self.dll_lib=ctypes.WinDLL("./SeednKey.dll")

        # self.lineEdit_send.setInputMethodHints(Qt.InputMethodHint)
        reg = QRegExp("[a-fA-F0-9]+$")
        regVal = QRegExpValidator()
        regVal.setRegExp(reg)
        self.lineEdit_send.setValidator(regVal)


        self.pushButton_start.clicked.connect(self.run_bus)
        self.comboBox_channel.activated.connect(self.update_channel_cfg_ui)
        self.pushButton_send.clicked.connect(self.send_uds)
        self.comboBox_eculist.activated.connect(self.set_ecu_diag_id)

        self.set_canParams()

        # self.dll_lib=ctypes.WinDLL("./GenerateKeyExImpl.dll")


    def refresh_ui(self):
        self.refresh_drive()
        self.update_channel_lists_ui()
        # 重新加载后将channel_choose复位
        # self.channel_choose = 0
        self.update_channel_cfg_ui()

    def refresh_drive(self):
        self.__vectorAvailableConfigs = get_channel_configs()
        self.vectorConfigs.clear()
        for channel_list in self.__vectorAvailableConfigs:
            # print(channel_list.channel_bus_capabilities)
            # print(xldefine.XL_BusCapabilities.XL_BUS_ACTIVE_CAP_CAN.value)
            # print(xldefine.XL_BusCapabilities.XL_BUS_COMPATIBLE_CAN.value)
            if(channel_list.channel_bus_capabilities & xldefine.XL_BusCapabilities.XL_BUS_ACTIVE_CAP_CAN):
                self.vectorConfigs.append({
                    'name': channel_list.name,
                    'transceiver_name': channel_list.transceiver_name,
                    'channel_index': channel_list.channel_index,
                    'hw_type':channel_list.hw_type,
                    'hw_index': channel_list.hw_index,
                    'hw_channel': channel_list.hw_channel,
                    'serial_number': channel_list.serial_number,
                    'is_on_bus': channel_list.is_on_bus,
                    'is_support_canfd': bool(channel_list.channel_capabilities.value & \
                                             xldefine.XL_ChannelCapabilities.XL_CHANNEL_FLAG_CANFD_BOSCH_SUPPORT.value),
                    'can_op_mode': channel_list.bus_params.can.can_op_mode
                })
                # print(channel_list.channel_index)
    def update_channel_lists_ui(self):
        self.comboBox_channel.clear()
        for channel in self.vectorConfigs:
            self.comboBox_channel.addItem(str(channel["name"]) +
                                          ' ' +
                                          str(channel['transceiver_name']) +
                                          ' ' +
                                          str(channel['serial_number']))
        if self.channel_choose + 1 > len(self.vectorConfigs):
            self.channel_choose = 0
            self.comboBox_channel.setCurrentIndex(self.channel_choose)
        else:
            self.comboBox_channel.setCurrentIndex(self.channel_choose)

    def update_channel_cfg_ui(self):
        self.checkBox_bustype.setDisabled(False)
        self.channel_choose = self.comboBox_channel.currentIndex()
        self.checkBox_bustype.setDisabled(False)
        if self.vectorConfigs[self.channel_choose]['is_on_bus']:
            if self.vectorConfigs[self.channel_choose][
                'can_op_mode'] & xldefine.XL_CANFD_BusParams_CanOpMode.XL_BUS_PARAMS_CANOPMODE_CAN20:

                self.checkBox_sendcanfd.setChecked(False)
                self.checkBox_bustype.setChecked(False)
                self.checkBox_bustype.setDisabled(True)
            elif self.vectorConfigs[self.channel_choose][
                'can_op_mode'] & xldefine.XL_CANFD_BusParams_CanOpMode.XL_BUS_PARAMS_CANOPMODE_CANFD:

                self.checkBox_bustype.setChecked(True)
                self.checkBox_bustype.setDisabled(True)

        else:
            if self.vectorConfigs[self.channel_choose]['is_support_canfd']:
                pass
                # self.checkBox_bustype.setChecked(True)
            else:
                self.checkBox_sendcanfd.setChecked(False)
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

            self.checkBox_bustype.setDisabled(False)
            self.comboBox_channel.setDisabled(False)
            self.pushButton_send.setDisabled(True)
            self.checkBox_sendcanfd.setDisabled(False)

            self.lineEdit_responseid.setDisabled(False)
            self.lineEdit_requestid.setDisabled(False)
            self.lineEdit_functionid.setDisabled(False)
        else:
            self.connect_vector_can_interfaces()
            self.create_uds_client(self.canbus)

            if self.checkBox_bustype.isChecked():
                pass
            else:
                self.checkBox_sendcanfd.setChecked(False)
            self.checkBox_sendcanfd.setDisabled(True)

            self.lineEdit_responseid.setDisabled(True)
            self.lineEdit_requestid.setDisabled(True)
            self.lineEdit_functionid.setDisabled(True)

    def connect_vector_can_interfaces(self):
        self.refresh_ui()
        VectorBus.set_application_config(
            app_name=self.appName,
            app_channel=self.vectorConfigs[self.channel_choose]['channel_index'],
            hw_type=self.vectorConfigs[self.channel_choose]['hw_type'],
            hw_index=self.vectorConfigs[self.channel_choose]['hw_index'],
            hw_channel=self.vectorConfigs[self.channel_choose]['hw_channel'],
        )
        if self.checkBox_bustype.isChecked():
            busParams_dict = self.vectorChannelCanParams.canfd._asdict()
        else:
            busParams_dict = self.vectorChannelCanParams.can._asdict()

        if self.vectorConfigs[self.channel_choose]["is_on_bus"]:
            self.canbus = VectorBus(
                channel=self.vectorConfigs[self.channel_choose]['channel_index'],
                app_name=self.appName,
                fd=self.checkBox_bustype.isChecked())
        else:
            self.canbus = VectorBus(
                channel=self.vectorConfigs[self.channel_choose]['channel_index'],
                app_name=self.appName,
                fd=self.checkBox_bustype.isChecked(),
                **busParams_dict)
            # self.__vectorAvailableConfigs = get_channel_configs()
            # print(self.__vectorAvailableConfigs[2].bus_params.canfd)

    def get_diag_id_by_str(self, id_str):
        try:
            # 尝试将字符串解释为十六进制数
            id = int(id_str, 10)
            return id
        except ValueError:
            # 如果不是有效的十六进制数，则尝试将其解释为十进制数
            try:
                id = int(id_str, 16)
                return id
            except ValueError:
                print(' 不是有效的十六进制或十进制字符串')

    def create_uds_client(self, bus):
        # tp_addr = isotp.Address(isotp.AddressingMode.Normal_29bits, txid=0x18DA05F1, rxid=0x18DAF105,
        #                         functional_id=0x18DB33F1)

        tx_id_str = self.lineEdit_requestid.text()
        txid = self.get_diag_id_by_str(tx_id_str)

        rx_id_str = self.lineEdit_responseid.text()
        rxid = self.get_diag_id_by_str(rx_id_str)

        functional_id_str = self.lineEdit_functionid.text()
        functionalid = self.get_diag_id_by_str(functional_id_str)

        if txid is None:
            txid = 0x123
        if rxid is None:
            rxid = 0x234
        if functionalid is None:
            functionalid = 0x345

        tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=txid, rxid=rxid,
                                functional_id=functionalid)
        # tp_addr = isotp.Address(isotp.AddressingMode.Normal_29bits, txid=txid, rxid=rxid,
        #                         functional_id=functionalid)


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
            'can_fd': self.checkBox_sendcanfd.isChecked(),  # Does not set the can_fd flag on the output CAN messages
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
        # self.stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotpparams)              # isotp v1.x has no notifier support
        self.stack = isotp.NotifierBasedCanStack(bus=bus, notifier=self.notifier, address=tp_addr,
                                                 params=isotpparams,
                                                 error_handler=self.handle_error)  # Network/Transport layer (IsoTP protocol). Register a new listenenr

        self.conn = PythonIsoTpConnection(self.stack)  # interface between Application and Transport layer
        # with Client(conn, config=uds_config) as client:  # Application layer (UDS protocol)
        #     client.change_session(1)
        # conn.close()
        # stack.stop()



        config = dict(udsoncan.configs.default_client_config)
        config['p2_timeout']=1.5
        # config['data_identifiers'] = {
        #     'default': '>H',  # Default codec is a struct.pack/unpack string. 16bits little endian
        #     0xF190: udsoncan.AsciiCodec(15),  # Codec that read ASCII string. We must tell the length of the string
        #     0xf110:MyCodec()
        # }


        self.uds_client=Client(self.conn, request_timeout=2, config=config)
        self.uds_client.open()

        # try:
        #     response = self.uds_client.test_data_identifier([0xF195])
        #
        #     print(response)
        # except TimeoutException as e:
        #     print(e)
        # req = Request(services.WriteDataByIdentifier, data=bytes([0x00,0x11,0x22,0x33,0x44,0x55,0x66]))
        # try:
        #     response = self.uds_client.send_request(req)
        #
        #     if response.positive:
        #         # 获取响应数据
        #         data = response.data
        #         print(f"Data: {data.hex()}")
        #     else:
        #         # 处理否定响应
        #         print(f"Negative response: {response.code_name}")
        # except TimeoutException as e:
        #     print(e)
        # except:
        #     print('error')



        # with Client(conn, request_timeout=2, config=config) as client:
        #     response = client.read_data_by_identifier([0xF190])
        #     print(response.service_data.values[0xF190])  # This is a dict of DID:Value
        #
        #     # Or, if a single DID is expected, a shortcut to read the value of the first DID
        #     vin = client.read_data_by_identifier_first(0xF190)






        self.canudsthread = canUDSClientThread(conn=self.uds_client, send_queue=self.send_queue,dll_path=self.dll_path)

        self.canudsthread.send_data.connect(self.print_tx)
        self.canudsthread.rec_data.connect(self.print_rx)
        self.sig_dll_path.connect(self.canudsthread.load_dll)

        self.canudsthread.sig_send_state.connect(self.canudsthread.set_send_state)

        self.canudsthread.start()

        self.is_run = True

        self.pushButton_start.setText('Stop')

        self.checkBox_bustype.setDisabled(True)
        self.comboBox_channel.setDisabled(True)
        self.pushButton_send.setDisabled(False)

    def print_tx(self, data):
        text = 'Tx:' + data.hex(" ").upper() + '\r'
        self.textEdit_trace.insertPlainText(text)
        self.textEdit_trace.moveCursor(QTextCursor.End)

    def print_rx(self, data):
        # text = 'Rx:' + data.hex(" ").upper() + '\r'
        # self.textEdit_trace.insertPlainText(text)
        # self.textEdit_trace.moveCursor(QTextCursor.End)
        self.textEdit_trace.insertPlainText(data)
        self.textEdit_trace.moveCursor(QTextCursor.End)

    def handle_error(self, error):

        # if isinstance(error, FlowControlTimeoutError):
        #     print(error)
        # elif isinstance(error, BlockingSendFailure):
        #     print(error)
        # elif isinstance(error, ConsecutiveFrameTimeoutError):
        #     print(error)
        # elif isinstance(error, InvalidCanDataError):
        #     print(error)
        # elif isinstance(error, UnexpectedFlowControlError):
        #     print(error)
        # elif isinstance(error, UnexpectedConsecutiveFrameError):
        #     print(error)
        # elif isinstance(error, ReceptionInterruptedWithSingleFrameError):
        #     print(error)
        # elif isinstance(error, ReceptionInterruptedWithFirstFrameError):
        #     print(error)
        # elif isinstance(error, MaximumWaitFrameReachedError):
        #     print(error)
        # elif isinstance(error, FrameTooLongError):
        #     print(error)
        # elif isinstance(error, ChangingInvalidRXDLError):
        #     print(error)
        # elif isinstance(error, MissingEscapeSequenceError):
        #     print(error)
        # elif isinstance(error, InvalidCanFdFirstFrameRXDL):
        #     print(error)
        # elif isinstance(error, OverflowError):
        #     print(error)

        self.canudsthread.sig_send_state.emit(error)
        text = 'Tx error:' + str(error) + '\r'
        self.textEdit_trace.insertPlainText(text)
        self.textEdit_trace.moveCursor(QTextCursor.End)

    def str_to_bytes(self, input_str):
        # 移除输入字符串中的空格
        input_str = input_str.replace(' ', '')

        # 检查输入字符串是否是有效的十六进制字符串
        if not input_str:
            raise ValueError("输入字符串为空")
        if len(input_str) % 2 != 0:
            raise ValueError("字符串长度必须是偶数")
        if not all(c in '0123456789abcdefABCDEF' for c in input_str):
            raise ValueError("字符串包含非法字符")

        # 尝试将字符串转换为字节对象
        try:
            bytes_list = bytes.fromhex(input_str)
            return bytes_list
        except ValueError:
            raise ValueError("无效的十六进制字符串")

    def make_uds_request(self, uds_bytes):
        if uds_bytes[0] == 0x10:
            print('DiagnosticSessionControl')
            req = Request(services.DiagnosticSessionControl, subfunction=uds_bytes[1])

            return req
        elif uds_bytes[0] == 0x11:
            req = Request(services.ECUReset, subfunction=uds_bytes[1])
            return req
        elif uds_bytes[0] == 0x27:
            print('SecurityAccess')
            if uds_bytes[1]%2 ==1:
                req = Request(services.SecurityAccess, subfunction=uds_bytes[1], data=uds_bytes[2:])
                return req
            else:
                self.textEdit_trace.insertPlainText('Send Security Level Erroe:'+uds_bytes.hex(' ') + '\r')
                self.textEdit_trace.moveCursor(QTextCursor.End)
                # self.rec_data.emit('Send Security Level Erroe' + '\r')

        elif uds_bytes[0] == 0x28:
            print('CommunicationControl')
            req = Request(services.CommunicationControl, subfunction=uds_bytes[1], data=uds_bytes[2])
            return req
        elif uds_bytes[0] == 0x83:
            print('AccessTimingParameter')
        elif uds_bytes[0] == 0x84:
            print('SecuredDataTransmission')
        elif uds_bytes[0] == 0x3e:
            print('TesterPresent')
            req = Request(services.TesterPresent, subfunction=uds_bytes[1] & 0x7f,
                          suppress_positive_response=bool(uds_bytes[1] & 0x80))
            return req
        elif uds_bytes[0] == 0x85:
            print('ControlDTCSetting')
        elif uds_bytes[0] == 0x86:
            print('ResponseOnEvent')
        elif uds_bytes[0] == 0x87:
            print('LinkControl')
        elif uds_bytes[0] == 0x22:
            print('ReadDataByIdentifier')
            req = Request(services.ReadDataByIdentifier, data=uds_bytes[1:])
            return req
        elif uds_bytes[0] == 0x2e:
            print('WriteDataByIdentifier')
            req = Request(services.WriteDataByIdentifier, data=uds_bytes[1:])
            return req
        elif uds_bytes[0] == 0x23:
            print('ReadMemoryByAddress')
        elif uds_bytes[0] == 0x2f:
            print('InputOutputControlByIdentifier')
        elif uds_bytes[0] == 0x31:
            print('RoutineControl')
        elif uds_bytes[0] == 0x24:
            print('ReadScalingDataByIdentifier')
        elif uds_bytes[0] == 0x2a:
            print('ReadDataByPeriodicIdentifier')
        elif uds_bytes[0] == 0x3d:
            print('WriteMemoryByAddress')
        elif uds_bytes[0] == 0x2c:
            print('DynamicallyDefineDataIdentifier')
        elif uds_bytes[0] == 0x14:
            print('ClearDiagnosticInformation')
        elif uds_bytes[0] == 0x19:
            print('ReadDTCInformation')
        elif uds_bytes[0] == 0x34:
            print('RequestDownload')
        elif uds_bytes[0] == 0x35:
            print('RequestUpload')
        elif uds_bytes[0] == 0x36:
            print('TransferData')
        elif uds_bytes[0] == 0x37:
            print('RequestTransferExit')
        elif uds_bytes[0] == 0x38:
            print('RequestFileTransfer')
        elif uds_bytes[0] == 0x29:
            print('Authentication')
        else:
            raise ValueError('无效服务')

    def send_uds(self):
        # 队列过多时不响应发送请求
        if self.send_queue.qsize() <= 2:
            data_str = self.lineEdit_send.text()
            try:
                uds_bytes = self.str_to_bytes(data_str)
                req = self.make_uds_request(uds_bytes)
                if req is not None:
                    self.send_queue.put(req)
                else:
                    print('req == None')
            except ValueError as e:
                print(e)


# class canUDSClientThread(QThread):
#     send_data = pyqtSignal(object)
#     rec_data = pyqtSignal(object)
#     sig_send_state = pyqtSignal(object)
#
#     def __init__(self, conn, send_queue):
#         super().__init__()
#         self.daemon = True  # 设置为守护进程
#         self.conn = conn
#         self.send_queue = send_queue
#         self.stop_flag = 0;
#         self.send_state = 'Normal'
#
#     def run(self):
#         self.conn.open()
#         # client=Client(conn=self.conn, config=self.config,request_timeout=2)
#         while True:
#             try:
#                 if self.stop_flag == 1:
#                     break
#                 req = self.send_queue.get(block=True, timeout=1)  # 设置超时时间，例如 1 秒
#
#                 # req = Request(services.ECUReset, subfunction=1)
#                 self.send_data.emit(req.get_payload())
#                 self.conn.send(req.get_payload())
#
#                 payload = self.conn.wait_frame(timeout=1.2)  # 流控帧超时1s,这里等待时间需要大于1s
#                 if self.send_state == 'Normal':
#                     if payload is None:
#                         self.rec_data.emit('ECU No Response\r')
#                     else:
#
#                         response = Response.from_payload(payload)
#
#                         # self.rec_data.emit(response)
#
#                         if response.service == req.service:
#                             if response.code == Response.Code.PositiveResponse:
#                                 self.rec_data.emit('PositiveResponse\r')
#                             else:
#                                 self.rec_data.emit(f'NegativeResponse：{response.code}\r')
#                         else:
#                             self.rec_data.emit(f'response service error\r')
#
#                 else:
#                     print(self.send_state)
#
#
#             except queue.Empty:
#                 # 处理队列为空的情况，例如打印日志或进行其他操作
#                 pass
#
#     def stop_thread(self):
#         self.stop_flag = 1
#
#     def set_send_state(self, error):
#         self.send_state = error

# 发送保持会话线程
class canTesterPresentThread(QThread):
    def __init__(self, conn, send_queue):
        super().__init__()

# 发送自定义报文线程，如唤醒报文
class cansendmessageThread(QThread):
    def __init__(self, conn, send_queue):
        super().__init__()

class canUDSClientThread(QThread):
    send_data = pyqtSignal(object)
    rec_data = pyqtSignal(object)
    sig_send_state = pyqtSignal(object)


    def __init__(self, conn, send_queue,dll_path):
        super().__init__()
        self.daemon = True  # 设置为守护进程
        self.conn = conn
        self.send_queue = send_queue
        self.stop_flag = 0;
        self.send_state = 'Normal'
        self.dll_path=dll_path
        self.dll_lib = None
        self.generated_key =None


    def run(self):
        self.load_dll(self.dll_path)
        self.conn.open()
        # client=Client(conn=self.conn, config=self.config,request_timeout=2)
        while True:
            try:
                if self.stop_flag == 1:
                    break

                req = self.send_queue.get(block=True, timeout=1)  # 设置超时时间，例如 1 秒
                self.send_data.emit(req.get_payload())
                try:
                    response = self.conn.send_request(req)
                    data_raw = response.original_payload
                    self.rec_data.emit(f"Positive: {data_raw.hex(' ')}\r")

                    if data_raw[0]==0x67 and data_raw[1]==req.get_payload()[1]:
                        # 当前python是64位，解锁dll是32位，无法直接调用，考虑做一个64位dll调用32位dll
                        # 此处回复key是固定值，待实现调用dll后再完成发送key的功能

                        length = len(data_raw)
                        seed_bytes = data_raw[2:length]
                        print(length)
                        seed_array = (ctypes.c_ubyte * len(seed_bytes))(*seed_bytes)
                        seed_length = ctypes.c_uint(len(seed_bytes))
                        security_level = ctypes.c_uint(data_raw[1])
                        variant_string = None
                        Options_string = None

                        # 准备输出数据
                        max_key_size = length - 2
                        key_array = (ctypes.c_ubyte * max_key_size)()
                        actual_key_size = ctypes.c_uint()


                        # 定义函数的返回类型和参数类型
                        try:
                            self.dll_lib.GenerateKeyEx.restype = ctypes.c_int
                            self.dll_lib.GenerateKeyEx.argtypes = [
                                ctypes.POINTER(ctypes.c_ubyte),  # ipSeedArray
                                ctypes.c_uint,  # iSeedArraySize
                                ctypes.c_uint,  # iSecurityLevel
                                ctypes.POINTER(ctypes.c_char),  # ipVariant
                                ctypes.POINTER(ctypes.c_ubyte),  # iopKeyArray
                                ctypes.c_uint,  # iMaxKeyArraySize
                                ctypes.POINTER(ctypes.c_uint)  # oActualKeyArraySize
                            ]


                            # 调用DLL函数
                            result = self.dll_lib.GenerateKeyEx(
                                seed_array,  # ipSeedArray
                                seed_length,  # iSeedArraySize
                                security_level,  # iSecurityLevel
                                ctypes.POINTER(ctypes.c_char)(),  # ipVariant (None or empty)
                                key_array,  # iopKeyArray
                                ctypes.c_uint(max_key_size),  # iMaxKeyArraySize
                                ctypes.byref(actual_key_size)  # oActualKeyArraySize
                            )

                            # 检查返回值
                            if result == 0:
                                self.generated_key = bytearray(key_array)[:actual_key_size.value]
                            else:
                                self.generated_key=None

                        except AttributeError as e:
                            self.generated_key=None

                        except Exception as e:
                            self.generated_key = None


                        if self.generated_key==None:
                            try:
                                self.dll_lib.GenerateKeyExOpt.restype = ctypes.c_int
                                self.dll_lib.GenerateKeyExOpt.argtypes = [
                                    ctypes.POINTER(ctypes.c_ubyte),  # ipSeedArray
                                    ctypes.c_uint,  # iSeedArraySize
                                    ctypes.c_uint,  # iSecurityLevel
                                    ctypes.POINTER(ctypes.c_char),  # ipVariant
                                    ctypes.POINTER(ctypes.c_char),  # ipOptions
                                    ctypes.POINTER(ctypes.c_ubyte),  # iopKeyArray
                                    ctypes.c_uint,  # iMaxKeyArraySize
                                    ctypes.POINTER(ctypes.c_uint)  # oActualKeyArraySize
                                ]


                                # 调用DLL函数
                                result = self.dll_lib.GenerateKeyExOpt(
                                    seed_array,  # ipSeedArray
                                    seed_length,  # iSeedArraySize
                                    security_level,  # iSecurityLevel
                                    ctypes.POINTER(ctypes.c_char)(),  # ipVariant (None or empty)
                                    ctypes.POINTER(ctypes.c_char)(),  # ipVariant (None or empty)
                                    key_array,  # iopKeyArray
                                    ctypes.c_uint(max_key_size),  # iMaxKeyArraySize
                                    ctypes.byref(actual_key_size)  # oActualKeyArraySize
                                )

                                # 检查返回值
                                if result == 0:
                                    self.generated_key = bytearray(key_array)[:actual_key_size.value]
                                else:
                                    self.generated_key = None

                            except AttributeError as e:
                                self.generated_key = None

                            except Exception as e:
                                self.generated_key = None




                        if self.generated_key == None:
                            self.generated_key = bytes([0x00] * (length - 2))

                        req1 = Request(services.SecurityAccess, subfunction=data_raw[1]+1, data=bytes(self.generated_key))
                        self.send_data.emit(req1.get_payload())
                        response = self.conn.send_request(req1)
                        data_raw = response.original_payload
                        self.rec_data.emit(f"Positive: {data_raw.hex(' ')}\r")
                        # print(f'level {data_raw[1]}')


                except NegativeResponseException as e:
                    print(e)
                    self.rec_data.emit(f"Negative response: {e.response.code_name}\r")
                except InvalidResponseException as e:
                    print(e)
                    data_raw = e.response.original_payload
                    self.rec_data.emit(f"Invalid Response: {data_raw.hex(' ')}\r")

                except UnexpectedResponseException as e:
                    print(e)
                    data_raw = e.response.original_payload
                    self.rec_data.emit(f"Unexpected Response: {data_raw.hex(' ')}\r")
                except ConfigError as e:
                    self.rec_data.emit(str(e) + '\r')
                except TimeoutException as e:
                    if self.send_state != 'Normal':
                        self.send_state = 'Normal'
                        pass
                    else:
                        self.rec_data.emit(str(e) + '\r')
                except Exception as e:
                    self.rec_data.emit(str(e) + '\r')




            except queue.Empty:
                # 处理队列为空的情况，例如打印日志或进行其他操作
                pass

    def load_dll(self,dll_path):
        try:
            self.dll_lib=ctypes.WinDLL(dll_path)
        except:
            self.dll_lib=None

    def stop_thread(self):
        self.stop_flag = 1

    def set_send_state(self, error):
        self.send_state = error

class MyCodec(DidCodec):
    def encode(self, val):
        return bytes(val)  # 直接将列表转换为字节序列

    def decode(self, payload):
        return list(payload)  # 将字节序列转换回列表


if __name__ == "__main__":
    # 高dpi
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setStyle("WindowsVista")
    w = MainWindows()
    w.show()
    sys.exit(app.exec_())
