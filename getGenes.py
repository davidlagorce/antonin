import itertools
import shutil
import time
import csv
import subprocess

import xmltodict
import os, os.path


def getGenesData(geneXML):
    """
    Read an xml return a dict with xmltodict package
    :return: xml parsed as dict
    """
    with open(geneXML, "r", encoding='ISO-8859-1') as ini:
        xml_dict = xmltodict.parse(ini.read())
    return xml_dict




if __name__ == "__main__":

    genesData = getGenesData('en_product6.xml')