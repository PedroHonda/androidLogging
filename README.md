# androidLogging
Android Logging Tool

## Summary

- General tool with the main purpose of make Android Logging easier with a GUI
- At first, the focus will be to collect the following log types and also combine them all
    - tcpdump
    - aplogs
    - video recording

## Pre-conditions to run the tool

- Python 3.7 installed
- Have root access to your Android device

## Graphic User Interface with TKinter

- All credits to the template used in this project goes to Bryan Oakley (https://stackoverflow.com/users/7432/bryan-oakley)
- His Template is available here: https://stackoverflow.com/questions/7546050
- Also available on this project in /templates/graphic.py

## ADB commands to collect logs

- Many adb commands used here are standard, but in any case, feel free to modify `/src/adbCommands.py` to your liking

## How to use the tool

- 1. Connect your Android device to your PC.
- 2. Run the `run.py` available.
- 3. Make sure the device selected (barcode) is the one you want to collect logs.
- 4. To collect TCPdump logs, you need to root your device using `Rooting` button.
- 5. Select the log types you want to collect.
- 6. Best practices is to Clean the log folder. Then, click `START` button to start logging.
- 7. And finally hit `STOP` when you are satisfied.
- 8. To copy to your machine, click `PULL`, and logs will be named after the current timestamp under `logs/` folder.