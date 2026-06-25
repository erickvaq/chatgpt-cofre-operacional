# -*- coding: utf-8 -*-
import os
import shutil
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

PASTAS_PROJETO = {
    "Importados": ROOT_DIR / "00_IMPORTAR_DOCUMENTOS",
    "Documentos Convertidos": ROOT_DIR / "01_DOCUMENTOS_CONVERTIDOS",
    "Agua Viva": Path(r"C:\Users\Windows User\Desktop\AGUA VIVA\- CONTRATOS AGUA VIVA")
}

def normalizar_texto(texto):
    if not texto:
        return ""
    texto = texto.lower()
    # Substituir acentos comuns
    substituicoes = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u',
        'ã': 'a', 'õ': 'o', 'ç': 'c',
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
    }
    for k, v in substituicoes.items():
        texto = texto.replace(k, v)
    return texto.strip()

def localizar_diretorio_cliente(query, lote=None):
    base_dir = PASTAS_PROJETO["Agua Viva"]
    if not base_dir.exists():
        print(f"Aviso: Diretorio do Agua Viva nao encontrado: {base_dir}")
        return []
        
    query_parts = [normalizar_texto(p) for p in query.split() if p.strip()]
    matches = []
    
    for root, dirs, files in os.walk(base_dir):
        for d in dirs:
            d_norm = normalizar_texto(d)
            if all(qp in d_norm for qp in query_parts):
                matches.append(Path(root) / d)
                
    if lote and len(matches) > 1:
        lote_norm = normalizar_texto(lote)
        matches = [m for m in matches if lote_norm in normalizar_texto(m.name)]
        
    return matches

def extrair_texto_docx(caminho_docx):
    import zipfile
    import xml.etree.ElementTree as ET
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragrafos = []
    try:
        with zipfile.ZipFile(caminho_docx) as z:
            xml_content = z.read('word/document.xml')
            root = ET.fromstring(xml_content)
            for p in root.findall('.//w:p', ns):
                texto = "".join(t.text or "" for t in p.findall('.//w:t', ns))
                paragrafos.append(texto)
        return "\n".join(paragrafos)
    except Exception as e:
        print(f"Erro ao extrair DOCX: {e}")
        return ""

def extrair_texto_pdf(caminho_pdf):
    try:
        import pypdf
        reader = pypdf.PdfReader(caminho_pdf)
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    except Exception as e:
        print(f"Erro ao extrair PDF: {e}")
        return ""

def parsear_dados_contrato(texto, nome_sugerido):
    dados = {
        'cliente': nome_sugerido,
        'lote': '-',
        'quadra': '-',
        'data_assinatura': '-',
        'vencimento': '-',
        'previsao_quitacao': '-',
        'valor_parcela': 0.0,
        'total_parcelas': 0,
        'valor_total_contrato': 0.0,
        'entrada': 0.0,
        'area': '-'
    }
    
    if not texto:
        return dados
        
    # Extrair lote e quadra
    lote_match = re.search(r'\blote\b\s*(?:nº\.?\s*)?([A-Za-z0-9]+)', texto, re.IGNORECASE)
    quadra_match = re.search(r'quadra\s*([A-H])', texto, re.IGNORECASE)
    if lote_match:
        dados['lote'] = lote_match.group(1).upper()
    if quadra_match:
        dados['quadra'] = quadra_match.group(1).upper()
        
    # Total de parcelas
    total_match = re.search(r'(\d+)\s*(?:\([^)]*\))?\s*parcelas', texto, re.IGNORECASE)
    if total_match:
        dados['total_parcelas'] = int(total_match.group(1))
        
    # Valor da parcela
    val_match = re.search(r'(?:parcela|prestacao|cada uma|sucessivas)\s*(?:de|no valor de|no valor cada uma de|no valor)?\s*R\$\s*(\d+[\.,]\d\d)', texto, re.IGNORECASE)
    if val_match:
        val_str = val_match.group(1).replace('.', '').replace(',', '.')
        dados['valor_parcela'] = float(val_str)
        
    # Entrada
    ent_match = re.search(r'(?:entrada|sinal)\s*(?:de|no valor de)?\s*R\$\s*(\d+[\.,]\d\d)', texto, re.IGNORECASE)
    if ent_match:
        ent_str = ent_match.group(1).replace('.', '').replace(',', '.')
        dados['entrada'] = float(ent_str)
        
    # Área
    area_match = re.search(r'(?:área total de|área de)\s*(\d+[\.,]?\d*)\s*(?:m²|metros quadrados)', texto, re.IGNORECASE)
    if not area_match:
        area_match = re.search(r'(\d+[\.,]?\d*)\s*(?:m²|metros quadrados)', texto, re.IGNORECASE)
    if area_match:
        dados['area'] = f"{area_match.group(1)} m²"
        
    # Data de assinatura
    data_match = re.search(r'(\d+\s*de\s*[a-zA-Z]+\s*de\s*\d{4})', texto, re.IGNORECASE)
    if data_match:
        dados['data_assinatura'] = data_match.group(1)
        
    dados['valor_total_contrato'] = dados['entrada'] + (dados['total_parcelas'] * dados['valor_parcela'])
    
    return dados

