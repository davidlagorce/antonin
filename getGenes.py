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

def feedMatrixGenes(matrixGenes , orpha , symbol):
    if not orpha in matrixGenes:
        matrixGenes['ORPHA:' + orpha] = [symbol]
    else:
        matrixGenes['ORPHA:' + orpha].append(symbol)
    return matrixGenes

def getGenesMatrix(geneData):

    matrixGenes = {}
    for disorder in geneData["JDBOR"]["DisorderList"]["Disorder"]:
        orpha = disorder['OrphaCode']
        if isinstance( disorder['DisorderGeneAssociationList']['DisorderGeneAssociation'], dict):
            matrixGenes = feedMatrixGenes(matrixGenes , orpha , disorder['DisorderGeneAssociationList']['DisorderGeneAssociation']['Gene']['Symbol'])
        else:
            for DisorderGeneAssociation in disorder['DisorderGeneAssociationList']['DisorderGeneAssociation']:
                matrixGenes = feedMatrixGenes(matrixGenes , orpha , DisorderGeneAssociation['Gene']['Symbol'])
    return matrixGenes


if __name__ == "__main__":

    genesData = getGenesData('en_product6.xml')
    matrixGenes = getGenesMatrix(geneData)
    
    print(json.dumps(matrixGenes, indent=2))