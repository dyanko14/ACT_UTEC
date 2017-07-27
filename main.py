"""--------------------------------------------------------------------------
 Business   | Asesores y Consultores en Tecnología S.A. de C.V.
 Programmer | Dyanko Cisneros Mendoza
 Customer   | United TEChnologies (UTEC)
 Project    | Divisible Room
 Version    | 0.1 --------------------------------------------------------- """

## CONTROL SCRIPT IMPORT -------------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (ContactInterface, DigitalIOInterface, \
    EthernetClientInterface, EthernetServerInterfaceEx, FlexIOInterface, \
    IRInterface, RelayInterface, SerialInterface, SWPowerInterface, \
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Wait
import re

## PROCESOR DEFINITION ---------------------------------------------------------
IPCP = ProcessorDevice('IPCP250')

## MODULE IMPORT ---------------------------------------------------------------
## RS-232:
import extr_dsp_DMP64_v1_0_0_1 as DeviceA
import extr_matrix_DXPHD4k_Series_v1_1_1_0 as DeviceB
## IR/Serial:
import smsg_display_UNxxJ6000_UNxxJ7000_Series_v1_000A as DeviceC
import smsg_display_UNxxJ6000_UNxxJ7000_Series_v1_000B as DeviceD

## MODULE INSTANCE -------------------------------------------------------------
DMP64 = DeviceB.SerialClass(IPCP, 'COM1', Baud=38400, Model='DMP64')
MATRIX = DeviceA.SerialClass(IPCP, 'COM2', Baud=9600, Model='DXP 44 HD 4k')
#LCD1 = DeviceC.SerialClass(IPCP, 'IRS1', Baud=9600, Model='UN75J6300')
#LCD2 = DeviceD.SerialClass(IPCP, 'IRS2', Baud=9600, Model='UN75J6300')

## USER INTERFACE DEFINITION ---------------------------------------------------
TLP1 = UIDevice('Panel A')
TLP2 = UIDevice('Panel B')

'''PANEL - ROOM A ...........................................................'''
## Index
A_BtnIndex    = Button(TLP1, 1)
## Main
A_BtnRoom     = Button(TLP1, 2)
A_BtnVideo    = Button(TLP1, 3)
A_BtnAudio    = Button(TLP1, 4)
A_BtnPower    = Button(TLP1, 5)
A_BtnRoomA    = Button(TLP1, 10)
A_BtnRoomB    = Button(TLP1, 11)
A_BtnLAN1     = Button(TLP1, 12)
A_BtnLAN2     = Button(TLP1, 13)
A_LblMaster   = Label(TLP1, 14)
## Room
A_BtnROpen    = Button(TLP1, 20)
A_BtnRClose   = Button(TLP1, 21)
A_LblRMode    = Label(TLP1, 22)
A_LblRActv    = Label(TLP1, 23)
## Video
A_BtnLCD1     = Button(TLP1, 30)
A_BtnLCD2     = Button(TLP1, 31)
## Display Individual
A_BtnHDMI     = Button(TLP1, 40)
A_BtnShare    = Button(TLP1, 41)
A_BtnSignal1  = Button(TLP1, 42)
A_BtnSignal2  = Button(TLP1, 43)
A_BtnPwrOn    = Button(TLP1, 44)
A_BtnPwrOff   = Button(TLP1, 45)
## Display A
A_BtnAHDMI1    = Button(TLP1, 50)
A_BtnAShare1   = Button(TLP1, 51)
A_BtnAHDMI2    = Button(TLP1, 52)
A_BtnAShare2   = Button(TLP1, 53)
A_BtnASignal1  = Button(TLP1, 54)
A_BtnASignal2  = Button(TLP1, 55)
A_BtnASignal3  = Button(TLP1, 56)
A_BtnASignal4  = Button(TLP1, 57)
A_BtnAPwrOn    = Button(TLP1, 58)
A_BtnAPwrOff   = Button(TLP1, 59)
A_BtnABack     = Button(TLP1, 60)
## Display B
A_BtnBHDMI1    = Button(TLP1, 70)
A_BtnBShare1   = Button(TLP1, 71)
A_BtnBHDMI2    = Button(TLP1, 72)
A_BtnBShare2   = Button(TLP1, 73)
A_BtnBSignal1  = Button(TLP1, 74)
A_BtnBSignal2  = Button(TLP1, 75)
A_BtnBSignal3  = Button(TLP1, 76)
A_BtnBSignal4  = Button(TLP1, 77)
A_BtnBPwrOn    = Button(TLP1, 78)
A_BtnBPwrOff   = Button(TLP1, 79)
A_BtnBBack     = Button(TLP1, 84)
## Audio
A_BtnVolLess  = Button(TLP1, 85, repeatTime=0.1)
A_BtnVolPlus  = Button(TLP1, 86, repeatTime=0.1)
A_BtnMute     = Button(TLP1, 87)
A_LvlSpk      = Level(TLP1, 88)
## PowerOff
A_BtnPowerAll = Button(TLP1, 90, repeatTime=1)
A_LblPowerAll = Label(TLP1, 91)

