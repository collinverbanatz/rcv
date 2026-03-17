import maya.cmds as cmds

import nmrig.build.rigModule as nmModule
import nmrig.build.chain as nmChain
import nmrig.build.fk as nmFk
import nmrig.libs.attribute as nmAttr

class FkChain(nmModule.RigModule, nmFk.FK):
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 gimbal=None,
                 offset=None,
                 pad='auto',
                 ctrl_scale=1,
                 remove_last=True,
                 fk_shape='circle',
                 gimbal_shape='circle',
                 offset_shape='square',
                 model_path=None,
                 guide_path=None):
        
        self.__dict__.update(locals())

        if self.pad == 'auto':
            self.pad = len(str(len(self.guide_list))) + 1

        super().__init__(
            side=side,
            part=part,
            guide_list=guide_list,
            ctrl_scale=ctrl_scale,
            model_path=model_path,
            guide_path=guide_path
        )

        # self.__dict__.update(locals())

        # if self.pad == 'auto':
        #     self.pad = len(str(len(self.guide_list))) + 1

        self.create_module()


    def create_module(self):
        print("Creating FK Chain Module")
        super(FkChain, self).create_module()
        print("Module created, building rig")
        self.control_rig()
        print("Control rig built, building output rig")
        self.output_rig()
        print("Output rig built, building skeleton")
        self.skeleton()
        #self.add_plugs()
        print("part_grp:", self.part_grp, type(self.part_grp), cmds.objExists(self.part_grp))


    def control_rig(self):
        self.build_fk_controls()
        cmds.parent(self.fk_ctrls[0].top, self.control_grp)

    def output_rig(self):
        self.build_fk_chain()
        cmds.parent(self.fk_joints[0], self.module_grp)

    def skeleton(self):
        fk_chain = nmChain.Chain(transform_list=self.fk_joints,
                                 prefix=self.side,
                                 suffix='JNT',
                                 name=self.part)
        fk_chain.create_from_transforms(parent=self.skel)

        if self.remove_last:
            cmds.delete(self.fk_ctrls[-1].top)
            self.bind_joints = fk_chain.joints[:-1]

        else:
            self.bind_joints = fk_chain.joints

        self.tag_bind_joints(self.bind_joints)


    def add_plugs(self):

        nmAttr.Attribute(node=self.part_grp, type='plug',
                         value=['add fk plug here'], name='skeletonPlugs',
                         children_name=[self.bind_joints[0]])

    