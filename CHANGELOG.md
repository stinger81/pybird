# PYBIRD

## Change Log

### Version 0.9.0-PA


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



