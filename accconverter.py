#!/usr/bin/env python
# Written by Andres Erbsen and Sandra Schumann, distributed under the GNU GPLv3

import sys

def main():
    fin = open(sys.argv[1], 'r')
    t = [rida.split() for rida in fin.read().split('\n') if rida]
    s = ""
    startCam = int(t[0][0])
    startSen = int(t[0][1])
    accs = []
    gyrs = []
    
    for rida in t:
        if rida[0] == "A":
            accs.append([int(rida[1]), float(rida[2]), float(rida[3]), float(rida[4])])
        elif rida[0] == "G":
            gyrs.append([int(rida[1]), float(rida[2]), float(rida[3]), float(rida[4])])
    
    accs.sort()
    gyrs.sort()
    
    startTime = min(accs[0][0], gyrs[0][0])
    dpoints = []
    
    accp = 0
    accn = 1
    gyri = 0
    
    while gyri < len(gyrs) and accn < len(accs):
        if gyrs[gyri][0] < startTime:
            gyri += 1
        elif gyrs[gyri][0] > accs[accn][0] or accs[accp][0] == accs[accn][0]:
            accp += 1
            accn += 1
        else:
            ndata = []
            ndata.append((accs[accn][1]-accs[accp][1])*(gyrs[gyri][0]-accs[accp][0])/(accs[accn][0]-accs[accp][0])+accs[accp][1])
            ndata.append((accs[accn][2]-accs[accp][2])*(gyrs[gyri][0]-accs[accp][0])/(accs[accn][0]-accs[accp][0])+accs[accp][2])
            ndata.append((accs[accn][3]-accs[accp][3])*(gyrs[gyri][0]-accs[accp][0])/(accs[accn][0]-accs[accp][0])+accs[accp][3])
            dpoints.append([str(float(gyrs[gyri][0]+startSen-startCam)/1000000000),str(-ndata[2]),str(-ndata[1]),str(-ndata[0]),str(-gyrs[gyri][3]),str(-gyrs[gyri][2]),str(-gyrs[gyri][1]),"0.0","0.0","0.0"])
            gyri += 1
    
    for rida in dpoints:
        s += "[10]("+','.join(rida)+")\n"
    fout = open(sys.argv[2], 'w')
    fout.write(s)
    fout.close()
    return 0

if __name__ == '__main__':
	main()

