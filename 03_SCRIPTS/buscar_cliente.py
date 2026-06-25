import os
import sys
import re
import unicodedata
from pathlib import Path

# Ajustar sys.path para carregar o precheck
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "00_SISTEMA_PRECHECK"))

try:
    from precheck_regras import executar_precheck, normalizar_texto
    executar_precheck("buscar_cliente.py")
except ImportError as e:
    print(f"ERRO: Nao foi possivel carregar o precheck de regras: {e}")
    sys.exit(1)

from widepay_bootstrap import garantir_widepay_real_ou_parar

# Se o argumento --precheck-only estiver presente, encerra com sucesso apos o precheck
if "--precheck-only" in sys.argv:
    print("Precheck concluido com sucesso. Modo --precheck-only ativo: Nao buscando cliente.")
    sys.exit(0)

# Caminhos padrão do projeto
PASTAS_PROJETO = {
    "Relatorios Gerados": ROOT_DIR / "02_RELATORIOS_GERADOS",
    "Dados Temporarios (Conferencia)": ROOT_DIR / "07_DADOS_TEMPORARIOS",
    "Contratos Clientes": ROOT_DIR / "01_CONTRATOS_CLIENTES",
    "Documentos Convertidos": ROOT_DIR / "01_DOCUMENTOS_CONVERTIDOS",
    "Importados": ROOT_DIR / "00_IMPORTAR_DOCUMENTOS",
    "Contratos Agua Viva (Somente Leitura)": Path(r"C:\Users\Windows User\Desktop\AGUA VIVA\- CONTRATOS AGUA VIVA")
}

def abrir_arquivo_externo(caminho):
    """Abre um arquivo ou diretorio usando a associacao padrao do Windows (equivalente a Start-Process)."""
    if not os.path.exists(caminho):
        print(f"ERRO: O arquivo/caminho nao existe: {caminho}")
        return False
    try:
        os.startfile(caminho)
        print(f"Abrindo com sucesso: {os.path.basename(caminho)}")
        return True
    except Exception as e:
        # Fallback usando subprocess se os.startfile der erro
        try:
            import subprocess
            subprocess.run(["cmd", "/c", "start", "", str(caminho)], shell=True)
            print(f"Abrindo com sucesso (via CMD): {os.path.basename(caminho)}")
            return True
        except Exception as err:
            print(f"ERRO ao abrir arquivo externamente: {err}")
            return False

def scan_arquivos_cliente(query):
    """Busca arquivos que contem o termo query de forma insensivel a acentos e caixa."""
    query_norm = normalizar_texto(query).replace("_", " ").replace("-", " ")
    arquivos_encontrados = []
    
    for nome_pasta, pasta in PASTAS_PROJETO.items():
        if not os.path.exists(pasta):
            continue
        for root, dirs, files in os.walk(pasta):
            for file in files:
                file_norm = normalizar_texto(file).replace("_", " ").replace("-", " ")
                if query_norm in file_norm:
                    arquivos_encontrados.append({
                        "nome": file,
                        "caminho": os.path.join(root, file),
                        "pasta_grupo": nome_pasta,
                        "extensao": os.path.splitext(file)[1].lower()
                    })
    return arquivos_encontrados

