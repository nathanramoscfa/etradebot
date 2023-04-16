.. _scheduling:

##########
Scheduling
##########

Running your strategy
=====================

You can schedule ``main.py`` to run automatically. However, ETradeBot in live trading mode will only run if the New
York Stock Exchange (NYSE) is open. The program will check if the NYSE is open and halt if it is closed. This is
intended to prevent E-Trade server errors when submitting trades because server errors are highly likely to occur when
the market is closed.

The following is rough guide to scheduling ETradeBot to run automatically. Refer to the documentation for each method
before using:

* `Windows Task Scheduler <https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page>`_
* `Microsoft Azure <https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer>`_
* `Google Cloud <https://cloud.google.com/scheduler/docs/quickstart>`_
* `Amazon Web Services <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html>`_

Run Locally: Windows Task Scheduler
-----------------------------------

This method allows you to schedule main.py to run using the Windows Task Scheduler. You can have Windows Task Scheduler
run a batch file (.bat) with all the commands or you can manually configure the task in Windows Task Scheduler. The
easiest way to configure the task is to use a batch file.

Note that the task scheduler will only run the task if the following conditions are true:

1. The user setting up the task must have administrative privileges.
2. The computer must be turned on and the user must be logged in.
3. The computer must be connected to the internet.

If these conditions are not true, the task will not run and ETradeBot will not be able to submit trades. The task will
not run if the computer is turned off or in sleep mode where sign-in is required.

Option 1: Configuring the Task Scheduler with a Batch File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Refer to the `Windows Task Scheduler documentation <https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page>`_
for more information. The following configuration was tested on Windows 11 using Anaconda and Python 3.11. If you are
using a different operating system, package distribution, or Python version, you may have to modify the commands.

1. Open a text editor like Notepad and copy and paste the following commands, replacing the paths with the correct
   paths on your system:

    .. code-block:: bash

        @echo off
        rem Run Python script in a given conda environment from a batch file.

        rem Define here the path to your conda installation.
        set CONDA_PATH=C:\Users\25del\anaconda3

        rem Define here the name of your conda environment.
        set CONDA_ENV=etradebot

        rem Set ETradeBot to either preview or live trading mode.
        set PREVIEW=True

        rem Activate the conda environment.
        call %CONDA_PATH%\Scripts\activate.bat %CONDA_ENV%

        rem Navigate to the directory where etradebot root directory is located.
        cd C:\Users\User\etradebot

        rem Run your script.
        python main.py %PREVIEW%

        rem End the Python program.
        taskkill /IM python.exe /F

        rem Deactivate the conda environment.
        call conda deactivate

    Note to:

    * Replace ``CONDA_PATH`` with the path to your conda installation.
    * Replace ``CONDA_ENV`` with the name of your conda environment. If you named your conda environment ``etradebot``,
      then you do not need to change this.
    * Change ``PREVIEW`` to ``False`` if you want to run ETradeBot in live trading mode.
    * Replace ``C:\Users\User\etradebot`` with the path to the etradebot root directory.

2. Save the file as ``main_run.bat``, in the etradebot root directory. This will be the file that the task scheduler
   will run.
3. Open Windows Task Scheduler and click on "Create Task" in the right-hand pane. If you are prompted to select a user,
   select the user that you want to run the task as.
4. Give the task a name (e.g., "etradebot") and description (e.g., "Run etradebot") on the "General" tab.
5. In the "Security options" section, select the options, "Run only when user is logged on" and "Run with highest
   privileges".
6. In the "Triggers" tab, click "New" to add a new trigger.

    * Choose a frequency from the list: One time, Daily, Weekly, Monthly.
    * Choose a start date and time.
    * In the "Advanced settings" section, check the box labelled "Enabled".
    * Click "OK" to save the trigger.

7. In the "Actions" tab, click "New" to add a new action.

    * In the "Action" dropdown, select "Start a program".
    * In the "Program/script" field, enter the full path to the Python executable
      (e.g., ``"C:\Users\User\etradebot\run_main.bat"``).
    * Click "OK" to save the action.

