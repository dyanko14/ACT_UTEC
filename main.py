## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface,
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface,
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait
import re

print(Version())

## End ControlScript Import ----------------------------------------------------
##
## Begin User Import -----------------------------------------------------------

## End User Import -------------------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------
IPCP   = ProcessorDevice('IPCP350')
## End Device/Processor Definition ---------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------
TLP1   = UIDevice('TouchPanelA')
TLP2   = UIDevice('TouchPanelB')
#--
Matrix = SerialInterface(IPCP, 'COM1', Baud=9600)
DMP64  = SerialInterface(IPCP, 'COM2', Baud=9600)
#--
#LCD1   = SerialInterface(IPCP, 'IRS2', Baud=9600)
#LCD2   = SerialInterface(IPCP, 'IRS3', Baud=9600)
## End Device/User Interface Definition ----------------------------------------
##
## Begin Communication Interface Definition ------------------------------------
'''PANEL - ROOM A ...........................................................'''
## Index
A_BtnIndex    = Button(TLP1, 1)
## Main
A_BtnRoom     = Button(TLP1, 2)
A_BtnVideo    = Button(TLP1, 3)
A_BtnAudio    = Button(TLP1, 4)
A_BtnStatus   = Button(TLP1, 5)
A_BtnPwrOff   = Button(TLP1, 6)
A_LblMaster   = Label(TLP1, 300)
A_LblRoom     = Label(TLP1, 301)
## Room
A_BtnROpen    = Button(TLP1, 11)
A_BtnRClose   = Button(TLP1, 12)
A_LblRMode    = Label(TLP1, 13)
A_LblRActv    = Label(TLP1, 14)
## Video (Master Mode)
A_BtnLCD1     = Button(TLP1, 21)
A_BtnLCD2     = Button(TLP1, 22)
## Display L
A_BtnLHDMI    = Button(TLP1, 31)
A_BtnLShare   = Button(TLP1, 32)
A_BtnLPwrOn   = Button(TLP1, 33)
A_BtnLPwrOff  = Button(TLP1, 34)
## Display L (Master Mode)
A_BtnFLHDMI1  = Button(TLP1, 41)
A_BtnFLShare1 = Button(TLP1, 42)
A_BtnFLHDMI2  = Button(TLP1, 43)
A_BtnFLShare2 = Button(TLP1, 44)
A_BtnFLPwrOn  = Button(TLP1, 45)
A_BtnFLPwrOff = Button(TLP1, 46)
A_BtnFLBack   = Button(TLP1, 47)
## Display R (Master Mode)
A_BtnFRHDMI1  = Button(TLP1, 51)
A_BtnFRShare1 = Button(TLP1, 52)
A_BtnFRHDMI2  = Button(TLP1, 53)
A_BtnFRShare2 = Button(TLP1, 54)
A_BtnFRPwrOn  = Button(TLP1, 55)
A_BtnFRPwrOff = Button(TLP1, 56)
A_BtnFRBack   = Button(TLP1, 57)
## Audio
A_BtnVolLess  = Button(TLP1, 61, repeatTime = 0.1)
A_BtnVolPlus  = Button(TLP1, 62, repeatTime = 0.1)
A_BtnMute     = Button(TLP1, 63)
A_LvlRoom     = Level(TLP1, 64)
A_LblAudio    = Label(TLP1, 65)
## Status Room A
A_Btn232LCD1  = Button(TLP1, 71)
A_BtnLANHDMI  = Button(TLP1, 72)
A_BtnLANDMP64 = Button(TLP1, 73)
## Status (Master Mode)
A_Btn232LCD1  = Button(TLP1, 81)
A_Btn232LCD2  = Button(TLP1, 82)
A_BtnLANHDMI  = Button(TLP1, 83)
A_BtnLANDMP64 = Button(TLP1, 84)
## PowerOff
A_BtnPowerAll = Button(TLP1, 90)
A_LblPowerAll = Label(TLP1, 91)
A_LblTexttAll = Label(TLP2, 92)

