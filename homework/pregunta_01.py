"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import os
    import pandas as pd

    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", encoding="latin1")
    df = df.iloc[:, 1:]

    df.rename(columns={"lÃ­nea_credito": "línea_credito"}, inplace=True)

   # Lista de columnas de texto que quieres limpiar
    columnas_texto = [
    "sexo", "tipo_de_emprendimiento", "idea_negocio", 
    "línea_credito", "barrio"
    ]

    for col in columnas_texto:
        df[col] = df[col].str.replace("_", " ").str.replace("-", " ").str.lower()
        if col != "barrio":
            df[col] = df[col].str.strip()

    #Convertir estrato y comuna a enteros
    df["estrato"] = pd.to_numeric(df["estrato"]).astype("Int64")
    df["comuna_ciudadano"] = pd.to_numeric(df["comuna_ciudadano"]).astype("Int64")

    #Convertir monto del crédito a entero
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace("[$,]", "", regex=True)
        .astype(float)
        .astype(int)
    )

    #Eliminar filas con valores faltantes en columnas clave
    df = df.dropna(subset=[
        "sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio",
        "estrato", "comuna_ciudadano", "fecha_de_beneficio", 
        "monto_del_credito", "línea_credito"
    ]) 

    for col in columnas_texto:
        df = df[df[col] != 'nan']

        # Organizar columna "fecha_de_beneficio"
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(
        lambda f: f"{f.split('/')[2]}/{f.split('/')[1]}/{f.split('/')[0]}" if len(f.split('/')[0]) == 4 else f
    )

     # Eliminar duplicados ya con texto limpio
    df = df.drop_duplicates()

    #Crear carpeta de salida si no existe
    os.makedirs("files/output", exist_ok=True)

    #Guardar el archivo limpio
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)

    print(df.shape)

if __name__ == "__main__":
    pregunta_01()

