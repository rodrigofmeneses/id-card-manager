import os
import pandas as pd
from pprint import pprint
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import messagebox, ttk

# Script para automatizar a criação de crachás no formato
""" Diretório raiz deve ter a seguinte estrutura
ORGÃO/
    dados/
        ps_dados.csv
        ps_frente.txt
        ps_verso.txt
    fotos/
        3x4/
"""


def find_button():
    """Localiza o diretório raiz e gera vizualização se entrada for válida."""
    dialog_path = askdirectory()
    try:
        assert dialog_path != ''
        assert open(dialog_path + '/dados/ps_dados.csv') and os.listdir(
            dialog_path + '/fotos/3x4'
        )
    except AssertionError:
        return
    except FileNotFoundError:
        msg = f'          SELECIONE A PASTA RAIZ DO ORGÃO \n VERIFIQUE A ESTRUTURA DE PASTAS E ARQUIVOS.'
        messagebox.showerror(title='Pasta incorreta!', message=msg)
        return

    dir_path.set(dialog_path)
    # Localização das pastas e arquivos
    data_path = f'{dir_path.get()}/dados/ps_dados.csv'
    photos_dir_path = f'{dir_path.get()}/fotos/3x4'

    # Leitura e tratamento dos dados
    global df
    df = pd.read_csv(data_path, sep=';')
    df.fillna(0, inplace=True)
    df.matricula = [int(mat) for mat in df.matricula]
    df.identidade = [int(mat) for mat in df.identidade]

    # Arquivos dentro da pasta selecionada
    matriculas_jpg = [matricula for matricula in os.listdir(photos_dir_path)]
    # Apenas suas matrículas
    matriculas = [int(matricula.split('.')[0]) for matricula in matriculas_jpg]
    # Composição completa de todos os funcionários
    path_fotos = [
        f'{photos_dir_path}/{str(matricula)}.jpg' for matricula in df.matricula
    ]
    # Criar coluna no df com caminho
    df = df.assign(foto=path_fotos)
    # Criar coluna com respeito a visibilidade
    df = df.assign(mostrar_foto=len(df) * [True])
    # Filtrar por funcionários que tem foto
    df = df[df.matricula.isin(matriculas)]

    # Exibir na tela
    clear_data()
    data_tv['column'] = list(df.columns)
    data_tv['show'] = 'headings'

    for column in data_tv['columns']:
        data_tv.heading(
            column, text=column
        )   # let the column heading = column name

    df_rows = (
        df.to_numpy().tolist()
    )   # turns the dataframe into a list of lists
    for row in df_rows:
        data_tv.insert(
            '', 'end', values=row
        )   # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

    # Mostrar o botão de salvar
    save_frame.pack(anchor=tk.W, fill='x', **padding)


def save_button():
    """Salva os arquivos no formato do photoshop"""
    try:
        assert dir_path.get() != ''
        df.drop(columns=['nome', 'identidade', 'admissao']).to_csv(
            f'{dir_path.get()}/dados/ps_frente.txt', index=False, sep=' '
        )

        df.drop(
            columns=['nome_guerra', 'cargo', 'foto', 'mostrar_foto', 'lotacao']
        ).to_csv(f'{dir_path.get()}/dados/ps_verso.txt', index=False, sep=' ')
        save_message.set('Arquivos salvos com sucesso!')
    except AssertionError:
        save_message.set('Falha ao salvar arquivos!')
        print('dir path vazio')


def clear_data():
    # '''Limpa a visualização de data_tv'''
    data_tv.delete(*data_tv.get_children())


root = tk.Tk()
root.title('ID Card Manager')
root.geometry('1900x450')

padding = {'padx': 5, 'pady': 5}

folder_frame = ttk.LabelFrame(root, text='Folder')

dir_path = tk.StringVar()
ttk.Button(folder_frame, text='Find', command=find_button).pack(
    side=tk.LEFT, **padding
)
ttk.Label(folder_frame, text='Folder:').pack(side=tk.LEFT, **padding)
tk.Label(folder_frame, textvariable=dir_path).pack(
    side=tk.LEFT, fill='x', **padding
)
folder_frame.pack(fill='x', **padding)

data_frame = ttk.LabelFrame(root, text='Data')
data_frame.pack(fill='x', **padding)
data_tv = ttk.Treeview(data_frame)
treescrolly = tk.Scrollbar(
    data_frame, orient='vertical', command=data_tv.yview
)   # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(
    data_frame, orient='horizontal', command=data_tv.xview
)   # command means update the xaxis view of the widget
data_tv.configure(
    xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set
)   # assign the scrollbars to the Treeview Widget
treescrollx.pack(
    side='bottom', fill='x'
)   # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(
    side='right', fill='y'
)   # make the scrollbar fill the y axis of the Treeview widget
data_tv.pack(fill='x', **padding)

save_frame = ttk.LabelFrame(root, text='Save')
ttk.Button(save_frame, text='Save', command=save_button).pack(
    side=tk.LEFT, **padding
)
save_message = tk.StringVar()
ttk.Label(save_frame, textvariable=save_message).pack(side=tk.LEFT, **padding)

root.mainloop()