'''PANEL - ROOM B ...........................................................'''
## Index
B_BtnIndex    = Button(TLP2, 1)
## Main
B_BtnRoom     = Button(TLP2, 2)
B_BtnVideo    = Button(TLP2, 3)
B_BtnAudio    = Button(TLP2, 4)
B_BtnStatus   = Button(TLP2, 5)
B_BtnPwrOff   = Button(TLP2, 6)
B_LblMaster   = Label(TLP2, 300)
B_LblRoom     = Label(TLP2, 301)
## Room
B_BtnROpen    = Button(TLP2, 11)
B_BtnRClose   = Button(TLP2, 12)
B_LblRMode    = Label(TLP2, 13)
B_LblRActv    = Label(TLP2, 14)
## Video (Master Mode)
B_BtnLCD1     = Button(TLP2, 21)
B_BtnLCD2     = Button(TLP2, 22)
## Display L
B_BtnLHDMI    = Button(TLP2, 31)
B_BtnLShare   = Button(TLP2, 32)
B_BtnLPwrOn   = Button(TLP2, 33)
B_BtnLPwrOff  = Button(TLP2, 34)
## Display L (Master Mode)
B_BtnFLHDMI1  = Button(TLP2, 41)
B_BtnFLShare1 = Button(TLP2, 42)
B_BtnFLHDMI2  = Button(TLP2, 43)
B_BtnFLShare2 = Button(TLP2, 44)
B_BtnFLPwrOn  = Button(TLP2, 45)
B_BtnFLPwrOff = Button(TLP2, 46)
B_BtnFLBack   = Button(TLP2, 47)
## Display R (Master Mode)
B_BtnFRHDMI1  = Button(TLP2, 51)
B_BtnFRShare1 = Button(TLP2, 52)
B_BtnFRHDMI2  = Button(TLP2, 53)
B_BtnFRShare2 = Button(TLP2, 54)
B_BtnFRPwrOn  = Button(TLP2, 55)
B_BtnFRPwrOff = Button(TLP2, 56)
B_BtnFRBack   = Button(TLP2, 57)
## Audio
B_BtnVolLess  = Button(TLP2, 61, repeatTime = 0.1)
B_BtnVolPlus  = Button(TLP2, 62, repeatTime = 0.1)
B_BtnMute     = Button(TLP2, 63)
B_LvlRoom     = Level(TLP2, 64)
B_LblAudio    = Label(TLP1, 65)
## Status Room A
B_Btn232LCD1  = Button(TLP2, 71)
B_BtnLANHDMI  = Button(TLP2, 72)
B_BtnLANDMP64 = Button(TLP2, 73)
## Status (Master Mode)
B_Btn232LCD1  = Button(TLP2, 81)
B_Btn232LCD2  = Button(TLP2, 82)
B_BtnLANHDMI  = Button(TLP2, 83)
B_BtnLANDMP64 = Button(TLP2, 84)
## PowerOff
B_BtnPowerAll = Button(TLP2, 90)
B_LblPowerAll = Label(TLP2, 91)
B_LblTexttAll = Label(TLP2, 92)

'''Panel A-B Group Buttons ..................................................'''
PageIndex  = [A_BtnIndex, B_BtnIndex]
#--
PageMain   = [B_BtnRoom, B_BtnVideo, B_BtnAudio, B_BtnStatus, B_BtnPwrOff,
             A_BtnRoom, A_BtnVideo, A_BtnAudio, A_BtnStatus, A_BtnPwrOff]
AGroupMain = MESet([A_BtnRoom, A_BtnVideo, A_BtnAudio, A_BtnStatus, A_BtnPwrOff])
BGroupMain = MESet([B_BtnRoom, B_BtnVideo, B_BtnAudio, B_BtnStatus, B_BtnPwrOff])
#--
PageRoom   = [A_BtnROpen, A_BtnRClose, B_BtnROpen, B_BtnRClose]
AGroupRoom = MESet([A_BtnROpen, A_BtnRClose])
BGroupRoom = MESet([B_BtnROpen, B_BtnRClose])
#--
PageVideo  = [A_BtnLCD1, A_BtnLCD2, B_BtnLCD1, B_BtnLCD2]
#--
PageLCD    = [A_BtnLHDMI, A_BtnLShare, A_BtnLPwrOn, A_BtnLPwrOff,
              B_BtnLHDMI, B_BtnLShare, B_BtnLPwrOn, B_BtnLPwrOff]
#--
PageLCD1F  = [A_BtnFLHDMI1, A_BtnFLShare1, A_BtnFLHDMI2, A_BtnFLShare2,
              A_BtnFLPwrOn, A_BtnFLPwrOff, A_BtnFLBack,
              B_BtnFLHDMI1, B_BtnFLShare1, B_BtnFLHDMI2, B_BtnFLShare2,
              B_BtnFLPwrOn, B_BtnFLPwrOff, B_BtnFLBack]
GroupLCD1  = MESet([A_BtnFLHDMI1, A_BtnFLShare1])
GroupLCD1F = MESet([A_BtnFLHDMI1, A_BtnFLShare1, A_BtnFLHDMI2, A_BtnFLShare2])
#--
PageLCD2F  = [A_BtnFRHDMI1, A_BtnFRShare1, A_BtnFRHDMI2, A_BtnFRShare2,
              A_BtnFRPwrOn, A_BtnFRPwrOff, A_BtnFRBack,
              B_BtnFRHDMI1, B_BtnFRShare1, B_BtnFRHDMI2, B_BtnFRShare2,
              B_BtnFRPwrOn, B_BtnFRPwrOff, B_BtnFRBack]
