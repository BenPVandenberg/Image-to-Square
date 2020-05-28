import os
from PIL import Image, UnidentifiedImageError


def resize_image(image_name):
    try:
        # Original Image
        im = Image.open(image_name)
        width, height = im.size

        # New Image
        newim = Image.new(im.mode, (max(width, height), max(width, height)), (255, 255, 255, 0))
        new_width, new_height = newim.size

        # combine
        coords_to_paste = (int((new_width - width) / 2), 0)
        newim.paste(im, coords_to_paste)

        new_name = image_name[:image_name.find('.')] + "_square.png"
        newim.save('converted/' + new_name, 'PNG')
    except PermissionError:
        print('ERROR: Missing Permissions for image "' + image_name + '"')
    except UnidentifiedImageError:
        print('ERROR: Not a valid image: "' + image_name + '"')


# May add filters if required
def get_images():
    return os.listdir()


def main():
    print('Creating converted folder')
    try:
        os.mkdir('converted')
    except FileExistsError:
        pass
    print('Files Found:')
    images = [i for i in get_images() if i not in ['convert.exe', 'converted']]
    print(images)

    print('Start Converting Images')
    done = 0
    for image in images:
        resize_image(image)
        done += 1
        print(str(done) + '/' + str(len(images)) + ' completed')

    print('Done.')


if __name__ == '__main__':
    main()
