def getPts(ptsTxtFile):
    points = []
    ptsFile = open(ptsTxtFile, "r")
    while True:
        line = ptsFile.readline().strip('\n')
        if not line:
            break
        point = line.split(" ")
        points.append((float(point[0]), float(point[1])))
    return points

def getSeqs(seqTxtFile):
    seqs = []
    seqFile = open(seqTxtFile, "r")
    while True:
        line = seqFile.readline().strip('\n')
        if not line:
            break
        seqs.append(line)
    seqFile.close()
    return seqs