GroupLCD2  = MESet([B_BtnFRHDMI1, B_BtnFRShare1])
GroupLCD2F = MESet([B_BtnFRHDMI1, B_BtnFRShare1, B_BtnFRHDMI2, B_BtnFRShare2])
#--
PageAudio  = [A_BtnVolLess, A_BtnVolPlus, A_BtnMute,
              B_BtnVolLess, B_BtnVolPlus, B_BtnMute]
#--
PagePwrOff = [A_BtnPowerAll, B_BtnPowerAll]
#--
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']

## End Communication Interface Definition --------------------------------------
def Initialize():
    global Room
    global Audio
    TLP1.ShowPage('Index')
    TLP2.ShowPage('Index')
    #Test
    
    pass

## Event Definitions -----------------------------------------------------------
## Data Dictionaries -----------------------------------------------------------
Room = {
    'Mode'   : '', #['Mixed', 'Separado']
    'Last'   : ''  #['PanelA', 'PanelB']
}
Audio = {
    'Mute_A' : '', #['On', 'Off']
    'Mute_B' : '', #['On', 'Off']
    'Mute_M' : '', #['On', 'Off']
    'Vol_A'  : '',
    'Vol_B'  : '',
    'Vol_M'  : ''
}
## Data Parsing ----------------------------------------------------------------
ResponsePattern = re.compile('Out([0-9]{1,3}) In([0-9]{1,3}) (All|Vid|RGB|Aud)')
ResponseString = ''
@event(Matrix, 'ReceiveData')
def MatrixReceiveDataEvent(interface, rcvString):
    global ResponseString
    print(rcvString)
    rcvString = rcvString.decode()
    ResponseString = ResponseString + rcvString
    print(ResponseString)
    MatchObject = ResponsePattern.search(ResponseString)
    if '\r\n' in ResponseString:
        print('CR\LF Found')
        if MatchObject:
            Output = int(MatchObject.group(1))
            Input = int(MatchObject.group(2))
            SwitchMode = MatchObject.group(3)
            print('Input: {0}, Output: {1}, Type: {2}'.format(Input, Output, SwitchMode))
            SetStatus(Input, Output, SwitchMode)
            ResponseString = ''
        else:
            print('No Match Found')
    else:
        print(ResponseString, 'is not a complete response')
#--
def SetStatus(input, output, mode):
    print('SetStatus called')
    #The button list begin with 0 index
    if output == 1 and mode == 'Vid':
        GroupLCD1.SetCurrent(input-1)  #Display L
        GroupLCD1F.SetCurrent(input-1) #Display L - Master
    elif output == 2 and mode == 'Vid':
        GroupLCD2.SetCurrent(input-1)  #Display R
        GroupLCD2F.SetCurrent(input-1) #Display R - Master
#--
@event(DMP64, 'ReceiveData')
def DMP64ReceiveDataEvent(interface, rcvstring):
    print(rcvstring)
    pass

'''PANEL - ROOM A ...........................................................'''
## Index -----------------------------------------------------------------------
@event(PageIndex, ButtonEventList)
def IndexEvents(button, state):
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnIndex and state == 'Pressed':
            print("Touch A: Index Pressed")
            TLP1.ShowPage('Main')
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnIndex and state == 'Pressed':
            print("Touch B: Index Pressed")
            TLP2.ShowPage('Main')
    pass

