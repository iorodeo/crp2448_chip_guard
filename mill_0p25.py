from __future__ import print_function
import os 
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

fileName = 'crp2448_chip_guard.dxf'

feedrate = 120.0
thruDepth = 0.27
magnetDepth = 0.0625
startZ = 0.0
safeZ = 0.3
toolDiam = 0.25 
overlap = 0.5
overlapFinish = 0.6
maxCutDepth = 0.04
direction = 'ccw'
startDwell = 0.5

prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.FeedRate(feedrate))

# Cut through holes
layerNames = ['mount_carriage_thru_hole', 'mount_magnet_thru_hole']
param = {
        'fileName'     : fileName,
        'layers'       : layerNames, 
        'depth'        : thruDepth,
        'startZ'       : startZ,
        'safeZ'        : safeZ,
        'toolDiam'     : toolDiam,
        'toolOffset'   : 'inside',
        'direction'    : direction,
        'maxCutDepth'  : maxCutDepth,
        'startDwell'   : startDwell,
        }
boundary = cnc_dxf.DxfCircBoundary(param)
prog.add(boundary)

# Mill magnet pocket
layerNames = ['adapter_magnet_pocket_hole']
param = {
        'fileName'       : fileName,
        'layers'         : layerNames,
        'depth'          : magnetDepth,
        'startZ'         : startZ,
        'safeZ'          : safeZ,
        'overlap'        : overlap,
        'overlapFinish'  : overlapFinish,
        'maxCutDepth'    : maxCutDepth,
        'toolDiam'       : toolDiam,
        'direction'      : direction,
        'startDwell'     : startDwell,
        }
pocket = cnc_dxf.DxfCircPocket(param)
prog.add(pocket)

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, dummy = os.path.splitext(__file__)
fileName = '{0}.ngc'.format(baseName)
print('generating: {0}'.format(fileName))
prog.write(fileName)
