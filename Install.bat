@REM msiexec /i programas\graphviz-2.28.0.msi
@REM pause

cd modulos/fado-python3-master
pip install .
pause

cd ..
cd future-0.16.0
pip install .
pause

cd ..
cd decorator-4.3.0
pip install .
pause

cd ..
cd networkx-2.1
pip install .
pause

cd ..
cd pydot-1.2.4
pip install .
pause

cd ..
cd pyparsing-2.2.0
pip install .
pause

cd ..\..
pip install .
pause