## Main ------------------------------------------------------------------------
@event(PageMain, ButtonEventList)
def MainEvents(button, state):
    #--
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnRoom and state == 'Pressed':
            TLP1.ShowPopup('Room')
            A_LblMaster.SetText('Modo de Sala')
            AGroupMain.SetCurrent(A_BtnRoom)
            print('Touch A: %s' % ('Room'))
        #--
        elif button is A_BtnVideo and state == 'Pressed':
            if Room['Mode'] == 'Mixed':
                TLP1.ShowPopup('Video')
                A_LblMaster.SetText('Selección de Display')
                AGroupMain.SetCurrent(A_BtnVideo)
                print('Touch A: %s' % ('Video Master'))
                #--
            elif Room['Mode'] == 'Separado':
                TLP1.ShowPopup('Display_1A')
                A_LblMaster.SetText('Control de Video')
                AGroupMain.SetCurrent(A_BtnVideo)
                print('Touch A: %s' % ('Video'))
        #--
        elif button is A_BtnAudio and state == 'Pressed':
            if Room['Mode'] == 'Mixed':
                TLP1.ShowPopup('Audio')
                A_LblMaster.SetText('Control de Audio')
                AGroupMain.SetCurrent(A_BtnAudio)
                A_LblAudio.SetText('Control de Audio en Sala A')
                print('Touch A: %s' % ('Audio Master'))
            elif Room['Mode'] == 'Separado':
                TLP1.ShowPopup('Audio')
                A_LblMaster.SetText('Control de Audio')
                AGroupMain.SetCurrent(A_BtnAudio)
                A_LblAudio.SetText('Control de Audio en todo el Auditorio')
                print('Touch A: %s' % ('Audio'))
        #--
        elif button is A_BtnStatus and state == 'Pressed':
            if Room['Mode'] == 'Mixed':
                TLP1.ShowPopup('Status_1Full')
                A_LblMaster.SetText('Información de Dispositivos')
                AGroupMain.SetCurrent(A_BtnStatus)
                print('Touch A: %s' % ('Status Master'))
                #--
            elif Room['Mode'] == 'Separado':
                TLP1.ShowPopup('Status_1A')
                A_LblMaster.SetText('Información de Dispositivos')
                AGroupMain.SetCurrent(A_BtnStatus)
                print('Touch A: %s' % ('Status'))
        #--
        elif button is A_BtnPwrOff and state == 'Pressed':
            A_LblPowerAll.SetText('Mantener 3s para Apagar el Sistema')
            if Room['Mode'] == 'Mixed':
                TLP1.ShowPopup('x_PowerOff')
                A_LblMaster.SetText('¿Apagar el Sistema?')
                AGroupMain.SetCurrent(A_BtnPwrOff)
                A_LblTexttAll.SetText('Esto Apagará los equipos de la Sala A')
                print('Touch A: %s' % ('PowerOff Master'))
                #--
            if Room['Mode'] == 'Separado':
                TLP1.ShowPopup('x_PowerOff')
                A_LblMaster.SetText('¿Apagar el Sistema?')
                AGroupMain.SetCurrent(A_BtnPwrOff)
                A_LblTexttAll.SetText('Esto Apagará los equipos del Auditorio')
                print('Touch A: %s' % ('PowerOff'))
    #--
    elif button.Host.DeviceAlias == 'TouchPanelB':
        #--
        if button is B_BtnRoom and state == 'Pressed':
            TLP2.ShowPopup('Room')
            B_LblMaster.SetText('Modo de Sala')
            BGroupMain.SetCurrent(B_BtnRoom)
            print('Touch B: %s' % ('Room'))
        #--
        elif button is B_BtnVideo and state == 'Pressed':
            if Room['Mode'] == 'Mixed':
                TLP2.ShowPopup('Video')
                B_LblMaster.SetText('Selección de Display')
                BGroupMain.SetCurrent(B_BtnVideo)
                print('Touch B: %s' % ('Video Master'))
                #--
            elif Room['Mode'] == 'Separado':
                TLP2.ShowPopup('Display_1A')
                B_LblMaster.SetText('Control de Video')
                BGroupMain.SetCurrent(B_BtnVideo)
                print('Touch B: %s' % ('Video'))
        #--
        elif button is B_BtnAudio and state == 'Pressed':
            if Room['Mode'] == 'Mixed':
                TLP2.ShowPopup('Audio')
                B_LblMaster.SetText('Control de Audio')
                BGroupMain.SetCurrent(B_BtnAudio)
                B_LblAudio.SetText('Control de Audio en Sala B')
                print('Touch B: %s' % ('Audio Master'))
            elif Room['Mode'] == 'Separado':
                TLP2.ShowPopup('Audio')
                B_LblMaster.SetText('Control de Audio')
                BGroupMain.SetCurrent(B_BtnAudio)
                B_LblAudio.SetText('Control de Audio en el Auditorio')
                print('Touch B: %s' % ('Audio'))
        #--
        elif button is B_BtnStatus and state == 'Pressed':
            if Room['Mode'] == 'Mixed':
                TLP2.ShowPopup('Status_1Full')
                B_LblMaster.SetText('Información de Dispositivos')
                BGroupMain.SetCurrent(B_BtnStatus)
                print('Touch B: %s' % ('Status Master'))
                #--
            elif Room['Mode'] == 'Separado':
                TLP2.ShowPopup('Status_1A')
                B_LblMaster.SetText('Información de Dispositivos')
                BGroupMain.SetCurrent(B_BtnStatus)
                print('Touch B: %s' % ('Status'))
        #--
        elif button is B_BtnPwrOff and state == 'Pressed':
            B_LblPowerAll.SetText('Mantener 3s para Apagar el Sistema')
            if Room['Mode'] == 'Mixed':
                TLP2.ShowPopup('x_PowerOff')
                B_LblMaster.SetText('¿Apagar el Sistema?')
                BGroupMain.SetCurrent(B_BtnPwrOff)
                B_LblTexttAll.SetText('Esto Apagará los equipos de la Sala B')
                print('Touch B: %s' % ('PowerOff Master'))
                #--
            if Room['Mode'] == 'Separado':
                TLP2.ShowPopup('x_PowerOff')
                B_LblMaster.SetText('¿Apagar el Sistema?')
                BGroupMain.SetCurrent(B_BtnPwrOff)
                B_LblTexttAll.SetText('Esto Apagará los equipos del Auditorio')
                print('Touch B: %s' % ('PowerOff'))
    pass
