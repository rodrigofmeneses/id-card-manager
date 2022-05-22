import pandas as pd
import PySimpleGUI as sg
from buttons import search_button, save_button
from pathlib import Path
from PySimpleGUI import (    
    Window, Frame, Table, Text, Button, popup
)
from tkinter.filedialog import askdirectory

sg.theme('DarkAmber')

root_directory_path = Text('Diretóridos arquivos', key='--ROOT-TEXT--')
layout_directory = [
    [Button('Procurar', key='--PROCURAR--'), root_directory_path]
]

headings = ['matricula', 'nome', 'nome_guerra', 'cargo', 
            'identidade', 'admissao', 'lotacao', 'foto', 'mostrar_foto']
# table_data = [['Marta', 'Linda', 'Maravilhosa']]
table_data = [[]]

layout_data = [[
    Table(
        table_data,
        headings=headings,
        key='--TABLE--',
        justification='left'
    )
]]

saved_directory_path = Text('', key='--SAVE-TEXT--')
layout_save = [
    [Button('Salvar', key='--SALVAR--'), saved_directory_path]
]

directory = Frame('Diretório', layout=layout_directory) 
data = Frame('Tabela', layout=layout_data)
save = Frame(
    'Salvar', 
    layout=layout_save, 
    key='--SAVE-FRAME--', 
    visible=False
)

window = Window(
    'ID Card',
    layout=[
        [directory],
        [data],
        [save]
    ]
)


def search_button(root_path):
    file_path = root_path.parent.parent / 'dados/ps_dados.csv'
    df = pd.read_csv(file_path, sep=';')
    df.fillna(0, inplace=True)
    df.matricula = [int(mat) for mat in df.matricula]
    df.identidade = [int(mat) for mat in df.identidade]

    # matrículas dentro da pasta
    photos_path = root_path / 'fotos/3x4'
    matriculas_pasta = [
        int(matricula.name.split('.')[0]) for matricula in photos_path.iterdir()
    ]
    # Composição completa de todos os funcionários
    path_fotos = [
        f'{photos_path}/{str(matricula)}.jpg' for matricula in df.matricula
    ]
    # Criar coluna no df com caminho
    df = df.assign(foto=path_fotos)
    # Criar coluna com respeito a visibilidade
    df = df.assign(mostrar_foto=len(df) * [True])
    # Filtrar por funcionários que tem foto
    df = df[df.matricula.isin(matriculas_pasta)]

    return df, df.values.tolist()

def save_button(df, data_path):
    # Salva os arquivos
    df.drop(
        columns=['nome', 'identidade', 'admissao']
    ).to_csv(f'{data_path}/dados/ps_frente.csv', index=False)

    df.drop(
        columns=['nome_guerra', 'cargo', 'foto', 'mostrar_foto', 'lotacao']
    ).to_csv(f'{data_path}/dados/ps_verso.csv', index=False)

    return f'Arquivos Salvos com sucesso em: \n {data_path / "dados"}'

while True:
    event, values = window.read()
    match(event):
        case '--PROCURAR--':
            root_path = Path(str(askdirectory()))
            df, table_data = search_button(root_path)
            window['--ROOT-TEXT--'].update(root_path)
            window['--TABLE--'].update(table_data)
            window['--SAVE-FRAME--'].update(visible = True)
        case '--SALVAR--':
            data_path = root_path.parent.parent
            save_text = save_button(df, data_path)
            window['--SAVE-TEXT--'].update(save_text)
        case None:
            break
        case _:
            print(event, values)

window.close()
