# -*- coding: utf-8 -*-
import os
import sys
import shutil
import re
import argparse
from pathlib import Path

# Ajustar sys.path para carregar o precheck
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "00_SISTEMA_PRECHECK"))

try:
    from precheck_regras import executar_precheck, normalizar_texto
    executar_precheck("gerar_conferencia_cliente.py")
except ImportError as e:
    print(f"ERRO: Nao foi possivel carregar o precheck de regras: {e}")
    sys.exit(1)

try:
    from config_widepay_cdp import CDP_PORT
except ImportError:
    CDP_PORT = 9444

from widepay_bootstrap import garantir_widepay_real_ou_parar

PASTAS_PROJETO = {
    "Importados": ROOT_DIR / "00_IMPORTAR_DOCUMENTOS",
    "Documentos Convertidos": ROOT_DIR / "01_DOCUMENTOS_CONVERTIDOS",
    "Dados Temporarios": ROOT_DIR / "07_DADOS_TEMPORARIOS",
    "Agua Viva": Path(r"C:\Users\Windows User\Desktop\AGUA VIVA\- CONTRATOS AGUA VIVA")
}

def localizar_diretorio_cliente(query):
    base_dir = PASTAS_PROJETO["Agua Viva"]
    if not base_dir.exists():
        print(f"ERRO: Diretorio de consulta do Agua Viva nao encontrado: {base_dir}")
        return None
        
    query_parts = [normalizar_texto(p) for p in query.split() if p.strip()]
    matches = []
    
    for root, dirs, files in os.walk(base_dir):
        for d in dirs:
            d_norm = normalizar_texto(d)
            if all(qp in d_norm for qp in query_parts):
                matches.append(Path(root) / d)
                
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

def identificar_referencias_pagamento(descricao):
    texto = normalizar_texto(descricao or "")
    refs = []
    meses_nome = {
        "janeiro": "01", "jan": "01", "fevereiro": "02", "fev": "02",
        "marco": "03", "mar": "03", "abril": "04", "abr": "04",
        "maio": "05", "mai": "05", "junho": "06", "jun": "06",
        "julho": "07", "jul": "07", "agosto": "08", "ago": "08",
        "setembro": "09", "set": "09", "outubro": "10", "out": "10",
        "novembro": "11", "nov": "11", "dezembro": "12", "dez": "12",
    }
    for nome, numero in meses_nome.items():
        if re.search(rf"\b{re.escape(nome)}\b", texto) and numero not in refs:
            refs.append(numero)
    if any(t in texto for t in ("ref", "referente", "atraso", "atrazo", "parcela", "apart", "competencia", "mes", "meses")):
        for token in re.findall(r"\b\d{1,2}\b", texto):
            mes = int(token)
            if 1 <= mes <= 12:
                ref = f"{mes:02d}"
                if ref not in refs:
                    refs.append(ref)
    return refs

def interpretar_cobrancas_recebidas(dados, cobrancas):
    valor_base = float(dados.get("valor_parcela") or 0.0)
    interpretados = []
    for cob in cobrancas:
        if "recebido" not in str(cob.get("status", "")).lower():
            continue
        refs = identificar_referencias_pagamento(cob.get("descricao", ""))
        tipo = "Carne" if cob.get("pertence_a_carne") else "Avulsa"
        obs = []
        if refs:
            qtd = len(refs)
            obs.append("referencias identificadas na descricao")
        elif cob.get("pertence_a_carne"):
            qtd = 1
            refs = [cob.get("vencimento") or "vencimento do boleto"]
            obs.append("boleto de carne tratado pelo vencimento")
        elif valor_base > 0 and cob.get("valor_original", 0) > 0:
            proporcao = float(cob.get("valor_original", 0)) / valor_base
            qtd = max(1, int(round(proporcao)))
            if abs(proporcao - qtd) <= 0.20:
                obs.append("quantidade inferida por valor original/base da parcela")
            else:
                obs.append("REFERENCIA NAO IDENTIFICADA - proporcao de valor nao exata")
        else:
            qtd = 1
            obs.append("REFERENCIA NAO IDENTIFICADA")
        interpretados.append({
            "id": cob.get("id", "-"),
            "tipo": tipo,
            "descricao": cob.get("descricao", "-") or "-",
            "vencimento": cob.get("vencimento", "-"),
            "pagamento": cob.get("pagamento", "-"),
            "valor_original": float(cob.get("valor_original") or 0.0),
            "valor_recebido": float(cob.get("valor_recebido") or 0.0),
            "valor_base": valor_base,
            "refs": ", ".join(refs) if refs else "REFERENCIA NAO IDENTIFICADA",
            "qtd": qtd,
            "obs": "; ".join(obs),
        })
    return interpretados

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

