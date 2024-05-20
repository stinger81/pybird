# PYBIRD

## Change Log

### Version 0.10
- added once and start to timing option 
  - once will run at a specific time 
  - start will run at the start of the system

- add a pybird apps 
  - PY0START (Pybird Startup Logger)
    - Log the following data 
      - Start Time 
      - session id 
      - Pybird Dir Size 
      - Pybird Remote Dir Size 
      - Pybird Home Dir Size 
  - PY1SYS (Pybird System Monitor)
    - log the following data ever X minutes 
      - CPU % 
      - MEMORY % Used 
      - MEMORY Used KB/MB/GB/TB/PB 
      - MEMORY Free KB/MB/GB/TB/PB 
      - DISK % Used 
      - DISK Used KB/MB/GB/TB/PB 
      - DISK Free KB/MB/GB/TB/PB 
      - PYBIRD HOME DIR SIZE KB/MB/GB/TB/PB 
      - PYBIRD DATA DIR SIZE KB/MB/GB/TB/PB
    - save all data above to a csv file 
- add support to 
  - Select a specific config file 
  - Select a specific network 
  - Select a specific remote directory 
  - Select a specific platform 
- fix error in keychain when not encrypting data 
- added restriction that if encryption is enabled, keychain entries can not be entered untill key is there



### Version 0.9.1
- fixed sys arg error 
- add a CLI command to select a specific configuration file 
  - must be located in the config folder 
- Add multi network support 
  - can switch between saved data 
  - can switch between different key storage

### Version 0.9.0

- Dev Move
  - Dev mode added to system
  - All log length restrictions lifted
  - forced debug mode
  - can only be executed by `--dev` flag
- Added nre PYBIRD.py file which serves as the primary file to run the system
- Split boot mode into two separate modes
  - headless_mode
    - Prints message at start up stating it is in headless mode
    - disabled all log prints
    - sysargs
      - `-h|--headless` if true after it enables headless mode, false will disable the mode
  - operations mode
    - will disable tet and debug mode
    - sysargs
      - `-o|--operations` if true after it enables operations mode, false will disable the mode
- added secure access to all saved data
  - save key used to access app comfig
  - key required to access app data
  - key is hashed into encryption of file to protect it
- Mongo DB Atlas Changes
  - removed suport for secondary database
  - all data based are now initialized within teh program its self. this removed the limitations on database creation
- TCSVariables chnages
  - split into three files. All inherited into the file TCS_variables.py
    - Constant
      - all static variables
    - variables
      - all variables that can be changed by system state
    - error
      - all error messages
- exporting logs 
  - New automatic save structure 
    - logs -> int(UNIXTIME)_YEAR_MONTH_DAY->LOGS HERE 
      - 817265876_2020_12DEC_25 
  - fix the broken location structure 
  - add sub methods to do most of the repeated work 
    - Specific key words -> list 
    - get path location(standard loc) -> str 
    - get expected path -> str 
    - NEW export specific log(list of logs) UI select 
    - NEW export list logs (list of logs) UI select 
    - Specific methods 
      - export log (exports all logs, NO SLT)
      - export master log (NO SLT)
      - build master from session (NO SLT)
      - export session log (NO SLT)
      - export specific session 
      - export app log (NO SLT)
      - Export specific app logs 
      - NEW export SYS apps all 
      - NEW export specific SYS app 
- update session file to not be nested in a dir 
- timing update
  - Apps are ececuted in the order they are listed in the config file 
  - add an override to pybrid config for minumum time between start of steps(if min not exceed will sleep)
  - remove sleep completely(will allow for future versions to have realtime commanding)
    - replace with an interstep delay (set in pybird config)
  - remove step on boot and step on shutdown 
  - add string to select timing method
    - 'step' = step based timing
    - 'time' = time based timing
    - 'cont' = continuous timing (will run as fast as possible, No recommend for apps that post to social media)
    - 'test' = run every X minutes
    - 'request' = app will request specific times to run 
  - STEP BASED TIMING 
    - used a delta from last execution to determine to step 
    - add start time, will calulate the initial step to be based on a standard time, if blank set last step to 0.0 
  - TIME BASED TIMING 
    - will execute an a specific time 
    - will be a list of utc times in 24hr format 
    - each time will have the days of which to execute before it 
      - E = EVERYDAY 
      - M = MONDAY 
      - T = TUESDAY 
      - W = WEDNESDAY 
      - R = THURSDAY 
      - F = FRIDAY 
      - S = SATURDAY 
      - U = SUNDAY 
    - EXAMPLE 
      - ['12:00:00 E', '13:00:00 M', '14:00:00 T', '15:00:00 W', '16:00:00 R', '17:00:00 F', '18:00:00 S', '19:00:00 U'] 
      - will execute at 12:00 UTC every day 
      - will execute at 13:00 UTC every Monday 
      - will execute at 14:00 UTC every Tuesday 
      - will execute at 15:00 UTC every Wednesday 
      - will execute at 16:00 UTC every Thursday 
      - will execute at 17:00 UTC every Friday 
      - will execute at 18:00 UTC every Saturday 
    -   will execute at 19:00 UTC every Sunday 
