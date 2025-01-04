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

    header = ft.Row(
            controls=[
                ft.Container(
                    width=399,
                    height=66,
                    content=ft.Row(
                        controls=[
                            ft.Image(src="https://i.ibb.co/SrqCT9S/logo.png", width=154, height=51),
                            ft.IconButton(ft.icons.MENU, on_click=lambda _:  page.drawer.toggle(), icon_size=33),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        
                    ),
    
                )
            ]
        )

    bottom_menu = ft.BottomAppBar(
            content=ft.Row(
                [
                    ft.IconButton(ft.icons.ADD_CIRCLE_OUTLINE_ROUNDED, on_click=lambda _: page.go("/page_expense")),
                    ft.IconButton(ft.icons.DOCUMENT_SCANNER_OUTLINED, on_click=lambda _: page.snack_bar.show(ft.SnackBar(ft.Text("Busca clicada!")))),
                    ft.IconButton(ft.icons.HOME_OUTLINED, on_click=lambda _: page.go("/page_parcial", size=150)),
                    ft.IconButton(ft.icons.DOCUMENT_SCANNER_OUTLINED, on_click=lambda _: page.snack_bar.show(ft.SnackBar(ft.Text("Busca clicada!")))),
                    ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.snack_bar.show(ft.SnackBar(ft.Text("Configurações clicadas!")))),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            bgcolor="#EEEEEE",
            padding=10,
            height=60
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

        def format_number(e):
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

        goal_value_liquid = ft.TextField(label="Valor total da meta", prefix_text="€ ",
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
            date_picker.pick_date()

        def on_date_selected(e, field):
            if date_picker.value:
                field.value = date_picker.value.strftime("%d/%m/%Y")
                page.update()
        
        goal_start = ft.TextField(
            label="Início da meta",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            width=page.width * 0.47,
            border_radius=21,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            helper_text="* Data do Início da meta",
            content_padding=ft.padding.symmetric(vertical=6, horizontal=9),
            suffix=ft.IconButton(
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda e: pick_date(e, goal_start),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=21)  # Estilizando o botão para que ele acompanhe o arredondamento
                )
            )
        )

        goal_end = ft.TextField(
            label="Fim da meta",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            width=page.width * 0.47,
            border_radius=21,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            helper_text="* Data do Fim da Meta",
            content_padding=ft.padding.symmetric(vertical=6, horizontal=9),
            suffix=ft.IconButton(
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda e: pick_date(e, goal_end)
            )
        )

        goal_dates = ft.Container(
            ft.Row(
                controls=[goal_start, goal_end]
            )
        )
        day_off = ft.TextField(
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
        
        fleet_discount = ft.TextField(
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
        tax_discount = ft.TextField(
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

        global button_salve
        button_salve = ft.ElevatedButton(
            text="SALVAR", bgcolor={"disabled": "#d3d3d3", "": "#4CAF50"}, color="white"
        )
        global space_space_space

        space_space_space = ft.Container(height=0.9)
    
        page.overlay.append(date_picker)
        page.views.append(
            ft.View(
                "/page_new_goal",
                controls=[
                    header,
                    title_app(
                           icon = ft.Icon(ft.icons.MORE_TIME),
                           title = ft.Text("NOVO OBJETIVO", size=18),
                    ),
                    space_space_space,
                    goal_value_liquid,
                    space_space_space,
                    goal_dates,
                    space_space_space,
                    day_off,
                    space_space_space,
                    fleet_discount,
                    space_space_space,
                    tax_discount,    
                    space_space_space,
                    button_salve,
                    bottom_menu
                ]
            )
        )
        page.update()

    def page_expense():
        page.views.clear()

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

        global expense_value
        expense_value = ft.TextField(label="Valor da despesa", prefix_text="€ ",
            border_radius=21, 
            text_size=18,
            on_change=format_number_accounting,
            label_style=ft.TextStyle(
              color="#AAAAAA",  # Cor do label
              size=14,          # Tamanho opcional
            ),
            helper_text="* Valor líquido pretendido ao fim da meta.",
            content_padding=ft.padding.symmetric(vertical=12, horizontal=12)
        )

        def pick_date(e, field):
            # Adiciona o DatePicker à página antes de abrir
            page.add(date_picker2)
            page.open(date_picker2)  # Usa o método correto para abrir o DatePicker

        def on_date_selected(e, field):
            if date_picker2.value:
                # Formata a data selecionada no formato "dd/mm/yyyy"
                field.value = date_picker2.value.strftime("%d/%m/%Y")
                page.update()

        # Criação do DatePicker
        date_picker2 = ft.DatePicker(
            on_change=lambda e: on_date_selected(e, expense_date)  # Define o on_change diretamente
        )

        # Criação do TextField para data
        expense_date = ft.TextField(
            label="Data da despesa",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
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
        
        global observation

        observation = ft.TextField(
            label="Observação",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            border_radius=21,
            text_size=18,
            helper_text="*Observação",
        )
    
        dropdown = ft.Dropdown(
            label="Despesas:",  # Texto de rótulo do dropdown
            options=[
                ft.dropdown.Option("Manutenção"),
                ft.dropdown.Option("Gasolína"),
                ft.dropdown.Option("Gasóleo"),
                ft.dropdown.Option("GPL"),
                ft.dropdown.Option("Recarga Bateria"),
                ft.dropdown.Option("Alimentação"),
                ft.dropdown.Option("Portagem")
            ],
            on_change=lambda e: on_option_selected(e),  # Defina uma função para tratar a mudança
            border_radius=21,
            content_padding=ft.padding.symmetric(vertical=6, horizontal=9),
            
        )
        def on_option_selected(e):
            # Alterar a cor de fundo e do texto dependendo da seleção
            if e.control.value == "Manutenção":
                dropdown.bgcolor = "#E0E0E0"  # Cor de fundo quando "Opção 1" é selecionada
                dropdown.style = ft.TextStyle(color="#FF5722")  # Cor do texto para "Opção 1"
            elif e.control.value == "Gasolína":
                dropdown.bgcolor = "#FFEB3B"  # Cor de fundo quando "Opção 2" é selecionada
                dropdown.style = ft.TextStyle(color="#000000")  # Cor do texto para "Opção 2"
            elif e.control.value == "Gasóleo":
                dropdown.bgcolor = "#B25900"  # Cor de fundo quando "Opção 3" é selecionada
                dropdown.style = ft.TextStyle(color="#FFFFFF")  # Cor do texto para "Opção 3"
            elif e.control.value == "GPL":
                dropdown.bgcolor = "#4CAF50"  # Cor de fundo quando "Opção 3" é selecionada
                dropdown.style = ft.TextStyle(color="#FFFFFF")  # Cor do texto para "Opção 3"
            elif e.control.value == "Recarga Bateria":
                dropdown.bgcolor = "#B200B2"  # Cor de fundo quando "Opção 3" é selecionada
                dropdown.style = ft.TextStyle(color="#FFFFFF")  # Cor do texto para "Opção 3"
            elif e.control.value == "Alimentação":
                dropdown.bgcolor = "#FF7F00"  # Cor de fundo quando "Opção 3" é selecionada
                dropdown.style = ft.TextStyle(color="#FFFFFF")  # Cor do texto para "Opção 3"
            else:
                dropdown.bgcolor = "#00B200"  # Cor de fundo quando "Opção 4" é selecionada
                dropdown.style = ft.TextStyle(color="#CCCCCC")  # Cor do texto para "Opção 4"
            
            page.update()  # Atualizar a página após a mudança

        page.views.append(
            ft.View(
                "/page_expense",
                controls=[
                    header,
                    title_app(
                           icon = ft.Icon(ft.icons.MONEY_OFF_SHARP),
                           title = ft.Text("NOVA DESPESA", size=18),
                    ),
                    expense_value,
                    space_space_space,
                    expense_date,
                    space_space_space,
                    dropdown,
                    space_space_space,
                    observation,
                    space_space_space,
                    button_salve,
                    bottom_menu
                ]
            )
        )
        page.update()
    def page_daily_bolt(param):
        page.views.clear()

        def format_number(e):
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

        daily_value_bolt = ft.TextField(label=f"Valor líquido da {param}", prefix_text="€ ",
            border_radius=21, 
            text_size=18,
            on_change=format_number,
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,               # Tamanho opcional
            ),
            helper_text=f"* *Valor líquido das corridas. Sem a % da {param}.",
            content_padding=ft.padding.symmetric(vertical=12, horizontal=12)
        )

        daily_value_bolt_tips = ft.TextField(label=f"Valor gorjetas da {param}", prefix_text="€ ",
            border_radius=21, 
            text_size=18,
            on_change=format_number,
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,               # Tamanho opcional
            ),
            helper_text="* Valor das gorjetas",
            content_padding=ft.padding.symmetric(vertical=12, horizontal=12)
        )
        
        date_picker = ft.DatePicker(on_change=None)  # on_change definido depois dinamicamente

        def pick_date(e, field):
            date_picker.on_change = lambda e: on_date_selected(e, field)
            date_picker.pick_date()

        def on_date_selected(e, field):
            if date_picker.value:
                field.value = date_picker.value.strftime("%d/%m/%Y")
                page.update()
        
        daily_bolt_date = ft.TextField(
            label=f"Data da diária da {param}",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            width=page.width * 0.47,
            border_radius=21,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            helper_text="* Data da diária",
            content_padding=ft.padding.symmetric(vertical=6, horizontal=9),
            suffix=ft.IconButton(
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda e: pick_date(e, daily_bolt_date),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=21)  # Estilizando o botão para que ele acompanhe o arredondamento
                )
            )
        )

        def hour_validy(e):
            texto = e.control.value
            if not texto:
                return
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
                    e.control.border_color = ft.colors.RED
            else:
                e.control.border_color = ft.colors.RED
                
            page.update()

        working_hours = ft.TextField(
            label="Hora trabalhadas (HH:MM)",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=21,
            on_change=hour_validy
        )

        distance_traveled = ft.TextField(
            label="Distância percorrida",suffix_text="KMs",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=21,
            on_change=format_number_only999
        )

        trips_made = ft.TextField(
            label="Viagens realizadas",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=21,
            on_change=format_number_only99
        )

        button_salve = ft.ElevatedButton(
            text="SALVAR", bgcolor={"disabled": "#d3d3d3", "": "#4CAF50"}, color="white"
        )

        space_space_space = ft.Container(height=0.9)
        observation = ft.TextField(
            label="Observação",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            border_radius=21,
            text_size=18,
            helper_text="*Observação",
        )

        page.overlay.append(date_picker)
        page.views.append(
            ft.View(
                "/page_daily_bolt",
                controls=[
                    header,
                    title_app(
                           icon = ft.Icon(ft.icons.MORE_TIME),
                           title = ft.Text(f"DIÁRIA {param.upper()}", size=18),
                    ),
                    space_space_space,
                    daily_value_bolt,
                    space_space_space,
                    daily_value_bolt_tips,
                    space_space_space,
                    daily_bolt_date,
                    space_space_space,
                    working_hours,
                    space_space_space,
                    distance_traveled,
                    space_space_space,
                    trips_made,
                    space_space_space,
                    observation,
                    button_salve,
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

            cursor.execute("SELECT name FROM users WHERE email = %s", (email_login,))
            resultado = cursor.fetchone()

            cursor.fetchall() 

            cursor.close()
            conn.close()

            if resultado:
                return resultado[0]  # Resultado[0] contém o nome do usuário
            else:
                return None 

        user_name = search_user_name(email_login.value)

        message_welcome = ft.Container(
            width=399,
            height=42,
            alignment=ft.Alignment(0, 0),
            content=ft.Text(f"Hi {user_name}, good luck today! :)", size=15, weight=ft.FontWeight.BOLD,  text_align=ft.TextAlign.CENTER),
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
                                            padding=3,
                                            content=ft.Image(
                                                src="https://i.ibb.co/80MV450/flag.png",
                                            ),
                                        ),
                                        ft.Container(
                                            content=ft.Image(
                                                src="https://i.ibb.co/RQcfZVd/car.png",
                                                width=154,
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
                            ft.Text("OBJETIVO DE HOJE", size=15, color=ft.colors.BLACK),
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
                                on_click=lambda e: page.go("/page_daily_bolt?param=Bolt")
                            ),
                            ft.Container(
                                content=ft.Image(
                                    src="https://i.ibb.co/RQFGzX5/button-uber.png",
                                    width=154,
                                    height=51,
                                ),
                                on_click=lambda e: page.go("/page_daily_bolt?param=Uber")
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
                    """INSERT INTO users (name, surname, email, password) VALUES (%s, %s, %s, %s)""",
                    (name, surname, email, hash_password)
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
        elif page.route == "/page_daily_bolt":
            page_daily_bolt()
        elif page.route.startswith("/page_daily_bolt"):
            # Captura o valor do parâmetro da URL
            param = page.route.split("?param=")[-1] if "?param=" in page.route else "Desconhecido"
            page_daily_bolt(param)

    # Definindo o handler para mudanças de rota
    page.on_route_change = route_change

    # Definindo a rota inicial
    page.go("/")

ft.app(target=main)