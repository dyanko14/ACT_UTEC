from extronlib.interface import EthernetClientInterface, EthernetServerInterface, SerialInterface, IRInterface, RelayInterface
from re import compile, search
from extronlib.system import Wait, ProgramLog


class DeviceClass:

    def __init__(self):
        self.Unidirectional = 'False'
        self.connectionCounter = 15

        # Do not change this the variables values below
        self.DefaultResponseTimeout = 0.3
        self._compile_list = {}
        self.Subscription = {}
        self.ReceiveData = self.__ReceiveData
        self._ReceiveBuffer = b''
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True
        self.Models = {}

        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'GroupMicInputGain': {'Parameters': ['Group'], 'Status': {}},
            'GroupMixpointGain': {'Parameters': ['Group'], 'Status': {}},
            'GroupMute': {'Parameters': ['Group'], 'Status': {}},
            'GroupOutputVolume': {'Parameters': ['Group'], 'Status': {}},
            'GroupPostMixerTrim': {'Parameters': ['Group'], 'Status': {}},
            'GroupPreMixerGain': {'Parameters': ['Group'], 'Status': {}},
            'GroupVirtualReturnGain': {'Parameters': ['Group'], 'Status': {}},
            'MicGain': {'Parameters': ['Input'], 'Status': {}},
            'MicMute': {'Parameters': ['Input'], 'Status': {}},
            'MixpointGain': {'Parameters': ['Input', 'Output'], 'Status': {}},
            'MixpointMute': {'Parameters': ['Input', 'Output'], 'Status': {}},
            'OutputMute': {'Parameters': ['Output'], 'Status': {}},
            'OutputVolume': {'Parameters': ['Output'], 'Status': {}},
            'PremixGain': {'Parameters': ['Input'], 'Status': {}},
            'PremixMute': {'Parameters': ['Input'], 'Status': {}},
            'PresetRecall': {'Status': {}},
            'PresetSave': {'Status': {}},
            'VirtualReturnGain': {'Parameters': ['Channel'], 'Status': {}},
            'VirtualReturnMute': {'Parameters': ['Channel'], 'Status': {}}
        }

        self.GroupFunction = {}

        self.VerboseDisabled = True
        self.PasswdPromptCount = 0
        self.Authenticated = 'Not Needed'
        self.devicePassword = None

        if self.Unidirectional == 'False':
            self.AddMatchString(compile(b'Vrb3\r\n'), self.__MatchVerboseMode, None)
            self.AddMatchString(compile(b'GrpmD([0-9]{2})\*([-+][0-9]{5})\r\n'), self.__MatchGroup, None)
            self.AddMatchString(compile(b'DsG(4000[0-5])\*([0-9]{5})\r\n'), self.__MatchMicGain, None)
            self.AddMatchString(compile(b'DsM(4000[0-5])\*(0|1)\r\n'), self.__MatchMicMute, None)
            self.AddMatchString(compile(b'DsG2([0-9]{2})([0-9]{2})\*([0-9]{5})\r\n'), self.__MatchMixpointGain, None)
            self.AddMatchString(compile(b'DsM2([0-9]{2})([0-9]{2})\*(0|1)\r\n'), self.__MatchMixpointMute, None)
            self.AddMatchString(compile(b'DsM(6000[0-3])\*(0|1)\r\n'), self.__MatchOutputMute, None)
            self.AddMatchString(compile(b'DsG(6000[0-3])\*([0-9]{5})\r\n'), self.__MatchOutputVolume, None)
            self.AddMatchString(compile(b'DsG(4010[0-5])\*([0-9]{5})\r\n'), self.__MatchPremixGain, None)
            self.AddMatchString(compile(b'DsM(4010[0-5])\*(0|1)\r\n'), self.__MatchPremixMute, None)
            self.AddMatchString(compile(b'DsG(5000[0-3])\*([0-9]{5})\r\n'), self.__MatchVirtualReturnGain, None)
            self.AddMatchString(compile(b'DsM(5000[0-3])\*(0|1)\r\n'), self.__MatchVirtualReturnMute, None)
            self.AddMatchString(compile(b'E([0-9]{2})\r\n'), self.__MatchError, None)

            if 'Serial' not in self.ConnectionType:
                self.AddMatchString(compile(b'Password:'), self.__MatchPassword, None)
                self.AddMatchString(compile(b'Login Administrator\r\n'), self.__MatchLoginAdmin, None)
                self.AddMatchString(compile(b'Login User\r\n'), self.__MatchLoginUser, None)

    def __MatchPassword(self, match, tag):
        self.PasswdPromptCount += 1
        if self.PasswdPromptCount > 1:
            print('Log in failed. Please supply proper Admin password')
        else:
            self.SetPassword(None, None)
        self.Authenticated = 'None'

    def SetPassword(self, value, qualifier):
        if self.devicePassword is not None:
            self.Send('{0}\r\n'.format(self.devicePassword))
        else:
            self.MissingCredentialsLog('Password')

    def __MatchLoginAdmin(self, match, tag):
        self.Authenticated = 'Admin'
        self.PasswdPromptCount = 0

    def __MatchLoginUser(self, match, tag):
        self.Authenticated = 'User'
        self.PasswdPromptCount = 0
        print('Logged in as User. May have limited functionality.')

    def __MatchVerboseMode(self, match, qualifier):
        self.VerboseDisabled = False
        self.OnConnected()

    def SetGroupMicInputGain(self, value, qualifier):
        ValueConstraints = {
            'Min': -18,
            'Max': 80
        }

        group = qualifier['Group']
        if 1 <= int(group) <= 32 and ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            level = int(value * 10)
            commandString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupMicInputGain'
            self.__SetHelper('GroupMicInputGain', commandString, value, qualifier, 3)
        else:
            print('Invalid Command for SetGroupMicInputGain')

    def UpdateGroupMicInputGain(self, value, qualifier):
        group = qualifier['Group']
        if 1 <= int(group) <= 32:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupMicInputGain'
            self.__UpdateHelper('GroupMicInputGain', commandString, value, qualifier)
        else:
            print('Invalid Command for UpdateGroupMicInputGain')

    def SetGroupMixpointGain(self, value, qualifier):
        ValueConstraints = {
            'Min': -35,
            'Max': 25
        }

        group = qualifier['Group']
        if 1 <= int(group) <= 32 and ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            level = int(value * 10)
            commandString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupMixpointGain'
            self.__SetHelper('GroupMixpointGain', commandString, value, qualifier, 3)
        else:
            print('Invalid Command for SetGroupMixpointGain')

    def UpdateGroupMixpointGain(self, value, qualifier):
        group = qualifier['Group']
        if 1 <= int(group) <= 32:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupMixpointGain'
            self.__UpdateHelper('GroupMixpointGain', commandString, value, qualifier)
        else:
            print('Invalid Command for UpdateGroupMixpointGain')

    def SetGroupMute(self, value, qualifier):
        ValueStateValues = {
            'On': '1',
            'Off': '0'
        }

        group = qualifier['Group']
        if 1 <= int(group) <= 32:
            commandString = 'wd{0}*{1}grpm\r\n'.format(group, ValueStateValues[value])
            self.GroupFunction[group] = 'GroupMute'
            self.__SetHelper('GroupMute', commandString, value, qualifier)
        else:
            print('Invalid Command for SetGroupMute')

    def UpdateGroupMute(self, value, qualifier):
        group = qualifier['Group']
        if 1 <= int(group) <= 32:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupMute'
            self.__UpdateHelper('GroupMute', commandString, value, qualifier)
        else:
            print('Invalid Command for UpdateGroupMute')

    def SetGroupOutputVolume(self, value, qualifier):
        ValueConstraints = {
            'Min': -100,
            'Max': 0
        }

        group = qualifier['Group']
        if 1 <= int(group) <= 32 and ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            level = int(value * 10)
            commandString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupOutputVolume'
            self.__SetHelper('GroupOutputVolume', commandString, value, qualifier, 3)
        else:
            print('Invalid Command for SetGroupOutputVolume')

    def UpdateGroupOutputVolume(self, value, qualifier):
        group = qualifier['Group']
        if 1 <= int(group) <= 32:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupOutputVolume'
            self.__UpdateHelper('GroupOutputVolume', commandString, value, qualifier)

    def SetGroupPostMixerTrim(self, value, qualifier):
        ValueConstraints = {
            'Min': -12,
            'Max': 12
        }

        group = qualifier['Group']
        if 1 <= int(group) <= 32 and ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            level = int(value * 10)
            commandString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupPostMixerTrim'
            self.__SetHelper('GroupPostMixerTrim', commandString, value, qualifier, 3)
        else:
            print('Invalid Command for SetGroupPostMixerTrim')

    def UpdateGroupPostMixerTrim(self, value, qualifier):
        group = qualifier['Group']
        if 1 <= int(group) <= 32:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupPostMixerTrim'
            self.__UpdateHelper('GroupPostMixerTrim', commandString, value, qualifier)

    def SetGroupPreMixerGain(self, value, qualifier):
        ValueConstraints = {
            'Min': -100,
            'Max': 12
        }

        group = qualifier['Group']
        if 1 <= int(group) <= 32 and ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            level = int(value * 10)
            commandString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupPreMixerGain'
            self.__SetHelper('GroupPreMixerGain', commandString, value, qualifier, 3)
        else:
            print('Invalid Command for SetGroupPreMixerGain')

    def UpdateGroupPreMixerGain(self, value, qualifier):
        group = qualifier['Group']
        if 1 <= int(group) <= 32:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupPreMixerGain'
            self.__UpdateHelper('GroupPreMixerGain', commandString, value, qualifier)

    def SetGroupVirtualReturnGain(self, value, qualifier):
        ValueConstraints = {
            'Min': -100,
            'Max': 12
        }

        group = qualifier['Group']
        if 1 <= int(group) <= 32 and ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            level = int(value * 10)
            commandString = 'wd{0}*{1:+06d}grpm\r\n'.format(group, level)
            self.GroupFunction[group] = 'GroupVirtualReturnGain'
            self.__SetHelper('GroupVirtualReturnGain', commandString, value, qualifier, 3)
        else:
            print('Invalid Command for SetGroupVirtualReturnGain')

    def UpdateGroupVirtualReturnGain(self, value, qualifier):
        group = qualifier['Group']
        if 1 <= int(group) <= 32:
            commandString = 'wd{0}grpm\r\n'.format(group)
            self.GroupFunction[group] = 'GroupVirtualReturnGain'
            self.__UpdateHelper('GroupVirtualReturnGain', commandString, value, qualifier)

    def __MatchGroup(self, match, tag):

        group = str(int(match.group(1)))
        if group in self.GroupFunction:
            command = self.GroupFunction[group]
            if command == 'GroupMute':
                GroupMuteStateNames = {
                    '1': 'On',
                    '0': 'Off'
                }
                qualifier = {'Group': group}
                value = match.group(2).decode()[-1]
                self.WriteStatus(command, GroupMuteStateNames[value], qualifier)
            elif command in ['GroupMicInputGain', 'GroupPreMixerGain',
                             'GroupOutputVolume', 'GroupMixpointGain',
                             'GroupPostMixerTrim', 'GroupVirtualReturnGain'
                             ]:
                qualifier = {'Group': group}
                value = int(int(match.group(2)) / 10)
                self.WriteStatus(command, value, qualifier)

    def SetMicGain(self, value, qualifier):
        ValueConstraints = {
            'Min': -18,
            'Max': 80
        }

        channel = int(qualifier['Input'])
        if 1 <= channel <= 6 and ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            level = 2048 + int(value * 10)
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(channel + 39999, level)
            self.__SetHelper('MicGain', commandString, value, qualifier, 3)
        else:
            print('Invalid Command for SetMicGain')

    def UpdateMicGain(self, value, qualifier):
        channel = int(qualifier['Input'])
        if 1 <= channel <= 6:
            commandString = 'wG{0}AU\r\n'.format(channel + 39999)
            self.__UpdateHelper('MicGain', commandString, value, qualifier)
        else:
            print('Invalid Command for UpdateMicGain')

    def __MatchMicGain(self, match, tag):
        channel = str(int(match.group(1)) - 39999)
        qualifier = {'Input': channel}
        value = round((int(match.group(2)) - 2048) / 10)
        self.WriteStatus('MicGain', value, qualifier)

    def SetMicMute(self, value, qualifier):
        ValueStateValues = {
            'On': '1',
            'Off': '0'
        }

        channel = int(qualifier['Input'])
        if 1 <= channel <= 6:
            commandString = 'wM{0}*{1}AU\r\n'.format(channel + 39999, ValueStateValues[value])
            self.__SetHelper('MicMute', commandString, value, qualifier)
        else:
            print('Invalid Command for SetMicMute')

    def UpdateMicMute(self, value, qualifier):
        channel = int(qualifier['Input'])
        if 1 <= channel <= 6:
            commandString = 'wM{0}*AU\r\n'.format(channel + 39999)
            self.__UpdateHelper('MicMute', commandString, value, qualifier)
        else:
            print('Invalid Command for UpdateMicMute')

    def __MatchMicMute(self, match, tag):
        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        channel = str(int(match.group(1)) - 39999)
        qualifier = {'Input': channel}
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('MicMute', value, qualifier)

    def SetMixpointGain(self, value, qualifier):
        MixpointGainInputStateValues = {
            '1': '00', '2': '01', '3': '02', '4': '03', '5': '04', '6': '05',
            'A': '06', 'B': '07', 'C': '08', 'D': '09',
        }
        MixpointOutputStateValues = {
            '1': '00', '2': '01', '3': '02', '4': '03',
            'A': '04', 'B': '05', 'C': '06', 'D': '07',
        }

        ValueConstraints = {
            'Min': -35,
            'Max': 25
        }

        Input, Output = qualifier['Input'], qualifier['Output']
        if ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            inputValue = MixpointGainInputStateValues[Input]
            outputValue = MixpointOutputStateValues[Output]
            level = 2048 + int(value * 10)
            commandString = 'wG2{0}{1}*{2:05d}AU\r\n'.format(inputValue, outputValue, level)
            self.__SetHelper('MixpointGain', commandString, value, qualifier, 3)
        else:
            print('Invalid Command for SetMixpointGain')

    def UpdateMixpointGain(self, value, qualifier):
        MixpointGainInputStateValues = {
            '1': '00', '2': '01', '3': '02', '4': '03', '5': '04', '6': '05',
            'A': '06', 'B': '07', 'C': '08', 'D': '09',
        }

        MixpointOutputStateValues = {
            '1': '00', '2': '01', '3': '02', '4': '03',
            'A': '04', 'B': '05', 'C': '06', 'D': '07',
        }

        Input, Output = qualifier['Input'], qualifier['Output']
        inputValue = MixpointGainInputStateValues[Input]
        outputValue = MixpointOutputStateValues[Output]
        commandString = 'wG2{0}{1}AU\r\n'.format(inputValue, outputValue)
        self.__UpdateHelper('MixpointGain', commandString, value, qualifier)

    def __MatchMixpointGain(self, match, tag):
        MixpointGainInputStateNames = {
            '00': '1', '01': '2', '02': '3', '03': '4', '04': '5', '05': '6',
            '06': 'A', '07': 'B', '08': 'C', '09': 'D',
        }

        MixpointOutputStateNames = {
            '00': '1', '01': '2', '02': '3', '03': '4',
            '04': 'A', '05': 'B', '06': 'C', '07': 'D'
        }

        if 0 <= int(match.group(1).decode()) <= 36:
            Input = MixpointGainInputStateNames[match.group(1).decode()]
            Output = MixpointOutputStateNames[match.group(2).decode()]
            value = round((int(match.group(3)) - 2048) / 10)
            qualifier = {'Input': Input, 'Output': Output}
            self.WriteStatus('MixpointGain', value, qualifier)

    def SetMixpointMute(self, value, qualifier):
        MixpointInputStateValues = {
            '1': '00', '2': '01', '3': '02', '4': '03', '5': '04', '6': '05',
            'A': '06', 'B': '07', 'C': '08', 'D': '09'
        }

        MixpointOutputStateValues = {
            '1': '00', '2': '01', '3': '02', '4': '03',
            'A': '04', 'B': '05', 'C': '06', 'D': '07',
        }

        ValueStateValues = {
            'On': '1',
            'Off': '0'
        }

        Input, Output = qualifier['Input'], qualifier['Output']
        inputValue = MixpointInputStateValues[Input]
        outputValue = MixpointOutputStateValues[Output]
        commandString = 'wM2{0}{1}*{2}AU\r\n'.format(inputValue, outputValue, ValueStateValues[value])
        self.__SetHelper('MixpointMute', commandString, value, qualifier)

    def UpdateMixpointMute(self, value, qualifier):
        MixpointInputStateValues = {
            '1': '00', '2': '01', '3': '02', '4': '03', '5': '04', '6': '05',
            'A': '06', 'B': '07', 'C': '08', 'D': '09'
        }

        MixpointOutputStateValues = {
            '1': '00', '2': '01', '3': '02', '4': '03',
            'A': '04', 'B': '05', 'C': '06', 'D': '07',
        }

        Input, Output = qualifier['Input'], qualifier['Output']
        inputValue = MixpointInputStateValues[Input]
        outputValue = MixpointOutputStateValues[Output]
        commandString = 'wM2{0}{1}AU\r\n'.format(inputValue, outputValue)
        self.__UpdateHelper('MixpointMute', commandString, value, qualifier)

    def __MatchMixpointMute(self, match, tag):
        MixpointInputStateNames = {
            '00': '1', '01': '2', '02': '3', '03': '4', '04': '5', '05': '6',
            '06': 'A', '07': 'B', '08': 'C', '09': 'D'
        }

        MixpointOutputStateNames = {
            '00': '1', '01': '2', '02': '3', '03': '4',
            '04': 'A', '05': 'B', '06': 'C', '07': 'D'
        }

        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        if 0 <= int(match.group(1).decode()) <= 36:
            Input = MixpointInputStateNames[match.group(1).decode()]
            Output = MixpointOutputStateNames[match.group(2).decode()]
            value = ValueStateValues[match.group(3).decode()]
            qualifier = {'Input': Input, 'Output': Output}
            self.WriteStatus('MixpointMute', value, qualifier)

    def SetOutputMute(self, value, qualifier):
        ValueStateValues = {
            'On': '1',
            'Off': '0'
        }

        channel = int(qualifier['Output'])
        if 1 <= channel <= 4:
            commandString = 'wM{0}*{1}AU\r\n'.format(channel + 59999, ValueStateValues[value])
            self.__SetHelper('OutputMute', commandString, value, qualifier)
        else:
            print('Invalid Command for SetOutputMute')

    def UpdateOutputMute(self, value, qualifier):
        channel = int(qualifier['Output'])
        if 1 <= channel <= 4:
            commandString = 'wM{0}*AU\r\n'.format(channel + 59999)
            self.__UpdateHelper('OutputMute', commandString, value, qualifier)
        else:
            print('Invalid Command for UpdateOutputMute')

    def __MatchOutputMute(self, match, tag):
        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        channel = str(int(match.group(1)) - 59999)
        qualifier = {'Output': channel}
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('OutputMute', value, qualifier)

    def SetOutputVolume(self, value, qualifier):
        ValueConstraints = {
            'Min': -100,
            'Max': 0
        }

        channel = int(qualifier['Output'])
        if 1 <= channel <= 4 and ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            level = 2048 + int(value * 10)
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(channel + 59999, level)
            self.__SetHelper('OutputVolume', commandString, value, qualifier, 3)
        else:
            print('Invalid Command for SetOutputVolume')

    def UpdateOutputVolume(self, value, qualifier):
        channel = int(qualifier['Output'])
        if 1 <= channel <= 4:
            commandString = 'wG{0}AU\r\n'.format(channel + 59999)
            self.__UpdateHelper('OutputVolume', commandString, value, qualifier)
        else:
            print('Invalid Command for UpdateOutputVolume')

    def __MatchOutputVolume(self, match, tag):
        channel = str(int(match.group(1)) - 59999)
        qualifier = {'Output': channel}
        value = round((int(match.group(2)) - 2048) / 10)
        self.WriteStatus('OutputVolume', value, qualifier)

    def SetPremixGain(self, value, qualifier):
        ValueConstraints = {
            'Min': -100,
            'Max': 12
        }

        channel = int(qualifier['Input'])
        if 1 <= channel <= 6 and ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            level = 2048 + int(value * 10)
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(channel + 40099, level)
            self.__SetHelper('PremixGain', commandString, value, qualifier, 3)
        else:
            print('Invalid Command for SetPremixGain')

    def UpdatePremixGain(self, value, qualifier):
        channel = int(qualifier['Input'])
        if 1 <= channel <= 6:
            commandString = 'wG{0}AU\r\n'.format(channel + 40099)
            self.__UpdateHelper('PremixGain', commandString, value, qualifier)
        else:
            print('Invalid Command for UpdatePremixGain')

    def __MatchPremixGain(self, match, tag):
        channel = str(int(match.group(1)) - 40099)
        qualifier = {'Input': channel}
        value = round((int(match.group(2)) - 2048) / 10)
        self.WriteStatus('PremixGain', value, qualifier)

    def SetPremixMute(self, value, qualifier):
        ValueStateValues = {
            'On': '1',
            'Off': '0'
        }

        channel = int(qualifier['Input'])
        if 1 <= channel <= 6:
            commandString = 'wM{0}*{1}AU\r\n'.format(channel + 40099, ValueStateValues[value])
            self.__SetHelper('PremixMute', commandString, value, qualifier)
        else:
            print('Invalid Command for SetPremixMute')

    def UpdatePremixMute(self, value, qualifier):
        channel = int(qualifier['Input'])
        if 1 <= channel <= 6:
            commandString = 'wM{0}*AU\r\n'.format(channel + 40099)
            self.__UpdateHelper('PremixMute', commandString, value, qualifier)
        else:
            print('Invalid Command for UpdatePremixMute')

    def __MatchPremixMute(self, match, tag):
        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        channel = str(int(match.group(1)) - 40099)
        qualifier = {'Input': channel}
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('PremixMute', value, qualifier)

    def SetPresetRecall(self, value, qualifier):
        if 0 < int(value) <= 32:
            commandString = '{0}.'.format(value)
            self.__SetHelper('PresetRecall', commandString, value, qualifier)
        else:
            print('Invalid Command for SetPresetRecall')

    def SetPresetSave(self, value, qualifier):
        if 0 < int(value) <= 32:
            commandString = '{0},'.format(value)
            self.__SetHelper('PresetSave', commandString, value, qualifier)
        else:
            print('Invalid Command for SetPresetSave')

    def SetVirtualReturnGain(self, value, qualifier):
        VirtualChannels = ['A', 'B', 'C', 'D']

        ValueConstraints = {
            'Min': -100,
            'Max': 12
        }

        channel = qualifier['Channel']
        if channel in VirtualChannels and ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            level = 2048 + int(value * 10)
            ChannelValue = ord(channel) + 49935
            commandString = 'wG{0}*{1:05d}AU\r\n'.format(ChannelValue, level)
            self.__SetHelper('VirtualReturnGain', commandString, value, qualifier, 3)
        else:
            print('Invalid Command for SetVirtualReturnGain')

    def UpdateVirtualReturnGain(self, value, qualifier):
        VirtualChannels = ['A', 'B', 'C', 'D']

        channel = qualifier['Channel']
        if channel in VirtualChannels:
            ChannelValue = ord(channel) + 49935
            commandString = 'wG{0}AU\r\n'.format(ChannelValue)
            self.__UpdateHelper('VirtualReturnGain', commandString, value, qualifier)
        else:
            print('Invalid Command for UpdateVirtualReturnGain')

    def __MatchVirtualReturnGain(self, match, tag):
        channel = chr(int(match.group(1)) - 49935)
        qualifier = {'Channel': channel}
        value = round((int(match.group(2)) - 2048) / 10)
        self.WriteStatus('VirtualReturnGain', value, qualifier)

    def SetVirtualReturnMute(self, value, qualifier):
        VirtualChannels = ['A', 'B', 'C', 'D']

        ValueStateValues = {
            'On': '1',
            'Off': '0'
        }

        channel = qualifier['Channel']
        if channel in VirtualChannels:
            ChannelValue = ord(channel) + 49935
            commandString = 'wM{0}*{1}AU\r\n'.format(ChannelValue, ValueStateValues[value])
            self.__SetHelper('VirtualReturnMute', commandString, value, qualifier)
        else:
            print('Invalid Command for SetVirtualReturnMute')

    def UpdateVirtualReturnMute(self, value, qualifier):
        VirtualChannels = ['A', 'B', 'C', 'D']

        channel = qualifier['Channel']
        if channel in VirtualChannels:
            ChannelValue = ord(channel) + 49935
            commandString = 'wM{0}AU\r\n'.format(ChannelValue)
            self.__UpdateHelper('VirtualReturnMute', commandString, value, qualifier)
        else:
            print('Invalid Command for UpdateVirtualReturnMute')

    def __MatchVirtualReturnMute(self, match, tag):
        ValueStateValues = {
            '1': 'On',
            '0': 'Off'
        }

        channel = chr(int(match.group(1)) - 49935)
        qualifier = {'Channel': channel}
        value = ValueStateValues[match.group(2).decode()]
        self.WriteStatus('VirtualReturnMute', value, qualifier)

    def __SetHelper(self, command, commandstring, value, qualifier, queryDisallowTime=0):
        self.Debug = True
        if self.VerboseDisabled:
            @Wait(1)
            def SendVerbose():
                self.Send('w3cv\r\n')
                self.Send(commandstring)
        else:
            self.Send(commandstring)

    def __UpdateHelper(self, command, commandstring, value, qualifier):
        if self.initializationChk:
            self.OnConnected()
            self.initializationChk = False

        self.counter += 1
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

    def __MatchError(self, match, tag):
        DeviceErrorCodes = {
            '01': 'Invalid input number (number is too large)',
            '12': 'Invalid port number',
            '13': 'Invalid parameter (number is out of range)',
            '14': 'Not valid for this configuration',
            '17': 'System timed out',
            '22': 'Busy',
            '23': 'Checksum error (for file uploads)',
            '24': 'Privilege violation',
            '25': 'Device is not present',
            '26': 'Maximum connections exceeded',
            '27': 'Invalid event number',
            '28': 'Bad filename or file not found',
        }

        if match.group(1).decode() in DeviceErrorCodes:
            print(DeviceErrorCodes[match.group(1).decode()])
        else:
            print('Unrecognized error code: ' + match.group(0).decode())

    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0

    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False

        self.Authenticated = 'Not Needed'
        self.PasswdPromptCount = 0
        self.VerboseDisabled = True

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

    # Send Update Commands

    def Update(self, command, qualifier=None):
        method = 'Update%s' % command
        if hasattr(self, method) and callable(getattr(self, method)):
            getattr(self, method)(None, qualifier)
        else:
            print(command, 'does not support Update.')

    def __ReceiveData(self, interface, data):
        # handling incoming unsolicited data
        self._ReceiveBuffer += data
        # check incoming data if it matched any expected data from device module
        if self.CheckMatchedString() and len(self._ReceiveBuffer) > 10000:
            self._ReceiveBuffer = b''

    # Add regular expression so that it can be check on incoming data from device.
    def AddMatchString(self, regex_string, callback, arg):
        if regex_string not in self._compile_list:
            self._compile_list[regex_string] = {'callback': callback, 'para': arg}

    # Check incoming unsolicited data to see if it matched with device expectancy.
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

    # This method is to tie an specific command with a parameter to a call back method
    # when its value is updated. It sets how often the command will be query, if the command
    # have the update method.
    # If the command doesn't have the update feature then that command is only used for feedback
    def SubscribeStatus(self, command, qualifier, callback):
        Command = self.Commands.get(command)
        if Command:
            if command not in self.Subscription:
                self.Subscription[command] = {'method': {}}

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
        if command in self.Subscription:
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
