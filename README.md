# Administration Server CLI

##Presentation
Admin server CLI is a custom Python package which provides simple clients to interact
with the administration server.

The package provides 2 CLIs:
+ asconf: this client provides commands to configure the client environment information.
+ asdm: this client provides commands to list, create and delete deployment markers.
+ aspb: this client can be used to create, list and delete performance baseline.

##Installation
To install the package, run:
```aidl
pip install railai-admin-server-cli --extra-index-url http://10.62.65.209:4040/railai/dev --trusted-host 10.62.65.209
```

##Configuration
Before using the CLIs, configure the url of the admin server you want to 
interact with:
```aidl
asconf url admin-server.isus.emc.com
```

The configuration is stored in a yaml file in your home folder. 

The default file name is '.railai-admin-server.yml'. The configuration file name can be configured using
the environment variable ADMIN_SERVER_CONFIG_FILE_PATH. 
For instance:
```aidl
ADMIN_SERVER_CONFIG_FILE_PATH=my-file.yml
```
would store the configuration in a file called my-file.yml under your home folder.

The home folder is not configurable.

#Documentation
To get more information about the CLIs and their respective commands, use the help command:
```aidl
asconf --help
asdm --help
aspb --help
```