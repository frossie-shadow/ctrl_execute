#!/usr/bin/env python

#
# LSST Data Management System
# Copyright 2008-2016 LSST Corporation.
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

import sys
from lsst.ctrl.execute.qCommand import QCommand

if __name__ == "__main__":
    platform = sys.argv[1]
    jobId = sys.argv[2]

    cmd = QCommand(platform)

    command = "%s %s@%s %s/qdel %s" % (cmd.remoteLoginCmd, cmd.userName, cmd.hostName, cmd.utilityPath, jobId)
    exitCode = cmd.runCommand(command)
    sys.exit(exitCode)
