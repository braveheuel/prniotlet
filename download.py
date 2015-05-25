#!/usr/bin/env python3
#
import requests
from lxml import html
import argparse

class xkcdloader:

    def __init__(self):
        self.cacheDir = "~/.xkcd/"

    def load(self, number=""):
        response = requests.get('http://xkcd.com/%s' % number)
        parsed_body = html.fromstring(response.text)
        print(parsed_body.xpath('//*[@id="comic"]/img/@title'))
        print(parsed_body.xpath('//*[@id="comic"]/img/@alt'))
        print(parsed_body.xpath('//*[@id="comic"]/img/@src'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Load image and description of xkcd')
    parser.add_argument('comic_number', metavar="number", type=str, help="Number of comic to load", default="", nargs="*")
    args = parser.parse_args()
    print(args.comic_number)
    xkcdl = xkcdloader()
    xkcdl.load(args.comic_number)
