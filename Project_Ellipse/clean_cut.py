'''
This file is intent to:
        Remove all images that has been cut(pictures of size 240x100) or added up(GEIs)

Author: Jinhao Wei
'''
import os

def Clean(path):
    for dirs in os.listdir(path):
        abs_path = path + dirs + "/"
        if os.path.isdir(abs_path):
            for images in os.listdir(abs_path):
                images = abs_path + images
                if ("cut" in images or "sum" in images):
                    os.remove(images)
                        
                        
Clean("./train/")
Clean("./test/")
