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
- For instance, I will base this on Motorola devices