## Room ------------------------------------------------------------------------
@event(PageRoom, ButtonEventList)
def RoomEvents(button, state):
    #--
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnROpen and state == 'Pressed':
            Room['Mode'] = 'Mixed'
            Room['Last'] = 'PanelA'
            #Label Feedback - Both Panels
            A_LblRoom.SetText('Panel A: Mixed')
            B_LblRoom.SetText('Panel B: Mixed')
            A_LblRMode.SetText(Room['Mode'])
            B_LblRMode.SetText(Room['Mode'])
            A_LblRActv.SetText(Room['Last'])
            B_LblRActv.SetText(Room['Last'])
            #Button Feedback - Both Panels
            AGroupRoom.SetCurrent(A_BtnROpen)
            BGroupRoom.SetCurrent(B_BtnROpen)
            AGroupMain.SetCurrent(A_BtnRoom)
            BGroupMain.SetCurrent(B_BtnRoom)
            #AV Actions
            DMP64.Send('2.') #Recall Preset
            #View the same Popup - Both Panels
            TLP1.ShowPopup('Room')
            TLP2.ShowPopup('Room')
            #Console Feedback
            print('Touch A: %s' % ('Room Mixed'))
        #--
        elif button is A_BtnRClose and state == 'Pressed':
            Room['Mode'] = 'Separado'
            Room['Last'] = 'PanelA'
            #Label Feedback - Both Panels
            A_LblRoom.SetText('Panel A: Separado')
            B_LblRoom.SetText('Panel B: Separado')
            A_LblRMode.SetText(Room['Mode'])
            B_LblRMode.SetText(Room['Mode'])
            A_LblRActv.SetText(Room['Last'])
            B_LblRActv.SetText(Room['Last'])
            #Button Feedback - Both Panels
            AGroupRoom.SetCurrent(A_BtnRClose)
            BGroupRoom.SetCurrent(B_BtnRClose)
            AGroupMain.SetCurrent(A_BtnRoom)
            BGroupMain.SetCurrent(B_BtnRoom)
            #AV Actions
            DMP64.Send('1.') #Recall Preset
            #View the same Popup - Both Panels
            TLP1.ShowPopup('Room')
            TLP2.ShowPopup('Room')
            #Console Feedback
            print('Touch A: %s' % ('Room Separado'))
    #--
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnROpen and state == 'Pressed':
            Room['Mode'] = 'Mixed'
            Room['Last'] = 'PanelB'
            #Label Feedback - Both Panels
            A_LblRoom.SetText('Panel A: Mixed')
            B_LblRoom.SetText('Panel B: Mixed')
            A_LblRMode.SetText(Room['Mode'])
            B_LblRMode.SetText(Room['Mode'])
            A_LblRActv.SetText(Room['Last'])
            B_LblRActv.SetText(Room['Last'])
            #Button Feedback - Both Panels
            AGroupRoom.SetCurrent(A_BtnROpen)
            BGroupRoom.SetCurrent(B_BtnROpen)
            AGroupMain.SetCurrent(A_BtnRoom)
            BGroupMain.SetCurrent(B_BtnRoom)
            #AV Actions
            DMP64.Send('2.') #Recall Preset
            #View the same Popup - Both Panels
            TLP1.ShowPopup('Room')
            TLP2.ShowPopup('Room')
            #Console Feedback
            print('Touch B: %s' % ('Room Mixed'))
        #--
        elif button is B_BtnRClose and state == 'Pressed':
            Room['Mode'] = 'Separado'
            Room['Last'] = 'PanelB'
            #Label Feedback - Both Panels
            A_LblRoom.SetText('Panel A: Separado')
            B_LblRoom.SetText('Panel B: Separado')
            A_LblRMode.SetText(Room['Mode'])
            B_LblRMode.SetText(Room['Mode'])
            A_LblRActv.SetText(Room['Last'])
            B_LblRActv.SetText(Room['Last'])
            #Button Feedback - Both Panels
            AGroupRoom.SetCurrent(A_BtnRClose)
            BGroupRoom.SetCurrent(B_BtnRClose)
            AGroupMain.SetCurrent(A_BtnRoom)
            BGroupMain.SetCurrent(B_BtnRoom)
            #AV Actions
            DMP64.Send('1.') #Recall Preset
            #View the same Popup - Both Panels
            TLP1.ShowPopup('Room')
            TLP2.ShowPopup('Room')
            #Console Feedback
            print('Touch B: %s' % ('Room Separado'))
    pass
