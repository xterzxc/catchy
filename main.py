import os
import json
import configparser
import flet as ft
from telethon import TelegramClient
import ocrspace

class Catchy:
    def __init__(self):
        self.settings_manager = SettingsManager()
        self.api = ocrspace.API()
        self.page = None 
        self.upload_btn = None
        self.loading_indicator = None
        self.result_text = None
        self.icon = None
        self.icon_resized = None
        self.title_text = None
        self.tabs = {}
        self.current_tab = "home"
        self.history_file = 'history.json'
        self.history = self.load_history()

    async def text_from_image_telegram(self, image_path):
        '''
        Using the Telegram API to send 
        image to the bot and receive text response.
        '''

        self.client = TelegramClient(
            session='imgtotext', 
            api_id=self.settings_manager.get_setting('telegram_api_id'),
            api_hash=self.settings_manager.get_setting('telegram_api_hash'),
        )
        
        await self.client.start(self.settings_manager.get_setting('telegram_phone_number'))

        async with self.client.conversation('@imageToText_bot') as c:
            await c.send_file(image_path)
            response = await c.get_response()
            return response.text
    
    def text_from_image_ocr(self, image_path):
        '''
        Using OCR Space API to get text from image.
        '''
        return self.api.ocr_file(image_path)
    
    def start(self, page: ft.Page):
        self.page = page
        self.setup_ui()
        self.page.update()
        self.update_history_tab()

    def setup_ui(self):
        '''
        Full UI page setup
        '''
        self.page.window.width = 800
        self.page.window.height = 700
        self.page.bgcolor = ft.colors.WHITE
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # UI
        self.icon = ft.Image(
            src="assets/ico1.svg",
            width=300,
            height=300,
        )

        self.second_icon = ft.Image(
            src="assets/ico2.svg",
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
            on_click=self.on_file_upload,
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
            title=ft.Text("Catchy 0.0.1"),
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.BUILD_SHARP, on_click=lambda e: self.page.launch_url('https://github.com/xterzxc/catchy')),
                ft.IconButton(ft.icons.SETTINGS, on_click=lambda e: self.switch_tab("settings")),
                ft.IconButton(ft.icons.HISTORY, on_click=lambda e: self.switch_tab("history")),
                ft.IconButton(ft.icons.INFO, on_click=lambda e: self.switch_tab("about")),
            ],
        )


        # switching tabs
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
            on_click=self.on_file_upload,
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
            value=self.settings_manager.get_setting('telegram_api_id'),
            label="Your Telegram API ID",
            color=ft.colors.BLACK,
            width=500,
        )
        self.tg_hash_text = ft.TextField(
            value=self.settings_manager.get_setting('telegram_api_hash'),
            label="Your Telegram API Hash",
            color=ft.colors.BLACK,
            width=500,
        )

        self.tg_number_text = ft.TextField(
            value=self.settings_manager.get_setting('telegram_phone_number'),
            label="Your Telegram Phone Number",
            color=ft.colors.BLACK,
            width=500,
        )

        self.telegram_ocr_switcher = ft.Dropdown(
            options=[
                ft.dropdown.Option("OCR"),
                ft.dropdown.Option("Telegram"),
            ],
            value=self.settings_manager.get_setting('ocr_telegram_switcher'),
            width=300,
            on_change=lambda e: self.settings_manager.set_setting('ocr_telegram_switcher', e.control.value)
        )

        self.ctrlv_status_switcher = ft.Switch(
            label="", 
            value=True, 
            on_change=lambda e: self.settings_manager.set_setting('ctrlv_status_switcher', str(e.control.value))
        )

        self.submit_button = ft.ElevatedButton(
            text="Save",
            on_click=lambda e: (
                self.settings_manager.set_setting('telegram_api_id', self.tg_id_text.value),
                self.settings_manager.set_setting('telegram_api_hash', self.tg_hash_text.value),
                self.settings_manager.set_setting('telegram_phone_number', self.tg_number_text.value),
                self.settings_manager.set_setting('ocr_telegram_switcher', self.telegram_ocr_switcher.value),
                self.settings_manager.set_setting('ctrlv_status_switcher', str(self.ctrlv_status_switcher.value)),
                self.settings_manager.save_settings()
            )
        )


        ctrlv_status_switcher_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        value="Ctrl + V to upload image",
                        color=ft.colors.BLACK,
                        size=16,
                        weight="bold"
                    ),
                    self.ctrlv_status_switcher
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=8
            ),
            padding=8
        )
        # on_click=submit_button_clicked
        
        # c.value - on_change=checkbox_changed
        # сделать разные контейнеры под разные настройки. телега левый верх свой контейнер с  alignmentами
        return ft.Container(
            content=ft.Column(
                [
                    self.tg_id_text,
                    self.tg_hash_text,
                    self.tg_number_text,
                    self.telegram_ocr_switcher,
                    ctrlv_status_switcher_container,
                    self.submit_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            visible=False,
        )
    
    def history_tab(self):
        self.clear_button = ft.ElevatedButton(
            text="Clear History",
            on_click=self.clear_history,
            color=ft.colors.RED,
            width=150
        )
        
        self.history_list_view = ft.ListView(
            controls=self.create_history_items(),
            height=500,
            width=800,
            spacing=10,
            padding=ft.Padding(left=10, right=10, top=10, bottom=10),
        )
        
        history_content = ft.Column(
            controls=[
                self.clear_button,
                self.history_list_view
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        return ft.Container(
            content=history_content,
            alignment=ft.alignment.center_left,
            padding=ft.Padding(top=10, right=10, bottom=10, left=10),
            visible=False,
        )

    def create_history_items(self):
        history_items = []
        
        for i, record in enumerate(self.history):
            text_field = ft.TextField(
                value=f"{i + 1}: {record['extracted_text']}",
                multiline=True,
                read_only=True,
                color=ft.colors.BLACK,
                border_color=ft.colors.TRANSPARENT,
                width=750,
                height=100,
            )
            history_items.append(text_field)
        
        return history_items

    def clear_history(self, e):
        self.history = []
        self.save_history()
        self.update_history_tab()

    def update_history_tab(self):
        if self.history_list_view:
            self.history_list_view.controls = self.create_history_items()
            self.page.update()


    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f)

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

    def on_file_upload(self, e):
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
            if self.settings_manager.get_setting('ocr_telegram_switcher') == 'OCR':
                extracted_text = self.text_from_image_ocr(image_path)
            elif self.settings_manager.get_setting('ocr_telegram_switcher') == 'Telegram':
                extracted_text = await self.text_from_image_telegram(image_path)
            self.result_text.value = extracted_text

            self.history.append({
                'extracted_text': extracted_text
            })

            if len(self.history) > 10:
                self.history.pop(0)
            self.save_history()

            self.result_text.visible = True
            self.loading_indicator.visible = False

            self.upload_btn.text = "Upload Another Image"
            self.upload_btn.visible = True

            self.page.update()
            self.update_history_tab()

        else:
            self.upload_btn.visible = True
            self.loading_indicator.visible = False

            self.page.update()


class SettingsManager:
    def __init__(self, config_file='settings.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.set_default_settings()
            self.save_settings()


    def set_default_settings(self):
        self.config['Catchy'] = {
            'telegram_api_hash': '',
            'telegram_api_id': '',
            'telegram_phone_number': '',
            'ctrlv_status_switcher': True,
            'ocr_telegram_switcher': 'OCR',
        }

    def save_settings(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get_setting(self, option):
        return self.config.get('Catchy', option)

    def set_setting(self, option, value):
        self.config['Catchy'][option] = value
        self.save_settings()


if __name__ == "__main__":
    app = Catchy()
    ft.app(target=app.start)
