import flet as ft
def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 15
    page.margin = 0
    page.title = "TVDE - FINANCIAL"

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="black",
            on_primary="#15CD74",
            background="green",
        )
    )
    layout = ft.Container(
        expand=True, bgcolor="white",
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(
                    ft.Image(src="https://i.ibb.co/9q4BY9c/logo.jpg"),
                    height=300,
                    margin=20,
                    padding=20,
                ),
                ft.Container(
                    height=300,
                    content=ft.Column(
                        controls=[
                            ft.TextField(label="Email", border_radius=21),
                            ft.TextField(label="Password", password=True, can_reveal_password=True, border_radius=21),
                            ft.ElevatedButton(text="ENTER", bgcolor="black", color="white"),
                        ],

                    ),
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(ft.Text("New User", size=18)),
                            ft.Container(ft.Text("|")),
                            ft.Container(ft.Text("Forget Password", size=18)),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ),
            ]
        )
    )

    page.add(layout)

ft.app(target = main)