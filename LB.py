import flet as ft
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Cria uma conexão com o banco de dados MySQL."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="acesso123",
            database="a mimir"
        )
        print("Conexão bem-sucedida!")
    except Error as e:
        print(f"Ocorreu um erro: {e}")
    return connection

def menu(page: ft.Page):
    page.title = "Livraria Itinerante"
    page.theme = ft.Theme(color_scheme_seed='green')
    page.add(ft.Text(value='Bem vindo a Biblioteca Itinerante!', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK))
    radio_group = ft.RadioGroup(
         value='Leitor',
        content=ft.Column(  # Usamos uma coluna para adicionar os RadioButtons
            controls=[
                ft.Radio(value="Leitor", label="Leitor"),
                ft.Radio(value='Autor', label='Autor')
            ]))
    
    page.add(ft.TextField(label='Nome:', text_align=ft.TextAlign.LEFT))
    page.add(ft.TextField(label='Senha:', password=True, text_align=ft.TextAlign.LEFT))
    
    def on_send_click(e):
            conn = create_connection()
            cursor.execute('')#Adicione uma lógica beleza?
            if conn:
                # Aqui você pode executar consultas, por exemplo, buscar livros
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM leitores AND autores;")  # Substitua pela sua consulta
                    results = cursor.fetchall()
                    for row in results:
                        print(row)
                except Error as e:
                    print(f"Ocorreu um erro ao executar a consulta: {e}")
                finally:
                    cursor.close()
                    conn.close()

    send_button = ft.ElevatedButton(text='Enviar', on_click=on_send_click)
    add_reader_button = ft.ElevatedButton(text='Cadastrar novo leitor',on_click=lambda e: add_reader)
    page.add(send_button, add_reader_button, radio_group)

    def add_reader(e):
            dialog.open = True
            page.update()

            dialog = ft.AlertDialog(
                title=ft.Text("Cadastro de leitor"),
                content=ft.Column([
                    ft.TextField(label="Digite seu nome:", text_align=ft.TextAlign.LEFT),
                    ft.TextField(label='Digite sua senha:', password=True, text_align=ft.TextAlign.LEFT)
                ]),
                actions=[
                    ft.ElevatedButton(text='Cadastrar leitor',),
                    ft.TextButton("Fechar", on_click=lambda e: dialog.close())
                ],
            )
            page.overlay.append(dialog)

ft.app(target=menu)
