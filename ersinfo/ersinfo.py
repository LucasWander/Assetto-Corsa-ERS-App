import datetime
import acsys  # pylint: disable=import-error
import ac  # pylint: disable=import-error
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



APP_NAME = "ERS Info"
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
l_SpeedMS = 0
b_ChangeUnit = 0
l_BatteryCapacity = 0
l_BarCharge = 0

current_energy_unit = ["kJ","mJ","Wh","kWh"]
energy_unit_counter = 0

energy_units = {
    "kJ": 1000,
    "mJ": 1000000,
    "Wh": 3600,
    "kWh": 3600000
}


def prepare_log_string(message):
    return str(datetime.datetime.now()) + " @@@@ " + APP_NAME + " @@@@ " + message


def ac_log(message):
    full_message = prepare_log_string(message)

    # Escreve no arquivo py_log.txt
    ac.log(full_message)


def ac_console(message):
    full_message = prepare_log_string(message)

    # Escreve no console do jogo
    ac.console(full_message)


def on_activation(*args):
    global enabled
    enabled = True


def on_desactivation(*args):

    global enabled
    enabled = False

def getErsCurrentJoules():
    return ac.getCarState(0, acsys.CS.ERSCurrentKJ) * 1000

def getErsCurrent():
    global energy_units, current_energy_unit, energy_unit_counter

    return getErsCurrentJoules() / energy_units[current_energy_unit[energy_unit_counter]]

def getERSMax():
     global energy_units, current_energy_unit, energy_unit_counter

     return ac.getCarState(0, acsys.CS.ERSMaxJ) / energy_units[current_energy_unit[energy_unit_counter]]

def changeEnergyUnit(*args):

    global energy_unit_counter

    if(energy_unit_counter == 3):
        energy_unit_counter = 0
    else:
        energy_unit_counter += 1

def acMain(ac_version):

    global l_lapcount, l_fuel, l_ERSRecovery, l_ERSDelivery, l_ERSHeatCharging, l_ERSCurrentKJ, l_ERSMaxJ, l_KersCharge, l_KersInput, l_SpeedMS, b_ChangeUnit, energy_unit_counter, current_energy_unit, l_BatteryCapacity, l_BarCharge


    appWindow = ac.newApp(APP_NAME)
    ac.setSize(appWindow, 600, 500)

    ac_log("Testando a função de log")
    ac_console("Testando a função de console")

    ac.addOnAppActivatedListener(appWindow, on_activation)
    ac.addOnAppDismissedListener(appWindow, on_desactivation)

    b_ChangeUnit = ac.addButton(appWindow, "Change energy unit")
    ac.setSize(b_ChangeUnit, 150, 30)
    ac.setPosition(b_ChangeUnit, 300, 30)
    ac.addOnClickedListener(b_ChangeUnit, changeEnergyUnit)


    l_SpeedMS = ac.addLabel(appWindow, "Speed: {}m/s".format(ac.getCarState(0,acsys.CS.SpeedMS)))
    ac.setPosition(l_SpeedMS, 3, 300)

    l_lapcount = ac.addLabel(appWindow, "Laps: 0")
    ac.setPosition(l_lapcount, 3, 30)

    l_fuel = ac.addLabel(appWindow, "Fuel: {}".format(info.physics.fuel))
    ac.setPosition(l_fuel, 3, 60)

    l_ERSRecovery = ac.addLabel(appWindow, "ERS Recovery: {}".format(
        ac.getCarState(0, acsys.CS.ERSRecovery)))
    ac.setPosition(l_ERSRecovery, 3, 90)

    l_ERSDelivery = ac.addLabel(appWindow, "ERS Delivery: {}".format(
        ac.getCarState(0, acsys.CS.ERSDelivery)))
    ac.setPosition(l_ERSDelivery, 3, 120)

    l_ERSHeatCharging = ac.addLabel(appWindow, "ERS Heat Charging: {}".format(
        ac.getCarState(0, acsys.CS.ERSHeatCharging)))
    ac.setPosition(l_ERSHeatCharging, 3, 150)

    l_ERSCurrentKJ = ac.addLabel(appWindow, "ERS Current: {:03.3f}{}".format(
        getErsCurrent(), current_energy_unit[energy_unit_counter]))
    ac.setPosition(l_ERSCurrentKJ, 3, 180)

    l_ERSMaxJ = ac.addLabel(appWindow, "ERS Max: {:03.3f}{}".format(
        getERSMax(), current_energy_unit[energy_unit_counter]))
    ac.setPosition(l_ERSMaxJ, 3, 210)

    l_KersCharge = ac.addLabel(appWindow, "Kers Max Charge: {}%".format(
        ac.getCarState(0, acsys.CS.KersCharge)))
    ac.setPosition(l_KersCharge, 3, 240)

    l_BatteryCapacity = ac.addLabel(appWindow, "Energy Storage capacity: {}{}".format(0,current_energy_unit[energy_unit_counter]))
    ac.setPosition(l_BatteryCapacity,3,330)

    l_KersInput = ac.addLabel(appWindow, "Kers Input: {}".format(
        ac.getCarState(0, acsys.CS.KersInput)))
    ac.setPosition(l_KersInput, 3, 270)

    l_BarCharge = ac.addLabel(appWindow, "{}%".format(
        ac.getCarState(0, acsys.CS.KersCharge)))

    ac.setPosition(l_BarCharge, 341, 130)

    ac.addRenderCallback(appWindow, onFormRender)

    return "ERS Info"

