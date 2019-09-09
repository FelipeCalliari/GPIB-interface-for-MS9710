import visa
import numpy


def IsConnected(func):
    def func_wrapper(self, *args, **kwargs):
        #print("SELF: {}\nFUNCTION: {}\nARGS: {}\nKWARGS: {}".format(self, func, args, kwargs))
        if self._connected:
            return func(self, *args, **kwargs)
        else:
            pass # Not connected to GPIB instrument
    return func_wrapper


class OSA(object):
    def __init__(self):
        try:
            self._rm = visa.ResourceManager()
            self._visa = True
        except:
            self._rm = None
            self._visa = False
            raise ImportError("Could not import pyVisa.")

        self._instr = None
        self._connected = False


    @property
    def list_devices(self):
        if self._visa:
            resources = self._rm.list_resources()
            if resources != ():
                return resources
        return ("")


    @property
    def connected(self):
        return self._connected


    def connect(self, GPIB_Addr):
        if self._visa:
            try:
                self._instr = self._rm.open_resource(GPIB_Addr)
                self._instr.write("*CLS")
                self._instr.timeout = 15000
                self._connected = True
            except:
                self._connected = False

    
    @property
    @IsConnected
    def ckearStatus(self):
        self._instr.write("*CLS")
    
    
    @IsConnected
    def UserMode(self):
        self._instr.control_ren(0)


    @property
    @IsConnected
    def Wavelength_Center(self):
        """
        Wavelength Center

        Format = xxxx.xx
        """
        return self._instr.query("CNT?")

    
    @Wavelength_Center.setter
    @IsConnected
    def Wavelength_Center(self, value):
        value = self._formatFloat(value, 600, 1750)
        if value is not None:
            self._instr.write("CNT {:7.2f}".format(value))


    @property
    @IsConnected
    def Wavelength_Span(self):
        """
        Wavelength Span

        Format = xxxx.x
        """
        return self._instr.query("SPN?")

    
    @Wavelength_Span.setter
    @IsConnected
    def Wavelength_Span(self, value):
        value = self._formatFloat(value, 600, 1750)
        if value is not None:
            self._instr.write("SPN {:7.1f}".format(value))


    @property
    @IsConnected
    def Wavelength_Start(self):
        """
        Wavelength Start

        Format = xxxx.x
        """
        return self._instr.query("STA?")

    
    @Wavelength_Start.setter
    @IsConnected
    def Wavelength_Start(self, value):
        value = self._formatFloat(value, 600, 1750)
        if value is not None:
            self._instr.write("STA {:7.1f}".format(value))


    @property
    @IsConnected
    def Wavelength_Stop(self):
        """
        Wavelength Stop

        Format = xxxx.x
        """
        return self._instr.query("STO?")

    
    @Wavelength_Stop.setter
    @IsConnected
    def Wavelength_Stop(self, value):
        value = self._formatFloat(value, 600, 1750)
        if value is not None:
            self._instr.write("STO {:7.1f}".format(value))


    @property
    @IsConnected
    def Wavelength_Marker_Value(self):
        """
        Wavelength Marker Value

        Format = WL or FREQ
        """
        return self._instr.query("MKV?")

    
    @Wavelength_Marker_Value.setter
    @IsConnected
    def Wavelength_Marker_Value(self, value):
        if value in ["WL", "FREQ"]:
            self._instr.write("MKV {}".format(value))


    @property
    @IsConnected
    def Level_Level_Scale(self):
        """
        Level Level Scale

        Format = LOG or LIN
        """
        return self._instr.query("LVS?")

    
    @property
    @IsConnected
    def Level_Log_Scale(self):
        """
        Level Log Scale

        Format = 0.1 to 10.0 dB/div
        """
        return self._instr.query("LOG?")

    
    @Level_Log_Scale.setter
    @IsConnected
    def Level_Log_Scale(self, value):
        value = self._formatFloat(value, 0.1, 10.0)
        if value is not None:
            self._instr.write("LOG {:4.1f}".format(value))


    @property
    @IsConnected
    def Level_Lin_Scale(self):
        """
        Level Linear Scale

        Format = 1 pW to 1 W
        """
        return self._instr.query("LLV?")

    
    @Level_Lin_Scale.setter
    @IsConnected
    def Level_Lin_Scale(self, value):
        self._instr.write("LLV {}".format(value))


    @property
    @IsConnected
    def Level_Opt_Att(self):
        """
        Level Optical Attenuator

        Format = ON or OFF
        """
        return self._instr.query("ATT?")

    
    @Level_Opt_Att.setter
    @IsConnected
    def Level_Opt_Att(self, value):
        if value in ["ON", "OFF"]:
            self._instr.write("ATT {}".format(value))


    @property
    @IsConnected
    def Resolution_Res(self):
        """
        Resolution - Resolution

        Format = 0.05, 0.07, 0.10, 0.20, 0.50 or 1.00
        """
        return self._instr.query("RES?")

    
    @Resolution_Res.setter
    @IsConnected
    def Resolution_Res(self, value):
        if value in [0.05, 0.07, 0.10, 0.20, 0.50, 1.00]:
            self._instr.write("RES {}".format(value))


    @property
    @IsConnected
    def VBW(self):
        """
        Video Bandwidth

        Format = 10 Hz, 100 Hz, 1 kHz, 100 kHz, 1 MHz
        """
        return self._instr.query("VBW?")

    
    @VBW.setter
    @IsConnected
    def VBW(self, value):
        self._instr.write("VBW {}".format(value))


    @property
    @IsConnected
    def Average_Point_Average(self):
        """
        Average - Point Average

        Format = 2 to 1000, or OFF
        """
        return self._instr.query("AVT?")

    
    @Average_Point_Average.setter
    @IsConnected
    def Average_Point_Average(self, value):
        if value == "OFF":
            self._instr.write("AVT OFF")
        else:
            value = self._formatInt(value, 2, 1000)
            if value is not None:
                self._instr.write("AVT {}".format(value))


    @property
    @IsConnected
    def Average_Sweep_Average(self):
        """
        Average - Sweep Average

        Format = 2 to 1000, or OFF
        """
        return self._instr.query("AVS?")

    
    @Average_Sweep_Average.setter
    @IsConnected
    def Average_Sweep_Average(self, value):
        if value == "OFF":
            self._instr.write("AVS OFF")
        else:
            value = self._formatInt(value, 2, 1000)
            if value is not None:
                self._instr.write("AVS {}".format(value))


    @property
    @IsConnected
    def Average_Smooth(self):
        """
        Average - Smooth

        Format = 3, 5, 7, 9, 11, or OFF
        """
        return self._instr.query("SMT?")

    
    @Average_Smooth.setter
    @IsConnected
    def Average_Smooth(self, value):
        if value in [3, 5, 7, 9, 11, "OFF"]:
            self._instr.write("SMT {}".format(value))


    @property
    @IsConnected
    def Sampling_Points(self):
        """
        Sampling Points

        Format = 51, 101, 251, 501, 1001, 2001 or 5001
        """
        return self._instr.query("MPT?")

    
    @Sampling_Points.setter
    @IsConnected
    def Sampling_Points(self, value):
        if value in [51, 101, 251, 501, 1001, 2001, 5001]:
            self._instr.write("MPT {}".format(value))


    @property
    @IsConnected
    def Peak_Search(self):
        """
        Peak Search

        Format = PEAK, NEXT, LAST, LEFT, RIGHT
        """
        return self._instr.query("PKS?")

    
    @Peak_Search.setter
    @IsConnected
    def Peak_Search(self, value):
        if value in ["PEAK", "NEXT", "LAST", "LEFT", "RIGHT"]:
            self._instr.write("PKS {}".format(value))


    @property
    @IsConnected
    def Dip_Search(self):
        """
        Dip Search

        Format = PEAK, NEXT, LAST, LEFT, RIGHT
        """
        return self._instr.query("DPS?")

    
    @Dip_Search.setter
    @IsConnected
    def Dip_Search(self, value):
        if value in ["PEAK", "NEXT", "LAST", "LEFT", "RIGHT"]:
            self._instr.write("DPS {}".format(value))


    @property
    @IsConnected
    def Memory_Select(self):
        """
        Memory Select

        Format = A, B
        """
        return self._instr.query("MSL?")

    
    @Memory_Select.setter
    @IsConnected
    def Memory_Select(self, value):
        if value in ["A", "B"]:
            self._instr.write("MSL {}".format(value))


    @property
    @IsConnected
    def Trace_Select(self):
        """
        Trace Select

        Format = A, B, AB, A_B, B_A
        """
        return self._instr.query("TSL?")

    
    @Trace_Select.setter
    @IsConnected
    def Trace_Select(self, value):
        if value in ["A", "B", "AB", "A_B", "B_A"]:
            self._instr.write("TSL {}".format(value))


    @property
    @IsConnected
    def Max_Hold(self):
        """
        Max Hold

        Format = ON or OFF
        """
        value = self._instr.query("DMD?").replace("\r\n", "")
        if value == "MHL":
            return "ON"
        elif value == "NRM":
            return "OFF"
        return None

    
    @Max_Hold.setter
    @IsConnected
    def Max_Hold(self, value):
        if value == "ON":
            self._instr.write("DMD MHL")
        else:
            self._instr.write("DMD NRM")


    @property
    @IsConnected
    def Dynamic_Range(self):
        """
        Dynamic Range

        Format = NORMAL or HIGH
        """
        return self._instr.query("DRG?")

    
    @Dynamic_Range.setter
    @IsConnected
    def Dynamic_Range(self, value):
        if value in ["NORMAL", "HIGH"]:
            self._instr.write("DRG {}".format(value))


    @property
    @IsConnected
    def Marker_Off(self):
        self._instr.write("EMK")


    @property
    @IsConnected
    def Sweep_Single(self):
        self._instr.write("SSI")


    @property
    @IsConnected
    def Sweep_Repeat(self):
        self._instr.write("SRT")


    @property
    @IsConnected
    def Sweep_Stop(self):
        self._instr.write("SST")


    @property
    @IsConnected
    def Measuring(self):
        return int(self._instr.query("MOD?"))


    @property
    @IsConnected
    def Memory_Data_DMA(self):
        return self._instr.query("DMA?")


    @property
    @IsConnected
    def Memory_Data_DMB(self):
        return self._instr.query("DMB?")


    @property
    @IsConnected
    def Memory_Data_DQA(self):
        return self._instr.query("DQA?")


    @property
    @IsConnected
    def Memory_Data_DQB(self):
        return self._instr.query("DQB?")


    def __two_compl(self, val, bits):
        if (val >> bits-1):
            # negative number
            return val - 2**bits
        else:
            # positive number
            return val


    def __split_len(self, seq, length):
        """
        Example: 
           >>> split_len("HELLO WORLD", 2)
           ['HE', 'LL', 'O ', 'WO', 'RL', 'D']
        """
        return [seq[i:i+length] for i in range(0, len(seq), length)]


    def __BinaryFormat(self, data):
        scale = self.Level_Level_Scale
        start, stop, n_points = [float(i) for i in self.Memory_Data_Format_A.split(",")]
        dx = numpy.linspace(start, stop, int(n_points))
        if "LOG" in scale:
            # LOG SCALE
            # for each 2 bytes do
            # q = bytearray([233, 162])   <==>   -57.26 dBm
            # (1e-2 * two_compl( (q[0] << 8) + q[1], 16 ))
            t = "LOG"
            q = self.__split_len(data, 2)
            dy = numpy.empty(int(n_points), dtype=float)
            for i in range(int(n_points)):
                dy[i] = (1e-2 * self.__two_compl( (q[i][0] << 8) + q[i][1], 16 ))
        else:
            # LINEAR SCALE
            # for each 4 bytes do
            # q = bytearray([255, 247, 39, 16])   <==>   1E-9 mW
            # (1e-4*((q[2] << 8) + q[3])) * (10**two_compl((q[0] << 8) + q[1], 16))
            t = "LIN"
            q = self.__split_len(data, 4)
            dy = numpy.empty(int(n_points), dtype=float)
            for i in range(int(n_points)):
                dy[i] = (1e-4*((q[i][2] << 8) + q[i][3])) * (10**self.__two_compl((q[i][0] << 8) + q[i][1], 16))
        return [dx, dy, t]


    @property
    @IsConnected
    def Memory_Data_DBA(self):
        self._instr.write("DBA?")
        data = self._instr.read_raw()
        return self.__BinaryFormat(data)


    @property
    @IsConnected
    def Memory_Data_DBB(self):
        self._instr.write("DBB?")
        data = self._instr.read_raw()
        return self.__BinaryFormat(data)


    @property
    @IsConnected
    def Memory_Data_Format_A(self):
        """
        lambda1, lambda2, n
        """
        return self._instr.query("DCA?")


    @property
    @IsConnected
    def Memory_Data_Format_B(self):
        """
        lambda1, lambda2, n
        """
        return self._instr.query("DCB?")


    def _formatFloat(self, value, min, max):
        try:
            value = float(value)
            if min <= value <= max:
                return value
            else:
                return None
        except:
            return None


    def _formatInt(self, value, min, max):
        try:
            value = int(value)
            if min <= value <= max:
                return value
            else:
                return None
        except:
            return None