'''PANEL - ROOM B ...........................................................'''
## Index
B_BtnIndex    = Button(TLP2, 1)
## Main
B_BtnRoom     = Button(TLP2, 2)
B_BtnVideo    = Button(TLP2, 3)
B_BtnAudio    = Button(TLP2, 4)
B_BtnPower    = Button(TLP2, 5)
B_BtnRoomA    = Button(TLP2, 10)
B_BtnRoomB    = Button(TLP2, 11)
B_BtnLAN1     = Button(TLP2, 12)
B_BtnLAN2     = Button(TLP2, 13)
B_LblMaster   = Label(TLP2, 14)
## Room
B_BtnROpen    = Button(TLP2, 20)
B_BtnRClose   = Button(TLP2, 21)
B_LblRMode    = Label(TLP2, 22)
B_LblRActv    = Label(TLP2, 23)
## Video
B_BtnLCD1     = Button(TLP2, 30)
B_BtnLCD2     = Button(TLP2, 31)
## Display Individual
B_BtnHDMI     = Button(TLP2, 40)
B_BtnShare    = Button(TLP2, 41)
B_BtnSignal1  = Button(TLP2, 42)
B_BtnSignal2  = Button(TLP2, 43)
B_BtnPwrOn    = Button(TLP2, 44)
B_BtnPwrOff   = Button(TLP2, 45)
## Display A
B_BtnAHDMI1    = Button(TLP2, 50)
B_BtnAShare1   = Button(TLP2, 51)
B_BtnAHDMI2    = Button(TLP2, 52)
B_BtnAShare2   = Button(TLP2, 53)
B_BtnASignal1  = Button(TLP2, 54)
B_BtnASignal2  = Button(TLP2, 55)
B_BtnASignal3  = Button(TLP2, 56)
B_BtnASignal4  = Button(TLP2, 57)
B_BtnAPwrOn    = Button(TLP2, 58)
B_BtnAPwrOff   = Button(TLP2, 59)
B_BtnABack     = Button(TLP2, 60)
## Display B
B_BtnBHDMI1    = Button(TLP2, 70)
B_BtnBShare1   = Button(TLP2, 71)
B_BtnBHDMI2    = Button(TLP2, 72)
B_BtnBShare2   = Button(TLP2, 73)
B_BtnBSignal1  = Button(TLP2, 74)
B_BtnBSignal2  = Button(TLP2, 75)
B_BtnBSignal3  = Button(TLP2, 76)
B_BtnBSignal4  = Button(TLP2, 77)
B_BtnBPwrOn    = Button(TLP2, 78)
B_BtnBPwrOff   = Button(TLP2, 79)
B_BtnBBack     = Button(TLP2, 84)
## Audio
B_BtnVolLess  = Button(TLP2, 85, repeatTime=0.1)
B_BtnVolPlus  = Button(TLP2, 86, repeatTime=0.1)
B_BtnMute     = Button(TLP2, 87)
B_LvlSpk      = Level(TLP2, 88)
## PowerOff
B_BtnPowerAll = Button(TLP2, 90, repeatTime=1)
B_LblPowerAll = Label(TLP2, 91)

'''Panel A-B Group Buttons ..................................................'''
PageIndex  = [A_BtnIndex, B_BtnIndex]
#
PageMain   = [A_BtnRoom, A_BtnVideo, A_BtnAudio, A_BtnPower,
              B_BtnRoom, B_BtnVideo, B_BtnAudio, B_BtnPower]
AGroupMain = MESet([A_BtnRoom, A_BtnVideo, A_BtnAudio, A_BtnPower])
BGroupMain = MESet([B_BtnRoom, B_BtnVideo, B_BtnAudio, B_BtnPower])
#
PageRoom   = [A_BtnROpen, A_BtnRClose, B_BtnROpen, B_BtnRClose]
AGroupRoom = MESet([A_BtnROpen, A_BtnRClose])
BGroupRoom = MESet([B_BtnROpen, B_BtnRClose])
#
PageVideo  = [A_BtnLCD1, A_BtnLCD2, B_BtnLCD1, B_BtnLCD2]
#
PageLCD    = [A_BtnHDMI, A_BtnShare, A_BtnPwrOn, A_BtnPwrOff,
              B_BtnHDMI, B_BtnShare, B_BtnPwrOn, B_BtnPwrOff]
#
PageLCD1   = [A_BtnAHDMI1, A_BtnAShare1, A_BtnAHDMI2, A_BtnAShare2, A_BtnAPwrOn, A_BtnAPwrOff, A_BtnABack,
              B_BtnAHDMI1, B_BtnAShare1, B_BtnAHDMI2, B_BtnAShare2, B_BtnAPwrOn, B_BtnAPwrOff, B_BtnABack]
