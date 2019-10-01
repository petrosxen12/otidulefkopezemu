# otidulefkolampe
Hack{Cyprus} 2019 Project

Computer software that monitors and records the users screen usage. The user selects and categorizes desktop apps as productive and unproductive. The categorization is then used to determine the overall productivity of the user. 

The productivity data is then transmitted to a RasberryPi through an API which uses a DotMatrix and RGB LED-lights to convey it to the user.

The Dot-Matrix displays overall productivity while the RGB LED-lights provide information about real-time productivity. 

**Running the application:**:

Run `window_tracker.py` from `core` and then `rgbdot.py` on the Raspberry Pi via python. 


A demo video can be seen here (57 seconds):

https://www.youtube.com/watch?v=KHuNAQ5H4co
