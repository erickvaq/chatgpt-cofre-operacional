import os
import sys
import re
import datetime
import unicodedata

# Caminhos padrão do projeto (absolutos)
PROJETO_ROOT = r"C:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes"
REGRAS_PADRAO = os.path.join(PROJETO_ROOT, "05_PROMPTS_E_REGRAS", "REGRAS_PERSISTENTES_DO_PROJETO.md")
LOG_PADRAO = os.path.join(PROJETO_ROOT, "07_DADOS_TEMPORARIOS", "LOG_LEITURA_REGRAS.md")

def normalizar_texto(texto):
    """Remove acentos e converte para minusculas para busca insensivel."""
    if not texto:
        return ""
    texto_nfd = unicodedata.normalize('NFD', texto)
    sem_acentos = "".join(c for c in texto_nfd if unicodedata.category(c) != 'Mn')
    return sem_acentos.lower()

def buscar_arquivo_regras():
    """Tenta localizar o arquivo de regras de forma robusta."""
    if os.path.exists(REGRAS_PADRAO):
        return REGRAS_PADRAO
    
    relativo_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "05_PROMPTS_E_REGRAS", "REGRAS_PERSISTENTES_DO_PROJETO.md"))
    if os.path.exists(relativo_script):
        return relativo_script
        
    relativo_cwd = os.path.abspath(os.path.join("05_PROMPTS_E_REGRAS", "REGRAS_PERSISTENTES_DO_PROJETO.md"))
    if os.path.exists(relativo_cwd):
        return relativo_cwd
        
    atual = os.getcwd()
    for _ in range(4):
        caminho_teste = os.path.join(atual, "05_PROMPTS_E_REGRAS", "REGRAS_PERSISTENTES_DO_PROJETO.md")
        if os.path.exists(caminho_teste):
            return caminho_teste
        pai = os.path.dirname(atual)
        if pai == atual:
            break
        atual = pai
        
    return None

def buscar_caminho_log():
    """Retorna o caminho onde o log deve ser gravado."""
    if os.path.exists(os.path.dirname(LOG_PADRAO)):
        return LOG_PADRAO
    
    relativo_log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "07_DADOS_TEMPORARIOS"))
    if not os.path.exists(relativo_log_dir):
        try:
            os.makedirs(relativo_log_dir, exist_ok=True)
        except Exception:
            pass
            
    if os.path.exists(relativo_log_dir):
        return os.path.join(relativo_log_dir, "LOG_LEITURA_REGRAS.md")
        
    return "LOG_LEITURA_REGRAS.md"

def registrar_log(script_chamador, resultado, qtd_regras, detalhes):
    """Grava ou atualiza o log de precheck em formato Markdown."""
    caminho_log = buscar_caminho_log()
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    precisa_cabecalho = not os.path.exists(caminho_log) or os.path.getsize(caminho_log) == 0
    nova_linha = f"| {data_hora} | {script_chamador} | {resultado} | {qtd_regras} | {detalhes} |\n"
    
    try:
        if precisa_cabecalho:
            with open(caminho_log, "w", encoding="utf-8") as f:
                f.write("# Log de Leitura Automatica de Regras Persistentes\n\n")
                f.write("Este log registra todas as verificacoes automaticas de regras persistentes feitas antes da execucao de scripts e rotinas importantes no projeto.\n\n")
                f.write("| Data e Hora | Script Chamador | Resultado | Regras Encontradas | Detalhes |\n")
                f.write("|---|---|---|---|---|\n")
                f.write(nova_linha)
        else:
            with open(caminho_log, "a", encoding="utf-8") as f:
                f.write(nova_linha)
    except Exception as e:
        print(f"[AVISO LOG] Nao foi possivel escrever no log: {e}")

