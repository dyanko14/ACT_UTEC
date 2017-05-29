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
A_BtnLBack    = Button(TLP1, 35)
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
## End Communication Interface Definition --------------------------------------
## Main
APageMain  = [A_BtnRoom, A_BtnVideo, A_BtnAudio, A_BtnStatus, A_BtnPwrOff]
AGroupMain = MESet(APageMain)
## Room
APageRoom  = [A_BtnROpen, A_BtnRClose]
AGroupRoom = MESet(APageRoom)
## Video
APageVideo = [A_BtnLCD1, A_BtnLCD2]
## Display L
APageLCD1  = [A_BtnLHDMI, A_BtnLShare, A_BtnLPwrOn, A_BtnLPwrOff, A_BtnLBack]
## Display L (Master Mode)
APageLCD1F = [A_BtnFLHDMI1, A_BtnFLShare1, A_BtnFLHDMI2, A_BtnFLShare2,
              A_BtnFLPwrOn, A_BtnFLPwrOff, A_BtnFLBack]
## Display R (Master Mode)
APageLCD2F = [A_BtnFRHDMI1, A_BtnFRShare1, A_BtnFRHDMI2, A_BtnFRShare2,
              A_BtnFRPwrOn, A_BtnFRPwrOff, A_BtnFRBack]
## Audio
APageAudio = [A_BtnVolLess, A_BtnVolPlus, A_BtnMute]
## Status Room A
## Status (Master Mode)
## PowerOff
ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']


def Initialize():
    pass

## Event Definitions -----------------------------------------------------------
## Data Dictionaries -----------------------------------------------------------
Room = {
    'Mode' : '', #['Abierto', 'Cerrado']
    'Last' : ''  #['Panel1', 'Panel2']
}

'''PANEL - ROOM A ...........................................................'''
## Index -----------------------------------------------------------------------
@event(A_BtnIndex, ButtonEventList)
def IndexEvents(button, state):
    TLP1.ShowPage('Main')
    pass

## Main ------------------------------------------------------------------------
@event(APageMain, ButtonEventList)
def A_MainEvents(button, state):
    #--
    if button is A_BtnRoom and state == 'Pressed':
        TLP1.ShowPopup('Room')
        A_LblMaster.SetText('Modo de Sala')
        AGroupMain.SetCurrent(A_BtnRoom)
        print('Touch %s Mode: %s' % ('A','Room'))
    #--
    elif button is A_BtnVideo and state == 'Pressed':
        if Room['Mode'] == 'Abierto':
            TLP1.ShowPopup('Video')
            A_LblMaster.SetText('Selección de Display')
            AGroupMain.SetCurrent(A_BtnVideo)
            print('Touch %s Mode: %s' % ('A','Video Master'))
            #--
        elif Room['Mode'] == 'Cerrado':
            TLP1.ShowPopup('Display_1A')
            A_LblMaster.SetText('Control de Video')
            AGroupMain.SetCurrent(A_BtnVideo)
            print('Touch %s Mode: %s' % ('A','Video'))
    #--
    elif button is A_BtnAudio and state == 'Pressed':
        if Room['Mode'] == 'Abierto':
            TLP1.ShowPopup('Audio')
            A_LblMaster.SetText('Control de Audio')
            AGroupMain.SetCurrent(A_BtnAudio)
            print('Touch %s Mode: %s' % ('A','Audio Master'))
        elif Room['Mode'] == 'Cerrado':
            TLP1.ShowPopup('Audio')
            A_LblMaster.SetText('Control de Audio')
            AGroupMain.SetCurrent(A_BtnAudio)
            print('Touch %s Mode: %s' % ('A','Audio'))
    #--
    elif button is A_BtnStatus and state == 'Pressed':
        if Room['Mode'] == 'Abierto':
            TLP1.ShowPopup('Status_1Full')
            A_LblMaster.SetText('Información de Dispositivos')
            AGroupMain.SetCurrent(A_BtnStatus)
            print('Touch %s Mode: %s' % ('A','Status Master'))
            #--
        elif Room['Mode'] == 'Cerrado':
            TLP1.ShowPopup('Status_1A')
            A_LblMaster.SetText('Información de Dispositivos')
            AGroupMain.SetCurrent(A_BtnStatus)
            print('Touch %s Mode: %s' % ('A','Status'))
    #--
    elif button is A_BtnPwrOff and state == 'Pressed':
        if Room['Mode'] == 'Abierto':
            TLP1.ShowPopup('x_PowerOff')
            A_LblMaster.SetText('¿Apagar el Sistema?')
            AGroupMain.SetCurrent(A_BtnPwrOff)
            print('Touch %s Mode: %s' % ('A','PowerOff Master'))
            #--
        if Room['Mode'] == 'Cerrado':
            TLP1.ShowPopup('x_PowerOff')
            A_LblMaster.SetText('¿Apagar el Sistema?')
            AGroupMain.SetCurrent(A_BtnPwrOff)
            print('Touch %s Mode: %s' % ('A','PowerOff Master'))
    pass