- update step structure 
  - add config option to load_data_before_step 
    - if true will execute the method (load_data) before the step 
  - add config option to save_data_after_step 
    - if true will execute the method (save_data) after the step
  

### Version 0.8.8-PA
- **ALL PREVIOUSLY ADDED KEYS WILL NEED TO BE RE-ADDED TO BE COMPLIANT WITH NEW KEY SYSTEM**
  - Keychain was heavily updated, old atlas keys will not work
- ATLAS DB
  - Moved atlas db names to app config file from node config file
  - Added support for the primary and secondary atlas db to use a different uri
- PYBIRDUI
  - added support to export specific app and session logs
- PYBIRDMgrUI
  - updated the twitter and atlas UI


### Version 0.8.7-PA
- **ALL PREVIOUSLY ADDED KEYS WILL NEED TO BE RE-ADDED TO BE COMPLIANT WITH NEW KEY SYSTEM**
- Added log length limitation
  - configured through pybird config
- Added support for generic key files
  - Must be named appName.keyIdentifier.GEN.txt to be used with the key upload system
  - the appName and keyIdentifier will be unique to each key
- Updated the .pybird structure
  - .pybird
    - .aes
    - .app
      - APPNAME
        - .atlas
        - .x
        - .general
- Added command to PYBIRDMgrUI.py to remove all keys for an app
- Added command to PYBIRDMgrUI.py to remove a specific key for an app
- Upgraded twitter key manager to be more compliant with new generic key system
- Updated TCS_variables.py to support new key system and provide paths based off of app names and key identifiers


### Version 0.8.6-PA
- moved session ID parameters to `TCS_variables.py`
- removed support for api v1.1
- changed EC2 platform code
  - `aws-ec2` --> `aws-ec2-linux2`
- added support for AWS-EC2 Amazon Linux 2023
  - Platform code - `aws-ec2-linux2023`
- Added Session Logging to Logs
- Fixed error in encryption and key storage
- fixed bootloader errors on AWS EC2
- Added options in config for what types of logs should be generated 
- cleaned up code across all files
- updated service for new naming scheme
- added log export functionality
  - Export Master Log
    - Will only export the master log
  - Export Session Log
    - Will only export session logs
  - Export App Log
    - Will only export app logs
  - Build Master Log From Session Logs
    -  Will take all the session logs and export as a single fill

### Version 0.8.3-Dev
- Optimized all imports
- cleaned up all files
- removed SDK, it was outdated by 6 major versions
- removed `$PYBIRD/server` dir, moved all items into `$PYBIRD/src`
- removed unused/old variables from `TCS_variables.py`
- removed mode functions from TCS_core
- added priority queue to datastructures
- moved watchdog to `$PYBIRD/src`


### Version 0.8.2-Dev
- added a naming scheme file
- Updated Naming Scheme
    - PYBIRD - Used for UI's and primary service
    - TAS - App Subsystem | Contains the user level framework/Plugins for using the PYBIRD system
    - TBS - Boot Subsystem | Used for running pybird on Boot
    - TCS - Core Subsystem | Contains the core PYBIRD framework. Includes:
        - > Configuration
        - > I/O Utilities
        - > Logging
        - > Core Framework
        - > Variables 
    - TDS - Data Subsystem | contains basic data structures and a way to save user data to memory
        - > MongoDB Atlas Support
        - > NVM Names based data storage (Data is not guarantied to transfer between instances)
    - TKS - Keychain Subsystem | Securely store keys/credentials separately from the Main PYBIRD Files
    - TNS - Node Subsystem | Used to build/run an instance of PYBIRD
    - TWM - Twitter Manager | Used to manage twitter
    - WDT - Watchdog | classes for managing the software watchdog

- added a standardized way to save and load keys from keychain
- fixed error in display logs for linux, used old log dir
- fixed bug in config file read error



### Version 0.8.1-Dev
- Cleaned up code and removed unused imports
- Improved Stability
    - Added error handling for invalid atlas credentials
    - added error handling for invalid myStart() methods
