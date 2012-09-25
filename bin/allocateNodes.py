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
import optparse, traceback, time
import lsst.pex.config as pexConfig
from lsst.ctrl.execute.Allocator import Allocator
from lsst.ctrl.execute.AllocatorParser import AllocatorParser
from string import Template
import eups

def main():
    p = AllocatorParser(sys.argv)
    platform = p.getPlatform()

    creator = Allocator(platform, p.getOpts())

    platformPkgDir = eups.productDir("ctrl_platform_"+platform)
    if platformPkgDir is not None:
        configName = os.path.join(platformPkgDir, "etc", "config", "pbsConfig.py")
    else:
        raise RuntimeError("ctrl_platform_%s was not found.  Is it setup?" % platform)
    

    if creator.load(configName) == False:
        raise RuntimeError("Couldn't find pbs config file for platform: %s" % platform)

    
    pbsName = os.path.join(platformPkgDir, "etc", "templates", "generic.pbs.template")
    generatedPBSFile = creator.createPBSFile(pbsName)

    condorFile = os.path.join(platformPkgDir, "etc", "templates", "glidein_condor_config.template")
    generatedCondorConfigFile = creator.createCondorConfigFile(condorFile)

    scratchDirParam = creator.getScratchDirectory()
    template = Template(scratchDirParam)
    scratchDir = template.substitute(USER_HOME=creator.getUserHome())
    
    hostName = creator.getHostName()

    utilityPath = creator.getUtilityPath()

    cmd = "gsiscp %s %s:%s/%s" % (generatedPBSFile, hostName, scratchDir, os.path.basename(generatedPBSFile))
    runCommand(cmd)

    cmd = "gsiscp %s %s:%s/%s" % (generatedCondorConfigFile, hostName, scratchDir, os.path.basename(generatedCondorConfigFile))
    runCommand(cmd)

    cmd = "gsissh %s %s/qsub %s/%s" % (hostName, utilityPath, scratchDir, os.path.basename(generatedPBSFile))
    runCommand(cmd)

    print "Node set name:"
    print creator.getNodeSetName()

def runCommand(cmd):
    print cmd
    cmd_split = cmd.split()
    pid = os.fork()
    if not pid:
#        sys.stdin.close()
#        sys.stdout.close()
#        sys.stderr.close()
#            os.close(0)
#            os.close(1)
#            os.close(2)
        os.execvp(cmd_split[0], cmd_split)
    os.wait()[0]

if __name__ == "__main__":
    main()