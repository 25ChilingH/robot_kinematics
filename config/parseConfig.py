def getPts(ptsTxtFile):
    points = []
    seqs = []
    ptsFile = open(ptsTxtFile, "r")
    while True:
        line = ptsFile.readline().strip('\n')
        if not line:
            break
        idx = line.find('(')
        seqs.append(line[:idx])
        point = line[idx+1:line.find(')')].split(',')
        points.append((float(point[0]), float(point[1])))
    return points, seqs
