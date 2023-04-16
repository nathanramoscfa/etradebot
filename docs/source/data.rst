.. _data:

#########
Data APIs
#########

About Data APIs
=====================

To run automated trading strategies, ETradeBot needs financial data APIs installed. There are two options for accessing
financial data with ETradeBot: the free `Yahooquery <https://yahooquery.dpguthrie.com/>`_ library that comes bundled
with ETradeBot and provides access to Yahoo Finance data, and the
`Bloomberg SDK <https://www.bloomberg.com/professional/support/api-library/>`_.

The Bloomberg SDK, also known as BLPAPI or the Bloomberg API, is a software development kit that grants developers
programmable access to Bloomberg's extensive financial data and services. It allows developers to integrate Bloomberg
data feeds, analytics, and other features directly into their custom applications, trading systems, or data analysis
tools. A subscription to the Bloomberg Professional Service costing about $30,000 per year is necessary to access this
data, however, you do not need a subscription to install the Bloomberg SDK. You can find more information about the
Bloomberg Professional Service at the provided `link <https://www.bloomberg.com/professional/>`_.

It's worth noting that regardless of whether you have a Bloomberg Professional Service subscription, ETradeBot requires
the installation of the Bloomberg SDK. However, if you don't have the subscription, you can still obtain financial data
for free using the Yahooquery library. Yahooquery is included as a required dependency of ETradeBot.

Installing the Bloomberg SDK
----------------------------

You can install the Bloomberg SDK using the following steps:

1. Go to the `Bloomberg download page <https://www.bloomberg.com/professional/support/api-library/>`_.
2. Download the version of the Bloomberg SDK that corresponds to your operating system.

    * "C++ Supported Release" works for most systems.

3. Follow the installation instructions for your operating system.
4. Extract the contents of the downloaded file (usually a .zip file) to a suitable directory, for example, C:\blpapi.
5. Set the required environment variables:

    * Right-click on 'This PC' or 'My Computer', and choose 'Properties'.
    * Click on 'Advanced system settings' on the left side.
    * In the 'System Properties' window, go to the 'Advanced' tab and click on 'Environment Variables'.
    * Under 'System variables', click on 'New' and add the following variables:

                * Variable name: BLPAPI_ROOT
                * Variable value: ``C:\blpapi`` (or the path where you extracted the Bloomberg API SDK)

                * Variable name: BLPAPI_INCDIR
                * Variable value: ``C:\blpapi\include`` (or the 'include' directory within the extracted SDK)

                * Variable name: BLPAPI_LIBDIR
                * Variable value: ``C:\blpapi\lib`` (or the 'lib' directory within the extracted SDK)

    * Click 'OK' to save the environment variables, and then click 'OK' again to close the 'System Properties' window.

Installing C++ Build Tools
--------------------------

Bloomberg SDK requires the C++ build tools to be installed on your system. You can install the C++ build tools using the following steps:

1. Go to the `Visual Studio Build Tools download page <https://visualstudio.microsoft.com/visual-cpp-build-tools/>`_.
2. Click "Download Build Tools" and run the installer once the download is complete.
3. In the installer, choose "Desktop development with C++" and ensure the latest versions are selected of:

    * MSVC v143 - VS 2022 C++ x64/x86 build tools
    * Windows 11 SDK

4. Install the selected components by clicking the "Install" button.
5. Once the installation is complete, restart your computer to ensure the changes take effect.

Troubleshooting
---------------

If you are having trouble installing the Bloomberg SDK, you can try the following steps:

1. Ensure that you have the latest version of the Bloomberg SDK installed.
2. Ensure that you have the latest version of the C++ build tools installed.
3. Ensure that you have set the required environment variables.
4. Try restarting your computer after installing the Bloomberg SDK and C++ build tools.

If you are still encountering issues, please `open an issue <https://github.com/nathanramoscfa/etradebot/issues>`_ and provide as much information as possible.
