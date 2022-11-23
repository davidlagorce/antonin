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
        matrixGenes[orpha] = [symbol]
    else:
        matrixGenes[orpha].append(symbol)
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

def getGenesDetails(matrixGenes):

    listUniquesGenes = []
    TotalAnnotations = 0
    NumberOrpha = 0
    for orpha,genes in matrixGenes.items():
        NumberOrpha += 1
        for gene in genes:
            TotalAnnotations += 1
            if not gene in listUniquesGenes:
                listUniquesGenes.append(gene)

    print('Number of Unique Genes in Database:' , len(listUniquesGenes) )
    print('Number of Total Annotations:' , TotalAnnotations)
    print('Number of Disorders Annotated:', NumberOrpha)


def getGenetic(xml):
    data = {}
    with open(xml) as file:
        line = file.readline()
        while line != '':
            if line.find("<OrphaCode>") != -1:
                orphacode = line.split('<OrphaCode>')[1].split('</OrphaCode>')[0]
                line = file.readline()
                while line.find('/DisorderType') == -1:

                    if line.find('DisorderType') != -1:
                        DisorderTypeLine = file.readline()
                        if DisorderTypeLine.find('Category')  == -1 and DisorderTypeLine.find('Clinical group')  == -1:
                            data[orphacode] = DisorderTypeLine.split('<Name lang="en">')[1].split('</Name>')[0]
                    line = file.readline()
            line = file.readline()
        file.close()
    print(len(data))



if __name__ == "__main__":
    matrixGenes = getGenesMatrix(getGenesData(r'C:\Users\dlagorce\Desktop\en_product6.xml'))
    getGenesDetails(matrixGenes)
    getGenetic(r'C:\Users\dlagorce\Desktop\classif_156.xml')