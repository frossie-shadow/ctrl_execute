#!/usr/bin/env python

# 
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
# 
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the LSST License Statement and 
# the GNU General Public License along with this program.  If not, 
# see <http://www.lsstcorp.org/LegalNotices/>.
#

from __future__ import with_statement
import re, sys, os, os.path, shutil, subprocess
import lsst.pex.config as pexConfig

class FakeTypeMap(dict):
   def __init__(self, configClass):
       self.configClass = configClass

   def __getitem__(self, k):
       return self.setdefault(k, self.configClass)

class UserInfoConfig(pexConfig.Config):
    name = pexConfig.Field("user name", str, default=None)
    home = pexConfig.Field("user home", str, default=None)

class UserConfig(pexConfig.Config):
    user = pexConfig.ConfigField("user", UserInfoConfig)

class CondorInfoConfig(pexConfig.Config):
    platform = pexConfig.ConfigChoiceField("platform info", FakeTypeMap(UserConfig))

if __name__ == "__main__":
    config = CondorInfoConfig()
    config.load("/lsst/home/srp/.lsst/condor-info.py")

    for i in config.platform.keys():
        print i
