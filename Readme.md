## Setup
The setup procedure is only tested on macOS, although steps for both macOS and Windows have been given.
If you are good on computer savvy, the whole setup should cost around 5-10mins.

### 1. install python 2.7.10 
Skip this step for macOS
### 2. install required libraries 
typing the following command in terminal of Mac or power shell of Windows.
 - `pip install requests` 
 - `pip install urllib3`  

### 3. add your requirement in
You can query with specific requirement, including, boarding station, destination, date and type of seats for each train if you know the train number.
### 4. test the program
On windows, fire up a power shell at the source code folder and run `python query_train_ticket.py`  
On Mac and Linux, use terminal instead of power shell.

### 5. Schedule regular checking
On windows, you can use Task Scheduler provided out of the box. You may need to create a simple batch file to execute python script.
On macOS, you can create crontab job for scheduled tasks.
It's recommended to schedule the task at once per minute. Once you have successfully booked your desired tickets, remember to stop the scheduled task.


## limitation
1. Sender email is designed for a gmail account. And there should be no 2-factor authentication.
2. Make sure the machine-generated emails do not go to your spam folder.
3. The script works on Dec 30, 2016. It is not guaranteed to be functional any more if 12306.cn changes its API.


## To improve
1. Add station code mapping json.
2. Introduce more seat type code, especially for high speed rail way.
