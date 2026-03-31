import maya.cmds as cmds
import nmrig.build.buildPart as nmPart
from importlib import reload
import nmrig.libs.ng as ng
from pathlib import Path
import nmrig.libs.skin as nmSkin
import json as json
import nmrig.libs.file as nmFile
import nmrig.build.ik as nmIk
reload(nmIk)

reload(nmPart)
reload(nmSkin)
reload(ng)
reload(nmFile)

def build():
    np = r"/run/media/collindv/KINGSTON/Special_problems/tutorial2/Geo/model_geo.mb"
    gp = r"/run/media/collindv/KINGSTON/Special_problems/tutorial2/Geo/guides_002.mb"
    sw = Path(
        "/run/media/collindv/KINGSTON/Special_problems/tutorial2/Geo/ninja_skin_005.json"
    )

    # windows
    # np = r"D:\Special_problems\tutorial2\Geo\model_geo.mb"
    # gp = r"D:\Special_problems\tutorial2\Geo\guides_002.mb"
    # sw = Path(r"D:\Special_problems\tutorial2\Geo\ninja_skin_005.json")

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


    # apply skin tools to the legs and arms
    with open(sw, "r") as f:
        data = json.load(f)

    print("Top level keys:", data.keys())
    print("Influences raw:", data.get("influences"))
    print("Type of influences:", type(data.get("influences")))


    joint_list = ng.get_influences_from_ng_json(sw)

    if not cmds.ls(cmds.listHistory('Body_GEO'), type='skinCluster'):
        print("Joint list:", joint_list)
        print("Joint count:", len(joint_list))
        print("Body exists:", cmds.objExists("Body_GEO"))
        nmSkin.skin_mesh(bind_joints=joint_list, geometry="Body_GEO", name=None, dual_quaternion=True)
        print("Skin cluster created.")
    
    ng.apply_ng_skin_weights(sw, "Body_GEO")
    print("Weights applied from ngSkinTools JSON.")

    ng.cleanup_ng_data_nodes()