#
PageLCD2   = [A_BtnBHDMI1, A_BtnBShare1, A_BtnBHDMI2, A_BtnBShare2, A_BtnBPwrOn, A_BtnBPwrOff, A_BtnBBack,
              B_BtnBHDMI1, B_BtnBShare1, B_BtnBHDMI2, B_BtnBShare2, B_BtnBPwrOn, B_BtnBPwrOff, B_BtnBBack]
#
PageAudio  = [A_BtnVolLess, A_BtnVolPlus, A_BtnMute,
              B_BtnVolLess, B_BtnVolPlus, B_BtnMute]
#
PagePower  = [A_BtnPowerAll, B_BtnPowerAll]

ButtonEventList = ['Pressed', 'Released', 'Held', 'Repeated', 'Tapped']

print('Extron Library v' + Version())

## INITIALIZATE ----------------------------------------------------------------
def Initialize():
    """This is the last function that loads when starting the system """
    ## OPEN CONNECTION SOCKETS
    ## RS-232
    MATRIX.Initialize()
    ## DATA INITIALIZE
    global Room
    global Audio
    global CounterM
    global CounterA
    global CounterB
    CounterM = None
    CounterA = None
    CounterB = None
    ## TOUCHPANEL ACTIONS
    TLP1.ShowPage('Index')
    TLP2.ShowPage('Index')
    pass

## SUBSCRIBE FUNCTIONS ---------------------------------------------------------
def subscribe_matrix():
    """This send Subscribe Commands to Device """
    #
    MATRIX.SubscribeStatus('ConnectionStatus', None, matrix_parsing)
    #
    MATRIX.SubscribeStatus('OutputTieStatus', {'Output':'1', 'Tie Type':'Video'}, matrix_parsing)
    MATRIX.SubscribeStatus('OutputTieStatus', {'Output':'2', 'Tie Type':'Video'}, matrix_parsing)
    MATRIX.SubscribeStatus('OutputTieStatus', {'Output':'3', 'Tie Type':'Video'}, matrix_parsing)
    MATRIX.SubscribeStatus('OutputTieStatus', {'Output':'4', 'Tie Type':'Video'}, matrix_parsing)
    #
    MATRIX.SubscribeStatus('OutputTieStatus', {'Output':'1', 'Tie Type':'Audio'}, matrix_parsing)
    MATRIX.SubscribeStatus('OutputTieStatus', {'Output':'2', 'Tie Type':'Audio'}, matrix_parsing)
    #
    MATRIX.SubscribeStatus('SignalStatus', {'Input' : '1'}, matrix_parsing)
    MATRIX.SubscribeStatus('SignalStatus', {'Input' : '2'}, matrix_parsing)
    MATRIX.SubscribeStatus('SignalStatus', {'Input' : '3'}, matrix_parsing)
    MATRIX.SubscribeStatus('SignalStatus', {'Input' : '4'}, matrix_parsing)
    pass

## UPDATE FUNCTIONS ------------------------------------------------------------
def update_matrix():
    """This send Update Commands to Device"""
    #
    MATRIX.Update('OutputTieStatus', {'Output':'1', 'Tie Type':'Video'})
    MATRIX.Update('OutputTieStatus', {'Output':'2', 'Tie Type':'Video'})
    MATRIX.Update('OutputTieStatus', {'Output':'3', 'Tie Type':'Video'})
    MATRIX.Update('OutputTieStatus', {'Output':'4', 'Tie Type':'Video'})
    #
    MATRIX.Update('OutputTieStatus', {'Output':'1', 'Tie Type':'Audio'})
    MATRIX.Update('OutputTieStatus', {'Output':'2', 'Tie Type':'Audio'})
    #
    MATRIX.Update('SignalStatus', {'Input' : '1'})
    MATRIX.Update('SignalStatus', {'Input' : '2'})
    MATRIX.Update('SignalStatus', {'Input' : '3'})
    MATRIX.Update('SignalStatus', {'Input' : '4'})
    pass

