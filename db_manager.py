# -*- coding: utf-8 -*-
__author__ = "Davide Tonin"
__version__ = "1.0, 2017-10-10"

# -- IMPORT
from mysql.connector import MySQLConnection, Error
import datetime, os

# -- VARIABILI
booldebug = True
db_config = {'password': '',
                'host': '',
                'user': '',
                'database': ''}

# -- FUNZIONI
def connect(db='monitoring'):
    """ Connect to MySQL database """
    db_config['database'] = db
    try:
        if booldebug:
            print('Connettendo al database MySql...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            if booldebug:
                print('Connessione stabilita.')
            return conn
        else:
            if booldebug:
                print('Connessione fallita.')
            return None

    except Error as error:
        if booldebug:
            print(error)
        return None


def upload_on_db(table, data, db="monitoring"):
    """Carica i dati sul database
    Scrive su un file tutti gli INSERT in modo tale da averne una copia
    data -> lista di dizionari (chiavi=colonne, valori=righe)
    """
    if (len(data) == 0):
        if (booldebug):
            print("Lista dei dati vuota")
        return
    
    conn = connect(db)
    connected = True
    if (type(conn) != MySQLConnection):
        connected = False
    else:
        cursor = conn.cursor()

    backup_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),"db_backup")
    if not os.path.isdir(backup_dir):
        os.mkdir(backup_dir)

    file_backup = open(os.path.join(backup_dir,os.environ['COMPUTERNAME']+"_" + table +"_" + datetime.datetime.now().strftime("%d_%m_%y") + "_db_backup.sql"),"w")

    try:
        db_columns = ",".join(data[0].keys())

        if booldebug:
            print(db_columns)

        for element in data:
            db_row = "'"+"','".join(element.values())+"'"
            if booldebug:
                print(db_row)
            query = "INSERT INTO "+table+"("+db_columns+") VALUES("+db_row+");"
            file_backup.write(query+"\n")
            if booldebug:
                print(query)
            if (connected):
                cursor.execute(query)
                conn.commit()

    except Error as e:
        print('Error:', e)

    if (connected):
        cursor.close()
        conn.close()

    file_backup.close()
