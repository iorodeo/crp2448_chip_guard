from __future__ import print_function
import os 
import sys
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

side = sys.argv[1]
if not side in ('left','right'):
    raise ValueError, 'side must be either left or right'
fileName = 'crp2448_chip_guard_{0}.dxf'.format(side)

feedrate = 120.0
thruDepth = 0.27
magnetDepth = 0.0625
startZ = 0.0
safeZ = 0.3
toolDiam = 0.375 
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
layerNames = ['guard_clearance_hole']
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

# Boundaries
prog.add(gcode_cmd.PathBlendMode(P=0.01))
layerNames = ['guard_boundary', 'mount_boundary', 'adapter_boundary']
param = {
        'fileName'    : fileName,
        'layers'      : layerNames,
        'depth'       : thruDepth,
        'startZ'      : startZ,
        'safeZ'       : safeZ,
        'toolDiam'    : toolDiam,
        'direction'   : direction,
        'cutterComp'  : 'outside',
        'maxCutDepth' : maxCutDepth,
        'startDwell'  : startDwell,
        'startCond'   : 'minX',
        'maxArcLen'   : 3.0e-2, 
        'ptEquivTol'  : 1.0e-5,
        }
boundary = cnc_dxf.DxfBoundary(param)
prog.add(boundary)
prog.add(gcode_cmd.ExactPathMode())

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, dummy = os.path.splitext(__file__)
fileName = '{0}_{1}.ngc'.format(baseName,side)
print('generating: {0}'.format(fileName))
prog.write(fileName)
