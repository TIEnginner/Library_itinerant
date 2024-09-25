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

def verify_user(nome, senha):
    """Verifica se o usuário existe no banco de dados."""
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM leitores WHERE nome = %s AND senha = %s", (nome, senha))
                return cursor.fetchone() is not None
        except Error as e:
            print(f"Ocorreu um erro ao verificar usuário: {e}")
        finally:
            conn.close()
    return False

def verify_author(nome, senha):
    """Verifica se o autor existe no banco de dados."""
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM autores WHERE nome = %s AND senha = %s", (nome, senha))
                return cursor.fetchone() is not None
        except Error as e:
            print(f"Ocorreu um erro ao verificar autor: {e}")
        finally:
            conn.close()
    return False

def menu(page: ft.Page):
    page.title = "Livraria Itinerante"
    page.theme = ft.Theme(color_scheme_seed='green')
    page.add(ft.Text(value='Bem-vindo à Biblioteca Itinerante!', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK))
    
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
            actions=[ft.ElevatedButton(text='Cadastrar leitor', on_click=readers_registration)],
        )

        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def create_author_dashboard(e):
        global T, S
        T = ft.TextField(label='Digite seu nome:', text_align=ft.TextAlign.LEFT)
        S = ft.TextField(label='Digite sua senha:', password=True, text_align=ft.TextAlign.LEFT)

        dialogo = ft.AlertDialog(
            title=ft.Text("Cadastro de autor"),
            content=ft.Column([T, S]),
            actions=[ft.ElevatedButton(text='Cadastrar autor', on_click=authors_registration)],
        )

        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    def warning_error():
        popup = ft.AlertDialog(
            title=ft.Text("Aviso"),
            content=ft.Text("Erro, não foi possível acessar esta página.")
        )
        page.dialog = popup
        popup.open = True
        page.update()

    def on_send_click(e):
        nome = name_field.value.strip()
        senha = password_field.value.strip()

        if not nome or not senha:
            snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos."))
            page.snack_bar = snack_bar
            snack_bar.open = True
            page.update()
            return

        if verify_user(nome, senha):
            informations_dashboard()
        elif verify_author(nome, senha):
            informations_dashboard()
        else:
            warning_error()

    send_button = ft.ElevatedButton(text='Enviar', on_click=on_send_click)
    add_reader_button = ft.ElevatedButton(text='Cadastrar novo leitor', on_click=add_reader)
    add_author_button = ft.ElevatedButton(text='Cadastrar novo autor', on_click=create_author_dashboard)
    
    page.add(name_field, password_field, send_button, add_reader_button, add_author_button, radio_group)

    def informations_dashboard():
        data = [
            {"category": "Livros", "value": 120},
            {"category": "Leitores", "value": 45},
            {"category": "Empréstimos", "value": 10},
        ]

        dialog_data = ft.AlertDialog(
            title=ft.Text('Informações Gerais:'),
            content=ft.Column(
                controls=[
                    ft.Text(f"Número total de livros: {data[0]['value']}"),
                    ft.Text(f"Número total de leitores: {data[1]['value']}"),
                    ft.Text(f"Número de empréstimos ativos: {data[2]['value']}")
                ]
            )
        )
        page.add(
            ft.Column([
                ft.Text("Estatísticas de Leitura"),
                ft.BarChart(data=data),
                ft.ElevatedButton("Gerenciar Livros", on_click=lambda e: None)
            ])
        )

    def readers_registration(e):
        nome = R.value.strip()
        senha = P.value.strip()
        email = E.value.strip()

        if not nome or not senha or not email:
            snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos."))
            page.snack_bar = snack_bar
            snack_bar.open = True
            page.update()
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
                    snack_bar = ft.SnackBar(ft.Text("Leitor cadastrado com sucesso!"))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
            except Error as e:
                snack_bar = ft.SnackBar(ft.Text("Erro ao cadastrar leitor."))
                page.snack_bar = snack_bar
                snack_bar.open = True
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            finally:
                conn.close()
            page.update()

    def authors_registration(e):
        name = T.value.strip()
        senha = S.value.strip()

        if not name or not senha:
            snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos."))
            page.snack_bar = snack_bar
            snack_bar.open = True
            page.update()
            return
        
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO autores (nome, senha) VALUES (%s, %s)",
                                   (name, senha))
                    conn.commit()
                    snack_bar = ft.SnackBar(ft.Text("Autor cadastrado com sucesso!"))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
            except Error as e:
                snack_bar = ft.SnackBar(ft.Text("Erro ao cadastrar o autor."))
                page.snack_bar = snack_bar
                snack_bar.open = True
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            finally:
                conn.close()
            page.update()

ft.app(target=menu)
