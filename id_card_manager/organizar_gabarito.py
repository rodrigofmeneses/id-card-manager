import pandas as pd
import os

# cracha1,cracha2,...,mostrar_cracha1,monstrar_cracha2,...
colunas = [f'cracha{i}' for i in range(1, 11)]
colunas = colunas + [f'mostrar_cracha{i}' for i in range(1, 11)]

crachas_frente = os.listdir(os.getcwd()[:-6] + '\\saida\\crachas\\frente')
crachas_verso = os.listdir(os.getcwd()[:-6] + '\\saida\\crachas\\verso')

crachas_frente = [ os.getcwd()[:-6] + '\\saida\\crachas\\frente\\' + c for c in crachas_frente]
crachas_verso = [ os.getcwd()[:-6] + '\\saida\\crachas\\verso\\' + c for c in crachas_verso]

df_frente = pd.DataFrame(columns=colunas)
df_verso = pd.DataFrame(columns=colunas)

for i in range(6):
    df_frente = df_frente.append(pd.DataFrame([crachas_frente[i*10: (i+1) * 10] + 10 * [True]], columns=colunas), ignore_index=True)
    df_verso = df_verso.append(pd.DataFrame([crachas_verso[i*10: (i+1) * 10] + 10 * [True]], columns=colunas), ignore_index=True)

df_frente.to_csv('gabarito_frente.csv', index=False)
df_verso.to_csv('gabarito_verso.csv', index=False)