def onFormRender(deltaT):

    kersValue = ac.getCarState(0,acsys.CS.KersCharge)

    usage = getErsCurrent()/getERSMax()


    ac.glColor4f(255,255,255, 0.4)
    ac.glQuad(300,90, 40, 100)

    ac.glColor4f(0, 255, 0,0.5)
    ac.glQuad(300, 90-((100*kersValue)-100), 40, (100*kersValue))

    ac.glColor4f(255,255,255, 0.4)
    ac.glQuad(400,90, 40, 100)



    ac.glColor4f(0, 0, 255,0.5)
    ac.glQuad(400, 90-((100*usage)-100), 40, (100*usage))

def acUpdate(deltaT):

    global enabled

    if(not enabled):
        return


    global l_lapcount, lapcount, l_fuel, l_ERSRecovery, l_ERSDelivery, l_ERSHeatCharging, l_ERSCurrentKJ, l_ERSMaxJ, l_KersCharge, l_KersInput, l_SpeedMS, energy_unit_counter, current_energy_unit


    laps = ac.getCarState(0, acsys.CS.LapCount)

    fuel = info.physics.fuel
    ac.setText(l_fuel, "Laps: {}".format(fuel))

    ac.setText(l_ERSRecovery, "ERS Recovery: {}".format(
        ac.getCarState(0, acsys.CS.ERSRecovery)))

    ac.setText(l_ERSDelivery, "ERS Delivery: {}".format(
        ac.getCarState(0, acsys.CS.ERSDelivery)))

    ac.setText(l_ERSHeatCharging, "ERS Heat Charging: {}".format(
        ac.getCarState(0, acsys.CS.ERSHeatCharging)))

    ac.setText(l_ERSCurrentKJ, "ERS Current: {:03.3f}{}".format(
        getErsCurrent(), current_energy_unit[energy_unit_counter]))

    ac.setText(l_ERSMaxJ, "ERS Max: {:03.3f}{}".format(
        getERSMax(), current_energy_unit[energy_unit_counter]))

    ac.setText(l_KersCharge, "Kers Max Charge: {}%".format(
        ac.getCarState(0, acsys.CS.KersCharge)))


    ac.setText(l_BarCharge, "{:.1f}%".format(
        100*ac.getCarState(0, acsys.CS.KersCharge)))

    ac.setText(l_KersInput, "Kers Input: {}".format(
        ac.getCarState(0, acsys.CS.KersInput)))


    ac.setText(l_SpeedMS, "Speed: {}m/s".format(ac.getCarState(0,acsys.CS.SpeedMS)))

    # does not provide an accurate value, because of the assetto corsa physics
    x = (getErsCurrent() * 100)/(100 - (100*ac.getCarState(0, acsys.CS.KersCharge)))
    ac.console(str(x))


    if(x != 0):
        ac.setText(l_BatteryCapacity, "Energy Storage capacity: {}{}".format(x,current_energy_unit[energy_unit_counter]))

    if laps > lapcount:
        lapcount = laps
        ac.setText(l_lapcount, "Laps: {}".format(lapcount))


def acShutdown():
    ac_log("Session ending")
