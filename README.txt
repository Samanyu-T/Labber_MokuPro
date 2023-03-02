The following steps set up a Python Environment for Labber:

1) Copy this folder C:\Program Files\Keysight\Labber\python-labber into your 'envs' folder in conda
2) Inside of this env run: pip install moku
3) Install any other necessary packages 
4) Open Instrument Server and change its Python Preference to this environment
5) Change the folder with Local Drivers to the Folder containing these drivers

Now you should be good to go !!

To add functionality in the Multi-Instrument Mode follow this naming protocol:

3-letter Abbreviation for an instrument e.g. OSC for oscilloscope
The name of the parameter e.g. Timespan 
Then importantly ' - ' + The slot in which the instrument is in.

So: 'OSC Timespan - 1' sets the Timespan of an Oscilloscope in Slot 1

This naming ensures that there are no duplications and ensures that the coding in Python is much simpler.

Once you use these names, you can easily add additional functionality to the Labber Drivers
