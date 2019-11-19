#!/usr/bin/env python

# Define needed Imports

import os
import sys
import time
import json
import random
import shcol
import pandas
import datetime
import argparse
import logging
import argcomplete
from path import Path
from escpos.printer import Usb, Dummy
from escpos.exceptions import USBNotFoundError
from argcomplete.completers import ChoicesCompleter

## Set local variables

logging.basicConfig(level="WARNING", format="%(asctime)s %(message)s")
logging.warning("Logging is set")

configpath = Path(os.path.expanduser("~") + "/.config/print_coupon")
configfile = Path(os.path.expanduser("~") + "/.config/print_coupon/stores.json")
data = pandas.DataFrame(json.loads(configfile.bytes().decode("utf-8")))
stores = data.keys()

# Define the argparse class SetAction


class SetAction(argparse.Action):
    """
    An argparse Action class to set the action config variable to either list, stop, or
    start the instances for a specific environment(s)
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string in ["-l", "--list"]:
            shcol.print_columnized(stores, sort_items=True)
            sys.exit()


def strTimeProp(start, end, format, prop):
    """Get a date in a range of two formatted dates.
    start and end should be strings specifying dates formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned date will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, "%m/%d/%y", prop)


def get_args(stores):

    parser = argparse.ArgumentParser(
        description="""
        Pick a list of addresses and dates
    """
    )
    parser.add_argument(
        "-w",
        "--wait",
        help="Specify the seconds to wait in between prints",
        metavar="wait",
        type=int,
        default=2,
    ).completer = ChoicesCompleter(range(1, 11))
    parser.add_argument(
        "-s",
        "--store",
        help="Specify specific store to print",
        metavar="store",
        default="random",
    ).completer = ChoicesCompleter(stores)
    parser.add_argument(
        "-n",
        "--number",
        help="The amount of coupons to print",
        metavar="number",
        type=int,
        default=10,
    ).completer = ChoicesCompleter(range(1, 100))
    parser.add_argument(
        "-l", "--list", help="List all stores", nargs=0, action=SetAction
    )
    parser.add_argument(
        "-d",
        "--device",
        help="Specify the device to use: Default USB",
        nargs=1,
        default="usb",
    ).completer = ChoicesCompleter(["usb", "Dummy"])
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    logging.warning("args = %s", args)
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()
    return args


def print_coupon(store, p, num):
    now = datetime.datetime.now().strftime("%m/%d/%y")
    randate = randomDate("10/01/18", now, random.random())
    if store != "random":
        rand = store
    elif store == "random" or store == "":
        rand = random.choice(stores)
    street = data.get(rand).street
    city = data.get(rand).city
    phone = data.get(rand).phone

    addr = "\n" + street + "\n" + city + "\n" + phone + "\n"

    logging.warning(
        "{0}: Printing a random coupon or for {1} on {2}".format(num, rand, randate)
    )

    p.set(align="center")
    p.image(configpath + "/cvs.png", impl="bitImageRaster", center=True)
    p.set(font="a", align="center", smooth=True)
    p.text(addr)
    p.set(font="b", custom_size=True, width=3, height=3, align="center", smooth=True)
    p.image(configpath + "/courtesy_coupon2.png", impl="bitImageRaster", center=True)
    p.set(font="a", align="center", smooth=True)
    p.text(
        "\nPLEASE ACCEPT THIS COUPON\nIN APPRECIATION FOR ALERTING US TO\nDATE CODED PRODUCT\n\n"
    )
    p.barcode("499710000002", "UPC-A", 74, 3, "off", "")
    p.text("\n49971\n")
    p.text("\nCOUPON VALUE $3.50\nDATE ISSUED: " + randate)
    p.text("\n*************************************\n")
    p.image(configpath + "/bottom_warning.png", impl="bitImageRaster")
    p.cut()


def main():

    args = get_args(stores)
    if "dummy" in str(args.device).lower():
        p = Dummy()
        p.hw("init")
    if "usb" in str(args.device).lower():
        try:
            p = Usb(0x0416, 0x5011, in_ep=0x81, out_ep=0x03, profile="TM-P80")
        except USBNotFoundError:
            logging.warning("USB Device not found falling back to Dummy Device")
            p = Dummy()
            p.hw("init")
    p.cut()
    logging.warning("I need to cut")
    time.sleep(3)
    if args.number:
        start = int(1)
        done = int(args.number)
        while done != start:
            print_coupon(args.store, p, start)
            start += 1
            time.sleep(int(args.wait))
    print_coupon(args.store, p, start)


if __name__ == "__main__":
    main()