- added a way to upload atlas and twitter credentials
    - Setting in `PYBIRD_SERVER_CONFIG.toml`
    ```
    [system_config.credentials]
        delete_dir_after_upload=true # if true all setting below will be ignored, the entire directory will be deleted. Strongly recommended to increase security and prevent accidental overwrites

        delete_file_after_upload=true # it is strongly recommended that this is deleted after upload for security reasons 
    ```
    - to upload credential
        - create the directory `$PYBRID/add_cred`
        - to upload twitter credentials
            - create a file called `APPCODE.x.json` APPCODE should be replaced with the 4-6 char appcode
            ```
            {
                "APPCODE": {
                    "consumer_key": {
                        "api_key": "",
                        "api_secret": ""
                    },
                    "authentication_token": {
                        "bearer_token": "",
                        "access_token": "",
                        "access_token_secret": ""
                    },
                    "oAuth2":{
                        "client_id": "",
                        "client_secret": ""
                    }
                }
            }
            ```
            **IMPORTANT: If the APPCODE in the json file and the name of the file do not match it will not upload**
        - to upload atlas credentials
            - create a file called `APPCODE.atlas.json` APPCODE should be replaced with the 4-6 char appcode
            ```
            {
                "APPCODE": {
                    "uri":"",
                    "api_version":"",
                    "dedicated": {
                        "dedicated_allowed": true,
                        "dedicated_name": ""
                    },
                    "shared": {
                        "shared_allowed": true,
                        "shared_name": ""
                    }
                }
            }
            ```
            **IMPORTANT: If the APPCODE in the json file and the name of the file do not match it will not upload**
        - create as many files as needed to add all of your credentials PYBIRD can handle it
        - Run PYBIRDMgrUI.py and follow the prompts to upload all credentials
        
            
            



### Version 0.8-Dev
- logs are now stored in teh data dir and then exported for viewing
- logs are now in csv format
- added an export and clear log option to UI
- Added a Non-Volatile Memory option to save python object for future use
    - `self.data_interface` to use
- Added an example app to the `/src` dir
- added additional user input options to TCS_UIutils.py
- created a data structures file `TCS_dataStruct.py` which has a queue and stack implemented
- added sessions to system, allows for a common session ID to be displayed across multiple subprocesses
- added colored CLI to interface with predetermined colors for certain message types
- created a session and appdata dir under the data dir
    - used to store app data
- added a way to generate AES keys





### Version 0.5.2-Dev to 0.7-DEV

My bad forgot to document


### Version 0.5.1-Dev

- upgraded logging method parameter msgtype to logType
- added delimiter log method for multiline logging

### Version 0.5-Dev

- Changed root directory *.twitter* -> *.pybird*
- Upgraded log_db
    - if enables in apps .json config the database is automatically set to "log"
    - NOTE: The dedicated database must be enabled for the app. Contact Sales Rep to enable
- "TWIT" was replaced in all variables with "PYBIRD"
- Environment tags changed

    ````python
    PYBIRD_TAG = 'PYBIRD'
    PYBIRD_REMOTE_DIR_TAG = 'PYBIRDRemoteDir'
    PYBIRD_PLATFORM_TAG = 'PYBIRDPlatform'
    PYBIRD_PYTHON_TAG = 'PYBIRDPython'
    ````
- added an option to disable remote directories to the system config file
- Upgraded nodes
    - nodes now hav there own configuration .csv file.
    - node configuration moved from */config* -> */nodes*
    - node are now all controlled from a common file */src/TNS_node_instance.py*
- debug mode is now forced when test mode is enabled
- all version control removed from individual files, now located in *TCS_utils.py*
- added multiline logging
    - separates into lines based off of "\n" character
    - log_multiline(self, in_string:str, msgtype="msg"):
        - standard logging
    - dlog_multiline(self, in_string:str, msgtype="msg"):
        - debug logging
- upgraded interface so that it can be used outside of an app
- added shutdown methods

### Version 0.4.1-DEV

- Version is now controlled per file
- Added MongoDB Atlas Support
    - Keychain updated to support adding Atlas credentials to *~/.twitter/.atlas*
    - encryption support added for Atlas Credentials
    - Added dedicated date pool to apps (Using MongoDB)
        - create/access a collection with *collectionVariable = self.data_pool.get_collection("insert collection here")*
        - Standard MongoDB Collection operation can be used: [Tutorial](https://pymongo.readthedocs.io/en/stable/tutorial.html)
        - Database operations can be done by accessing *self._data_pool*
            - *self._data_pool.database_status* will return a dictionary with the database status
    - Added dedicated shared date pool to apps (Using MongoDB)
        - create/access a collection with *collectionVariable = self.shared_data_pool.get_collection("insert collection here")*
        - Standard MongoDB Collection operation can be used: [Tutorial](https://pymongo.readthedocs.io/en/stable/tutorial.html)
        - Database operations can be done by accessing *self._shared_data_pool*
            - *self._shared_data_pool.database_status* will return a dictionary with the database status
- Added Logging Method
    - ~~*log_db(database_collection, in_string, msgtype="msg")*~~ DEPRECATED



