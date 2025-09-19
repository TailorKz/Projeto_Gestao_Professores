import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import re
import os

# --- CONFIGURAÇÃO DO TESSERACT ---
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


def extrair_texto_de_imagem(caminho_imagem):
    """Extrai texto de um arquivo de imagem usando Tesseract."""
    try:
        texto = pytesseract.image_to_string(Image.open(caminho_imagem), lang='por')
        return texto
    except Exception as e:
        print(f"Erro ao processar imagem {caminho_imagem}: {e}")
        return ""

def processar_nf(caminho_arquivo):
    """
    Processa um ficheiro (PDF ou Imagem) para extrair texto e depois
    procura informações específicas da Nota Fiscal.
    """
    texto_completo = ""
    
    if caminho_arquivo.lower().endswith('.pdf'):
        try:
            doc_pdf = fitz.open(caminho_arquivo)
            pagina = doc_pdf.load_page(0)
            pix = pagina.get_pixmap(dpi=200)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            texto_completo = pytesseract.image_to_string(img, lang='por')
            doc_pdf.close()
        except Exception as e:
            print(f"Erro ao processar PDF {caminho_arquivo}: {e}")
            return {}
    elif caminho_arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
        texto_completo = extrair_texto_de_imagem(caminho_arquivo)
    
    # --- Bloco de Debug ---
    print("----------- INÍCIO DO TEXTO EXTRAÍDO PELO OCR -----------")
    print(texto_completo)
    print("------------ FIM DO TEXTO EXTRAÍDO PELO OCR ------------")

    if not texto_completo:
        return {}

    dados_extraidos = {
        'numero': None,
        'data': None,
        'valor': None
    }

    # --- LÓGICA DE BUSCA MELHORADA ---

    # 1. Tenta o padrão de NÚMERO da nota fiscal mais recente (número no final da linha seguinte)
    match_numero = re.search(r'N[úu]mero\s+da\s+NFS-e\s*\n.*?(\d+)\s*$', texto_completo, re.IGNORECASE | re.MULTILINE)
    
    # 2. Se o primeiro padrão falhar, tenta o padrão antigo (número no início da linha seguinte)
    if not match_numero:
        match_numero = re.search(r'N[úu]mero\s+da\s+NFS-e.*?\n(\d+)', texto_completo, re.IGNORECASE)

    if match_numero:
        dados_extraidos['numero'] = match_numero.group(1).strip()

    # Padrão para DATA DE EMISSÃO
    match_data = re.search(r'(\d{2}/\d{2}/\d{4})', texto_completo)
    if match_data:
        dados_extraidos['data'] = match_data.group(1).strip()

    # Padrão para VALOR LÍQUIDO (já flexível)
    match_valor = re.search(r'Valor\s+L[íi]quido(?:\s+da\s+NFS-e)?\s*\n.*?(?:R\$\s*)?([\d\.,]+)\s*$', texto_completo, re.IGNORECASE | re.MULTILINE)
    if match_valor:
        valor_str = match_valor.group(1).replace('.', '').replace(',', '.')
        dados_extraidos['valor'] = float(valor_str)

    print(f"Dados extraídos de {os.path.basename(caminho_arquivo)}: {dados_extraidos}")
    return dados_extraidos