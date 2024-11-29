import os
import glob
from datetime import datetime
import PIL.Image
import PIL.ExifTags
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from tqdm import tqdm


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
    except:
        pass
    return exif

#dir_list = os.listdir(".")
dir_list = glob.glob("*.MOV")
inc = 0
for i in tqdm(dir_list):
    inc+= 1
    file_ext = os.path.splitext(i)[1]
    if file_ext.lower() == ".mov":
        try:
            parser = createParser(i)
            metadata = extractMetadata(parser)
            datetime_object = metadata.get('creation_date')
        finally:
            parser = None
            metadata

        fmt_date = "%Y:%m:%d %H:%M:%S"
        new_name = datetime_object.strftime('%Y%m%d_%H%M%S') + str(inc) + "i" + file_ext
        print("Rename "+i + " to " + new_name)
        os.rename(i,new_name)

    if "DateTime" in get_file_meta(i).keys():
        str_date = get_file_meta(i)["DateTime"][:-1]
        fmt_date = "%Y:%m:%d %H:%M:%S"
        datetime_object = datetime.strptime(str_date, fmt_date )
        make = str(get_file_meta(i)["Make"])
        if make.strip().lower() == "apple":
            new_name = datetime_object.strftime('%Y%m%d_%H%M%S') + str(inc) + "i" + file_ext
            print("Rename "+i + " to " + new_name)
            os.re(i,new_name)
        else:
            print("Skip " + i + " make: " + make)
