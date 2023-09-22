def main(inputFile,queryLocId,d1,d2):
    fileopen = open(inputFile, "r")
    
    header = fileopen.readline().strip().split(',')
    clm1 = header.index('LocId')
    clm2 = header.index('Latitude')
    clm3 = header.index('Longitude')
    clm4 = header.index('Category')

    lines = fileopen.readlines()
    
    queryLocId = queryLocId.upper()
    LocIdList,xList,yList,CatList = [],[],[],[]

    for line in lines:
        line = line.strip().split(",")
        LocId = (line[clm1]).upper()
        x = float(line[clm2])
        y = float(line[clm3])
        Cat = (line[clm4]).upper()
        
        LocIdList.append(LocId)
        xList.append(x)
        yList.append(y)
        CatList.append(Cat)
        
    if queryLocId in LocIdList:
        
        item = LocIdList.index(queryLocId)
        xId,yId = xList[item],yList[item]
        catId = CatList[item]

        NE = (xId+d1, yId+d2)
        NW = (xId-d1, yId+d2)
        SW = (xId-d1, yId-d2)
        SE = (xId+d1, yId-d2)
        
        output1,output2,output3 = [],[],[]
        
        for x,y in zip(xList,yList):
            index = xList.index(x)
            if x >= SW[0] and x <= SE[0] and y <= NW[1] and y >= SW[1] and (x,y) != (xId,yId):
                LocItem = LocIdList[index]
                output1.append(LocItem)
                if catId == CatList[index]:
                    output2.append(LocItem)
                    d = ( ((xId-x)**2) + ((yId-y)**2) ) ** 0.5
                    output3.append(round(d,4))
        
        CatLen = len(output3)
        if CatLen >0:
            avg = sum(output3) / CatLen
            variance = sum([((a - avg) ** 2) for a in output3]) / CatLen
            std = variance ** 0.5
            output4 = [round(avg,4),round(std,4)]
        else:
            output4 = []
        
        return output1,output2,sorted(output3),output4

    else:
        return "QueryLocId not found"