import pandas as pd
import os

# Ler dados
#df = pd.read_csv('Listagem de Empregados.csv', sep=';')
df = pd.read_csv('Listagem de Empregados Extra.csv', sep=';')

# Criar caminho para fotos
# path_fotos = ['D:\\Gráfica MArte\\Crachás\\Detran 2021\\fotos\\3x4\\' + str(image) + '.jpg' for image in list(df['matricula'])]


path_fotos = [os.getcwd()[:-6] + '\\fotos\\3x4\\' + str(matricula) + '.jpg' for matricula in list(df['matricula'])]

# Criar coluna no df com caminho
df = df.assign(foto = path_fotos)
# Criar coluna com respeito a visibilidade
df = df.assign(mostrar_foto = df.shape[0] * [True])


# cracha_frente.csv
df_frente = df.drop(columns=['nome', 'identidade', 'admissao'])

# cracha_verso.csv
df_verso = df.drop(columns=['nome_guerra', 'cargo', 'foto', 'mostrar_foto', 'lotacao'])

# Salvar csv
df_frente.to_csv('cracha_frente.csv', index=False)
df_verso.to_csv('cracha_verso.csv', index=False)