def obter_clientes_cadastrados():
    import re
    clientes = set()
    
    # 1. Buscar nas subpastas das quadras do Loteamento Agua Viva
    pasta_agua_viva = PASTAS_PROJETO.get("Contratos Agua Viva (Somente Leitura)")
    if pasta_agua_viva and os.path.exists(pasta_agua_viva):
        for quadra_dir in os.listdir(pasta_agua_viva):
            quadra_path = os.path.join(pasta_agua_viva, quadra_dir)
            if os.path.isdir(quadra_path) and "quadra" in quadra_dir.lower():
                for cliente_dir in os.listdir(quadra_path):
                    cliente_path = os.path.join(quadra_path, cliente_dir)
                    if os.path.isdir(cliente_path):
                        # Isolar o nome do cliente limpando do lote (ex: "Ana Carolina E7...")
                        nome = re.sub(r'\b[A-H]\d+\b', '', cliente_dir, flags=re.IGNORECASE)
                        nome = re.sub(r'\b(Lote|Quadra|Agua Viva|Leandro Meirelles|carne\d*|apart\d*|wp-pdf-\w+|v\d+|final|corrigido|previa)\b', '', nome, flags=re.IGNORECASE)
                        nome = re.sub(r'\b(docx|pdf|txt|html|md|jpg|jpeg|png)\b', '', nome, flags=re.IGNORECASE)
                        nome = nome.replace("-", " ").replace("_", " ").strip()
                        nome = re.sub(r'\s+', ' ', nome)
                        if len(nome) > 3:
                            clientes.add((nome.title(), cliente_dir))
                            
    # 2. Buscar em 01_CONTRATOS_CLIENTES
    pasta_contratos = PASTAS_PROJETO.get("Contratos Clientes")
    if pasta_contratos and os.path.exists(pasta_contratos):
        for cliente_dir in os.listdir(pasta_contratos):
            if os.path.isdir(os.path.join(pasta_contratos, cliente_dir)):
                nome = cliente_dir.replace("_", " ").replace("-", " ").strip()
                nome = re.sub(r'\s+', ' ', nome)
                if len(nome) > 3:
                    clientes.add((nome.title(), cliente_dir))
                    
    # 3. Buscar em 02_RELATORIOS_GERADOS
    pasta_relatorios = PASTAS_PROJETO.get("Relatorios Gerados")
    if pasta_relatorios and os.path.exists(pasta_relatorios):
        for item in os.listdir(pasta_relatorios):
            if os.path.isdir(os.path.join(pasta_relatorios, item)):
                # Se for uma pasta dedicada de cliente (ex: CAMILA_FERROLHO_V3_FINAL)
                nome = re.sub(r'(_V\d+|_FINAL|_CORRIGIDO)', '', item, flags=re.IGNORECASE)
                nome = nome.replace("_", " ").replace("-", " ").strip()
                nome = re.sub(r'\s+', ' ', nome)
                if len(nome) > 3 and "teste" not in nome.lower():
                    clientes.add((nome.title(), item))
                    
    return list(clientes)