## Video -----------------------------------------------------------------------
@event(PageVideo, ButtonEventList)
def VideoEvents(button, state):
    #--
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnLCD1 and state == 'Pressed':
            TLP1.ShowPopup('Display_1Full')
            print('Touch A: %s' % ('Display L'))
        elif button is A_BtnLCD2 and state == 'Pressed':
            TLP1.ShowPopup('Display_2Full')
            print('Touch A: %s' % ('Display R'))
    #--
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnLCD1 and state == 'Pressed':
            TLP2.ShowPopup('Display_1Full')
            print('Touch B: %s' % ('Display L'))
        elif button is B_BtnLCD2 and state == 'Pressed':
            TLP2.ShowPopup('Display_2Full')
            print('Touch B: %s' % ('Display R'))
    pass
## Display L-R -----------------------------------------------------------------
@event(PageLCD, ButtonEventList)
def LCDEvents(button, state):
    #--
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnLHDMI and state == 'Pressed':
            Matrix.Send('1*1%') #Video
            Matrix.Send('2*1$') #Audio De-embedded
            print('Touch A: %s' % ('Display L - HDMI A'))
        elif button is A_BtnLShare and state == 'Pressed':
            Matrix.Send('2*1%') #Video
            Matrix.Send('2*1$') #Audio De-embedded
            print('Touch A: %s' % ('Display L - Share A'))
        elif button is A_BtnLPwrOn and state == 'Pressed':
            #LCD1.Send(b'\x08\x22\x00\x00\x00\x02\xD4')
            print('Touch A: %s' % ('Display L - PowerOn'))
        elif button is A_BtnLPwrOff and state == 'Pressed':
            #LCD1.Send(b'\x08\x22\x00\x00\x00\x01\xD5')
            print('Touch A: %s' % ('Display L - PowerOff'))
    #--
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnLHDMI and state == 'Pressed':
            Matrix.Send('3*2%') #Video
            Matrix.Send('3*2$') #Audio De-embedded
            print('Touch B: %s' % ('Display R - HDMI A'))
        elif button is B_BtnLShare and state == 'Pressed':
            Matrix.Send('4*2%') #Video
            Matrix.Send('4*2$') #Audio De-embedded
            print('Touch B: %s' % ('Display R - Share'))
        elif button is B_BtnLPwrOn and state == 'Pressed':
            #LCD2.Send(b'\x08\x22\x00\x00\x00\x02\xD4')
            print('Touch B: %s' % ('Display R - PowerOn'))
        elif button is B_BtnLPwrOff and state == 'Pressed':
            #LCD2.Send(b'\x08\x22\x00\x00\x00\x01\xD5')
            print('Touch B: %s' % ('Display R - PowerOff'))
    pass
## Display L (Master Mode) -----------------------------------------------------
@event(PageLCD1F, ButtonEventList)
def LCD1F_Events(button, state):
    #--
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnFLHDMI1 and state == 'Pressed':
            Matrix.Send('1*1%') #Video
            print('Touch A: %s' % ('Display L Master - HDMI A'))
        elif button is A_BtnFLShare1 and state == 'Pressed':
            Matrix.Send('2*1%') #Video
            print('Touch A: %s' % ('Display L Master - Share A'))
        elif button is A_BtnFLHDMI2 and state == 'Pressed':
            Matrix.Send('3*1%') #Video
            print('Touch A: %s' % ('Display L Master - HDMI B'))
        elif button is A_BtnFLShare2 and state == 'Pressed':
            Matrix.Send('4*1%') #Video
            print('Touch A: %s' % ('Display L Master - Share B'))
        elif button is A_BtnFLPwrOn and state == 'Pressed':
            #LCD1.Send(b'\x08\x22\x00\x00\x00\x02\xD4')
            print('Touch A: %s' % ('Display L Master - PowerOn'))
        elif button is A_BtnFLPwrOff and state == 'Pressed':
            #LCD1.Send(b'\x08\x22\x00\x00\x00\x01\xD5')
            print('Touch A: %s' % ('Display L Master - PowerOff'))
        elif button is A_BtnFLBack and state == 'Pressed':
            TLP1.ShowPopup('Video')
            print('Touch A: %s' % ('Display L Master - Back'))
    #--
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnFLHDMI1 and state == 'Pressed':
            Matrix.Send('1*1%') #Video
            print('Touch B: %s' % ('Display L Master - HDMI A'))
        elif button is B_BtnFLShare1 and state == 'Pressed':
            Matrix.Send('2*1%') #Video
            print('Touch B: %s' % ('Display L Master - Share A'))
        elif button is B_BtnFLHDMI2 and state == 'Pressed':
            Matrix.Send('3*1%') #Video
            print('Touch B: %s' % ('Display L Master - HDMI B'))
        elif button is B_BtnFLShare2 and state == 'Pressed':
            Matrix.Send('4*1%') #Video
            print('Touch B: %s' % ('Display L Master - Share B'))
        elif button is B_BtnFLPwrOn and state == 'Pressed':
            #LCD1.Send(b'\x08\x22\x00\x00\x00\x02\xD4')
            print('Touch B: %s' % ('Display L Master - PowerOn'))
        elif button is B_BtnFLPwrOff and state == 'Pressed':
            #LCD1.Send(b'\x08\x22\x00\x00\x00\x01\xD5')
            print('Touch B: %s' % ('Display L Master - PowerOff'))
        elif button is B_BtnFLBack and state == 'Pressed':
            TLP2.ShowPopup('Video')
            print('Touch B: %s' % ('Display L Master - Back'))
    pass
