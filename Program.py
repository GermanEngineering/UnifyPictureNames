import exifread
from shutil import copy2
import os
from datetime import datetime
import logging
import Progress


def UnifyPictureNames():
    processedFiles = 0
    renamedFiles = 0
    unchangedFiles = 0
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
                logging.info("{0} - No capture time found for: \"{1}\"".format(GetFormattedDatetimeNow(), os.path.join(path, file)))

            # WhatsApp images
            if "WA" in file:
                newFile = file.replace("IMG-", "")
                copy2(os.path.join(path, file), GetUniqueFile(path.replace("input", "output"), newFile))
                logging.debug("{0} - {1} --> {2}".format(GetFormattedDatetimeNow(), os.path.join(path, file), os.path.join(path.replace("input", "output"), newFile)))
                renamedFiles += 1
            # pictures with creation timestamp
            elif captureTime != "":
                _, fileExtension = os.path.splitext(file)
                newFile = captureTime.replace(":", "").replace(" ", "_") + fileExtension.lower()
                copy2(os.path.join(path, file), GetUniqueFile(path.replace("input", "output"), newFile))
                logging.debug("{0} - {1} --> {2}".format(GetFormattedDatetimeNow(), os.path.join(path, file), os.path.join(path.replace("input", "output"), newFile)))
                renamedFiles += 1
            # files without creation timestamp
            else:
                copy2(os.path.join(path, file), GetUniqueFile(path.replace("input", "output"), file))
                unchangedFiles += 1

            processedFiles += 1
            Progress.PrintProgress(processedFiles)

    logging.info("{0} - Processed Files: {1} | RenamedFiles: {2} | Unchanged Files: {3}".format(GetFormattedDatetimeNow(), processedFiles, renamedFiles, unchangedFiles))


def GetFormattedDatetimeNow():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# Check if file already exists and rename if needed
def GetUniqueFile(fileDirectory, file):
    fileName, fileExtension = os.path.splitext(file)
    filePath = os.path.join(fileDirectory, fileName)
    if os.path.isfile("{0}{1}".format(filePath, fileExtension)):
        fileNumber = 2
        while os.path.isfile("{0}_{1}{2}".format(filePath, fileNumber, fileExtension)):
            fileNumber += 1
        filePath = "{0}_{1}".format(filePath, fileNumber)

    return "{0}{1}".format(filePath, fileExtension)


try:
    logging.basicConfig(filename="UnifyPictureNames.log", level=logging.INFO)
    logging.info("{0} - ##### Program Start #####".format(GetFormattedDatetimeNow()))
    UnifyPictureNames()
    logging.info("{0} - ##### Execution Finished #####\n".format(GetFormattedDatetimeNow()))
except Exception as e:
    logging.exception("{0} - {1}".format(GetFormattedDatetimeNow(), e))
