from extronlib.interface import EthernetClientInterface, SerialInterface
from re import compile, search
from extronlib.system import Wait, ProgramLog

class DeviceClass():

    def __init__(self):

        self.Unidirectional = 'False'
        self.connectionCounter = 15

        self.DefaultResponseTimeout = 0.3
        self._compile_list = {}
        self.Subscription = {}
        self.ReceiveData = self.__ReceiveData
        self._ReceiveBuffer = b''
        self.counter = 0
        self.OutputStatus = {'Video': [], 'Audio': []}
        self.outputInit = {'Audio': [], 'Video': []}
        self.connectionFlag = True
        self.initializationChk = True
        self.lastInputSignalUpdate = 0
        self.VerboseDisabled = True
        self.PasswdPromptCount = 0
        self.Authenticated = 'Not Needed'
        self.Debug = False
        self.devicePassword = None
        self.OutputSize = 16
        self.InputSize = 16
        
        self.OutputStatus['Video'] = [('0') for i in range(0, self.OutputSize)]
        self.OutputStatus['Audio'] = [('0') for i in range(0, self.OutputSize)]
        self.outputInit['Video'] = ['0' for i in range(0, self.InputSize)]
        self.outputInit['Audio'] = ['0' for i in range(0, self.InputSize)]
        self.Models = {
            'DXP 44 HD 4k': self.extr_15_1865_44,
            'DXP 84 HD 4k': self.extr_15_1865_84,
            'DXP 88 HD 4k': self.extr_15_1865_88,
            'DXP 168 HD 4k': self.extr_15_1865_168,
            'DXP 1616 HD 4k': self.extr_15_1865_1616,
        }

        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'AudioMute': {'Parameters': ['Output'], 'Status': {}},
            'AudioOutputMute': {'Parameters': ['Output'], 'Status': {}},
            'ExecutiveMode': {'Status': {}},
            'GlobalAudioMute': {'Status': {}},
            'GlobalVideoMute': {'Status': {}},
            'InputGain': {'Parameters': ['Input'], 'Status': {}},
            'InputTieStatus': {'Parameters': ['Input', 'Output'], 'Status': {}},
            'MatrixTieCommand': {'Parameters': ['Input', 'Output', 'Tie Type'], 'Status': {}},
            'OutputTieStatus': {'Parameters': ['Output', 'Tie Type'], 'Status': {}},
            'OutputVolume': {'Parameters': ['Output'], 'Status': {}},
            'RecallPreset': {'Status': {}},
            'SavePreset': {'Status': {}},
            'SignalStatus': {'Parameters': ['Input'], 'Status': {}},
            'Temperature': {'Status': {}},
            'VideoMute': {'Parameters': ['Output'], 'Status': {}},
        }

        

        if self.Unidirectional == 'False':
            self.AddMatchString(compile(b'Amt([0-1])\r\n'), self.__MatchAudioMuteGlobal, None)
            self.AddMatchString(compile(b'Amt([0-9]{1,2})\*([0-7])\r\n'), self.__MatchAudioMute, None)
            self.AddMatchString(compile(b'In([0-9]{2}) Aud((\+|-)[0-9]{2,3})'), self.__MatchInputGain, None)
            self.AddMatchString(compile(b'(Out(\d+) )?In(\d+) (All|RGB|Vid|Aud)\r\n'), self.__MatchOutputTieStatus, None)
            self.AddMatchString(compile(b'Out([0-9]{2}) Vol([0-9]{1,3})\r\n'), self.__MatchOutputVolume, None)
            self.AddMatchString(compile(b'Vgp00\*Out(\d{2})([0-9 -]*)Vid\r\n'), self.__MatchAllMatrixTie, 'Video')
            self.AddMatchString(compile(b'Vgp00\*Out(\d{2})([0-9 -]*)Aud\r\n'), self.__MatchAllMatrixTie, 'Audio')
            self.AddMatchString(compile(b'Exe(0|1|2)\r\n'), self.__MatchExecutiveMode, None)
            self.AddMatchString(compile(b'Vmt([0-1])\r\n'), self.__MatchVideoMuteGlobal, None)
            self.AddMatchString(compile(b'Vmt([0-9]{1,2})\*([0-1])\r\n'), self.__MatchVideoMute, None)
            self.AddMatchString(compile(b'Frq00 ([0-1]+)\r\n'), self.__MatchSignalStatus, None)
            self.AddMatchString(compile(b'Sts00\*([0-9.]{1,}) ([0-9.]{1,}) ([0-9.]{1,})\r\n'), self.__MatchTemperature, None)
            self.AddMatchString(compile(b'E(\d+)\r\n'), self.__MatchErrors, None)
            self.AddMatchString(compile(b'Vrb3\r\n'), self.__MatchVerboseMode, None)
            self.AddMatchString(compile(b'Password:'), self.__MatchPassword, None)
            self.AddMatchString(compile(b'Login Administrator\r\n'), self.__MatchLoginAdmin, None)
            self.AddMatchString(compile(b'Login User\r\n'), self.__MatchLoginUser, None)

    def __MatchPassword(self, match, tag):
        self.PasswdPromptCount += 1
        if self.PasswdPromptCount > 2:
            print(['Log in failed. Please supply proper Admin password'])
        else:
            if self.devicePassword:
                self.Send(self.devicePassword + '\r\n')
            else:
                self.MissingCredentialsLog('Password')

        self.Authenticated = 'None'

    def __MatchLoginAdmin(self, match, tag):
        self.Authenticated = 'Admin'
        self.PasswdPromptCount = 0

    def __MatchLoginUser(self, match, tag):
        self.Authenticated = 'User'
        self.PasswdPromptCount = 0
        print(['Logged in as User. May have limited functionality.'])

    def __MatchVerboseMode(self, match, qualifier):

        self.VerboseDisabled = False
        self.UpdateAllMatrixTie(None, None)
        self.OnConnected()

    def UpdateAllMatrixTie(self, value, qualifier):
        self.Send('w0*1*1vc\r')
        self.Send('w0*1*2vc\r')

    def __MatchAllTie(self, match, tag):
        typeDic = {
            b'All': 'Audio/Video',
            b'RGB': 'Video',
            b'Vid': 'Video',
            b'Aud': 'Audio',
        }

        _input = str(int(match.group(3)))
        type = typeDic[match.group(4)]
        output = 1
        while output <= self.OutputSize:
            if 'Audio' in type:
                if output <= self.AudioOutputLimit:
                    self.__SetMatrixStatus(str(int(output)), _input, 'Audio')
            if 'Video' in type:
                self.__SetMatrixStatus(str(int(output)), _input, 'Video')
            output += 1

    def __MatchAllMatrixTie(self, match, tag):
        output = int(match.group(1))  
        inputList = match.group(2).decode().split() 
        opTag = 'Video' if tag == 'Audio' else 'Audio' 

        for value in inputList:
            if value == '--':
                break
                #value = '0'
            else:
                value = str(int(value))
            
            if str(output) not in self.outputInit[tag]:
                if value == '0' and output <= self.AudioOutputLimit:
                    self.WriteStatus('OutputTieStatus', '0', {'Output': str(output), 'Tie Type': tag})
                    self.WriteStatus('OutputTieStatus', '0', {'Output': str(output), 'Tie Type': 'Audio/Video'})
                for inp in range(1, self.InputSize+1):
                    inputStr = str(inp)
                    if value == '0':
                        if self.outputInit[tag][int(inputStr)-1] == value and self.outputInit[opTag][int(inputStr)-1] == value:
                            self.WriteStatus('InputTieStatus', 'Untied', {'Input': inputStr, 'Output': str(output)})
                    elif inputStr != value and self.outputInit[opTag][output-1] == '0':
                        self.WriteStatus('InputTieStatus', 'Untied', {'Input':inputStr, 'Output':str(output)})                     
                self.outputInit[tag][output-1] = str(output)
            if output < self.OutputSize:
                self.__SetMatrixStatus(str(output), value, tag)
            output += 1 

    def __SetMatrixStatus(self, output, newInput, tag):
        oldInput = self.OutputStatus[tag][int(output) - 1]
        opTag = 'Audio' if tag == 'Video' else 'Video'
        if oldInput != newInput:
            self.WriteStatus('OutputTieStatus', newInput, {'Output': output, 'Tie Type': tag})
            opInVal = self.ReadStatus('OutputTieStatus', {'Output': output, 'Tie Type': opTag})

            prevInputTieStatus = self.ReadStatus('InputTieStatus', {'Input': oldInput, 'Output': output})
            if prevInputTieStatus == 'Audio/Video':
                self.WriteStatus('InputTieStatus', opTag, {'Input': oldInput, 'Output': output})
            else:
                self.WriteStatus('InputTieStatus', 'Untied', {'Input': oldInput, 'Output': output})

            if opInVal == newInput:
                self.WriteStatus('OutputTieStatus', newInput, {'Output': output, 'Tie Type': 'Audio/Video'})
                self.WriteStatus('InputTieStatus', 'Audio/Video', {'Input': newInput, 'Output': output})
            else:
                self.WriteStatus('OutputTieStatus', '0', {'Output': output, 'Tie Type': 'Audio/Video'})
                self.WriteStatus('InputTieStatus', tag, {'Input': newInput, 'Output': output})
           
            self.OutputStatus[tag][int(output) - 1] = newInput

    def SetAudioMute(self, value, qualifier):
        AudioMuteState = {
            'Off': '0',
            'On': '1',
        }
        channel = int(qualifier['Output'])
        if channel < 0 or channel > self.OutputSize:
            print('Invalid Set Command for AudioMute')
        else:
            self.__SetHelper('AudioMute', '{0}*{1}Z'.format(channel, AudioMuteState[value]), value, qualifier)

    def UpdateAudioMute(self, value, qualifier):
        channel = int(qualifier['Output'])
        if channel < 0 or channel > self.OutputSize:
            print('Invalid Update Command for AudioMute')
        else:
            self.__UpdateHelper('AudioMute', '{0}Z'.format(channel), qualifier)

    def __MatchAudioMuteGlobal(self, match, qualifier):
        AudioMuteName = {
            '1': 'On',
            '0': 'Off',
            }

        AudioOutputMuteName = {
            '1': 'HDMI audio mute',
            '0': 'Off',
            }
        
        for i in range(1, self.VolumeSize + 1):
            self.WriteStatus('AudioOutputMute', AudioOutputMuteName[match.group(1).decode()], {'Output': str(i)})

        for i in range(1, self.OutputSize + 1):
            self.WriteStatus('AudioMute', AudioMuteName[match.group(1).decode()], {'Output': str(i)})

    def __MatchAudioMute(self, match, qualifier):
        AudioMuteName = {
            '1': 'On',
            '0': 'Off',
            }

        AudioOutputMuteName = {
            '0': 'Off',
            '1': 'HDMI audio mute',
            '2': 'Analog audio mute',
            '3': 'HDMI and Analog audio mute',
            '4': 'S/PDIF mute',
            '5': 'HDMI audio and S/PDIF mute',
            '6': 'Analog audio and S/PDIF mute',
            '7': 'HDMI audio, Analog audio, and S/PDIF mute'
            }
        
        if 1 <= int(match.group(1).decode()) <= self.VolumeSize:
            self.WriteStatus('AudioOutputMute', AudioOutputMuteName[match.group(2).decode()], {'Output': str(int(match.group(1).decode()))})

        if int(match.group(2).decode()) < 2:
            self.WriteStatus('AudioMute', AudioMuteName[match.group(2).decode()], {'Output': str(int(match.group(1).decode()))})
        else:
            self.WriteStatus('AudioMute', 'On', {'Output': str(int(match.group(1).decode()))})

    def SetAudioOutputMute(self, value, qualifier):
        AudioMuteState = {
            'Off': '0',
            'HDMI audio mute': '1',
            'Analog audio mute': '2',
            'HDMI and Analog audio mute': '3',
            'S/PDIF mute': '4',
            'HDMI audio and S/PDIF mute': '5',
            'Analog audio and S/PDIF mute': '6',
            'HDMI audio, Analog audio, and S/PDIF mute': '7'
        }
        channel = int(qualifier['Output'])
        if channel < 1 or channel > self.VolumeSize:
            print('Invalid Command for SetAudioOutputMute')
        else:
            self.__SetHelper('AudioOutputMute', '{0}*{1}Z'.format(channel, AudioMuteState[value]), value, qualifier)

    def UpdateAudioOutputMute(self, value, qualifier):
        channel = int(qualifier['Output'])
        if channel < 1 or channel > self.VolumeSize:
            print('Invalid Command for UpdateAudioOutputMute')
        else:
            self.__UpdateHelper('AudioOutputMute', '{0}Z'.format(channel), qualifier)

    def SetExecutiveMode(self, value, qualifier):
        ExecutiveModeState = {
            'Off': '0',
            'Mode 1': '1',
            'Mode 2': '2',
        }
        self.__SetHelper('ExecutiveMode', '{0}X'.format(ExecutiveModeState[value]), value, qualifier)

    def UpdateExecutiveMode(self, value, qualifier):
        self.__UpdateHelper('ExecutiveMode', 'X', qualifier)

    def __MatchExecutiveMode(self, match, qualifier):
        ExecutiveModeName = {
            '0': 'Off',
            '1': 'Mode 1',
            '2': 'Mode 2',
        }
        self.WriteStatus('ExecutiveMode', ExecutiveModeName[match.group(1).decode()], None)

    def SetInputGain(self, value, qualifier):

        ValueConstraints = {
            'Min': -20,
            'Max': 0
        }

        input = qualifier['Input']

        if 1 <= int(input) <= self.InputSize and ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            InputGainCmdString = '{0}*{1}G'.format(input, value)
            self.__SetHelper('InputGain', InputGainCmdString, value, qualifier)
        else:
            print('Invalid Set Command for InputGain')

    def UpdateInputGain(self, value, qualifier):
        input = qualifier['Input']
        if 1 <= int(input) <= self.InputSize:
            InputGainCmdString = '{0}G'.format(input)
            self.__UpdateHelper('InputGain', InputGainCmdString, qualifier)
        else:
            print('Invalid Update Command for InputGain')

    def __MatchInputGain(self, match, tag):
        input = str(int(match.group(1).decode()))
        value = int(match.group(2).decode())
        self.WriteStatus('InputGain', value, {'Input': input})

    def SetMatrixTieCommand(self, value, qualifier):

        TieTypeValues = {
            'Audio/Video': '!',
            'Video': '%',
            'Audio': '$',
        }

        Input = int(qualifier['Input'])
        tieType = qualifier['Tie Type']
        Output = qualifier['Output']

        if Output == 'All':
            Output = 0
        else:
            Output = int(qualifier['Output'])

        if Output < 0 or Output > self.OutputSize:
            print('Invalid Output number for MatrixTieCommand')
        elif Input < 0 or Input > self.InputSize:
            print('Invalid Input number for MatrixTieCommand')
        else:
            if Output == 0:
                MatrixTieCmdString = '{0}*{1}'.format(Input, TieTypeValues[tieType])
                self.__SetHelper('MatrixTieCommand', MatrixTieCmdString, value, qualifier)
            else:
                MatrixTieCmdString = '{0}*{1}{2}'.format(Input, Output, TieTypeValues[tieType])
                self.__SetHelper('MatrixTieCommand', MatrixTieCmdString, Output, qualifier)

    def __MatchOutputTieStatus(self, match, qualifier):
        if match.group(1):
            TieTypeStates = {
                'Aud': 'Audio',  
                'Vid': 'Video', 
                'RGB': 'Video', 
                'All': 'Audio/Video',
            }
            # output number in string.
            # input number in string
            output, _input = str(int(match.group(2))), str(int(match.group(3)))
            tieType = TieTypeStates[match.group(4).decode()]  # Tie Type

            if 'Audio' in tieType and int(output) <= self.AudioOutputLimit:
                if output not in self.outputInit['Audio']:
                    if _input == '0':  # if current tie is 0 for output then force it
                        self.WriteStatus('OutputTieStatus', '0', {'Output': output, 'Tie Type':'Audio'})
                    for inp in range(1, self.InputSize+1):
                        inputStr = str(inp)
                        if inputStr != _input or _input == '0':
                            self.WriteStatus('InputTieStatus', 'Untied', {'Input':inputStr, 'Output':output})
                    self.outputInit['Audio'].append(output)
                self.__SetMatrixStatus(output, _input, 'Audio')
            if 'Video' in tieType:
                if output not in self.outputInit['Video']:
                    if _input == '0':  # if current tie is 0 for output then force it
                        self.WriteStatus('OutputTieStatus', '0', {'Output':output, 'Tie Type':'Video'})
                    for inp in range(1, self.InputSize+1):
                        inputStr = str(inp)
                        if inputStr != _input or _input == '0':
                            self.WriteStatus('InputTieStatus', 'Untied', {'Input':inputStr, 'Output':output})
                    self.outputInit['Video'].append(output)
                self.__SetMatrixStatus(output, _input, 'Video')
        else:
            self.__MatchAllTie(match, None)

    def SetOutputVolume(self, value, qualifier):

        ValueConstraints = {
            'Min': 0,
            'Max': 100
        }

        output = qualifier['Output']

        if 1 <= int(output) <= self.VolumeSize and ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            OutputVolumeCmdString = '{0}*{1}V'.format(output, value)
            self.__SetHelper('OutputVolume', OutputVolumeCmdString, value, qualifier)
        else:
            print('Invalid Set Command for OutputVolume')

    def UpdateOutputVolume(self, value, qualifier):
        output = qualifier['Output']
        if 1 <= int(output) <= self.VolumeSize:
            OutputVolumeCmdString = '{0}V'.format(output)
            self.__UpdateHelper('OutputVolume', OutputVolumeCmdString, qualifier)
        else:
            print('Invalid Update Command for OutputVolume')

    def __MatchOutputVolume(self, match, tag):
        output = str(int(match.group(1).decode()))
        value = int(match.group(2).decode())
        self.WriteStatus('OutputVolume', value, {'Output': output})

    def SetGlobalAudioMute(self, value, qualifier):
        AudioMuteState = {
            'Off': '0*Z',
            'On': '1*Z',
        }
        GlobalAudioString = AudioMuteState[value]
        self.__SetHelper('AudioMuteState', GlobalAudioString, value, qualifier)

    def SetGlobalVideoMute(self, value, qualifier):
        VideoMuteState = {
            'Off': '0*B',
            'On': '1*B',
        }
        GlobalVideoString = VideoMuteState[value]
        self.__SetHelper('VideoMuteState', GlobalVideoString, value, qualifier)

    def __MatchVideoMuteGlobal(self, match, qualifier):
        VideoMuteName = {
            '1': 'On',
            '0': 'Off',
        }
        for i in range(1, self.OutputSize + 1):
            self.WriteStatus('VideoMute', VideoMuteName[match.group(1).decode()], {'Output': str(i)})

    def SetVideoMute(self, value, qualifier):
        VideoMuteState = {
            'Off': '0',
            'On': '1',
        }
        channel = qualifier['Output']
        if int(channel) < 0 or int(channel) > self.OutputSize:
            print('Invalid Set Command for VideoMute')
        else:
            self.__SetHelper('VideoMute', '{0}*{1}B'.format(channel, VideoMuteState[value]), value, qualifier)

    def UpdateVideoMute(self, value, qualifier):
        channel = qualifier['Output']
        if int(channel) < 0 or int(channel) > self.OutputSize:
            print('Invalid Update Command for VideoMute')
        else:
            VideoMuteCmdString = '{0}B'.format(channel)
            self.__UpdateHelper('VideoMute', VideoMuteCmdString, {'Output': channel})

    def __MatchVideoMute(self, match, qualifier):
        VideoMuteName = {
            '0': 'Off',
            '1': 'On',
        }
        self.WriteStatus('VideoMute', VideoMuteName[match.group(2).decode()], {'Output': match.group(1).decode()})

    def SetSavePreset(self, value, qualifier):
        if int(value) <= 32 or int(value) > 0:
            SavePresetCmdString = '{0},'.format(value)
            self.__SetHelper('SavePreset', SavePresetCmdString, value, qualifier)
        else:
            print('Invalid Set Command for SavePreset')

    def SetRecallPreset(self, value, qualifier):
        if int(value) <= 32 or int(value) > 0:
            RecallPresetCmdString = '{0}.'.format(value)
            self.__SetHelper('RecallPreset', RecallPresetCmdString, value, qualifier)
        else:
            print('Invalid Set Command for RecallPreset')

    def UpdateSignalStatus(self, value, qualifier):
        self.__UpdateHelper('SignalStatus', '0LS', qualifier)

    def __MatchSignalStatus(self, match, qualifier):

        InputList = match.group(1).decode()
        input = 1
        for stat in InputList:
            value = 'No Signal Detected' if stat == '0' else 'Signal Detected'
            self.WriteStatus('SignalStatus', value, {'Input': str(input)})
            input += 1

    def UpdateTemperature(self, value, qualifier):
        self.__UpdateHelper('Temperature', 'S', qualifier)

    def __MatchTemperature(self, match, qualifier):
        value = int(float(match.group(2).decode()))
        self.WriteStatus('Temperature', str(value) + ' C', None)

    def __SetHelper(self, command, commandstring, value, qualifier):
        self.Debug = True
        self.Send(commandstring)

    def __UpdateHelper(self, command, commandstring, qualifier):
        if self.initializationChk:
            self.OnConnected()
            self.initializationChk = False

        self.counter = self.counter + 1
        if self.counter > self.connectionCounter and self.connectionFlag:
            self.OnDisconnected()
        
        if self.Authenticated in ['User', 'Admin', 'Not Needed']:
            if self.Unidirectional == 'True':
                print('Inappropriate Command ', command)
            else:
                if self.VerboseDisabled:
                    @Wait(1)
                    def SendVerbose():
                        self.Send('w3cv\r\n')
                        self.Send(commandstring)
                else:
                    self.Send(commandstring)
        else:
            print('Inappropriate Command ', command)

    def __MatchErrors(self, match, tag):
        DEVICE_ERROR_CODES = {
            '01': 'Invalid input number (too large)',
            '10': 'Invalid command',
            '11': 'Invalid preset number',
            '12': 'Invalid output number or port number',
            '13': 'Invalid parameter (out of range)',
            '14': 'Command not available for this configuration',
            '17': 'System timed out (caused by direct write of global presets)',
            '21': 'Invalid room number',
            '22': 'Busy',
            '24': 'Privilege violation',
            '25': 'Device not present',
            '26': 'Maximum number of connections exceeded',
            '27': 'Invalid event number',
            '28': 'Bad filename or file not found',
            '30': 'Hardware failure (followed by a colon [:] and a descriptor number)',
            '31': 'Attempt to break port pass-through when it has not been set',
        }
        value = match.group(1).decode()
        if value in DEVICE_ERROR_CODES:
            print([DEVICE_ERROR_CODES[value]])
        else:
            print(['Unrecognized error code: ' + match.group(0).decode()])

    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0
        

    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False
        if 'Serial' not in self.ConnectionType:
            self.Authenticated = 'Not Needed'
            self.PasswdPromptCount = 0
        self.VerboseDisabled = True
        self.lastInputSignalUpdate = 0

    def extr_15_1865_44(self):
        self.InputSize = 4
        self.OutputSize = 4
        self.VolumeSize = 2
        self.AudioOutputLimit = 2
        self.MatrixListInit()

    def extr_15_1865_84(self):
        self.InputSize = 8
        self.OutputSize = 4
        self.VolumeSize = 2
        self.AudioOutputLimit = 2
        self.MatrixListInit()

    def extr_15_1865_88(self):
        self.InputSize = 8
        self.OutputSize = 8
        self.VolumeSize = 2
        self.AudioOutputLimit = 2
        self.MatrixListInit()

    def extr_15_1865_168(self):
        self.InputSize = 16
        self.OutputSize = 8
        self.VolumeSize = 4
        self.AudioOutputLimit = 4
        self.MatrixListInit()

    def extr_15_1865_1616(self):
        self.InputSize = 16
        self.OutputSize = 16
        self.VolumeSize = 4
        self.AudioOutputLimit = 4
        self.MatrixListInit()
        
        
    def MatrixListInit(self):
        self.OutputStatus['Video'] = ['0' for i in range(0, self.OutputSize)]
        self.OutputStatus['Audio'] = ['0' for i in range(0, self.OutputSize)]
        self.outputInit['Video'] = ['0' for i in range(0, self.InputSize)]
        self.outputInit['Audio'] = ['0' for i in range(0, self.InputSize)]

    ######################################################
    # RECOMMENDED not to modify the code below this point
    ######################################################    
    # Send Control Commands
    def Set(self, command, value, qualifier=None):
        method = 'Set%s' % command
        if hasattr(self, method) and callable(getattr(self, method)):
            getattr(self, method)(value, qualifier)
        else:
            print(command, 'does not support Set.')
    
    def MissingCredentialsLog(self, credential_type):
        if isinstance(self, EthernetClientInterface):
            port_info = 'IP Address: {0}:{1}'.format(self.IPAddress, self.IPPort)
        elif isinstance(self, SerialInterface):
            port_info = 'Host Alias: {0}\r\nPort: {1}'.format(self.Host.DeviceAlias, self.Port)
        else:
            return 
        ProgramLog("{0} module received a request from the device for a {1}, "
                   "but device{1} was not provided.\n Please provide a device{1} "
                   "and attempt again.\n Ex: dvInterface.device{1} = '{1}'\n Please "
                   "review the communication sheet.\n {2}"
                   .format(__name__, credential_type, port_info), 'warning') 

    # Send Update Commands
    def Update(self, command, qualifier=None):
        method = 'Update%s' % command
        if hasattr(self, method) and callable(getattr(self, method)):
            getattr(self, method)(None, qualifier)
        else:
            print(command, 'does not support Update.') 

    # This method is to tie an specific command with a parameter to a call back method
    # when its value is updated. It sets how often the command will be query, if the command
    # have the update method.
    # If the command doesn't have the update feature then that command is only used for feedback 
    def SubscribeStatus(self, command, qualifier, callback):
        Command = self.Commands.get(command)
        if Command:
            if command not in self.Subscription:
                self.Subscription[command] = {'method':{}}
        
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
        
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        if Parameter in qualifier:
                            Method[qualifier[Parameter]] = {}
                            Method = Method[qualifier[Parameter]]
                        else:
                            return
        
            Method['callback'] = callback
            Method['qualifier'] = qualifier    
        else:
            print(command, 'does not exist in the module')

    # This method is to check the command with new status have a callback method then trigger the callback
    def NewStatus(self, command, value, qualifier):
        if command in self.Subscription :
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
            Command = self.Commands[command]
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        break
            if 'callback' in Method and Method['callback']:
                Method['callback'](command, value, qualifier)  

    # Save new status to the command
    def WriteStatus(self, command, value, qualifier=None):
        self.counter = 0
        if not self.connectionFlag:
            self.OnConnected()
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    if Parameter in qualifier:
                        Status[qualifier[Parameter]] = {}
                        Status = Status[qualifier[Parameter]]
                    else:
                        return  
        try:
            if Status['Live'] != value:
                Status['Live'] = value
                self.NewStatus(command, value, qualifier)
        except:
            Status['Live'] = value
            self.NewStatus(command, value, qualifier)            

    # Read the value from a command.
    def ReadStatus(self, command, qualifier=None):
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    return None
        try:
            return Status['Live']
        except:
            return None

    def __ReceiveData(self, interface, data):
    # handling incoming unsolicited data
        self._ReceiveBuffer += data
        # check incoming data if it matched any expected data from device module
        if self.CheckMatchedString() and len(self._ReceiveBuffer) > 10000:
            self._ReceiveBuffer = b''

    # Add regular expression so that it can be check on incoming data from device.
    def AddMatchString(self, regex_string, callback, arg):
        if regex_string not in self._compile_list:
            self._compile_list[regex_string] = {'callback': callback, 'para':arg}
                

    # Check incoming unsolicited data to see if it was matched with device expectancy. 
    def CheckMatchedString(self):
        for regexString in self._compile_list:
            while True:
                result = search(regexString, self._ReceiveBuffer)                
                if result:
                    self._compile_list[regexString]['callback'](result, self._compile_list[regexString]['para'])
                    self._ReceiveBuffer = self._ReceiveBuffer.replace(result.group(0), b'')
                else:
                    break
        return True 

    def MissingCredentialsLog(self, credential_type):
        if isinstance(self, EthernetClientInterface):
            port_info = 'IP Address: {0}:{1}'.format(self.IPAddress, self.IPPort)
        elif isinstance(self, SerialInterface):
            port_info = 'Host Alias: {0}\r\nPort: {1}'.format(self.Host.DeviceAlias, self.Port)
        else:
            return
        ProgramLog("{0} module received a request from the device for a {1}, "
                   "but device{1} was not provided.\n Please provide a device{1} "
                   "and attempt again.\n Ex: dvInterface.device{1} = '{1}'\n Please "
                   "review the communication sheet.\n {2}"
                   .format(__name__, credential_type, port_info), 'warning')

class SerialClass(SerialInterface, DeviceClass):

    def __init__(self, Host, Port, Baud=9600, Data=8, Parity='None', Stop=1, FlowControl='Off', CharDelay=0, Model=None):
        SerialInterface.__init__(self, Host, Port, Baud, Data, Parity, Stop, FlowControl, CharDelay)
        self.ConnectionType = 'Serial'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()

class EthernetClass(EthernetClientInterface, DeviceClass):

    def __init__(self, Hostname, IPPort, Protocol='TCP', ServicePort=0, Model=None):
        EthernetClientInterface.__init__(self, Hostname, IPPort, Protocol, ServicePort)
        self.ConnectionType = 'Ethernet'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass
        if len(self.Models) > 0:
            if Model not in self.Models:
                print('Model mismatch')
            else:
                self.Models[Model]()

