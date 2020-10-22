# Firefighter Stopwatch
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-green.svg)](https://github.com/JSC-electronics/Adeon/blob/master/LICENSE)
[![Donate](https://img.shields.io/badge/donate-PayPal-blueviolet.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=SESX9ABM7V8KA&source=url)

This repository contains the code we originally developed to assist with Firefighter competitions. You can read about it in [our blog post][firefighter-stopwatch].

<img src="https://github.com/vzahradnik/vzahradnik-blog/raw/master/content/posts/2019-06-17-stopwatch-for-firefighter-competitions/images/stopwatch-gui.gif">

## Features
- Measure split time and total time for each team
- On each checkpoint, also measure pressure, water flow, and engine RPMs
- Display results on the screen
- Store data into CSV file for later analysis

## Technical details
This tool was originally written for the Raspberry Pi. If you install the latest Raspberry Pi OS with GUI and all the Python libraries specified in the [requirements.txt](requirements.txt) file, you should have no issues running it. All sensors and triggers for this application should be connected to the Raspberry Pi GPIO bus. For the exact pinout, see the script source code.

### Used libraries
- [Gpiozero][gpiozero] - creates an abstraction layer over Raspberry Pi's GPIO. Working with the GPIO bus is then easier.
- [Pillow][pillow] - displays images in the GUI
- Adafruit libraries - used for communication with sensors
- [Tcl/Tk][tkinter] - GUI library
- Some other dependencies. For a complete list, see the [requirements.txt](requirements.txt) file

## Installation on the Raspberry Pi
- First, install and configure the Gpiozero library, as instructed [here][gpiozero-install]
- Then, download this repository, e.g., into the `Documents` folder
```bash
[pi@raspberry Documents]$ git clone https://github.com/JSC-electronics/firefighter-stopwatch.git
Cloning into 'firefighter-stopwatch'...
remote: Enumerating objects: 167, done.
remote: Counting objects: 100% (167/167), done.
remote: Compressing objects: 100% (67/67), done.
remote: Total 167 (delta 94), reused 167 (delta 94), pack-reused 0
Receiving objects: 100% (167/167), 62.68 KiB | 197.00 KiB/s, done.
Resolving deltas: 100% (94/94), done.
[pi@raspberry Documents]$
```
- Create Python virtual environment:
```bash
[pi@raspberry firefighter-stopwatch (develop)]$ python3 -m venv venv
created virtual environment CPython3.8.6.final.0-64 in 191ms
  creator CPython3Posix(dest=/home/vzahradnik/Documents/firefighter-stopwatch/venv, clear=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/vzahradnik/.local/share/virtualenv)
    added seed packages: pip==20.1.1, setuptools==50.2.0, wheel==0.35.1
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator
```
- Load the environment and install required libraries
```bash
source venv/bin/activate
python -m pip install -r requirements.txt
```
- Install Tcl/Tk GUI library using `apt-get`. Python provides only bindings to control the library, but it must be installed system-wide
- Finally, you can run the script
```bash
python stopwatch.py
```

## Running on a regular PC
One of the reasons we used the Gpiozero library was that it supports a `remote GPIO`. If you have a Raspberry Pi, you can hook up all sensors into the RPi, set up a GPIO server, and then connect to the RPi from your PC. The code will work as if it was run on the Raspberry Pi. Please follow [this guide][remote-gpio] to make it work.

### Limitations
- The Adafruit libraries, which are used to read water pressure, don't support running on a PC. Therefore, our script disables pressure measurement. Other features should work fine.
- This script was also modified to be run without any additional config. However, in this case, there's nothing much to do. All the functionality requires GPIO access. Without GPIO, you can at least see the GUI.

## Usage
We know this application was developed for very specific usage. However, it still demonstrates how to build a decent GUI, work with GPIO bus, evaluate data in a background thread, etc.

### Files
- `stopwatch.py` - main script file
- `config.json` - contains configuration variables. If the script doesn't find the config, it still contains reasonable defaults
- `gfx/` - graphical assets used in the GUI
- `l10n` - app translations

Our script uses relative paths, so if you keep the folder structure, everything should work OK.

## Localization
Originally, our GUI was in the Czech language. To make it easier for you, we implemented translations using [GNU gettext][gettext]. Now you should see the GUI in English while we also maintain Czech and Slovak translations.

## License

Copyright (c) 2019-2020 JSC electronics. All rights reserved.

Licensed under the [Apache-2.0](LICENSE) license.

[//]: # (Used references)
[firefighter-stopwatch]: https://www.zahradnik.io/stopwatch-for-firefighter-competitions
[tkinter]: https://docs.python.org/3/library/tkinter.html
[pillow]: https://python-pillow.org/
[gpiozero]: https://gpiozero.readthedocs.io/en/stable/
[gpiozero-install]: https://gpiozero.readthedocs.io/en/stable/installing.html
[remote-gpio]: https://gpiozero.readthedocs.io/en/stable/remote_gpio.html
[gettext]: https://docs.python.org/3/library/gettext.html