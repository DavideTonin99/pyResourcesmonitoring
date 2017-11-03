@ECHO OFF

REM --- avvio USBDEVIEW.exe
USBDEVIEW.exe /scomma usb_devices_list.csv
REM --- avvio il programma python per il monitoring
REM --- python main.py
main.py
PAUSE
