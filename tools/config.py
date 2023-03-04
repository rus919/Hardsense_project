from configparser import ConfigParser
import os

configfile_name = "configs/default.ini"
# weaponConfig_name = "weaponConfig.ini"
config_object = ConfigParser()

if not os.path.isfile(configfile_name):
# Create the configuration file as it doesn't exist yet
    cfgfile = open(configfile_name, "w")

    config_object["TRIGGERBOT"] = {
        "enabled": "1",
        "Key": "110",
        "Delay Before Shot": "1",
        "Delay After Shot": "300"
    }
    
    with open(configfile_name, 'w') as conf:
        config_object.write(conf)
    config_object.write(cfgfile)
    cfgfile.close()

config_object = ConfigParser()
config_object.read(configfile_name)

config_trigger = config_object["TRIGGERBOT"]

triggerbotEnabled = int(config_trigger["enabled"])
triggerbotKey = int(config_trigger["Key"])
triggerbotDelayBeforeShot = int(config_trigger["Delay Before Shot"])
triggerbotDelayAfterShot = int(config_trigger["Delay After Shot"])