def parsear_dados_conferencia(caminho_md):
    """Tenta extrair resumo financeiro estruturado a partir de um markdown de conferencia."""
    dados = {
        "cliente": None,
        "lote": None,
        "total_parcelas": None,
        "parcelas_pagas": None,
        "parcelas_restantes": None,
        "percentual_pago": None,
        "valor_pago": None,
        "valor_restante": None,
        "arquivo_origem": os.path.basename(caminho_md)
    }
    
    try:
        with open(caminho_md, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            
        for linha in linhas:
            if "|" in linha:
                partes = linha.split("|")
                if len(partes) >= 3:
                    col1 = normalizar_texto(partes[1].strip())
                    col2 = partes[2].strip().replace("**", "").replace("*", "")
                    
                    # Ignorar linha de separador (ex: |---|---|)
                    if not col1 or all(c == '-' for c in col1):
                        continue
                        
                    if "cliente" in col1 or "nome" in col1:
                        if "loteamento" not in col1 and not dados["cliente"]:
                            dados["cliente"] = col2
                    elif "lote" in col1 and not dados["lote"]:
                        dados["lote"] = col2
                    elif ("total de parcelas" in col1 or "total do contrato" in col1) and not dados["total_parcelas"]:
                        dados["total_parcelas"] = col2
                    elif "parcelas pagas" in col1 and not dados["parcelas_pagas"]:
                        dados["parcelas_pagas"] = col2
                    elif "parcelas restantes" in col1 and not dados["parcelas_restantes"]:
                        dados["parcelas_restantes"] = col2
                    elif "percentual pago" in col1 and not dados["percentual_pago"]:
                        dados["percentual_pago"] = col2
                    elif ("total pago" in col1 or "valor pago" in col1) and not dados["valor_pago"]:
                        dados["valor_pago"] = col2
                    elif ("total ainda a pagar" in col1 or "valor restante" in col1 or "a pagar" in col1) and not dados["valor_restante"]:
                        dados["valor_restante"] = col2
    except Exception as e:
        print(f"[AVISO PARSE] Nao foi possivel parsear o arquivo {caminho_md}: {e}")
        
    # Se conseguiu ler pelo menos o cliente ou lote, consideramos valido
    if dados["cliente"] or dados["lote"]:
        return dados
    return None

def gerar_painel_hta(dados, pdf_principal, html_previa, html_painel, conferencia_md):
    nome_cliente = dados["cliente"] or "Cliente Desconhecido"
    lote = dados["lote"] or "Nao informado"
    total_parcelas = dados["total_parcelas"] or "Nao informado"
    parcelas_pagas = dados["parcelas_pagas"] or "Nao informado"
    parcelas_restantes = dados["parcelas_restantes"] or "Nao informado"
    percentual_pago = dados["percentual_pago"] or "Nao informado"
    valor_pago = dados["valor_pago"] or "Nao informado"
    valor_restante = dados["valor_restante"] or "Nao informado"
    
    # Gerar nome de arquivo HTA limpo
    nome_limpo = re.sub(r'[^a-zA-Z0-9]', '_', normalizar_texto(nome_cliente).upper())
    pasta_paineis = ROOT_DIR / "07_DADOS_TEMPORARIOS" / "PAINEIS_CLIENTES"
    os.makedirs(pasta_paineis, exist_ok=True)
    caminho_hta = pasta_paineis / f"PAINEL_CLIENTE_{nome_limpo}.hta"
    
    # Escapar caminhos para JS do HTA
    def esc(p):
        return str(p).replace("\\", "\\\\") if p else ""
        
    js_pdf = esc(pdf_principal)
    js_previa = esc(html_previa)
    js_painel = esc(html_painel)
    js_pasta = esc(PASTAS_PROJETO["Relatorios Gerados"])
    js_conferencia = esc(conferencia_md)
    
    nome_pdf_base = os.path.basename(pdf_principal) if pdf_principal else "Nao localizado"
    
    # Conteudo HTML do HTA
    conteudo_hta = f"""<!DOCTYPE html>
<html>
<head>
    <title>Painel do Cliente - {nome_cliente}</title>
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <hta:application 
        id="oApp" 
        applicationname="PainelCliente" 
        border="thin" 
        borderstyle="normal" 
        caption="yes" 
        maximizebutton="no" 
        minimizebutton="yes" 
        showintaskbar="yes" 
        singleinstance="yes" 
        sysmenu="yes" 
        windowstate="normal" 
    />
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #ECEFF1;
            color: #37474F;
            margin: 0;
            padding: 20px;
        }}
        h2 {{
            color: #2E7D32;
            margin-top: 0;
            border-bottom: 2px solid #A5D6A7;
            padding-bottom: 10px;
            font-size: 18px;
        }}
        .dados-container {{
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        td {{
            padding: 6px 8px;
            border-bottom: 1px solid #ECEFF1;
            font-size: 13px;
        }}
        td.label {{
            font-weight: bold;
            color: #546E7A;
            width: 40%;
        }}
        .btn-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}
        button {{
            background-color: #2E7D32;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            font-size: 13px;
            height: 40px;
        }}
        button:hover {{
            background-color: #1B5E20;
        }}
        button:disabled {{
            background-color: #B0BEC5;
            color: #78909C;
            cursor: not-allowed;
        }}
        button.btn-secundario {{
            background-color: #1565C0;
        }}
        button.btn-secundario:hover {{
            background-color: #0D47A1;
        }}
        button.btn-secundario:disabled {{
            background-color: #B0BEC5;
            color: #78909C;
        }}
        button.btn-alerta {{
            background-color: #F9A825;
            color: #37474F;
        }}
        button.btn-alerta:hover {{
            background-color: #F57F17;
        }}
        button.btn-alerta:disabled {{
            background-color: #B0BEC5;
            color: #78909C;
        }}
        button.btn-close {{
            background-color: #C62828;
            grid-column: span 2;
        }}
        button.btn-close:hover {{
            background-color: #B71C1C;
        }}
        .caminho-copiar {{
            font-size: 11px;
            color: #78909C;
            word-break: break-all;
            margin-top: 15px;
            border-top: 1px solid #CFD8DC;
            padding-top: 10px;
        }}
    </style>
    <script>
        window.resizeTo(580, 640);
        window.moveTo((screen.width - 580)/2, (screen.height - 640)/2);

        var shell = new ActiveXObject("WScript.Shell");
        var PROJETO_ROOT = "{esc(ROOT_DIR)}";

        function abrirArquivo(caminho) {{
            if (!caminho) {{
                alert("Caminho nao disponivel.");
                return;
            }}
            try {{
                shell.Run('cmd.exe /c "' + PROJETO_ROOT + '\\\\ABRIR_ARQUIVO_EXTERNO.bat" "' + caminho + '"', 0, false);
            }} catch(e) {{
                alert("Erro ao abrir arquivo: " + e.message);
            }}
        }}

        function copiarTexto(texto) {{
            if (!texto) {{
                alert("Caminho nao disponivel para copiar.");
                return;
            }}
            try {{
                window.clipboardData.setData("Text", texto);
                alert("Caminho copiado com sucesso!");
            }} catch(e) {{
                alert("Nao foi possivel copiar: " + e.message);
            }}
        }}

        function fecharApp() {{
            window.close();
        }}
    </script>
</head>
<body>
    <h2>Painel do Cliente - {nome_cliente}</h2>
    
    <div class="dados-container">
        <table>
            <tr><td class="label">Cliente:</td><td><strong>{nome_cliente}</strong></td></tr>
            <tr><td class="label">Lote/Quadra:</td><td>{lote}</td></tr>
            <tr><td class="label">Total do Contrato:</td><td>{total_parcelas}</td></tr>
            <tr><td class="label">Parcelas Pagas:</td><td>{parcelas_pagas}</td></tr>
            <tr><td class="label">Parcelas Restantes:</td><td>{parcelas_restantes}</td></tr>
            <tr><td class="label">Percentual Pago:</td><td>{percentual_pago}</td></tr>
            <tr><td class="label">Valor Pago:</td><td>{valor_pago}</td></tr>
            <tr><td class="label">Valor Restante:</td><td>{valor_restante}</td></tr>
            <tr><td class="label">Arquivo Principal:</td><td>{nome_pdf_base}</td></tr>
        </table>
    </div>

    <div class="btn-container">
        <button onclick="abrirArquivo('{js_pdf}')" {"" if js_pdf else "disabled"}>Abrir PDF Corrigido</button>
        <button class="btn-secundario" onclick="abrirArquivo('{js_previa}')" {"" if js_previa else "disabled"}>Abrir Previa HTML</button>
        <button class="btn-secundario" onclick="abrirArquivo('{js_painel}')" {"" if js_painel else "disabled"}>Abrir Painel HTML</button>
        <button class="btn-secundario" onclick="abrirArquivo('{js_pasta}')" {"" if js_pasta else "disabled"}>Abrir Pasta Relatorios</button>
        <button class="btn-alerta" onclick="abrirArquivo('{js_conferencia}')" {"" if js_conferencia else "disabled"}>Abrir Conferencia .md</button>
        <button class="btn-alerta" onclick="copiarTexto('{js_pdf}')" {"" if js_pdf else "disabled"}>Copiar Caminho PDF</button>
        <button class="btn-close" onclick="fecharApp()">Fechar Painel</button>
    </div>

    <div class="caminho-copiar">
        <strong>Caminho do PDF Principal:</strong><br>
        {pdf_principal or "Nao localizado"}
    </div>
</body>
</html>
"""
    
    with open(caminho_hta, "w", encoding="utf-8") as f:
        f.write(conteudo_hta)
        
    print(f"Painel HTA criado em: {caminho_hta}")
    return caminho_hta

def abrir_painel_hta(caminho_hta):
    """Abre o arquivo HTA usando o Windows Explorer (Start-Process)."""
    try:
        os.startfile(caminho_hta)
        return True
    except Exception:
        try:
            import subprocess
            subprocess.run(["cmd", "/c", "start", "", str(caminho_hta)], shell=True)
            return True
        except Exception as e:
            print(f"[ERRO HTA] Nao foi possivel abrir o painel: {e}")
            return False

def exibir_resumo(dados):
    """Exibe o resumo financeiro estruturado de forma visual no console."""
    print("\n=======================================================")
    print("           RESUMO FINANCEIRO DO CLIENTE")
    print("=======================================================")
    print(f" Cliente:          {dados['cliente'] or 'Nao encontrado'}")
    print(f" Lote/Quadra:      {dados['lote'] or 'Nao encontrado'}")
    print(f" Total do Contrato:{dados['total_parcelas'] or 'Nao encontrado'}")
    print(f" Parcelas Pagas:   {dados['parcelas_pagas'] or 'Nao encontrado'}")
    print(f" Parcelas Restantes:{dados['parcelas_restantes'] or 'Nao encontrado'}")
    print(f" Percentual Pago:  {dados['percentual_pago'] or 'Nao encontrado'}")
    print(f" Valor Pago:       {dados['valor_pago'] or 'Nao encontrado'}")
    print(f" Valor Restante:   {dados['valor_restante'] or 'Nao encontrado'}")
    print(f" Origem dos Dados: {dados['arquivo_origem']}")
    print("=======================================================")

def main():
    # 1. Obter query de busca
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Digite o nome do cliente para buscar: ").strip()
        
    if not query:
        print("Busca cancelada. Nome vazio.")
        sys.exit(0)

    garantir_widepay_real_ou_parar(query)
        
    # Obter todos os clientes cadastrados a partir das pastas físicas
    clientes_cadastrados = obter_clientes_cadastrados()
    
    query_norm = normalizar_texto(query)
    clientes_filtrados = []
    for nome, pasta in clientes_cadastrados:
        if query_norm in normalizar_texto(nome) or query_norm in normalizar_texto(pasta):
            if (nome, pasta) not in clientes_filtrados:
                clientes_filtrados.append((nome, pasta))
                
    # Se encontrou na lista mapeada, usa
    if clientes_filtrados:
        if len(clientes_filtrados) > 1:
            print("\n=======================================================")
            print("        MULTIPLOS CLIENTES ENCONTRADOS")
            print("=======================================================")
            for idx, (nome, _) in enumerate(clientes_filtrados, 1):
                print(f"  {idx}. {nome}")
            print(f"  {len(clientes_filtrados)+1}. Cancelar")
            print("=======================================================")
            
            while True:
                try:
                    opc = int(input(f"Escolha um cliente (1-{len(clientes_filtrados)+1}): ").strip())
                    if opc == len(clientes_filtrados) + 1:
                        print("Busca cancelada.")
                        sys.exit(0)
                    if 1 <= opc <= len(clientes_filtrados):
                        selecionado = clientes_filtrados[opc-1]
                        query = selecionado[0]
                        query_pasta = selecionado[1]
                        break
                    else:
                        print("Opcao invalida.")
                except ValueError:
                    print("Por favor, digite um numero valido.")
        else:
            selecionado = clientes_filtrados[0]
            query = selecionado[0]
            query_pasta = selecionado[1]
    else:
        query_pasta = query
        
    print(f"\nBuscando arquivos para: '{query}'...")
    arquivos = scan_arquivos_cliente(query)
    if query_pasta != query:
        arquivos_pasta = scan_arquivos_cliente(query_pasta)
        caminhos_existentes = {a["caminho"] for a in arquivos}
        for a in arquivos_pasta:
            if a["caminho"] not in caminhos_existentes:
                arquivos.append(a)
                
    if not arquivos:
        print(f"Nenhum arquivo encontrado para a busca '{query}'.")
        sys.exit(0)
        
    # 2. Separar e filtrar arquivos
    arquivos_pdf = []
    arquivos_html = []
    arquivos_md = []
    outros = []
    
    pdf_corrigido = None
    html_previa = None
    html_painel = None
    
    for arq in arquivos:
        ext = arq["extensao"]
        nome = arq["nome"]
        
        if ext == ".pdf":
            arquivos_pdf.append(arq)
            # Prioriza a versao corrigida como PDF principal
            if "_corrigido" in nome.lower():
                pdf_corrigido = arq["caminho"]
            elif not pdf_corrigido:
                pdf_corrigido = arq["caminho"]
        elif ext == ".html":
            arquivos_html.append(arq)
            if "_previa" in nome.lower():
                html_previa = arq["caminho"]
            elif "abrir_relatorio" in nome.lower() or "painel" in nome.lower():
                html_painel = arq["caminho"]
        elif ext == ".md":
            arquivos_md.append(arq)
        else:
            outros.append(arq)
            
    # 3. Tentar carregar resumo a partir de MD de conferencia
    dados_resumo = None
    for arq in arquivos_md:
        if "conferencia" in arq["nome"].lower() or "calculos" in arq["nome"].lower() or "consolidado" in arq["nome"].lower():
            dados_resumo = parsear_dados_conferencia(arq["caminho"])
            if dados_resumo:
                break
                
    # Se nao conseguiu parsear dados do resumo (porque nao achou MD de conferencia), 
    # cria um dicionario basico para poder desenhar o HTA
    if not dados_resumo:
        dados_resumo = {
            "cliente": query.capitalize(),
            "lote": "Nao localizado",
            "total_parcelas": "Nao localizado",
            "parcelas_pagas": "Nao localizado",
            "parcelas_restantes": "Nao localizado",
            "percentual_pago": "Nao localizado",
            "valor_pago": "Nao localizado",
            "valor_restante": "Nao localizado",
            "arquivo_origem": "Nenhum markdown de conferencia encontrado"
        }
        
    # Se tiver resumo parseado, exibe no terminal
    exibir_resumo(dados_resumo)
    
    # 3.5. Gerar e abrir o painel HTA dinamicamente
    conferencia_md = None
    for arq in arquivos_md:
        if "conferencia" in arq["nome"].lower() or "calculos" in arq["nome"].lower() or "consolidado" in arq["nome"].lower():
            conferencia_md = arq["caminho"]
            break
    if not conferencia_md and arquivos_md:
        conferencia_md = arquivos_md[0]["caminho"]
        
    try:
        caminho_hta = gerar_painel_hta(dados_resumo, pdf_corrigido, html_previa, html_painel, conferencia_md)
        abriu_hta = abrir_painel_hta(caminho_hta)
        if abriu_hta:
            print("\nPainel HTA visual com botoes clicaveis aberto com sucesso.")
            print("Caso o painel feche ou voce queira interagir pelo terminal, use o menu abaixo (Plano B).")
    except Exception as e:
        print(f"\n[Aviso] Nao foi possivel abrir o painel visual HTA: {e}")
        
    # 4. Listar arquivos encontrados
    print("\nArquivos localizados no projeto:")
    indice = 1
    opcoes_arquivos = {}
    
    # Listar PDFs
    if arquivos_pdf:
        print("\n  [PDFs - Relatorios Finais]")
        for arq in arquivos_pdf:
            tipo = " (Corrigido/Principal)" if arq["caminho"] == pdf_corrigido else ""
            print(f"   {indice}. {arq['nome']}{tipo}")
            opcoes_arquivos[indice] = arq["caminho"]
            indice += 1
            
    # Listar HTMLs
    if arquivos_html:
        print("\n  [HTMLs - Previa/Painel]")
        for arq in arquivos_html:
            tipo = " (Previa)" if arq["caminho"] == html_previa else (" (Painel de Acesso)" if arq["caminho"] == html_painel else "")
            print(f"   {indice}. {arq['nome']}{tipo}")
            opcoes_arquivos[indice] = arq["caminho"]
            indice += 1
            
    # Listar MDs
    if arquivos_md:
        print("\n  [MDs - Auditoria/Conferencia]")
        for arq in arquivos_md:
            print(f"   {indice}. {arq['nome']}")
            opcoes_arquivos[indice] = arq["caminho"]
            indice += 1
            
    # Listar Outros
    if outros:
        print("\n  [Outros Arquivos]")
        for arq in outros:
            print(f"   {indice}. {arq['nome']} (Pasta: {arq['pasta_grupo']})")
            opcoes_arquivos[indice] = arq["caminho"]
            indice += 1
            
    # 5. Menu interativo de opcoes
    while True:
        print("\n=======================================================")
        print("               OPCOES DE ABERTURA RAPIDA")
        print("=======================================================")
        
        menu_opcoes = []
        if pdf_corrigido:
            menu_opcoes.append(("1", "Abrir PDF Principal/Corrigido", pdf_corrigido))
        else:
            menu_opcoes.append(("1", "Abrir PDF Principal (Nao encontrado)", None))
            
        if html_previa:
            menu_opcoes.append(("2", "Abrir Previa HTML", html_previa))
        else:
            menu_opcoes.append(("2", "Abrir Previa HTML (Nao encontrada)", None))
            
        if html_painel:
            menu_opcoes.append(("3", "Abrir Painel do Cliente (HTML)", html_painel))
        else:
            # Tenta ABRIR_RELATORIO_CAMILA.html na pasta de relatorios gerados como padrao
            html_padrao = PASTAS_PROJETO["Relatorios Gerados"] / "ABRIR_RELATORIO_CAMILA.html"
            if os.path.exists(html_padrao):
                menu_opcoes.append(("3", "Abrir Painel do Cliente (HTML)", html_padrao))
            else:
                menu_opcoes.append(("3", "Abrir Painel do Cliente (HTML) (Nao encontrado)", None))
                
        menu_opcoes.append(("4", "Abrir Pasta de Relatorios Gerados", PASTAS_PROJETO["Relatorios Gerados"]))
        
        # Imprime o menu
        for num, desc, path in menu_opcoes:
            status = "" if path else " [INDISPONIVEL]"
            print(f"  {num}. {desc}{status}")
            
        print("  5. Abrir um arquivo especifico da lista acima")
        print("  6. Sair")
        print("=======================================================")
        
        escolha = input("Escolha uma opcao (1-6): ").strip()
        
        if escolha == "1":
            path = menu_opcoes[0][2]
            if path:
                abrir_arquivo_externo(path)
            else:
                print("Arquivo indisponivel.")
        elif escolha == "2":
            path = menu_opcoes[1][2]
            if path:
                abrir_arquivo_externo(path)
            else:
                print("Arquivo indisponivel.")
        elif escolha == "3":
            path = menu_opcoes[2][2]
            if path:
                abrir_arquivo_externo(path)
            else:
                print("Arquivo indisponivel.")
        elif escolha == "4":
            abrir_arquivo_externo(menu_opcoes[3][2])
        elif escolha == "5":
            try:
                num_arq = int(input(f"Digite o numero do arquivo a abrir (1-{indice-1}): ").strip())
                if num_arq in opcoes_arquivos:
                    abrir_arquivo_externo(opcoes_arquivos[num_arq])
                else:
                    print("Numero de arquivo invalido.")
            except ValueError:
                print("Por favor, digite um numero valido.")
        elif escolha == "6":
            print("Saindo do sistema de busca.")
            break
        else:
            print("Opcao invalida. Escolha entre 1 e 6.")

if __name__ == "__main__":
    main()
