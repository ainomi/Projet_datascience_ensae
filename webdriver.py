#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb
sudo apt-get update
sudo -E apt-get install -y /tmp/chrome.deb
pip install chromedriver-autoinstaller selenium

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()