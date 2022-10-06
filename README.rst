auto-menorah
============

Self-lighting menorah!
======================

Software Dependencies
=====================
This project depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_ (8.0.0-beta.0 or later)
* `CircuitPython asyncio module <https://github.com/adafruit/Adafruit_CircuitPython_asyncio>`_
* `CircuitPython datetime module <https://github.com/adafruit/Adafruit_CircuitPython_Datetime>`_
* `CircuitPython requests module <https://github.com/adafruit/Adafruit_CircuitPython_Requests>`_
* `CircuitPython ticks module <https://github.com/adafruit/Adafruit_CircuitPython_ticks>`_


Software Installation
=====================

Installing CircuitPython
------------------------

| You can instructions for installing the latest version of CircuitPython for the Raspberry Pi Pico here:
| `<https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython>`_

Adding CircuitPython Modules & Drivers
--------------------------------------

| Please ensure all module & driver dependencies are available on the CircuitPython filesystem. This is easily achieved by downloading the Adafruit library and driver bundle:
| `<https://circuitpython.org/libraries>`_

Adding Code to Board
--------------------

Add the following files and folders from the repository to the CIRCUITPY filesystem:

* ``code.py`` file
* ``support`` folder

Additionally, you'll want to add a file named ``secrets.py`` to the filesystem that looks like this:

.. code-block:: python

    secrets = {
        "ssid": "YourWiFiName",
        "password": "YourWiFiPassword"
    }

    location = {
        "zipcode" = "Your5DigitZipcode"
    }

You'll want to update the fields with your Wi-Fi network's name and password, and zipcode accordingly.  Don't share it with anyone!
