msiexec /i programas\graphviz-2.28.0.msi
pause

cd modulos/fado-python3-master
python setup.py install
pause

cd ..
cd future-0.16.0
python setup.py install
pause

cd ..
cd decorator-4.3.0
python setup.py install
pause

cd ..
cd networkx-2.1
python setup.py install
pause

cd ..
cd pydot-1.2.4
python setup.py install
pause

cd ..
cd pyparsing-2.2.0
python setup.py install
pause

cd..\..
python setup.py install --user
pause