# Highspot
Highspot code problem.

## App parameters

```highspot <input-file> <changes-file> <output-file>```

- input-file: See ```mixtape.json``` 

- changes-file: Changes to be merged into ```mixtape.json``` 

- output-file: The result of the merge will be written to this file. 

All 3 files are formatted as JSON.

## Using the app

### Install the app
This app uses Python 3.7.4. The installer script will use pyenv to install this version if it is not found.

```cd Highspot```

```install.sh```

### Run the app

```pyenv exec highspot <input-file> <changes-file> <output-file>```






