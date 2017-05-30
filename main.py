## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface,
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface,
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait

print(Version())

## End ControlScript Import ----------------------------------------------------
##
## Begin User Import -----------------------------------------------------------

## End User Import -------------------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------
IPCP = ProcessorDevice('IPCP350')
## End Device/Processor Definition ---------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------
TLP1 = UIDevice('TouchPanelA')
TLP2 = UIDevice('TouchPanelB')
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
#--
PageLCD2F  = [A_BtnFRHDMI1, A_BtnFRShare1, A_BtnFRHDMI2, A_BtnFRShare2,
              A_BtnFRPwrOn, A_BtnFRPwrOff, A_BtnFRBack,
              B_BtnFRHDMI1, B_BtnFRShare1, B_BtnFRHDMI2, B_BtnFRShare2,
              B_BtnFRPwrOn, B_BtnFRPwrOff, B_BtnFRBack]
#--
PageAudio  = [A_BtnVolLess, A_BtnVolPlus, A_BtnMute,
              B_BtnVolLess, B_BtnVolPlus, B_BtnMute]
#--
PagePwrOff = [A_BtnPowerAll, B_BtnPowerAll]
#--
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']

## End Communication Interface Definition --------------------------------------
def Initialize():
    TLP1.ShowPage('Index')
    TLP2.ShowPage('Index')
    pass

