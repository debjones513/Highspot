printf "\n *** Installing pyenv *** \n"
brew install pyenv

printf "\n *** Installing Python 3.7.4 *** \n"
pyenv install -s 3.7.4

printf "\n *** Setting 'pyenv global 3.7.4' *** \n"
pyenv global 3.7.4

printf "\n *** Python versions currently installed *** \n"
pyenv versions

printf "\n *** Installing Highspot utility *** \n"
pip3 install -e .