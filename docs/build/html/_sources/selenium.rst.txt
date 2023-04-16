.. _selenium:

########
Selenium
########

Configuring Selenium
====================

ETradeBot uses the Python library Selenium to interact with the E*TRADE website. If you plan to use ETradeBot, you will
need to install Selenium on your machine.

Installation
------------

If you followed the instructions in the :ref:`Environment <environment>` section, you should already have selenium
installed in your Python environment. If not, you can install Selenium using pip, the Python package manager. To
install the latest version of Selenium, run the following command:

.. code-block:: bash

    pip install selenium

Web Drivers
-----------

Selenium requires a web driver to interact with web pages. The driver acts as a proxy between Selenium and the web page
being automated.

ETradeBot supports two web drivers: Chrome and Edge. You should choose the driver that matches the browser you plan to
use with ETradeBot. The ETradeBot root directory contains a ``chromedriver.exe`` and ``msedgedriver.exe``, however,
these web drivers may not correspond to your browser version. You will simply have to replace these executable files
with the version of web driver that matches your browser version. Follow the instruction below to proceed.

Chrome
~~~~~~

To use Chrome with Selenium, you will need to download the
`ChromeDriver <https://sites.google.com/chromium.org/driver/>`_ executable and place it in the root directory of
ETradeBot.

You can download the ChromeDriver executable for your operating system from the
`official ChromeDriver downloads page <https://sites.google.com/chromium.org/driver/>`_. Make sure to download the
version that matches the version of Chrome you have installed. You can find your version of Chrome by:

1. Opening the Chrome browser and click on the three dots in the top right corner.
2. Click on "About Chrome" at the bottom of the left-panel menu.
3. You should see your version displayed, for example:

    * Version 111.0.5563.64 (Official Build) (64-bit)

4. You would then download the ChromeDriver version whose version number is closest to yours.

Once you have downloaded the ChromeDriver executable, extract it to the root directory of your ETradeBot project. This
is the same directory that contains the ``main.py`` file.

Edge
~~~~

To use Edge with Selenium, you will need to download the
`EdgeDriver <https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/>`_ executable and add it to your
system path.

You can download the EdgeDriver executable for your operating system from the
`official EdgeDriver downloads page <https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/>`_. Make
sure to download the version that matches the version of Edge you have installed. You can find your version of Edge by:

1. Opening the Edge browser and click on the three dots in the top right corner.
2. Click on "About Microsoft Edge" at the bottom of the left-panel menu.
3. You should see your version displayed, for example:

    * Version 111.0.1661.44 (Official build) (64-bit)

4. You would then download the EdgeDriver version whose version number is closest to yours.

Once you have downloaded the EdgeDriver executable, extract it to the root directory of your ETradeBot project. This is
the same directory that contains the ``main.py`` file.

Further Reading
---------------

For more information on using Selenium with Python, please refer to the official
`Selenium documentation <https://selenium-python.readthedocs.io/>`_.