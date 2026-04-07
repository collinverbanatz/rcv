import maya.cmds as cmds
import nmrig.build.buildPart as nmPart
from importlib import reload
import nmrig.libs.ng as ng
from pathlib import Path
import nmrig.libs.skin as nmSkin
import json as json
import nmrig.build.parts.fkChain as nmFkChain
import nmrig.build.parts.ikChain as nmIkChain

reload(nmPart)
reload(nmSkin)
reload(ng)
reload(nmFkChain)
reload(nmIkChain)

def build():
    np = r"/run/media/collindv/KINGSTON/Special_problems/tutorial2/Geo/samurai_002.mb"
    gp = r"/run/media/collindv/KINGSTON/Special_problems/tutorial2/Geo/samurai_guides_004.mb"
    sw = Path(
        "/run/media/collindv/KINGSTON/Special_problems/tutorial2/Geo/samurai_skin_004.json"
    )
    clothes = Path(
        "/run/media/collindv/KINGSTON/Special_problems/tutorial2/Geo/samurai_skin_clothes_001.json"
    )

    #windows
    # np = r"D:\Special_problems\tutorial2\Geo\samurai_002.mb"
    # gp = r"D:\Special_problems\tutorial2\Geo\samurai_guides_004.mb"
    # sw = Path(r"D:\Special_problems\tutorial2\Geo\samurai_skin_003.json")
    # clothes = Path(r"D:\Special_problems\tutorial2\Geo\samurai_skin_clothes_001.json")


    cmds.file(new=True, f=True)

    root = nmPart.build_module(
        module_type='root',
        side='Cn',
        part='root',
        model_path=np,
        guide_path=gp
    )

    cmds.viewFit('perspShape', fitFactor=1, all=True, animate=True)

    # create hips
    hips = nmFkChain.FkChain(
        side="Cn",
        part="hips",
        guide_list=["Hips"],
        gimbal=True,
        offset=True,
        pad="auto",
        ctrl_scale=1,
        remove_last=True,
        fk_shape="circle",
        gimbal_shape="circle",
        offset_shape="circle",
        model_path=None,
        guide_path=None,
    )

    # create shoulders
    LeftShoulder = nmFkChain.FkChain(
        side="Lf",
        part="shoulder",
        guide_list=["LeftShoulder"],
        gimbal=True,
        offset=True,
        pad="auto",
        ctrl_scale=1,
        remove_last=True,
        fk_shape="circle",
        gimbal_shape="circle",
        offset_shape="circle",
        model_path=None,
        guide_path=None,
    )
    RightShoulder = nmFkChain.FkChain(
        side="Rt",
        part="shoulder",
        guide_list=["RightShoulder"],
        gimbal=True,
        offset=True,
        pad="auto",
        ctrl_scale=1,
        remove_last=True,
        fk_shape="circle",
        gimbal_shape="circle",
        offset_shape="circle",
        model_path=None,
        guide_path=None,
    )
    # create spine
    spine = nmFkChain.FkChain(
        side="Cn",
        part="spine",
        guide_list=["Spine", "Spine1", "Spine2"],
        gimbal=True,
        offset=True,
        pad="auto",
        ctrl_scale=1,
        remove_last=False,
        fk_shape="circle",
        gimbal_shape="circle",
        offset_shape="circle",
        model_path=None,
        guide_path=None,
    )

    # create head
    head = nmFkChain.FkChain(
        side="Cn",
        part="head",
        guide_list=["Neck", "Head", "HeadTop_End"],
        gimbal=True,
        offset=True,
        pad="auto",
        ctrl_scale=1,
        remove_last=True,
        fk_shape="circle",
        gimbal_shape="circle",
        offset_shape="circle",
        model_path=None,
        guide_path=None,
    )

    for s in ['Lf', 'Rt']:

        if s == 'Lf':
            fs = 'Left'
            left_arm = nmPart.build_module(
                module_type="bipedLimb",
                side=s,
                part="arm",
                guide_list=[fs + "Arm", fs + "ForeArm", fs + "Hand"],
                fk_shape="circle",
                gimbal_shape="gear_2D",
                offset_shape="circle",
                offset_pv=30,
                ctrl_scale=15,
            )
        else:
            fs = 'Right'
            right_arm = nmPart.build_module(
                module_type="bipedLimb",
                side=s,
                part="arm",
                guide_list=[fs + "Arm", fs + "ForeArm", fs + "Hand"],
                fk_shape="circle",
                gimbal_shape="gear_2D",
                offset_shape="circle",
                offset_pv=30,
                ctrl_scale=15,
            )

        # arm = nmPart.build_module(
        #     module_type='bipedLimb',
        #     side=s,
        #     part='arm',
        #     guide_list=[
        #         fs + 'Arm',
        #         fs + 'ForeArm',
        #         fs + 'Hand'
        #     ],
        #     fk_shape='circle',
        #     gimbal_shape='gear_2D',
        #     offset_shape='circle',
        #     offset_pv=30,
        #     ctrl_scale=15
        # )

    for s in ['Lf', 'Rt']:

        if s == 'Lf':
            fs = 'Left'
            left_leg = nmPart.build_module(
                module_type="bipedLimb",
                side=s,
                part="leg",
                guide_list=[fs + "UpLeg", fs + "Leg", fs + "Foot"],
                fk_shape="circle",
                gimbal_shape="gear_2D",
                offset_shape="circle",
                offset_pv=30,
                ctrl_scale=15,
            )
        else:
            fs = 'Right'
            right_leg = nmPart.build_module(
                module_type="bipedLimb",
                side=s,
                part="leg",
                guide_list=[fs + "UpLeg", fs + "Leg", fs + "Foot"],
                fk_shape="circle",
                gimbal_shape="gear_2D",
                offset_shape="circle",
                offset_pv=30,
                ctrl_scale=15,
            )

        # leg = nmPart.build_module(
        #     module_type='bipedLimb',
        #     side=s,
        #     part='leg',
        #     guide_list=[
        #         fs + 'UpLeg',
        #         fs + 'Leg',
        #         fs + 'Foot'
        #     ],
        #     fk_shape='circle',
        #     gimbal_shape='gear_2D',
        #     offset_shape='circle',
        #     offset_pv=30,
        #     ctrl_scale=15
        # )

    # parent joints
    cmds.parent("Cn_hips_01_JNT", "Cn_root_JNT")
    cmds.parent("Cn_spine_01_JNT", "Cn_hips_01_JNT")
    cmds.parent("Cn_head_01_JNT", "Cn_spine_01_JNT")
    cmds.parent("Lf_shoulder_01_JNT", "Cn_spine_03_JNT")
    cmds.parent("Rt_shoulder_01_JNT", "Cn_spine_03_JNT")
    cmds.parent("Lf_arm_01_JNT", "Lf_shoulder_01_JNT")
    cmds.parent("Rt_arm_01_JNT", "Rt_shoulder_01_JNT")
    cmds.parent("Lf_leg_01_JNT", "Cn_hips_01_JNT")
    cmds.parent("Rt_leg_01_JNT", "Cn_hips_01_JNT")

    # parent contros
    cmds.parent("Lf_shoulder", "Cn_spine_03_offset_CTRL")
    cmds.parent("Rt_shoulder", "Cn_spine_03_offset_CTRL")
    cmds.parent("Lf_arm", "Lf_shoulder_01_fk_JNT")
    cmds.parent("Rt_arm", "Rt_shoulder_01_fk_JNT")
    cmds.parent("Cn_head", "Cn_spine_03_offset_CTRL")
    cmds.parent("Cn_hips", "Cn_root_02_CTRL")
    cmds.parent("Cn_spine", "Cn_hips_01_fk_JNT")
    cmds.parent("Lf_leg", "Cn_hips_01_fk_JNT")
    cmds.parent("Rt_leg", "Cn_hips_01_fk_JNT")

    # apply skin tools to the legs and arms
    with open(sw, "r") as f:
        data = json.load(f)

    print("Top level keys:", data.keys())
    print("Influences raw:", data.get("influences"))
    print("Type of influences:", type(data.get("influences")))


    joint_list = ng.get_influences_from_ng_json(sw)
    joint_list_clothes = ng.get_influences_from_ng_json(clothes)

    if not cmds.ls(cmds.listHistory('samurai'), type='skinCluster'):
        print("Joint list:", joint_list)
        print("Joint count:", len(joint_list))
        print("Body exists:", cmds.objExists("samurai"))
        nmSkin.skin_mesh(bind_joints=joint_list, geometry="samurai", name=None, dual_quaternion=True)
        print("Skin cluster created.")

    if not cmds.ls(cmds.listHistory('pasted__hakama3'), type='skinCluster'):
        nmSkin.skin_mesh(bind_joints=joint_list_clothes, geometry="pasted__hakama3", name=None, dual_quaternion=True)

    
    ng.apply_ng_skin_weights(sw, "samurai")
    ng.apply_ng_skin_weights(clothes, "pasted__hakama3")
    print("Weights applied from ngSkinTools JSON.")

    ng.cleanup_ng_data_nodes()