## Room ------------------------------------------------------------------------
@event(APageRoom, ButtonEventList)
def A_RoomEvents(button, state):
    #--
    if button is A_BtnROpen and state == 'Pressed':
        Room['Mode'] = 'Abierto'
        A_LblRMode.SetText('Abierto')
        A_LblRoom.SetText('Panel A: Abierto')
        A_LblRActv.SetText('Panel A')
        AGroupRoom.SetCurrent(A_BtnROpen)
        print('Touch %s Room Mode: %s' % ('A','Abierto'))
    #--
    elif button is A_BtnRClose and state == 'Pressed':
        Room['Mode'] = 'Cerrado'
        A_LblRMode.SetText('Cerrado')
        A_LblRoom.SetText('Panel A: Cerrado')
        A_LblRActv.SetText('Panel A')
        AGroupRoom.SetCurrent(A_BtnRClose)
        print('Touch %s Room Mode: %s' % ('A','Cerrado'))
    pass
## Video -----------------------------------------------------------------------
@event(APageVideo, ButtonEventList)
def A_VideoEvents(button, state):
    if button is A_BtnLCD1 and state == 'Pressed':
        TLP1.ShowPopup('Display_1Full')
        print('Touch %s Mode: %s' % ('A','Display L'))
    elif button is A_BtnLCD2 and state == 'Pressed':
        TLP1.ShowPopup('Display_2Full')
        print('Touch %s Mode: %s' % ('A','Display R'))
    pass
## Display L -------------------------------------------------------------------
@event(APageLCD1, ButtonEventList)
def A_LCD1Events(button, state):
    if button is A_BtnLHDMI and state == 'Pressed':
        print('Touch %s Mode: %s - %s %s' % ('A','Display L', 'HDMI', 'A'))
    elif button is A_BtnLShare and state == 'Pressed':
        print('Touch %s Mode: %s - %s %s' % ('A','Display L', 'ShareLink', 'A'))
    elif button is A_BtnLPwrOn and state == 'Pressed':
        print('Touch %s Mode: %s - %s' % ('A','Display L', 'PowerOn'))
    elif button is A_BtnLPwrOff and state == 'Pressed': 
        print('Touch %s Mode: %s - %s' % ('A','Display L', 'PowerOff'))
    elif button is A_BtnLBack and state == 'Pressed': 
        print('Touch %s Mode: %s - %s' % ('A','Display L', 'Back'))
    pass
## Display L (Master Mode) -----------------------------------------------------
@event(APageLCD1F, ButtonEventList)
def A_LCD1FEvents(button, state):
    if button is A_BtnFLHDMI1 and state == 'Pressed':
        print('Touch %s Mode: %s - %s %s' % ('A','Display L Master', 'HDMI', 'A'))
    elif button is A_BtnFLShare1 and state == 'Pressed':
        print('Touch %s Mode: %s - %s %s' % ('A','Display L Master', 'ShareLink', 'A'))
    elif button is A_BtnFLHDMI2 and state == 'Pressed':
        print('Touch %s Mode: %s - %s %s' % ('A','Display L Master', 'HDMI', 'B'))
    elif button is A_BtnFLShare2 and state == 'Pressed':
        print('Touch %s Mode: %s - %s %s' % ('A','Display L Master', 'ShareLink', 'B'))
    elif button is A_BtnFLPwrOn and state == 'Pressed':
        print('Touch %s Mode: %s - %s' % ('A','Display L Master', 'PowerOn'))
    elif button is A_BtnFLPwrOff and state == 'Pressed':
        print('Touch %s Mode: %s - %s' % ('A','Display L Master', 'PowerOff'))
    elif button is A_BtnFLBack and state == 'Pressed':
        print('Touch %s Mode: %s - %s' % ('A','Display L Master', 'Back'))
    pass
