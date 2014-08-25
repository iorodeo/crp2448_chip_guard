from __future__ import print_function
import os 
import sys
import dxfgrabber
from py2gcode import gcode_cmd
from py2gcode import cnc_dxf

side = sys.argv[1]
if not side in ('left','right'):
    raise ValueError, 'side must be either left or right'
fileName = 'crp2448_chip_guard_{0}.dxf'.format(side)

feedrate = 25.0

dwg = dxfgrabber.readfile(fileName)
layerNames = [layer.name for layer in dwg.layers]
layerNames = [name for name in layerNames if 'tap_hole_6-32' in name]
#layerNames = ['guard_tap_hole_6-32', 'adapter_tap_hole_6-32']

prog = gcode_cmd.GCodeProg()
prog.add(gcode_cmd.GenericStart())
prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.FeedRate(feedrate))

param = { 
        'dwg'         : dwg,
        'layers'      : layerNames,
        'dxfTypes'    : ['CIRCLE'],
        'startZ'      : 0.00,
        'stopZ'       : -0.27,
        'safeZ'       : 0.3,
        'stepZ'       : 0.03,
        'startDwell'  : 2.0,
        }
drill = cnc_dxf.DxfDrill(param)
prog.add(drill)

prog.add(gcode_cmd.Space())
prog.add(gcode_cmd.End(),comment=True)
baseName, dummy = os.path.splitext(__file__)
fileName = '{0}_{1}.ngc'.format(baseName,side)
print('generating: {0}'.format(fileName))
prog.write(fileName)
