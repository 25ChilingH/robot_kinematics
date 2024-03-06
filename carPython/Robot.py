import configparser
from utils import computePltPoints
from sim.config import parseConfig


class Robot:
    DEFAULT_CONFIG_FILE = "./sim/config/robot_map.cfg"
    KEYS = [
        "UNIT_LINE_SPACING",
        "DEG_ARC_SPACING",
        "DEG_TURN_SPACING",
        "SEC_CONTROL_LOOP",
        "ROBOT_WIDTH",
        "ROBOT_LENGTH",
        "POINTS_FILE",
        "DRIVE",
    ]

    config = configparser.ConfigParser()
    config.read(DEFAULT_CONFIG_FILE)

    unitPerDot = float(config.get("FLOAT", KEYS[0]))
    degPerDot = float(config.get("FLOAT", KEYS[1]))
    turnDegPerDot = float(config.get("FLOAT", KEYS[2]))
    delay = float(config.get("FLOAT", KEYS[3]))
    robotWidth = float(config.get("FLOAT", KEYS[4]))
    robotLength = float(config.get("FLOAT", KEYS[5]))
    ptsFile = config.get("STRING", KEYS[6])
    drive = config.get("STRING", KEYS[7])
    points, sequences = parseConfig.getPts(ptsFile)

    pltPoints = computePltPoints(
        points, sequences, unitPerDot, degPerDot, drive, turnDegPerDot
    )
