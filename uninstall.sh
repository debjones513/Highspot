printf "\n *** Currently installed untilities *** \n"
pip3 freeze

printf "\n *** Uninstalling Highspot app *** \n"
pip3 uninstall highspot

printf "\n *** Currently installed untilities *** \n"
pip3 freeze
printf "\n The above output will be removed when the highspot project is removed.\n"

printf "\n *** Setting 'pyenv global system' *** \n"
pyenv global system

printf "\n *** Python versions currently installed *** \n"
pyenv versions

printf "\n *** Uninstalling Python 3.7.4 *** \n"
pyenv uninstall 3.7.4

printf "\n *** Python versions currently installed *** \n"
pyenv versions

printf "\n *** Uninstalling pyenv *** \n"
brew uninstall pyenv