"""
#if __name__ == "__main__":
    #upload_on_db("network",[{'name': '[00000000] Intel(R) PRO/1000 MT Desktop Adapter', 'default_gateway': '10.0.2.2', 'computer_name': 'TONIN', 'mac_address': '08:00:27:C5:13:0C', 'ip_address': '10.0.2.15'}, {'name': '[00000001] Microsoft Kernel Debug Network Adapter', 'default_gateway': '', 'computer_name': 'TONIN', 'mac_address': 'None', 'ip_address': ''}, {'name': '[00000002] Microsoft ISATAP Adapter', 'default_gateway': '', 'computer_name': 'TONIN', 'mac_address': 'None', 'ip_address': ''}, {'name': '[00000003] Microsoft Teredo Tunneling Adapter', 'default_gateway': '', 'computer_name': 'TONIN', 'mac_address': 'None', 'ip_address': ''}])
    #upload_on_db("os",[{'os_name': 'Microsoft Windows 10 Pro', 'build_number': '10586', 'version': '10.0.10586', 'system_directory': 'C:\\Windows\\system32', 'install_date': '20161013160339.000000+120', 'service_pack': '0', 'distributed': 'False', 'number_of_users': '2', 'computer_name': 'TONIN', 'os_type': '18', 'windows_directory': 'C:\\Windows'}])
    #upload_on_db("product",[{'name': 'KB4023057', 'computer_name': 'TONIN'}, {'name': 'Python 2.7.14', 'computer_name': 'TONIN'}, {'name': 'Windows 10 Update and Privacy Settings', 'computer_name': 'TONIN'}, {'name': 'UpdateAssistant', 'computer_name': 'TONIN'}])
    #upload_on_db("usb", [{'description': 'Mediatek Bluetooth Adaptor', 'firmware_revision': '0.00', 'device_name': '', 'disabled': 'No', 'drive_letter': '', 'connected': 'Yes', 'device_type': 'Wireless Controller', 'serial_number': '', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}, {'description': 'SM-G950F', 'firmware_revision': '4.00', 'device_name': '', 'disabled': 'No', 'drive_letter': '', 'connected': 'No', 'device_type': 'Unknown', 'serial_number': '', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}, {'description': 'SAMSUNG Mobile USB Modem', 'firmware_revision': '4.00', 'device_name': '', 'disabled': 'No', 'drive_letter': 'COM5', 'connected': 'No', 'device_type': 'Communication', 'serial_number': '', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}, {'description': 'USB Composite Device', 'firmware_revision': '2.30', 'device_name': 'Port_#0005.Hub_#0003', 'disabled': 'No', 'drive_letter': '', 'connected': 'No', 'device_type': 'Unknown', 'serial_number': '', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}, {'description': 'SAMSUNG Android ADB Interface', 'firmware_revision': '4.00', 'device_name': 'Port_#0006.Hub_#0003', 'disabled': 'No', 'drive_letter': '', 'connected': 'No', 'device_type': 'Vendor Specific', 'serial_number': '', 'safe_to_unplug': 'No', 'computer_name': 'TONIN'}, {'description': 'Generic STORAGE DEVICE USB Device', 'firmware_revision': '2.72', 'device_name': 'Port_#0006.Hub_#0003', 'disabled': 'No', 'drive_letter': '', 'connected': 'No', 'device_type': 'Mass Storage', 'serial_number': '000000000272', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}, {'description': 'SAMSUNG Mobile USB Composite Device ', 'firmware_revision': '4.00', 'device_name': 'Port_#0006.Hub_#0003', 'disabled': 'No', 'drive_letter': '', 'connected': 'No', 'device_type': 'Unknown', 'serial_number': '04157df4d3374004', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}, {'description': 'Corsair Voyager SliderX1 USB Device', 'firmware_revision': '11.00', 'device_name': 'Port_#0006.Hub_#0003', 'disabled': 'No', 'drive_letter': 'H:', 'connected': 'No', 'device_type': 'Mass Storage', 'serial_number': 'AATGYE375RJI2JBR', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}, {'description': 'SanDisk Cruzer Edge USB Device', 'firmware_revision': '1.03', 'device_name': 'Port_#0006.Hub_#0003', 'disabled': 'No', 'drive_letter': '', 'connected': 'No', 'device_type': 'Mass Storage', 'serial_number': '200517382007DD414D02', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}, {'description': 'USB Speakers', 'firmware_revision': '5.04', 'device_name': 'USB 2.0 PC Camera', 'disabled': 'No', 'drive_letter': '', 'connected': 'Yes', 'device_type': 'Audio', 'serial_number': '', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}, {'description': 'Dispositivo video USB', 'firmware_revision': '5.04', 'device_name': 'USB 2.0 PC Camera', 'disabled': 'No', 'drive_letter': '', 'connected': 'Yes', 'device_type': 'Video', 'serial_number': '', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}, {'description': 'USB Composite Device', 'firmware_revision': '5.04', 'device_name': 'USB 2.0 PC Camera', 'disabled': 'No', 'drive_letter': '', 'connected': 'Yes', 'device_type': 'Unknown', 'serial_number': '', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}, {'description': 'USB Composite Device', 'firmware_revision': '2.30', 'device_name': 'USB Keyboard', 'disabled': 'No', 'drive_letter': '', 'connected': 'Yes', 'device_type': 'Unknown', 'serial_number': '', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}, {'description': 'Generic STORAGE DEVICE USB Device', 'firmware_revision': '9.03', 'device_name': 'USB Storage', 'disabled': 'No', 'drive_letter': 'E:', 'connected': 'Yes', 'device_type': 'Mass Storage', 'serial_number': '000000000903', 'safe_to_unplug': 'Yes', 'computer_name': 'TONIN'}])"""
