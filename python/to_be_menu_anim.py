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
    """現在開いているシーンのキャラクタのスペーストランスファを表示する。"""
    pass


@menu.command_item("Edit export setting", divider="Export")
def edit_export_setting():
    """現在開いているシーンのエクスポート設定を編集する。"""
    pass


@menu.command_item("debug", folder="debug")
def debug():
    """現在開いているシーンのエクスポート設定を編集する。"""
    pass
