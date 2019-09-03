# Highspot
Highspot code problem.

#### Validate Output
For this coding exercise, you can manually\visually validate output. For production code, 
this would need to be done programmatically, by comparing the changes file to the output - validate 
all changes are present. You could calc original file size, size of removes, size of data added and verify
resulting file size against calculated file size.

#### How to scale this application to handle very large input files and/or very large changes files
##### Scale problem 1
The app loads the files into memory, and memory is limited. For extremely large files, the data can be batched 
into memory using raw file reads if nothing else. This would require tracking which entries have been processed. Third 
party solutions exist for batching json, such as https://www.dataquest.io/blog/python-json-tutorial

##### Scale problem 2
The app first validates the changes file data by making a pass through both the mixtape.json file, 
and the changes-file. If this validation was deemed worth while when working with very large files, then the validation 
would need to be split up - for example load the user ids from mixtape.json and changes-file, and validate just 
the user ids. Then load the playlist ids from mixtape.json and changes-file and validate removes, etc. 
These operations will cost processing time...

##### Scale problem 3
Because the app loads the entire file into memory, it also writes the entire result in one shot. For extremely 
large files we would need to batch the output.  

playlistUpdates() would iterate over the playlists section in mixtape.json using batching. Removals are just a 
failure to write that playlist to the output file, and updates could be done by 
making the change in memory, then doing the write on a per-entry basis, or better, batching the updates and writes.
Batching is more efficient because it reduces disk accesses, cache entries, etc.

We make a call to sort the data we have in memory - that is still valid, still works, but should be considered when 
evaluating the runtime. Keeping things sorted, in general, is a good idea, because it adds order to the data rather 
than manipulating randomized data. It is a tool for optimizing runtimes.

userAddPlaylist() is just doing appends, so no memory pressure there, but the algorithm to get a new playlist id 
would have to change - if the file is extremely large, we don't necessarily want to load all playlists just 
to get a new id. One option would be tracking the holes, and highest id used so far in a look-aside list.

As called out in the code, playlistUpdates() uses a look-aside list to quickly determine if the entry from mixtape.json 
needs to be updated. This code re-uses a validation list. If we do need to update, the code walks all user_add_playlist
entries to find the update data. This becomes an n^2 algorithm if every entry in mixtape.json's playlists is being 
changed (where n is number of playlists). A log base 2 algorithm could be used with sorted data. If the 
file data is sorted, you could batching through both files in alpha-numeric order, then the look up in changes-file
is no longer n operations, but 'entries in the batch' operations.

I will stop here due to time constaints - interesting problem...

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

**Should non-existant playlist ids be skipped and warned? Should this be checked up front and no processing 
one in this case since it indicates inconsistency in the meta-data?**

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

**Same as above, how should inconsistencies be handled?**

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

**If a song is missing from mixtape.json do we continue and warn? Fail?**

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