## Display R (Master Mode) -----------------------------------------------------
@event(APageLCD2F, ButtonEventList)
def A_LCD2Events(button, state):
    if button is A_BtnFRHDMI1 and state == 'Pressed':
        print('Touch %s Mode: %s - %s %s' % ('A','Display R Master', 'HDMI', 'A'))
    elif button is A_BtnFRShare1 and state == 'Pressed':
        print('Touch %s Mode: %s - %s %s' % ('A','Display R Master', 'ShareLink', 'A'))
    elif button is A_BtnFRHDMI2 and state == 'Pressed':
        print('Touch %s Mode: %s - %s %s' % ('A','Display R Master', 'HDMI', 'B'))
    elif button is A_BtnFRShare2 and state == 'Pressed':
        print('Touch %s Mode: %s - %s %s' % ('A','Display R Master', 'ShareLink', 'B'))
    elif button is A_BtnFRPwrOn and state == 'Pressed':
        print('Touch %s Mode: %s - %s' % ('A','Display R Master', 'PowerOn'))
    elif button is A_BtnFRPwrOff and state == 'Pressed':
        print('Touch %s Mode: %s - %s' % ('A','Display R Master', 'PowerOff'))
    elif button is A_BtnFRBack and state == 'Pressed':
        print('Touch %s Mode: %s - %s' % ('A','Display R Master', 'Back'))
    pass
## Audio -----------------------------------------------------------------------
@event(APageAudio, ButtonEventList)
def A_AudioEvents(button, state):
    if button is A_BtnVolLess and state == 'Pressed':
        if Room['Mode'] == 'Abierto':
            print('Touch %s Mode: %s - %s' % ('A','Audio Master', 'Vol -'))
        elif Room['Mode'] == 'Cerrado':
            print('Touch %s Mode: %s - %s' % ('A','Audio', 'Vol -'))
   
    elif button is A_BtnVolLess and state == 'Repeated':
        if Room['Mode'] == 'Abierto':
            print('Touch %s Mode: %s - %s' % ('A','Audio Master', 'Vol -'))
        elif Room['Mode'] == 'Cerrado':
            print('Touch %s Mode: %s - %s' % ('A','Audio', 'Vol -'))
    #--
    elif button is A_BtnVolPlus and state == 'Pressed':
        if Room['Mode'] == 'Abierto':
            print('Touch %s Mode: %s - %s' % ('A','Audio Master', 'Vol +'))
        elif Room['Mode'] == 'Cerrado':
            print('Touch %s Mode: %s - %s' % ('A','Audio', 'Vol +'))

    elif button is A_BtnVolPlus and state == 'Repeated':
        if Room['Mode'] == 'Abierto':
            print('Touch %s Mode: %s - %s' % ('A','Audio Master', 'Vol +'))
        elif Room['Mode'] == 'Cerrado':
            print('Touch %s Mode: %s - %s' % ('A','Audio', 'Vol +'))
    #--
    elif button is A_BtnMute and state == 'Pressed':
        if Room['Mode'] == 'Abierto':
            print('Touch %s Mode: %s - %s' % ('A','Audio Master', 'Mute'))
        elif Room['Mode'] == 'Cerrado':
            print('Touch %s Mode: %s - %s' % ('A','Audio', 'Mute'))
    pass
## Status ----------------------------------------------------------------------
## PowerOff --------------------------------------------------------------------
@event(A_BtnPowerAll, 'Pressed')
def A_PowerEvent(button, state):
    if Room['Mode'] == 'Abierto':
        print('Touch %s Mode: %s - %s' % ('A','Power Master', 'All'))
    if Room['Mode'] == 'Cerrado':
        print('Touch %s Mode: %s - %s' % ('A','Power', 'All'))
    pass

'''PANEL - ROOM B ...........................................................'''
## Video -----------------------------------------------------------------------
## Display L -------------------------------------------------------------------
## Display L (Master Mode) -----------------------------------------------------
## Display R (Master Mode) -----------------------------------------------------
## Audio -----------------------------------------------------------------------
## Status ----------------------------------------------------------------------
## PowerOff --------------------------------------------------------------------

## End Events Definitions-------------------------------------------------------

Initialize()

