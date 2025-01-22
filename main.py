import flet as ft
import re
import mysql.connector
from datetime import datetime
import time
import datetime
from hashlib import sha256
import smtplib
import random
import string
import sqlite3
import MYSQL_db_tvde_users_external
import SQLite_db_tvde_content_internal

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.width = 435  # Largura típica de um smartphone
    page.window.height = 810  # Altura típica de um smartphone
    page.title = "TVDE - FINANCIAL"
    page.scroll = ft.ScrollMode.AUTO
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="black",
            on_primary="#15CD74",
            background="red",
        )
    )

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    pb = ft.PopupMenuButton(
        icon=ft.icons.MENU,
        shadow_color=ft.colors.GREEN_300,
        bgcolor="#F1F1F1",
        icon_size=33,
        items=[
                ft.PopupMenuItem(text="MENU"),
                ft.PopupMenuItem(icon=ft.icons.DATA_EXPLORATION_OUTLINED, text="Parciais", on_click=lambda _: page.go("/page_parcial")),
                ft.PopupMenuItem(icon=ft.icons.ADD_CIRCLE_OUTLINE_ROUNDED, text="Lançamentos" , on_click=lambda _: page.go("/page_more_date")),
                ft.PopupMenuItem(icon=ft.icons.ADD_CHART_OUTLINED, text="Novo Objetivo", on_click=lambda _: page.go("/page_new_goal")),
                ft.PopupMenuItem(icon=ft.icons.CALCULATE_OUTLINED, text="Relatórios", on_click=lambda _: page.go("/page_reports")),
                ft.PopupMenuItem(icon=ft.icons.CONTACTS_OUTLINED, text="Minha conta", on_click=lambda _: page.go("/page_my_account")),
                ft.PopupMenuItem(icon=ft.icons.SETTINGS_APPLICATIONS_SHARP, text="Configuração", on_click=lambda _: page.go("/page_settings")),
                ft.PopupMenuItem(icon=ft.icons.WORKSPACE_PREMIUM_OUTLINED, text="SEJA PREMIUM", on_click=lambda _: page.go("/page_premium")),
                ft.PopupMenuItem(),  # divider
                ft.PopupMenuItem(
                    icon=ft.icons.EXIT_TO_APP_SHARP, text="SAIR",on_click=lambda _: page.go("/")
                ),
        ]
    )

    header = ft.Row(
            controls=[
                ft.Container(
                    width=399,
                    expand=True,
                    height=66,
                    content=ft.Row(
                        controls=[
                            ft.Image(src="https://i.ibb.co/SrqCT9S/logo.png", width=154, height=51),
                            pb
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                    ),
                )
            ]
        )

    bottom_menu = ft.BottomAppBar(
            content=ft.Row(
                [
                    ft.IconButton(ft.icons.HOME_OUTLINED, on_click=lambda _: page.go("/page_parcial")),
                    ft.IconButton(ft.icons.ADD_CIRCLE_OUTLINE_ROUNDED, on_click=lambda _: page.go("/page_more_date")),
                    ft.IconButton(ft.icons.CALCULATE_OUTLINED, on_click=lambda _: page.go("/page_reports")),
                    ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go("/page_settings")),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            bgcolor="#EEEEEE",
            padding=10,
            height=60
        )

    button_edit = ft.ElevatedButton(
        text="Editar perfil", bgcolor={"disabled": "#d3d3d3", "": "#4CAF50"}, color="white"
        )
    
    button_premium = ft.ElevatedButton(
        text="CONTINUAR", bgcolor={"disabled": "#d3d3d3", "": "#4CAF50"}, color="white"
        )

    def page_message_screen(msg):
        page.views.clear()
        page.views.append(
            ft.View(
                "/message_screen",
                controls=[
                    ft.Container(
                        content=ft.Text(msg, color=ft.colors.GREEN, size=21)
                    )
                ]  
            )
        )
        page.update()
        time.sleep(3)

    def title_app(icon, title):
        return ft.Container(  # Retornando o Container corretamente
            content=ft.Row(  # Para alinhar o ícone e o título
                controls=[icon, title],  # Passando o ícone diretamente
                alignment=ft.MainAxisAlignment.CENTER  # Alinha no centro
            ),
            padding=ft.padding.only(bottom=21),
            border=ft.border.only(bottom=ft.border.BorderSide(0.3, ft.colors.GREY_900))
        )
    
    def page_menu():
        page.views.clear()

        page_menu_open = ft.Container(
            bgcolor=ft.colors.AMBER_300,
            width=435,
            height=600,
            border_radius=21,
            content=ft.Column(
                controls=[
                    ft.Image(src="https://i.ibb.co/SrqCT9S/logo.png"),
                    ft.Text(f"Hi {user_name}, good luck today! :)", size=15, weight=ft.FontWeight.BOLD,  text_align=ft.TextAlign.CENTER),
                    ft.border.only(bottom=ft.border.BorderSide(0.3, ft.colors.GREY_900)),
                    ft.Container(height=90),
                    ft.Text("Nome: "),
                    ft.Text("Email: "),
                    ft.Text("Tipo de Conta: "),
                    ft.Container(height=90),
                    ft.Text("Seja PREMIUM agora"),
                    ft.Row(
                        ft.Text("SEJA \n PREMIUM \n AQUI"),
                        ft.Image(src="https://i.ibb.co/SrqCT9S/logo.png"),
                        ft.Text("Desbloqueie relatórios completos..."),
                    ),
                    ft.ElevatedButton(
                        text="SAIR", bgcolor={"disabled": "#D00000", "": "#4CAF50"}, color="white"
                    )
                ]
            )
        )
        page.views.append(
                ft.View(
                    "/page_menu",
                    controls=[
                        page_menu_open
                    ]
                )

            )
        page.update

    def page_premium():
        page.views.clear()

        page.views.append(
            ft.View(
                "/page_premium",
                controls=[
                    header,
                    title_app(
                           icon = ft.Icon(ft.icons.WORKSPACE_PREMIUM_OUTLINED),
                           title = ft.Text("PREMIUM", size=21),
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.VERIFIED, color="GREEN"),
                            ft.Text("CONTROLE SEUS GANHOS E GASTOS")
                        ]
                    ), 
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.VERIFIED, color="GREEN"),
                            ft.Text("DESBLOQUEIE RELATÓRIOS COMPLETOS")
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.VERIFIED, color="GREEN"),
                            ft.Text("RELATÓRIOS EXCLUSIVOS")
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.VERIFIED, color="GREEN"),
                            ft.Text("SEM PROPAGANDAS")
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.VERIFIED, color="GREEN"),
                            ft.Text("CANCELE A QUALQUER MOMENTO")
                        ]
                    ),
                    ft.Container(),
                    button_premium,
                    bottom_menu
                ]
            )
        )

        page.update()

    def page_my_account():
        page.views.clear()

        page.views.append(
            ft.View(
                "/page_my_account",
                controls=[
                    header,
                    title_app(
                           icon = ft.Icon(ft.icons.ACCOUNT_CIRCLE_OUTLINED),
                           title = ft.Text("MINHA CONTA", size=21),
                    ),
                    ft.Container(
                        ft.Row(
                            controls=[
                                 ft.Container(
                                    content=ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=18), 
                                    padding=ft.padding.all(9),  # Adicione o padding desejado
                                ),
                                ft.Text(f"Nome: {user_name} {surname}", size=15)
                            ]
                        ),
                    ),
                    ft.Container(
                        border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.GREY_200)),
                    ),

                    ft.Container(
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(ft.icons.EMAIL_OUTLINED, size=18),
                                    padding=ft.padding.all(9),  # Adicione o padding desejado
                                ),
                                ft.Text(f"Email: {email_login.value}", size=15)
                            ]
                        ),
                    ),
                    ft.Container(
                        border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.GREY_200)),
                    ),
                    ft.Container(
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(ft.icons.WORKSPACE_PREMIUM_OUTLINED, size=18), 
                                    padding=ft.padding.all(9),  # Adicione o padding desejado
                                ),
                                ft.Text(f"Tipo de Conta: {account_type}", size=15)
                            ]
                        ),
                    ),
                    ft.Container(
                        border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.GREY_200)),
                    ),
                      ft.Container(
                        ft.Row(
                            controls=[
                                 ft.Container(
                                    content=ft.Icon(ft.icons.DATE_RANGE, size=18,),  
                                    padding=ft.padding.all(9),  # Adicione o padding desejado
                                ),
                                ft.Text(f"Data da conta: {date_start}" , size=15)
                            ]
                        ),
                    ),
                    ft.Container(
                        border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.GREY_200)),
                    ),
                    button_edit,
                    bottom_menu
                ]
            )
        )

        page.update()

    def page_reports():
        page.views.clear()

        big_button_reports_daily_summary = ft.Container(
                        width=180,
                        height=135,
                        bgcolor="#EFEFEF",
                        border_radius=21,
                        margin=6,
                        on_click=lambda e: page.go("/page_expense"),
                        content=
                            ft.Column(  
                                controls=[
                                    ft.Icon(ft.icons.TODAY, size=36),
                                    ft.Text("Resumo Diário")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
        )

        big_button_reports_platform = ft.Container(
                        width=180,
                        height=135,
                        bgcolor="#EFEFEF",
                        border_radius=21,
                        margin=6,
                        on_click=lambda e: page.go("/page_expense"),
                        content=
                            ft.Column(  
                                controls=[
                                    ft.Icon(ft.icons.ADD_TO_HOME_SCREEN, size=36),
                                    ft.Text("Relatório de Plataforma")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
        )

        big_button_reports_delailed_expenses = ft.Container(
                        width=180,
                        height=135,
                        bgcolor="#EFEFEF",
                        border_radius=21,
                        margin=6,
                        on_click=lambda e: page.go("/page_expense"),
                        content=
                            ft.Column(  
                                controls=[
                                    ft.Icon(ft.icons.EURO, size=39),
                                    ft.Text("Despesas")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
        )

        big_button_reports_profit_by_race = ft.Container(
                        width=180,
                        height=135,
                        bgcolor="#EFEFEF",
                        border_radius=21,
                        margin=6,
                        on_click=lambda e: page.go("/page_expense"),
                        content=
                            ft.Column(  
                                controls=[
                                    ft.Icon(ft.icons.DIRECTIONS_CAR, size=36),
                                    ft.Text("Lucro por Corrida")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
        )

        big_button_reports_monthly = ft.Container(
                        width=180,
                        height=135,
                        bgcolor="#EFEFEF",
                        border_radius=21,
                        margin=6,
                        on_click=lambda e: page.go("/page_expense"),
                        content=
                            ft.Column(  
                                controls=[
                                    ft.Icon(ft.icons.CALENDAR_MONTH, size=36    ),
                                    ft.Text("Relatório Mensal")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
        )

        page.views.append(
            ft.View(
                "/page_reports",
                controls=[
                    header,
                    title_app(
                           icon = ft.Icon(ft.icons.CALCULATE_OUTLINED),
                           title = ft.Text("RELATÓRIOS", size=21),
                    ),
                    ft.Row(
                        controls=[big_button_reports_daily_summary,
                            big_button_reports_platform,]
                    ),
                    ft.Row(
                        controls=[big_button_reports_delailed_expenses,
                        big_button_reports_profit_by_race]
                    ),
                    big_button_reports_monthly,
                    bottom_menu
                ]
            )
        )

        page.update()
    
    def page_settings():
        page.views.clear()

        page.views.append(
            ft.View(
                "/page_settings",
                controls=[
                    header,
                    title_app(
                           icon = ft.Icon(ft.icons.SETTINGS_APPLICATIONS_SHARP),
                           title = ft.Text("CONFIGURAÇÃO", size=21),
                    ),
                    ft.Text("Idioma do APP"),
                    ft.Text("Tema: Claro / Escuro"),
                    ft.Text("Apagar dados"),
                    ft.Text("Personalizar graficos"),
                    bottom_menu
                ]
            )
        )

        page.update()

    def page_login():
        page.views.clear()

        def validate_email(e):
            if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email_login.value):
                email_login.error_text = None
            else:
                email_login.error_text = "O email digitado não é válido."
            email_login.update()

        def valid_email_password(email_login, password_login):
            hash_password_login = sha256(password_login.value.encode()).hexdigest()
            
            # Conectar ao banco de dados    
            conn = mysql.connector.connect(
                host="localhost",                    
                user="root",                    
                password="",                    
                database="db_tvde_users_external"       
            )
                
            cursor = conn.cursor()
            cursor = conn.cursor(buffered=True)

            # Verificar se o email existe no banco de dados
            cursor.execute("""SELECT password FROM users WHERE email = %s""", (email_login.value,))

            result = cursor.fetchone()
            
            if result is None:
                email_login.error_text = "Email não encontrado"
                email_login.update() 
            else:
                stored_password = result[0]   
                if hash_password_login == stored_password:
                    print("Login bem-sucedido!")
                    page.go("/page_parcial")  # Navegar para "page_new_goal" se o login for bem-sucedido
                else:
                    password_login.error_text = "Senha incorreta"
                    password_login.update()

            cursor.close()  
            conn.close()

        global email_login
        email_login = ft.TextField(label="Email", border_radius=21, on_change=validate_email)
        password_login = ft.TextField(label="Password", password=True, can_reveal_password=True, border_radius=21)
        button_login = ft.ElevatedButton(
            text="LOGIN", bgcolor={"disabled": "#d3d3d3", "": "#4CAF50"}, color="white",
            on_click=lambda e: valid_email_password(email_login, password_login)
        )
        
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
                                    ft.Image(src="https://i.ibb.co/SrqCT9S/logo.png"),
                                    padding=90,
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[email_login, password_login, button_login],
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

    def page_new_goal():
        page.views.clear()

        def validate_date(e=None):
            # Inicializa as mensagens de erro e o estado do botão
            start_date_error = None
            end_date_error = None
            valid = True

            try:
                # Verifica se o campo de início tem um valor válido
                if goal_start_field.value.strip():
                    start_date = datetime.datetime.strptime(goal_start_field.value.strip(), "%d/%m/%Y")
                else:
                    start_date_error = "Use DD/MM/AAAA."
                    valid = False

                # Verifica se o campo de fim tem um valor válido
                if goal_end_field.value.strip():
                    end_date = datetime.datetime.strptime(goal_end_field.value.strip(), "%d/%m/%Y")
                else:
                    end_date_error = "Use DD/MM/AAAA."
                    valid = False

                # Verifica se as datas são válidas e comparáveis
                if valid and start_date >= end_date:
                    start_date_error = "Data Início < Data Fim "
                    end_date_error = "Data de fim > data de início"
                    valid = False

            except ValueError:
                # Define mensagens de erro para valores inválidos
                if goal_start_field.value.strip():
                    start_date_error = "Use DD/MM/AAAA."
                if goal_end_field.value.strip():
                    end_date_error = "Use DD/MM/AAAA."
                valid = False

            # Atualiza os campos com mensagens de erro
            goal_start_field.error_text = start_date_error
            goal_end_field.error_text = end_date_error
            button_salve.disabled = not valid

            # Atualiza os elementos na interface
            goal_start_field.update()
            goal_end_field.update()
            button_salve.update()

        # Vincule a função aos eventos de mudança de valor dos campos
            goal_start_field.on_change = validate_date
            goal_end_field.on_change = validate_date
      
        def format_number(e):
            # Filtra e mantém apenas os dígitos numéricos
            raw_value = ''.join(filter(str.isdigit, e.control.value))

            if raw_value:
                # Adiciona vírgula para centavos, separando os dois últimos dígitos
                if len(raw_value) > 2:
                    raw_value = raw_value[:-2] + ',' + raw_value[-2:]
                else:
                    raw_value = '00,' + raw_value

                # Converte para inteiro e formata com separador de milhar (ponto)
                integer_part = raw_value.split(',')[0]
                decimal_part = raw_value.split(',')[1]

                # Formata a parte inteira com ponto como separador de milhar
                formatted_integer = f"{int(integer_part):,}".replace(',', '.')

                # Junta a parte inteira formatada com a parte decimal
                formatted_value = f"{formatted_integer},{decimal_part}"

                # Atualiza o campo com o valor formatado, sem o símbolo de euro
                e.control.value = formatted_value
                e.control.update()

                # Verifica se o valor é menor ou igual a 0
                if int(raw_value.replace(',', '')) <= 0:
                    # Exibe uma mensagem de erro
                    e.control.error_text = "O valor deve ser maior que 0."
                    e.control.update()

                    # Desabilita o botão
                    for control in e.page.controls:
                        if hasattr(control, 'name') and control.name == 'button_salve':
                            control.enabled = False
                            control.update()
                else:
                    # Limpa a mensagem de erro se o valor for válido
                    e.control.error_text = ""
                    e.control.update()

                    # Habilita o botão se o valor for válido
                    for control in e.page.controls:
                        if hasattr(control, 'name') and control.name == 'button_salve':
                            control.enabled = True
                            control.update()

            else:
                # Campo vazio
                e.control.value = ""
                e.control.error_text = "Campo não pode estar vazio."
                e.control.update()

                # Desabilita o botão se o campo estiver vazio
                for control in e.page.controls:
                    if hasattr(control, 'name') and control.name == 'button_salve':
                        control.enabled = False
                        control.update()

        def format_number_only99(e):
        # Remove qualquer caractere que não seja dígito
            raw_value = ''.join(filter(str.isdigit, e.control.value))
            
            if raw_value:
                # Converte para inteiro e formata com separador de milhar
                integer_value = min(int(raw_value[:2]), 99)
                formatted_value = str(integer_value)
            else:
                formatted_value = ""

            # Atualiza o TextField com o valor formatado
            e.control.value = formatted_value
            e.control.update()

        goal_field = ft.TextField(label="Valor total da meta", prefix_text="€ ",
            border_radius=21, 
            text_size=18,
            on_change=format_number,
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,               # Tamanho opcional
            ),
            helper_text="* Valor líquido pretendido ao fim da meta.",
            content_padding=ft.padding.symmetric(vertical=12, horizontal=12)
        )
        
        date_picker = ft.DatePicker(on_change=None)  # on_change definido depois dinamicamente

        def pick_date(e, field):
            date_picker.on_change = lambda e: on_date_selected(e, field)
            page.open(date_picker)

        def on_date_selected(e, field):
            if date_picker.value:
                field.value = date_picker.value.strftime("%d/%m/%Y")
                validate_date(e)  
                page.update()
        
        goal_start_field = ft.TextField(
            label="Início da meta",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            on_change=validate_date,
            width=page.width * 0.47,
            border_radius=21,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            helper_text="* Data do Início da meta",
            content_padding=ft.padding.symmetric(vertical=6, horizontal=9),
            expand=True,
            suffix=ft.IconButton(
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda e: pick_date(e, goal_start_field),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=21)  # Estilizando o botão para que ele acompanhe o arredondamento
                )
            )
        )

        goal_end_field = ft.TextField(
            label="Fim da meta",
            on_change=validate_date,
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            width=page.width * 0.47,
            border_radius=21,
            expand=True,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            helper_text="* Data do Fim da Meta",
            content_padding=ft.padding.symmetric(vertical=6, horizontal=9),
            suffix=ft.IconButton(
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda e: pick_date(e, goal_end_field)
            )
        )

        goal_dates = ft.Container(
            ft.Row(
                controls=[goal_start_field, goal_end_field]
            )
        )
        day_off_field = ft.TextField(
            label="Dias de Folga",
            on_change=format_number_only99,
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,               # Tamanho opcional
            ),
            border_radius=21,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            helper_text="* Quantos dias terá de folga.",
            content_padding=ft.padding.symmetric(vertical=12, horizontal=9)
        )
        
        fleet_discount_field = ft.TextField(
            label="Desconto da Frota",
            on_change=format_number_only99,
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,               # Tamanho opcional
            ),
            suffix_text="%",
            border_radius=21,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            helper_text="Desconto da frota.",
            content_padding=ft.padding.symmetric(vertical=12, horizontal=9)
        )
        tax_discount_field = ft.TextField(
            label="Imposto",
            on_change=format_number_only99,
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,               # Tamanho opcional
            ),
            suffix_text="%",
            border_radius=21,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            helper_text="Imposto.",
            content_padding=ft.padding.symmetric(vertical=12, horizontal=9)
        )
       
           # Função para salvar no banco de dados
        
        def save_goal(e):
                # Coletar os valores dos campos
                goal = float(goal_field.value.replace('.', '').replace(',', '.'))
                goal_start = goal_start_field.value
                goal_end = goal_end_field.value
                day_off = int(day_off_field.value)
                fleet_discount = float(fleet_discount_field.value)
                tax_discount = float(tax_discount_field.value)

                # Conectar ao banco e inserir os dados
                conn = sqlite3.connect("db_tvde_content_internal.db")
                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO goal (goal, goal_start, goal_end, day_off, fleet_discount, tax_discount)
                VALUES (?,?,?,?,?,?)
                """, (goal, goal_start, goal_end, day_off, fleet_discount, tax_discount)
                )
                
                conn.commit()
                conn.close()

                # Feedback e limpeza
                if cursor.rowcount > 0:
                    page_message_screen("Meta cadastrada com sucesso!!!")
                    page.go("/page_parcial")
                else:
                    page_message_screen("Houve algum erro. Tente Novamente mais tarde!!!")
                    page.go("/page_new_goal")


        # Exibe o SnackBar de sucesso

                goal_field.value = ""
                goal_start_field.value = ""
                goal_end_field.value = ""
                day_off_field.value = ""
                fleet_discount_field.value = ""
                tax_discount_field.value = ""
                page.update()

        button_salve = ft.ElevatedButton(
        text="SALVAR", bgcolor={"disabled": "#d3d3d3", "": "#4CAF50"}, color="white", on_click=save_goal)

        page.overlay.append(date_picker)
        page.views.append(
            ft.View(
                "/page_new_goal",
                controls=[
                    header,
                    title_app(
                           icon = ft.Icon(ft.icons.MORE_TIME),
                           title = ft.Text("NOVO OBJETIVO", size=21),
                    ),
                    ft.Container(height=0.9),
                    goal_field,
                    ft.Container(height=0.9),
                    goal_dates,
                    ft.Container(height=0.9),
                    day_off_field,
                    ft.Container(height=0.9),
                    fleet_discount_field,
                    ft.Container(height=0.9),
                    tax_discount_field,    
                    ft.Container(height=0.9),
                    button_salve,
                    bottom_menu
                ]
            )
        )
        page.update()

    def page_expense():
        page.views.clear()

        def validate_date(e=None):
            # Obtém o valor do campo de data
            input_date = expense_date.value.strip()
            try:
                # Verifica se o formato é DD/MM/AAAA e se a data é válida
                parsed_date = datetime.strptime(input_date, "%d/%m/%Y")
                
                # Normaliza o campo para um formato consistente (opcional)
                expense_date.value = parsed_date.strftime("%d/%m/%Y")
                expense_date.error_text = None  # Limpa o erro
                
                # Habilita o botão se todos os campos estiverem válidos
                button_add_expense.disabled = not all_fields_valid()
            except ValueError:
                # Exibe erro se a data for inválida
                expense_date.error_text = (
                    "Data inválida! Insira no formato DD/MM/AAAA e use uma data válida."
                )
                button_add_expense.disabled = True
            finally:
                expense_date.update()
                page.update()

        result_label = ft.Text(value="", color="black")
    
        def on_date_selected(e):
        # Atualiza o campo de data com a seleção do DatePicker
            if date_picker2.value:
                parsed_date = date_picker2.value
                expense_date.value = parsed_date.strftime("%d/%m/%Y")
                validate_date()  # Revalida após a seleção
                page.update()

        def format_number(e):
            # Filtra e mantém apenas os dígitos numéricos
            raw_value = ''.join(filter(str.isdigit, e.control.value))

            if raw_value:
                # Adiciona vírgula para centavos, separando os dois últimos dígitos
                if len(raw_value) > 2:
                    raw_value = raw_value[:-2] + ',' + raw_value[-2:]
                else:
                    raw_value = '00,' + raw_value

                # Converte para inteiro e formata com separador de milhar (ponto)
                integer_part = raw_value.split(',')[0]
                decimal_part = raw_value.split(',')[1]

                # Formata a parte inteira com ponto como separador de milhar
                formatted_integer = f"{int(integer_part):,}".replace(',', '.')

                # Junta a parte inteira formatada com a parte decimal
                formatted_value = f"{formatted_integer},{decimal_part}"

                # Atualiza o campo com o valor formatado, sem o símbolo de euro
                e.control.value = formatted_value
                e.control.update()

                # Verifica se o valor é menor ou igual a 0
                if int(raw_value.replace(',', '')) <= 0:
                    # Exibe uma mensagem de erro
                    e.control.error_text = "O valor deve ser maior que 0."
                    e.control.update()

                    # Desabilita o botão
                    for control in e.page.controls:
                        if hasattr(control, 'name') and control.name == 'button_salve':
                            control.enabled = False
                            control.update()
                else:
                    # Limpa a mensagem de erro se o valor for válido
                    e.control.error_text = ""
                    e.control.update()

                    # Habilita o botão se o valor for válido
                    for control in e.page.controls:
                        if hasattr(control, 'name') and control.name == 'button_salve':
                            control.enabled = True
                            control.update()

            else:
                # Campo vazio
                e.control.value = ""
                e.control.error_text = "Campo não pode estar vazio."
                e.control.update()

                # Desabilita o botão se o campo estiver vazio
                for control in e.page.controls:
                    if hasattr(control, 'name') and control.name == 'button_salve':
                        control.enabled = False
                        control.update()
        
        def all_fields_valid():
        # Verifica se todos os campos obrigatórios estão válidos
            return (
                expense_value.value.strip() and  # Valor preenchido
                expense_date.value.strip() and  # Data preenchida
                not expense_date.error_text and  # Data válida
                expense_name.value  # Nome da despesa selecionado
            )

        def validate_all_fields():
            """
            Verifica todos os campos obrigatórios e habilita o botão de cadastro se estiverem válidos.
            """
            # Verificar se todos os campos obrigatórios têm valores válidos
            all_valid = (
                bool(expense_value.value.strip()) and  # Verifica se o campo Valor da despesa não está vazio
                bool(expense_date.value.strip()) and  # Verifica se a data da despesa foi preenchida
                bool(expense_name.value)  # Verifica se uma despesa foi selecionada no dropdown
            )

            # Verificar campos condicionais (quantidades específicas para opções de despesas)
            if expense_name.value in ["Gasolína", "Gasóleo"] and not expense_amount_liters.value.strip():
                all_valid = False
            elif expense_name.value == "GPL" and not expense_amount_cubic_meters.value.strip():
                all_valid = False
            elif expense_name.value == "Recarga Bateria" and not expense_amount_energy.value.strip():
                all_valid = False

            # Habilitar ou desabilitar o botão com base na validação
            button_add_expense.disabled = not all_valid
            page.update()

        global expense_value
        expense_value = ft.TextField(label="Valor da despesa", prefix_text="€ ",
            border_radius=21, 
            text_size=18,
            on_change=lambda e: (format_number(e), validate_all_fields()), 
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            content_padding=ft.padding.symmetric(vertical=12, horizontal=12)
        )

        def pick_date(e, field):
            # Adiciona o DatePicker à página antes de abrir
            page.add(date_picker2)
            page.open(date_picker2)  # Usa o método correto para abrir o DatePicker

        def on_date_selected(e):
            # Atualiza o campo de data com a seleção do DatePicker
            if date_picker2.value:
                parsed_date = date_picker2.value
                expense_date.value = parsed_date.strftime("%d/%m/%Y")
                validate_date()  # Revalida após a seleção
                page.update()

        # Criação do DatePicker
        date_picker2 = ft.DatePicker(on_change=on_date_selected)
        global expense_date
        # Criação do TextField para data
        expense_date = ft.TextField(
            label="Data da despesa",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            on_change=lambda e: (validate_date(e), validate_all_fields()), 
            border_radius=21,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            helper_text="* Data da despesa.",
            content_padding=ft.padding.symmetric(vertical=6, horizontal=9),
            suffix=ft.IconButton(
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda e: pick_date(e, expense_date),  # Chama pick_date para abrir o DatePicker
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=21)  # Estilizando o botão
                )
            )
        )
        
        global observation_expense
        observation_expense = ft.TextField(
            label="Observação",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            border_radius=21,
            text_size=18,
            helper_text="Observação",
            multiline=True
        )

        global expense_name
        expense_name = ft.Dropdown(
            label="Despesas:",  # Texto de rótulo do dropdown
            options=[
                ft.dropdown.Option("Manutenção"),
                ft.dropdown.Option("Gasolína"),
                ft.dropdown.Option("Gasóleo"),
                ft.dropdown.Option("GPL"),
                ft.dropdown.Option("Recarga Bateria"),
                ft.dropdown.Option("Alimentação"),
                ft.dropdown.Option("Seguro"),
                ft.dropdown.Option("Portagem")
            ], # Defina uma função para tratar a mudança
            border_radius=21,
            on_change=lambda e: (on_option_selected(e), validate_all_fields()),
            content_padding=ft.padding.symmetric(vertical=6, horizontal=9),
        )

        global expense_amount_cubic_meters, expense_amount_energy, expense_amount_liters
        expense_amount_liters = ft.TextField(label="Litros", visible=False, border_radius=21,  on_change=lambda e: validate_all_fields() )
        expense_amount_cubic_meters = ft.TextField(label="Metros Cúbicos (m³)", visible=False, border_radius=21, on_change=lambda e: validate_all_fields())
        expense_amount_energy = ft.TextField(label="Energia (kWh)", visible=False, border_radius=21,  on_change=lambda e: validate_all_fields() )

        def on_option_selected(e):
            expense_amount_liters.visible = False
            expense_amount_cubic_meters.visible = False
            expense_amount_energy.visible = False
            # Alterar a cor de fundo e do texto dependendo da seleção
            if e.control.value == "Manutenção":
                expense_name.bgcolor = "#E0E0E0"  # Cor de fundo quando "Opção 1" é selecionada
                expense_name.style = ft.TextStyle(color="#FF5722")  # Cor do texto para "Opção 1"
            elif e.control.value == "Gasolína":
                expense_amount_liters.visible = True
                expense_name.bgcolor = "#FFEB3B"  # Cor de fundo quando "Opção 2" é selecionada
                expense_name.style = ft.TextStyle(color="#000000")  # Cor do texto para "Opção 2"
            elif e.control.value == "Gasóleo":
                expense_name.bgcolor = "#B25900"  # Cor de fundo quando "Opção 3" é selecionada
                expense_amount_liters.visible = True
                expense_name.style = ft.TextStyle(color="#FFFFFF")  # Cor do texto para "Opção 3"
            elif e.control.value == "GPL":
                expense_name.bgcolor = "#4CAF50"  # Cor de fundo quando "Opção 3" é selecionada
                expense_amount_cubic_meters.visible = True
                expense_name.style = ft.TextStyle(color="#FFFFFF")  # Cor do texto para "Opção 3"
            elif e.control.value == "Recarga Bateria":
                expense_name.bgcolor = "#B200B2"  # Cor de fundo quando "Opção 3" é selecionada
                expense_amount_energy.visible = True
                expense_name.style = ft.TextStyle(color="#FFFFFF")  # Cor do texto para "Opção 3"
            elif e.control.value == "Alimentação":
                expense_name.bgcolor = "#FF7F00"  # Cor de fundo quando "Opção 3" é selecionada
                expense_name.style = ft.TextStyle(color="#FFFFFF")  # Cor do texto para "Opção 3"
            elif e.control.value == "Seguro":
                expense_name.bgcolor = "#007FFF"  # Cor de fundo quando "Opção 3" é selecionada
                expense_name.style = ft.TextStyle(color="#FFFFFF")  # Cor do texto para "Opção 3"
            else:
                expense_name.bgcolor = "#00B200"  # Cor de fundo quando "Opção 4" é selecionada
                expense_name.style = ft.TextStyle(color="#CCCCCC")  # Cor do texto para "Opção 4"
            # Atualizar a página após a mudança
            page.update()

        # Agora você pode acessar o valor dela corretamente
        def cadastrar_despesa():
            # Limpar mensagens de erro anteriores e bordas
            page.controls = [control for control in page.controls if not isinstance(control, ft.Text) or control.color != "red"]

            # Verificar se os campos obrigatórios estão preenchidos
            error_messages = []

            # Verificar campos obrigatórios
            if not expense_value.value:
                expense_value.border_color = "red"  # Mudar a borda para vermelho
                error_messages.append(("O valor da despesa é obrigatório.", expense_value))
                page.update()
            else:
                expense_value.border_color = None  # Restaurar a borda original

            if not expense_date.value:
                expense_date.border_color = "red"
                error_messages.append(("A data da despesa é obrigatória.", expense_date))
                page.update()
            else:
                expense_date.border_color = None

            if not expense_name.value:
                expense_name.border_color = "red"
                error_messages.append(("O nome da despesa é obrigatório.", expense_name))
                page.update()
            else:
                expense_name.border_color = None

            # Verificar os campos de quantidade obrigatórios
            if not expense_amount_liters.value and (expense_name.value == "Gasolína" or expense_name.value == "Gasóleo"):
                expense_amount_liters.border_color = "red"
                error_messages.append(("A quantidade de litros é obrigatória.", expense_amount_liters))
                page.update()
            else:
                expense_amount_liters.border_color = None

            if not expense_amount_cubic_meters.value and expense_name.value == "GPL":
                expense_amount_cubic_meters.border_color = "red"
                error_messages.append(("A quantidade de metros cúbicos é obrigatória.", expense_amount_cubic_meters))
                page.update()
            else:
                expense_amount_cubic_meters.border_color = None

            if not expense_amount_energy.value and expense_name.value == "Recarga Bateria":
                expense_amount_energy.border_color = "red"
                error_messages.append(("A quantidade de energia é obrigatória.", expense_amount_energy))
                page.update()
            else:
                expense_amount_energy.border_color = None

            # Se houver mensagens de erro, exiba-as abaixo dos campos correspondentes
            if error_messages:
                # Organizar as mensagens abaixo dos campos correspondentes
                for i, (message, control) in enumerate(error_messages):
                    # Adicionar a mensagem abaixo do campo
                    page.add(ft.Text(message, color="red"), top=control.top + control.height + 10)
                
                # Atualizar a página imediatamente após adicionar as mensagens
                page.update()
                return  # Impede o cadastro se houver erro

            # Obter os valores dos campos
            expense_value_text = expense_value.value.replace("€", "").replace(".", "").replace(",", ".")
            expense_date_text = expense_date.value
            observation_expense_value = observation_expense.value
            expense_name_text = expense_name.value

            # Inicializar as variáveis de valor das quantidades específicas com valores vazios ou None
            expense_amount_liters_value = None
            expense_amount_cubic_meters_value = None
            expense_amount_energy_value = None

            # Obter o valor da despesa com base na opção selecionada
            if expense_name_text == "Gasolína" or expense_name_text == "Gasóleo":
                expense_amount_liters_value = expense_amount_liters.value
            elif expense_name_text == "GPL":
                expense_amount_cubic_meters_value = expense_amount_cubic_meters.value
            elif expense_name_text == "Recarga Bateria":
                expense_amount_energy_value = expense_amount_energy.value

            # Conectar ao banco de dados SQLite
            conn = sqlite3.connect("db_tvde_content_internal.db")
            cursor = conn.cursor()

            # Inserir os dados na tabela
            cursor.execute('''
                INSERT INTO expense (expense_value, expense_date, expense_name, expense_amount_liters, expense_amount_cubic_meters, expense_amount_energy, observation_expense)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (expense_value_text, expense_date_text, expense_name_text, expense_amount_liters_value, expense_amount_cubic_meters_value, expense_amount_energy_value, observation_expense_value))

            # Confirmar a transação e fechar a conexão
        
            if cursor.rowcount > 0:
                page_message_screen("Despesa cadastrada com sucesso!")
                page.go("/page_more_date")
            else:
                page_message_screen("Houve algum erro. Tente Novamente mais tarde!!!")
                page.go("/page_more_date")
           
            conn.commit()
            conn.close()        

            # Limpar os campos após o cadastro (se necessário)
            expense_value.value = ""
            expense_date.value = ""
            expense_name.value = None
            observation_expense.value = ""
            expense_amount_liters.value = ""
            expense_amount_cubic_meters.value = ""
            expense_amount_energy.value = ""

            # Atualizar a página para refletir a limpeza dos campos
            page.update()

        # Criação do botão para adicionar a despesa
        button_add_expense = ft.ElevatedButton(
            text="Cadastrar Despesa", 
            on_click=lambda e: cadastrar_despesa(),
        )

        # Adicionando os controles na página
        page.views.append(
            ft.View(
                "/page_expense",
                controls=[
                    header,
                    title_app(
                        icon=ft.Icon(ft.icons.MONEY_OFF_SHARP),
                        title=ft.Text("NOVA DESPESA", size=21),
                    ),
                    expense_value,
                    ft.Container(height=0.9),
                    expense_date,
                    ft.Container(height=0.9),
                    expense_name,
                    ft.Container(height=0.9),
                    expense_amount_liters,
                    expense_amount_cubic_meters,
                    expense_amount_energy,
                    observation_expense,
                    result_label,
                    ft.Container(height=0.9),
                    button_add_expense,
                    bottom_menu
                ]
            )
        )
        page.update()

    def page_more_date():
        page.views.clear()

        big_button_bolt = ft.Container(
                        width=180,
                        height=135,
                        bgcolor="#EFEFEF",
                        border_radius=21,
                        margin=10,
                        on_click=lambda e: page.go("/page_daily?param=Bolt"),
                        content=
                            ft.Column(  
                                controls=[
                                    ft.Image(src="https://i.ibb.co/FKM5tjP/icon-bolt51x51.png"),
                                    ft.Text("Diária Bolt")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
        )

        big_button_uber = ft.Container(
                        width=180,
                        height=135,
                        bgcolor="#EFEFEF",
                        border_radius=21,
                        on_click=lambda e: page.go("/page_daily?param=Uber"),
                        content=
                            ft.Column(  
                                controls=[
                                    ft.Image(src="https://i.ibb.co/5xGNqkc/icon-uber51x51.png"),
                                    ft.Text("Diária Uber")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
                            
        )


        big_button_expense = ft.Container(
                        width=180,
                        height=135,
                        bgcolor="#EFEFEF",
                        border_radius=21,
                        margin=10,
                        on_click=lambda e: page.go("/page_expense"),
                        content=
                            ft.Column(  
                                controls=[
                                    ft.Icon(ft.icons.MONEY_OFF_SHARP, size=48),
                                    ft.Text("Nova Despesa")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
        )

        
        big_button_new_goal = ft.Container(
                        width=180,
                        height=135,
                        bgcolor="#EFEFEF",
                        border_radius=21,
                        on_click=lambda e: page.go("/page_new_goal"),
                        content=
                            ft.Column(  
                                controls=[
                                    ft.Icon(ft.icons.ADD_CHART_OUTLINED, size=48),
                                    ft.Text("Novo Objetivo")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            )
        )


        page.views.append(
            ft.View(
                "page_more_date",
                controls=[
                    header,
                    title_app(
                        icon=ft.Icon(ft.icons.ADD_CIRCLE_OUTLINE_ROUNDED),
                        title=ft.Text("LANÇAMENTOS", size=21)
                    ),
                    ft.Row(
                        controls=[big_button_bolt, big_button_uber],
                    ),
                    ft.Row(
                        controls=[big_button_expense, big_button_new_goal],
                    ),
                    bottom_menu
                ]
            )
        )

        page.update()

    def page_daily(param):
        page.views.clear()

        def validate_fields():
            # Inicializa variáveis de erro para cada campo
            value_error = None
            trips_error = None
            date_error = None
            hour_error = None
        

            # Validação do campo de valor líquido (daily_value_field)
            if daily_value_field.value:
                try:
                    value = float(daily_value_field.value.replace('€ ', '').replace('.', '').replace(',', '.'))
                    if value <= 0:
                        value_error = "* O valor líquido deve ser maior que zero."
                except ValueError:
                    value_error = "* O valor líquido não está formatado corretamente."
            
            # Validação do campo de viagens realizadas (trips_made_field)
            if trips_made_field.value:
                try:
                    trips = int(trips_made_field.value)
                    if trips <= 0:
                        trips_error = "* O número de viagens realizadas deve ser maior que zero."
                except ValueError:
                    trips_error = "* O número de viagens deve ser um valor válido."
            else:
                trips_error = "* O campo de viagens realizadas é obrigatório e deve ser maior que zero."

            # Validação do campo de data (daily_date_field)
            if daily_date_field.value:
                try:
                    date_value = datetime.datetime.strptime(daily_date_field.value, "%d/%m/%Y")
                except ValueError:
                    date_error = "* A data não está no formato correto (DD/MM/AAAA)."
            else:
                date_error = "* A data da diária é obrigatória."

            # Validação do campo de tempo gasto (working_hours_field)
            if working_hours_field.value:
                try:
                    time_value = datetime.datetime.strptime(working_hours_field.value, "%H:%M")
                    if time_value.hour < 0 or time_value.hour > 23 or time_value.minute < 0 or time_value.minute > 59:
                        hour_error = "* Entre 00:00 e 23:59."
                except ValueError:
                    hour_error = "* Entre 00:00 e 23:59."
            else:
                hour_error = "* O campo é obrigatório."

            # Aplica as mensagens de erro nos campos correspondentes
            daily_value_field.error_text = value_error
            trips_made_field.error_text = trips_error
            daily_date_field.error_text = date_error
            working_hours_field.error_text = hour_error

            # Se qualquer erro ocorrer, desabilita os botões
            if value_error or trips_error or date_error or hour_error:
                btn_bolt.visible = False
                btn_bolt.disabled = True
                btn_uber.visible = False
                btn_uber.disabled = True
            else:
                btn_bolt.visible = True
                btn_bolt.disabled = False
                btn_uber.visible = True
                btn_uber.disabled = False

            # Atualiza os campos e botões
            daily_value_field.update()
            trips_made_field.update()
            daily_date_field.update()
            working_hours_field.update()
            btn_bolt.update()
            btn_uber.update()
            configure_buttons(param)

        def format_number_accounting(e):
                # Remove qualquer caractere que não seja dígito
                raw_value = ''.join(filter(str.isdigit, e.control.value))

                if raw_value:
                    # Adiciona vírgula para centavos, separando os dois últimos dígitos
                    if len(raw_value) > 2:
                        raw_value = raw_value[:-2] + ',' + raw_value[-2:]
                    else:
                        raw_value = '00,' + raw_value

                    # Converte para inteiro e formata com separador de milhar (ponto)
                    integer_part = raw_value.split(',')[0]
                    decimal_part = raw_value.split(',')[1]

                    # Formata a parte inteira com ponto como separador de milhar
                    formatted_integer = f"{int(integer_part):,}".replace(',', '.')

                    # Junta a parte inteira formatada com a parte decimal
                    formatted_value = f"{formatted_integer},{decimal_part}"

                else:
                    formatted_value = ""

                # Atualiza o TextField com o valor formatado
                e.control.value = formatted_value
                e.control.update()
            
        def format_number_only99(e):
        # Remove qualquer caractere que não seja dígito
            raw_value = ''.join(filter(str.isdigit, e.control.value))
            
            if raw_value:
                # Converte para inteiro e formata com separador de milhar
                integer_value = min(int(raw_value[:2]), 99)
                formatted_value = str(integer_value)
            else:
                formatted_value = ""

            # Atualiza o TextField com o valor formatado
            e.control.value = formatted_value
            e.control.update()

        def validate_date(e):
            # Chama a validação sempre que a data mudar
            validate_fields()
        
        def format_number_only999(e):
        # Remove qualquer caractere que não seja dígito
            raw_value = ''.join(filter(str.isdigit, e.control.value))
            
            if raw_value:
                # Converte para inteiro e formata com separador de milhar
                integer_value = min(int(raw_value[:3]), 999)
                formatted_value = str(integer_value)
            else:
                formatted_value = ""

            # Atualiza o TextField com o valor formatado
            e.control.value = formatted_value
            e.control.update()

        daily_value_field = ft.TextField(label=f"Valor líquido da {param}", prefix_text="€ ",
            border_radius=21, 
            text_size=18,
            on_change=format_number_accounting, 
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=15,               # Tamanho opcional
            ),
            helper_text=f"* Valor das corridas. Sem a % da {param}.",
            content_padding=ft.padding.symmetric(vertical=12, horizontal=12)
        )

        daily_value_tips_field = ft.TextField(label=f"Valor gorjetas da {param}", prefix_text="€ ",
            border_radius=21, 
            text_size=18,
            on_change=format_number_accounting,
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=15,               # Tamanho opcional
            ),
            content_padding=ft.padding.symmetric(vertical=12, horizontal=12)
        )
        
        date_picker = ft.DatePicker(on_change=None)  # on_change definido depois dinamicamente

        def pick_date(e, field):
            date_picker.on_change = lambda e: on_date_selected(e, field)
            date_picker.pick_date()

        def on_date_selected(e, field):
            if date_picker.value:
                field.value = date_picker.value.strftime("%d/%m/%Y")
                validate_date(e)
                page.update()
        
        daily_date_field = ft.TextField(
            label=f"Data da diária da {param}",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=15,          # Tamanho opcional
            ),
            on_change=validate_date,
            border_radius=21,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            helper_text="* Data da diária",
            content_padding=ft.padding.symmetric(vertical=6, horizontal=9),
            suffix=ft.IconButton(
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda e: pick_date(e, daily_date_field),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=21)  # Estilizando o botão para que ele acompanhe o arredondamento
                )
            )
        )

        def hour_validy(e):
            texto = e.control.value
            hour_error = None

            if not texto:
                hour_error = "* O campo de tempo gasto é obrigatório."
            else:
                # Remove tudo o que não for número
                texto = ''.join(filter(str.isdigit, texto))

                # Verifica se o texto tem pelo menos 4 caracteres (para hora e minutos)
                if len(texto) == 4:
                    # Corrige o formato para HH:MM
                    texto_corrigido = texto[:2] + ':' + texto[2:]
                    e.control.value = texto_corrigido
                    texto = texto_corrigido  # Atualiza a variável texto com o valor corrigido
                elif len(texto) > 4:
                    # Se o usuário tentar inserir mais de 4 caracteres, limitamos à quantidade necessária
                    texto_corrigido = texto[:2] + ':' + texto[2:4]
                    e.control.value = texto_corrigido
                    texto = texto_corrigido  # Atualiza a variável texto com o valor corrigido

                # Agora, validamos se a hora e os minutos são válidos
                if len(texto) == 5 and texto[2] == ":" and texto[:2].isdigit() and texto[3:].isdigit():
                    horas, minutos = texto.split(":")
                    if 0 <= int(horas) <= 23 and 0 <= int(minutos) <= 59:
                        e.control.border_color = ft.colors.GREEN
                    else:
                        hour_error = "* 00:00 e 23:59."
                        e.control.border_color = ft.colors.RED
                else:
                    hour_error = "* Use HH:MM."
                    e.control.border_color = ft.colors.RED

            # Atualiza a mensagem de erro
            e.control.error_text = hour_error
            e.control.update()

            # Verifica se todos os campos estão válidos
            validate_fields()

        working_hours_field = ft.TextField(
            label="Tempo gasto (HH:MM)",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=21,
            expand=True,
            on_change=lambda e: hour_validy(e)  # Chama a validação sempre que o campo for alterado
        )

        distance_traveled_field = ft.TextField(
            label="Distância percorrida",suffix_text="KMs",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=21,
            expand=True,
            on_change=format_number_only999
        )

        contatenate_textfield_field = ft.Container(
            ft.Row(
                controls=[working_hours_field, distance_traveled_field]
            )
        )

        trips_made_field = ft.TextField(
            label="Viagens realizadas",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=21,
            helper_text="* Viagens realizadas",
            on_change=format_number_only99
        )

        observation_field = ft.TextField(
            label="Observação",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=15,          # Tamanho opcional
            ),
            border_radius=21,
            text_size=18,
        )

        def save_daily_bolt_uber(param):
            # Validar o parâmetro
            if param not in ["Bolt", "Uber"]:
                page_message_screen("Parâmetro inválido!")
                return

            # Coletar os valores dos campos
            try:
                daily_value = float(daily_value_field.value.replace('.', '').replace(',', '.')) if daily_value_field.value else 0.0
                daily_value_tips = float(daily_value_tips_field.value.replace('.', '').replace(',', '.')) if daily_value_tips_field.value else 0.0
                daily_date = daily_date_field.value if daily_date_field.value else None
                working_hours = working_hours_field.value if working_hours_field.value else "00:00"
                distance_traveled = float(distance_traveled_field.value) if distance_traveled_field.value else 0.0
                trips_made = int(trips_made_field.value) if trips_made_field.value else 0
                observation = observation_field.value if observation_field.value else ""
            except ValueError as e:
                page_message_screen("Erro ao coletar os valores dos campos. Verifique os dados inseridos!")
                return

            # Escolher a tabela com base no parâmetro
            table_name = "Bolt" if param == "Bolt" else "Uber"

            # Conectar ao banco e inserir os dados
            try:
                conn = sqlite3.connect("db_tvde_content_internal.db")
                cursor = conn.cursor()
                cursor.execute(f"""
                INSERT INTO {table_name} 
                (daily_value, daily_value_tips, daily_date, working_hours, distance_traveled, trips_made, observation)
                VALUES (?,?,?,?,?,?,?)
                """, (daily_value, daily_value_tips, daily_date, working_hours, distance_traveled, trips_made, observation))
                
                conn.commit()

                if cursor.rowcount > 0:
                    page_message_screen(f"Diária {param} cadastrada com sucesso!!")
                else:
                    page_message_screen("Houve algum erro. Tente novamente mais tarde!")
            except sqlite3.Error as e:
                page_message_screen(f"Erro ao salvar os dados: {e}")
            finally:
                conn.close()

            # Limpar os campos após o cadastro
            daily_value_field.value = ""
            daily_value_tips_field.value = ""
            daily_date_field.value = ""
            working_hours_field.value = ""
            distance_traveled_field.value = ""
            trips_made_field.value = ""
            observation_field.value = ""
            page.update()

            # Ir para a página parcial
            page.go("/page_parcial")

        def configure_buttons(param):
            # Verifica o valor de 'param' e ajusta a visibilidade
            if param == "Bolt":
                btn_bolt.visible = True
                btn_uber.visible = False
            elif param == "Uber":
                btn_bolt.visible = False
                btn_uber.visible = True
            else:
                # Caso param seja inválido, torna ambos invisíveis
                btn_bolt.visible = False
                btn_uber.visible = False

            # Atualiza a página para refletir as mudanças
            page.update()

        btn_bolt = ft.ElevatedButton(
        text="Cadastrar Bolt",
        on_click=lambda _: save_daily_bolt_uber("Bolt"),
        visible=False,  # Inicialmente invisível
        disabled=True    # Inicialmente desabilitado
    )

        btn_uber = ft.ElevatedButton(
        text="Cadastrar Uber",
        on_click=lambda _: save_daily_bolt_uber("Uber"),
        visible=False,  # Inicialmente invisível
        disabled=True    # Inicialmente desabilitado
        )

        configure_buttons(param)
        
        page.overlay.append(date_picker)
        page.views.append(
            ft.View(
                "/page_daily",
                controls=[
                    header,
                    title_app(
                           icon = ft.Icon(ft.icons.MORE_TIME),
                           title = ft.Text(f"DIÁRIA {param.upper()}", size=21),
                    ),
                    ft.Container(height=0.9),
                    daily_value_field,
                    ft.Container(height=0.9),
                    trips_made_field,
                    ft.Container(height=0.9),
                    daily_date_field,
                    ft.Container(height=0.9),
                    daily_value_tips_field,
                    ft.Container(height=0.9),
                    contatenate_textfield_field,
                    ft.Container(height=0.9),
                    observation_field,
                    btn_bolt,
                    btn_uber,
                    bottom_menu
                ]
            )
        )
        page.update()

    def page_parcial():
        def search_user_name(email_login):
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="db_tvde_users_external"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT name, surname, email, account_type, date_start FROM users WHERE email = %s", (email_login,))
            resultado = cursor.fetchone()

            cursor.fetchall() 

            cursor.close()
            conn.close()

            if resultado:
                return  {
                    "name": resultado[0],
                    "account_type": resultado[3],
                    "surname": resultado[1],
                    "date_start": resultado[4]
                }  # Resultado[0] contém o nome do usuário...
            else:
                return None 
            
        global user_name
        global account_type
        global date_start
        global surname

        user_details = search_user_name(email_login.value)

        user_name = user_details["name"]
        surname = user_details["surname"]
        account_type = user_details["account_type"]
        date_start = user_details["date_start"]
        
        message_welcome = ft.Container(
            width=399,
            height=42,
            alignment=ft.Alignment(0, 0),
            content=ft.Text(f"Olá {user_name}, boa sorte!!!", size=15, weight=ft.FontWeight.BOLD,  text_align=ft.TextAlign.CENTER),
        )

        goal = ft.Row(
            controls=[
                ft.Container(
                    width=399,
                    height=87,
                    content=ft.Column(
                        controls=[
                            ft.Text("OBJETIVO GERAL", size=15, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                            ft.Text("€ 1.720", size=27, color=ft.colors.BLACK),
                            ft.Text("valores líquidos", size=12, color="#858585"),
                            ],
                            spacing=0, 
                            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza verticalmente na coluna
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
                    ),
                )
            ]
        )

        def details_goal(e):
            if details_goal.height == 0:  # Se o container estiver fechado
                details_goal.height = 99  # Expande o container
            else:
                details_goal.height = 0  # Fecha o container
            page.update()

        button = ft.ElevatedButton(
                text="« detalhes »",
                on_click=details_goal,
                width=120,  # Largura do botão
                height=27, # Define a ação de clique
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(
                size=12,  # Tamanho da fonte do botão
            ),
        )
        )
        button_container = ft.Container(
            content=button,
            alignment=ft.alignment.center,  # Centraliza o botão
        )

        details_goal = ft.Row(
            height=0,
            controls=[
                ft.Container(  
                    ft.Column(
                        width=193,
                        height=99,
                        controls=[
                            ft.Text("Início do Objetivo", size=15, weight=ft.FontWeight.BOLD),
                            ft.Text("12/09/2024",size=15),
                            ft.Text("Dias de Trabalho", size=15, weight=ft.FontWeight.BOLD),
                            ft.Text("24",size=15),
                            ft.Text("Despesas", size=15, weight=ft.FontWeight.BOLD),
                            ft.Text("€ 350,00", size=15)
                        ],
                        spacing=0, 
                    ),
                ),
                ft.Container(
                    ft.Column(
                        width=193,
                        height=99,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        controls=[
                            ft.Text("Fim do Objetivo", size=15, weight=ft.FontWeight.BOLD),
                            ft.Text("12/10/2024", size=15),
                            ft.Text("Folgas", size=15, weight=ft.FontWeight.BOLD),
                            ft.Text("6", size=15),
                            ft.Text("Ganhos até o momento", size=15, weight=ft.FontWeight.BOLD),
                            ft.Text("€ 1.365,00", size=15)
                        ],
                        spacing=0, 
                    ),
                ),
            ]
        )

        hourglass = ft.Row(
            controls=[
                ft.Container(
                    width=399,
                    height=99,
                    padding=0,
                    margin=0,
                    content=ft.Column(
                        controls=[
                            ft.Image(src="https://i.ibb.co/93ps7s5/hourglass.png", height=27, width=27),
                            ft.Container(
                                ft.Text("FALTAM 15 DIAS PARA FIM DO OBJETIVO", size=15, color="#858585"),
                                padding=ft.padding.only(bottom=21),
                            ),
                            ft.Container(
                                width=399,
                                height=30,
                                margin=0,
                                border=ft.border.only(bottom=ft.border.BorderSide(2, ft.colors.BLACK)),
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                          
                                            content=ft.Image(
                                                src="https://i.ibb.co/80MV450/flag.png",
                                            ),
                                        ),
                                        ft.Container(
                                            padding=ft.padding.only(top=9),
                                            content=ft.Image(
                                                src="https://i.ibb.co/RQcfZVd/car.png",
                                            ),
                                        ),
                                        ft.Container(
                                            padding=3,
                                            content=ft.Image(
                                                src="https://i.ibb.co/M5nXHpq/finish-line-5-stars.png",
                                            ),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),  
                            ),
                            ft.Container(
                                width=2,
                                height=15,
                                bgcolor="black",
                            )
                        ],
                        spacing=0, #remove espaçamento entre os elementos do Controls
                        horizontal_alignment="center", # Centraliza horizontalmente
                    ),
                ),
                
            ],
        )
        goal_today = ft.Row(
            controls=[
                ft.Container(
                    width=399,
                    height=123,
                    padding=0,
                    margin=0,
                    bgcolor="#EEEEEE",
                    border_radius=25,
                    content=ft.Column(
                        controls=[
                            ft.Text("PRÓXIMO OBJETIVO", size=15, color=ft.colors.BLACK),
                            ft.Text("€ 125.83", size=36, color="#15CD74", weight=ft.FontWeight.BOLD),
                            ft.Text("valores brutos", size=12, color="#B0B0B0"),
                            ],
                            spacing=0, 
                            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza verticalmente na coluna
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  #
                    ),
                )
            ],
            spacing=0,
        )
        button_bolt_uber = ft.Row(
            controls=[
                ft.Container(
                    width=399,
                    height=51,
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Image(
                                    src="https://i.ibb.co/kmjFKQ1/button-bolt.png",
                                    width=154,
                                    height=51,
                                ),
                                on_click=lambda e: page.go("/page_daily?param=Bolt")
                            ),
                            ft.Container(
                                content=ft.Image(
                                    src="https://i.ibb.co/RQFGzX5/button-uber.png",
                                    width=154,
                                    height=51,
                                ),
                                on_click=lambda e: page.go("/page_daily?param=Uber")
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                )
            ]
        )
            
        page.views.clear()
        page.views.append(
            ft.View(
                "/page_parcial",
                controls=[
                    bottom_menu,
                    header,
                    message_welcome,
                    goal_today,
                    hourglass,
                    goal,
                    button_bolt_uber,
                    details_goal,
                    button_container,
                    
                ]
            )
        )
        page.update()

    def page_register():
        page.views.clear()

        def validate_name(e):
            if len(name.value) > 3:
                name.error_text = None
            else:
                name.error_text = "O nome deve ter mais de 4 caracteres."
            name.update()
            validate_form()

        def validate_surname(e):
            if len(surname.value) > 3:
                surname.error_text = None
            else:
                surname.error_text = "O nome deve ter mais de 4 caracteres."
            surname.update()
            validate_form()
           
        def validate_email(e):
            global email_exist
            if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email.value):
                try:
                # Conectar ao banco de dados
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="db_tvde_users_external"  # Certifique-se de que este nome está correto
                    )
                    cursor = conn.cursor()

                    # Executar a consulta para verificar se o e-mail existe
                    cursor.execute("SELECT * FROM users WHERE email = %s", (email.value,))
                    result = cursor.fetchone()

                    # Verificar se o e-mail foi encontrado
                    if result:
                        email.error_text = "Email já cadastrado!"  # Mensagem se o e-mail existir
                        email_exist = True
                    else:
                        email.error_text = None
                        email_exist = False
                except mysql.connector.Error as error:
                    email.error_text = "Erro ao verificar o e-mail no banco de dados."
                    email_exist = False
            else:
                email.error_text = "O email digitado não é válido."
                email_exist = False
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
            if (len(name.value) > 4 and len(surname.value) > 4 and
                re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email.value) and
                password.value == password_confirm.value and password.value != "" and password_confirm.value != "" and not email_exist):
                button_to_db.disabled = False
            else:
                button_to_db.disabled = True
            button_to_db.update()

        def add_in_db(name, surname, email, password):
            # Concatenar prefixo e sufixo do telefone
            hash_password = sha256(password.encode()).hexdigest()
            
            # Conectar ao banco de dados
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="db_tvde_users_external"
            )
            cursor = conn.cursor()

            if name and email and password:
                cursor.execute(
                    """INSERT INTO users (name, surname, account_type, email, password, date_start) VALUES (%s, %s, %s, %s, %s, CURDATE())""",
                    (name, surname, "Básico", email, hash_password)
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
        email = ft.TextField(label="Email", border_radius=21, on_change=validate_email)
        password = ft.TextField(label="Password", password=True, can_reveal_password=True, border_radius=21)
        password_confirm = ft.TextField(label="Password confirm", password=True, can_reveal_password=True, border_radius=21, on_change=validate_password)
        
        button_to_db = ft.ElevatedButton(text="REGISTER", bgcolor={"disabled": "#d3d3d3", "": "#4CAF50"}, color="white", disabled=True,
                                          on_click=lambda e: add_in_db(name.value, surname.value, email.value, password.value))
        page.views.append(
            ft.View(
                "/register",
                controls=[
                    ft.Container(
                        ft.Image(src="https://i.ibb.co/SrqCT9S/logo.png"),
                    ),
                    ft.Text("Cadastro de Novo Usuário"),
                    ft.Row(controls=[name]),
                    ft.Row(controls=[surname]),
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
                        page_message_screen(f"Verifique seu email {field_email}, receberá um código para alterar o password.")
                        page.go("/page_new_password")
            
                except Exception as e:
                    print("Erro ao enviar o e-mail:", e)
                
            else:
                print("E-mail não encontrado.")

            #Fechar a conexão
            
    
        global field_email

        title = ft.Text("Recuperacao de senha")
        field_email = ft.TextField(label="Email", border_radius=21, on_change=validate_email)
        button_send = ft.ElevatedButton(text="Enviar", on_click=lambda e:verify_email_exist(field_email.value))

        page.views.append(
              
            ft.View(
                "/forget_password",
                controls=[
                    ft.Container(
                        ft.Image(src="https://i.ibb.co/SrqCT9S/logo.png"),
                        padding=90,
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
            validate_form()

        def validate_field_code(e):
            codigo_temporario
            if field_code.value == codigo_temporario:
                field_code.error_text = None
            else:
                field_code.error_text = "Código Errado!"
            field_code.update()
            validate_form()

        def validate_form():
            if (new_password.value == confirm_new_password.value and field_code.value == codigo_temporario and new_password.value != "" and  confirm_new_password != ""):
                button_updated_password.disabled = False
            else:
                button_updated_password.disabled = True
            button_updated_password.update()

        codigo_temporario
        field_email
        title = ft.Text("Criar novo password")
        field_code = ft.TextField(label="Code", border_radius=21, on_change=validate_field_code)
        new_password = ft.TextField(label="Novo password", border_radius=21, password=True, can_reveal_password=True)
        confirm_new_password = ft.TextField(label="Confirme o novo password", border_radius=21, password=True, can_reveal_password=True, on_change=validate_password)
        button_updated_password = ft.ElevatedButton(text="Alterar Passoword", bgcolor={"disabled": "#d3d3d3", "": "#4CAF50"}, color="white", disabled=True , on_click=lambda e:verify_code_email(field_code.value, new_password.value, field_email.value, codigo_temporario))
        page.views.append(
              
            ft.View(
                "/page_new_password",
                controls=[
                    ft.Container(
                        ft.Image(src="https://i.ibb.co/SrqCT9S/logo.png"),
                        padding=90,
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
            page_login()
        elif page.route == "/register":
            page_register()
        elif page.route == "/page_new_goal":
            page_new_goal()
        elif page.route == "/forget_password":
            page_forget_password()
        elif page.route == "/message_screen":
            page_message_screen()
        elif page.route == "/page_new_password":
            page_new_password()
        elif page.route == "/page_parcial":
            page_parcial()
        elif page.route == "/page_expense":
            page_expense()
        elif page.route == "/page_daily":
            page_daily()
        elif page.route == "/page_menu":
            page_menu()
        elif page.route == "/page_premium":
            page_premium()
        elif page.route == "/page_my_account":
            page_my_account()
        elif page.route == "/page_reports":
            page_reports()
        elif page.route == "/page_settings":
            page_settings()
        elif page.route == "/page_more_date":
            page_more_date()
        elif page.route.startswith("/page_daily"):
            # Captura o valor do parâmetro da URL
            param = page.route.split("?param=")[-1] if "?param=" in page.route else "Desconhecido"
            page_daily(param)

    # Definindo o handler para mudanças de rota
    page.on_route_change = route_change

    # Definindo a rota inicial
    page.go("/")

ft.app(target=main)