## DATA PARSING FUNCTIONS ------------------------------------------------------
## This receive the data of devices in real time
## This store the parsed data in dictionaries and activate feedback
## This works with the subscription methods of the Python modules
"""def matrix_parsing(command, value, qualifier):
    #Retrieve the Real Information of the Device
    if command == 'ConnectionStatus':
        print('Matrix Module Conex status: {}'.format(value))

        if value == 'Connected':
            Matrix_Data['ConexModule'] = True
            A_BtnLAN1.SetState(1)
            B_BtnLAN1.SetState(1)
        else:
            Matrix_Data['ConexModule'] = False
            A_BtnLAN1.SetState(0)
            B_BtnLAN1.SetState(0)
            ## Disconnect the IP Socket
            MATRIX.Disconnect()

    elif command == 'OutputTieStatus':
        if qualifier['Output'] == '1': ## Left Display
            if qualifier['Tie Type'] == 'Video':
                if value == '1':
                    BTNGROUP['LCD1_S'].SetCurrent(BTN['LHDMI'])
                elif value == '2':
                    BTNGROUP['LCD1_S'].SetCurrent(BTN['LVGA'])
                elif value == '3':
                    BTNGROUP['LCD1_S'].SetCurrent(BTN['LPTZ'])
                elif value == '4':
                    BTNGROUP['LCD1_S'].SetCurrent(BTN['LShare'])

        elif qualifier['Output'] == '2': ## Right Display
            if qualifier['Tie Type'] == 'Video':
                if value == '1':
                    BTNGROUP['LCD2_S'].SetCurrent(BTN['RHDMI'])
                elif value == '2':
                    BTNGROUP['LCD2_S'].SetCurrent(BTN['RVGA'])
                elif value == '3':
                    BTNGROUP['LCD2_S'].SetCurrent(BTN['RPTZ'])
                elif value == '4':
                    BTNGROUP['LCD2_S'].SetCurrent(BTN['RShare'])

        elif qualifier['Output'] == '3': ## VC Content Input
            if qualifier['Tie Type'] == 'Video':
                if value == '1':
                    BTNGROUP['VCPC_S'].SetCurrent(BTN['VCHDMI'])
                elif value == '2':
                    BTNGROUP['VCPC_S'].SetCurrent(BTN['VCVGA'])
                elif value == '3':
                    BTNGROUP['VCPC_S'].SetCurrent(BTN['VCPTZ'])
                elif value == '4':
                    BTNGROUP['VCPC_S'].SetCurrent(BTN['VCShare'])

        elif qualifier['Output'] == '4': ## Webex Input
            if qualifier['Tie Type'] == 'Video':
                if value == '1':
                    BTNGROUP['Webex'].SetCurrent(BTN['WHDMI'])
                elif value == '2':
                    BTNGROUP['Webex'].SetCurrent(BTN['WVGA'])
                elif value == '3':
                    BTNGROUP['Webex'].SetCurrent(BTN['WPTZ'])
                elif value == '4':
                    BTNGROUP['Webex'].SetCurrent(BTN['WShare'])
                elif value == '5':
                    BTNGROUP['Webex'].SetCurrent(BTN['WCisco1'])
                elif value == '6':
                    BTNGROUP['Webex'].SetCurrent(BTN['WCisco2'])

        elif qualifier['Output'] == '1': ## Audio HDMI Matrix Dembedder
            if qualifier['Tie Type'] == 'Audio':
                if value == '1':
                    BTNGROUP['Audio'].SetCurrent(BTN['XHDMI'])
                elif value == '2':
                    BTNGROUP['Audio'].SetCurrent(BTN['XVGA'])
                elif value == '4':
                    BTNGROUP['Audio'].SetCurrent(BTN['XShare'])

    elif command == 'SignalStatus':
        if qualifier['Input'] == '1':
            if value == 'Signal Detected':
                BTN['Signal1'].SetState(1)
            else:
                BTN['Signal1'].SetState(0)
        elif qualifier['Input'] == '2':
            if value == 'Signal Detected':
                BTN['Signal2'].SetState(1)
            else:
                BTN['Signal2'].SetState(0)
        elif qualifier['Input'] == '3':
            if value == 'Signal Detected':
                BTN['Signal3'].SetState(1)
            else:
                BTN['Signal3'].SetState(0)
        elif qualifier['Input'] == '4':
            if value == 'Signal Detected':
                BTN['Signal4'].SetState(1)
            else:
                BTN['Signal4'].SetState(0)
        elif qualifier['Input'] == '5':
            if value == 'Signal Detected':
                BTN['Signal5'].SetState(1)
            else:
                BTN['Signal5'].SetState(0)
        elif qualifier['Input'] == '6':
            if value == 'Signal Detected':
                BTN['Signal6'].SetState(1)
            else:
                BTN['Signal6'].SetState(0)
    pass"""

## EVENT FUNCTIONS ----------------------------------------------------------------
## This retunr 'Online' / 'Offline' status after to send a Connect()
## CAUTION: If you never make a Connect(), the Module never work with Subscriptions
@event(MATRIX, 'Online')
@event(MATRIX, 'Offline')
def matrix_conex_event(interface, state):
    """Matrix Open Port Status"""
    print('Matrix Conex Event: ' + state)
    #
    if state == 'Online':
        A_BtnLAN1.SetState(1)
        B_BtnLAN1.SetState(1)
        Matrix_Data['ConexEvent'] = True
        ## Send & Query Information
        subscribe_matrix()
        update_matrix()
    #
    else:
        A_BtnLAN1.SetState(0)
        B_BtnLAN1.SetState(0)
        Matrix_Data['ConexEvent'] = False
        trying_matrix()
    pass

