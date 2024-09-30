import flet as ft

def main(page: ft.Page):
    #colocar cores em variaveis para facilitar inclusao no projeto.
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 15
    page.margin = 0
    page.title = "TVDE - FINANCIAL"
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="black",
            on_primary="#15CD74",
            background="red",
        )
    )

    def home_page():
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                controls=[
                    ft.Container(
                        expand=True, bgcolor="white", border_radius=21,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                            controls=[
                                ft.Container(
                                    ft.Image(src="https://i.ibb.co/9q4BY9c/logo.jpg"),
                                    height=270,
                                    margin=20,
                                    padding=20,
                                    bgcolor="green"
                                ),
                                ft.Container(
                                    height=300,
                                    content=ft.Column(
                                        controls=[
                                            ft.TextField(label="Email", border_radius=21),
                                            ft.TextField(label="Password", password=True, can_reveal_password=True,
                                                         border_radius=21),
                                            ft.ElevatedButton(text="ENTER", bgcolor="black", color="white"),
                                        ],

                                    ),
                                ),
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Container(ft.Text("New User", size=18),
                                                         on_click=lambda e: page.go("/register")),
                                            ft.Container(ft.Text("|")),
                                            ft.Container(ft.Text("Forget Password", size=18),
                                                         on_click=lambda e: page.go("/forget_password")),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        page.update()

    def page_register():
        page.views.clear()
        global name, surname, phone, email, password, password_confirm
        name = ft.TextField(label="Name", border_radius=21)
        surname = ft.TextField(label="Surname", border_radius=21)
        phone = ft.TextField(label="Phone", border_radius=21)
        email = ft.TextField(label="Email", border_radius=21)
        password = ft.TextField(label="Password", password=True, can_reveal_password=True, border_radius=21)
        password_confirm = ft.TextField(label="Password confirm", password=True, can_reveal_password=True, border_radius=21)
        page.views.append(
            ft.View(
                "/register",
                controls=[
                    ft.Container(
                        ft.Image(src="https://i.ibb.co/9q4BY9c/logo.jpg"),
                        height=120,
                        margin=20,
                        padding=20,
                    ),
                    ft.Text("Cadastro de Novo Usuário"),
                    name, surname, phone, email, password, password_confirm,
                    ft.ElevatedButton(text="REGISTER", bgcolor="black", color="white"),
                ]
            )
        )
        page.update()

    def page_forget_password():
        page.views.clear()
        page.views.append(
            ft.View(
                "/forget_password",
                controls=[
                    ft.Text("Cadastro de Novo Usuário"),
                    ft.TextField(label="Nome"),
                    ft.TextField(label="Email"),
                    ft.ElevatedButton(text="Cadastrar", on_click=lambda e: page.go("/"))
                ]
            )
        )
        page.update()

    def route_change(route):
        if page.route == "/":
            home_page()
        elif page.route == "/register":
            page_register()
        elif page.route == "/forget_password":
            page_forget_password()

    # Definindo o handler para mudanças de rota
    page.on_route_change = route_change

    # Definindo a rota inicial
    page.go("/")


ft.app(target=main)
