import os
import json
import argparse
from os import makedirs
import sys
import numpy as np
import logging
import glob
from UliEngineering.Math.Coordinates import BoundingBox

folder_in = "../json"
folder_out = "../xml"


# json_filename = "_DSC4168_0EMcS1o2Sn.json"


def isValueCorrect(box):
    if ((box.maxy - box.minx) <= 32):
        return False
    if ((box.maxy - box.miny) <= 32):
        return False
    else:
        return True


def get_correct_coordinates(box):
    minx = int(box.minx)
    maxx = int(box.maxx)
    miny = int(box.miny)
    maxy = int(box.maxy)
    return min(minx, maxx), min(miny, maxy), max(minx, maxx), max(miny, maxy)


def get_xml_for_bbx(bbx_label, bbx_data):
    coords = []
    for point in bbx_data['points']['exterior']:
        coords.append(point)
    box = BoundingBox(np.asarray(coords))
    x_min, y_min, x_max, y_max = get_correct_coordinates(box)

    xml = "<object>\n"
    xml = xml + "\t<name>" + bbx_label + "</name>\n"
    xml = xml + "\t<pose>Unspecified</pose>\n"
    xml = xml + "\t<truncated>Unspecified</truncated>\n"
    xml = xml + "\t<difficult>Unspecified</difficult>\n"
    xml = xml + "\t<occluded>Unspecified</occluded>\n"
    xml = xml + "\t<bndbox>\n"
    xml = xml + "\t\t<xmin>" + str(x_min) + "</xmin>\n"
    xml = xml + "\t\t<xmax>" + str(x_max) + "</xmax>\n"
    xml = xml + "\t\t<ymin>" + str(y_min) + "</ymin>\n"
    xml = xml + "\t\t<ymax>" + str(y_max) + "</ymax>\n"
    xml = xml + "\t</bndbox>\n"
    xml = xml + "</object>\n"
    return xml


def convert_to_PascalVOC(fileName):
    try:
        file_path = os.path.join(folder_in, fileName + ".json")

        with open(file_path) as f:
            data = json.load(f)
        if len(data['objects']) == 0:
            logging.info("Ignoring Skipped Item");
            return False;

        width = data['size']['height']
        height = data['size']['width']
        image_dir_folder_Name = folder_in.split("/")[-1]

        xml = "<annotation>\n<folder>" + image_dir_folder_Name + "</folder>\n"
        xml = xml + "<filename>" + fileName + ".jpg</filename>\n"
        xml = xml + "<source>\n\t<database>Unknown</database>\n</source>\n"
        xml = xml + "<size>\n"
        xml = xml + "\t<width>" + str(width) + "</width>\n"
        xml = xml + "\t<height>" + str(height) + "</height>\n"
        xml = xml + "\t<depth>Unspecified</depth>\n"
        xml = xml + "</size>\n"
        xml = xml + "<segmented>Unspecified</segmented>\n"

        for member in data['objects']:
            if not member:
                continue;

            bbx_labels = member['classTitle']
            if not isinstance(bbx_labels, list):
                bbx_labels = [bbx_labels]

            for bbx_label in bbx_labels:
                xml = xml + get_xml_for_bbx(bbx_label, member)

        xml = xml + "</annotation>"

        # output to a file.
        xmlFilePath = os.path.join(folder_out, fileName + ".xml")
        with open(xmlFilePath, 'w') as f:
            f.write(xml)
        return True
    except Exception as e:
        logging.exception("Unable to process item " + fileName + "\n" + "error = " + str(e))
        return False


def main():
    if (not os.path.exists(folder_out)):
        makedirs(folder_out)

        # logging.exception(
        #     "Please specify a valid path to dataturks JSON output file, " + folder_out + " doesn't exist")
        # return

    count = 0;
    success = 0
    for json_file in glob.glob(folder_in + "/*.json"):
        # with open(json_file) as f:
        #     for line in lines:
        filename = os.path.splitext(os.path.basename(json_file))[0]
        status = convert_to_PascalVOC(filename)
        if (status):
            success = success + 1

        count += 1;
        if (count % 10 == 0):
            logging.info(str(count) + " items done ...")

    # logging.info("Completed: " + str(success) + " items done, " + str(
    #     len(lines) - success) + " items ignored due to errors or for being skipped items.")


def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""

    parser = argparse.ArgumentParser(
        description='Converts Supervisely output JSON file for Image bounding box to Pascal VOC format.')
    parser.add_argument('supervisely_JSON_FilePath',
                        help='Path to the JSON file downloaded from Dataturks.')
    parser.add_argument('image_download_dir',
                        help='Path to the directory where images will be dowloaded (if not already found in the directory).')
    parser.add_argument('pascal_voc_xml_dir',
                        help='Path to the directory where Pascal VOC XML files will be stored.')
    return parser


if __name__ == '__main__':
    # arg_parser = create_arg_parser()
    # parsed_args = arg_parser.parse_args(sys.argv[1:])
    # global supervisely_JSON_FilePath
    # global image_download_dir
    # global pascal_voc_xml_dir

    # setup global paths needed accross the script.
    # supervisely_JSON_FilePath = parsed_args.supervisely_JSON_FilePath
    # image_download_dir = parsed_args.image_download_dir
    # pascal_voc_xml_dir = parsed_args.pascal_voc_xml_dir
    # dataturks_JSON_FilePath = "Wheat.json"
    # image_download_dir = "image_dowload_folder"
    # pascal_voc_xml_dir = "pascal_voc_out_folder"
    main()
