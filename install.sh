cp ./unicguard.py /usr/lib/python2.7/unicguard.py
if [ $? -eq 0 ]; then
    echo Copyed unicguard to python2.7
fi
cp ./unicguard.py /usr/lib/python3/dist-packages/unicguard.py
if [ $? -eq 0 ]; then
    echo Copyed unicguard to python3 dist-packages
fi
cp ./unicguard.py /usr/lib/python3.5/unicguard.py
if [ $? -eq 0 ]; then
    echo Copyed unicguard to python3.5
fi
