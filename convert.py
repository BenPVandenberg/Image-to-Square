import os
import threading
from PIL import Image, UnidentifiedImageError

num_done = 0  # number of pics converted
pics_to_do = 0  # total number of pics to do


def resize_image(image_name):
    global num_done
    global pics_to_do
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

        # notify user and update num_done
        num_done += 1
        print(str(num_done) + '/' + str(pics_to_do) + ' completed')
    except PermissionError:
        print('ERROR: Missing Permissions for image "' + image_name + '"')
        # update pics_to_do
        pics_to_do -= 1
    except UnidentifiedImageError:
        print('ERROR: Not a valid image: "' + image_name + '"')
        # update pics_to_do
        pics_to_do -= 1


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
    global pics_to_do
    pics_to_do = len(images)

    print('Start Converting Images')
    # Init threads
    threads = []
    for image in images:
        t = threading.Thread(target=resize_image, args=(image,))
        threads.append(t)
        t.start()

    # wait for threads to close
    for t in threads:
        t.join()

    input("Done. Press Enter to exit")


if __name__ == '__main__':
    main()
