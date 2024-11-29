"""Module providing a function for printing renaming files."""
import os
import glob
from datetime import datetime
import PIL.Image
import PIL.ExifTags
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from tqdm import tqdm

"""Module providing a function for meta info."""
def get_file_meta(file):
    exif = {}
    try:
        img = PIL.Image.open(file)
        exif =  {
            PIL.ExifTags.TAGS[k] : v
            for k,v in img.getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        img.close()
    except Exception as e:
        print(e)
    return exif

#dir_list = os.listdir(".")
dir_list = glob.glob("*.MOV")
INC = 0
for i in tqdm(dir_list):
    INC+= 1
    file_ext = os.path.splitext(i)[1]
    if file_ext.lower() == ".mov":
        try:
            PARSER = createParser(i)
            metadata = extractMetadata(PARSER)
            datetime_object = metadata.get('creation_date')
        finally:
            PARSER = None


        FMT_DATE = "%Y:%m:%d %H:%M:%S"
        new_name = datetime_object.strftime('%Y%m%d_%H%M%S') + str(INC) + "i" + file_ext
        print("Rename "+i + " to " + new_name)
        os.rename(i,new_name)

    if "DateTime" in get_file_meta(i).keys():
        str_date = get_file_meta(i)["DateTime"][:-1]
        FMT_DATE = "%Y:%m:%d %H:%M:%S"
        datetime_object = datetime.strptime(str_date, FMT_DATE )
        MAKE = str(get_file_meta(i)["Make"])
        if MAKE.strip().lower() == "apple":
            new_name = datetime_object.strftime('%Y%m%d_%H%M%S') + str(INC) + "i" + file_ext
            print("Rename "+i + " to " + new_name)
            os.re(i,new_name)
        else:
            print("Skip " + i + " make: " + MAKE)