8. In the "Conditions" tab, "Power" section, select all of the options:

    * "Start the task only if the computer is on AC power".
    * "Stop if the computer switches to battery power".
    * "Wake the computer to run this task".

9. Click "OK" to save the task.

Option 2: Configuring the Task Scheduler Manually
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Refer to the `Windows Task Scheduler documentation <https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page>`_
for more information. The following configuration was tested on Windows 11 using Anaconda and Python 3.11. If you are
using a different operating system, you may have to have use a different method compatible with your system.

1. Open the Task Scheduler and click on "Create Task" in the right-hand pane. If you are prompted to select a user,
   select the user that you want to run the task as.
2. Give the task a name (e.g., "etradebot") and description (e.g., "Run etradebot") on the "General" tab.
3. In the "Security options" section, select the options, "Run only when user is logged on" and "Run with highest
   privileges".
4. In the "Triggers" tab, click "New" to add a new trigger.

    * Choose a frequency from the list: One time, Daily, Weekly, Monthly.
    * Choose a start date and time.
    * In the "Advanced settings" section, check the box labelled "Enabled".
    * Click "OK" to save the trigger.

5. In the "Actions" tab, click "New" to add a new action.

    * In the "Action" dropdown, select "Start a program".
    * In the "Program/script" field, enter the full path to the Python executable
      (e.g., ``C:\Users\User\anaconda3\envs\etradebot\python.exe``).
    * In the "Add arguments" field, enter the full path to the ``main.py`` file (e.g., ``main.py``).
    * In the "Start in" field, enter the full path to the etradebot root directory (e.g., ``C:\Users\User\etradebot``).
    * Click "OK" to save the action.

6. In the "Conditions" tab, "Power" section, select all of the options:

    * "Start the task only if the computer is on AC power".
    * "Stop if the computer switches to battery power".
    * "Wake the computer to run this task".

7. Click "OK" to save the task.

Run on the Cloud: Cloud Services
--------------------------------

Running ETradeBot on a cloud platform is a great way to run the bot 24/7 without having to worry about your computer
being on. Methods for running ETradeBot on the cloud include:

1. Create a virtual machine on a cloud platform and run ETradeBot on the virtual machine.
2. Use a cloud platform's task scheduler to run ETradeBot as a script on a set schedule.

The steps for running ETradeBot using a virtual machine are the same as running ETradeBot on your local machine. The
steps for running ETradeBot using a cloud platform's task scheduler are beyond the scope of this documentation but you
can find more information in the links below. There are many cloud platforms that you can use to run ETradeBot,
including:

1. Microsoft Azure: Refer to the `Microsoft Azure documentation <https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer>`_ for more information.
2. Google Cloud Platform: Refer to the `Google Cloud documentation <https://cloud.google.com/scheduler/docs/quickstart>`_ for more information.
3. Amazon Web Services: Refer to the `Amazon Web Services documentation <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html>`_ for more information.
4. IBM Cloud: Refer to the `IBM Cloud documentation <https://cloud.ibm.com/docs/Functions?topic=Functions-scheduler>`_ for more information.
5. Oracle Cloud: Refer to the `Oracle Cloud documentation <https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionscreatingfunction.htm>`_ for more information.
6. Alibaba Cloud: Refer to the `Alibaba Cloud documentation <https://www.alibabacloud.com/help/doc-detail/140626.htm>`_ for more information.
7. DigitalOcean: Refer to the `DigitalOcean documentation <https://www.digitalocean.com/docs/functions/how-to/schedule/>`_ for more information.
8. Rackspace: Refer to the `Rackspace documentation <https://developer.rackspace.com/docs/rackspace-federation/1/getting-started-with-rackspace-federation/>`_ for more information.
9. Linode: Refer to the `Linode documentation <https://www.linode.com/docs/guides/how-to-use-linode-scheduler/>`_ for more information.
10. Vultr: Refer to the `Vultr documentation <https://www.vultr.com/docs/how-to-use-vultr-scheduler>`_ for more information.