def carregar_dados_contrato(cliente_query, lote=None):
    """Localiza a pasta e arquivo de contrato, copia, converte e retorna dados estruturados."""
    matches = localizar_diretorio_cliente(cliente_query, lote)
    if not matches:
        print(f"Aviso: Nenhuma pasta contendo '{cliente_query}' localizada.")
        return None
        
    # Se houver múltiplos, escolhe o primeiro ou exige desambiguação
    pasta_cliente = matches[0]
    
    contratos = []
    for file in os.listdir(pasta_cliente):
        file_lower = file.lower()
        if file_lower.endswith(('.docx', '.pdf')) and "carne" not in file_lower and "recibo" not in file_lower and "wp-pdf" not in file_lower:
            contratos.append(pasta_cliente / file)
            
    if not contratos:
        print("Aviso: Nenhum arquivo de contrato (.docx ou .pdf) localizado na pasta do cliente.")
        return {
            'cliente': pasta_cliente.name,
            'lote': '-',
            'quadra': '-',
            'data_assinatura': '-',
            'vencimento': '-',
            'previsao_quitacao': '-',
            'valor_parcela': 0.0,
            'total_parcelas': 0,
            'valor_total_contrato': 0.0,
            'entrada': 0.0,
            'area': '-'
        }
        
    # Priorizar docx
    docx_contratos = [c for c in contratos if c.suffix.lower() == '.docx']
    contrato_arquivo = docx_contratos[0] if docx_contratos else sorted(contratos, key=lambda x: x.stat().st_size, reverse=True)[0]
    
    # Copiar e converter
    os.makedirs(PASTAS_PROJETO["Importados"], exist_ok=True)
    os.makedirs(PASTAS_PROJETO["Documentos Convertidos"], exist_ok=True)
    
    destino_import = PASTAS_PROJETO["Importados"] / contrato_arquivo.name
    shutil.copy(contrato_arquivo, destino_import)
    
    ext = contrato_arquivo.suffix.lower()
    nome_base = contrato_arquivo.stem
    destino_txt = PASTAS_PROJETO["Documentos Convertidos"] / f"{nome_base}_convertido.txt"
    
    texto_contrato = ""
    if ext == '.docx':
        texto_contrato = extrair_texto_docx(destino_import)
    elif ext == '.pdf':
        texto_contrato = extrair_texto_pdf(destino_import)
        
    with open(destino_txt, "w", encoding="utf-8") as f:
        f.write(texto_contrato)
        
    dados = parsear_dados_contrato(texto_contrato, pasta_cliente.name)
    return dados
