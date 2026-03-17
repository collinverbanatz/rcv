import maya.cmds as cmds

import nmrig.build.parts.root as nmRoot
import nmrig.build.parts.bipedLimb as nmLimb
import nmrig.libs.attribute as nmAttr
from importlib import reload
reload(nmRoot)
reload(nmLimb)

reload(nmAttr)

MODULE_DICT = {'root': nmRoot.Root,
               'bipedLimb': nmLimb.BipedLimb,
                }


def build_module(module_type, **kwargs):
    module = MODULE_DICT[module_type](**kwargs)
    module.create_module()

    nmAttr.Attribute(node=module.part_grp, type='string', name='moduleType',
                     value=module_type, lock=True)

    cmds.refresh()
    return module