## RECURSIVE FUNCTIONS ------------------------------------------------------------
## Help´s when the device was Off in the first Connect() method when the code starts
def trying_matrix():
    """Try to make a Connect() to device"""
    if Matrix_Data['ConexEvent'] == False:
        print('Tryng to make a Connect() in Matrix')
        MATRIX.Initialize() ## Have 4 seconds to try to connect
    pass
loop_trying_matrix = Wait(5, trying_matrix)

## RECURSIVE LOOP FUNCTIONS -----------------------------------------------------------
## This not affect any device
## This return True / False when no response is received from Module
## If in 5 times the data is not reported (connectionCounter = 5) from the Update Command
## Generate 'Connected' / 'Disconnected'
def update_loop_matrix():
    """Continuos Update Commands to produce Module Connected / Disconnected"""
    MATRIX.Update('SignalStatus', {'Input':'1'})
    loop_update_matrix.Restart()
loop_update_matrix = Wait(12, update_loop_matrix)

## DATA DICTIONARIES -----------------------------------------------------------
## Store real time information of devices
## TouchPanel
Room = {
    'Mixed'  : None, #['Mixed', 'Divided']
    'Last'   : None  #['Panel A', 'Panel B']
}
## RS-232
Matrix_Data = {
    'ConexModule' : None, # Module Connection
    'ConexEvent'  : None, # Physical Connection
}
Audio_Data = {
    'ConexModule' : None, # Module Connection
    'ConexEvent'  : None, # Physical Connection
    #
    'Mute_M' : None, #['On', 'Off']
    'Mute_A' : None, #['On', 'Off']
    'Mute_B' : None, #['On', 'Off']
    'Vol_M'  : None, # Gain Level
    'Vol_A'  : None, # Gain Level
    'Vol_B'  : None  # Gain Level
}

## BUTTON EVENTS ---------------------------------------------------------------
## Index -----------------------------------------------------------------------
@event(PageIndex, ButtonEventList)
def index_events(button, state):
    """Page Index Actions"""
    if state == 'Pressed':
        if Room['Mixed']:
            for item in [TLP1, TLP2]:
                item.ShowPage('Main')
                item.ShowPopup('x_Welcome')
        else:
            if button.Host.DeviceAlias == 'Panel A':
                TLP1.ShowPage('Main')
                TLP1.ShowPopup('x_Welcome')
            elif button.Host.DeviceAlias == 'Panel B':
                TLP2.ShowPage('Main')
                TLP2.ShowPopup('x_Welcome')
        # Notify to Console
        print(button.Host.DeviceAlias + ': Index Pressed')
    pass

## Main ------------------------------------------------------------------------
@event(PageMain, ButtonEventList)
def main_events(button, state):
    """Page Main Actions"""
    if state == 'Pressed':
        ## User Actions
        if button.ID == 2: # Room Mode
            # Notify to Console
            print(button.Host.DeviceAlias + ': Room Pressed')
            #
            if button.Host.DeviceAlias == 'Panel A':
                TLP1.ShowPopup('Room')
                A_LblMaster.SetText('Modo de Sala')
            #
            elif button.Host.DeviceAlias == 'Panel B':
                TLP2.ShowPopup('Room')
                B_LblMaster.SetText('Modo de Sala')
            #
            if Room['Mixed'] == True:
                AGroupMain.SetCurrent(A_BtnRoom)
                BGroupMain.SetCurrent(B_BtnRoom)
            else:
                if button.Host.DeviceAlias == 'Panel A':
                    AGroupMain.SetCurrent(A_BtnRoom)
                else:
                    BGroupMain.SetCurrent(B_BtnRoom)

        elif button.ID == 3: # Video Mode
            # Notify to Console
            print(button.Host.DeviceAlias + ': Video Pressed')
            #
            if Room['Mixed'] == True:
                TLP1.ShowPopup('Video')
                TLP2.ShowPopup('Video')
            else:
                if button.Host.DeviceAlias == 'Panel A':
                    TLP1.ShowPopup('Display')
                elif button.Host.DeviceAlias == 'Panel B':
                    TLP2.ShowPopup('Display')
            #
            if Room['Mixed'] == True:
                AGroupMain.SetCurrent(A_BtnVideo)
                BGroupMain.SetCurrent(B_BtnVideo)
            else:
                if button.Host.DeviceAlias == 'Panel A':
                    AGroupMain.SetCurrent(A_BtnVideo)
                else:
                    BGroupMain.SetCurrent(B_BtnVideo)

        elif button.ID == 4: # Audio Mode
            # Notify to Console
            print(button.Host.DeviceAlias + ': Info Pressed')
            #
            if Room['Mixed'] == True:
                TLP1.ShowPopup('Audio')
                TLP2.ShowPopup('Audio')
            else:
                if button.Host.DeviceAlias == 'Panel A':
                    TLP1.ShowPopup('Audio')
                elif button.Host.DeviceAlias == 'Panel B':
                    TLP2.ShowPopup('Audio')
            #
            if Room['Mixed'] == True:
                AGroupMain.SetCurrent(A_BtnAudio)
                BGroupMain.SetCurrent(B_BtnAudio)
            else:
                if button.Host.DeviceAlias == 'Panel A':
                    AGroupMain.SetCurrent(A_BtnAudio)
                else:
                    BGroupMain.SetCurrent(B_BtnAudio)

        elif button.ID == 5: # PowerOff Mode
            # Notify to Console
            print(button.Host.DeviceAlias + ': Info Pressed')
            #
            if Room['Mixed'] == True:
                TLP1.ShowPopup('x_PowerOff')
                TLP2.ShowPopup('x_PowerOff')
            else:
                if button.Host.DeviceAlias == 'Panel A':
                    TLP1.ShowPopup('x_PowerOff')
                elif button.Host.DeviceAlias == 'Panel B':
                    TLP2.ShowPopup('x_PowerOff')
            #
            if Room['Mixed'] == True:
                AGroupMain.SetCurrent(A_BtnPower)
                BGroupMain.SetCurrent(B_BtnPower)
            else:
                if button.Host.DeviceAlias == 'Panel A':
                    AGroupMain.SetCurrent(A_BtnPower)
                else:
                    BGroupMain.SetCurrent(B_BtnPower)
    pass

