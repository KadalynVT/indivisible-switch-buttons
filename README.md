# Indivisible: Switch-style buttons

For some reason the GoG version of Indivisible doesn't have a way to show the Switch button layout when using a pro controller, this is a mod that fixes that!

Grab the installer from [here](https://github.com/KadalynVT/indivisible-switch-buttons/releases/tag/v1.1)! Download and unzip `IndivisibleSwitchButtons.zip` then drag your Indivisible folder onto `IndivisibleSwitchButtons.exe`

## Run from source

First download the code however you like then open a PowerShell terminal and cd to the code directory.

You'll need a relatively new Python version installed. (3.10+ probably? newer the better..)

```ps1
py -m venv venv
. .\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py path\to\Indivisible
```

For the last command where it says `path\to\Indivisible` you can just drag your Indivisible folder into the terminal window instead of typing it.