## Event Definitions -----------------------------------------------------------
## Data Dictionaries -----------------------------------------------------------
Room = {
    'Mode' : '', #['Abierto', 'Cerrado']
    'Last' : ''  #['Panel1', 'Panel2']
}

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
    if button.Host.DeviceAlias == 'TouchPanelA':
        #--
        if button is A_BtnRoom and state == 'Pressed':
            TLP1.ShowPopup('Room')
            A_LblMaster.SetText('Modo de Sala')
            AGroupMain.SetCurrent(A_BtnRoom)
            print('Touch A: %s' % ('Room'))
        #--
        elif button is A_BtnVideo and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                TLP1.ShowPopup('Video')
                A_LblMaster.SetText('Selección de Display')
                AGroupMain.SetCurrent(A_BtnVideo)
                print('Touch A: %s' % ('Video Master'))
                #--
            elif Room['Mode'] == 'Cerrado':
                TLP1.ShowPopup('Display_1A')
                A_LblMaster.SetText('Control de Video')
                AGroupMain.SetCurrent(A_BtnVideo)
                print('Touch A: %s' % ('Video'))
        #--
        elif button is A_BtnAudio and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                TLP1.ShowPopup('Audio')
                A_LblMaster.SetText('Control de Audio')
                AGroupMain.SetCurrent(A_BtnAudio)
                A_LblAudio.SetText('Control de Audio en Sala A')
                print('Touch A: %s' % ('Audio Master'))
            elif Room['Mode'] == 'Cerrado':
                TLP1.ShowPopup('Audio')
                A_LblMaster.SetText('Control de Audio')
                AGroupMain.SetCurrent(A_BtnAudio)
                A_LblAudio.SetText('Control de Audio en todo el Auditorio')
                print('Touch A: %s' % ('Audio'))
        #--
        elif button is A_BtnStatus and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                TLP1.ShowPopup('Status_1Full')
                A_LblMaster.SetText('Información de Dispositivos')
                AGroupMain.SetCurrent(A_BtnStatus)
                print('Touch A: %s' % ('Status Master'))
                #--
            elif Room['Mode'] == 'Cerrado':
                TLP1.ShowPopup('Status_1A')
                A_LblMaster.SetText('Información de Dispositivos')
                AGroupMain.SetCurrent(A_BtnStatus)
                print('Touch A: %s' % ('Status'))
        #--
        elif button is A_BtnPwrOff and state == 'Pressed':
            A_LblPowerAll.SetText('Mantener 3s para Apagar el Sistema')
            if Room['Mode'] == 'Abierto':
                TLP1.ShowPopup('x_PowerOff')
                A_LblMaster.SetText('¿Apagar el Sistema?')
                AGroupMain.SetCurrent(A_BtnPwrOff)
                A_LblTexttAll.SetText('Esto Apagará los equipos de la Sala A')
                print('Touch A: %s' % ('PowerOff Master'))
                #--
            if Room['Mode'] == 'Cerrado':
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
            if Room['Mode'] == 'Abierto':
                TLP2.ShowPopup('Video')
                B_LblMaster.SetText('Selección de Display')
                BGroupMain.SetCurrent(B_BtnVideo)
                print('Touch B: %s' % ('Video Master'))
                #--
            elif Room['Mode'] == 'Cerrado':
                TLP2.ShowPopup('Display_1A')
                B_LblMaster.SetText('Control de Video')
                BGroupMain.SetCurrent(B_BtnVideo)
                print('Touch B: %s' % ('Video'))
        #--
        elif button is B_BtnAudio and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                TLP2.ShowPopup('Audio')
                B_LblMaster.SetText('Control de Audio')
                BGroupMain.SetCurrent(B_BtnAudio)
                B_LblAudio.SetText('Control de Audio en Sala B')
                print('Touch B: %s' % ('Audio Master'))
            elif Room['Mode'] == 'Cerrado':
                TLP2.ShowPopup('Audio')
                B_LblMaster.SetText('Control de Audio')
                BGroupMain.SetCurrent(B_BtnAudio)
                B_LblAudio.SetText('Control de Audio en el Auditorio')
                print('Touch B: %s' % ('Audio'))
        #--
        elif button is B_BtnStatus and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                TLP2.ShowPopup('Status_1Full')
                B_LblMaster.SetText('Información de Dispositivos')
                BGroupMain.SetCurrent(B_BtnStatus)
                print('Touch B: %s' % ('Status Master'))
                #--
            elif Room['Mode'] == 'Cerrado':
                TLP2.ShowPopup('Status_1A')
                B_LblMaster.SetText('Información de Dispositivos')
                BGroupMain.SetCurrent(B_BtnStatus)
                print('Touch B: %s' % ('Status'))
        #--
        elif button is B_BtnPwrOff and state == 'Pressed':
            B_LblPowerAll.SetText('Mantener 3s para Apagar el Sistema')
            if Room['Mode'] == 'Abierto':
                TLP2.ShowPopup('x_PowerOff')
                B_LblMaster.SetText('¿Apagar el Sistema?')
                BGroupMain.SetCurrent(B_BtnPwrOff)
                B_LblTexttAll.SetText('Esto Apagará los equipos de la Sala B')
                print('Touch B: %s' % ('PowerOff Master'))
                #--
            if Room['Mode'] == 'Cerrado':
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
            Room['Mode'] = 'Abierto'
            A_LblRoom.SetText('Panel A: Abierto')
            B_LblRoom.SetText('Panel B: Abierto')
            A_LblRMode.SetText('Abierto')
            B_LblRMode.SetText('Abierto')
            A_LblRActv.SetText('Panel A')
            B_LblRActv.SetText('Panel A')
            AGroupRoom.SetCurrent(A_BtnROpen)
            BGroupRoom.SetCurrent(B_BtnROpen)
            AGroupMain.SetCurrent(A_BtnRoom)
            BGroupMain.SetCurrent(B_BtnRoom)
            TLP1.ShowPopup('Room')
            TLP2.ShowPopup('Room')        
            print('Touch A: %s' % ('Room Abierto'))
        #--
        elif button is A_BtnRClose and state == 'Pressed':
            Room['Mode'] = 'Cerrado'
            A_LblRoom.SetText('Panel A: Cerrado')
            B_LblRoom.SetText('Panel B: Cerrado')
            A_LblRMode.SetText('Cerrado')
            B_LblRMode.SetText('Cerrado')
            A_LblRActv.SetText('Panel A')
            B_LblRActv.SetText('Panel A')
            AGroupRoom.SetCurrent(A_BtnRClose)
            BGroupRoom.SetCurrent(B_BtnRClose)
            AGroupMain.SetCurrent(A_BtnRoom)
            BGroupMain.SetCurrent(B_BtnRoom)
            TLP1.ShowPopup('Room')
            TLP2.ShowPopup('Room')  
            print('Touch A: %s' % ('Room Cerrado'))
    elif button.Host.DeviceAlias == 'TouchPanelB':
        #--
        if button is B_BtnROpen and state == 'Pressed':
            Room['Mode'] = 'Abierto'
            A_LblRoom.SetText('Panel A: Abierto')
            B_LblRoom.SetText('Panel B: Abierto')
            A_LblRMode.SetText('Abierto')
            B_LblRMode.SetText('Abierto')
            A_LblRActv.SetText('Panel B')
            B_LblRActv.SetText('Panel B')
            AGroupRoom.SetCurrent(A_BtnROpen)
            BGroupRoom.SetCurrent(B_BtnROpen)
            AGroupMain.SetCurrent(A_BtnRoom)
            BGroupMain.SetCurrent(B_BtnRoom)
            TLP1.ShowPopup('Room')
            TLP2.ShowPopup('Room')  
            print('Touch B: %s' % ('Room Abierto'))
        #--
        elif button is B_BtnRClose and state == 'Pressed':
            Room['Mode'] = 'Cerrado'
            A_LblRoom.SetText('Panel A: Cerrado')
            B_LblRoom.SetText('Panel B: Cerrado')
            A_LblRMode.SetText('Cerrado')
            B_LblRMode.SetText('Cerrado')
            A_LblRActv.SetText('Panel B')
            B_LblRActv.SetText('Panel B')
            AGroupRoom.SetCurrent(A_BtnRClose)
            BGroupRoom.SetCurrent(B_BtnRClose)
            AGroupMain.SetCurrent(A_BtnRoom)
            BGroupMain.SetCurrent(B_BtnRoom)
            TLP1.ShowPopup('Room')
            TLP2.ShowPopup('Room')  
            print('Touch B: %s' % ('Room Cerrado'))
    pass
