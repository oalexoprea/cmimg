import os
from datetime import datetime
import PIL.Image
import PIL.ExifTags

def get_file_meta(file):
    exif = {}
    try:
        img = PIL.Image.open(file)
        exif =  {
            PIL.ExifTags.TAGS[k] : v
            for k,v in img.getexif().items()
            if k in PIL.ExifTags.TAGS
        }
    except:
        pass
    return(exif)

dir_list = os.listdir(".")
inc = 0
for i in dir_list:
    inc+= 1
    if "DateTime" in get_file_meta(i).keys():
        str_date = get_file_meta(i)["DateTime"][:-1]
        fmt_date = "%Y:%m:%d %H:%M:%S"
        datetime_object = datetime.strptime(str_date, fmt_date )
        make = str(get_file_meta(i)["Make"])
        file_ext = os.path.splitext(i)[1]
        if make.strip().lower() == "apple":
            new_name = datetime_object.strftime('%Y%m%d_%H%M%S') + inc + "i" + file_ext
            print("Rename "+i + " to " + new_name)
            os.rename(i,new_name)
        else:
            print("Skip " + i + " make: " + make)


