import sys
import os
from PIL import Image, ImageOps

def main():
    if len(sys.argv) != 2:
        print('Usage: python3 app.py /path/to/directory')
        return

    path = sys.argv[1]
    print("supplied path {0}".format(sys.argv[1]))

    if os.path.exists(path) == False:
        print('path {0} does not exists'.format(path))
        return
    
    if os.path.isfile(path):
        print("supplied path {0} is a file...".format(path))
        convert_jpg_to_webp(path)
        return

    #path must be a directory, walk
    print("supplied path {0} is a directory, walking...".format(path))
    go_through_a_directory(path)


def go_through_a_directory(path: str):
    print("walking through a directory {0}".format(path))
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filepath = os.path.join(root, name)
            if isImage(filepath) is False:
                print("{0} is not an image, skipping....".format(filepath))
                continue

            convert_jpg_to_webp(filepath)
        for name in dirs:
            filepath = os.path.join(root, name)
            print("{0} is a directory".format(filepath))
            go_through_a_directory(filepath)


def isImage(path: str) -> bool:
    try:
        with Image.open(path) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False


def convert_jpg_to_webp(path: str):
    print("converting {0} to webp...".format(path))
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    img = img.convert('RGB')

    name, extension = os.path.splitext(path)

    new_name = f"{name}.webp"
    print("filename after conversion: {0}".format(new_name))
    img.save(new_name, 'webp', optimize = True, quality = 70)


if __name__ == '__main__':
    main()