---
description: Scheduling your trading bot
---

# Scheduling

You can schedule `main.py` to run at any time of the day or night.&#x20;

### Method 1: Windows Task Scheduler

1. Open the Task Scheduler by pressing the Windows key + R and typing `taskschd.msc`.
2. Click on the "Create Basic Task" option on the right-hand side of the Task Scheduler window.
3. Follow the prompts to create a new task, including selecting the trigger for when you want the task to run (in this case, daily at 9AM CST).
4. In the "Actions" tab, select "Start a program" and enter the path to your Python executable (e.g., `C:\Python38\python.exe`) followed by the path to your `main.py` file.
5. Click "Finish" to create the task and schedule it to run daily at 9AM CST.

### Method 2: Google Cloud

1. Create a new Google Cloud project and enable Cloud Functions and Cloud Scheduler.
2. Deploy your `main.py` file to Cloud Functions.
3. In Cloud Scheduler, create a new job and configure the schedule to run daily at 9AM CST.
4. Configure the job to call the URL of your Cloud Function that runs `main.py`.

### Method 3: Amazon Web Services

1. Create an Amazon EC2 instance and install Python and the necessary dependencies.
2. Upload your `main.py` file to the EC2 instance.
3. Use the `crontab` command to set up a cron job that runs your script daily at 9AM CST.

### Method 4: Microsoft Azure

1. Create an Azure Function App and upload your `main.py` file.
2. Use the Azure Scheduler to create a new job and configure the schedule to run daily at 9AM CST.
3. Configure the job to call the URL of your Azure Function that runs `main.py`.

Note that these are just examples of methods for running the `main.py` file on a set schedule, and there may be other methods available depending on your specific setup and needs. It's important to choose the method that best fits your requirements and resources.
