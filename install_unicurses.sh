wget https://netix.dl.sourceforge.net/project/pyunicurses/unicurses-1.2/UniCurses-1.2.zip
if [ $? -eq 0 ]; then
    echo Downloaded UniCurses-1.2.zip
fi
unzip UniCurses-1.2.zip
if [ $? -eq 0 ]; then
    echo Extracted UniCurses-1.2.zip
fi
cd UniCurses-1.2/
sudo python setup.py install
if [ $? -eq 0 ]; then
    echo Installed UniCurses-1.2 to Python
fi
sudo python3 setup.py install
if [ $? -eq 0 ]; then
    echo Installed UniCurses-1.2 to Python3
fi
cd ..
sudo rm -r -f UniCurses-1.2/
sudo rm UniCurses-1.2.zip
