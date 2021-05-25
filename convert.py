import os
import json
import xml.etree.ElementTree as ET
import plistlib as PL

current_dir = os.path.dirname(os.path.realpath(__file__))
input_dir = os.path.join(current_dir, 'raw_json')
output_dir = os.path.join(current_dir, 'output')
spine_dir = os.path.join(current_dir, 'spine')

def createPlist(file, content):
    newFilePath = os.path.join(output_dir, file.replace('/', '_')+ '.plist')

    frameDict = dict()
    metaDict = dict()
    pl = dict()
    pl['frames'] = frameDict 
    pl['metadata'] = metaDict 

    metaDict["format"] = 3
    metaDict["premultiplyAlpha"] = False
    # metaDict["pixelFormat"] = metaJson["format"]
    # metaDict["smartupdate"] = metaJson["smartupdate"]
    metaDict["textureFileName"] = file
    metaDict["realTextureFileName"] = file
    # texSize = metaJson["size"]
    # metaDict["size"] = "{"+"{}, {}".format(texSize['w'],texSize['h'])+"}"

    for key in content:
        data = content[key]

        rect = data["rect"]
        frameDict[key] = dict()
        subDict = frameDict[key]
        subDict["aliases"] = []
        subDict["spriteOffset"] = "{0, 0}"
        sizeStr = "{"+"{}, {}".format(rect[2],rect[3])+"}"
        subDict["spriteSize"] = sizeStr
        subDict["spriteSourceSize"] = sizeStr
        subDict["textureRect"] =  "{{"+"{}, {}".format(rect[0],rect[1])+"},"+sizeStr+"}"
        subDict["textureRotated"] = False

    with open(newFilePath, 'wb') as fp:
        PL.dump(pl, fp)
###############################################
def copySpriteFrameData(item, textDict):
    if(item["__type__"] == "cc.SpriteFrame"):
            itemData = item["content"]
            name = itemData["name"]
            texture = itemData["texture"]
            if texture in textDict:
                textDict[texture][name] = itemData
            else:
                textDict[texture] = {}
                textDict[texture][name] = itemData
###############################################
allContent = list()
textDict = {}
for subdir, dirs, files in os.walk(input_dir):
    for file in files:
        filePath = os.path.join(input_dir, file)
        f = open(filePath)
        try:
            contentJson = json.load(f)
            allContent.append(contentJson)
            # for i in contentJson:
            #     allContent.append(i) 
        except:
            print('File wrong format:')
            print(filePath)
################################################################################ create spine json
count = 0 
spineCount = 0
# print(allContent)
for item in allContent:
    try:
        if(item["__type__"] == 'sp.SkeletonData'):
            spineCount = spineCount + 1
            name = item["_name"] + '.json'
            content = item["_skeletonJson"]
            fs = open(os.path.join(spine_dir, name), "w")
            fs.write(json.dumps(content))
            fs.close()
    except:
        count = count + 1

print(count)
print(spineCount)
################################################################################ create spine json end
# fs = open(os.path.join(spine_dir, name), "w")
# fs.write(json.dumps(content))
# fs.close()
################################################################################ create sprite sheet
# for item in allContent:
#     try:
#         copySpriteFrameData(item, textDict)
#     except:
#         for t in item:
#             try:
#                 copySpriteFrameData(t, textDict)
#             except:
#                 break
# print("################################################################")
# for x in textDict:
#     createPlist(x, textDict[x])
################################################################################ create sprite sheet end

