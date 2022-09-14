## Development install
1. Deployment virtual enviroment, install packages from ```requirements.txt```:
```
cd ./temperature_monitor
pip install -r requirements.txt
```
2. Install stem packages in ```editable mode```:
```
pip install -e .
```
It find and run setup.py in ```editable mode```. It's meaning than any changes to the original package would reflect directly in your environment.

3.You can build the ```docs``` with ```setup.py``` also:
```
python setup.py build_sphinx
```
And you can also do it:
```
cd ./docs
make html
```
