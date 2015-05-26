# lib/piservices/remote
----
## AbstractRemoteLoader
* service
* remote_file = None
### load
### prepare_content_for_write
### write
### backup_if_no_backup_exists

### RemoteConfigFileWithTemplate
* service
* template_file = None
* remote_file   = None
#### render
#### replace
#### load_template
### RemoteConfigFileWithPartial
* separator
#### clean
#### render


### AbstractRemoteConfigLoader
* service
* remote_file = None
#### create_config_object
#### set/unset/get/all

### RemoteConfigIniLoader
#### ConfigObj

### RemoteShellVarsLoader
#### ConfigObj + strip add quotes

### RemoteConfigParser
#### ConfigParser

### RemoteWhitespaceConfigLoader
#### WhitespaceConfigEditor

