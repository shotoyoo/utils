import shutil
import os
l = os.listdir("photo")
for item in l:
    for ind,p in enumerate(os.listdir(os.path.join("photo", item))):
        shutil.copy(os.path.join("photo", item, p), "{}_{}.jpg".format(item, ind))