## Video -----------------------------------------------------------------------
@event(PageVideo, ButtonEventList)
def VideoEvents(button, state):
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnLCD1 and state == 'Pressed':
            TLP1.ShowPopup('Display_1Full')
            print('Touch A: %s' % ('Display L'))
        elif button is A_BtnLCD2 and state == 'Pressed':
            TLP1.ShowPopup('Display_2Full')
            print('Touch A: %s' % ('Display R'))
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
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnLHDMI and state == 'Pressed':
            print('Touch A: %s' % ('Display L - HDMI A'))
        elif button is A_BtnLShare and state == 'Pressed':
            print('Touch A: %s' % ('Display L - Share A'))
        elif button is A_BtnLPwrOn and state == 'Pressed':
            print('Touch A: %s' % ('Display L - PowerOn'))
        elif button is A_BtnLPwrOff and state == 'Pressed': 
            print('Touch A: %s' % ('Display L - PowerOff'))
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnLHDMI and state == 'Pressed':
            print('Touch B: %s' % ('Display R - HDMI A'))
        elif button is B_BtnLShare and state == 'Pressed':
            print('Touch B: %s' % ('Display R - Share'))
        elif button is B_BtnLPwrOn and state == 'Pressed':
            print('Touch B: %s' % ('Display R - PowerOn'))
        elif button is B_BtnLPwrOff and state == 'Pressed':
            print('Touch B: %s' % ('Display R - PowerOff'))
    pass
## Display L (Master Mode) -----------------------------------------------------
@event(PageLCD1F, ButtonEventList)
def LCD1F_Events(button, state):
    #--
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnFLHDMI1 and state == 'Pressed':
            print('Touch A: %s' % ('Display L Master - HDMI A'))
        elif button is A_BtnFLShare1 and state == 'Pressed':
            print('Touch A: %s' % ('Display L Master - Share A'))
        elif button is A_BtnFLHDMI2 and state == 'Pressed':
            print('Touch A: %s' % ('Display L Master - HDMI B'))
        elif button is A_BtnFLShare2 and state == 'Pressed':
            print('Touch A: %s' % ('Display L Master - Share B'))
        elif button is A_BtnFLPwrOn and state == 'Pressed':
            print('Touch A: %s' % ('Display L Master - PowerOn'))
        elif button is A_BtnFLPwrOff and state == 'Pressed':
            print('Touch A: %s' % ('Display L Master - PowerOff'))
        elif button is A_BtnFLBack and state == 'Pressed':
            TLP1.ShowPopup('Video')
            print('Touch A: %s' % ('Display L Master - Back'))
    #--
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnFLHDMI1 and state == 'Pressed':
            print('Touch B: %s' % ('Display L Master - HDMI A'))
        elif button is B_BtnFLShare1 and state == 'Pressed':
            print('Touch B: %s' % ('Display L Master - Share A'))
        elif button is B_BtnFLHDMI2 and state == 'Pressed':
            print('Touch B: %s' % ('Display L Master - HDMI B'))
        elif button is B_BtnFLShare2 and state == 'Pressed':
            print('Touch B: %s' % ('Display L Master - Share B'))
        elif button is B_BtnFLPwrOn and state == 'Pressed':
            print('Touch B: %s' % ('Display L Master - PowerOn'))
        elif button is B_BtnFLPwrOff and state == 'Pressed':
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
            print('Touch A: %s' % ('Display R Master - HDMI A'))
        elif button is A_BtnFRShare1 and state == 'Pressed':
            print('Touch A: %s' % ('Display R Master - Share A'))
        elif button is A_BtnFRHDMI2 and state == 'Pressed':
            print('Touch A: %s' % ('Display R Master - HDMI B'))
        elif button is A_BtnFRShare2 and state == 'Pressed':
            print('Touch A: %s' % ('Display R Master - Share B'))
        elif button is A_BtnFRPwrOn and state == 'Pressed':
            print('Touch A: %s' % ('Display R Master - PowerOn'))
        elif button is A_BtnFRPwrOff and state == 'Pressed':
            print('Touch A: %s' % ('Display R Master - PowerOff'))
        elif button is A_BtnFRBack and state == 'Pressed':
            TLP1.ShowPopup('Video')
            print('Touch A: %s' % ('Display R Master - Back'))
    #--
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnFRHDMI1 and state == 'Pressed':
            print('Touch B: %s' % ('Display R Master - HDMI A'))
        elif button is B_BtnFRShare1 and state == 'Pressed':
            print('Touch B: %s' % ('Display R Master - Share A'))
        elif button is B_BtnFRHDMI2 and state == 'Pressed':
            print('Touch B: %s' % ('Display R Master - HDMI B'))
        elif button is B_BtnFRShare2 and state == 'Pressed':
            print('Touch B: %s' % ('Display R Master - Share B'))
        elif button is B_BtnFRPwrOn and state == 'Pressed':
            print('Touch B: %s' % ('Display R Master - PowerOn'))
        elif button is B_BtnFRPwrOff and state == 'Pressed':
            print('Touch B: %s' % ('Display R Master - PowerOff'))
        elif button is B_BtnFRBack and state == 'Pressed':
            TLP2.ShowPopup('Video')
            print('Touch B: %s' % ('Display R Master - Back'))
    pass
