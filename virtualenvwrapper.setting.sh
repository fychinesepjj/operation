#!/bin/bash

if [ `id -u` != '0' ]; then
    PROJECT_PATH=/var/app
    WORKON_HOME=$PROJECT_PATH/virtualenvs
    if [ ! -d "$PROJECT_PATH" ];then
        sudo mkdir -p $PROJECT_PATH
        sudo chmod 777 $PROJECT_PATH
        echo "Create $PROJECT_PATH"
    elif [ ! -d "$WORKON_HOME" ];then
        sudo mkdir -p $WORKON_HOME
        sudo chmod 777 $WORKON_HOME
        echo "Create $WORKON_HOME"
    else
        echo "$PROJECT_PATH, $WORKON_HOME OK."
    fi

    export VIRTUALENV_USE_DISTRIBUTE=1
    export WORKON_HOME
    source /usr/local/bin/virtualenvwrapper.sh
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
    export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
    export PIP_VIRTUALENV_BASE=$WORKON_HOME
    export PIP_RESPECT_VIRTUALENV=true

fi