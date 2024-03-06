def getPts(ptsTxtFile):
    points = []
    seqs = []
    ptsFile = open(ptsTxtFile, "r")
    while True:
        line = ptsFile.readline().strip('\n')
        if not line:
            break
        action = line.split(" ")
        points.append((float(action[0]), float(action[1])))
        if len(action) > 2:
            seqs.append(action[2])
    return points, seqs
