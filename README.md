# aiAmy


## Install for developpers
Requirements :
-python >3.11.9 (I'm using 3.13.2)
-if you want to compile everything yourself, stick to python 3.11.9 because of this https://github.com/PyAV-Org/PyAV/issues/1140

Commands :
```
#Create a virtual env (a copy of your python install basically) so the libs get installed only inside this ".venv" folder and not everywhere in the system.
python -m venv .venv

#Activate the venv.
.venv/Scripts/activate

#Install nexaai lib in binary form
pip install nexaai --prefer-binary --index-url https://github.nexa.ai/whl/cpu --extra-index-url https://pypi.org/simple --no-cache-dir

#Read the pypriject.toml and install the libs.
pip install -e .[dev]

#Launch the program.
python aiAmy/main.py
```