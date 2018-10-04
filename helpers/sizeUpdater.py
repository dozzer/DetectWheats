from xml.etree import ElementTree
from termcolor import colored
from os.path import isdir
from os import makedirs, rmdir
import os
from sys import exit
from glob import glob as xmlFiles
import shutil
import argparse

# Directories
# train_directory = 'train/wrong_data'  # It should contain the xml files with bounding boxes
# test_directory = 'test/wrong_data'  # It should contain the xml files with bounding boxes
input_folder = "../annotations/wrong_data"

out_folder = "../annotations/wrong_data/fixed"

if not isdir(input_folder):
    print(colored('[!]', 'yellow', attrs=['bold']), colored('The training or test directories do not exist'))
    exit(1)
else:
    print(colored('[Ok]', 'green'), colored('Directories exists'))

counter_ok = 0
counter_fail = 0;
everythingWentAsExpected = True


def copy_image(folder, file):
    name = os.path.split(file)[0]+"/"+os.path.splitext(os.path.split(file)[1])[0] + ".jpg"
    shutil.copy2(name, folder)


def fix_file(folder, file):
    xmlFile = ElementTree.parse(file)
    boxes = xmlFile.findall('object/bndbox')
    file_can_be_recovered = True
    for box in boxes:
        # xmin, ymin, xmax, ymax = box.getchildren()

        xmin = int(box.find('xmin').text)
        xmax = int(box.find('xmax').text)
        ymin = int(box.find('ymin').text)
        ymax = int(box.find('ymax').text)

        out_xmin = min(xmax, xmin)
        out_xmax = max(xmax, xmin)

        out_ymin = min(ymax, ymin)
        out_ymax = max(ymax, ymin)

        box.find('xmin').text = str(out_xmin)
        box.find('xmax').text = str(out_xmax)
        box.find('ymin').text = str(out_ymin)
        box.find('ymax').text = str(out_ymax)
        print("ok")

    xmlFile.write(folder + "/" + os.path.split(file)[1])
    copy_image(folder, file)


for tree in [input_folder]:
    # if args.move and not isdir(tree + '/wrong_data'):
    #     makedirs(tree + '/wrong_data')

    for file in xmlFiles(tree + '/*.xml'):
        xmlFile = ElementTree.parse(file)
        boxes = xmlFile.findall('object/bndbox')
        file_can_be_recovered = True
        for box in boxes:
            # xmin, ymin, xmax, ymax = box.getchildren()
            xmin = box.find('xmin')
            ymin = box.find('ymin')
            xmax = box.find('xmax')
            ymax = box.find('ymax')
            x_value = int(xmax.text) - int(xmin.text)
            y_value = int(ymax.text) - int(ymin.text)

            if (abs(x_value) < 32 or abs(y_value) < 32):
                # print(colored('xmax , xmin ', 'red', attrs=['bold']), (xmax.text, xmin.text))
                file_can_be_recovered = False
            # else:
            #     if (x_value < 0):
            #         # print(colored('xmax - xmin', 'yellow', attrs=['bold']), x_value)
            #         tmp = xmin.text
            #         xmin.text = xmax.text
            #         xmax.text = tmp
            #         print(colored('xmax , xmin ', 'yellow', attrs=['bold']), (xmax.text, xmin.text))
            #         box.set('xmin', xmin.text)
            #         box.set('xmax', xmax.text)
            #     if (y_value < 0):
            #         # print(colored('ymax - ymin', 'yellow', attrs=['bold']), y_value)
            #         tmp = ymin.text
            #         ymin.text = ymax.text
            #         ymax.text = tmp
            #         print(colored('ymax , ymin ', 'yellow', attrs=['bold']), (ymax.text, ymin.text))
            #         box.set('ymin', ymin.text)
            #         box.set('ymax', ymax.text)

            # x_value = int(xmax.text) - int(xmin.text)
            # y_value = int(ymax.text) - int(ymin.text)
            #
            # if x_value < 33 or y_value < 33:
            #     print(colored('[!]', 'red'),
            #           'File {} contains a bounding box smaller than 32 in height or width'.format(file))
            #     print(colored('xmax - xmin', 'yellow', attrs=['bold']), x_value)
            #     print(colored('ymax - ymin', 'yellow', attrs=['bold']), y_value)
            #     everythingWentAsExpected = False

            # if args.move:
            #     wrongPicture = xmlFile.find('filename')
            #     try:
            #         shutil.move(file, tree + '/wrong_data/')
            #         shutil.move(tree + '/' + wrongPicture.text, tree + '/wrong_data/')
            #         print(colored('Files moved to' + tree + '/wrong_data', 'blue'))
            #     except Exception as e:
            #         print(colored(e, 'blue'))
        if (file_can_be_recovered):
            print(colored('[Ok] ', 'green'), file)
            counter_ok = counter_ok + 1
            fix_file(out_folder, file)
        else:
            print(colored('[Fail] ', 'red'), file)
            counter_fail = counter_fail + 1

print(colored('[Ok]', 'green'), 'files:', counter_ok)
print(colored('[Error]', 'red'), ' files:', counter_fail)
# if everythingWentAsExpected:
#     print(colored('[Ok]', 'green'), 'All bounding boxes are equal or larger than 32 :-)')
#     # try:
#     #     rmdir(train_directory + '/wrong_data')
#     #     rmdir(test_directory + '/wrong_data')
#     # except OSError:
#     #     print(colored('[Info]', 'blue'), 'Directories wrong_data were not removed because they contain some files')
#
# else:
#     print()
#     print(colored('[Error]', 'red'), ' (╯°□°)╯ ┻━┻')
