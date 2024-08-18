import flet as ft
from telethon import TelegramClient
from test import api_id, api_hash, phone_number

class Catchy:
    def __init__(self):
        self.client = TelegramClient('imgtotext', api_id, api_hash)
        self.page = None
        self.upload_btn = None
        self.loading_indicator = None
        self.result_text = None
        self.icon = None
        self.icon_resized = None
        self.title_text = None
        self.tabs = {}
        self.current_tab = "home"

    async def text_from_image(self, image_path):
        '''
        Using the Telegram API to send 
        image to the bot and receive text response.
        '''
        await self.client.start(phone_number)

        async with self.client.conversation('@imageToText_bot') as c:
            await c.send_file(image_path)
            response = await c.get_response()
            return response.text

    def start(self, page: ft.Page):
        self.page = page
        self.setup_ui()
        self.page.update()

    def setup_ui(self):
        self.page.window.width = 800
        self.page.window.height = 700
        self.page.bgcolor = ft.colors.WHITE
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # UI
        self.icon = ft.Image(
            src="ico1.svg",
            width=300,
            height=300,
        )

        self.second_icon = ft.Image(
            src="ico2.svg",
            width=300,
            height=300,
        )


        self.title_text = ft.Text(
            value="Catchy",
            size=30,
            weight="bold",
            color=ft.colors.BLACK,
            text_align=ft.TextAlign.CENTER,
        )

        self.upload_btn = ft.ElevatedButton(
            text="Upload Image",
            on_click=self.on_upload,
            color=ft.colors.WHITE,
        )

        self.loading_indicator = ft.ProgressRing(visible=False)

        self.result_text = ft.TextField(
            value="",
            multiline=True,
            label="Catchy",
            width=500,
            height=200,
            read_only=True,
            text_align=ft.TextAlign.LEFT,
            border_color=ft.colors.BLUE,
            focused_border_color=ft.colors.BLUE_ACCENT,
            color=ft.colors.BLACK,
            visible=False,
        )



        # appbar
        self.page.appbar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.icons.HOME, 
                on_click=lambda e: self.switch_tab("home"),
            ),
            title=ft.Text("version 0.0.0"),
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.BUILD_SHARP, on_click=lambda e: self.page.launch_url('https://github.com/xterzxc/catchy')),
                ft.IconButton(ft.icons.SETTINGS, on_click=lambda e: self.switch_tab("settings")),
                ft.IconButton(ft.icons.HISTORY, on_click=lambda e: self.switch_tab("history")),
                ft.IconButton(ft.icons.INFO, on_click=lambda e: self.switch_tab("about")),
            ],
        )

        self.tabs = {
            "home": self.home_tab(),
            "history": self.history_tab(),
            "settings": self.settings_tab(),
            "about": self.about_tab(),
        }

        self.page.add(
            *[
                self.tabs[tab_name]
                for tab_name in self.tabs
            ]
        )

        self.switch_tab(self.current_tab)



    def home_tab(self):
        self.icon = ft.Image(
            src="ico1.svg",
            width=300,
            height=300,
        )

        self.upload_btn = ft.ElevatedButton(
            text="Upload Image",
            on_click=self.on_upload,
            color=ft.colors.WHITE,
        )

        self.loading_indicator = ft.ProgressRing(visible=False)

        self.result_text = ft.TextField(
            value="",
            multiline=True,
            label="Extracted Text",
            width=500,
            height=200,
            read_only=True,
            text_align=ft.TextAlign.LEFT,
            border_color=ft.colors.BLUE,
            focused_border_color=ft.colors.BLUE_ACCENT,
            color=ft.colors.BLACK,
            visible=False,
        )

        return ft.Container(
            content=ft.Column(
                [
                    self.icon,
                    self.upload_btn,
                    self.loading_indicator,
                    self.result_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            visible=False,
        )

    def settings_tab(self):


        self.tg_id_text = ft.TextField(
            label="Your Telegram API ID",
            color=ft.colors.BLACK,
        )
        self.tg_hash_text = ft.TextField(
            label="Your Telegram API Hash",
            color=ft.colors.BLACK,
        )

        self.upload_switcher = ft.Switch(label="", value=True)
        self.submit_button = ft.ElevatedButton(text="Submit")


        upload_switch_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        value="Ctrl + V to upload image",
                        color=ft.colors.BLACK,
                        size=16,
                        weight="bold"
                    ),
                    self.upload_switcher
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=8  # Add spacing between text and switch
            ),
            padding=8
        )
        # on_click=submit_button_clicked
        
        # c.value - on_change=checkbox_changed
        return ft.Container(
            content=ft.Column(
                [
                    self.tg_id_text,
                    self.tg_hash_text,
                    upload_switch_container,
                    self.submit_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            visible=False,
        )
    
    def history_tab(self):
        return ft.Container(
            content=ft.Text("history tab..."),
            alignment=ft.alignment.center,
        )
    
    def about_tab(self):
        return ft.Container(
            content=ft.Text("about tab..."),
            alignment=ft.alignment.center,
        )

    def switch_tab(self, tab_name):
        for tab in self.tabs.values():
            tab.visible = False
        
        self.tabs[tab_name].visible = True
        self.page.update()

    def on_upload(self, e):
        self.upload_btn.visible = False
        self.loading_indicator.visible = True
        self.page.update()

        file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allow_multiple=False)

    async def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            image_path = e.files[0].path
            extracted_text = await self.text_from_image(image_path)
            self.result_text.value = extracted_text

            self.result_text.visible = True
            self.loading_indicator.visible = False

            self.upload_btn.text = "Upload Another Image"
            self.upload_btn.visible = True

            self.page.update()
        else:
            self.upload_btn.visible = True
            self.loading_indicator.visible = False

            self.page.update()


if __name__ == "__main__":
    app = Catchy()
    ft.app(target=app.start)
