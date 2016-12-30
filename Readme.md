# Setup
The setup procedure is only tested on macOS, although steps for both macOS and Windows have been given.
If you are good on computer savvy, the whole setup should cost around 5-10mins.

### 1. install python 2.7.10 
Mac OS can skip this step.
### 2. install required libraries 
typing the following command in terminal of Mac or power shell of Windows.
 	* `pip install requests` 
	* `pip install urllib3` 
### 3. give the train service in the source code
You can query with specific requirement, including, boarding station, destination, date and type of seats for each train if you know the train number.
### 4. execute the program
On windows, fire up a power shell at the source code folder and run `python query_train_ticket.py`  
On Mac and Linux, use terminal instead of power shell.


# limitation





### One big headache is the authorization

refer to https://segmentfault.com/a/1190000007544239 
12306.cn is using self signed cert, DER encoded. Need to convert to pem

First convert cer certificate to pem format
`openssl x509 -in srca.cer -inform der -outform pem -out srca.cer.pem`
use verify argument to add the pem
`verify='srca.cer.pem'`   


### ssl warning ignore
Due to python version, I need to skip the warning of "Common Name"
```
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
```


### Another issue is to convert unicode to chinese characters

One solution, 
`resp.encoding = 'utf-8'`
or
`string.encode('utf-8')