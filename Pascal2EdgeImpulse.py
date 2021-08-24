# This script converts Pascal VOC to an Edge Impulse JSON file
# To use it, change the path to the path where your annotation files in Pascal VOC format are
# Change resize_ratio to 1 if you're not doing any resizing. 
# The file will output as "bounding_boxes.labels"

# To use it, place it in the same folder as your labels and run the edge impulse uploader: 
# edge-impulse-uploader *(must install the edge impulse CLI first)*
# see doc here https://docs.edgeimpulse.com/docs/cli-uploader

import xmltodict
import json
import os 
from collections import Counter
import time

# start = time.time()

# If resizing, add your own resize ratio here. If not, change to 1
resize_ratio = 1.3

def Pascal2JSON(path):
    attrDict = dict()
    attrDict["version"] = 1
    attrDict["type"] = "bounding-box-labels"
    images = dict()

    for filename in  os.listdir(path):
        annotations = list()
        if filename.endswith(".xml"):
            
            print(filename)
            #doc = xmltodict.parse(open(annotation_path).read())
            doc = xmltodict.parse(open(os.path.join(path, filename)).read())
            #print(doc['annotation']['filename'])
            n = 0

            if 'object' in doc['annotation']:
                #print("object found")
                #print(doc['annotation']['object'])

                for obj in doc['annotation']['object']:
                    #print("Object before conversion= %s", obj)
                    if obj == "name": # hacky code to break in case the xml file only has a single Object
                        n = 1
                        obj = doc['annotation']['object']
                    #print("Object after conversion = %s", obj)
                    annotation = dict()
                    #print(obj['name'])
                    annotation["label"] = str(obj['name']) #TypeError: string indices must be integers
                    xmin = int(obj["bndbox"]["xmin"]) / resize_ratio
                    ymin = int(obj["bndbox"]["ymin"]) / resize_ratio
                    width = (int(obj["bndbox"]["xmax"]) / resize_ratio) - xmin
                    height = (int(obj["bndbox"]["ymax"]) / resize_ratio) - ymin

                    annotation["x"] = round(xmin)
                    annotation["y"] = round(ymin)
                    annotation["width"] = round(width)
                    annotation["height"] = round(height)
                    annotations.append(annotation)
                    if n==1:
                        #print("n is one")
                        break
            filename = filename.replace(".xml",".jpg")
            images[filename] = annotations
            #image[str(doc['annotation']['filename'])] = annotations
        #images.append(image)

    attrDict["boundingBoxes"] = images

    # Write the dictionary created from XML to a JSON string
    jsonString = json.dumps(attrDict)
    with open("bounding_boxes.labels", "w") as f:
        f.write(jsonString)

path = "C:\\Users\\044560\\Documents\\EdgeImpulseTalk\\subset\\annotations"
Pascal2JSON(path)

# end = time.time() - start
# print("time is %.2f", end)