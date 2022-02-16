import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfile
from tkinter import ttk
import pandas as pd
import os
from pprint import pprint

# Script para automatizar a criação de crachás no formato
''' Selecionar o arquivo com os dados
    Selecionar a pasta com as fotos
    Exibir na tela as informações
    Criar o arquivo de leitura do photoshop
'''

def find_folder_button():
    ''' Botão 'Find Folder'.
    Responsável por salvar o diretório onde estão as imagens 3x4,
    escrever na tela e adicionar os novos widgets.
    '''
    dialog_path = askdirectory()
    try:
        assert dialog_path != '', ''
        dir_path.set(dialog_path)
    except AssertionError:
        print('Invalid dir path')

def save_button():
    ''' Botão 'Save'.
    Selecionar ou criar arquivo de saída.
    '''
    file = asksaveasfile(defaultextension=".txt")
    try:
        file.write(dir_path)
    except:
        print('Error save file')

def test_button():
    data_path = f'{dir_path.get()}\\dados\\dados.csv'
    df = pd.read_csv(data_path)
    
    data_widget["column"] = list(df.columns)
    data_widget["show"] = "headings"

    for column in data_widget["columns"]:
        data_widget.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        data_widget.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

    # Arquivos dentro da pasta selecionada
    # matriculas_jpg = [
    #     matricula 
    #     for matricula in os.listdir(dir_path.get())
    # ]
    # Apenas suas matrículas
    # matriculas_dir_path = [
    #     int(matricula.split('.')[0]) 
    #     for matricula in matriculas_jpg
    # ]
    # Composição completa de todos os funcionários
    # path_fotos = [
    #     dir_path.get() + '/' +  str(matricula) + '.jpg' 
    #     for matricula in df.matricula
    # ]    
    # # Criar coluna no df com caminho
    # df = df.assign(foto = path_fotos)
    # # Criar coluna com respeito a visibilidade
    # df = df.assign(mostrar_foto = len(df) * [True])
    # # Filtrar por funcionários que tem foto
    # df = df[df.matricula.isin(matriculas_dir_path)]


root = tk.Tk()
root.title("ID Card Manager")
root.geometry('1000x500')

# mainframe = ttk.Frame(root, padding='3 3 3 3')
padding = {'padx': 5, 'pady': 5}

folder_frame = ttk.LabelFrame(root, text='Folder')

dir_path = tk.StringVar()
ttk.Button(folder_frame, text="Find", command=find_folder_button).pack(
    side=tk.LEFT,
    **padding
)
ttk.Label(folder_frame, text='Folder:').pack(
    side=tk.LEFT,
    **padding
)
dir_path_widget = tk.Label(folder_frame, textvariable=dir_path)
dir_path_widget.pack(
    side=tk.LEFT,
    fill='x',
    **padding
)
folder_frame.pack(
    fill='x',
    **padding
)

data_frame = ttk.LabelFrame(root, text='Data')
data_frame.pack(
    fill='x',
    **padding
)

data_widget = ttk.Treeview(data_frame)

treescrolly = tk.Scrollbar(data_frame, orient="vertical", command=data_widget.yview) # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(data_frame, orient="horizontal", command=data_widget.xview) # command means update the xaxis view of the widget
data_widget.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
data_widget.pack(
    fill='x',
    **padding
)

save_frame = ttk.LabelFrame(root, text='Save')
ttk.Button(save_frame, text="Save", command=save_button).pack(
    side=tk.LEFT,
    **padding
)   
ttk.Button(save_frame, text="Test", command=test_button).pack(
    side=tk.LEFT,
    **padding
)
save_frame.pack(
    anchor=tk.W,
    fill='x',
    **padding
)

root.mainloop()