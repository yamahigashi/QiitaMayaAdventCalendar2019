# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import inspect
import functools
from textwrap import dedent

import maya.cmds as cmds

from logging import getLogger, WARN, DEBUG, INFO, StreamHandler  # NOQA


if False:
    # For type annotation
    from typing import Module, Optional, Dict, List, Tuple, Pattern, Callable, Any, Text, cast, TYPE_CHECKING  # type: ignore  # NOQA
    unicode = Text
# ----------------------------------------------------------------------------
handler = StreamHandler()
handler.setLevel(DEBUG)

logger = getLogger(__name__)
logger.setLevel(DEBUG)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False

# ----------------------------------------------------------------------------

__all__ = [

    "command_item",

    "register_module_menu",
    "deregister_module_menu",

]


class GmlCommandMenu(object):
    """Base class that represents a command menu item."""
    pass


'''  for reference purpose
def command_item(label, folder=None, divider=None):
    # type: (Text, Optional[Text], Optional[Text]) -> Callable
    """Decorator that converts a function into Maya command menu."""

    def decorator(func):

        @functools.wraps(func)
        def wrap(*args, **kwargs):
            return func()

        # these lines are sample for using not wrapped function but using class prototyping.
        CommandMenu = type(
            'GmlCommandMenuItem',
            (GmlCommandMenu,),
            {'__doc__': func.__doc__}
        )

        CommandMenu.__name__ = func.__name__
        CommandMenu.__module__ = func.__module__
        CommandMenu.__call__ = staticmethod(func)
        setattr(CommandMenu, "linenumber", inspect.getsourcelines(func)[1])
        setattr(CommandMenu, "folder", folder)
        setattr(CommandMenu, "label", label)
        setattr(CommandMenu, "divider", divider)

        return CommandMenu()

    return decorator
'''


# ----------------------------------------------------------------------------
# decorators
# ----------------------------------------------------------------------------
def command_item(label, folder=None, divider=None):
    # type: (Text, Optional[Text], Optional[Text]) -> Callable
    """Decorator that converts a function into Maya command menu."""

    def decorator(func):

        @functools.wraps(func)
        def wrap(*args, **kwargs):
            return func()

        setattr(wrap, "linenumber", inspect.getsourcelines(func)[1])
        setattr(wrap, "folder", folder)
        setattr(wrap, "label", label)
        setattr(wrap, "divider", divider)
        setattr(wrap, "is_maya_menu_item", True)
        return wrap

    return decorator


# ----------------------------------------------------------------------------
# exported functions
# ----------------------------------------------------------------------------
def get_folder_name_for_module(module):
    # type: (Module) -> Text
    package_path = module.__name__
    safe_package_name = package_path.replace(".", "_")

    return safe_package_name


def register_module_menu(module, menu_label, parent_menu_name):
    # type: (Module, Text, Text) -> None  # noqa

    package_path = module.__name__
    safe_package_name = get_folder_name_for_module(module)

    folder = cmds.menuItem(
        safe_package_name,
        label=menu_label,
        subMenu=True,
        tearOff=True,
        parent=parent_menu_name
    )

    members = [o for o in inspect.getmembers(module, inspect.isfunction) if _is_menu_item(o[1])]
    for klass_info in inspect.getmembers(module, inspect.isclass):
        logger.debug(klass_info)
        if not klass_info[1].__module__ == module.__name__:
            continue

        for method in inspect.getmembers(klass_info[1], inspect.ismethod):
            logger.debug(method)
            if _is_menu_item(method[1]):
                members.append(method)

    members.sort(key=_linenumber)

    for func in members:
        parent = folder

        func_name = func[0]
        label = func[1].label
        sub_folder_label = func[1].folder
        divider = func[1].divider
        annotation = _get_annotation(func[1])

        if sub_folder_label:
            sub_folder_name = sub_folder_label.replace(" ", "_").replace("-", "_")
            sub_folder_name = "{}_{}".format(safe_package_name, sub_folder_name)
            exists = cmds.menuItem(sub_folder_name, exists=True)

            if exists:
                parent = sub_folder_name

            else:
                parent = cmds.menuItem(
                    sub_folder_name,
                    label=sub_folder_label,
                    subMenu=True,
                    tearOff=True,
                    parent=folder
                )

        if isinstance(divider, str) or isinstance(divider, unicode):
            cmds.menuItem(
                dividerLabel=divider,
                parent=parent,
                divider=True
            )

        cmds.menuItem(
            "{}_{}".format(package_path, func_name),
            label=label,
            parent=parent,
            echoCommand=True,
            annotation=annotation,
            command=func[1],
        )


def deregister_module_menu(module):
    # type: (Module) -> None  # noqa

    safe_package_name = module.__package__.replace(".", "_")
    members = [o for o in inspect.getmembers(module) if isinstance(o[1], GmlCommandMenu)]

    for func in members:
        func_name = func[0]
        try:
            item_name = "{}_{}".format(safe_package_name, func_name)
            cmds.deleteUI(item_name, menuItem=True)
        except RuntimeError:
            logger.error("menu item: {} can not delete".format(item_name))

    try:
        cmds.deleteUI("{}".format(safe_package_name), menuItem=True)
    except RuntimeError:
        logger.error("menu folder: {} can not delete".format(safe_package_name))


# ----------------------------------------------------------------------------
# Internal functions
# ----------------------------------------------------------------------------
def _linenumber(m):
    try:
        return m[1].linenumber
    except AttributeError:
        return 999999


def _generate_invoked_code(package_path, func_name):
    return dedent("""
        import {} as x
        x.{}()
    """.format(package_path, func_name))


def _is_menu_item(item):
    # type: (Any) -> bool
    try:
        return hasattr(item, "is_maya_menu_item")
    except AttributeError:
        return False

    # return isinstance(item, GmlCommandMenu)


def _get_annotation(func):
    # type: (Callable) -> Text
    doc = func.__doc__
    if not doc:
        return ""

    doc = dedent(doc)
    lines = [x.strip() for x in doc.splitlines(True)]
    doc = "".join(lines)

    return doc
