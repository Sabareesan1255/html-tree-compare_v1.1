import sys

from bs4 import BeautifulSoup
# from tabulate import tabulate
import json
# import jsondiff as jd
# from jsondiff import diff
# from pprint import pprint
import pathlib

glob_level_slice = 0


def getRecursiveChildsJson(childNodes):
    retLst = []

    for child in childNodes:
        # print("\tChld - {}", child.name)

        pathN = '.'.join(reversed([p.name for p in child.parentGenerator() if p]))

        global glob_level_slice

        elementNLevel = len(pathN.split(".")) - glob_level_slice
        if str(child.attrs).__eq__('{}'):
            levelNJson = {"tagName": child.name, "attrs": child.attrs, "level": elementNLevel, "childs": []}
        else:
            levelNJson = {"tagName": child.name+"["+str(child.attrs)+"]", "attrs": child.attrs, "level": elementNLevel, "childs": []}

        subChildNodes = child.find_all(recursive=False)

        # print("\t\tsubChl - {}", len(subChildNodes))

        if len(subChildNodes) > 0:
            subChildJson = getRecursiveChildsJson(subChildNodes)

            if len(subChildJson) >= 0:
                for sls in subChildJson:
                    levelNJson["childs"].append(sls)

        retLst.append(levelNJson)

    return retLst


def generateJsonData(contents, fileType, outputJsonFile, outputJsFile, isMasterFile=False):
    soup = None

    if fileType == 'xml':
        soup = BeautifulSoup(contents, 'xml')
    if fileType == 'html':
        soup = BeautifulSoup(contents, 'lxml')

    nestArr = []

    initJson = {
        "levelMax": 0,
        "nodeList": []
    }

    for elem in soup.findAll():

        # print("Element - {}", elem.name)
        # for p in elem.parentGenerator():
        #     print("Parents - {}",p.name)

        path = '.'.join(reversed([p.name for p in elem.parentGenerator() if p]))
        # print("{:>10} | {} | {:>10}".format(elem.name, elem.attrs, path))

        nestArr.append([elem.name, elem.attrs, path, len(path.split(".")) - glob_level_slice])

        elementLevel = len(path.split(".")) - glob_level_slice

        if elementLevel > initJson["levelMax"]:
            initJson["levelMax"] = elementLevel

        if elementLevel == 1:
            # print("recursive child list")
            if str(elem.attrs).__eq__('{}'):
                levelOneJson = {"tagName": elem.name, "attrs": elem.attrs, "level": elementLevel, "childs": []}
            else:
                levelOneJson = {"tagName": elem.name+"["+str(elem.attrs)+"]", "attrs": elem.attrs, "level": elementLevel, "childs": []}

            childNodes = elem.find_all(recursive=False)

            # print("chl - {}", len(childNodes))

            if len(childNodes) > 0:
                childJson = getRecursiveChildsJson(childNodes)

                if len(childJson) >= 0:
                    for ls in childJson:
                        levelOneJson["childs"].append(ls)

            initJson["nodeList"].append(levelOneJson)

        # else:
        # print("check with existing parent list")

    # print(tabulate(nestArr, headers=["tag", "attrs", "tree", "level"]))

    global depthCompareLevel

    if depthCompareLevel == 0 and isMasterFile is True:
        depthCompareLevel = initJson["levelMax"]

    jsonString = json.dumps(initJson)
    jsonFile = open(outputJsonFile, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    jsFile = open(outputJsFile, "w")
    if isMasterFile is True:
        jsFile.write("const masterDataJson = " + jsonString)
    else:
        jsFile.write("const compareDataJson = " + jsonString)
    jsFile.close()


# print(sys.argv)
# print(len(sys.argv))

if len(sys.argv) != 4:
    print("Invalid inputs provided please provide")
    print("python <script_path> <compare_file_1_path> <compare_file_2_path> <depth>")
    print("EG: python compareDiff.py cmpA.html cmpB.html 5")
    sys.exit()

cmpAFile = sys.argv[1]
cmpBFile = sys.argv[2]
depthCompareLevel = sys.argv[3]

if depthCompareLevel.isnumeric():
    depthCompareLevel = int(depthCompareLevel)
else:
    print("Depth level must be number")
    sys.exit()


def readJsonFile(file):
    with open(file, 'r') as ff:
        data = json.load(ff)
        return data


if pathlib.Path(cmpAFile).exists() and pathlib.Path(cmpBFile).exists() and pathlib.Path(
        cmpAFile).is_file() and pathlib.Path(cmpBFile).is_file():

    if pathlib.Path(cmpAFile).suffix == pathlib.Path(cmpBFile).suffix:

        if pathlib.Path(cmpAFile).suffix == '.xml' or pathlib.Path(cmpAFile).suffix == ".html":

            fileAContents = ""
            fileBContents = ""

            with open(cmpAFile, 'r', encoding="utf-8") as f:
                fileAContents = f.read()

            with open(cmpBFile, 'r', encoding="utf-8") as f:
                fileBContents = f.read()

            jsonSavePath = pathlib.Path(cmpAFile).parent
            # jsonSavePath = pathlib.Path(jsonSavePath).joinpath('/')

            if pathlib.Path(cmpAFile).suffix == '.xml':
                generateJsonData(fileAContents, 'xml', pathlib.Path(jsonSavePath).joinpath('dataA.json'), pathlib.Path(jsonSavePath).joinpath('dataA.js'), True)
                generateJsonData(fileBContents, 'xml', pathlib.Path(jsonSavePath).joinpath('dataB.json'), pathlib.Path(jsonSavePath).joinpath('dataB.js'))

            if pathlib.Path(cmpAFile).suffix == '.html':
                generateJsonData(fileAContents, 'html', pathlib.Path(jsonSavePath).joinpath('dataA.json'), pathlib.Path(jsonSavePath).joinpath('dataA.js'), True)
                generateJsonData(fileBContents, 'html', pathlib.Path(jsonSavePath).joinpath('dataB.json'), pathlib.Path(jsonSavePath).joinpath('dataB.js'))

            # print("depth level for comparison = {}".format(depthCompareLevel))
            #
            # df = diff(readJsonFile('dataA.json'), readJsonFile('dataB.json'),syntax='explicit',marshal=True)
            #
            # print(df)
            #
            # pprint(df["$update"])

        else:
            print("Currently html, xml compare is only supported")
            sys.exit()

    else:
        print("Two files should be of same file type")
        sys.exit()

else:
    print("Unable to find the input files provided")
    sys.exit()