## Display R (Master Mode) -----------------------------------------------------
@event(PageLCD2F, ButtonEventList)
def A_LCD2Events(button, state):
    #--
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnFRHDMI1 and state == 'Pressed':
            Matrix.Send('1*2%') #Video
            print('Touch A: %s' % ('Display R Master - HDMI A'))
        elif button is A_BtnFRShare1 and state == 'Pressed':
            Matrix.Send('2*2%') #Video
            print('Touch A: %s' % ('Display R Master - Share A'))
        elif button is A_BtnFRHDMI2 and state == 'Pressed':
            Matrix.Send('3*2%') #Video
            print('Touch A: %s' % ('Display R Master - HDMI B'))
        elif button is A_BtnFRShare2 and state == 'Pressed':
            Matrix.Send('4*2%') #Video
            print('Touch A: %s' % ('Display R Master - Share B'))
        elif button is A_BtnFRPwrOn and state == 'Pressed':
            #LCD2.Send(b'\x08\x22\x00\x00\x00\x02\xD4')
            print('Touch A: %s' % ('Display R Master - PowerOn'))
        elif button is A_BtnFRPwrOff and state == 'Pressed':
            #LCD2.Send(b'\x08\x22\x00\x00\x00\x01\xD5')
            print('Touch A: %s' % ('Display R Master - PowerOff'))
        elif button is A_BtnFRBack and state == 'Pressed':
            TLP1.ShowPopup('Video')
            print('Touch A: %s' % ('Display R Master - Back'))
    #--
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnFRHDMI1 and state == 'Pressed':
            Matrix.Send('1*2%') #Video
            print('Touch B: %s' % ('Display R Master - HDMI A'))
        elif button is B_BtnFRShare1 and state == 'Pressed':
            Matrix.Send('2*2%') #Video
            print('Touch B: %s' % ('Display R Master - Share A'))
        elif button is B_BtnFRHDMI2 and state == 'Pressed':
            Matrix.Send('3*2%') #Video
            print('Touch B: %s' % ('Display R Master - HDMI B'))
        elif button is B_BtnFRShare2 and state == 'Pressed':
            Matrix.Send('4*2%') #Video
            print('Touch B: %s' % ('Display R Master - Share B'))
        elif button is B_BtnFRPwrOn and state == 'Pressed':
            #LCD2.Send(b'\x08\x22\x00\x00\x00\x02\xD4')
            print('Touch B: %s' % ('Display R Master - PowerOn'))
        elif button is B_BtnFRPwrOff and state == 'Pressed':
            #LCD2.Send(b'\x08\x22\x00\x00\x00\x01\xD5')
            print('Touch B: %s' % ('Display R Master - PowerOff'))
        elif button is B_BtnFRBack and state == 'Pressed':
            TLP2.ShowPopup('Video')
            print('Touch B: %s' % ('Display R Master - Back'))
    pass
