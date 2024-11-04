import flet as ft
import re
import mysql.connector
import time
from hashlib import sha256
import smtplib
import random
import string
import sqlite3
import MYSQL_db_tvde_users_external
import SQLite_db_tvde_content_internal

def main(page: ft.Page):
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

    def page_message_screen(msg):
        page.views.clear()
        page.views.append(
            ft.View(
                "/message_screen",
                controls=[
                    ft.Container(
                        padding=210,
                        content=ft.Text(msg, color=ft.colors.GREEN, size=50)
                    )
                ]  
            )
        )
        page.update()
        time.sleep(1)

    def home_page():
        page.views.clear()

        def validate_email(e):
            if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email_login.value):
                email_login.error_text = None
            else:
                email_login.error_text = "O email digitado não é válido."
            email_login.update()

        def valid_email_password(email_login, password_login):

            hash_password_login = sha256(password_login.encode()).hexdigest()
            
            # Conectar ao banco de dados    
            conn = mysql.connector.connect(
                host="localhost",                    
                user="root",                    
                password="",                    
                database="db_tvde_users_external"       
            )
                
            cursor = conn.cursor()

            # Verificar se o email existe no banco de dados
            cursor.execute("""SELECT password FROM users WHERE email = %s""", (email_login,))

            result = cursor.fetchone()
            
            if result is None:
                email_login.error_text = "Email não encontrado"
                email_login.update() 
            else:
                stored_password = result[0]   
                if hash_password_login == stored_password:
                    print("Login bem-sucedido!")
                else:
                    password_login.error_text = "Senha incorreta"
                    password_login.update()
            cursor.close()  
            conn.close() 

        email_login = ft.TextField(label="Email", border_radius=21, on_change=validate_email)
        password_login = ft.TextField(label="Password", password=True, can_reveal_password=True , border_radius=21)
        button_login = ft.ElevatedButton(text="LOGIN", bgcolor={"disabled": "#d3d3d3", "": "#4CAF50"}, color="white",
                                          on_click=lambda e: valid_email_password(email_login.value, password_login.value))
        
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
                                ),
                                ft.Container(
                                    height=300,
                                    content=ft.Column(
                                        controls=[
                                            email_login,
                                            password_login,
                                            button_login,
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

        def validate_name(e):
            if len(name.value) > 4:
                name.error_text = None
            else:
                name.error_text = "O nome deve ter mais de 4 caracteres."
            name.update()
            validate_form()
        
        def validate_surname(e):
            if len(surname.value) > 4:
                surname.error_text = None
            else:
                surname.error_text = "O nome deve ter mais de 4 caracteres."
            surname.update()
            validate_form()
            
        def validate_phone_prefix(e):
            if re.match(r"^\d{4}$", phone_prefix.value):
                phone_prefix.error_text = None
            else:
                phone_prefix.error_text = "O prefixo deve ter 4 dígitos."
            phone_prefix.update()
            validate_form()
        
        def validate_phone_suffix(e):
            if re.match(r"^\d{9}$", phone_suffix.value):
                phone_suffix.error_text = None
            else:
                phone_suffix.error_text = "O sufixo deve ter 9 dígitos."
            phone_suffix.update()
            validate_form()            
        
        def validate_email(e):
            if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email.value):
                email.error_text = None
            else:
                email.error_text = "O email digitado não é válido."
            email.update()
            validate_form()
            
        def validate_password(e):
            if password.value == password_confirm.value:
                password_confirm.error_text = None
            else:
                password_confirm.error_text = "As senhas não coincidem."
            password_confirm.update()
            validate_form()

        def validate_form():
            if (len(name.value) > 4 and
                len(surname.value) > 4 and
                re.match(r"^\d{4}$", phone_prefix.value) and 
                re.match(r"^\d{9}$", phone_suffix.value) and
                re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email.value) and
                password.value == password_confirm.value and password.value != "" and password_confirm.value != ""):
                button_to_db.disabled = False
            else:
                button_to_db.disabled = True
            button_to_db.update()

        def add_in_db(name, surname, phone_prefix, phone_suffix, email, password):
            # Concatenar prefixo e sufixo do telefone
            hash_password = sha256(password.encode()).hexdigest()
            phone = f"{phone_prefix}{phone_suffix}"
            
            # Conectar ao banco de dados
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="db_tvde_users_external"
            )
            cursor = conn.cursor()

            if name and surname and phone and email and password:
                cursor.execute(
                    """INSERT INTO users (name, surname, phone, email, password) VALUES (%s, %s, %s, %s, %s)""",
                    (name, surname, phone, email, hash_password)
                )
                if cursor.rowcount > 0:
                    conn.commit()
                    page_message_screen("Usuário cadastrado com sucesso!")
                    page.go("/")
                else:
                    page_message_screen("Houve algum erro. Tente Novamente mais tarde!!!")
                    page.go("/")
            
            cursor.close()
            conn.close()
        
        name = ft.TextField(label="Name", border_radius=21, on_change=validate_name)
        surname = ft.TextField(label="Surname", border_radius=21, on_change=validate_surname)
        phone_prefix = ft.TextField(label="Prefixo (4 dígitos)", on_change=validate_phone_prefix, border_radius=21, width=150)
        phone_suffix = ft.TextField(label="Sufixo (9 dígitos)", on_change=validate_phone_suffix, border_radius=21)
        email = ft.TextField(label="Email", border_radius=21, on_change=validate_email)
        password = ft.TextField(label="Password", password=True, can_reveal_password=True, border_radius=21)
        password_confirm = ft.TextField(label="Password confirm", password=True, can_reveal_password=True, border_radius=21, on_change=validate_password)
        
        button_to_db = ft.ElevatedButton(text="REGISTER", bgcolor={"disabled": "#d3d3d3", "": "#4CAF50"}, color="white", disabled=True,
                                          on_click=lambda e: add_in_db(name.value, surname.value, phone_prefix.value, phone_suffix.value, email.value, password.value))
        page.views.append(
            ft.View(
                "/register",
                controls=[
                    ft.Container(
                        ft.Image(src="https://i.ibb.co/9q4BY9c/logo.jpg"),
                        height=270,
                        margin=20,
                        padding=20,
                    ),
                    ft.Text("Cadastro de Novo Usuário"),
                    ft.Row(controls=[name]),
                    ft.Row(controls=[surname]), 
                    ft.Row(controls=[phone_prefix, phone_suffix]),
                    ft.Row(controls=[email]),
                    ft.Row(controls=[password]),
                    ft.Row(controls=[password_confirm]),
                    ft.Row(controls=[button_to_db]),
                ]
            )
        )
        page.update()

    def page_forget_password():
        page.views.clear()
        
        def validate_email(e):
            if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', field_email.value):
                field_email.error_text = None
            else:
                field_email.error_text = "O email digitado não é válido."
            field_email.update()

        def verify_email_exist(field_email):

            #Connect the db database="db_tvde_users_external"
            conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "db_tvde_users_external"
            )
            
            cursor = conn.cursor()

            cursor.execute(
                " SELECT * FROM users WHERE email = %s ", (field_email,)
            )

            result = cursor.fetchone()

            if result:
                global codigo_temporario
                # Gerar um código temporário
                codigo_temporario = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
                print("E-mail encontrado. Código gerado:", codigo_temporario)
    
                # Aqui, você pode enviar o código por e-mail
                # Configuração do servidor SMTP
                remetente = "flavioalmeidamata@gmail.com"
                senha = "bqpdemqisaloczbg"

                try:
                    # Conectar ao servidor SMTP e enviar o e-mail
                    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
                        servidor.starttls()  # Ativar criptografia
                        servidor.login(remetente, senha)
                        mensagem = f"Subject: Redefinição de Senha\n\nCódigo temporário é: {codigo_temporario}"
                        servidor.sendmail(remetente, field_email, mensagem.encode("utf-8"))
                        page_message_screen("Enviamos um código para renovar o password")
                        page.go("/page_new_password")
            
                except Exception as e:
                    print("Erro ao enviar o e-mail:", e)
                
            else:
                print("E-mail não encontrado.")

            #Fechar a conexão
            cursor.close()
            conn.close()
    
        global field_email

        title = ft.Text("Recuperacao de senha")
        field_email = ft.TextField(label="Email", border_radius=21, on_change=validate_email)
        button_send = ft.ElevatedButton(text="Enviar", on_click=lambda e:verify_email_exist(field_email.value))

        page.views.append(
              
            ft.View(
                "/forget_password",
                controls=[
                    ft.Container(
                        ft.Image(src="https://i.ibb.co/9q4BY9c/logo.jpg"),
                        height=270,
                        margin=20,
                        padding=20,
                    ),
                    title,
                    field_email,
                    button_send
                ]
            )
        )
        page.update()

    def page_new_password():
        page.views.clear()

        def verify_code_email(field_code, new_password, field_email, codigo_temporario):
            hash_new_password = sha256(new_password.encode()).hexdigest()
            if field_code == codigo_temporario:
                try:
                # Conectar ao banco de dados
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="db_tvde_users_external"
                    )
                    cursor = conn.cursor()

                    # Executa a atualização
                    cursor.execute(
                        "UPDATE users SET password = %s WHERE email = %s", (hash_new_password, field_email)
                    )
                    conn.commit()  # Confirma a transação

                    # Verifica se alguma linha foi atualizada
                    if cursor.rowcount > 0:
                        page_message_screen("Seu password foi alterado com sucesso!")
                        page.go("/")
                    else:
                        page_message_screen("Não foi possível alterar o password. Usuário não encontrado.")
                        page.go("/page_new_password")
            
                except mysql.connector.Error as err:
                    print(f"Erro ao conectar ou executar a consulta: {err}")
                    page_message_screen("Ocorreu um erro ao alterar a senha. Tente novamente mais tarde.")
                    page.go("/page_new_password")

                finally:
                    # Certifique-se de fechar o cursor e a conexão
                    cursor.close()
                    conn.close()
            else:
                page_message_screen("Código incorreto. Tente novamente!")
                page.go("/")
            
        def validate_password(e):
            if new_password.value == confirm_new_password.value:
                confirm_new_password.error_text = None
            else:
                confirm_new_password.error_text = "As senhas não coincidem."
            confirm_new_password.update()

        def validate_field_code(e):
            codigo_temporario
            if field_code.value == codigo_temporario:
                field_code.error_text = None
            else:
                field_code.error_text = "Código Errado!"
            field_code.update()

        codigo_temporario
        field_email
        title = ft.Text("Criar novo password")
        field_code = ft.TextField(label="Code", border_radius=21, on_change=validate_field_code)
        new_password = ft.TextField(label="Novo password", border_radius=21, password=True, can_reveal_password=True)
        confirm_new_password = ft.TextField(label="Confirme o novo password", border_radius=21, password=True, can_reveal_password=True, on_change=validate_password)
        button_updated_password = ft.ElevatedButton(text="Alterar Passoword", on_click=lambda e:verify_code_email(field_code.value, new_password.value, field_email.value, codigo_temporario))
        page.views.append(
              
            ft.View(
                "/page_new_password",
                controls=[
                    ft.Container(
                        ft.Image(src="https://i.ibb.co/9q4BY9c/logo.jpg"),
                        height=270,
                        margin=20,
                        padding=20,
                    ),
                    title,
                    field_code,
                    new_password,
                    confirm_new_password,
                    button_updated_password
                  
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
        elif page.route == "/message_screen":
            page_message_screen()
        elif page.route == "/page_new_password":
            page_new_password()

    # Definindo o handler para mudanças de rota
    page.on_route_change = route_change

    # Definindo a rota inicial
    page.go("/")

ft.app(target=main)