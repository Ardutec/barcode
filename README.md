# barcode
 Reads array of barcodes, take a picture of them, and upload in AWS S3 database via REST API.


#### Run the script in command line ###

This tutorial is tested for the rasbian buster full version. On a freshly installed rasbian OS, first of all, install git if, not already installed.
Enter this command to install git
``` 
sudo apt-get install git
```
Now, to download the barcode project enter the command in your shell. It may ask for username and password. Enter the email ID and corresponding github password.
```
git clone https://github.com/Ardutec/barcode
```
Save "barcode" folder in Raspberry pi parent directory. i.e. /home/pi/. In this folder prefix.json contain list of allowed prefixes, barCodeRec.log contain record of all barcode readings.  

Go to the directory "/etc/xdg/lxsession/LXDE-pi/autostart"
```
cd /etc/xdg/lxsession/LXDE-pi/autostart
```
Add this line at the end of etc/xdg/lxsession/LXDE-pi/autostart file 
@lxterminal --command="/home/pi/barcode/arscript.sh"
For that enter this command.
```
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```
Reboot Raspberry pi 
```
sudo reboot
```
If everthing other is well it will start runing python code on terminal.
