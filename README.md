# barcode
 Reads array of barcodes, take a picture of them, and upload in database 2


#### Run the script in command line ###

Extract and save "barcode" folder in Raspberry pi parent directory. i.e. /home/pi/. In this folder prefix.json contain list of allowed prefixes, barCodeRec.log contain record of all barcode readings.  

Go to the directory /etc/xdg/lxsession/LXDE-pi/autostart
> cd /etc/xdg/lxsession/LXDE-pi/autostart

Add this line at the end of etc/xdg/lxsession/LXDE-pi/autostart file 
@lxterminal --command="/home/pi/barcode/arscript.sh"
> sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

Reboot Raspberry pi 
> sudo reboot

If everthing other is well it will start runing python code on terminal.