## Audio -----------------------------------------------------------------------
@event(PageAudio, ButtonEventList) #Programar Feedback de Mute DMP64
def AudioEvents(button, state):
    #--
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnVolLess and state == 'Pressed':
            if Room['Mode'] == 'Mixed':
                print('Touch A: %s' % ('Audio Master Vol-'))
            elif Room['Mode'] == 'Separado':
                print('Touch A: %s' % ('Audio Vol-'))
       
        elif button is A_BtnVolLess and state == 'Repeated':
            if Room['Mode'] == 'Mixed':
                print('Touch A: %s' % ('Audio Master Vol-'))
            elif Room['Mode'] == 'Separado':
                print('Touch A: %s' % ('Audio Vol-'))
        #--
        elif button is A_BtnVolPlus and state == 'Pressed':
            if Room['Mode'] == 'Mixed':
                print('Touch A: %s' % ('Audio Master Vol+'))
            elif Room['Mode'] == 'Separado':
                print('Touch A: %s' % ('Audio Vol+'))
    
        elif button is A_BtnVolPlus and state == 'Repeated':
            if Room['Mode'] == 'Mixed':
                print('Touch A: %s' % ('Audio Master Vol+'))
            elif Room['Mode'] == 'Separado':
                print('Touch A: %s' % ('Audio Vol+'))
        #--
        elif button is A_BtnMute and state == 'Pressed':
            print('Touch A: %s' % ('Audio Mute Pressed'))
            if Room['Mode'] == 'Mixed':
                #--
                if Audio['Mute_M'] == 'On':
                    DMP64.Send('WD3*0GRPM\r') #Group Mute 3 Off
                    print('Touch A: %s' % ('Audio Master Mute Off'))
                    #--
                elif Audio['Mute_M'] == 'Off':
                    DMP64.Send('WD3*1GRPM') #Group Mute 3 On
                    print('Touch A: %s' % ('Audio Master Mute On'))
                #--
            elif Room['Mode'] == 'Separado':
                #--
                if Audio['Mute_A'] == 'On':
                    DMP64.Send('WD1*0GRPM\r') #Group Mute 1 Off
                    print('Touch A: %s' % ('Audio Mute Off'))
                    #--
                elif Audio['Mute_A'] == 'Off':
                    DMP64.Send('WD1*1GRPM\r') #Group Mute 1 On
                    print('Touch A: %s' % ('Audio Mute On'))
    #--
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnVolLess and state == 'Pressed':
            if Room['Mode'] == 'Mixed':
                print('Touch B: %s' % ('Audio Master Vol-'))
            elif Room['Mode'] == 'Separado':
                print('Touch B: %s' % ('Audio Vol-'))
       
        elif button is B_BtnVolLess and state == 'Repeated':
            if Room['Mode'] == 'Mixed':
                print('Touch B: %s' % ('Audio Master Vol-'))
            elif Room['Mode'] == 'Separado':
                print('Touch B: %s' % ('Audio Vol-'))
        #--
        elif button is B_BtnVolPlus and state == 'Pressed':
            if Room['Mode'] == 'Mixed':
                print('Touch B: %s' % ('Audio Master Vol+'))
            elif Room['Mode'] == 'Separado':
                print('Touch B: %s' % ('Audio Vol+'))
    
        elif button is B_BtnVolPlus and state == 'Repeated':
            if Room['Mode'] == 'Mixed':
                print('Touch B: %s' % ('Audio Master Vol+'))
            elif Room['Mode'] == 'Separado':
                print('Touch B: %s' % ('Audio Vol+'))
        #--
        elif button is B_BtnMute and state == 'Pressed':
            print('Touch B: %s' % ('Audio Mute Pressed'))
            if Room['Mode'] == 'Mixed':
                #--
                if Audio['Mute_M'] == 'On':
                    DMP64.Send('WD3*0GRPM\r') #Group Mute 3 Off 
                    print('Touch B: %s' % ('Audio Master Mute Off'))
                    #--
                elif Audio['Mute_M'] == 'Off':
                    DMP64.Send('WD3*1GRPM') #Group Mute 3 On
                    print('Touch B: %s' % ('Audio Master Mute On'))
                #--
            elif Room['Mode'] == 'Separado':
                #--
                if Audio['Mute_B'] == 'On':
                    DMP64.Send('WD2*0GRPM\r') #Group Mute 2 Off
                    print('Touch B: %s' % ('Audio Mute Off'))
                    #--
                elif Audio['Mute_B'] == 'Off':
                    DMP64.Send('WD2*1GRPM\r') #Group Mute 2 On
                    print('Touch B: %s' % ('Audio Mute On'))
    pass
## Status ----------------------------------------------------------------------
## PowerOff --------------------------------------------------------------------
@event(PagePwrOff, ButtonEventList)
def PowerEvents(button, state):
    #--
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnPowerAll and state == 'Pressed':
            if Room['Mode'] == 'Mixed':
                print('Touch A: %s' % ('Power Master All'))
            if Room['Mode'] == 'Separado':
                print('Touch A: %s' % ('Power All'))
    #--
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnPowerAll and state == 'Pressed':
            if Room['Mode'] == 'Mixed':
                print('Touch B: %s' % ('Power Master All'))
            if Room['Mode'] == 'Separado':
                print('Touch B: %s' % ('Power All'))
    pass

## End Events Definitions-------------------------------------------------------
Initialize()
