import flet as ft
import re
import mysql.connector
from datetime import datetime
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
                ft.PopupMenuItem(icon=ft.icons.INSERT_CHART_OUTLINED, text="Relatórios", on_click=lambda _: page.go("/page_reports")),
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
                            pb,
                            ft.Image(src="https://i.ibb.co/SrqCT9S/logo.png", width=154, height=51)
                            
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                    ),
                )
            ]
        )
    def on_change(e):
        destinos = ["/page_parcial", "/page_more_date", "/page_reports", "/page_settings"]
        page.go(destinos[e.control.selected_index])

    bottom_menu = ft.BottomAppBar(
        content=ft.NavigationBar(
            indicator_color="#19D278",
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.HOME_OUTLINED, label="Início"),
                ft.NavigationBarDestination(icon=ft.icons.ADD_CIRCLE_OUTLINE_ROUNDED, label="Novo dado"),
                ft.NavigationBarDestination(icon=ft.icons.INSERT_CHART_OUTLINED, label="Relatórios"),
                ft.NavigationBarDestination(icon=ft.icons.SETTINGS, label="Config"),
            ],
            on_change=on_change,
        ),
        bgcolor="#EEEEEE",
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

        with sqlite3.connect("db_tvde_content_internal.db", detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()  # Inicializando o cursor

            # Recuperar as datas 'goal_start' e 'goal_end' da tabela 'goal'
            cursor.execute("SELECT goal_start, goal_end FROM goal ORDER BY id DESC LIMIT 1")
            goal_result = cursor.fetchone()

            if goal_result:
                goal_start = datetime.strptime(goal_result[0], '%d/%m/%Y')  # Convertendo string para datetime
                goal_end = datetime.strptime(goal_result[1], '%d/%m/%Y')
            else:
                goal_start, goal_end = None, None

            def fetch_expenses(start_date, end_date):
                """Consulta as despesas entre start_date e end_date."""
                cursor.execute(""" 
                    SELECT SUM(expense_value) 
                    FROM expense 
                    WHERE date(substr(expense_date, 7, 4) || '-' || substr(expense_date, 4, 2) || '-' || substr(expense_date, 1, 2)) 
                    BETWEEN date(?) AND date(?)
                """, (start_date, end_date))
                result = cursor.fetchone()
                return result[0] if result else 0.0
            
            def fetch_goal_from_db():
                # Executar a consulta para obter o valor do objetivo, fleet_discount e tax_discount
                cursor.execute("SELECT goal, fleet_discount, tax_discount FROM goal ORDER BY id DESC LIMIT 1")  # Ajuste conforme necessário
                result = cursor.fetchone()

                if result:
                    # Garantir que goal_value, fleet_discount e tax_discount sejam do tipo float
                    try:
                        goal_value = float(result[0])  # Convertendo para float
                        # Formatar o valor final para exibição
                        return f"{goal_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    except ValueError:
                        return "Erro ao converter os valores"
                else:
                    return "€ 0.00"
                
            def fetch_goal_gross():
                cursor.execute("SELECT goal_gross FROM goal ORDER BY id DESC LIMIT 1")
                goal_gross_result = cursor.fetchone()
                
                if goal_gross_result and goal_gross_result[0] is not None:
                    return float(goal_gross_result[0])
                return 0.0
            
            def fetch_goal_sum_tip(goal_start, goal_end):
                cursor.execute("""
                    SELECT 
                        (SELECT COALESCE(SUM(daily_value_tips), 0) 
                        FROM uber 
                        WHERE daily_date >= ? AND daily_date <= ?) +
                        (SELECT COALESCE(SUM(daily_value_tips), 0) 
                        FROM bolt 
                        WHERE daily_date >= ? AND daily_date <= ?)
                """, (goal_start, goal_end, goal_start, goal_end))
                
                total_tips = cursor.fetchone()[0]  # Pega o resultado da soma
                return float(total_tips) if total_tips is not None else 0.0

            
            def fetch_last_fleet_discount():
                # Consulta SQL para pegar o último valor da coluna "fleet_discount"
                query = "SELECT fleet_discount FROM goal ORDER BY id DESC LIMIT 1"  # Altere 'sua_tabela' para o nome da tabela correta
                
                cursor.execute(query)
                result = cursor.fetchone()
                
                # Se encontrou algum valor, retorna ele
                if result:
                    return result[0]  # O valor de "fleet_discount" estará na primeira posição
                else:
                    return None  # Se não encontrar nenhum valor, retorna None
                # Função para criar um botão grande
        def create_big_button(icon, text, on_click_action):
            return ft.Container(
                width=165,
                height=121,
                bgcolor="#EFEFEF",
                border_radius=21,
                margin=ft.Margin(top=6, bottom=6, left=15, right=6),
                on_click=on_click_action,
                content=ft.Column(
                    controls=[
                        icon,
                        ft.Text(text)  # Aqui garantimos que text é envolvido em ft.Text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        goal_value2 = fetch_goal_from_db()

        goal_gross2 = fetch_goal_gross()

        goal_sum_tips = fetch_goal_sum_tip(goal_start, goal_end)

        expenses = fetch_expenses(goal_start.strftime('%Y-%m-%d'), goal_end.strftime('%Y-%m-%d'))

        goal_value2_float = float(goal_value2.replace(",", ".")) if isinstance(goal_value2, str) else float(goal_value2)
        goal_sum_tips_float = float(goal_sum_tips.replace(",", ".")) if isinstance(goal_sum_tips, str) else float(goal_sum_tips)

        # Soma os valores já convertidos
        total_value = total_gain + goal_sum_tips_float

        fleet_discount = fetch_last_fleet_discount()

        if fleet_discount is None:
            fleet_discount_float = 0.0  # Se não houver desconto, assume 0%
        else:
            # Garantir que o valor está no formato correto
            fleet_discount_float = float(fleet_discount.replace(",", ".")) if isinstance(fleet_discount, str) else float(fleet_discount)

        fleet_discount_value = total_gain * (fleet_discount_float / 100)


        panel_reports = ft.Container(
        width=381,
        height=234,
        bgcolor="#EFEFEF",
        border_radius=21,
        margin=6,
        padding=12,
        content=ft.Column(
            spacing=5,  # Adiciona espaçamento entre os itens
            controls=[
                # Cabeçalho com ícone
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.TRENDING_UP, size=24, color="blue"),  # Ícone de tendência
                        ft.Text("Resumo do Objetivo", size=15),
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Divider(),  # Linha divisória para separar título do conteúdo

                # Layout melhorado usando Colunas para alinhar os textos
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Objetivo Líquido:", size=12, weight=ft.FontWeight.BOLD),
                                ft.Text("Gorjetas:", size=12, weight=ft.FontWeight.BOLD),
                                ft.Text("Ganhos até agora + Gorjetas:", size=12, weight=ft.FontWeight.BOLD),
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        
                        ft.Column(
                            controls=[
                                ft.Text(f"€ {goal_value2_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), size=12),
                                ft.Text(f"€ {goal_sum_tips_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), size=12),
                                ft.Text(f"€ {total_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), size=12),
                            ],
                            alignment=ft.MainAxisAlignment.END
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(),

                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Despesas:", size=12, weight=ft.FontWeight.BOLD),
                                ft.Text("Pago a frota:", size=12, weight=ft.FontWeight.BOLD),
                                ft.Text("Objetivo Bruto:", size=12, weight=ft.FontWeight.BOLD),
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(f"€ {expenses if expenses is not None else 0.0:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), size=12),
                                ft.Text(f"€ {fleet_discount_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), size=12),
                                ft.Text(f"€ {goal_gross2:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), size=12),
                            ],
                            alignment=ft.MainAxisAlignment.END
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
            ]
        )
    )


        primeira = ft.Container(
            content=ft.Row(
                controls=[
                    create_big_button(
                        ft.Icon(ft.icons.EURO, size=39),
                        "Despesas",
                        lambda e: page.go("/page_reports_expense")
                    ),
                    create_big_button(
                        ft.Icon(ft.icons.ADD_TO_HOME_SCREEN, size=36),
                        "Plataforma",
                        lambda e: page.go("/page_expense")
                    )
                ]
            )
        )

        segunda = ft.Container(
            content=ft.Row(
                controls=[
                    create_big_button(
                        ft.Icon(ft.icons.DIRECTIONS_CAR, size=36),
                        "Lucros",
                        lambda e: page.go("/page_expense")
                    ),
                    create_big_button(
                        ft.Icon(ft.icons.CALENDAR_MONTH, size=36), 
                        "Mensal", 
                        lambda e: page.go("/page_expense")
                    )
                ]
            )
        )



        page.views.append(
            ft.View(
                "/page_reports",
                controls=[
                    header,
                    title_app(
                           icon = ft.Icon(ft.icons.INSERT_CHART_OUTLINED),
                           title = ft.Text("RELATÓRIOS", size=21),
                    ),
                    panel_reports,
                    primeira,
                    segunda,
                    bottom_menu
                ]
            )
        )

        page.update()


    def page_reports_expense():
        page.views.clear()

        selected_date_range = ft.Container(
            width=390,  # Defina o tamanho do contêiner conforme necessário
            alignment=ft.alignment.center,  # Centraliza o texto dentro do contêiner
            content=ft.Text(
                "Selecione um intervalo de datas:",
                size=15,
                weight=ft.FontWeight.BOLD,
            ),
        )

        # Criando o DatePicker
        date_picker = ft.DatePicker(on_change=None)  # on_change será atribuído dinamicamente

        # Função para abrir o DatePicker ao clicar no ícone de calendário
        def pick_date(e, field):
            date_picker.on_change = lambda e: on_date_selected(e, field)
            page.open(date_picker)

        # Função para tratar a seleção da data
        def on_date_selected(e, field):
            if date_picker.value:
                field.value = date_picker.value.strftime("%d/%m/%Y")
                page.update()

        # Campos para seleção de data com 'expand' ativado para torná-los expansíveis
        start_date_field = ft.TextField(
            label="Data de Início",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            on_change=None,  # A validação de data será feita dinamicamente
            width=140,       # Ajustando a largura para se ajustarem lado a lado
            border_radius=21,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            content_padding=ft.padding.symmetric(vertical=6, horizontal=9),
            expand=True,  # Tornando o campo expansível
            suffix=ft.IconButton(
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda e: pick_date(e, start_date_field),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=21)  # Estilizando o botão para que ele acompanhe o arredondamento
                )
            )
        )

        end_date_field = ft.TextField(
            label="Data de Fim",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            on_change=None,  # A validação de data será feita dinamicamente
            width=140,       # Ajustando a largura para se ajustarem lado a lado
            border_radius=21,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            content_padding=ft.padding.symmetric(vertical=6, horizontal=9),
            expand=True,  # Tornando o campo expansível
            suffix=ft.IconButton(
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda e: pick_date(e, end_date_field),
            )
        )

        # Container que engloba os campos de data lado a lado
        date_range_container = ft.Container(
            width=390,
            alignment=ft.alignment.center,
            content=ft.Column(
                controls=[
                    ft.Row(  # Usando Row para colocar os campos lado a lado
                        controls=[
                            start_date_field,
                            end_date_field,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER  # Ajustado para alinhar corretamente os campos
                    ),
                    # Centralizando o botão
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Gerar Relatório",  # Texto do botão
                                on_click=lambda e: generate_report(start_date_field, end_date_field),  # Função a ser chamada ao clicar
                                width=200,  # Largura do botão
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=21)  # Botão com borda arredondada
                                )
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER  # Alinhando o botão ao centro dentro do Row
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

        # Variável para armazenar a mensagem do relatório
        report_message = ft.Text("", size=12, text_align=ft.TextAlign.END )
        # Certifique-se de que os valores são float
        total_liters = 0
        total_energy = 0
        total_cubic_meters = 0
        total_expense = 0

        def generate_report(start_date_field, end_date_field):
            start_date = start_date_field.value
            end_date = end_date_field.value
            message = f"Relatório de {start_date} a {end_date}"
            report_message.value = message  # Exibe a mensagem ao lado do título "Despesas"
            
            # Inicializa as variáveis com 0 antes de fazer a consulta
      
            # Verifica se as datas estão preenchidas
            if not start_date or not end_date:
                report_message.value = "Preencha ambas as datas."
                page.update()
                return

            try:
                print("Conectando ao banco de dados...")  # Depuração
                conn = sqlite3.connect("db_tvde_content_internal.db")
                cursor = conn.cursor()

                print("Executando consulta SQL...")  # Depuração
                query = """
                SELECT 
                    COALESCE(SUM(expense_amount_liters), 0) AS total_liters,
                    COALESCE(SUM(expense_amount_energy), 0) AS total_energy,
                    COALESCE(SUM(expense_amount_cubic_meters), 0) AS total_cubic_meters,
                    COALESCE(SUM(expense_value), 0) AS total_expense
                FROM expense
                WHERE expense_date BETWEEN ? AND ?
                """
                cursor.execute(query, (start_date, end_date))
                result = cursor.fetchone()
                print("Resultado da consulta:", result)  # Depuração

                # Atribui os resultados se existirem, caso contrário mantém 0
                if result:
                    total_liters, total_energy, total_cubic_meters, total_expense = result
                else:
                    total_liters, total_energy, total_cubic_meters, total_expense = 0
                conn.close()

            except Exception as e:
                print(f"Erro: {str(e)}")  # Depuração
                report_message.value = f"Erro ao gerar o relatório: {str(e)}"
                page.update()
                return
            
            total_liters = float(total_liters)
            total_energy = float(total_energy)
            total_cubic_meters = float(total_cubic_meters)
            total_expense = float(total_expense)

            # Atualiza a interface com os resultados
            report_message.value = (
                f"🔹 Gasolina Litros: € {total_liters:.2f}\n"
                f"🔹 Energia: €{total_energy:.2f}\n"
                f"🔹 Gás Natural: €{total_cubic_meters:.2f}\n"
                f"🔹 Total de Despesas: €{total_expense:.2f}"
            )
            page.update()

        # Criação do botão para gerar relatório
        generate_report_button = ft.ElevatedButton(
            "Gerar Relatório", 
            on_click=lambda e: generate_report(start_date_field, end_date_field)
        )

        # Adicionando a tela ao "views" com o botão e o resultado do relatório
        page.views.append(
            ft.View(
                "/page_reports",
                controls=[
                    header,
                    title_app(
                        icon=ft.Icon(ft.icons.EURO),
                        title=ft.Text("RELATÓRIO DE DESPESAS", size=21),
                    ),
                    ft.Column(
                        controls=[
                            selected_date_range,
                            ft.Container(),
                            date_range_container,
                            ft.Container(),  # Container centralizado
                        ],
                    ),
                    ft.Container(
                        width=390,
                        bgcolor="#EFEFEF",
                        border_radius=21,
                        margin=6,
                        padding=12,
                        content=ft.Column(
                            spacing=5,
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                ft.Icon(ft.icons.RECEIPT_LONG, size=20, color="blue"),
                                                ft.Text("Despesas", size=15, weight=ft.FontWeight.BOLD),
                                            ],
                                            alignment=ft.MainAxisAlignment.START,
                                        ),
                                        ft.Row(
                                            controls=[report_message],
                                            alignment=ft.MainAxisAlignment.END,  # Alinha o report_message à direita
                                            expand=True,  # Garante que o espaço à direita será usado para alinhar à direita
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                ft.Divider(),
                                ft.Row(
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text("Gasolina:", size=12),
                                                ft.Text("Gasóleo:", size=12),
                                                ft.Text("Gás Natural:", size=12),
                                                ft.Text("Carga Energia:", size=12),
                                                ft.Text("Manutenção:", size=12),
                                                ft.Text("Comissão do Operador(Frota):", size=12),
                                                ft.Text("Portagem:", size=12),
                                                ft.Text("Alimentação:", size=12),
                                                ft.Text("Seguro:", size=12),
                                                ft.Text("Impostos:", size=12),
                                                ft.Text("Outros custos:", size=12),
                                            ],
                                            alignment=ft.MainAxisAlignment.START
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Text(f"€ {total_liters:.2f}", size=12),
                                                ft.Text(f"€ {total_energy:.2f}", size=12),
                                                ft.Text(f"€ {total_cubic_meters:.2f}", size=12),
                                                ft.Text(f"€ {total_expense:.2f}", size=12),
                                            ],
                                            alignment=ft.MainAxisAlignment.END
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                generate_report_button,  # Botão para gerar o relatório
                            ]
                        )
                    ),
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
                # Conectar ao banco SQLite para verificar metas
                    conn_sqlite = sqlite3.connect("db_tvde_content_internal.db")
                    cursor_sqlite = conn_sqlite.cursor()

                    # Executar uma consulta para buscar o valor de goal_successful
                    cursor_sqlite.execute("SELECT goal_successful FROM goal ORDER BY id DESC LIMIT 1")
                    goal_successful = cursor_sqlite.fetchone()

                    cursor_sqlite.execute("SELECT COUNT(*) FROM goal")
                    meta_count = cursor_sqlite.fetchone()[0]

                    # Verificar se o valor foi encontrado e retornar o resultado
                    if goal_successful:
                        goal_successful = goal_successful[0]  # Se encontrar o valor
                    else:
                        goal_successful = "default_value"  # Valor padrão se não encontrar nenhum

                    conn_sqlite.close()

                    # Redirecionar o usuário com base na existência de metas
                    if meta_count > 0 and goal_successful == "negativo":
                        page.go("/page_parcial")
                    elif meta_count > 0 and goal_successful == "positivo":
                        page_message_screen("Parabéns vc bateu a meta!!!")
                        time.sleep(3)
                        page.go("/page_new_goal")  # Página principal
                        
                    else:
                        page.go("/page_new_goal")  # Página de nova meta
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
                    start_date = datetime.strptime(goal_start_field.value.strip(), "%d/%m/%Y")
                else:
                    start_date_error = "Use DD/MM/AAAA."
                    valid = False

                # Verifica se o campo de fim tem um valor válido
                if goal_end_field.value.strip():
                    end_date = datetime.strptime(goal_end_field.value.strip(), "%d/%m/%Y")
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

            validate_button_state()  # Atualiza o estado do botão

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
            
            validate_button_state()  # Atualiza o estado do botão

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
            helper_text="Quantos dias terá de folga.",
            content_padding=ft.padding.symmetric(vertical=12, horizontal=9)
        )
        
        fleet_discount_field = ft.TextField(
            label="Taxa da Frota",
            on_change=format_number_only99,
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,               # Tamanho opcional
            ),
            suffix_text="%",
            border_radius=21,
            text_size=18,
            keyboard_type=ft.KeyboardType.DATETIME,
            helper_text="Taxa da frota.",
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
       
        def validate_button_state():
            # Verifica se todos os campos estão validados
            valid = True

            # Verifica a validação da data
            if goal_start_field.error_text or goal_end_field.error_text:
                valid = False

            # Verifica a validação do valor
            if goal_field.error_text:
                valid = False

            # Verifica a validação do campo "day_off", se necessário
            if day_off_field.error_text:
                valid = False

            # Verifica a validação do campo de descontos
            if fleet_discount_field.error_text or tax_discount_field.error_text:
                valid = False

            # Ativa ou desativa o botão conforme o estado de validação
            button_salve.disabled = not valid
            button_salve.update()

        
        def save_goal(e):
            global day_off
            global goal_start
            global goal_end
            global fleet_discount
            # Coletar os valores dos campos
            goal = float(goal_field.value.replace('.', '').replace(',', '.'))
            goal_start = goal_start_field.value
            goal_end = goal_end_field.value
            day_off = int(day_off_field.value)
            fleet_discount = float(fleet_discount_field.value)
            tax_discount = float(tax_discount_field.value)

            # Verifica se o campo de desconto de imposto não está vazio antes de converter
            tax_discount_value = tax_discount_field.value.strip()  # Remove espaços em branco
            if tax_discount_value:  # Verifica se não está vazio
                tax_discount = float(tax_discount_value)
            else:
                tax_discount = 0.0  # Atribui um valor padrão (0.0) se estiver vazio
            
            # Conectar ao banco para verificar se as datas já existem
            conn = sqlite3.connect("db_tvde_content_internal.db")
            cursor = conn.cursor()

            try:
                # Verificar se já existe um objetivo com as mesmas datas de início e fim
                cursor.execute("""
                    SELECT 1 FROM goal WHERE goal_start = ? AND goal_end = ?
                """, (goal_start, goal_end))

                # Se encontrar um resultado, significa que já existe
                if cursor.fetchone():
                    snack_bar = ft.SnackBar(
                        content=ft.Container(
                            content=ft.Text(f"Já existe um objetivo nestas datas {goal_start} , {goal_end}  \n Tente outra data!", weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.center,  # Alinha o conteúdo (texto) dentro do Container
                        ),
                        bgcolor="red"  # Cor de fundo vermelha
                    )
                    page.overlay.append(snack_bar)
                    snack_bar.open = True
                    page.go("/page_new_goal")
                    conn.close()
                    return

                # Calcular o valor bruto (goal_gross)
                total_discount = fleet_discount + tax_discount
                global goal_gross
                goal_gross = goal / (1 - (total_discount / 100))

                # Inserir os dados no banco
                cursor.execute("""
                    INSERT INTO goal (goal, goal_gross, goal_start, goal_end, day_off, fleet_discount, tax_discount)
                    VALUES (?,?,?,?,?,?,?)
                """, (goal, goal_gross, goal_start, goal_end, day_off, fleet_discount, tax_discount))
                
                conn.commit()
                
                # Verifica se a inserção foi bem-sucedida
                if cursor.rowcount > 0:
                    page_message_screen("Meta cadastrada com sucesso!!!")
                    page.go("/page_parcial")
                else:
                    page_message_screen("Houve algum erro. Tente novamente mais tarde!!!")
                    page.go("/page_new_goal")

            except sqlite3.IntegrityError as e:
                snack_bar = ft.SnackBar(
                    content=ft.Container(
                        content=ft.Text(f"Já existe um objetivo nestas datas {goal_start} , {goal_end}  \n Tente outra data!", weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.center,  # Alinha o conteúdo (texto) dentro do Container
                    ),
                    bgcolor="red"  # Cor de fundo vermelha
                )
                page.overlay.append(snack_bar)
                snack_bar.open = True
                page.go("/page_new_goal")
            
            finally:
                conn.close()

            # Limpa os campos
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

        def validate_date():
            # Obtém o valor do campo de data
            input_date = expense_date.value.strip()
            try:
                parsed_date = datetime.strptime(input_date, "%d/%m/%Y")
                expense_date.value = parsed_date.strftime("%d/%m/%Y")
                expense_date.error_text = None
                expense_date.update()
                return True  # Data válida
            except ValueError:
                expense_date.error_text = "Data inválida! Use o formato DD/MM/AAAA."
                expense_date.update()
                return False  # Data inválida

        result_label = ft.Text(value="", color="black")

        def format_number_33(e):
            try:
                # Filtra e mantém apenas os dígitos numéricos e o ponto decimal
                raw_value = ''.join(filter(lambda x: x.isdigit() or x == '.', e.control.value))

                if raw_value:
                    # Converte para float, garantindo que o valor seja tratado corretamente
                    float_value = float(raw_value)

                    # Formata o número para duas casas decimais
                    formatted_value = f"{float_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                    # Atualiza o campo com o valor formatado
                    e.control.value = formatted_value
                    e.control.update()
            except ValueError:
                # Se ocorrer algum erro de conversão, limpar o valor
                e.control.value = ""
                e.control.update()
    
        def on_date_selected(e):
        # Atualiza o campo de data com a seleção do DatePicker
            if date_picker2.value:
                parsed_date = date_picker2.value
                expense_date.value = parsed_date.strftime("%d/%m/%Y")
                page.update()

        def format_number(e):
            # Filtra e mantém apenas os dígitos numéricos
            raw_value = ''.join(filter(str.isdigit, e.control.value)).replace(",", ".")
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
            page.update()
        
        def all_fields_valid():
        # Verifica se todos os campos obrigatórios estão válidos
            return (
                validate_date() and
                expense_value.value.strip() and  # Valor preenchido
                not expense_date.error_text and  # Data válida
                expense_name.value  # Nome da despesa selecionado
            )

        def validate_all_fields():
               # Revalida todos os campos, mas sem chamar validate_date diretamente
            all_valid = all_fields_valid()
            button_add_expense.disabled = not all_valid
            button_add_expense.update()
            page.update()

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
        # Criação do TextField para data
        expense_date = ft.TextField(
            label="Data da despesa",
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=14,          # Tamanho opcional
            ),
            on_change=lambda e: validate_all_fields(), 
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
                ft.dropdown.Option("Gasolina"),
                ft.dropdown.Option("Gasóleo"),
                ft.dropdown.Option("GNV"),
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
        expense_amount_liters = ft.TextField(label="Litros", visible=False, border_radius=21, on_change=lambda e: (format_number(e), validate_all_fields()))
        expense_amount_cubic_meters = ft.TextField(label="Metros Cúbicos (m³)", visible=False, border_radius=21, on_change=lambda e: (format_number(e), validate_all_fields()))
        expense_amount_energy = ft.TextField(label="Energia (kWh)", visible=False, border_radius=21, on_change=lambda e: (format_number(e), validate_all_fields()))

        def on_option_selected(e):
            expense_amount_liters.visible = False
            expense_amount_cubic_meters.visible = False
            expense_amount_energy.visible = False
            # Alterar a cor de fundo e do texto dependendo da seleção
            if e.control.value == "Manutenção":
                expense_name.bgcolor = "#E0E0E0"  # Cor de fundo quando "Opção 1" é selecionada
                expense_name.style = ft.TextStyle(color="#FF5722")  # Cor do texto para "Opção 1"
            elif e.control.value == "Gasolina":
                expense_amount_liters.visible = True
                expense_name.bgcolor = "#FFEB3B"  # Cor de fundo quando "Opção 2" é selecionada
                expense_name.style = ft.TextStyle(color="#000000")  # Cor do texto para "Opção 2"
            elif e.control.value == "Gasóleo":
                expense_name.bgcolor = "#B25900"  # Cor de fundo quando "Opção 3" é selecionada
                expense_amount_liters.visible = True
                expense_name.style = ft.TextStyle(color="#FFFFFF")  # Cor do texto para "Opção 3"
            elif e.control.value == "GNV":
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
            all_fields_valid()
            # Limpar mensagens de erro anteriores e bordas
            page.controls = [control for control in page.controls if not isinstance(control, ft.Text) or control.color != "red"]

            # Verificar se os campos obrigatórios estão preenchidos
            error_messages = []

            # Verificar campos obrigatórios
            # Verificar o campo `expense_value`
            try:
                # Converte o valor para float removendo os símbolos (€ e separadores)
                expense_value_text = expense_value.value.replace("€", "").replace(".", "").replace(",", ".").strip()
                expense_value_number = float(expense_value_text)
                
                # Valida se o valor é maior que zero
                if expense_value_number <= 0:
                    raise ValueError("O valor da despesa deve ser maior que zero.")
                else:
                    expense_value.border_color = None
            except (ValueError, TypeError):
                expense_value.border_color = "red"
                error_messages.append(("O valor da despesa é inválido ou menor que zero.", expense_value))


             # Validar data
            if not validate_date():
                expense_date.border_color = "red"
                error_messages.append(("Data inválida! Use o formato DD/MM/AAAA.", expense_date))
            else:
                expense_date.border_color = None

            if not expense_name.value:
                expense_name.border_color = "red"
                error_messages.append(("O nome da despesa é obrigatório.", expense_name))
                page.update()
            else:
                expense_name.border_color = None

            # Verificar os campos de quantidade obrigatórios
            if not expense_amount_liters.value and (expense_name.value == "Gasolina" or expense_name.value == "Gasóleo"):
                expense_amount_liters.border_color = "red"
                error_messages.append(("A quantidade de litros é obrigatória.", expense_amount_liters))
                page.update()
            else:
                expense_amount_liters.border_color = None

            if not expense_amount_cubic_meters.value and expense_name.value == "GNV":
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
            elif expense_name_text == "GNV":
                expense_amount_cubic_meters_value = expense_amount_cubic_meters.value
            elif expense_name_text == "Recarga Bateria":
                expense_amount_energy_value = expense_amount_energy.value

            
            expense_amount_liters_value = expense_value.value.replace("€", "").replace(".", "").replace(",", ".").strip()
            expense_amount_liters_value = float(expense_amount_liters_value)

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
            tips_error = None
            trips_error = None
            date_error = None

            # Validação do campo de valor líquido (daily_value_field)
            if daily_value_field.value:
                try:
                    value = float(daily_value_field.value.replace('€ ', '').replace('.', '').replace(',', '.'))
                    if value <= 0:
                        value_error = "* O valor líquido deve ser maior que zero."
                except ValueError:
                    value_error = "* O valor líquido não está formatado corretamente."
            else:
                value_error = "* O campo de valor líquido é obrigatório."

            # Validação do campo de gorjetas (daily_value_tips_field) - opcional
            if daily_value_tips_field.value:
                try:
                    tips = float(daily_value_tips_field.value.replace('€ ', '').replace('.', '').replace(',', '.'))
                    if tips < 0:
                        tips_error = "* O valor das gorjetas não pode ser negativo."
                except ValueError:
                    tips_error = "* O valor das gorjetas não está formatado corretamente."

            # Validação do campo de viagens realizadas (trips_made_field) - obrigatório
            if trips_made_field.value:
                try:
                    trips = int(trips_made_field.value)
                    if trips <= 0:
                        trips_error = "* O número de viagens realizadas deve ser maior que zero."
                except ValueError:
                    trips_error = "* O número de viagens deve ser um valor válido."
            else:
                trips_error = "* O campo de viagens realizadas é obrigatório."

            # Validação do campo de data (daily_date_field)
            if daily_date_field.value:
                try:
                    date_value = datetime.strptime(daily_date_field.value, "%d/%m/%Y")
                except ValueError:
                    date_error = "* A data não está no formato correto (DD/MM/AAAA)."
            else:
                date_error = "* A data da diária é obrigatória."

            # Validação do campo de tempo gasto (working_hours_field)
            if working_hours_field.value:
                try:
                    time_value = datetime.strptime(working_hours_field.value, "%H:%M")
                    if time_value.hour < 0 or time_value.hour > 23 or time_value.minute < 0 or time_value.minute > 59:
                        hour_error = "* Entre 00:00 e 23:59."
                except ValueError:
                    hour_error = "* Entre 00:00 e 23:59."

            # Aplica as mensagens de erro nos campos correspondentes
            daily_value_field.error_text = value_error
            daily_value_tips_field.error_text = tips_error
            trips_made_field.error_text = trips_error
            daily_date_field.error_text = date_error

            # Se qualquer erro ocorrer, desabilita os botões
            if value_error or tips_error or trips_error or date_error:
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
            daily_value_tips_field.update()
            trips_made_field.update()
            daily_date_field.update()
            working_hours_field.update()
            btn_bolt.update()
            btn_uber.update()
            configure_buttons(param)
            
            daily_value_field.on_change = lambda e: (validate_fields(), format_number_accounting(e))
            trips_made_field.on_change = lambda e: validate_fields()
            daily_date_field.on_change = lambda e: validate_fields()

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

        daily_value_field = ft.TextField(label=f"Valor líquido da {param}.", prefix_text="€ ",
            border_radius=21, 
            text_size=18,
            on_change=format_number_accounting, 
            label_style=ft.TextStyle(
                color="#AAAAAA",  # Cor do label
                size=15,               # Tamanho opcional
            ),
            helper_text=f"* Valor líquido da {param} com impostos.",
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

            # Verifica se o campo está vazio (campo opcional)
            if not texto:
                # Não gera erro se o campo for vazio
                e.control.border_color = ft.colors.TRANSPARENT
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
            helper_text=f"*Todas as Viagens realizadas da {param}",
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
                snack_bar = ft.SnackBar(
                    content=ft.Container(
                        content=ft.Text(f"Já existe uma diária nesta data {daily_date} \n Tente outra data!", weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.center,  # Alinha o conteúdo (texto) dentro do Container
                    ),
                    bgcolor="red"  # Cor de fundo vermelha
                )
                page.overlay.append(snack_bar)
                snack_bar.open = True
                
                page.update()
                time.sleep(3)
                
                
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

    def page_parcial(page):
        conn_sqlite = sqlite3.connect("db_tvde_content_internal.db")
        cursor_sqlite = conn_sqlite.cursor()

        # Executar uma consulta para buscar o valor de goal_successful
        cursor_sqlite.execute("SELECT goal_successful FROM goal ORDER BY id DESC LIMIT 1")
        goal_successful = cursor_sqlite.fetchone()

        cursor_sqlite.execute("SELECT COUNT(*) FROM goal")
        meta_count = cursor_sqlite.fetchone()[0]

        # Verificar se o valor foi encontrado e retornar o resultado
        if goal_successful:
            goal_successful = goal_successful[0]  # Se encontrar o valor
        else:
            goal_successful = "default_value"  # Valor padrão se não encontrar nenhum

        conn_sqlite.close()

        # Verificar o redirecionamento com base no resultado da meta
        if meta_count > 0:
            if goal_successful == "negativo":
                page.go("/page_parcial")
            elif goal_successful == "positivo":
                snack_bar = ft.SnackBar(
                    content=ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(f"Parabéns!!! Você alcançou o último Objetivo. \n Crie um NOVO OBJETIVO!", size=15, weight=ft.FontWeight.BOLD),
                                ft.Icon(ft.icons.ADD_CIRCLE_OUTLINE_ROUNDED, size=30)  # Ícone após o texto
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,  # Alinha o conteúdo no centro
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha verticalmente no centro
                        ),
                        alignment=ft.alignment.center,  # Alinha o conteúdo dentro do Container
                    ),
                    bgcolor="green",
                    padding=ft.Padding(top=36, bottom=36, left=0, right=6),
                )
        
                page.overlay.append(snack_bar)
                snack_bar.open = True
                page.update()
        
                time.sleep(9)

        # Navegar para a próxima página ou executar outro código
        page.go("/next_page")

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
            height=48,
            alignment=ft.Alignment(0, 0),
            content=ft.Text(f"🍀\n Olá {user_name}, boa sorte!", size=18, text_align=ft.TextAlign.CENTER),
        )

        def fetch_goal_from_db():
            conn = sqlite3.connect("db_tvde_content_internal.db")
            cursor = conn.cursor()

            # Executar a consulta para obter o valor do objetivo, fleet_discount e tax_discount
            cursor.execute("SELECT goal, fleet_discount, tax_discount FROM goal ORDER BY id DESC LIMIT 1")  # Ajuste conforme necessário
            result = cursor.fetchone()

            cursor.close()
            conn.close()

            if result:
                # Garantir que goal_value, fleet_discount e tax_discount sejam do tipo float
                try:
                    goal_value = float(result[0])  # Convertendo para float
                    # Formatar o valor final para exibição
                    return f"€ {goal_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                except ValueError:
                    return "Erro ao converter os valores"
            else:
                return "€ 0.00"
        global goal_value
        # Exemplo de como chamar a função
        goal_value = fetch_goal_from_db()

        goal = ft.Row(
            controls=[
                ft.Container(
                    width=399,
                    height=87,
                    padding=ft.Padding(top=12, bottom=6, left=0, right=0), 
                    content=ft.Column(
                        controls=[
                            ft.Text("OBJETIVO GERAL", size=18, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                            ft.Text(goal_value, size=36, color=ft.colors.BLACK),
                            ft.Text("Valores líquidos sem taxas e impostos", size=9, color="#858585"),
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
       
        # Registrar adaptadores para datetime
        sqlite3.register_adapter(datetime, lambda x: x.isoformat())
        sqlite3.register_converter("datetime", lambda x: datetime.fromisoformat(x.decode("utf-8")))

        def fetch_goal_details_from_db(page):
            def fetch_daily_values(cursor, table_name, start_date, end_date):
                """
                Consulta valores diários entre start_date e end_date.
                """
                query = f"""
                    SELECT daily_value
                    FROM {table_name}
                    WHERE 
                        date(substr(daily_date, 7, 4) || '-' || substr(daily_date, 4, 2) || '-' || substr(daily_date, 1, 2)) 
                        BETWEEN date(?) AND date(?)
                """
                cursor.execute(query, (start_date, end_date))
                return cursor.fetchall()

            with sqlite3.connect("db_tvde_content_internal.db", detect_types=sqlite3.PARSE_DECLTYPES) as conn:
                cursor = conn.cursor()  # Inicializando o cursor

                # Recuperar as datas 'goal_start' e 'goal_end' da tabela 'goal'
                cursor.execute("SELECT goal_start, goal_end FROM goal ORDER BY id DESC LIMIT 1")
                goal_result = cursor.fetchone()

                if goal_result:
                    goal_start = datetime.strptime(goal_result[0], '%d/%m/%Y')  # Convertendo string para datetime
                    goal_end = datetime.strptime(goal_result[1], '%d/%m/%Y')
                else:
                    goal_start, goal_end = None, None

                # Consultar o valor de "day_off" da tabela "goal"
                cursor.execute("SELECT day_off FROM goal ORDER BY id DESC LIMIT 1")
                day_off_result = cursor.fetchone()
                day_off = day_off_result[0] if day_off_result else 0

                def fetch_expenses(start_date, end_date):
                    """Consulta as despesas entre start_date e end_date."""
                    cursor.execute(""" 
                        SELECT SUM(expense_value) 
                        FROM expense 
                        WHERE date(substr(expense_date, 7, 4) || '-' || substr(expense_date, 4, 2) || '-' || substr(expense_date, 1, 2)) 
                        BETWEEN date(?) AND date(?)
                    """, (start_date, end_date))
                    result = cursor.fetchone()
                    return result[0] if result else 0.0

                # Consultar despesas entre goal_start e goal_end
                expenses = fetch_expenses(goal_start.strftime('%Y-%m-%d'), goal_end.strftime('%Y-%m-%d'))

                # Consultar Uber entre goal_start e goal_end
                uber_data = fetch_daily_values(cursor, "uber", goal_start.strftime('%Y-%m-%d'), goal_end.strftime('%Y-%m-%d'))

                # Consultar Bolt entre goal_start e goal_end
                bolt_data = fetch_daily_values(cursor, "bolt", goal_start.strftime('%Y-%m-%d'), goal_end.strftime('%Y-%m-%d'))

                # Somar os valores diários
                uber_gain = sum(float(row[0]) for row in uber_data if row[0])
                bolt_gain = sum(float(row[0]) for row in bolt_data if row[0])

                total_gain = uber_gain + bolt_gain

                # Recuperar o valor de 'goal_gross' da tabela 'goal' e garantir que seja um float
                cursor.execute("SELECT goal_gross FROM goal ORDER BY id DESC LIMIT 1")
                goal_gross_result = cursor.fetchone()
                goal_gross = float(goal_gross_result[0]) if goal_gross_result and goal_gross_result[0] else 0.0

                # Atualizar o valor total_gain na tabela 'goal'
                cursor.execute("""
                    UPDATE goal 
                    SET total_gain = ? 
                    WHERE goal_start = ? AND goal_end = ?
                """, (total_gain, goal_start.strftime('%d/%m/%Y'), goal_end.strftime('%d/%m/%Y')))
                
                # Caso não exista um registro com essas datas, você pode usar um INSERT para garantir que o valor seja armazenado
                if cursor.rowcount == 0:  # Se não encontrou o registro para atualizar
                    cursor.execute("""
                        INSERT INTO goal (goal_start, goal_end, total_gain)
                        VALUES (?, ?, ?)
                    """, (goal_start.strftime('%d/%m/%Y'), goal_end.strftime('%d/%m/%Y'), total_gain))

                # Verificar se o total_gain é maior ou igual ao goal_gross
                if total_gain >= goal_gross:
                    # Se o total_gain for suficiente, atualizar para 'positivo'
                    cursor.execute("""
                        UPDATE goal 
                        SET goal_successful = 'positivo' 
                        WHERE goal_start = ? AND goal_end = ?
                    """, (goal_start.strftime('%d/%m/%Y'), goal_end.strftime('%d/%m/%Y')))


                else:
                    # Se o total_gain não for suficiente, atualizar para 'negativo'
                    cursor.execute("""
                        UPDATE goal 
                        SET goal_successful = 'negativo' 
                        WHERE goal_start = ? AND goal_end = ?
                    """, (goal_start.strftime('%d/%m/%Y'), goal_end.strftime('%d/%m/%Y')))

                # Confirma as alterações
                conn.commit()

                return goal_start, goal_end, expenses, total_gain, day_off, goal_gross
            
        global total_gain
        # Atualizando a chamada para refletir 6 valores
        goal_start, goal_end, expenses, total_gain, day_off, goal_gross = fetch_goal_details_from_db(page)


        global days_of_work
        # Agora podemos calcular o número de dias de trabalho corretamente
        days_of_work = (goal_end - goal_start).days + 1

        days_of_work -= int(day_off)

        expenses = expenses if expenses is not None else 0.0



        # Formatação e exibição dos dados
        details_goal = ft.Row(
            height=0,
            controls=[
                ft.Container(  
                    ft.Column(
                        width=193,
                        height=99,
                        controls=[
                            ft.Text("Início do Objetivo", size=15, weight=ft.FontWeight.BOLD),
                            ft.Text(goal_start.strftime("%d/%m/%Y") if goal_start else "Data não encontrada", size=15),
                            ft.Text("Dias de Trabalho", size=15, weight=ft.FontWeight.BOLD),
                            ft.Text(str(days_of_work), size=15),
                            ft.Text("Despesas", size=15, weight=ft.FontWeight.BOLD),
                            ft.Text(f"€ {expenses:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), size=15)  # Formatação das despesas
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
                            ft.Text(goal_end.strftime("%d/%m/%Y") if goal_end else "Data não encontrada", size=15),
                            ft.Text("Folgas", size=15, weight=ft.FontWeight.BOLD),
                            ft.Text(str(day_off), size=15),  # Folgas: valor de day_off
                            ft.Text("Ganhos até agora", size=15, weight=ft.FontWeight.BOLD),
                            ft.Text(f"€ {total_gain:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), size=15)  # Formatação dos ganhos
                        ],
                        spacing=0, 
                    ),
                ),
            ]
        )
        
        def fetch_goal_from_db2():
            # Conectando ao banco SQLite
            conn = sqlite3.connect("db_tvde_content_internal.db")  # Nome correto do arquivo SQLite
            cursor = conn.cursor()

            # Realiza a consulta para pegar o valor da meta e as datas
            cursor.execute("SELECT goal, goal_start, goal_end FROM goal ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()

            conn.close()  # Fecha a conexão com o banco de dados

            if result:
                goal_value = result[0]
                goal_start = datetime.strptime(result[1], "%d/%m/%Y")
                goal_end = datetime.strptime(result[2], "%d/%m/%Y")

                # Calcula os dias restantes
                today = datetime.today()
                remaining_days = (goal_end - today).days  # Diferença entre a data final e hoje

                return goal_value, goal_start, goal_end, remaining_days
            else:
                return None, None, None, None

        # Usando a função fetch_goal_from_db para obter o valor da meta e os dias restantes
        goal_value, goal_start, goal_end, remaining_days = fetch_goal_from_db2()

        # Se a meta e os dias restantes foram encontrados
        if goal_value is not None:
            remaining_text = remaining_days - int(day_off)
        else:
            remaining_text = "XX"

                # Garantir que remaining_text seja um número
        if isinstance(remaining_text, str):
            try:
                remaining_text = remaining_text
            except ValueError:
                # Caso não seja possível converter para inteiro, atribui um valor padrão (0, por exemplo)
                remaining_text = 0

        # Agora, subtraímos day_off de remaining_text
        remaining_text += 2
            
        remaining_text2 = ft.Text(
            f"{remaining_text}",  # O valor estilizado do texto
            size=24,
            weight=ft.FontWeight.BOLD
        )


                    # Definir um valor padrão para total_gain, caso a consulta falhe
        # Buscar goal_gross e calcular a porcentagem de progresso
        with sqlite3.connect("db_tvde_content_internal.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT goal_gross FROM goal ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()

        # Garantir que há um resultado válido e fazer a conversão para float
        if result and result[0]:
            try:
                goal_gross = float(result[0])  # Converte para float
                if goal_gross > 0:  # Agora a comparação é feita com um número
                    total_gain_car_position = (total_gain / goal_gross) * 100  # Regra de três para percentual
                else:
                    total_gain_car_position = 0  # Se goal_gross for 0 ou negativo
            except ValueError:
                total_gain_car_position = 0  # Caso não consiga converter para float
        else:
            total_gain_car_position = 0  # Se não houver dado

  

        # Largura total disponível dentro do container roxo
        container_width = 399  # Largura do container roxo
        flag_width = 0  # Largura da bandeira
        car_width = 18  # Largura do carro (aproximada)
        finish_width = 30  # Largura da linha de chegada

        # Definir os limites do espaço em que o carro pode se mover
        start_position = -flag_width  # Para sobrepor a bandeira
        end_position = container_width - finish_width - car_width  # Para alinhar com a linha de chegada

        # Calcular a posição do carro baseado no progresso
        car_position = start_position + (total_gain_car_position / 100) * (end_position - start_position)

  

        # Criar a interface
        hourglass = ft.Row(
            controls=[
                ft.Container(
                    width=399,
                    height=81,
                    padding=0,
                    margin=0,
                    content=ft.Column(
                        controls=[
                            ft.Image(
                                src="https://i.ibb.co/93ps7s5/hourglass.png",
                                height=27,
                                width=27
                            ),
                            ft.Container(
                                padding=ft.Padding(top=0, bottom=12, left=0, right=0),   
                                content=ft.Row(
                                    controls=[
                                        ft.Text("FALTAM", size=15, color="#858585"),
                                        remaining_text2,  # Coloca o texto estilizado no meio
                                        ft.Text("DIAS PARA FIM DO OBJETIVO", size=15, color="#858585"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,  # Alinha ao centro
                                    expand=True  # Torna o Row expansível
                                ),
                            ),
                            ft.Container(
                                width=399,
                                height=30,
                                margin=0,
                                border=ft.border.only(bottom=ft.border.BorderSide(2, ft.colors.BLACK)),
                                content=ft.Stack(
                                    controls=[
                                        # Bandeira vermelha fixada à esquerda
                                        ft.Container(
                                            left=0,
                                            content=ft.Image(
                                                src="https://i.ibb.co/80MV450/flag.png",
                                            ),
                                        ),
                                        # Carro verde com posição dinâmica baseada no total_gain
                                        ft.Container(
                                            left=car_position,
                                            padding=ft.padding.only(top=7, left=0, right=5, bottom=0),
                                            content=ft.Image(
                                                src="https://i.ibb.co/27GrFHLV/car.png",
                                            ),
                                            alignment=ft.Alignment(0, 0),
                                        ),
                                        # Linha de chegada preta fixada à direita (não será empurrada)
                                        ft.Container(
                                            right=0,  # Garante que fique sempre na extrema direita
                                            width=finish_width,  # Mantém a largura correta
                                            content=ft.Image(
                                                src="https://i.ibb.co/M5nXHpq/finish-line-5-stars.png",
                                            ),
                                        ),
                                    ],
                                ),
                            ),

                            ft.Container(
                                width=3,
                                height=6,
                                bgcolor="black",
                            ),
                        ],
                        spacing=0,
                        horizontal_alignment="center",
                        
                    ),
                ),
            ],
        )


            
        def fetch_goal_from_db4(total_gain):
            with sqlite3.connect("db_tvde_content_internal.db") as conn:
                cursor = conn.cursor()

                # Obter os dados da meta mais recente
                cursor.execute("SELECT goal_gross, goal_start, goal_end, day_off FROM goal ORDER BY id DESC LIMIT 1")
                result = cursor.fetchone()

            if result:
                # Extrair valores da meta
                goal_gross = float(result[0])  # Garantir que seja float
                goal_start = datetime.strptime(result[1], "%d/%m/%Y")
                goal_end = datetime.strptime(result[2], "%d/%m/%Y")
                day_off = int(result[3]) if result[3] else 0  # Garantir que day_off seja int

                # Calcular a porcentagem concluída do objetivo
                total_gain_car_position = (total_gain / goal_gross) * 100 if goal_gross > 0 else 0

                # Calcular os dias de trabalho totais
                days_of_work = (goal_end - goal_start).days + 1  # Intervalo total
                days_of_work -= day_off  # Remover dias de folga

                # **Contar quantos registros existem nas tabelas `uber` e `bolt`**
                with sqlite3.connect("db_tvde_content_internal.db") as conn:
                    cursor = conn.cursor()

                    # Contar **todas** as inserções na tabela Uber
                    cursor.execute("""
                        SELECT COUNT(*) FROM uber 
                        WHERE daily_date BETWEEN ? AND ?
                    """, (goal_start.strftime("%d/%m/%Y"), goal_end.strftime("%d/%m/%Y")))
                    uber_entries = cursor.fetchone()[0]  
                    uber_entries = int(uber_entries) if uber_entries else 0  # Garantir que seja inteiro

                    # Contar **todas** as inserções na tabela Bolt
                    cursor.execute("""
                        SELECT COUNT(*) FROM bolt 
                        WHERE daily_date BETWEEN ? AND ?
                    """, (goal_start.strftime("%d/%m/%Y"), goal_end.strftime("%d/%m/%Y")))
                    bolt_entries = cursor.fetchone()[0]  
                    bolt_entries = int(bolt_entries) if bolt_entries else 0  # Garantir que seja inteiro

                    # **Encontrar as datas comuns entre as tabelas `uber` e `bolt`**
                    cursor.execute("""
                        SELECT COUNT(*) FROM uber
                        WHERE daily_date IN (SELECT daily_date FROM bolt WHERE daily_date BETWEEN ? AND ?)
                    """, (goal_start.strftime("%d/%m/%Y"), goal_end.strftime("%d/%m/%Y")))
                    common_entries = cursor.fetchone()[0]
                    common_entries = int(common_entries) if common_entries else 0  # Garantir que seja inteiro

                # Log para depuração
                print(f"🚗 Registros no Uber: {uber_entries}")
                print(f"⚡ Registros no Bolt: {bolt_entries}")
                print(f"🔄 Datas Comuns: {common_entries}")

                # **Agora somamos corretamente os registros, subtraindo as datas comuns**
                insertions_count = uber_entries + bolt_entries - common_entries  # Subtrai as entradas duplicadas

                # Subtrair os dias de trabalho já registrados
                days_of_work -= insertions_count

                print(f"⚡⚡⚡ Total de Inserções Contadas: {insertions_count}")

                # Evitar valores inválidos para days_of_work
                if days_of_work > 0:
                    remaining_goal = goal_gross - total_gain
                    daily_value = remaining_goal / days_of_work
                    return daily_value, total_gain_car_position
                else:
                    return 0, total_gain_car_position  # Retorna 0 para evitar erro
            else:
                return "Erro ao recuperar os dados do banco de dados", 0

        # Assumindo que `total_gain` é obtido de outra função

        # Calcular daily_value_value e total_gain_car_position com base no total_gain
        daily_value_value, total_gain_car_position = fetch_goal_from_db4(total_gain)

        # Calcular a posição do carro baseado no progresso
        car_position = start_position + (total_gain_car_position / 100) * (end_position - start_position)


        
        goal_today = ft.Row(
            controls=[
                ft.Container(
                    width=399,
                    height=123,
                    padding=0,
                    margin=0,
                    border_radius=25,
                    content=ft.Column(
                        controls=[
                            ft.Text("OBJETIVO DIÁRIO", size=15, color=ft.colors.BLACK),
                            ft.Container(
                                content=ft.Text(f"€ {daily_value_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), 
                                    size=42, 
                                    color="#15CD74", 
                                    weight=ft.FontWeight.BOLD
                                ),
                                shadow=ft.BoxShadow(color="#15CD74", blur_radius=180)  # Sombra
                            ),
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
                    height=72,
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
                    ft.Container(),
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
            page_parcial(page)
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
        elif page.route == "/page_reports_expense":
            page_reports_expense()
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