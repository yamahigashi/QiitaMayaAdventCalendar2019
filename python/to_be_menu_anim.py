import qiita_adventcal_menu as menu


@menu.command_item("Synoptic")
def open_synoptic():
    from mgear import synoptic
    synoptic.open()


@menu.command_item("Studio Library")
def open_studiolibrary():
    import studiolibrary
    studiolibrary.main()


@menu.command_item("Mirror selected animation", divider="")
def mirror_selected_animation():
    pass


@menu.command_item("IK/FK Space Transfer")
def show_space_transfer():
    """$B8=:_3+$$$F$$$k%7!<%s$N%-%c%i%/%?$N%9%Z!<%9%H%i%s%9%U%!$rI=<($9$k!#(B"""
    pass


@menu.command_item("Edit export setting", divider="Export")
def edit_export_setting():
    """$B8=:_3+$$$F$$$k%7!<%s$N%(%/%9%]!<%H@_Dj$rJT=8$9$k!#(B"""
    pass


@menu.command_item("debug", folder="debug")
def debug():
    """$B8=:_3+$$$F$$$k%7!<%s$N%(%/%9%]!<%H@_Dj$rJT=8$9$k!#(B"""
    pass
