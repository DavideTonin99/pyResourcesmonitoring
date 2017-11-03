# -*- coding: utf-8 -*-
__author__ = "Davide Tonin"
__version__ = "1.0, 2017-10-10"

# -- IMPORT
from xml.dom import minidom
import datetime, os

# -- VARIABILI
results_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)),'results'))
booldebug = True

# -- FUNZIONI
def write_csv(filename, data):
    """data -> lista di dizionari contenti le informazioni da scrivere
    """
    if (len(data) == 0):
	return

    csv_dir = os.path.normpath(os.path.join(results_dir, "csv"))
    
    if not os.path.isdir(csv_dir):
        os.makedirs(csv_dir)

    filename = os.path.join(csv_dir,filename)
    file_out = open(filename, "w")
    str_out = ""
    str_out = ";".join(data[0].keys()) + "\n"

    for element in data:
        for value in element.values():
            str_out += (value+";")
        str_out = str_out[:-1] + "\n"

    file_out.write(str_out)
    file_out.close()


def write_xml(filename, data, root_tag):
    """data -> lista di dizionari contenti le informazioni da scrivere
    """
    if (len(data) == 0):
	return

    xml_dir = os.path.normpath(os.path.join(results_dir, "xml"))
    
    if not os.path.isdir(xml_dir):
        os.makedirs(xml_dir)

    filename = os.path.join(xml_dir,filename)

    xml_document = minidom.Document()
    try:
        # se c'e' gia' qualcosa di scritto correttamente sul file xml lo mantengo
        document_tree = minidom.parse(filename).documentElement
        if booldebug:
            print("Struttura file recuperata da "+filename)
    except:
        # altrimenti creo la nuova struttura
        document_tree = xml_document.createElement(root_tag)
        if booldebug:
            print("Creata struttura del file, root tag: "+root_tag)

    xml_document.appendChild(document_tree)

    id_index = 1

    time_stamp = datetime.datetime.now()

    for element in data:
        elementChild = xml_document.createElement("element")
        # imposta l'id con numero identificatore e data del log
        elementChild.setAttribute("id", str(id_index) + " " + str(time_stamp))
        id_index += 1

        for feature_k, feature_v in element.items():
            featureChild = xml_document.createElement(str(feature_k))
            featureChild.appendChild(xml_document.createTextNode(str(feature_v)))
            elementChild.appendChild(featureChild)

            if booldebug:
                print("Aggiunto su contenuto del file: " + feature_k)

        document_tree.appendChild(elementChild)

    xml_content = xml_document.toprettyxml(indent="\t").replace("\t\t\n", "").replace("\t\n", "")

    file_out = open(filename, "w")
    file_out.write(xml_content)
    file_out.close()

    if booldebug:
        print("Terminata scrittura su file xml")
