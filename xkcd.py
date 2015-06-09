#!/usr/bin/env python3
#
import requests
from lxml import html
import argparse
import os
import io
from PIL import Image
import shutil
import pickle

cacheDir=os.path.expanduser("~") + "/.cache/xkcd/"
pickle_filename = "data.pickle"
print_width = 384

class xkcdDataStructure(object):
    description = None
    name = None
    image_source = None
    instance = None
    directory = None
    image = None

    def getImage(self):
        if image:
            return Image.frombytes(**self.image)

    def setImage(self, image):
        self.image = dict(
            data = image.tobytes(),
            size = image.size,
            mode = image.mode
        )

def load(number="", overwrite=False):
    response = requests.get('http://xkcd.com/%s' % number)
    parsed_body = html.fromstring(response.text)
    meta_data = {}
    meta_data["description"] = parsed_body.xpath('//*[@id="comic"]/img/@title')[0].__str__()
    meta_data["name"] = parsed_body.xpath('//*[@id="comic"]/img/@alt')[0].__str__()
    meta_data["image_source"] = "http:%s" % (parsed_body.xpath('//*[@id="comic"]/img/@src')[0])
    meta_data["instance"] = os.path.split(os.path.splitext(meta_data["image_source"])[0])[1]
    meta_data["directory"] = "%s%s" % (cacheDir, meta_data["instance"])

    if os.path.isdir(meta_data["directory"]) and overwrite:
        print("Already downloaded %s, removing first..." % meta_data["instance"])
        shutil.rmtree(meta_data["directory"])

    if os.path.isdir(meta_data["directory"]):
        print("Already downloaded: %s" % meta_data["instance"])
        print("Using pickled variant")
        meta_data = _load_from_file(meta_data["directory"])
    else:
        os.makedirs(meta_data["directory"])
        image = _download_image(meta_data)
        _convert_image(image, meta_data)
        _save_meta_data(meta_data)

    print(meta_data)

    return meta_data

def _save_meta_data(data):
    with open("%s%s%s" % (data["directory"], os.sep, pickle_filename), "wb") as outfile:
        pickle.dump(data, outfile)

def _convert_image(image, data):
    converted_image = image.convert("1", dither=Image.NEAREST)
    converted_image.save("%s%s%s" % (data["directory"], os.sep, "converted.png"), "PNG")
    data["image"] = converted_image

def _download_image(data):
    print("Downloading image...")
    url2retrieve = data["image_source"]
    r = requests.get(url2retrieve)
    if not r.status_code == 200:
        i = 0
        raise Exception("Could not retrieve image! Status code %d" % r.status_code)
    raw_image = Image.open(io.BytesIO(r.content))
    raw_image.save("%s%s%s" % (data["directory"], os.sep, "image.png"), "PNG")
    return raw_image

def _load_from_file(path):
    with open("%s%s%s" % (path, os.sep, pickle_filename), "rb") as infile:
        return pickle.load(infile)

if __name__ == "__main__":
    if not os.path.exists(cacheDir):
        os.makedirs(cacheDir)
    parser = argparse.ArgumentParser(description='Load image and description of xkcd')
    parser.add_argument('comic_number', metavar="number", type=str, help="Number of comic to load", default="", nargs="*")
    parser.add_argument('-f', '--overwrite', action='store_true', help="Overwrite if already exists")
    args = parser.parse_args()
    load("" if args.comic_number == "" else args.comic_number[0])
