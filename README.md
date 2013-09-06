## Live Rsync BETA plugin for Sublime Text 3 (only)

This plugin was made because 2 weeks of painfull trying to launch lsyncd on Mac OS X.
Live Rsync uses 'rsync' command line application to synchronize with remote servers.

Just clone it in your Packages directory, edit your Project file with settings

For every folder in project you can set settings, and some part of this settings you can set global in RsyncHandler settings file.

```JSON
    {
        "folders":
        [
            {
                "follow_symlinks": true,
                "path": "/some/path",
                "live_rsync": {
                    //settings here
                }
            }
        ]
    }
```

### Settings
#### Destination
```JSON
    "destination" : "user@server:/path/to/upload",
```
Destination to sync. If you want to sync via ssh - add user name to login.

#### Exclude patterns
```JSON
    "exclude" : "*git*",
```
Exclude files, folders - just rsync exclude format.

#### Rsync Settings
```JSON
    "sync_settings" : "urvz",
```
Default is update, recursive, verbose and zip.

#### SSH
```JSON
    "ssh" : true,
```
Boolean flag, if true it will connect to remote server through ssh

#### Full update folder on sublime start / project change
```JSON
    "full_update_on_start" : true,
```
If set true - tries update folder on destination server when current Project changed to another and when Sublime starting.

### Commands
Available in "Go To Anywhere" prefixed "LiveRsync:"

#### Upload Current File
Uploads only one current file to destination of folder.

#### Upload Full Project
Uploads every folder of project with settings to this folder

#### Disable\Enable Auto-uploading
Stops\Starts auto uploading when file changes

#### Show latest logs
Here you can see debug information (updates automatically) about whats going on with your updates

When you save file, it'll uploads automatically (if setting turned on) and after upload finished you will see 'LR: Done.' in status bar of current View.