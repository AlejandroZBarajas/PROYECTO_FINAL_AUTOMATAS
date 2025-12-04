import re

ER_PALABRA_BASICA = r'^[a-záéíóúüñ]+$'

ER_PUNTUACION = r'^[.,;:¿?¡!]$'

ER_DIGITO = r'^\d+$'


def cargar_diccionario(archivo):
    diccionario_palabras_validas = set()
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                palabra = linea.strip().lower()
                if palabra:
                    diccionario_palabras_validas.add(palabra)
        
        print(f"Diccionario cargado")
        print("="*11 + "\n")
        return diccionario_palabras_validas
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'")
        return set()
    except Exception as e:
        print(f"Error al leer diccionario: {e}")
        return set()


def preprocesar_texto(texto):

    texto_normalizado = texto.lower()
    
    texto_separado = re.sub(r'([.,;:¿?¡!])', r' \1 ', texto_normalizado)
    
    lexemas = texto_separado.split()
    
    return lexemas


def clasificar_lexema(lexema, diccionario):

    if lexema in diccionario:
        return "PALABRA_VALIDA_ESPANOL"
    
    if re.match(ER_PUNTUACION, lexema):
        return "PUNTUACION"
    
    if re.match(ER_DIGITO, lexema):
        return "DIGITO"
    
    return "ERROR_ORTOGRAFICO"


def analizar_texto(archivo_entrada, diccionario):
    resultados = []
    
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            texto_completo = f.read()
        
        print(f"ANÁLISIS LÉXICO DE '{archivo_entrada}'")
        print(f"{'='*11}\n")
        
        
        
        lexemas = preprocesar_texto(texto_completo)
        
        print(f"Total de lexemas detectados: {len(lexemas)}\n")
        print(f"{'LEXEMA':<25} {'CLASIFICACIÓN':<30}")
        print(f"{'-'*50}")
        
        for lexema in lexemas:
            if lexema:  
                clasificacion = clasificar_lexema(lexema, diccionario)
                resultados.append((lexema, clasificacion))
                print(f"{lexema:<25} {clasificacion:<30}")
        
        return resultados
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_entrada}'")
        return []
    except Exception as e:
        print(f"Error al procesar texto: {e}")
        return []

def generar_reporte(resultados, archivo_salida='tokens_salida.txt'):
    if not resultados:
        return
    
    total = len(resultados)
    palabras_validas = sum(1 for _, tipo in resultados if tipo == "PALABRA_VALIDA_ESPANOL")
    puntuaciones = sum(1 for _, tipo in resultados if tipo == "PUNTUACION")
    digitos = sum(1 for _, tipo in resultados if tipo == "DIGITO")
    errores = sum(1 for _, tipo in resultados if tipo == "ERROR_ORTOGRAFICO")
    errores_lista = [lexema for lexema, tipo in resultados if tipo == "ERROR_ORTOGRAFICO"]
    errores_unicos = list(set(errores_lista))
    
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            
            f.write("\n")
            f.write("ZUÑIGA | VAZQUEZ | ZUÑIGA\n")
            f.write("="*11 + "\n")

            f.write("\n")
            f.write("ANÁLISIS LÉXICO DE 'texto_entrada.txt'\n")
            f.write("="*11 + "\n")
            f.write("\n")
            
            
            f.write("\n")
            
            f.write(f"{'LEXEMA':<26}{'CLASIFICACIÓN':<30}\n")
            f.write("-"*50 + "\n")
            f.write("\n")
            f.write("="*10 + "\n")
            for lexema, tipo in resultados:
                f.write(f"{lexema:<26}{tipo:<30}\n")
            
            f.write("\n")
            f.write("="*50 + "\n")
            f.write("\n")
            
            f.write(f"Total de lexemas detectados: {total}\n")
            f.write("="*5 + "\n")
            f.write(f"Total de palabras validas: {palabras_validas}\n")   
            f.write("="*5 + "\n")
            f.write(f"Total de signos de puntuacion: {puntuaciones}\n")
            f.write("="*5 + "\n")
            f.write(f"Total de dígitos: {digitos}\n")
            f.write("="*5 + "\n")
            f.write(f"Total de errores: {errores}\n")
            f.write("="*5 + "\n")
            
        print(f"\nReporte guardado en '{archivo_salida}'")
    except Exception as e:
        print(f"✗ Error al guardar reporte: {e}")
    except Exception as e:
        print(f"Error al guardar reporte: {e}")

def main():
    print("PRÁCTICA 2\n")
    print("ZUÑIGA | VAZQUEZ | ZUÑIGA\n")
    print("="*11 + "\n")
    
    ARCHIVO_DICCIONARIO = "diccionario_espanol.txt"
    ARCHIVO_ENTRADA = "texto_entrada.txt"
    
    diccionario = cargar_diccionario(ARCHIVO_DICCIONARIO)
    
    if not diccionario:
        print("No se puede continuar sin diccionario")
        return
    
    resultados = analizar_texto(ARCHIVO_ENTRADA, diccionario)
    
    generar_reporte(resultados)


if __name__ == "__main__":
    main()