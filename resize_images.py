from PIL import Image
import pathlib
import os

maxsize = (320, 320)
input_path = "C:\\Users\\044560\\Documents\\EdgeImpulseTalk\\subset\\images"
output_path = "C:\\Users\\044560\\Documents\\EdgeImpulseTalk\\subset\\output"

for input_img_path in os.listdir(input_path):
    input_img_path = os.path.join(input_path, input_img_path)
    if input_img_path.endswith(".png"):
        output_img_path = str(input_img_path).replace(input_path, output_path)
        output_img_path = output_img_path.replace(".png", ".jpg")
       
        with Image.open(input_img_path) as im:
            im.thumbnail(maxsize)
            im.save(output_img_path, "JPEG", dpi=(72,72))
            #print(f"processing file {input_img_path} done...")

  