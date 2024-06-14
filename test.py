file = open('Test3.gcode', 'r')
gcode = file.readlines()
normalInfillSpeed = 0


def getFirstLayerLine():
    layerChanges = []
    for index, line in enumerate(gcode):
        if(';LAYER_CHANGE' in line):
            # print(index)
            layerChanges.append({"line": line, "index": index})
            if(len(layerChanges) > 2):
                break
    return {"start": layerChanges[0], "end": layerChanges[1]}


# print(getFirstLayerLine())

def getLines(endLine, startLine=0):
    lines = []
    for index, line in enumerate(gcode):
        if(index >= startLine and index < endLine):
            lines.append({"line": line, "index": index})
    return lines

layers = getFirstLayerLine()

firstLayers = getLines(layers["end"]["index"], layers["start"]["index"])

def findTypes(desiredType, listOfLayers):
    layerChanges = []
    for index, element in enumerate(listOfLayers):
        if(type(element) == type({})):
            if(';TYPE:' in element["line"]):
                # print(line)
                layerChanges.append({"line": element["line"], "index": element["index"]})
                # if(len(layerChanges) > 2):
                #     break
        else:
            if(';TYPE:' in element):
                # print(line)
                layerChanges.append({"line": element, "index": index})
                # if(len(layerChanges) > 2):
                #     break
    return list(filter(lambda x: desiredType in x["line"], layerChanges))
# print(*firstLayers, sep="\n")

solidInfillLayers = findTypes("Solid infill", firstLayers)

beginLayer = lambda x : x[1]["index"] if(len(x) > 1) else layers["end"]["index"]

# print(firstLayers[77])
# print(beginLayer(solidInfillLayers))
# print(solidInfillLayers)

# print(beginLayer(solidInfillLayers), solidInfillLayers[0]["index"])

solidInfillLines = getLines(beginLayer(solidInfillLayers), solidInfillLayers[0]["index"])

def getInfillSpeed():
    listOfInfills = findTypes("Solid infill", gcode)
    infillLines = getLines(len(gcode), listOfInfills[-1]["index"])
    for line in infillLines:
        if("F" in line["line"]):
            if("2700" in line["line"]):
                pass
                # print("THIS", line)


normalInfillSpeed = getInfillSpeed()

# print(*solidInfillLines, sep="\n")

for line in solidInfillLines:
    # print(line)
    if("F" in line["line"]):
        # pass
        print(line)
        editedLine = line["line"]
        # print(editedLine.index("F"))
        editedLine = editedLine[:editedLine.index("F")] + "F" + str(int(editedLine[editedLine.index("F")+1:editedLine.index("\n")]) * 2)
        print(editedLine)
        gcode[line['index']] = editedLine

with open("Test4.gcode", "w") as file:
    file.writelines(gcode)
        



# print("Results:", findTypes("Solid infill"))

