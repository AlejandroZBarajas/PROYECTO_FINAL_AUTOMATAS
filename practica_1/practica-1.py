import re

def cargar_diccionario(archivo):

    diccionario = {}
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                palabra = linea.strip().lower()
                if palabra:  
                    token = f"KW_{palabra.upper()}"
                    diccionario[palabra] = token
        print(f"Diccionario cargado: {len(diccionario)} palabras clave")
        return diccionario
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'")
        return {}
    except Exception as e:
        print(f"Error al leer diccionario: {e}")
        return {}

REGEX = r'^[smrhif][a-z]{1,7}$'

def es_identificador_valido(palabra):

    return re.match(REGEX, palabra) is not None


def analizar_palabra(palabra, diccionario):

    palabra_lower = palabra.lower()
    
    if palabra_lower in diccionario:
        return diccionario[palabra_lower], palabra
    
    if es_identificador_valido(palabra_lower):
        return "IDENTIFICADOR", palabra_lower
    
    return "ERROR_LEXICO", palabra


def procesar_texto(archivo_entrada, diccionario):

    resultados = []
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        palabras = contenido.split()
        
        print(f"\n{'='*40}")
        print(f"Validación de '{archivo_entrada}'")
        print(f"{'='*40}\n")
        
        for palabra in palabras:
            if palabra:
                token, lexema = analizar_palabra(palabra, diccionario)
                resultados.append((lexema, token))
                print(f"  {lexema:20} -> {token}")
        
        return resultados
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_entrada}'")
        return []
    except Exception as e:
        print(f"Error al procesar texto: {e}")
        return []


def generar_reporte(resultados):
    if not resultados:
        return
    
    total = len(resultados)
    palabras_clave = sum(1 for _, token in resultados if token.startswith("KW_"))
    identificadores = sum(1 for _, token in resultados if token == "IDENTIFICADOR")
    errores = sum(1 for _, token in resultados if token == "ERROR_LEXICO")
    
    try:
        with open('tokens_salida.txt', 'w', encoding='utf-8') as f:
            
            f.write("\n")
            f.write("ZUÑIGA | VAZQUEZ | ZUÑIGA\n")
            f.write("="*40 + "\n")            
            f.write("\n")
            
            f.write(f"{"LEXEMA":<22} -> {"TOKEN"}\n")
            f.write(f"{'='*40}\n")
            
            for lexema, token in resultados:
                f.write(f"  {lexema:<20} -> {token}\n")

            f.write(f"{'='*40}\n")
            f.write(f"Total de tokens:     {total}\n")
            f.write(f"Palabras clave:      {palabras_clave}\n")
            f.write(f"Identificadores:     {identificadores}\n")
            f.write(f"Errores léxicos:     {errores}\n")
            
        print("\nReporte guardado en 'tokens_salida.txt'")
    except Exception as e:
        print(f"✗ Error al guardar reporte: {e}")


def main():

    print("Practica 1.")
    print("="*11 + "\n")
    
    ARCHIVO_DICCIONARIO = "diccionario.txt"
    ARCHIVO_ENTRADA = "texto_entrada.txt"
    
    diccionario = cargar_diccionario(ARCHIVO_DICCIONARIO)
    resultados = procesar_texto(ARCHIVO_ENTRADA, diccionario)
    generar_reporte(resultados)


if __name__ == "__main__":
    main()