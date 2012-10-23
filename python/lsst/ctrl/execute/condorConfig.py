#!/usr/bin/env python

# 
# LSST Data Management System
# Copyright 2008-2012 LSST Corporation.
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

import lsst.pex.config as pexConfig

class PlatformConfig(pexConfig.Config):
    """Platform specific information
    defaultRoot - the remote directory where orca jobs are executed.
    localScratch - local directory where Condor stores files
    idsPerJob - the number of ids to execute, per job. 
    dataDirectory - remote directory where data that jobs will use is kept.
    fileSystemDomain - network domain name of remote system.
    eupsPath - location of remote EUPS stack.
    """
    defaultRoot = pexConfig.Field("default root working for directories",str, default=None) 
    localScratch = pexConfig.Field("local scratch directory",str, default=None) 
    idsPerJob = pexConfig.Field("ids per job",int, default=1)
    dataDirectory = pexConfig.Field("data directory", str, default=None)
    fileSystemDomain = pexConfig.Field("filesystem domain", str, default=None)
    eupsPath = pexConfig.Field("eups path", str, default=None)

class CondorConfig(pexConfig.Config):
    """A pex_config file describing the platform specific information required
    to fill out templates for running ctrl_orca jobs
    """
    platform = pexConfig.ConfigField("platform configuration", PlatformConfig)

class FakeTypeMap(dict):
   def __init__(self, configClass):
       self.configClass = configClass

   def __getitem__(self, k):
       return self.setdefault(k, self.configClass)