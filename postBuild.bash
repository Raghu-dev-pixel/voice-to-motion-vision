#!/bin/bash
# This file contains bash commands that will be executed at the end of the container build process,
# after all system packages and programming language specific package have been installed.
#
# Note: This file may be removed if you don't need to use it

#upgrade pip installer
python -m pip install --upgrade pip

#Install transformers
pip install transformers

#upgrade jupyter notepad
pip install --upgrade jupyter ipywidgets
jupyter nbextension enable --py widgetsnbextension

#Install torch
pip install torch torchvision torchaudio