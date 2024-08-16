import flet as ft

def main(page: ft.Page):
    page.title = "Catchy"
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
        file_picker = ft.FilePicker(on_result=on_file_picked)
        page.overlay.append(file_picker)

        page.update()

        file_picker.pick_files(allow_multiple=False)

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            print("Selected file:", e.files[0].name)

    upload_btn = ft.ElevatedButton(text="Upload Image", on_click=on_upload)

    title_text = ft.Text(
        value="Catchy",
        size=30,
        weight="bold",
        text_align=ft.TextAlign.CENTER,
    )


    page.add(
        ft.Column(
            [
                icon,
                title_text,
                upload_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )
    
ft.app(target=main)