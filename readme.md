# Fork of Network_Automation

Adds GUI 

## Create Executable
To build the project install the dependencies into a virtual env: pip install -r requirements.txt

(Windows) - configure the PYTHONPATH environment variable for the virtual env: env:PYTHONPATH='C:\python_projects\Network_Automation\venv\Lib\site-packages'

(linux / mac) - export PYTHONPATH='\path\to\venv'

If you dont have pyinstaller (used to create exe): pip install pyinstaller

In the directory containing start.py: pyinstaller --noconsole --onefile .\main.py

This will create a single exe called main.exe in \dist folder

Currently has issues with more than one screen.