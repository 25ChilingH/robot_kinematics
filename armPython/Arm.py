import utils


class Joint:
    def __init__(self, origin, axis):
        self.w = axis
        self.q = origin


class Arm:
    # M is the end effector's home configuration relative to the S frame
    # x, y, z, offset in m
    M = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0.345], [0, 0, 0, 1]]

    joints = [
        Joint([0, 0, 0.08], [0, 0, 1]),
        Joint([0, 0, 0], [1, 0, 0]),
        Joint([0, 0, 0.105], [0, 1, 0]),
        Joint([0, 0, 0.060], [0, 1, 0]),
        Joint([0, 0, 0.100], [0, 0, 0])
    ]

    # in deg
    thetas = [0, 0, 91, 0, 0]

    def getTransform(self):
        return utils.computeTransform(self.M, self.joints, self.thetas)


if __name__ == "__main__":
    a = Arm()
    print(a.getTransform())
