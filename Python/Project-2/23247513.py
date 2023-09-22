#Project 2/2022 - CITS1401
#Developed by Aline de Souza Andrade 23247513
#Program to read data and return analytical results

def main(inputFile,ListlocIDs,radius):
    check = checkInputs(inputFile,ListlocIDs,radius)
    if check:
        file = readFile(inputFile) #open file
        if file == None:
            return None,None,None,None
        else:
            title = headers(file) #check headers
            if title == None:
                return None,None,None,None
            else:
                ListlocIDs = [ListlocIDs[0].upper(),ListlocIDs[1].upper()]
                filesplit = cleanData(file,title,ListlocIDs) #remove duplicates/corrupt data
                if filesplit == None:
                    return None,None,None,None
                else:
                    locIdPosition = findPosition(ListlocIDs,filesplit) #find latitue and longitude locIds
                    C1Locations,C2Locations = checkLocations(locIdPosition,filesplit,radius) #locations inside radius
                    cat = justCategories(filesplit) #find all categories

                    categories = findCategories(C1Locations,C2Locations,cat) #output1
                    common = findCommon(C1Locations,C2Locations,cat) #output2
                    similarity = findSimilarity(categories) #output3
                    closest = closestId(C1Locations,C2Locations,locIdPosition,ListlocIDs,cat)#output4
                
                    return categories, similarity, common, closest
    else:
        return None,None,None,None
        
def checkInputs(inputFile,ListlocIDs,radius):
    if type(inputFile) == str and type(ListlocIDs) == list and len(ListlocIDs) == 2 and (type(radius) == int or type(radius) == float):
        return True
    else:
        print("Incorrect inputs. Please provide valid data.")
        return None
 
def readFile(inputFile):
    try:
        file = open(inputFile, "r")
        return file
    except IOError:
        print("File not found. Please provide a valid file.")
        return None

def headers(file):
    header=file.readline().upper().strip().split(',')
    headerCheck = ["LOCID","LATITUDE","LONGITUDE","CATEGORY"]
    headerlist = []
    count = 0
    for word in headerCheck:
        if word in header:
            headerlist.append(word)
        else:
            count += 1
    if count == 0:
        return header
    else:
        print("The required columns were not found. Please enter a valid file.")
        return None
    

def cleanData(file,title,ListlocIDs):
    h01 = title.index('LOCID')
    h02 = title.index('LATITUDE')
    h03 = title.index('LONGITUDE')
    h04 = title.index('CATEGORY')
    lines=file.readlines()
    data = {} #type:dict
    if len(lines) == 0:
        print("The data was not found. Please enter a valid file.")
        return None
    

    
    #check data
    for line in lines:
        line = line.strip().split(",")
        idN = line[h01].upper()
        lt = line[h02]
        lg = line[h03]
        cat = line[h04]

        test_lt = isNumber(lt)
        test_lg = isNumber(lg)

        if (idN.isalnum() and not idN.isalpha() and not idN.isnumeric()) and test_lt and test_lg and cat != '':
            
            value = lt,lg,cat
            if idN in data:
                del data[idN]
            else:
                data[idN] = value
            
    if ListlocIDs[0] in data and ListlocIDs[1] in data:
        return data
    else:
        print("LocId not found ou duplicated. Please enter a valid ID.")
        return None

#check latitude and longitude
def isNumber(n):
    try:
        float(n)
    except ValueError:
        return False
    return True


def findPosition(ListlocIDs,filesplit):
    locID1=filesplit[ListlocIDs[0]]
    locID2=filesplit[ListlocIDs[1]]
    
    locID1_lt = float(locID1[0])
    locID1_lg = float(locID1[1])
    
    locID2_lt = float(locID2[0])
    locID2_lg = float(locID2[1])

    locIdPosition = (locID1_lt,locID1_lg,locID2_lt,locID2_lg)
    return locIdPosition


def checkLocations(locIdPosition,filesplit,radius):
    locID1_lt = locIdPosition[0]
    locID1_lg = locIdPosition[1]
    locID2_lt = locIdPosition[2]
    locID2_lg = locIdPosition[3]
    C1 = {}
    C2 = {}
    
    for key, value in filesplit.items() :
        lt = float(value[0])
        lg = float(value[1])
        radius_C1 = (locID1_lt - lt) ** 2 + (locID1_lg - lg) ** 2
        radius_C2 = (locID2_lt - lt) ** 2 + (locID2_lg - lg) ** 2
        if radius_C1 <= radius ** 2:
            C1[key] = (value)
                
        if radius_C2 <= radius ** 2:
            C2[key] = (value)   

    return C1,C2

def justCategories(filesplit):
    categories = {}
    for value in filesplit.values() :
        categories[value[2]] = 0
    return categories

def findCategories(C1,C2,cat):
    catC1 = {x:cat[x] for x in cat}
    catC2 = {x:cat[x] for x in cat}
        
    for value in C1.values() :
        if value[2] in catC1:
            catC1[value[2]] = catC1.get(value[2],0)+1
    for value in C2.values() :
        if value[2] in catC2:
            catC2[value[2]] = catC2.get(value[2],0)+1
    categories = [catC1,catC2]
    return categories
    

def findCommon(C1,C2,cat):
    commonId = {x:[] for x,v in cat.items()} #type:dict

    for key,value in C1.items():
        if (key in C2 and C1[key] == C2[key]):
            if value[2] in commonId:
                IdValue = [key]
                commonId[value[2]].extend(IdValue)

    return commonId

def findSimilarity(categories):
    C1 = categories[0]
    C2 = categories[1]
    keys = set(C1.keys()) & set(C2.keys())
    sum_C1C2 = sum([C1[x] * C2[x] for x in keys])
    sumC1 = sum([C1[x]**2 for x in C1.keys()])
    sumC2 = sum([C2[x]**2 for x in C2.keys()])
    subtotal = (float(sumC1)**0.5) * (float(sumC2)**0.5)

    total = sum_C1C2 / subtotal

    return round(total,4)
    
def closestId(C1Locations,C2Locations,locIdPosition,ListlocIDs,cat):
    del C1Locations[ListlocIDs[0]]
    del C2Locations[ListlocIDs[1]]
    
    catC1 = {x:[] for x,v in cat.items()} #type:dict
    catC2 = {x:[] for x,v in cat.items()} #type:dict
    
    catC1Result = {}
    catC2Result = {}
    
    for key,value in C1Locations.items():
        lt = float(value[0])
        lg = float(value[1])
        distance = ((locIdPosition[0] - lt)**2 + (locIdPosition[1] - lg)**2)**0.5
        valueC1 = (key,distance)
        catC1[value[2]].append(valueC1)

    for key,value in C2Locations.items():
        lt = float(value[0])
        lg = float(value[1])
        distance = ((locIdPosition[2] - lt)**2 + (locIdPosition[3] - lg)**2)**0.5
        valueC2 = (key,distance)
        catC2[value[2]].append(valueC2)
        
    for key, value in catC1.items():
        if value:
            minvalue = min(value, key=lambda x: x[1])
            catC1Result[key] = minvalue[0],round(minvalue[1],4)
    for key, value in catC2.items():
        if value:
            minvalue = min(value, key=lambda x: x[1])
            catC2Result[key] = minvalue[0],round(minvalue[1],4)
    result = [catC1Result,catC2Result] 
    return result