import pandas as pd

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

def save_button():
    ...