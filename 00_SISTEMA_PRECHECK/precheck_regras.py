import os
import sys
import re
import datetime
import unicodedata

PROJETO_ROOT = r"C:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes"
REGRAS_PADRAO = os.path.join(PROJETO_ROOT, "05_PROMPTS_E_REGRAS", "REGRAS_PERSISTENTES_DO_PROJETO.md")
LOG_PADRAO = os.path.join(PROJETO_ROOT, "07_DADOS_TEMPORARIOS", "LOG_LEITURA_REGRAS.md")


def normalizar_texto(texto):
    if not texto:
        return ""
    texto_nfd = unicodedata.normalize("NFD", texto)
    sem_acentos = "".join(c for c in texto_nfd if unicodedata.category(c) != "Mn")
    return sem_acentos.lower()


def buscar_arquivo_regras():
    if os.path.exists(REGRAS_PADRAO):
        return REGRAS_PADRAO

    alternativas = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "05_PROMPTS_E_REGRAS", "REGRAS_PERSISTENTES_DO_PROJETO.md")),
        os.path.abspath(os.path.join("05_PROMPTS_E_REGRAS", "REGRAS_PERSISTENTES_DO_PROJETO.md")),
    ]
    for caminho in alternativas:
        if os.path.exists(caminho):
            return caminho

    atual = os.getcwd()
    for _ in range(4):
        candidato = os.path.join(atual, "05_PROMPTS_E_REGRAS", "REGRAS_PERSISTENTES_DO_PROJETO.md")
        if os.path.exists(candidato):
            return candidato
        pai = os.path.dirname(atual)
        if pai == atual:
            break
        atual = pai
    return None


def buscar_caminho_log():
    if os.path.exists(os.path.dirname(LOG_PADRAO)):
        return LOG_PADRAO

    relativo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "07_DADOS_TEMPORARIOS"))
    if not os.path.exists(relativo):
        try:
            os.makedirs(relativo, exist_ok=True)
        except Exception:
            pass
    if os.path.exists(relativo):
        return os.path.join(relativo, "LOG_LEITURA_REGRAS.md")
    return "LOG_LEITURA_REGRAS.md"


def registrar_log(script_chamador, resultado, qtd_regras, detalhes):
    caminho_log = buscar_caminho_log()
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"| {data_hora} | {script_chamador} | {resultado} | {qtd_regras} | {detalhes} |\n"

    try:
        precisa_cabecalho = not os.path.exists(caminho_log) or os.path.getsize(caminho_log) == 0
        if precisa_cabecalho:
            with open(caminho_log, "w", encoding="utf-8") as f:
                f.write("# Log de Leitura Automatica de Regras Persistentes\n\n")
                f.write("Este log registra as verificacoes automaticas de regras persistentes antes da execucao de rotinas importantes no projeto.\n\n")
                f.write("| Data e Hora | Script Chamador | Resultado | Regras Encontradas | Detalhes |\n")
                f.write("|---|---|---|---|---|\n")
                f.write(linha)
        else:
            with open(caminho_log, "a", encoding="utf-8") as f:
                f.write(linha)
    except Exception as e:
        print(f"[AVISO LOG] Nao foi possivel escrever no log: {e}")


