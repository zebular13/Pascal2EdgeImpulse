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

# minimum width/height of annotation 
min_size = 15
min_total_size = 300

def Pascal2JSON(input_path, output_path):
    attrDict = dict()
    attrDict["version"] = 1
    attrDict["type"] = "bounding-box-labels"
    images = dict()

    for filename in  os.listdir(input_path):
        annotations = list()
        if filename.endswith(".xml"):
            filename_jpg = filename.replace(".xml",".jpg")
            
            try:       
                print(filename)
                doc = xmltodict.parse(open(os.path.join(input_path, filename)).read())
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

                        #if height or width of any of the annotations is less than min_size, skip to next filename
                        #if(height<min_size) or (width < min_size):
                        if(height*width < min_total_size):
                            #annotation = dict()
                            raise Exception("file {0} has annotations smaller than {1}px".format(filename, min_size))

                        annotation["x"] = round(xmin)
                        annotation["y"] = round(ymin)
                        annotation["width"] = round(width)
                        annotation["height"] = round(height)
    
                        annotations.append(annotation)
                        if n==1:
                            #print("n is one")
                            break
                        
                        images[filename_jpg] = annotations
            except:
                #annotations = list()
                too_small_image = os.path.join(output_path, filename_jpg)
                print(too_small_image)
                too_small_annotation = os.path.join(input_path, filename)
                if os.path.exists(too_small_image):
                    os.remove(too_small_image)
                if os.path.exists(too_small_annotation):
                    os.remove(too_small_annotation)
                #print("file {0} has annotations smaller than {1}px".format(filename, min_size))
                continue

            
            #image[str(doc['annotation']['filename'])] = annotations
        #images.append(image)

    attrDict["boundingBoxes"] = images

    # Write the dictionary created from XML to a JSON string
    jsonString = json.dumps(attrDict)
    with open((os.path.join(output_path, "bounding_boxes.labels.json")), "w") as f:
        f.write(jsonString)

def CleanUpExtraImages(input_path, output_path):
    for filename in os.listdir(output_path):
        if filename.endswith(".jpg"):
            filename_xml = filename.replace(".jpg", ".xml")
            if not os.path.exists(os.path.join(output_path, filename_xml)):
                os.remove(os.path.join(output_path, filename))

input_path = "C:\\Users\\044560\\Documents\\EdgeImpulseTalk\\testset\\annotations"
output_path = "C:\\Users\\044560\\Documents\\EdgeImpulseTalk\\testset\\output"
Pascal2JSON(input_path, output_path)

#CleanUpExtraImages(input_path, output_path)

# end = time.time() - start
# print("time is {0}.format(end))