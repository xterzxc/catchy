import flet as ft
from telethon import TelegramClient, events
from test import api_id, api_hash, phone_number

client = TelegramClient('imgtotext', api_id, api_hash)



async def text_from_image(image_path):
    '''
    Using the Telegram API to send 
    image to the bot and receive text response.
    '''
    await client.start(phone_number)

    async with client.conversation('@imageToText_bot') as c:
        await c.send_file(image_path)

        response = await c.get_response()
        return response.text



def main(page: ft.Page):
    
    page.window.width = 800
    page.window.height = 600
    page.bgcolor = ft.colors.WHITE

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    icon = ft.Image(
        src="ico.svg",
        width=300,
        height=300,
    )


    def on_upload(e):
        loading_indicator.visible = True 
        file_picker = ft.FilePicker(on_result=on_file_picked)
        page.overlay.append(file_picker)

        page.update()

        file_picker.pick_files(allow_multiple=False)

    async def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            image_path = e.files[0].path
            extracted_text = await text_from_image(image_path)
            result_text.value = extracted_text

            result_text.visible = True
            loading_indicator.visible = False
            upload_btn.text = "Upload Another Image"

            page.update()



    upload_btn = ft.ElevatedButton(text="Upload Image", on_click=on_upload)
    loading_indicator = ft.ProgressRing(visible=False)

    title_text = ft.Text(
        value="Catchy",
        size=30,
        weight="bold",
        color=ft.colors.BLACK,
        text_align=ft.TextAlign.CENTER,
    )

    result_text = ft.Text(
        value="",
        size=16,
        text_align=ft.TextAlign.CENTER,
    )

    result_text = ft.TextField(
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


    page.add(
        ft.Column(
            [
                icon,
                title_text,
                upload_btn,
                loading_indicator,
                result_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )
    
ft.app(target=main)