def executar_precheck(script_chamador="Script Desconhecido"):
    caminho_regras = buscar_arquivo_regras()
    if not caminho_regras:
        print("ERRO CRITICO: Arquivo de regras persistentes nao foi encontrado!")
        registrar_log(script_chamador, "ERRO", 0, "Arquivo REGRAS_PERSISTENTES_DO_PROJETO.md nao localizado.")
        sys.exit(1)

    try:
        with open(caminho_regras, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        print(f"ERRO CRITICO: Nao foi possivel ler o arquivo de regras: {e}")
        registrar_log(script_chamador, "ERRO", 0, f"Falha na leitura do arquivo: {e}")
        sys.exit(1)

    numeros = [int(n) for n in re.findall(r"##\s*REGRA\s+(\d+)", conteudo, re.IGNORECASE)]
    if not numeros:
        print("ERRO: Nenhuma regra numerada (## REGRA X) foi encontrada no arquivo.")
        registrar_log(script_chamador, "ERRO", 0, "Nenhuma regra numerada localizada no markdown.")
        sys.exit(1)

    unicos = sorted(set(numeros))
    if len(unicos) != len(numeros):
        duplicadas = sorted({n for n in numeros if numeros.count(n) > 1})
        print(f"ERRO: Detectada duplicidade na numeracao das regras: {duplicadas}")
        registrar_log(script_chamador, "ERRO", len(unicos), f"Duplicidade nas regras: {duplicadas}")
        sys.exit(1)

    esperados = list(range(1, 10))
    if unicos != esperados:
        print(f"ERRO: Numeracao das regras inconsistente. Esperado {esperados}, encontrado {unicos}.")
        registrar_log(script_chamador, "ERRO", len(unicos), f"Numeracao inconsistente: {unicos}")
        sys.exit(1)

    conteudo_norm = normalizar_texto(conteudo)
    regras_criticas = {
        1: ("widepay, contratos e conflito de fontes", "widepay e a fonte principal financeira"),
        2: ("seguranca widepay e login", "nao acessar"),
        3: ("fluxo por cliente", "recalcular tudo do zero"),
        4: ("relatorios em lote e consolidado", "jsons locais recentes"),
        5: ("entrega visual e arquivos finais", "html"),
        6: ("github e rastreabilidade", "nunca inventar link github"),
        7: ("painel operacional", "painel operacional widepay"),
        8: ("economia operacional, skills e precheck", "precheck_regras.py"),
        9: ("painel operacional publico sempre limpo e verificado", "github normal"),
    }

    erros = []
    for num, (titulo, termo) in regras_criticas.items():
        titulo_norm = normalizar_texto(titulo)
        termo_norm = normalizar_texto(termo)
        regra_label = f"## regra {num}"
        if regra_label not in conteudo_norm:
            erros.append(f"REGRA {num} (obrigatoria) nao foi encontrada")
            continue
        if titulo_norm not in conteudo_norm:
            erros.append(f"REGRA {num} parece estar com o titulo modificado ou incorreto (esperado termo: '{titulo}')")
        elif termo_norm not in conteudo_norm:
            erros.append(f"REGRA {num} esta incompleta ou alterada (esperado termo: '{termo}')")

    if "regra prioritaria" not in conteudo_norm:
        erros.append("REGRA PRIORITARIA (fonte principal de instrucoes) nao foi encontrada")
    elif "ordem de prioridade" not in conteudo_norm:
        erros.append("REGRA PRIORITARIA esta incompleta (esperado termo: 'ordem de prioridade')")

    if "abrir widepay real antes de qualquer consulta" not in conteudo_norm:
        erros.append("REGRA OBRIGATORIA de abertura real do WidePay nao foi encontrada")
    elif "widepay real nao foi aberto" not in conteudo_norm:
        erros.append("REGRA OBRIGATORIA esta incompleta (esperado termo: 'widepay real nao foi aberto')")

    if "painel operacional publico sempre limpo e verificado" not in conteudo_norm:
        erros.append("REGRA 9 (painel operacional publico sempre limpo e verificado) nao foi encontrada")
    elif "painel publico oficial" not in conteudo_norm:
        erros.append("REGRA 9 esta incompleta (esperado termo: 'painel publico oficial')")

    if "parcelas restantes somente pelo contrato" not in conteudo_norm:
        erros.append("Regra de parcelas restantes somente pelo contrato nao foi encontrada")
    elif "nunca usar parcelas geradas no widepay como substituto do total do contrato" not in conteudo_norm:
        erros.append("Regra de parcelas restantes esta incompleta: WidePay nao pode substituir o total do contrato")
    if "contar no total pago do terreno/lote todos os boletos pagos ligados ao cliente" not in conteudo_norm:
        erros.append("Regra do total pago do terreno/lote nao foi encontrada")
    if "aceitar aliases e erros de digitacao comuns do nome do cliente" not in conteudo_norm:
        erros.append("Regra de aliases/erro de digitacao do cliente nao foi encontrada")
    if "sempre consultar e listar no relatorio do cliente todos os carnes e todas as cobrancas/boletos pagos ou em aberto localizados no widepay" not in conteudo_norm:
        erros.append("Regra de listagem completa de carnes e cobrancas/boletos no relatorio nao foi encontrada")
    if "aproveitar o autopreenchimento e tentar login automatico antes de pedir intervencao manual" not in conteudo_norm:
        erros.append("Regra de login automatico com senha salva no navegador nao foi encontrada")
    if "interpretacao individual de pagamentos widepay" not in conteudo_norm:
        erros.append("Regra de interpretacao individual de pagamentos WidePay nao foi encontrada")
    if "pagamentos recebidos interpretados" not in conteudo_norm:
        erros.append("Tabela obrigatoria de pagamentos recebidos interpretados nao foi encontrada nas regras")
    if "nunca usar o caso edmilson" not in conteudo_norm:
        erros.append("Bloqueio contra regra fixa baseada no caso Edmilson nao foi encontrado")

    caminho_procedimento = os.path.join(PROJETO_ROOT, "05_PROMPTS_E_REGRAS", "PROCEDIMENTO_WIDEPAY_OPERA_CDP_WMI.md")
    if not os.path.exists(caminho_procedimento):
        erros.append("Arquivo PROCEDIMENTO_WIDEPAY_OPERA_CDP_WMI.md nao foi encontrado")

    caminho_config = os.path.join(PROJETO_ROOT, "00_SISTEMA_PRECHECK", "config_widepay_cdp.py")
    if not os.path.exists(caminho_config):
        erros.append("Arquivo config_widepay_cdp.py nao foi encontrado")
    else:
        try:
            with open(caminho_config, "r", encoding="utf-8") as fc:
                cfg_content = fc.read()
                cfg_norm = normalizar_texto(cfg_content)
                if "localhost" not in cfg_norm:
                    erros.append("config_widepay_cdp.py deve conter o endpoint 'localhost'")
                if "9444" not in cfg_content:
                    erros.append("config_widepay_cdp.py deve conter a porta '9444'")
        except Exception as ec:
            erros.append(f"Erro ao ler config_widepay_cdp.py: {ec}")

    skills_a_validar = [
        (
            os.path.join(PROJETO_ROOT, ".agents", "skills", "widepay-core-operacional", "SKILL.md"),
            "SKILL.md da widepay-core-operacional",
            [
                ("regra zero", "Regra Zero nao encontrada na skill"),
                ("regra universal", "A skill nao reforca a Regra Universal"),
                ("carregar o widepay real", "A skill nao obriga a abertura real do WidePay"),
                ("widepay primeiro", "A skill nao reforca WidePay primeiro"),
                ("contratos locais depois", "A skill nao reforca contratos locais depois"),
                ("lista local preliminar", "A skill nao marca a lista local como preliminar quando falta WidePay"),
                ("fluxo local-first bloqueado", "A skill nao bloqueia o fluxo local-first"),
                ("widepay real nao foi aberto", "A skill nao bloqueia quando o WidePay real nao abre"),
                ("parcelas restantes somente pelo contrato", "A skill nao bloqueia parcelas restantes fora do contrato"),
                ("alias e erros de digitacao comuns", "A skill nao aceita aliases comuns do cliente"),
                ("interpretacao individual de pagamentos widepay", "A skill nao reforca interpretacao individual de pagamentos WidePay"),
                ("pagamentos recebidos interpretados", "A skill nao exige a tabela de pagamentos interpretados"),
            ],
        ),
        (
            os.path.join(PROJETO_ROOT, ".agents", "skills", "widepay-relatorio-pdf", "SKILL.md"),
            "SKILL.md da widepay-relatorio-pdf",
            [
                ("regra universal", "A skill de PDF nao reforca a Regra Universal"),
                ("widepay vem primeiro", "A skill de PDF nao reforca WidePay primeiro"),
                ("conferencia em markdown", "A skill de PDF nao reforca a conferencia em Markdown"),
                ("planilha consolidada", "A skill de PDF nao reforca a planilha consolidada"),
                ("par de entrega", "A skill de PDF nao reforca o par de entrega"),
                ("parcelas restantes pelo contrato", "A skill de PDF nao reforca parcelas restantes pelo contrato"),
                ("total pago do terreno/lote", "A skill de PDF nao reforca o total pago do terreno/lote"),
                ("pagamentos interpretados", "A skill de PDF nao exige pagamentos interpretados"),
                ("percentuais separados", "A skill de PDF nao separa percentual financeiro e percentual de parcelas"),
            ],
        ),
    ]

    for caminho_skill, rotulo_skill, requisitos_skill in skills_a_validar:
        if not os.path.exists(caminho_skill):
            erros.append(f"Arquivo {rotulo_skill} nao foi encontrado")
            continue
        try:
            with open(caminho_skill, "r", encoding="utf-8") as fs:
                skill_norm = normalizar_texto(fs.read())
            for termo, msg in requisitos_skill:
                if termo not in skill_norm:
                    erros.append(msg)
        except Exception as es:
            erros.append(f"Erro ao ler {rotulo_skill}: {es}")

    scripts_a_validar = [
        (
            os.path.join(PROJETO_ROOT, "03_SCRIPTS", "gerar_relatorio_cliente.py"),
            "gerar_relatorio_cliente.py",
            [
                ("validar_interpretacao_pagamentos", "Gerador final nao valida interpretacao individual de pagamentos"),
                ("interpretar_pagamentos_recebidos", "Gerador final nao interpreta pagamentos recebidos"),
                ("pagamentos_interpretados", "Gerador final nao carrega pagamentos interpretados"),
            ],
        ),
        (
            os.path.join(PROJETO_ROOT, "03_SCRIPTS", "gerar_conferencia_cliente.py"),
            "gerar_conferencia_cliente.py",
            [
                ("pagamentos recebidos interpretados", "Conferencia Markdown nao gera a tabela de pagamentos interpretados"),
                ("interpretar_cobrancas_recebidas", "Conferencia Markdown nao interpreta recebimentos"),
            ],
        ),
        (
            os.path.join(PROJETO_ROOT, "03_SCRIPTS", "relatorios_pdf", "gerar_pdf_final.py"),
            "gerar_pdf_final.py",
            [("pagamentos recebidos interpretados", "PDF nao contem tabela de pagamentos interpretados")],
        ),
        (
            os.path.join(PROJETO_ROOT, "03_SCRIPTS", "relatorios_pdf", "gerar_html_previa.py"),
            "gerar_html_previa.py",
            [("pagamentos recebidos interpretados", "HTML nao contem tabela de pagamentos interpretados")],
        ),
    ]
    for caminho_script, rotulo_script, requisitos_script in scripts_a_validar:
        if not os.path.exists(caminho_script):
            erros.append(f"Arquivo {rotulo_script} nao foi encontrado")
            continue
        try:
            with open(caminho_script, "r", encoding="utf-8") as fs:
                script_norm = normalizar_texto(fs.read())
            for termo, msg in requisitos_script:
                if termo not in script_norm:
                    erros.append(msg)
        except Exception as ev:
            erros.append(f"Erro ao ler {rotulo_script}: {ev}")

    regra_zero_pos = conteudo_norm.find("## regra zero")
    regra_prioritaria_pos = conteudo_norm.find("## regra prioritaria")
    regra_1_pos = conteudo_norm.find("## regra 1")
    if regra_zero_pos == -1:
        erros.append("REGRA ZERO (widepay primeiro, contratos depois) nao foi encontrada")
    else:
        if regra_prioritaria_pos != -1 and regra_zero_pos > regra_prioritaria_pos:
            erros.append("REGRA ZERO precisa aparecer antes da REGRA PRIORITARIA")
        if regra_1_pos != -1 and regra_zero_pos > regra_1_pos:
            erros.append("REGRA ZERO precisa aparecer antes da REGRA 1")
        if "widepay primeiro" not in conteudo_norm:
            erros.append("REGRA ZERO esta incompleta (esperado termo: 'widepay primeiro')")
        if "contratos e arquivos locais depois" not in conteudo_norm:
            erros.append("REGRA ZERO esta incompleta (esperado termo: 'contratos e arquivos locais depois')")
        if "lista local preliminar" not in conteudo_norm:
            erros.append("REGRA ZERO esta incompleta (esperado termo: 'lista local preliminar')")
        if "fluxo local-first bloqueado" not in conteudo_norm:
            erros.append("REGRA ZERO esta incompleta (esperado termo: 'fluxo local-first bloqueado')")

    regra_universal_pos = conteudo_norm.find("## regra universal")
    if regra_universal_pos == -1:
        erros.append("REGRA UNIVERSAL (fluxo padrao universal para relatorios WidePay) nao foi encontrada")
    else:
        requisitos_regra_universal = [
            ("cliente especifico", "REGRA UNIVERSAL esta incompleta (esperado termo: 'cliente especifico')"),
            ("intervalo de letras", "REGRA UNIVERSAL esta incompleta (esperado termo: 'intervalo de letras')"),
            ("grupo de clientes", "REGRA UNIVERSAL esta incompleta (esperado termo: 'grupo de clientes')"),
            ("widepay primeiro", "REGRA UNIVERSAL esta incompleta (esperado termo: 'widepay primeiro')"),
            ("lista local preliminar", "REGRA UNIVERSAL esta incompleta (esperado termo: 'lista local preliminar')"),
            ("planilha consolidada", "REGRA UNIVERSAL esta incompleta (esperado termo: 'planilha consolidada')"),
            ("conferencia em markdown", "REGRA UNIVERSAL esta incompleta (esperado termo: 'conferencia em markdown')"),
            ("painel publico", "REGRA UNIVERSAL esta incompleta (esperado termo: 'painel publico')"),
        ]
        for termo, msg in requisitos_regra_universal:
            if termo not in conteudo_norm:
                erros.append(msg)

    if erros:
        msg_erros = "; ".join(erros)
        print(f"ERRO: Falha na validacao de regras criticas: {msg_erros}")
        registrar_log(script_chamador, "ERRO", len(unicos), f"Falha critica de conteudo: {msg_erros}")
        sys.exit(1)

    msg_sucesso = f"REGRAS PERSISTENTES CARREGADAS COM SUCESSO - {len(unicos)} regras encontradas."
    print(msg_sucesso)
    registrar_log(script_chamador, "SUCESSO", len(unicos), f"Todas as regras ({len(unicos)}) carregadas e validadas com sucesso.")
    return True


if __name__ == "__main__":
    executar_precheck("precheck_regras.py (Standalone)")
