# -*- coding: utf-8 -*-
__author__ = "Davide Tonin"
__version__ = "1.0, 2017-10-10"

# -- IMPORT
import wmi, datetime, file_manager, os, db_manager

# -- VARIABILI
booldebug = True
cim = wmi.WMI()
file_date = datetime.datetime.now().strftime("%d_%m_%y")
time_stamp = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
computer_name = os.environ['COMPUTERNAME']

# -- FUNZIONI
def network_info():
    """Carica e salva le informazioni scelte delle schede di rete nella macchina
    Se è attiva la modalità debug, stampa a video il valore delle variabili contenenti le informazioni
    Scrive i valori su file csv, xml e li carica su database
    """
    filenameout_csv = computer_name+"_network_config_"+file_date+".csv"
    filenameout_xml = computer_name+"_network_config_"+file_date+".xml"
    network = []

    if booldebug:
        print("INIZIO FUNZIONE NETWORK\n-----------\n")
        print("Network info:\n")

    for network_config in cim.Win32_NetworkAdapterConfiguration():
        network_index = len(network)
        network.append({})

        network[network_index]['name'] = str(network_config.Caption)

        try:
            network[network_index]['default_gateway'] = str(network_config.DefaultIPGateway[0])
        except: network[network_index]['default_gateway'] = ""
        try:
            network[network_index]['ip_address'] = str(network_config.IPAddress[0])
        except: network[network_index]['ip_address'] = ""

        network[network_index]['mac_address'] = str(network_config.MACAddress)
        network[network_index]['computer_name'] = computer_name
        network[network_index]['time_stamp'] = time_stamp

        if booldebug:
            print('Name: '+network[network_index]['name'])
            print('Default Gateway: '+network[network_index]['default_gateway'])
            print('IP Address: '+network[network_index]['ip_address'])
            print('Mac Address: '+network[network_index]['mac_address'])

    file_manager.write_csv(filenameout_csv, network)
    file_manager.write_xml(filenameout_xml, network, root_tag="network_features")
    db_manager.upload_on_db(table="network",data=network)

    if booldebug:
        print("-----------\nFINE FUNZIONE NETWORK\n")


def os_info():
    """Carica e salva le informazioni scelte sul sistema operativo
    Se è attiva la modalità debug, stampa a video il valore delle variabili contenenti le informazioni
    Scrive i valori su file csv, xml e li carica su database
    """
    filenameout_csv = computer_name+"_os_info_"+file_date+".csv"
    filenameout_xml = computer_name+"_os_info_"+file_date+".xml"
    os_info = []

    if booldebug:
        print("INIZIO FUNZIONE INFORMAZIONI SISTEMA OPERATIVO\n-----------\n")
        print("OS info:\n")

    for info in cim.Win32_OperatingSystem():
        info_index= len(os_info)
        os_info.append({})

        os_info[info_index]["os_name"] = str(info.Caption)
        os_info[info_index]["build_number"] = str(info.BuildNumber)
        os_info[info_index]["distributed"] = str(info.Distributed)
        os_info[info_index]["install_date"] = str(info.InstallDate)
        os_info[info_index]["number_of_users"] = str(info.NumberOfUsers)
        os_info[info_index]["os_type"] = str(info.OSType)
        os_info[info_index]["service_pack"] = str(info.ServicePackMajorVersion)
        os_info[info_index]["windows_directory"] = str(info.WindowsDirectory)
        os_info[info_index]["system_directory"] = str(info.SystemDirectory)
        os_info[info_index]["version"] = str(info.Version)
        os_info[info_index]['computer_name'] = computer_name
        os_info[info_index]['time_stamp'] = time_stamp


        if booldebug:
            print('Name: '+os_info[info_index]["os_name"])
            print('Build Number: '+os_info[info_index]["build_number"])
            print('Computer Name: '+os_info[info_index]["computer_name"])
            print('Distributed: '+os_info[info_index]["distributed"])
            print('Install Date: '+os_info[info_index]["install_date"])
            print('Number of Users: '+os_info[info_index]["number_of_users"])
            print('Os Type: '+os_info[info_index]["os_type"])
            print('Service Pack: '+os_info[info_index]["service_pack"])
            print('Windows Directory: '+os_info[info_index]["windows_directory"])
            print('System Directory: '+os_info[info_index]["system_directory"])
            print('Version: '+os_info[info_index]["version"])

    file_manager.write_csv(filenameout_csv, os_info)
    file_manager.write_xml(filenameout_xml, os_info, root_tag="os_info")
    db_manager.upload_on_db(table="os",data=os_info)

    if booldebug:
        print("-----------\nFINE FUNZIONE INFORMAZIONI SISTEMA OPERATIVO\n")

def product_info():
    """Carica e salva le informazioni scelte dei software installati
    Se è attiva la modalità debug, stampa a video il valore delle variabili contenenti le informazioni
    Scrive i valori su file csv, xml e li carica su database
    """
    filenameout_csv = computer_name+"_product_info_"+file_date+".csv"
    filenameout_xml = computer_name+"_product_info_"+file_date+".xml"
    product = []

    if booldebug:
        print("INIZIO FUNZIONE PRODUCT\n-----------\n")
        print("Product info:\n")

    for software in cim.Win32_Product():
        product_index = len(product)
        product.append({})

        product[product_index]['name'] = str(software.Name)
        product[product_index]['computer_name'] = computer_name
        product[product_index]['time_stamp'] = time_stamp

        if (booldebug):
            print('Name: '+product[product_index]['name'])

    file_manager.write_csv(filenameout_csv, product)
    file_manager.write_xml(filenameout_xml, product, root_tag="product_features")
    db_manager.upload_on_db(table="product",data=product)

    if booldebug:
        print("-----------\nFINE FUNZIONE\n")


def usb_info():
    file_in = open(os.path.dirname(os.path.realpath(__file__))+"/usb_devices_list.csv")

    filenameout_csv = computer_name+"_usb_info_"+file_date+".csv"
    filenameout_xml = computer_name+"_usb_info_"+file_date+".xml"

    #filename_out = computer_name+"_usb_info_"+file_date+".xml"

    features_list = ['device_name','description','device_type','connected','safe_to_unplug','disabled','drive_letter','serial_number','firmware_revision']
    usb_features = []

    for line in file_in:

        if booldebug:
            print(line)

        line = line.split(",")

        if not (line[2] == "HID (Human Interface Device)"):
            usb_features_index = len(usb_features)
            usb_features.append({})
            # unisco caratteristiche scritte tra "" dopo split(",")
            for feature_id in range(len(line)):
                if feature_id < len(line)-1 and line[feature_id] != "" and line[feature_id][0] == '"' and '"' in line[feature_id+1]:
                    line[feature_id] = line[feature_id]+line[feature_id+1]
                    del line[feature_id+1]

            line = [line[0], line[1],line[2],line[3],line[4],line[5],line[7],line[8],line[13]]

            for feature_id in range(len(line)):
                usb_features[usb_features_index][features_list[feature_id]] = line[feature_id]
                if booldebug:
                    print("Aggiunto "+features_list[feature_id])
            usb_features[usb_features_index]['computer_name'] = computer_name
            usb_features[usb_features_index]['time_stamp'] = time_stamp
    file_in.close()

    file_manager.write_csv(filenameout_csv, usb_features)
    file_manager.write_xml(filename=filenameout_xml, data=usb_features, root_tag="usb_devices_list")
    db_manager.upload_on_db(table="usb", data=usb_features)


def main():
    network_info()
    product_info()
    os_info()
    usb_info()


# -- ELABORAZIONE
if __name__ == '__main__':
    main()