def consultar_widepay_real(nome_cliente):
    """
    Tenta consultar o WidePay real em modo somente leitura via CDP.
    """
    import subprocess
    import json
    
    script_path = ROOT_DIR / "03_SCRIPTS" / "consultar_widepay_cdp.py"
    print(f"\nChamando script de consulta CDP: {script_path} para o cliente: {nome_cliente}...")
    try:
        # Executar o subprocesso
        result = subprocess.run(
            [sys.executable, str(script_path), "--cliente", nome_cliente],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        print(result.stdout)
        if result.stderr:
            print(f"Stderr do script de consulta:\n{result.stderr}")
            
        # O arquivo JSON esperado e gerado por consultar_widepay_cdp.py
        # Usamos o nome pesquisado para localizar o JSON gerado
        nome_limpo = nome_cliente.replace(" ", "_").upper()
        caminho_json = ROOT_DIR / "07_DADOS_TEMPORARIOS" / "WIDEPAY_CONSULTAS" / f"WIDEPAY_{nome_limpo}.json"
        
        # Se não encontrar com o nome original, tenta normalizar/limpar (ex: Filinto Queiroz de Almeida -> Filinto Queiroz)
        if not caminho_json.exists():
            # Tentar encontrar qualquer JSON que comece com o primeiro nome na pasta de consultas
            primeiro_nome = nome_cliente.split()[0].upper()
            pasta_consultas = ROOT_DIR / "07_DADOS_TEMPORARIOS" / "WIDEPAY_CONSULTAS"
            if pasta_consultas.exists():
                for f_name in os.listdir(pasta_consultas):
                    if f_name.startswith(f"WIDEPAY_{primeiro_nome}") and f_name.endswith(".json"):
                        caminho_json = pasta_consultas / f_name
                        break
                        
        if caminho_json.exists():
            with open(caminho_json, "r", encoding="utf-8") as f:
                dados_wp = json.load(f)
            
            if dados_wp.get("status_conexao") != "LOGADO":
                print("WidePay está offline ou deslogado.")
                return None
                
            return dados_wp
            
    except Exception as e:
        print(f"Erro ao chamar consulta CDP: {e}")
        
    return None

def gerar_markdown_conferencia(dados, dados_wp, caminho_md):
    if not isinstance(dados_wp, dict):
        # WidePay não foi consultado ou falhou
        conteudo = f"""# RELATÓRIO DE CONFERÊNCIA — {dados['cliente'].upper()}
# Gerado em: 16/06/2026
# Finalidade: Auditar cálculos antes de gerar o PDF final

---

## 1. DADOS DO CONTRATO
| Campo                    | Valor                          |
|--------------------------|--------------------------------|
| Cliente                  | {dados['cliente']} |
| Lote                     | {dados['lote']} (Quadra {dados['quadra']}) |
| Empreendimento           | Fazenda Água Viva, Iaçú-BA     |
| Área                     | {dados['area']} |
| Entrada                  | R$ {dados['entrada']:.2f} |
| Total de parcelas        | **{dados['total_parcelas']} parcelas** |
| Status do contrato       | {'CONTRATO CONFIRMADO' if dados['total_parcelas'] > 0 else 'CONTRATO NAO CONFIRMADO - parcelas restantes bloqueadas'} |
| Valor de cada parcela    | R$ {dados['valor_parcela']:.2f} (nominal) |
| Valor total do contrato  | R$ {dados['valor_total_contrato']:.2f} |
| Vencimento               | {dados['vencimento']} |
| Data de assinatura       | {dados['data_assinatura']} |
| Previsão de quitação     | {dados['previsao_quitacao']} |

---

## 2. CARNÊS ENCONTRADOS
WIDEPAY NÃO CONSULTADO — AGUARDANDO LOGIN MANUAL, PRINTS OU EXPORTAÇÃO DO USUÁRIO.

---

## 3. COBRANÇAS/BOLETOS ENCONTRADOS
WIDEPAY NÃO CONSULTADO.

---

## 4. BOLETOS AVULSOS RECEBIDOS
WIDEPAY NÃO CONSULTADO.

---

## 5. BOLETOS AVULSOS EM ABERTO
WIDEPAY NÃO CONSULTADO.

---

## 6. POSSÍVEIS DUPLICIDADES
WIDEPAY NÃO CONSULTADO.

---

## 7. TOTAL PAGO EM CARNÊS
R$ 0,00 (WIDEPAY NÃO CONSULTADO)

---

## 8. TOTAL PAGO EM COBRANÇAS AVULSAS
R$ 0,00 (WIDEPAY NÃO CONSULTADO)

---

## 9. TOTAL PAGO CONSOLIDADO
R$ 0,00 (WIDEPAY NÃO CONSULTADO)

---

## 10. TOTAL PENDENTE CONSOLIDADO
R$ 0,00 (WIDEPAY NÃO CONSULTADO)

---

## 11. DIVERGÊNCIAS
Acesso ao WidePay pendente.

---

## 12. STATUS
`AGUARDANDO VALIDAÇÃO DO USUÁRIO`
"""
        with open(caminho_md, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return

    # WidePay consultado com sucesso
    carnes = dados_wp.get("carnes") or []
    cobrancas = dados_wp.get("cobrancas") or []
    boletos_avulsos = dados_wp.get("boletos_avulsos") or []
    possiveis_duplicidades = dados_wp.get("possiveis_duplicidades") or []
    totais_carnes = dados_wp.get("totais_carnes") or {}
    totais_cobrancas_avulsas = dados_wp.get("totais_cobrancas_avulsas") or {}
    totais_consolidados = dados_wp.get("totais_consolidados") or {}
    
    # 2. Carnês
    linhas_carnes = "| Carnê | Valor/Parcela | Parcelas Geradas | Parcelas Pagas | Total Recebido | Último Vencimento | Status     |\n"
    linhas_carnes += "|-------|--------------|------------------|----------------|----------------|-------------------|------------|\n"
    for c in carnes:
        linhas_carnes += f"| {c['carne']} | R$ {c['valor_parcela']:.2f} | {c['parcelas_geradas']} | {c['parcelas_pagas']} | R$ {c['total_recebido']:.2f} | {c['ultimo_vencimento']} | {c['status']} |\n"
        
    # 3. Cobranças/Boletos Encontrados
    linhas_cobrancas = "| ID | Forma | Descrição | Valor Original | Valor Recebido | Vencimento | Status | Tipo |\n"
    linhas_cobrancas += "|----|-------|-----------|----------------|----------------|------------|--------|------|\n"
    for cob in cobrancas:
        tipo = "Carnê" if cob["pertence_a_carne"] else "Avulsa"
        linhas_cobrancas += f"| {cob['id']} | {cob['forma']} | {cob['descricao']} | R$ {cob['valor_original']:.2f} | R$ {cob['valor_recebido']:.2f} | {cob['vencimento']} | {cob['status']} | {tipo} |\n"
        
    # 4. Boletos Avulsos Recebidos
    linhas_avulsos_recebidos = ""
    avulsos_recebidos = [cob for cob in boletos_avulsos if cob["status"] == "Recebido"]
    if avulsos_recebidos:
        linhas_avulsos_recebidos = "| ID | Descrição | Valor Recebido | Vencimento | Pagamento | Status |\n"
        linhas_avulsos_recebidos += "|----|-----------|----------------|------------|-----------|--------|\n"
        for cob in avulsos_recebidos:
            linhas_avulsos_recebidos += f"| {cob['id']} | {cob['descricao']} | R$ {cob['valor_recebido']:.2f} | {cob['vencimento']} | {cob['pagamento']} | {cob['status']} |\n"
    else:
        linhas_avulsos_recebidos = "Nenhum boleto avulso recebido."
        
    # 5. Boletos Avulsos em Aberto
    linhas_avulsos_abertos = ""
    avulsos_abertos = [cob for cob in boletos_avulsos if cob["status"] in ["Aguardando", "Vencido"]]
    if avulsos_abertos:
        linhas_avulsos_abertos = "| ID | Descrição | Valor Original | Vencimento | Status |\n"
        linhas_avulsos_abertos += "|----|-----------|----------------|------------|--------|\n"
        for cob in avulsos_abertos:
            linhas_avulsos_abertos += f"| {cob['id']} | {cob['descricao']} | R$ {cob['valor_original']:.2f} | {cob['vencimento']} | {cob['status']} |\n"
    else:
        linhas_avulsos_abertos = "Nenhum boleto avulso em aberto/vencido."
        
    # 6. Possíveis Duplicidades
    linhas_duplicidades = ""
    if possiveis_duplicidades:
        linhas_duplicidades = "| ID | Descrição | Valor Original | Valor Recebido | Vencimento | Status |\n"
        linhas_duplicidades += "|----|-----------|----------------|----------------|------------|--------|\n"
        for cob in possiveis_duplicidades:
            linhas_duplicidades += f"| {cob['id']} | {cob['descricao']} | R$ {cob['valor_original']:.2f} | R$ {cob['valor_recebido']:.2f} | {cob['vencimento']} | {cob['status']} |\n"
    else:
        linhas_duplicidades = "Nenhuma possível duplicidade encontrada."

    pagamentos_interpretados = interpretar_cobrancas_recebidas(dados, cobrancas)
    if pagamentos_interpretados:
        linhas_pagamentos_interpretados = "| Cliente | Lote/Quadra | ID | Tipo | Descricao WidePay | Vencimento | Pagamento | Valor Original | Valor Recebido | Valor Base Parcela | Referencias | Qtd. Parcelas | Observacao |\n"
        linhas_pagamentos_interpretados += "|---------|-------------|----|------|-------------------|------------|-----------|----------------|----------------|--------------------|-------------|---------------|------------|\n"
        for p in pagamentos_interpretados:
            linhas_pagamentos_interpretados += (
                f"| {dados['cliente']} | {dados['lote']} / {dados['quadra']} | {p['id']} | {p['tipo']} | {p['descricao']} | "
                f"{p['vencimento']} | {p['pagamento']} | R$ {p['valor_original']:.2f} | R$ {p['valor_recebido']:.2f} | "
                f"R$ {p['valor_base']:.2f} | {p['refs']} | {p['qtd']} | {p['obs']} |\n"
            )
    else:
        linhas_pagamentos_interpretados = "Nenhum pagamento recebido interpretado."
        
    # Divergências
    notas = []
    total_geradas = totais_carnes.get("parcelas_geradas", 0)
    if dados['total_parcelas'] <= 0:
        notas.append("Contrato local nao confirmou o total de parcelas; parcelas restantes ficam bloqueadas e nao podem ser calculadas pelas parcelas geradas no WidePay.")
    elif total_geradas > dados['total_parcelas']:
        notas.append(f"O total de parcelas geradas nos carnês do WidePay ({total_geradas}) excede o total pactuado no contrato ({dados['total_parcelas']}).")
    elif total_geradas < dados['total_parcelas'] and total_geradas > 0:
        notas.append(f"Ainda há parcelas a serem geradas nos carnês do WidePay ({dados['total_parcelas'] - total_geradas} restantes no contrato).")
        
    if boletos_avulsos:
        notas.append(f"Foram identificadas {len(boletos_avulsos)} cobranças avulsas no WidePay, totalizando R$ {totais_cobrancas_avulsas.get('total_pago', 0.0):.2f} pago e R$ {totais_cobrancas_avulsas.get('total_pendente', 0.0):.2f} pendente.")
        
    if possiveis_duplicidades:
        notas.append(f"Atenção: Foram detectadas {len(possiveis_duplicidades)} possíveis duplicidades no histórico de cobranças que foram desconsideradas dos totais.")
        
    if not notas:
        notas.append("Nenhuma divergência crítica identificada.")
    linhas_divergencias = "\n".join(f"- {n}" for n in notas)
    
    conteudo = f"""# RELATÓRIO DE CONFERÊNCIA — {dados['cliente'].upper()}
# Gerado em: 16/06/2026
# Finalidade: Auditar cálculos antes de gerar o PDF final

---

## 1. DADOS DO CONTRATO (Fonte: Contrato físico localizado na pasta de consulta)

| Campo                    | Valor                          |
|--------------------------|--------------------------------|
| Cliente                  | {dados['cliente']} |
| Lote                     | {dados['lote']} (Quadra {dados['quadra']}) |
| Empreendimento           | Fazenda Água Viva, Iaçú-BA     |
| Área                     | {dados['area']} |
| Entrada                  | R$ {dados['entrada']:.2f} |
| Total de parcelas        | **{dados['total_parcelas']} parcelas** |
| Status do contrato       | {'CONTRATO CONFIRMADO' if dados['total_parcelas'] > 0 else 'CONTRATO NAO CONFIRMADO - parcelas restantes bloqueadas'} |
| Valor de cada parcela    | R$ {dados['valor_parcela']:.2f} (nominal) |
| Valor total do contrato  | R$ {dados['valor_total_contrato']:.2f} |
| Vencimento               | {dados['vencimento']} |
| Data de assinatura       | {dados['data_assinatura']} |
| Previsão de quitação     | {dados['previsao_quitacao']} |

---

## 2. CARNÊS ENCONTRADOS (Fonte: Histórico de Carnês no WidePay)

{linhas_carnes}

---

## 3. COBRANÇAS/BOLETOS ENCONTRADOS (Fonte: Histórico de Cobranças no WidePay)

{linhas_cobrancas}

---

## 4. BOLETOS AVULSOS RECEBIDOS (Exclui duplicidades e boletos vinculados a carnês)

{linhas_avulsos_recebidos}

---

## 5. BOLETOS AVULSOS EM ABERTO

{linhas_avulsos_abertos}

---

## 6. POSSÍVEIS DUPLICIDADES (Desconsiderados dos cálculos para evitar dupla contagem)

{linhas_duplicidades}

---

## 6.1 PAGAMENTOS RECEBIDOS INTERPRETADOS

{linhas_pagamentos_interpretados}

---

## 7. TOTAL PAGO EM CARNÊS
R$ {totais_carnes.get('total_pago', 0.0):.2f} (baseado em {totais_carnes.get('parcelas_pagas', 0)} parcelas pagas nos carnês)

---

## 8. TOTAL PAGO EM COBRANÇAS AVULSAS
R$ {totais_cobrancas_avulsas.get('total_pago', 0.0):.2f}

---

## 9. TOTAL PAGO CONSOLIDADO
R$ {totais_consolidados.get('total_pago_consolidado', 0.0):.2f} (Carnês + Avulsos pagos)

---

## 10. TOTAL PENDENTE CONSOLIDADO
R$ {totais_consolidados.get('total_pendente_consolidado', 0.0):.2f} (Carnês pendentes + Avulsos em aberto/vencidos)

---

## 11. DIVERGÊNCIAS E AUDITORIA

{linhas_divergencias}

---

## 12. STATUS
`AGUARDANDO VALIDAÇÃO DO USUÁRIO`
"""
    with open(caminho_md, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"Relatorio de conferencia MD gerado em: {caminho_md}")

def main():
    parser = argparse.ArgumentParser(description="Gera conferencia de calculos de clientes de forma generica.")
    parser.add_argument("--cliente", required=True, help="Nome do cliente para busca e geracao.")
    parser.add_argument("--lote", help="Lote especifico (opcional).")
    parser.add_argument("--widepay-url", help="Link especifico do WidePay (opcional).")
    parser.add_argument("--usar-json", action="store_true", help="Usa o JSON existente para gerar a conferencia sem nova consulta")
    args = parser.parse_args()
    
    cliente_query = args.cliente
    print(f"Iniciando fluxo para o cliente: {cliente_query}...")

    garantir_widepay_real_ou_parar(cliente_query)
    
    # 1. Localizar pasta do cliente no Água Viva
    matches = localizar_diretorio_cliente(cliente_query)
    if not matches:
        print(f"AVISO: Nenhuma pasta contendo '{cliente_query}' encontrada na pasta de contratos. Seguindo somente com WidePay.")
        pasta_cliente = None
    elif len(matches) > 1:
        print(f"Multiplos resultados encontrados para '{cliente_query}':")
        for idx, m in enumerate(matches):
            print(f"  [{idx + 1}] {m.name}")
        # Se houver lote opcional, tenta desambiguar
        if args.lote:
            lote_norm = normalizar_texto(args.lote)
            filtrado = [m for m in matches if lote_norm in normalizar_texto(m.name)]
            if len(filtrado) == 1:
                pasta_cliente = filtrado[0]
                print(f"Desambiguado pelo lote '{args.lote}': {pasta_cliente.name}")
            else:
                print("Use o parametro --lote para filtrar um resultado unico.")
                sys.exit(1)
        else:
            print("Selecione um cliente informando o --lote correspondente.")
            sys.exit(1)
    else:
        pasta_cliente = matches[0]
        
    if pasta_cliente:
        print(f"Pasta do cliente localizada: {pasta_cliente}")
    else:
        print("Contrato local nao localizado; dados contratuais ficarao pendentes.")
    
    # 2. Localizar o contrato (docx ou pdf)
    contratos = []
    if pasta_cliente:
        for file in os.listdir(pasta_cliente):
            file_lower = file.lower()
            if file_lower.endswith(('.docx', '.pdf')) and "carne" not in file_lower and "recibo" not in file_lower and "wp-pdf" not in file_lower:
                contratos.append(pasta_cliente / file)
            
    if not contratos:
        print("AVISO: Nenhum contrato (.docx ou .pdf) localizado na pasta do cliente. Usando dados padrao.")
        contrato_arquivo = None
    else:
        # Prioritizar docx em relação a pdf
        docx_contratos = [c for c in contratos if c.suffix.lower() == '.docx']
        if docx_contratos:
            contrato_arquivo = docx_contratos[0]
        else:
            # Selecionar o maior arquivo como provável contrato
            contratos.sort(key=lambda x: x.stat().st_size, reverse=True)
            contrato_arquivo = contratos[0]
        print(f"Contrato localizado: {contrato_arquivo.name}")
        
    # 3. Copiar contrato para 00_IMPORTAR_DOCUMENTOS
    texto_contrato = ""
    dados_contrato = {
        'cliente': cliente_query,
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
    
    if contrato_arquivo:
        destino_import = PASTAS_PROJETO["Importados"] / contrato_arquivo.name
        print(f"Copiando contrato para: {destino_import}...")
        shutil.copy(contrato_arquivo, destino_import)
        
        # 4. Converter contrato para 01_DOCUMENTOS_CONVERTIDOS
        ext = contrato_arquivo.suffix.lower()
        nome_base = contrato_arquivo.stem
        destino_txt = PASTAS_PROJETO["Documentos Convertidos"] / f"{nome_base}_convertido.txt"
        
        print(f"Convertendo contrato para texto em: {destino_txt}...")
        if ext == '.docx':
            texto_contrato = extrair_texto_docx(destino_import)
        elif ext == '.pdf':
            texto_contrato = extrair_texto_pdf(destino_import)
            
        with open(destino_txt, "w", encoding="utf-8") as f:
            f.write(texto_contrato)
            
        # Parsear dados do contrato
        dados_contrato = parsear_dados_contrato(texto_contrato, contrato_arquivo.parent.name)
        
    # Ajustar nome limpo do cliente para o arquivo de conferência
    nome_limpo = re.sub(r'[^a-zA-Z0-9]', '_', normalizar_texto(dados_contrato['cliente']).upper())
    
    # 5. Tentar consultar WidePay real em modo somente leitura (Simulações removidas!)
    # 5. Tentar consultar WidePay real em modo somente leitura (Simulações removidas!)
    dados_wp = None
    if getattr(args, 'usar_json', False):
        print("Usando JSON existente (cache)...")
        caminho_json = ROOT_DIR / "07_DADOS_TEMPORARIOS" / "WIDEPAY_CONSULTAS" / f"WIDEPAY_{nome_limpo}.json"
        if caminho_json.exists():
            import json
            try:
                with open(caminho_json, "r", encoding="utf-8") as f:
                    dados_wp = json.load(f)
                
                # Recalcular usando o novo heurístico
                carnes_lista = dados_wp.get("carnes") or []
                raw_cobrancas = dados_wp.get("cobrancas") or []
                
                cobrancas_lista = []
                boletos_avulsos = []
                possiveis_duplicidades = []
                cobrancas_unicas = []
                
                for cob in raw_cobrancas:
                    is_duplicate = False
                    for existing in cobrancas_unicas:
                        if (existing["id"] == cob["id"] and cob["id"]) or (
                            existing["descricao"] == cob["descricao"] and 
                            existing["vencimento"] == cob["vencimento"] and 
                            abs(existing["valor_original"] - cob["valor_original"]) < 0.01 and 
                            abs(existing["valor_recebido"] - cob["valor_recebido"]) < 0.01 and 
                            existing["status"] == cob["status"]
                        ):
                            is_duplicate = True
                            break
                            
                    desc_lower = cob["descricao"].lower()
                    pertence_a_carne = "carne" in desc_lower or "carnê" in desc_lower
                    
                    if not pertence_a_carne:
                        for c in carnes_lista:
                            if c["status"].lower() != "cancelado":
                                if abs(cob["valor_original"] - float(c["valor_parcela"])) < 0.01:
                                    ref_lower = c["referencia"].lower()
                                    if not cob["descricao"].strip() or (ref_lower and ref_lower in desc_lower):
                                        if not any(word in desc_lower for word in ["atraso", "atrazos", "ref atraso", "atr", "mês", "mes"]):
                                            pertence_a_carne = True
                                            break
                                            
                    cob["pertence_a_carne"] = pertence_a_carne
                    cob["avulsa"] = not pertence_a_carne
                    cob["duplicidade"] = is_duplicate
                    cobrancas_lista.append(cob)
                    
                    if is_duplicate:
                        possiveis_duplicidades.append(cob)
                    else:
                        cobrancas_unicas.append(cob)
                        if cob["avulsa"]:
                            boletos_avulsos.append(cob)
                            
                # Recalcular totais
                total_pago_carnes = 0.0
                total_pendente_carnes = 0.0
                total_pagas_carnes = 0
                total_geradas_carnes = 0
                
                for c in carnes_lista:
                    if c["status"].lower() != "cancelado":
                        total_pago_carnes += float(c["total_recebido"])
                        total_pendente_carnes += float(c["total_pendente"])
                        total_pagas_carnes += int(c["parcelas_pagas"])
                        total_geradas_carnes += int(c["parcelas_geradas"])
                        
                totais_carnes = {
                    "total_pago": round(total_pago_carnes, 2),
                    "total_pendente": round(total_pendente_carnes, 2),
                    "parcelas_pagas": total_pagas_carnes,
                    "parcelas_geradas": total_geradas_carnes
                }
                
                total_pago_avulsas = 0.0
                total_pendente_avulsas = 0.0
                for cob in boletos_avulsos:
                    if cob["status"] == "Recebido":
                        total_pago_avulsas += cob["valor_recebido"]
                    elif cob["status"] in ["Aguardando", "Vencido"]:
                        total_pendente_avulsas += cob["valor_original"]
                        
                totais_cobrancas_avulsas = {
                    "total_pago": round(total_pago_avulsas, 2),
                    "total_pendente": round(total_pendente_avulsas, 2)
                }
                
                totais_consolidados = {
                    "total_pago_consolidado": round(total_pago_carnes + total_pago_avulsas, 2),
                    "total_pendente_consolidado": round(total_pendente_carnes + total_pendente_avulsas, 2)
                }
                
                dados_wp["cobrancas"] = cobrancas_lista
                dados_wp["boletos_avulsos"] = boletos_avulsos
                dados_wp["possiveis_duplicidades"] = possiveis_duplicidades
                dados_wp["totais_carnes"] = totais_carnes
                dados_wp["totais_cobrancas_avulsas"] = totais_cobrancas_avulsas
                dados_wp["totais_consolidados"] = totais_consolidados
                
            except Exception as e:
                print(f"Erro ao ler/reprocessar JSON de cache: {e}")
        else:
            print("Aviso: JSON de cache nao encontrado. Tentando consultar...")
            dados_wp = consultar_widepay_real(cliente_query)
    else:
        dados_wp = consultar_widepay_real(cliente_query)
    
    # 6. Gerar conferência em 07_DADOS_TEMPORARIOS
    caminho_md = PASTAS_PROJETO["Dados Temporarios"] / f"CONFERENCIA_CALCULOS_{nome_limpo}.md"
    gerar_markdown_conferencia(dados_contrato, dados_wp, caminho_md)
    
    print("\n[PROCESSO CONCLUIDO]")
    print(f"A conferencia MD foi criada com sucesso.")
    print("O processo de compilacao do PDF foi pausado aguardando validacao manual dos dados.")
    print(f"Caminho do MD: {caminho_md}")

if __name__ == "__main__":
    main()
