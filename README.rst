CircuitPythonukiah Software
===========================

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

You can either use the automated tool, or manually add the CircuitPython firmware.

Automated Installation
^^^^^^^^^^^^^^^^^^^^^^

If you're using bash, you can use ``load-firmware.sh`` to manage loading the firmware onto the board.
Just make sure the microcontroller is in bootloader mode, and run the script from the root folder.
You must provide the version of CircuitPython you want to load, which will be downloaded and
archived.  For example, if you wanted to load CircuitPython version 8.0.0-beta.1, you would run:

.. code-block:: shell

    sudo bash tools/load-firmware.sh 8.0.0-beta.1

Note that this requires root access (hence the use of ``sudo``).

Manual Installation
^^^^^^^^^^^^^^^^^^^

You can fund instructions for installing the latest version of CircuitPython for the QT Py ESP32-S2 here:
`<https://learn.adafruit.com/adafruit-qt-py-esp32-s2/circuitpython>`_

Adding Drivers and Software
---------------------------

You can either use the automated tool to load the necessary drivers and software, or do so manually.

Automated Installation of Drivers and Software
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you're using bash, you can use ``load-software.sh`` to manage loading the software and drivers
onto the board.  First you'll want to make sure you have ``circup`` installed.  Then, just make sure
the microcontroller is in USB mode (showing as ``CIRCUITPY``), and run the script from the root folder:

.. code-block:: shell

    sudo bash tools/load-software.sh

Note that this requires root access (hence the use of ``sudo``).

This will also generate a file named ``secrets.py``; instructions for filling out this file can be found
in the project parent repository.

Manually Adding Modules & Drivers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please ensure all module & driver dependencies are available on the CircuitPython filesystem. This is
easily achieved by downloading the Adafruit library and driver bundle:
`<https://circuitpython.org/libraries>`_

You can either use ``circup`` or manually download the libraries listed in ``requirements-circup.txt``.

Manually Adding Software
^^^^^^^^^^^^^^^^^^^^^^^^

Add the following files and folders from the ``microcontroller`` folder to the CIRCUITPY filesystem:

* ``code.py`` file
* ``settings.py`` file
* ``valid.py`` file
* ``support`` folder

Additionally, you'll want to add a file named ``secrets.py`` to the filesystem that looks like this:

.. code-block:: python

    secrets = {
        "ssid": "YourWiFiName",
        "password": "YourWiFiPassword",
    }

    location = {
        "zipcode" = "Your5DigitZipcode",
    }

Instructions for filling out this file can be found in the project parent repository.

Development tools
=================

The following is relevant if you plan on developing or making modifications to the code.

``requirements-dev.txt`` has all of the local tools needed for development.

Pre-Commit
----------

``pre-commit`` is set up for this repository.  To run, simply install it and use
``pre-commit run --all-files``.

Pytest
------

``pytest`` is used to verify the delta-based timing the microcontroller uses.  I think it's
unlikely you'll want to change, but if you do, it can verified using ``pytest --location 12345``,
where ``12345`` is your ZIP code (needed for the API call, a dummy ZIP code should be fine as
well).

Server Testing code
-------------------

If you're making modifications to the code, it can be helpful to have code running on a server that
acts as a mock time service to test changes.  The CircuitPythonukiah has built in test capabilities
that allow it to mimic it's typical usage with another server other than the Adafruit IO time
service.

The two tests that can be performed are the "fast" and "long" tests.  The fast test will quickly go
through important transitions (like lighting and potentially extinguishing candles) to test these
critical times.  The long test will mimic the acutal usage, only referencing a different server.

In order to use this code a .env file named ``.env`` must be present on the microcontroller.  It must
have two keys: ``TEST_SERVER`` and ``TEST_TYPE``.  ``TEST_SERVER`` is equal to the test server IP
address, and ``TEST_TYPE`` is either ``fast`` or ``long``.  Aditionally, the server have the files
from the ``server`` folder and must be running the code FastAPI script ``server_test.py`` from it,
which can be done using ``uvicorn``.  The CircuitPythonukiah software will then handle setting up the
test on the server.

``requirements-server.txt`` is provided for convenience in recording the Python requirements.