## Room ------------------------------------------------------------------------
@event(PageRoom, ButtonEventList)
def room_events(button, state):
    """Page Room Actions"""
    if state == 'Pressed':
        ## User Actions
        if button.ID == 20: #Mixed Room
            Room['Mixed'] = True
            print(button.Host.DeviceAlias + ': Mixed Mode Pressed')
            ## Feedback Buttons
            for item in [A_BtnRoomA, A_BtnRoomB, B_BtnRoomA, B_BtnRoomB]:
                item.SetState(1)
            for item in [A_LblRMode, B_LblRMode]:
                item.SetText("Mixed");
            ## TouchPanel Actions
            for item in [TLP1, TLP2]:
                item.ShowPage('Main')
                item.ShowPopup('Room')
            ## Mutually Exclusive
            AGroupRoom.SetCurrent(A_BtnROpen)
            BGroupRoom.SetCurrent(B_BtnROpen)
            AGroupMain.SetCurrent(A_BtnRoom)
            BGroupMain.SetCurrent(B_BtnRoom)
        
        elif button.ID == 21: #Divided Room
            Room['Mixed'] = False
            print(button.Host.DeviceAlias + ': Divided Mode Pressed')
            ## Feedback Buttons
            for item in [A_BtnRoomA, B_BtnRoomB]:
                item.SetState(1)
            for item in [A_BtnRoomB, B_BtnRoomA]:
                item.SetState(0)
            for item in [A_LblRMode, B_LblRMode]:
                item.SetText("Divided");
            ## Mutually Exclusive
            AGroupRoom.SetCurrent(A_BtnRClose)
            BGroupRoom.SetCurrent(B_BtnRClose)
    pass

## Video -----------------------------------------------------------------------
@event(PageVideo, ButtonEventList)
def video_events(button, state):
    """Page Video Actions"""
    if state == 'Pressed':
        ## User Actions
        if button.ID == 30: # LCD-A
            # Notify to Console
            print(button.Host.DeviceAlias + ': Display A Pressed')
            #
            if Room['Mixed'] == True:
                for item in [TLP1, TLP2]:
                    item.ShowPopup('DisplayA')
                for item in [A_LblMaster, B_LblMaster]:
                    item.SetText('Control de Pantalla A')

        elif button.ID == 31: # LCD-B
            # Notify to Console
            print(button.Host.DeviceAlias + ': Display A Pressed')
            #
            if Room['Mixed'] == True:
                for item in [TLP1, TLP2]:
                    item.ShowPopup('DisplayB')
                for item in [A_LblMaster, B_LblMaster]:
                    item.SetText('Control de Pantalla B')
    pass

