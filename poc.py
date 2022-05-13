from importlib.resources import path
import pathlib
import sys
import os

import toga
from toga.constants import COLUMN, ROW
from toga.style import Pack

import panel as pn

from streaming_tabulator import panel_app

_current_dir = os.path.dirname(os.path.realpath(__file__))

class PanelWebView(toga.App):

    current_zoom = 1.0

    icon_zoom_in = toga.icons.Icon(path=f"{_current_dir}/icons/ic_zoom_in_black_48dp.png")
    icon_zoom_out = toga.icons.Icon(path=f"{_current_dir}/icons/ic_zoom_out_black_48dp.png")
    icon_zoom_reset = toga.icons.Icon(path=f"{_current_dir}/icons/ic_aspect_ratio_black_48dp.png")
    icon_reload = toga.icons.Icon(path=f"{_current_dir}/icons/ic_refresh_black_48dp.png")

    def __init__(self, *args, panel_app):
        super().__init__(*args)

        self._apps = {':' : pathlib.Path(_current_dir) / pathlib.Path(panel_app)}

    def _show(self):
        print("show", flush=True)
        self.webview.url = f'http://localhost:{self.server.port}'

    async def _start_panel_app(self, widget, **kwargs):
        print("add panel app", flush=True)
        self.server = pn.serve(self._apps, port=0, show=False)
        self.server.io_loop.add_callback(self._show)
        
    
    def on_webview_load(self, _interface):
        print("on webview load")
        self.top_label.text = "www loaded!"


    def on_webview_button_press(self, _whatever, key, modifiers):
        print("on_webview_button_press", _whatever, key, modifiers)
        self.top_label.text = "got key={key} mod={modifiers}".format(
            key=key.value,
            modifiers=', '.join(m.value for m in modifiers)
        )

    def zoom_in(self, widget):
        self.current_zoom += 0.1
        self.webview.invoke_javascript(f"""document.body.style.zoom={self.current_zoom};this.blur();""")

    def zoom_out(self, widget):
        self.current_zoom -= 0.1
        self.webview.invoke_javascript(f"""document.body.style.zoom={self.current_zoom};this.blur();""")
    
    def zoom_reset(self, widget):
        self.current_zoom = 1.0
        self.webview.invoke_javascript(f"""document.body.style.zoom={self.current_zoom};this.blur();""")

    def reload(self, widget):
        self.current_zoom = 1.0
        self.webview.invoke_javascript(f"""window.location.reload();""")
        

    def startup(self):

        self.on_exit = self.on_exit_callback

        self.main_window = toga.MainWindow(title=self.name)
        self.top_label = toga.Label('www is loading |', style=Pack(flex=1, padding_left=10))
        self.add_background_task(self._start_panel_app)

        self.top_box = toga.Box(
            children=[
                self.top_label,
            ],
            style=Pack(flex=0, direction=ROW)
        )
        self.webview = toga.WebView(
            on_key_down=self.on_webview_button_press,
            on_webview_load=self.on_webview_load,
            style=Pack(flex=1)
        )

        box = toga.Box(
            children=[
                self.webview,
            ],
            style=Pack(flex=1, direction=COLUMN)
        )

        self.main_window.content = box

        menu_group_view = toga.Group('View')
       
        command_zoom_in = toga.Command(
            self.zoom_in,
            label='Zoom in',
            icon=self.icon_zoom_in,
            group=menu_group_view,
            order=1
        )
        command_zoom_out = toga.Command(
            self.zoom_out,
            label='Zoom out',
            icon=self.icon_zoom_out,
            group=menu_group_view,
            order=2
        )
        command_zoom_reset = toga.Command(
            self.zoom_reset,
            label='Reset zoom',
            tooltip='Resets zoom to its initial value',
            icon=self.icon_zoom_reset,
            group=menu_group_view,
            order=3
        )
        command_reload = toga.Command(
            self.reload,
            label="Reload",
            tooltip='Resets zoom to its initial value',
            icon=self.icon_reload,
            order=4
        )

        self.main_window.toolbar.add(
            command_zoom_in,
            command_zoom_out,
            command_zoom_reset,
            command_reload
        )

        self.main_window.show()

    
    def on_exit_callback(self, widget):
        self.main_window.confirm_dialog(title="Confirm", 
                                        message=f"Are you sure you want to close {self.app_name} ?",
                                        on_result=self.on_exit_confirm_callback)

    def on_exit_confirm_callback(self, widget, confirmed):
        
        if confirmed:
            self.server.io_loop.stop()
            self.server.stop()
            self._impl.exit()


def main( panel_app ):
    return PanelWebView('POC Toga with Panel', 'org.beeware.widgets.webview', "test", panel_app=panel_app)


if __name__ == '__main__':


    gui_app = main(sys.argv[1])
    gui_app.main_loop()
