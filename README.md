[ENG](#ENG) || [RUS](#RUS)

# ENG

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

---

# RUS

<h1 align=center>AirDrops Activity Automation</h1>

Этот проект представляет собой программу для автоматизации взаимодействия с различными сетями и проектами WEB3 с целью получения возможного AirDrop

<h2 align=center>Содержание</h2>

1. [Особенности](#Особенности)
2. [Технологии](#Технологии)
3. [Подготовка к работе](#Подготовка-к-работе)
4. [Использование](#Использование)
5. [ОТКАЗ ОТ ОТВЕТСТВЕННОСТИ](#ОТКАЗ-ОТ-ОТВЕТСТВЕННОСТИ)

## Особенности
Основные особенности этого приложения включают в себя:
  + удобный графический интерфейс
  + возможность задавать гибкие настройки
  + рандомизация взаимодействия с протоколами
  + возможность одновременного запуска разных проектов
  + возможность одновременного запуска одинаковых проектов с разными настройками
  + возможность масштабирования и добавления других проектов и протоколов
  + возможность запуска по расписанию
  + возможность сохранения и последующей загрузки нужных конфигураций настроек
  + безопасное завершение работы в случае необходимости (также есть возможность Force Stop)

## Технологии

| Технология / Библиотека | Описание |
| ----------- | ----------- |
| Python    | Язык программирования, на котором реализован проект   |
| MySQL    | Реляционная база данных для хранения истории выводов с биржи и депозитов на биржу   |
| SQLAlchemy    | Комплексный набор инструментов для работы с реляционными базами данных в Python   |
| web3py    | Библиотека для взаимодействия с Ethereum   |
| requests    | HTTP-библиотека для Python. Используется для отправки HTTP-запросов и получения ответов   |
| aptos-sdk    | Библиотека для взаимодействия с Aptos   |
| PySide6    | Библиотека для разработки графического интерфейса   |
| fake-useragent    | Библиотека для генерации User Agent   |

## Подготовка к работе
1. Установите [Python](https://www.python.org/downloads/)
2. Скачайте исходный код проекта
3. Разверните виртуальное окружение (venv) в папке с проектом. Для этого откройте терминал в папке с проектом и введите команду:  
   `python3 -m venv venv`
4. Активируйте виртуальное окружение командой  
   `source venv/bin/activate`
5. Установите зависимости проекта, которые находятся в файле requirements.txt. Для этого в терминале введите команду:  
   `pip install -r requirements.txt`
6. Добавьте кошельки и API ключи к бирже в файл `wallets_EXAMPLE.json` 
7. Внесите изменения в файл `.env.example` и переименуйте его в `.env`

## Использование
1. Запустите файл `main.py` командой:  
   `python3 main.py`
   Запустится программа и повится графический интерфейс  
   ![Главный экран](https://github.com/BG-SoftWare/pictures/raw/main/1.jpg)
2. Выберите проект, в котором хотите выполнить активность. Он откроется в новой вкладке на главном экране    
   ![Выбраный проект](https://github.com/BG-SoftWare/pictures/raw/main/3.jpg)
3. Выберите файл с кошельками
4. Отметьте интересующие кошельки и, если Вы хотите, чтобы порядок кошельков был случайным, оставьте отмеченным "Shuffle Wallets".
   ![Выбор кошельков](https://github.com/BG-SoftWare/pictures/raw/main/4.png)
5. Заполните поля в основном окне настроек проекта  
   ![Выбор кошельков](https://github.com/BG-SoftWare/pictures/raw/main/4.png)
   _* Для Aptos в блоке вывода с биржи на кошелек в полях min и max необходимо указать значение в APT и выбрать USDT или USDC для того, чтобы купить указанное количество APT либо выбрать APT, чтобы вывести уже купленный_  
   _* В блоках Swap, Pool, Lending значение указывается в проценте от выведенной с биржи суммы. В случае если вывода с биржи не было, процент берется от баланса кошелька_  
   _* В блоке депозита на биржу указывается количество токена, которое необходимо оставить на кошельке_  
6. Указать промежуток времени, которое необходимо потрать на каждый аккаунт либо включить функцию ASAP (As soon as possible)
7. Нажать кнопку "Run" и дождаться окончания выполнения программы. Если Вы указали Telegram-токен и ID чата, то после завершения работы, программа отправит уведомление в Telegram.

_Для запуска по расписанию необходимо нажать кнопку "Set schedule", установить нужную дату и время, заполнить все необходимы поля в настройках, нажать кнопку "Run" и НЕ ЗАКРЫВАТЬ программу.
В указанную дату и время программа начнёт выполнять взаимодействие по заданным настройкам._  
_Для сохранения конфига после ввода всех данных нажмите кнопку "Save config". Перед Вами появится окно, в котором необходимо указать имя конфига.
Все файлы конфигурации хранятся по пути settings/{project_name}/{settings_name} относительно файла main.py. Вы можете в любой момент удалить ненужный конфиг или внести в него изменения_

## ОТКАЗ ОТ ОТВЕТСТВЕННОСТИ
Пользователь этого программного обеспечения подтверждает, что оно предоставляется "как есть", без каких-либо явных или неявных гарантий. 
Разработчик программного обеспечения не несет ответственности за любые прямые или косвенные финансовые потери, возникшие в результате использования данного программного обеспечения. 
Пользователь несет полную ответственность за свои действия и решения, связанные с использованием программного обеспечения.
