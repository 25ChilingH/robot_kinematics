from simulator import simulate
from config import parseConfig
import configparser

DEFAULT_CONFIG_FILE = "./sim/config/robot_map.cfg"
KEYS = ["UNIT_LINE_SPACING", "DEG_ARC_SPACING",
        "DEG_TURN_SPACING", "SEC_CONTROL_LOOP",
        "POINTS_FILE"]

config = configparser.ConfigParser()
config.read(DEFAULT_CONFIG_FILE)

unitPerDot = float(config.get('FLOAT', KEYS[0]))
degPerDot = float(config.get('FLOAT', KEYS[1]))
turnDegPerDot = float(config.get('FLOAT', KEYS[2]))
delay = float(config.get('FLOAT', KEYS[3]))
ptsFile = config.get('STRING', KEYS[4])
points, sequences = parseConfig.getPts(ptsFile)

simulate(points, sequences, unitPerDot,
         degPerDot, turnDegPerDot, delay)
