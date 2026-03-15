#np = r"D:\Special_problems\tutorial2\Geo\model_geo.mb"
#gp = r"D:\Special_problems\tutorial2\Geo\guides_002.mb"


np = r"/run/media/collindv/KINGSTON/Special_problems/tutorial2/Geo/model_geo.mb"
gp = r"/run/media/collindv/KINGSTON/Special_problems/tutorial2/Geo/guides_002.mb"
import maya.cmds as cmds
import nmrig.build.buildPart as nmPart
from importlib import reload

reload(nmPart)

cmds.file(new=True, f=True)

root = nmPart.build_module(
    module_type='root',
    side='Cn',
    part='root',
    model_path=np,
    guide_path=gp
)

cmds.viewFit('perspShape', fitFactor=1, all=True, animate=True)

for s in ['Lf', 'Rt']:

    if s == 'Lf':
        fs = 'mixamorig:Left'
    else:
        fs = 'mixamorig:Right'

    arm = nmPart.build_module(
        module_type='bipedLimb',
        side=s,
        part='arm',
        guide_list=[
            fs + 'Arm',
            fs + 'ForeArm',
            fs + 'Hand'
        ],
        fk_shape='circle',
        gimbal_shape='gear_2D',
        offset_shape='circle',
        offset_pv=30,
        ctrl_scale=15
    )
    
for s in ['Lf', 'Rt']:

    if s == 'Lf':
        fs = 'mixamorig:Left'
    else:
        fs = 'mixamorig:Right'

    leg = nmPart.build_module(
        module_type='bipedLimb',
        side=s,
        part='leg',
        guide_list=[
            fs + 'UpLeg',
            fs + 'Leg',
            fs + 'Foot'
        ],
        fk_shape='circle',
        gimbal_shape='gear_2D',
        offset_shape='circle',
        offset_pv=30,
        ctrl_scale=15
    )