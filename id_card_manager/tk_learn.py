from ast import Str
from tkinter import *
from tkinter.filedialog import askdirectory, asksaveasfile
from tkinter import ttk
from pprint import pprint
import os

# Script para automatizar a criação de crachás no formato

def find_button():
    ''' Botão 'Find'.
    Responsável por salvar o diretório onde estão as imagens 3x4,
    escrever na tela e adicionar os novos widgets.
    '''
    dir_path = find_folder_dir()
    write_dir_text(text=dir_path)
    add_widgets()


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

def write_dir_text(text: Str):
    '''
    Escreve um texto no widget 'dir_path'.
    
        text -> Texto a ser escrito em 'dir_path'. 
    '''
    try:
        dir_path_widget.configure(state='normal')
        dir_path_widget.delete('1.0', 'end')
        dir_path_widget.insert('1.0', text)
        dir_path_widget.configure(state='disabled')
    except:
        print('Problema na escrita do text box')

def add_widgets():
    '''
    Adiciona os widgets na tela
    '''
    try:
        assert len(buttons.winfo_children()) == 1
        card_data_widget.pack(
            before=buttons
        )
        ttk.Button(buttons, text="Save", command=save_button).pack(
            side=LEFT
        )   
        ttk.Button(buttons, text="Test", command=test_func).pack(
            side=LEFT
        )
    except:
        print('Problema na insersão dos widgets')
    
def test_func():
    dir_path = dir_path_widget.get('1.0', END)[:-1]
    for matricula in os.listdir(dir_path):
        pprint(dir_path + '/' +  matricula)



root = Tk()
root.title("ID Card Manager")

mainframe = ttk.Frame(root, padding='3 3 3 3')
padding = {'padx': 5, 'pady': 5}
folder_frame = ttk.Frame(mainframe)

ttk.Label(folder_frame, text='Find:').pack(
    side=LEFT
)

dir_path = ''
dir_path_widget = Text(folder_frame, width=70, height=1, state='disabled')
dir_path_widget.pack(
    side=RIGHT
)

card_data = ''
card_data_widget = Text(mainframe, width=75, state='disabled')

folder_frame.pack(**padding)

buttons = ttk.Frame(mainframe)

ttk.Button(buttons, text="Find", command=find_button).pack(
    side=LEFT
)

buttons.pack(
    anchor=W,
    **padding
)

mainframe.pack()

root.mainloop()