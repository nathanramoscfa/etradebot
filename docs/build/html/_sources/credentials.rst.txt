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
    * Copy and paste these somewhere as you will need to save them in step 4.

3. Obtain API Cookie:

    * You will need to contact `E\-Trade customer service <https://us.etrade.com/contact-us>`_ to obtain a cookie that
      will need to be passed to the API so that their servers recognize your automated trading program, otherwise it
      will be blocked.
    * The best way to do this is to call the 1-800 number listed on the E-Trade website
      "`Contact Us <https://us.etrade.com/contact-us>`_" page.
    * Tell them you are calling to request an API cookie for your Python automated trading program.
    * They will then give you instructions on what you need to do.
    * It might take a couple days to verify you and obtain the cookie and call center wait times may vary.
    * It is typically best to call around 8AM EST on business days.

4. Save your credentials:

    * Open your terminal or command prompt and activate the ``etradebot`` environment if you have not already.

    .. code-block:: bash

        conda activate etradebot

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

5. Obtain your Account ID Key:

        You will need to use your credentials to obtain the ``accountIdKey`` for the account you want to use:

        * Open your terminal or command prompt.
        * Navigate to the ``etradebot`` root directory.

        .. code-block:: bash

            cd etradebot

        * Start the Python interpreter.

        .. code-block:: bash

            python

        * Import the ``list_accounts`` module. This line of code will log in to your E\-Trade account assuming you saved
          your credentials correctly in step 4.

        .. code-block:: python

            >>> from utils.list_accounts import get_account_list

        * Run the ``list_accounts`` function.

        .. code-block:: python

            >>> list_accounts()

        * This will output a ``pd.DataFrame`` of your accounts (``accountId`` is the account number) and their account ID
          keys, for example:

        .. code-block:: python

                                 accountIdKey        accountDesc accountMode accountType
            accountId
            840104290  JIdOIAcSpwR1Jva7RQBraQ         INDIVIDUAL      MARGIN   BROKERAGE

        * Copy the account ID key for the account you want to use and then use the following command to save it,
          replacing ``'JIdOIAcSpwR1Jva7RQBraQ'`` with your account ID key.

        .. code-block:: python

            >>> import keyring
            >>> keyring.set_password('etrade', 'accountIdKey', 'JIdOIAcSpwR1Jva7RQBraQ')

6. Once finished, verify that your credentials are stored:

    .. code-block:: python

        >>> from utils.credentials import show_credentials
        >>> show_credentials()

    * This should output your credentials, for example:

    .. code-block:: python

        consumer_key: 282683cc9e4b8fc81dea6bc687d46758
        consumer_secret: 2FrC9scEpzcwSEMy4vE7nodSzPLqfRINnTNY4voczyFM
        sandbox_key: 3TiQRgQCRGPo7Xdk6G8QDSEzX0Jsy6sKNcULcDavAGgU
        sandbox_secret: 7RrC9scEpzcwSEMy4vE7nodSzPLqfRINnTNY4voczyFM
        web_username: my_username
        web_password: my_password
        account_id: 840104290
        etrade_cookie: {'name': 'SWH', 'value': 'GRDKRORF5-he5abv74-25oj', 'domain': '.etrade.com', 'secure': True, 'httpOnly': True}
        account_id_key: JIdOIAcSpwR1Jva7RQBraQ