## Audio -----------------------------------------------------------------------
@event(PageAudio, ButtonEventList)
def AudioEvents(button, state):
    #--
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnVolLess and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                print('Touch A: %s' % ('Audio Master Vol-'))
            elif Room['Mode'] == 'Cerrado':
                print('Touch A: %s' % ('Audio Vol-'))
       
        elif button is A_BtnVolLess and state == 'Repeated':
            if Room['Mode'] == 'Abierto':
                print('Touch A: %s' % ('Audio Master Vol-'))
            elif Room['Mode'] == 'Cerrado':
                print('Touch A: %s' % ('Audio Vol-'))
        #--
        elif button is A_BtnVolPlus and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                print('Touch A: %s' % ('Audio Master Vol+'))
            elif Room['Mode'] == 'Cerrado':
                print('Touch A: %s' % ('Audio Vol+'))
    
        elif button is A_BtnVolPlus and state == 'Repeated':
            if Room['Mode'] == 'Abierto':
                print('Touch A: %s' % ('Audio Master Vol+'))
            elif Room['Mode'] == 'Cerrado':
                print('Touch A: %s' % ('Audio Vol+'))
        #--
        elif button is A_BtnMute and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                print('Touch A: %s' % ('Audio Master Mute'))
            elif Room['Mode'] == 'Cerrado':
                print('Touch A: %s' % ('Audio Mute'))
    #--
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnVolLess and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                print('Touch B: %s' % ('Audio Master Vol-'))
            elif Room['Mode'] == 'Cerrado':
                print('Touch B: %s' % ('Audio Vol-'))
       
        elif button is B_BtnVolLess and state == 'Repeated':
            if Room['Mode'] == 'Abierto':
                print('Touch B: %s' % ('Audio Master Vol-'))
            elif Room['Mode'] == 'Cerrado':
                print('Touch B: %s' % ('Audio Vol-'))
        #--
        elif button is B_BtnVolPlus and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                print('Touch B: %s' % ('Audio Master Vol+'))
            elif Room['Mode'] == 'Cerrado':
                print('Touch B: %s' % ('Audio Vol+'))
    
        elif button is B_BtnVolPlus and state == 'Repeated':
            if Room['Mode'] == 'Abierto':
                print('Touch B: %s' % ('Audio Master Vol+'))
            elif Room['Mode'] == 'Cerrado':
                print('Touch B: %s' % ('Audio Vol+'))
        #--
        elif button is B_BtnMute and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                print('Touch B: %s' % ('Audio Master Mute'))
            elif Room['Mode'] == 'Cerrado':
                print('Touch B: %s' % ('Audio Mute'))
    pass
## Status ----------------------------------------------------------------------
## PowerOff --------------------------------------------------------------------
@event(PagePwrOff, ButtonEventList)
def PowerEvents(button, state):
    if button.Host.DeviceAlias == 'TouchPanelA':
        if button is A_BtnPowerAll and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                print('Touch A: %s' % ('Power Master All'))
            if Room['Mode'] == 'Cerrado':
                print('Touch A: %s' % ('Power All'))
    elif button.Host.DeviceAlias == 'TouchPanelB':
        if button is B_BtnPowerAll and state == 'Pressed':
            if Room['Mode'] == 'Abierto':
                print('Touch B: %s' % ('Power Master All'))
            if Room['Mode'] == 'Cerrado':
                print('Touch B: %s' % ('Power All'))
    pass

## End Events Definitions-------------------------------------------------------
Initialize()
