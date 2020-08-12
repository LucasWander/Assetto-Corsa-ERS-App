import sys
import os
import platform

if platform.architecture()[0] == "64bit":
	sysdir = os.path.dirname(__file__)+'/stdlib64'
else:
	sysdir = os.path.dirname(__file__)+'/stdlib'

sys.path.insert(0, sysdir)
os.environ['PATH'] = os.environ['PATH'] + ";."

from lib.sim_info import info

import ac
import acsys
import datetime

APP_NAME = "Hybrid Info"
l_lapcount = 0
l_fuel = 0
lapcount = 0
enabled = True


l_ERSRecovery = 0
l_ERSDelivery = 0
l_ERSHeatCharging = 0
l_ERSCurrentKJ = 0
l_ERSMaxJ = 0
l_KersCharge = 0
l_KersInput = 0



def prepare_log_string(message):
    return  str(datetime.datetime.now()) + " @@@@ " + APP_NAME + " @@@@ " + message

def ac_log(message):
    full_message = prepare_log_string(message)

    #Escreve no arquivo py_log.txt
    ac.log(full_message)

def ac_console(message):
    full_message = prepare_log_string(message)

    #Escreve no console do jogo
    ac.console(full_message)

ac_console(str(a))
ac_log(str(sys.path))


def on_activation():
    global enabled
    ac_console("Ativando app")
    ac_log("ATIVANDO app")

    enabled = True

def on_desactivation():

    global enabled
    ac_console("Desativando app")
    ac_log("Desativando app")

    enabled = False

def acMain(ac_version):

    global l_lapcount, l_fuel, l_ERSRecovery, l_ERSDelivery, l_ERSHeatCharging, l_ERSCurrentKJ, l_ERSMaxJ, l_KersCharge, l_KersInput

    appWindow = ac.newApp("hybridinfo")
    ac.setSize(appWindow, 300,300)

    ac_log("Testando a função de log")
    ac_console("Testando a função de console")

    l_lapcount = ac.addLabel(appWindow, "Laps: 0")
    ac.setPosition(l_lapcount, 3, 30)

    l_fuel = ac.addLabel(appWindow, "Fuel: {}".format(info.physics.fuel))
    ac.setPosition(l_fuel, 3, 60)

    l_ERSRecovery = ac.addLabel(appWindow, "ERS Recovery: {}".format(ac.getCarState(0, acsys.CS.ERSRecovery)))
    ac.setPosition(l_ERSRecovery, 3, 90)


    l_ERSDelivery = ac.addLabel(appWindow, "ERS Delivery: {}".format(ac.getCarState(0,acsys.CS.ERSDelivery)))
    ac.setPosition(l_ERSDelivery, 3, 120)

    l_ERSHeatCharging = ac.addLabel(appWindow, "ERS Heat Charging: {}".format(ac.getCarState(0, acsys.CS.ERSHeatCharging)))
    ac.setPosition(l_ERSHeatCharging, 3, 150)

    l_ERSCurrentKJ = ac.addLabel(appWindow, "ERS Current KJ: {}".format(ac.getCarState(0, acsys.CS.ERSCurrentKJ)))
    ac.setPosition(l_ERSCurrentKJ, 3, 180)

    l_ERSMaxJ = ac.addLabel(appWindow, "ERS Max J: {}".format(ac.getCarState(0, acsys.CS.ERSMaxJ)))
    ac.setPosition(l_ERSMaxJ, 3, 210)

    l_KersCharge = ac.addLabel(appWindow, "Kers Max Charge: {}".format(ac.getCarState(0, acsys.CS.KersCharge)))
    ac.setPosition(l_KersCharge, 3, 240)

    l_KersInput = ac.addLabel(appWindow, "Kers Input: {}".format(ac.getCarState(0, acsys.CS.KersInput)))
    ac.setPosition(l_KersInput, 3, 270)


    return "hybridinfo"


def acUpdate(deltaT):

    global enabled

    if(not enabled):
        return

    #ac_console("Updading")

    global l_lapcount, lapcount, l_fuel, l_ERSRecovery, l_ERSDelivery, l_ERSHeatCharging, l_ERSCurrentKJ, l_ERSMaxJ, l_KersCharge, l_KersInput

    laps = ac.getCarState(0, acsys.CS.LapCount)

    fuel = info.physics.fuel
    ac.setText(l_fuel, "Laps: {}".format(fuel))

    ac.setText(l_ERSRecovery, "ERS Recovery: {}".format(ac.getCarState(0, acsys.CS.ERSRecovery)))

    ac.setText(l_ERSDelivery, "ERS Delivery: {}".format(ac.getCarState(0,acsys.CS.ERSDelivery)))

    ac.setText(l_ERSHeatCharging, "ERS Heat Charging: {}".format(ac.getCarState(0, acsys.CS.ERSHeatCharging)))

    ac.setText(l_ERSCurrentKJ, "ERS Current KJ: {}".format(ac.getCarState(0, acsys.CS.ERSCurrentKJ)))

    ac.setText(l_ERSMaxJ, "ERS Max J: {}".format(ac.getCarState(0, acsys.CS.ERSMaxJ)))

    ac.setText(l_KersCharge, "Kers Max Charge: {}".format(ac.getCarState(0, acsys.CS.KersCharge)))

    ac.setText(l_KersInput, "Kers Input: {}".format(ac.getCarState(0, acsys.CS.KersInput)))

    if laps > lapcount:
        lapcount = laps
        ac.setText(l_lapcount, "Laps: {}".format(lapcount))


def acShutdown():
    ac_log("Session ending")
