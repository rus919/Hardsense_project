from configparser import ConfigParser
import os

configfile_name = "config.ini"
weaponConfig_name = "weaponConfig.ini"
config_object = ConfigParser()

if not os.path.isfile(configfile_name):
# Create the configuration file as it doesn't exist yet
    cfgfile = open(configfile_name, "w")

    config_object["GENERAL"] = {
        "sensitivity": "1.5",
        "1": "659406436",
        "2": "4236378128"
    }
    config_object["TRIGGER"] = {
        "enabled": "1",
        "Key": "110",
        "DelayBeforeShot": "1",
        "DelayAfterShot": "300"
    }
    config_object["MAGNETTRIGGER"] = {
        "enabled": "0",
        "OnlyVisible": "0",
        "OnlyHS": "0",
        "Fov": "2.0",
        "Smooth": "1.0",
        "Key": "111",
        "DelayAfterShot": "300"
    }
    config_object["AIMBOT2"] = {
        "enabled": "1",
        "OnlyVisible": "0",
        "OnlyHS": "1",
        "RCS": "1",
        "Fov": "2.5",
        "Smooth": "15.0",
        "Key": "164"
    }
    config_object["DEFAULT-AIMBOT"] = {
        "enabled": "1",
        "OnlyVisible": "1",
        "OnlyHS": "0",
        "RCS": "1",
        "Fov": "1.5",
        "Smooth": "10.0",
        "Key": "1"
    }
    config_object["GLOCK-18"] = {
        "OnlyHS": "0",
        "Fov": "1.5",
        "Smooth": "10.0"
    }
    config_object["USP-S"] = {
        "OnlyHS": "0",
        "Fov": "1.5",
        "Smooth": "10.0"
    }
    config_object["DEAGLE"] = {
        "OnlyHS": "0",
        "Fov": "1.5",
        "Smooth": "10.0"
    }
    
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    config_object.write(cfgfile)
    cfgfile.close()

config_object = ConfigParser()
config_object.read("config.ini")

config_general = config_object["GENERAL"]
config_trigger = config_object["TRIGGER"]
config_trigger_magnet = config_object["MAGNETTRIGGER"]
config_aimbot = config_object["DEFAULT-AIMBOT"]
config_aimbot2 = config_object["AIMBOT2"]

sensitivity = float(config_general["sensitivity"])
value1 = int(config_general["1"])
value2 = int(config_general["2"])

triggerBot = int(config_trigger["enabled"])
triggerKey = int(config_trigger["Key"])
triggerDelayBeforeShot = int(config_trigger["DelayBeforeShot"])
triggerDelayAfterShot = int(config_trigger["DelayAfterShot"])

triggerMagnet = int(config_trigger_magnet["enabled"])
triggerMagnetVisibleOnly = int(config_trigger_magnet["OnlyVisible"])
triggerMagnetOnlyHS = int(config_trigger_magnet["OnlyHS"])
triggerMagnetFov = float(config_trigger_magnet["Fov"])
triggerMagnetSmooth = float(config_trigger_magnet["Smooth"])
triggerMagnetKey = int(config_trigger_magnet["Key"])
triggerMagnetDelayAfterShot = int(config_trigger_magnet["DelayAfterShot"])

aimbot = int(config_aimbot["enabled"])
aimbotVisibleOnly = int(config_aimbot["OnlyVisible"])
aimbotHead = int(config_aimbot["OnlyHS"])
aimbotRCS = int(config_aimbot["RCS"])
aimbotFov = float(config_aimbot["Fov"])
aimbotSmooth = float(config_aimbot["Smooth"])
aimbotKey = int(config_aimbot["Key"])


aimbot2 = int(config_aimbot2["enabled"])
aimbot2VisibleOnly = int(config_aimbot2["OnlyVisible"])
aimbot2Head = int(config_aimbot2["OnlyHS"])
aimbot2RCS = int(config_aimbot2["RCS"])
aimbot2Fov = float(config_aimbot2["Fov"])
aimbot2Smooth = float(config_aimbot2["Smooth"])
aimbot2Key = int(config_aimbot2["Key"])

glockHS = int(config_object["GLOCK-18"]["onlyhs"])
glockFov = float(config_object["GLOCK-18"]["fov"])
glockSmooth = float(config_object["GLOCK-18"]["smooth"])

uspsHS = int(config_object["USP-S"]["onlyhs"])
uspsFov = float(config_object["USP-S"]["fov"])
uspsSmooth = float(config_object["USP-S"]["smooth"])

deagleHS = int(config_object["DEAGLE"]["onlyhs"])
deagleFov = float(config_object["DEAGLE"]["fov"])
deagleSmooth = float(config_object["DEAGLE"]["smooth"])