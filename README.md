
<h1 align=center>AirDrops Activity Automation</h1>

This project is a program to automate the interaction with different networks and WEB3 projects to get a possible AirDrop

<h2 align=center>Contents</h2>

1. [Features](#Features)
2. [Technologies](#Technologies)
3. [Preparing to work](#Preparing-to-work)
4. [Usage](#Usage)
5. [DISCLAIMER](#DISCLAIMER)

## Features
The main features of this application include:
  + user-friendly graphical interface
  + the ability to set flexible settings
  + randomization of interaction with protocols
  + the ability to run different projects at the same time
  + the ability to run the same projects with different settings at the same time
  + ability to scale and add other projects and protocols
  + ability to run on a schedule
  + ability to save and then load the required configuration settings
  + safe shutdown in case of necessity

## Technologies

| Technology | Description |
| ----------- | ----------- |
| Python    | Programming language in which the project is implemented   |
| MySQL    | Relational database for storing transaction history   |
| SQLAlchemy    | SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL   |
| web3py    | A Python library for interacting with Ethereum.   |
| requests    | An elegant and simple HTTP library for Python  |
| aptos-sdk    | A Python library for interacting with Aptos   |
| PySide6    | Library for binding to Qt (GUI development)   |
| fake-useragent    | Library for User Agent generation   |

## Preparing to work
1. Install [Python](https://www.python.org/downloads/)
2. Download the source code of the project
3. Deploy the virtual environment (venv) in the project folder. To do this, open a terminal in the project folder and enter the command:  
   `python3 -m venv venv`
4. Activate the virtual environment with the command  
   `source venv/bin/activate`
5. Install the project dependencies, which are located in the requirements.txt file. To do this, enter the command in the terminal:  
   `pip install -r requirements.txt`
6. Add wallets and API keys to the exchange to the file `wallets_EXAMPLE.json` 
7. Change the values in the file `.env.example` and rename it to `.env`

## Usage
1. Run the `main.py` file with the command:  
   `python3 main.py`
   The program will start and the graphical interface will appear  
   ![Home screen](https://github.com/BG-SoftWare/pictures/raw/main/1.jpg)
2. Select the project in which you want to perform the activity. It opens in a new tab on the Home screen   
   ![Selected project](https://github.com/BG-SoftWare/pictures/raw/main/3.jpg)
3. Select a file with wallets
4. Check the wallets of interest and, if you want the order of the wallets to be random, leave "Shuffle Wallets" checked.
   ![Select a wallets](https://github.com/BG-SoftWare/pictures/raw/main/4.png)
5. Fill in the fields in the main project settings window    
   ![Filling the fields](https://github.com/BG-SoftWare/pictures/raw/main/4.png)
   _* For Aptos in the block of withdrawal from the exchange to the wallet in the fields min and max it is necessary to specify the value in APT and select USDT or USDC in order to buy the specified amount of APT or select APT to withdraw the already bought one_  
   _* In Swap, Pool, Lending blocks the value is specified as a percentage of the amount withdrawn from the exchange. If there was no withdrawal from the exchange, the percentage is taken from the wallet balance_  
   _* The exchange deposit block specifies the amount of token to be left on the wallet_  
6. Specify the amount of time to spend on each account or enable the ASAP feature (As soon as possible)
7. Press the "Run" button and wait for the program to finish executing. If you have specified Telegram token and chat ID, the program will send a notification to Telegram after it finishes.

_To run the program according to the schedule, press the "Set schedule" button, set the desired date and time, fill in all required fields in the settings, press the "Run" button and DO NOT CLOSE the program.
On the specified date and time the program will start to perform the interaction according to the specified settings._  
_To save the config after entering all data, click "Save config" button. A window will appear in front of you, in which you need to specify the name of the config.
All configuration files are stored in the path settings/{project_name}/{settings_name} relative to the main.py file. You can delete unnecessary config or make changes to it at any time_

## DISCLAIMER
The user of this software acknowledges that it is provided "as is" without any express or implied warranties. 
The software developer is not liable for any direct or indirect financial losses resulting from the use of this software. 
The user is solely responsible for his/her actions and decisions related to the use of the software.
