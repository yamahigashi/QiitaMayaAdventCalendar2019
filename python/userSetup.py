# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import inspect
from textwrap import dedent
import maya.cmds as cmds


def hoge():
    import maya.cmds as cmds
    import qiita_adventcal_menu as menu
    import to_be_menu_model as model
    import to_be_menu_anim as anim

    parent_menu = cmds.menu("qiita_adventcal_menu",
                            label="qiita 2019",
                            parent="MayaWindow",
                            tearOff=True
                            )

    menu.register_module_menu(model, "Modeling", parent_menu)
    menu.register_module_menu(anim, "Animation", parent_menu)


def __register_main_menu():
    cmds.evalDeferred(hoge)


if __name__ == '__main__':
    try:
        __register_main_menu()

    except Exception as e:
        # avoidng the "call userSetup.py chain" accidentally stop, all exception must collapse
        import traceback
        traceback.print_exc()