def executar_precheck(script_chamador="Script Desconhecido"):
    """Executa a validacao completa e dinamica das regras persistentes."""
    caminho_regras = buscar_arquivo_regras()
    
    if not caminho_regras:
        erro_msg = "ERRO CRITICO: Arquivo de regras persistentes nao foi encontrado!"
        print(erro_msg)
        registrar_log(script_chamador, "ERRO", 0, "Arquivo REGRAS_PERSISTENTES_DO_PROJETO.md nao localizado.")
        sys.exit(1)
        
    try:
        with open(caminho_regras, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        erro_msg = f"ERRO CRITICO: Nao foi possivel ler o arquivo de regras: {e}"
        print(erro_msg)
        registrar_log(script_chamador, "ERRO", 0, f"Falha na leitura do arquivo: {e}")
        sys.exit(1)
        
    # 1. Encontrar e parsear numeracao de regras dinamicamente
    padrao_regras_str = re.findall(r"##\s*REGRA\s+(\d+)", conteudo, re.IGNORECASE)
    numeros_regras = [int(n) for n in padrao_regras_str]
    
    if not numeros_regras:
        print("ERRO: Nenhuma regra numerada (## REGRA X) foi encontrada no arquivo.")
        registrar_log(script_chamador, "ERRO", 0, "Nenhuma regra numerada localizada no markdown.")
        sys.exit(1)
        
    qtd_regras = len(set(numeros_regras))
    
    # 2. Validar duplicidade de regras
    duplicadas = sorted(list(set([num for num in numeros_regras if numeros_regras.count(num) > 1])))
    if duplicadas:
        erro_msg = f"ERRO: Detectada duplicidade na numeracao das regras: {duplicadas}"
        print(erro_msg)
        registrar_log(script_chamador, "ERRO", qtd_regras, f"Duplicidade nas regras: {duplicadas}")
        sys.exit(1)
        
    # 3. Validar saltos de numeracao
    ordenados = sorted(list(set(numeros_regras)))
    esperados = list(range(1, len(ordenados) + 1))
    if ordenados != esperados:
        saltos = [x for x in esperados if x not in ordenados]
        erro_msg = f"ERRO: Detectado salto na numeracao das regras. Regras faltantes na sequencia: {saltos}"
        print(erro_msg)
        registrar_log(script_chamador, "ERRO", qtd_regras, f"Saltos na numeracao: faltam {saltos}")
        sys.exit(1)
        
    # 4. Validar presenca e conteudo basico de regras criticas
    # O mapeamento contem (numero_regra, palavra_chave_titulo, termo_obrigatorio_conteudo)
    regras_criticas = {
        1: ("visualizacao de pdf", "start-process"),
        5: ("prints do usuario sao fonte prioritaria de validacao", "fonte prioritaria"),
        6: ("auditar antes de gerar pdf final", "07_dados_temporarios"),
        9: ("entrega pratica de arquivos", "abrir_relatorio_"),
        10: ("nunca sobrescrever arquivos finais sem autorizacao", "_corrigido"),
        11: ("registro historico e modelo de auditoria", "camila ferrolho"),
        12: ("checklist obrigatorio antes da entrega final", "checklist"),
        13: ("leitura automatica obrigatoria das regras", "precheck_regras.py"),
        14: ("comando simples para buscar cliente", "buscar_cliente.bat"),
        16: ("abertura externa obrigatoria e organizacao de arquivos finais", "lancador externo"),
        17: ("padronizacao de escrita do cabecalho", "loteamento agua viva"),
        18: ("skills operacionais do projeto", "widepay-plugin"),
        19: ("pasta de contratos externa somente leitura", "somente leitura"),
        20: ("tratamento de multiplos resultados na busca de clientes", "buscar_cliente.bat"),
        21: ("consulta integrada de carnes e cobrancas/boletos", "proibido gerar conferencia final ou pdf considerando apenas carnes"),
        22: ("modo economico obrigatorio", "nao abrir navegador"),
        26: ("checagem de cobertura obrigatoria no widepay", "garantir que nenhum cliente ativo"),
        27: ("login widepay com autopreenchimento seguro do navegador", "quando o widepay abrir na tela de login"),
        28: ("foco no resultado final: relatorios de todos os clientes com eficiencia", "o objetivo principal dos fluxos do widepay nao e narrar cada etapa"),
        29: ("nao acessar configuracoes/contatos do widepay para relatorios", "dados bancarios"),
        30: ("resumo operacional leve e controle de execucao", "resumo_execucao_atual.md")
    }
    
    conteudo_norm = normalizar_texto(conteudo)
    erros_criticos = []
    
    for num, (titulo_term, desc_term) in regras_criticas.items():
        if num not in ordenados:
            erros_criticos.append(f"REGRA {num} (obrigatoria) nao foi encontrada")
            continue
            
        # Confere se os termos correspondentes estao no conteudo geral do markdown
        titulo_term_norm = normalizar_texto(titulo_term)
        desc_term_norm = normalizar_texto(desc_term)
        
        if titulo_term_norm not in conteudo_norm:
            erros_criticos.append(f"REGRA {num} parece estar com o titulo modificado ou incorreto (esperado termo: '{titulo_term}')")
        elif desc_term_norm not in conteudo_norm:
            erros_criticos.append(f"REGRA {num} esta incompleta ou alterada (esperado termo: '{desc_term}')")
            
    # Validar a REGRA PRIORITARIA separadamente
    if "regra prioritaria" not in conteudo_norm:
        erros_criticos.append("REGRA PRIORITARIA (fonte principal de instrucoes) nao foi encontrada")
    elif "prioridade operacional" not in conteudo_norm:
        erros_criticos.append("REGRA PRIORITARIA esta incompleta (esperado termo: 'prioridade operacional')")
        
    # Validar a REGRA CRITICA de Fluxo Generico e Modelo Metodologico separadamente
    if "fluxo generico de clientes e modelo metodologico" not in conteudo_norm:
        erros_criticos.append("REGRA CRITICA — Fluxo Genérico de Clientes e Modelo Metodológico nao foi encontrada")
    elif "recalcular do zero" not in conteudo_norm:
        erros_criticos.append("REGRA CRITICA esta incompleta (esperado termo: 'recalcular do zero')")

    # Validar a nova REGRA CRÍTICA do WidePay automático via Opera GX, WMI e CDP
    if "widepay automatica via opera gx, wmi e cdp" not in conteudo_norm and "widepay automatico via opera gx, wmi e cdp" not in conteudo_norm:
        erros_criticos.append("REGRA CRÍTICA — WidePay automático via Opera GX, WMI e CDP localhost:9444 nao foi encontrada")
    elif "opera profile_9444" not in conteudo_norm and "operaprofile_9444" not in conteudo_norm:
        erros_criticos.append("REGRA CRÍTICA — WidePay automático via Opera GX, WMI e CDP localhost:9444 esta incompleta")

    # Validar a existencia dos arquivos criticos
    caminho_procedimento = os.path.join(PROJETO_ROOT, "05_PROMPTS_E_REGRAS", "PROCEDIMENTO_WIDEPAY_OPERA_CDP_WMI.md")
    if not os.path.exists(caminho_procedimento):
        erros_criticos.append("Arquivo PROCEDIMENTO_WIDEPAY_OPERA_CDP_WMI.md nao foi encontrado")
        
    caminho_config = os.path.join(PROJETO_ROOT, "00_SISTEMA_PRECHECK", "config_widepay_cdp.py")
    if not os.path.exists(caminho_config):
        erros_criticos.append("Arquivo config_widepay_cdp.py nao foi encontrado")
    else:
        try:
            with open(caminho_config, "r", encoding="utf-8") as fc:
                cfg_content = fc.read()
                cfg_norm = normalizar_texto(cfg_content)
                if "localhost" not in cfg_norm:
                    erros_criticos.append("config_widepay_cdp.py deve conter o endpoint 'localhost'")
                if "9444" not in cfg_content:
                    erros_criticos.append("config_widepay_cdp.py deve conter a porta '9444'")
        except Exception as ec:
            erros_criticos.append(f"Erro ao ler config_widepay_cdp.py: {ec}")


            
    if erros_criticos:
        msg_erros = "; ".join(erros_criticos)
        print(f"ERRO: Falha na validacao de regras criticas: {msg_erros}")
        registrar_log(script_chamador, "ERRO", qtd_regras, f"Falha critica de conteudo: {msg_erros}")
        sys.exit(1)
        
    # Tudo certo!
    msg_sucesso = f"REGRAS PERSISTENTES CARREGADAS COM SUCESSO - {qtd_regras} regras encontradas."
    print(msg_sucesso)
    registrar_log(script_chamador, "SUCESSO", qtd_regras, f"Todas as regras ({qtd_regras}) carregadas e validadas com sucesso.")
    return True

if __name__ == "__main__":
    executar_precheck("precheck_regras.py (Standalone)")