## Display Divided -------------------------------------------------------------
@event(PageLCD, ButtonEventList)
def display_divided_events(button, state):
    """Page Display Actions"""
    if state == 'Pressed':
        ## User Actions
        if button.ID == 40: # HDMI
            # Notify to Console
            print(button.Host.DeviceAlias + ': HDMI Pressed')
            #
            if button.Host.DeviceAlias == 'Panel A':
                MATRIX.Set('MatrixTieCommand', None, {'Input':'1', 'Output':'1', 'Tie Type':'Audio/Video'})
                print("Matrix HDMI A to Display A")
            else:
                MATRIX.Set('MatrixTieCommand', None, {'Input':'3', 'Output':'2', 'Tie Type':'Audio/Video'})
                print("Matrix HDMI B to Display B")

        elif button.ID == 41: # WePresent
            # Notify to Console
            print(button.Host.DeviceAlias + ': WePresent Pressed')
            #
            if button.Host.DeviceAlias == 'Panel A':
                MATRIX.Set('MatrixTieCommand', None, {'Input':'2', 'Output':'1', 'Tie Type':'Audio/Video'})
                print("Matrix WePresent A to Display A")
            else:
                MATRIX.Set('MatrixTieCommand', None, {'Input':'4', 'Output':'2', 'Tie Type':'Audio/Video'})
                print("Matrix WePresent B to Display B")

        elif button.ID == 44: # PowerOn
            # Notify to Console
            print(button.Host.DeviceAlias + ': PowerOn Pressed')
            #
            if button.Host.DeviceAlias == 'Panel A':
                print("PowerOn Display A")
            else:
                print("PowerOn Display B")

        elif button.ID == 45: # PowerOff
            # Notify to Console
            print(button.Host.DeviceAlias + ': PowerOff Pressed')
            #
            if button.Host.DeviceAlias == 'Panel A':
                print("PowerOff Display A")
            else:
                print("PowerOff Display B")
    pass

## Display Full A --------------------------------------------------------------
@event(PageLCD1, ButtonEventList)
def display_full_a_events(button, state):
    """Page Display Full A Actions"""
    if state == 'Pressed':
        ## User Actions
        if button.ID == 50: # HDMI 1
            # Notify to Console
            print(button.Host.DeviceAlias + ': HDMI Pressed')
            MATRIX.Set('MatrixTieCommand', None, {'Input':'1', 'Output':'1', 'Tie Type':'Video'})
            print('Matrix HDMI 1 to Display A')

        elif button.ID == 51: # WePresent 1
            # Notify to Console
            print(button.Host.DeviceAlias + ': WePresent Pressed')
            MATRIX.Set('MatrixTieCommand', None, {'Input':'2', 'Output':'1', 'Tie Type':'Video'})
            print('Matrix WePresent 1 to Display A')

        elif button.ID == 52: # HDMI 2
            # Notify to Console
            print(button.Host.DeviceAlias + ': HDMI Pressed')
            MATRIX.Set('MatrixTieCommand', None, {'Input':'3', 'Output':'1', 'Tie Type':'Video'})
            print('Matrix HDMI 2 to Display A')

        elif button.ID == 53: # WePresent 2
            # Notify to Console
            print(button.Host.DeviceAlias + ': WePresent Pressed')
            MATRIX.Set('MatrixTieCommand', None, {'Input':'4', 'Output':'1', 'Tie Type':'Video'})
            print('Matrix WePresent 2 to Display A')

        elif button.ID == 58: # PowerOn
            # Notify to Console
            print(button.Host.DeviceAlias + ': PowerOn Pressed')
            #
            print('PowerOn Display A')

        elif button.ID == 59: # PowerOff
            # Notify to Console
            print(button.Host.DeviceAlias + ': PowerOff Pressed')
            #
            print('PowerOff Display A')

        elif button.ID == 60: # Back
            # Notify to Console
            print(button.Host.DeviceAlias + ': Back Pressed')
            #
            print('Back Display A')
            for item in [TLP1, TLP2]:
                item.ShowPopup('Video');
    pass

## Display Full B --------------------------------------------------------------
@event(PageLCD2, ButtonEventList)
def display_full_b_events(button, state):
    """Page Display Full B Actions"""
    if state == 'Pressed':
        ## User Actions
        if button.ID == 70: # HDMI 1
            # Notify to Console
            print(button.Host.DeviceAlias + ': HDMI Pressed')
            MATRIX.Set('MatrixTieCommand', None, {'Input':'1', 'Output':'2', 'Tie Type':'Video'})
            print('Matrix HDMI 1 to Display B')

        elif button.ID == 71: # WePresent 1
            # Notify to Console
            print(button.Host.DeviceAlias + ': WePresent Pressed')
            MATRIX.Set('MatrixTieCommand', None, {'Input':'2', 'Output':'2', 'Tie Type':'Video'})
            print('Matrix WePresent 1 to Display B')

        elif button.ID == 72: # HDMI 2
            # Notify to Console
            print(button.Host.DeviceAlias + ': HDMI Pressed')
            MATRIX.Set('MatrixTieCommand', None, {'Input':'3', 'Output':'2', 'Tie Type':'Video'})
            print('Matrix HDMI 2 to Display B')

        elif button.ID == 73: # WePresent 2
            # Notify to Console
            print(button.Host.DeviceAlias + ': WePresent Pressed')
            MATRIX.Set('MatrixTieCommand', None, {'Input':'4', 'Output':'2', 'Tie Type':'Video'})
            print('Matrix WePresent 2 to Display B')

        elif button.ID == 78: # PowerOn
            # Notify to Console
            print(button.Host.DeviceAlias + ': PowerOn Pressed')
            #
            print('PowerOn Display B')

        elif button.ID == 79: # PowerOff
            # Notify to Console
            print(button.Host.DeviceAlias + ': PowerOff Pressed')
            #
            print('PowerOff Display B')

        elif button.ID == 84: # Back
            # Notify to Console
            print(button.Host.DeviceAlias + ': Back Pressed')
            #
            print('Back Display B')
            for item in [TLP1, TLP2]:
                item.ShowPopup('Video');
    pass

