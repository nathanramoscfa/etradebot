.. _environment:

###########
Environment
###########

Configuring environment
=======================

Using Anaconda
--------------

1. Install Anaconda Navigator:

    * Go to the Anaconda `download page <https://www.anaconda.com/products/distribution>`_.
    * Download the version of Anaconda Navigator that corresponds to your operating system.
    * Follow the installation instructions for your operating system.

2. Clone the GitHub repository:

    * Open a terminal or command prompt.
    * Navigate to the directory where you want to clone the repository.
    * Run the following command:

    .. code-block:: bash

        git clone https://github.com/nathanramoscfa/etradebot.git

3. Create an environment using an environment.yml file:

    * Navigate to the cloned repository directory.
    * Open the ``environment.yml`` file in a text editor.
    * Make any necessary modifications to the file.
    * Save the changes to the ``environment.yml`` file.
    * Run the following command to create the environment:

    .. code-block:: bash

        conda env create -f environment.yml

    * This will create an environment with the name specified in the ``environment.yml`` file.

4. Activate the environment:

    * Run the following command to activate the environment:

    .. code-block:: bash

        conda activate etradebot

5. Verify the environment:

    * Run the following command to verify that the environment was created successfully:

    .. code-block:: bash

        conda env list

    * This will list all of the environments that are currently available.
    * The environment you created should be listed.

6. Install dependencies:

    * With the virtual environment activated, run the following command to install the dependencies from the ``requirements.txt`` file:

    .. code-block:: bash

        pip install -r requirements.txt

7. Install ETradeBot:

    * With the virtual environment activated, install ETradeBot using the following command:

    .. code-block:: bash

        pip install etradebot

Using venv
----------

1. Clone the GitHub repository:

    * Open a terminal or command prompt.
    * Navigate to the directory where you want to clone the repository.
    * Run the following command:

    .. code-block:: bash

        git clone https://github.com/nathanramoscfa/etradebot.git

2. Create a virtual environment:

    * Navigate to the cloned repository directory.
    * Run the following command to create a new virtual environment:

    .. code-block:: bash

        python3 -m venv etradebot

    * This will create a new virtual environment named ``env`` in the current directory.

3. Activate the virtual environment:

    * Run the following command to activate the virtual environment:

    .. code-block:: bash

        source etradebot/bin/activate

4. Install dependencies:

    * With the virtual environment activated, run the following command to install the dependencies from the ``requirements.txt`` file:

    .. code-block:: bash

        pip install -r requirements.txt

    * This will install all the required packages listed in the ``requirements.txt`` file.

5. Verify the installation:

    * Run the following command to verify that the packages were installed correctly:

    .. code-block:: bash

        pip list

    * This will list all the installed packages.

6. Install ETradeBot:

    * With the virtual environment activated, install ETradeBot using the following command:

    .. code-block:: bash

        pip install etradebot
