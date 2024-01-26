from simulator import simulate
from config import parseConfig
import configparser

DEFAULT_CONFIG_FILE = "./config/robot_map.cfg"
KEYS = ["UNIT_LINE_SPACING", "DEG_ARC_SPACING",
        "DEG_TURN_SPACING", "SEC_CONTROL_LOOP",
        "POINTS_FILE", "SEQUENCE_FILE"]

config = configparser.ConfigParser()
config.read(DEFAULT_CONFIG_FILE)

unitPerDot = float(config.get('FLOAT', KEYS[0]))
degPerDot = float(config.get('FLOAT', KEYS[1]))
turnDegPerDot = float(config.get('FLOAT', KEYS[2]))
delay = float(config.get('FLOAT', KEYS[3]))
ptsFile = config.get('STRING', KEYS[4])
seqFile = config.get('STRING', KEYS[5])
points = parseConfig.getPts(ptsFile)
sequences = parseConfig.getSeqs(seqFile)

simulate(points, sequences, unitPerDot,
         degPerDot, turnDegPerDot, delay)