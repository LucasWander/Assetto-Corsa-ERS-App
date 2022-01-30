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
is_enabled = True


label_ERSRecovery = 0
label_ERSDelivery = 0
label_ERSHeatCharging = 0
label_ERSCurrentKJ = 0
label_ERSMaxJ = 0
label_KersCharge = 0
label_KersInput = 0
label_SpeedMS = 0
button_ChangeUnit = 0
label_BarCharge = 0

current_energy_unit = ["kJ","mJ","Wh","kWh"]
energy_unit_counter = 0

energy_units = {
    "kJ": 1000,
    "mJ": 1000000,
    "Wh": 3600,
    "kWh": 3600000
}


def is_app_disabled():
    global is_enabled
    return not is_enabled



def update_label_ers_recovery():
    global label_ERSRecovery
    ac.setText(label_ERSRecovery, "MGU-K recovery mode: {}".format(ac.getCarState(0, acsys.CS.ERSRecovery)))

def update_label_ers_delivery():
    global label_ERSDelivery
    ac.setText(label_ERSDelivery, "MGU-K deploy mode: {}".format(ac.getCarState(0, acsys.CS.ERSDelivery)))

def update_label_ers_heat_charging():
    global label_ERSHeatCharging
    ac.setText(label_ERSHeatCharging, "MGU-H mode: {}".format(ac.getCarState(0, acsys.CS.ERSHeatCharging)))

def update_label_ers_current_kj():
    global label_ERSCurrentKJ, energy_unit_counter, current_energy_unit
    ac.setText(label_ERSCurrentKJ, "Energy consumed in this lap: {:03.3f}{}".format(getErsCurrent(), current_energy_unit[energy_unit_counter]))

def update_label_ers_max_j():
    global label_ERSMaxJ, energy_unit_counter, current_energy_unit
    ac.setText(label_ERSMaxJ, "Maximum energy allowed per lap: {:03.3f}{}".format(getERSMax(), current_energy_unit[energy_unit_counter]))

def update_label_kers_charge():
    global label_KersCharge
    ac.setText(label_KersCharge, "Stored energy: {:.2f}%".format(ac.getCarState(0, acsys.CS.KersCharge)*100))

def update_label_bar_charge():
    global label_BarCharge
    ac.setText(label_BarCharge, "{:.1f}%".format(100*ac.getCarState(0, acsys.CS.KersCharge)))

def update_label_kers_input():
    global label_KersInput
    ac.setText(label_KersInput, "MGU-K power level: {:.2f}".format(ac.getCarState(0, acsys.CS.KersInput)*100))

def update_label_speed_ms():
    global label_SpeedMS
    ac.setText(label_SpeedMS, "Speed: {:.1f}m/s".format(ac.getCarState(0,acsys.CS.SpeedMS)))

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
    global is_enabled
    is_enabled = True


def on_desactivation(*args):

    global is_enabled
    is_enabled = False

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

    global label_lapcount, label_ERSRecovery, label_ERSDelivery, label_ERSHeatCharging, label_ERSCurrentKJ, label_ERSMaxJ, label_KersCharge, label_KersInput, label_SpeedMS, button_ChangeUnit, energy_unit_counter, current_energy_unit, label_BarCharge


    appWindow = ac.newApp(APP_NAME)
    ac.setSize(appWindow, 600, 500)

    ac_log("Testando a função de log")
    ac_console("Testando a função de console")

    ac.addOnAppActivatedListener(appWindow, on_activation)
    ac.addOnAppDismissedListener(appWindow, on_desactivation)

    button_ChangeUnit = ac.addButton(appWindow, "Change energy unit")
    ac.setSize(button_ChangeUnit, 150, 30)
    ac.setPosition(button_ChangeUnit, 300, 30)
    ac.addOnClickedListener(button_ChangeUnit, changeEnergyUnit)


    label_SpeedMS = ac.addLabel(appWindow, "Speed: {:.1f}m/s".format(ac.getCarState(0,acsys.CS.SpeedMS)))
    ac.setPosition(label_SpeedMS, 3, 300)

    label_ERSRecovery = ac.addLabel(appWindow, "MGU-K recovery mode: {}".format(
        ac.getCarState(0, acsys.CS.ERSRecovery)))
    ac.setPosition(label_ERSRecovery, 3, 90)

    label_ERSDelivery = ac.addLabel(appWindow, "MGU-K deploy mode: {}".format(
        ac.getCarState(0, acsys.CS.ERSDelivery)))
    ac.setPosition(label_ERSDelivery, 3, 120)

    label_ERSHeatCharging = ac.addLabel(appWindow, "MGU-H mode: {}".format(
        ac.getCarState(0, acsys.CS.ERSHeatCharging)))
    ac.setPosition(label_ERSHeatCharging, 3, 150)

    label_ERSCurrentKJ = ac.addLabel(appWindow, "Energy consumed in this lap: {:03.3f}{}".format(
        getErsCurrent(), current_energy_unit[energy_unit_counter]))
    ac.setPosition(label_ERSCurrentKJ, 3, 180)

    label_ERSMaxJ = ac.addLabel(appWindow, "Maximum energy allowed per lap: {:03.3f}{}".format(
        getERSMax(), current_energy_unit[energy_unit_counter]))
    ac.setPosition(label_ERSMaxJ, 3, 210)

    label_KersCharge = ac.addLabel(appWindow, "Stored energy: {:.2f}%".format(
        ac.getCarState(0, acsys.CS.KersCharge)*100))
    ac.setPosition(label_KersCharge, 3, 240)



    label_KersInput = ac.addLabel(appWindow, "MGU-K power level: {}".format(
        ac.getCarState(0, acsys.CS.KersInput)*100))
    ac.setPosition(label_KersInput, 3, 270)

    label_BarCharge = ac.addLabel(appWindow, "{}%".format(
        ac.getCarState(0, acsys.CS.KersCharge)))

    ac.setPosition(label_BarCharge, 341, 130)

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


    if(is_app_disabled()):
        return

    update_label_ers_recovery()
    update_label_ers_delivery()
    update_label_ers_heat_charging()
    update_label_ers_current_kj()
    update_label_ers_max_j()
    update_label_kers_charge()
    update_label_bar_charge()
    update_label_kers_input()
    update_label_speed_ms()




def acShutdown():
    ac_log("Session ending")
