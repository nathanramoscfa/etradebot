.. _credentials:

###########
Credentials
###########

Obtaining credentials
=====================

1. Obtain Login Credentials:

    * You will need your E\-Trade username, password, and account number.

2. Obtain API Credentials:

    * Log into the `E-Trade Developer website <https://developer.etrade.com/home>`_ and log in with your E\-Trade login
      and password.
    * Select your account from the ``Accounts`` menu.
    * Select ``Create Key`` as the "Operation Type" and then click the ``Get Sandbox Key`` button.
    * The website should then show you your consumer key, consumer secret, sandbox key, and sandbox secret.

3. Obtain API Cookie:

    * You will need to contact `E\-Trade customer service <https://us.etrade.com/contact-us>`_ to obtain a cookie that
      will need to be passed to the API so that their servers recognize your automated trading program, otherwise it
      will be blocked.
    * The best way to do this is to call the 1-800 number listed on the E-Trade website
      "`Contact Us <https://us.etrade.com/contact-us>`_" page.
    * Tell them you are calling to request an API cookie for your Python automated trading program.
    * They will then give you instructions on what you need to do.
    * It might take a couple days to verify you and obtain the cookie, and call center wait times may vary.
    * It is typically best to call around 8AM EST on business days.

4. Install keyring:

    * You can install ``keyring`` using pip by running the following command in your terminal or command prompt:

    .. code-block:: bash

        pip install keyring

5. Save your credentials:

    * Open your terminal or command prompt.
    * Run the following commands to save your credentials to ``keyring``:

        * Enter your E\-Trade consumer key when prompted.

        .. code-block:: bash

            keyring set etrade consumer_key

        * Enter your E\-Trade consumer secret when prompted.

        .. code-block:: bash

            keyring set etrade consumer_secret

        * Enter your E\-Trade sandbox key when prompted.

        .. code-block:: bash

            keyring set etrade sandbox_key

        * Enter your E\-Trade sandbox secret when prompted.

        .. code-block:: bash

            keyring set etrade sandbox_secret

        * Enter your E\-Trade web username when prompted.

        .. code-block:: bash

            keyring set etrade web_username

        * Enter your E\-Trade web password when prompted.

        .. code-block:: bash

            keyring set etrade web_password

        * Enter your E\-Trade account ID when prompted.

        .. code-block:: bash

            keyring set etrade account_id

        * Enter your E\-Trade cookie when prompted.

        .. code-block:: bash

            keyring set etrade etrade_cookie

6. Verify that your credentials are stored:

    * Run the following command to verify that your credentials are stored in ``keyring``:

    .. code-block:: bash

        keyring get etrade consumer_key

    This should output your E\-Trade consumer key.