## Display Full A --------------------------------------------------------------
@event(PageAudio, ButtonEventList)
def audio_events(button, state):
    """Page Audio Actions"""
    if state == 'Pressed' or state == 'Repeated':
        ## User Actions
        if button.ID == 85: # Vol -
            if Room['Mixed'] == True:
                print(button.Host.DeviceAlias + ': Master Vol- Pressed')
            else:
                if button.Host.DeviceAlias == 'Panel A':
                    print(button.Host.DeviceAlias + ': Room A Vol- Pressed')
                else:
                    print(button.Host.DeviceAlias + ': Room B Vol- Pressed')

        elif button.ID == 86: # Vol +
            if Room['Mixed'] == True:
                print(button.Host.DeviceAlias + ': Master Vol+ Pressed')
            else:
                if button.Host.DeviceAlias == 'Panel A':
                    print(button.Host.DeviceAlias + ': Room A Vol+ Pressed')
                else:
                    print(button.Host.DeviceAlias + ': Room B Vol+ Pressed')

        elif button.ID == 87: # Mute
            if Room['Mixed'] == True:
                print(button.Host.DeviceAlias + ': Master Mute Pressed')
            else:
                if button.Host.DeviceAlias == 'Panel A':
                    print(button.Host.DeviceAlias + ': Room A Mute Pressed')
                else:
                    print(button.Host.DeviceAlias + ': Room B Mute Pressed')
    pass

## PowerOff --------------------------------------------------------------
@event(PagePower, ButtonEventList)
def audio_events(button, state):
    """Page PowerOff Actions"""
    global CounterM, CounterA, CounterB
    if state == 'Pressed':
        if Room['Mixed'] == True:
            CounterM = 3
            for item in PagePower:
                item.SetState(CounterM)
            for item in [A_LblPowerAll, B_LblPowerAll]:
                item.SetText('3')
                print(button.Host.DeviceAlias + ': Master PowerOff Pressed')
        else:
            if button.Host.DeviceAlias == 'Panel A':   
                CounterA = 3
                A_BtnPowerAll.SetState(CounterA)
                A_LblPowerAll.SetText('3')
                print(button.Host.DeviceAlias + ': Room A PowerOff Pressed')
            else:
                CounterB = 3
                B_BtnPowerAll.SetState(CounterB)
                B_LblPowerAll.SetText('3')
                print(button.Host.DeviceAlias + ': Room B PowerOff Pressed')

    elif state == 'Released':
        if Room['Mixed'] == True:
            CounterM = 0
            for item in PagePower:
                item.SetState(0)
            for item in [A_LblPowerAll, B_LblPowerAll]:
                item.SetText('')
                print(button.Host.DeviceAlias + ': Master PowerOff Released')
        else:
            if button.Host.DeviceAlias == 'Panel A':
                CounterA = 0
                A_BtnPowerAll.SetState(0)
                A_LblPowerAll.SetText('')
                print(button.Host.DeviceAlias + ': Room A PowerOff Released')
            else:
                CounterB = 0
                B_BtnPowerAll.SetState(0)
                B_LblPowerAll.SetText('')
                print(button.Host.DeviceAlias + ': Room B PowerOff Released')

    elif state == 'Repeated':
        if Room['Mixed'] == True:
            CounterM -= 1
            for item in PagePower:
                item.SetState(CounterM)
            for item in [A_LblPowerAll, B_LblPowerAll]:
                item.SetText(str(CounterM))
                print(button.Host.DeviceAlias + ': Master PowerOff Repeated')
                #
                if CounterM == 0:
                    for item in [TLP1, TLP2]:
                        item.ShowPage('Index')
                    print("Apagado Global OK")
        else:
            if button.Host.DeviceAlias == 'Panel A':
                CounterA -= 1
                A_BtnPowerAll.SetState(CounterA)
                A_LblPowerAll.SetText(str(CounterA))
                print(button.Host.DeviceAlias + ': Room A PowerOff Repeated')
                #
                if CounterA == 0:
                    TLP1.ShowPage('Index')
                    print("Apagado Room A OK")
            else:
                CounterB -= 1
                B_BtnPowerAll.SetState(CounterB)
                B_LblPowerAll.SetText(str(CounterB))
                print(button.Host.DeviceAlias + ': Room B PowerOff Repeated')
                #
                if CounterB == 0:
                    TLP2.ShowPage('Index')
                    print("Apagado Room B OK")
    pass

## End Events Definitions-------------------------------------------------------
Initialize()
