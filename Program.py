import exifread
from shutil import copy
import os

for file in os.listdir("input"):
    if file.lower().endswith(".jpg"):
        image = open("input\\{0}".format(file), "rb")
        metadata = exifread.process_file(image)
        try:
            device = str(metadata["Image Make"])
        except Exception:
            print("No device name found for: \"{0}\"".format(file))
            device = ""

        if "WA" in file:
            newFileName = file.replace("IMG-", "")
            copy("input\\{0}".format(file), "output\\{0}".format(file))
        elif device == "Apple":
            newFileName = str(metadata["EXIF DateTimeOriginal"]).replace(":", "").replace(" ", "_") + ".jpg"
            copy("input\\{0}".format(file), "output\\{0}".format(newFileName))
        else:
            copy("input\\{0}".format(file), "output\\{0}".format(file))
