import flet as ft
import re

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

        global name, surname, phone_prefix, phone_suffix, email, password, password_confirm

        def validate_name(e):
            # Verifica se o nome tem mais de 3 caracteres
            if len(name.value) > 4:
                name.error_text = None  # Remove mensagem de erro
            else:
                name.error_text = "O nome deve ter mais de 4 caracteres."
            name.update()
            validate_form()
        
        def validate_surname(e):
            # Verifica se o nome tem mais de 3 caracteres
            if len(surname.value) > 4:
                surname.error_text = None  # Remove mensagem de erro
            else:
                surname.error_text = "O nome deve ter mais de 4 caracteres."
            surname.update()
            validate_form()
            
        def validate_phone_prefix(e):
            # Verifica se o prefixo tem exatamente 4 dígitos
            if re.match(r"^\d{4}$", phone_prefix.value):
                phone_prefix.error_text = None
            else:
                phone_prefix.error_text = "O prefixo deve ter 4 dígitos."
            phone_prefix.update()
            validate_form()
        
        def validate_phone_suffix(e):
            # Verifica se o sufixo tem exatamente 9 dígitos
            if re.match(r"^\d{9}$", phone_suffix.value):
                phone_suffix.error_text = None
            else:
                phone_suffix.error_text = "O sufixo deve ter 9 dígitos."
            phone_suffix.update()
            validate_form()            
        
        def validate_email(e):
            if (re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email.value)):
                email.error_text = None
            else:
                email.error_text = "O email digitado não é valido."
            email.update()
            validate_form()
            
        def validate_password(e):
            # Verifica se o sufixo tem exatamente 9 dígitos
            if password.value == password_confirm.value:
                password_confirm.error_text = None
            else:
                password_confirm.error_text = "As senhas nao coencidem."
            password_confirm.update()
            validate_form()

        def validate_form():
            if (len(name.value) > 4 and
                len(surname.value) > 4 and
                re.match(r"^\d{4}$", phone_prefix.value) and 
                re.match(r"^\d{9}$", phone_suffix.value) and
                re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email.value) and
                password.value == password_confirm.value and password.value != "" and password_confirm.value != ""):
                button_to_db.disabled = False  # Habilita o botão de registro
            else:
                button_to_db.disabled = True  # Desabilita o botão de registro
            button_to_db.update()
            
        
        name = ft.TextField(label="Name", border_radius=21, on_change=validate_name)
        surname = ft.TextField(label="Surname", border_radius=21, on_change=validate_surname)
        phone_prefix = ft.TextField(label="Prefixo (4 dígitos)", on_change=validate_phone_prefix, border_radius=ft.border_radius.all(10))
        phone_suffix = ft.TextField(label="Sufixo (9 dígitos)", on_change=validate_phone_suffix, border_radius=ft.border_radius.all(10))
        email = ft.TextField(label="Email", border_radius=21, on_change=validate_email)
        password = ft.TextField(label="Password", password=True, can_reveal_password=True, border_radius=21)
        password_confirm = ft.TextField(label="Password confirm", password=True, can_reveal_password=True, border_radius=21, on_change=validate_password)
        button_to_db = ft.ElevatedButton(text="REGISTER", bgcolor={"disabled": "#d3d3d3", "": "#4CAF50"}, color="white", disabled=True)
        

        def add_in_db(name, password, password_confirm):
            #Funções de Validação
            # Valida name: Minimo tamanho 4 letras
        

            # Valida surname: Minimo tamanho 4 letras


            #Condicoao password equal
            if password.value != password_confirm.value:
                page.snack_bar = ft.SnackBar(
                    bgcolor="red",
                    content=ft.Text("As senhas não coincidem!"),
                    action="OK",
                )
                page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(
                    bgcolor="green",
                    content=ft.Text("As senhas coincidem!"),
                    action="OK",
                )
                page.snack_bar.open = True
            page.update()
                            
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
                    ft.Row(
                        controls = [
                            name
                        ]
                    ),
                    ft.Row(
                        controls = [
                            surname
                        ]
                    ), 
                    ft.Row(
                        controls = [
                            phone_prefix, 
                            phone_suffix 
                        ]
                    ),
                    ft.Row(
                        controls = [
                            email
                        ]
                    ),
                    ft.Row(
                        controls = [
                            password
                        ]
                    ),
                    ft.Row(
                        controls = [
                            password_confirm
                        ]
                    ),
                    ft.Row(
                        controls = [
                            button_to_db
                        ]
                    ),
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
