from ast import Str
from multiprocessing.dummy import active_children
from tkinter import *
from tkinter.filedialog import askdirectory, asksaveasfile
from tkinter import ttk
from pprint import pprint
import os

# Script para automatizar a criação de crachás no formato

def find_data_button():
    print(len(folder_frame.winfo_children()))
    if len(folder_frame.winfo_children()) == 1:
        add_folder_frame_widgets()

def find_folder_button():
    ''' Botão 'Find'.
    Responsável por salvar o diretório onde estão as imagens 3x4,
    escrever na tela e adicionar os novos widgets.
    '''
    dir_path = find_folder_dir()
    write_text_widget(dir_path_widget, dir_path)
    
    if len(buttons.winfo_children()) == 0:
        add_buttons_widgets()

def save_button():
    ''' Botão 'Save'.
    Selecionar ou criar arquivo de saída.
    '''
    file = asksaveasfile(defaultextension=".txt")
    try:
        file.write(dir_path)
    except:
        print('Error save file')

def find_folder_dir() -> Str:
    '''
    Abre janela para localizar diretório.
    return: Caminho para o diretório selecionado.
    '''
    try:
        path = askdirectory()
        assert path
    except:
        print('Campo de texto vazio')
    
    return path

def write_text_widget(widget, text: Str):
    '''
    Escreve um texto no widget 'dir_path'.
    
        text -> Texto a ser escrito em 'dir_path'. 
    '''
    try:
        widget.configure(state='normal')
        widget.delete('1.0', 'end')
        widget.insert('1.0', text)
        widget.configure(state='disabled')
    except:
        print('Problema na escrita do text box')

def add_folder_frame_widgets():
    '''Adiciona os widgets do folder_frame
    '''
    ttk.Button(folder_frame, text="Find Folder", command=find_folder_button).pack(
        side=LEFT,
        padx=5
    )
    ttk.Label(folder_frame, text='Folder:').pack(
        side=LEFT
    )
    dir_path_widget.pack(
        side=LEFT
    )
    card_data_widget.pack(
        before=buttons
    )


def add_buttons_widgets():
    '''
    Adiciona os widgets na tela
    '''
    ttk.Button(buttons, text="Save", command=save_button).pack(
        side=LEFT
    )   
    ttk.Button(buttons, text="Test", command=test_func).pack(
        side=LEFT
    )
    
def test_func():
    dir_path = dir_path_widget.get('1.0', END)[:-1]
    card_data = [dir_path + '/' +  matricula for matricula in os.listdir(dir_path)]
    print(card_data)
    write_text_widget(card_data_widget, card_data)
        # pprint(dir_path + '/' +  matricula)


root = Tk()
root.title("ID Card Manager")

mainframe = ttk.Frame(root, padding='3 3 3 3')
padding = {'padx': 5, 'pady': 5}

data_frame = ttk.Frame(mainframe)
ttk.Button(data_frame, text='Find Data', command=find_data_button).pack(
    side=LEFT,
    padx=5
)
ttk.Label(data_frame, text='Data:').pack(
    side=LEFT
)
data_path = ''
data_path_widget = Text(data_frame, width=70, height=1, state='disabled')
data_path_widget.pack(
    side=LEFT
)
data_frame.pack(**padding)

folder_frame = ttk.Frame(mainframe)

dir_path = ''
dir_path_widget = Text(folder_frame, width=70, height=1, state='disabled')
folder_frame.pack(**padding)

card_data = ''
card_data_widget = Text(mainframe, width=80, state='disabled')

buttons = ttk.Frame(mainframe)

buttons.pack(
    anchor=W,
    **padding
)

mainframe.pack()

root.mainloop()