import flet as ft
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Cria uma conexão com o banco de dados MySQL."""
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="acesso123",
            database="a mimir"
        )
        print("Conexão bem-sucedida!")
        return connection
    except Error as e:
        print(f"Ocorreu um erro: {e}")
        return None

def menu(page: ft.Page):
    page.title = "Livraria Itinerante"
    page.theme = ft.Theme(color_scheme_seed='green')
    page.add(ft.Text(value='Bem vindo a Biblioteca Itinerante!', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK))
    
    radio_group = ft.RadioGroup(
        value='Leitor',
        content=ft.Column(
            controls=[
                ft.Radio(value="Leitor", label="Leitor"),
                ft.Radio(value='Autor', label='Autor')
            ]
        )
    )
    
    name_field = ft.TextField(label='Nome:', text_align=ft.TextAlign.LEFT)
    password_field = ft.TextField(label='Senha:', password=True, text_align=ft.TextAlign.LEFT)

    def add_reader(e):
        global R, P, E
        R = ft.TextField(label="Digite seu nome:", text_align=ft.TextAlign.LEFT)
        P = ft.TextField(label='Digite sua senha:', password=True, text_align=ft.TextAlign.LEFT)
        E = ft.TextField(label='Digite seu email:', text_align=ft.TextAlign.LEFT)

        dialog = ft.AlertDialog(
            title=ft.Text("Cadastro de leitor"),
            content=ft.Column([R, P, E]),
            actions=[
                ft.ElevatedButton(text='Cadastrar leitor', on_click=readers_registration),
            ],
        )

        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def on_send_click(e):
        if radio_group.value == 'Leitor':
            create_reader_dashboard()

    send_button = ft.ElevatedButton(text='Enviar', on_click=on_send_click)
    add_reader_button = ft.ElevatedButton(text='Cadastrar novo leitor', on_click=add_reader)
    
    page.add(name_field, password_field, send_button, add_reader_button, radio_group)

    def create_reader_dashboard():
        data = [
            {"category": "Livros", "value": 120},
            {"category": "Leitores", "value": 45},
            {"category": "Empréstimos", "value": 10},
        ]
        
        page.add(
            ft.Column([
                ft.Text("Número total de livros: 120"),
                ft.Text("Número total de leitores: 45"),
                ft.Text("Número de empréstimos ativos: 10"),
                ft.Text("Estatísticas:"),
                ft.BarChart(data=data),
                ft.ElevatedButton("Gerenciar Livros", on_click='')  # Adicionar função neste botão
            ])
        )


    def readers_registration(e):
        nome = R.value.strip()
        senha = P.value.strip()
        email = E.value.strip()

        if not nome or not senha or not email:
            ft.SnackBar("Por favor, preencha todos os campos.", color=ft.colors.RED)
            return

        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO leitores (nome, senha, email) VALUES (%s, %s, %s)",
                        (nome, senha, email)
                    )
                    conn.commit()
                    ft.SnackBar("Leitor cadastrado com sucesso!")
            except Error as e:
                print(f"Ocorreu um erro ao executar a consulta: {e}")
                ft.SnackBar("Erro ao cadastrar leitor. {e}")
            finally:
                conn.close()

ft.app(target=menu)
