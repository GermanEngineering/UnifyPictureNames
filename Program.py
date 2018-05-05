import exifread
from shutil import copy
import os

for path, subDirectories, files in os.walk("input"):
    for file in files:

        # create output path
        if not os.path.exists(path.replace("input", "output")):
            os.makedirs(path.replace("input", "output"))

        # get file metadata
        metadata = exifread.process_file(open(os.path.join(path, file), "rb"))
        captureTime = ""
        try:
            captureTime = str(metadata["EXIF DateTimeOriginal"])
        except Exception:
            print("No capture time found for: \"{0}\"".format(os.path.join(path, file)))

        # WhatsApp images
        if "WA" in file:
            newFileName = file.replace("IMG-", "")
            copy(os.path.join(path, file), os.path.join(path.replace("input", "output"), newFileName))
        # pictures with creation timestamp
        elif captureTime != "":
            _, fileExtension = os.path.splitext(file)
            newFileName = captureTime.replace(":", "").replace(" ", "_") + fileExtension.lower()
            copy(os.path.join(path, file), os.path.join(path.replace("input", "output"), newFileName))
        # files without creation timestamp
        else:
            copy(os.path.join(path, file), os.path.join(path.replace("input", "output"), file))
