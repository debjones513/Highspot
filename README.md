# Highspot
Highspot code problem.

## App parameters

```highspot <input-file> <changes-file> <output-file>```

- input-file: The input file must contain the data in ```mixtape.json```. You may rename the file or copy the data
 to a new file if you'd like.

- changes-file: Changes to be applied to ```mixtape.json```. The format of this file is detailed below.

- output-file: The result of the changes to ```mixtape.json``` will be written to this file. 

All 3 files are formatted as JSON.

An empty input file is flagged as an error, since no operation can be performed, but we do copy the input file to 
the output file.

If the changes-file is empty, we just copy the input file to the output file and return success. 

**These cases would need more clarification for production code - if both are empty is this a success case? Is an empty
input file allowed? Is an empty changes file allowed?**

#### Changes-file format

The changes-file is JSON formatted and includes 3 sections: playlist_remove, playlist_add_song, user_add_playlist. 

- playlist_remove: An array of playlist ids. Value(s) correspond to an 'id' value in mixtape.json's 'playlists' section. 
In this example from mixtape.json, the playlist id is 1.
```  
"playlists" : [
    {
      "id" : "1",
      "user_id" : "2",
      "song_ids" : [
        "8",
        "32"
      ]
    },
]

``````

- playlist_add_song: An array of objects. Each object consists of a playlist_id, and a song_id. An entry in this 
section is a request to add the song represented by song_id to the playlist represented by playlist_id. Note that
a song may be added to a playlist multiple times - maybe it is a really good song...
In this example from mixtape.json, the song id is 1.

```  
"songs": [
    {
      "id" : "1",
      "artist": "Camila Cabello",
      "title": "Never Be the Same"
    },
```

- user_add_playlist: An array of objects. Each object consists of a user_id, and an array of song_id's. An entry in this 
section is a request to add a new playlist for the user represented by user_id. song_ids represents the songs to 
be added to the newly created playlist. 
In this example from mixtape.json, the user id is 1.
```
  "users" : [
    {
      "id" : "1",
      "name" : "Albin Jaye"
    },

```


##### Example changes-file
This project includes the ```mixtape-changes.json``` file. This file is included as an example of the 
changes-file format. The file name for the changes-file used with this app is defined by the user - use 
whatever changes-file name you'd like.

This example removes playlist 3, adds song 1 to playlist 1, and adds a new playlist for user 1. 
We have specified two songs for user 1's new playlist: song 1 and song 8.

```
{
  "playlist_remove" : [
    "3"
  ],
  "playlist_add_song" : [
    {
      "playlist_id" : "1",
      "song_id" : "1"
    }
  ],
  "user_add_playlist" : [
    {
      "user_id" : "1",
      "song_ids" : [
        "1",
        "8"
      ]
    }
  ]
}
```

## Install the app
This app uses Python 3.7.4. The installer script will install and use pyenv, to install Python version 3.7.4, 
if that Python version is not found.

```cd Highspot```

```install.sh```

## Run the app

```pyenv exec highspot <input-file> <changes-file> <output-file>```

## Uninstalling

!!! This script will undo all operations in the ```install.sh``` script !!!

If you are already using pyenv, or pyenv with Python 3.7.4, DO NOT RUN THIS SCRIPT.

```cd Highspot```

```uninstall.sh```

### To uninstall only the Highspot CLI
If you are already using pyenv, or pyenv with Python 3.7.4, you can run this script to uninstall only the Hihgspot app.

```cd Highspot```

```uninstall_app_only.sh```




