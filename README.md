# PMOI - Putta Mask On It!

PMOI utilizes TensorFlow machine learning running on a Python backend and sends results to an HTML UI.

This project is the cumulative effort of the following over the weekend of December 5-6, 2020 at the [Code for Good 2020 virtual hackathon from HackDuke](https://hackduke.org/).
* Albert Lua
* Daniel Trager
* Jason Leong
* Paul Shin
* Sai Coumar

![Sample UI screenshot](https://github.com/saiccoumar/PMOI/blob/main/sample.png?raw=true)

# Running PMOI
Our release of PMOI comes with an already pre-trained model `masknet2.h5`. Our backend runs on Python, more specifically built on Python 3.8.6 (any issues that may arise, such as TensorFlow, may be the result of incompabitilities).

### Prerequisites
* Python 3.8.6
* MacOS or Windows
* Camera device that is readable in slot 0 (generally a USB camera attached) [future feature, ability to change input]

### Windows
The following describes how PMOI runs:
1. Gets PIP to install required modules
2. Installs PIP
3. Runs `app.py` on Python
4. Launches `localhost:8000` for UI
To terminate the process, go to command prompt and `Ctrl+C`.

### MacOS
(Instructions pending)
