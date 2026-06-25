# -*- coding: utf-8 -*-
"""Entrada independente da aplicacao WideAPP_EXTRA."""

import argparse
import importlib
import subprocess
import sys
from datetime import datetime
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent
VENV_PYTHON = APP_DIR / ".venv" / "Scripts" / "python.exe"
EXECUTOR = APP_DIR / "executar_auditoria.py"
LOG_DIR = APP_DIR / "logs"
PRECHECK_DIR = ROOT_DIR / "00_SISTEMA_PRECHECK"
REQUIRED_MODULES = [
    "pandas",
    "openpyxl",
    "websockets",
    "bs4",
    "lxml",
    "playwright",
]


class WideApp:
    def __init__(self):
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = LOG_DIR / f"wideapp_extra_{stamp}.log"

    def log(self, message):
        message = str(message)
        line = f"[{datetime.now().isoformat(timespec='seconds')}] {message}"
        try:
            print(message)
        except UnicodeEncodeError:
            safe_message = message.encode("ascii", errors="replace").decode("ascii")
            print(safe_message)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def header(self):
        print("=" * 72)
        print(" WideAPP_EXTRA - Auditoria e Relatorios WidePay")
        print("=" * 72)
        print(f"Projeto: {ROOT_DIR}")
        print(f"Log: {self.log_path}")
        print()

    def validar_ambiente(self, exigir_widepay=False, exigir_executor=True):
        """Valida o ambiente de execução.

        exigir_widepay  — verifica Chrome/CDP/login WidePay.
        exigir_executor — verifica presença do executar_auditoria.py.
                          Deve ser False ao abrir apenas a interface gráfica,
                          pois o executor só é necessário para auditoria real.
        """
        self.log("VALIDACAO: iniciada")
        falhas = []

        exe_path = Path(sys.executable).resolve()
        expected_path = VENV_PYTHON.resolve()
        if exe_path.parent != expected_path.parent or exe_path.name.lower() not in ("python.exe", "pythonw.exe"):
            falhas.append(f"Python incorreto: {sys.executable}. Use {VENV_PYTHON}.")
        else:
            self.log(f"OK: Python do .venv em uso: {sys.executable}")

        if not VENV_PYTHON.exists():
            falhas.append(f"Python do .venv nao encontrado: {VENV_PYTHON}")

        if exigir_executor:
            if not EXECUTOR.exists():
                falhas.append(f"Executor principal nao encontrado: {EXECUTOR}")
        else:
            if EXECUTOR.exists():
                self.log(f"OK: executor disponivel: {EXECUTOR}")
            else:
                self.log(f"AVISO: executor ausente (nao necessario para interface): {EXECUTOR}")

        for module_name in REQUIRED_MODULES:
            try:
                importlib.import_module(module_name)
                self.log(f"OK: dependencia importada: {module_name}")
            except Exception as exc:
                falhas.append(f"Dependencia ausente ou invalida: {module_name} ({exc})")

        # Precheck de regras é opcional em modo portátil:
        # se o diretório não existir, apenas avisa sem bloquear.
        if PRECHECK_DIR.exists():
            try:
                sys.path.insert(0, str(PRECHECK_DIR))
                from precheck_regras import executar_precheck
                executar_precheck("WideAPP_EXTRA/main.py")
                self.log("OK: precheck de regras persistentes executado")
            except Exception as exc:
                falhas.append(f"Precheck falhou: {exc}")
        else:
            self.log("AVISO: 00_SISTEMA_PRECHECK nao encontrado — modo portavel, precheck ignorado")

        if exigir_widepay:
            try:
                sys.path.insert(0, str(APP_DIR))
                from app.login_navegador import garantir_navegador_conectado, obter_abas, validar_sessao_widepay

                ws_url = garantir_navegador_conectado()
                sessao = validar_sessao_widepay(ws_url)
                abas = obter_abas()
                urls_widepay = [
                    aba.get("url", "")
                    for aba in abas
                    if aba.get("type") == "page" and "widepay.com" in aba.get("url", "")
                ]
                if not ws_url or not urls_widepay:
                    falhas.append("WidePay nao foi localizado em aba CDP ativa.")
                elif not sessao.get("valida"):
                    falhas.append(
                        f"LOGIN_WIDEPAY_INVALIDO: {sessao.get('url')} | login={sessao.get('login')} | erro={sessao.get('erro')}"
                    )
                else:
                    self.log(f"OK: WidePay acessivel via CDP: {urls_widepay[0]}")
            except Exception as exc:
                falhas.append(f"Chrome/CDP/WidePay indisponivel: {exc}")

        if falhas:
            self.log("VALIDACAO: falhou")
            for falha in falhas:
                self.log(f"ERRO: {falha}")
            return False

        self.log("VALIDACAO: aprovada")
        return True

    def executar_auditoria(self, args):
        if not self.validar_ambiente(exigir_widepay=True):
            self.log("EXECUCAO: cancelada por falha de ambiente")
            return 1

        cmd = [str(VENV_PYTHON), str(EXECUTOR), *args]
        self.log("EXECUCAO: " + " ".join(cmd))

        proc = subprocess.Popen(
            cmd,
            cwd=str(ROOT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        with open(self.log_path, "a", encoding="utf-8") as log_file:
            for line in proc.stdout or []:
                print(line, end="")
                log_file.write(line)

        return_code = proc.wait()
        self.log(f"EXECUCAO: finalizada com codigo {return_code}")
        return return_code

    def menu(self):
        while True:
            self.header()
            print("1. Consultar cliente especifico")
            print("2. Consultar cliente + lote")
            print("3. Consultar por letra inicial")
            print("4. Consultar intervalo de letras")
            print("5. Gerar relatorio consolidado")
            print("6. Apenas validar ambiente")
            print("0. Sair")
            print()
            opcao = self._ler_input("Escolha uma opcao: ").strip().strip('"').strip("'")

            if opcao == "0":
                self.log("MENU: usuario saiu")
                return 0
            if opcao == "1":
                cliente = self._perguntar_obrigatorio("Nome do cliente")
                if cliente:
                    return self.executar_auditoria(["--cliente", cliente])
            elif opcao == "2":
                cliente = self._perguntar_obrigatorio("Nome do cliente")
                lote = self._perguntar_obrigatorio("Lote")
                if cliente and lote:
                    return self.executar_auditoria(["--cliente", cliente, "--lote", lote])
            elif opcao == "3":
                letra = self._perguntar_obrigatorio("Letra inicial")
                if letra:
                    return self.executar_auditoria(["--letra", letra[:1]])
            elif opcao == "4":
                letra_ini = self._perguntar_obrigatorio("Letra inicial")
                letra_fim = self._perguntar_obrigatorio("Letra final")
                if letra_ini and letra_fim:
                    return self.executar_auditoria(
                        ["--letra", letra_ini[:1], "--letra-fim", letra_fim[:1]]
                    )
            elif opcao == "5":
                args = self._menu_consolidado()
                if args:
                    return self.executar_auditoria(args)
            elif opcao == "6":
                ok = self.validar_ambiente(exigir_widepay=True)
                self._aguardar_enter("\nPressione Enter para voltar ao menu...")
                if not ok:
                    return 1
            else:
                print("Opcao invalida.")
                if not self._aguardar_enter("\nPressione Enter para tentar novamente..."):
                    return 1

    def abrir_interface_visual(self):
        from app.interface import abrir_interface

        # Para abrir a interface gráfica, não exigimos executor de auditoria
        # nem Chrome/CDP — esses só são necessários para auditoria real.
        # O precheck é ignorado em modo portátil (quando 00_SISTEMA_PRECHECK não existe).
        if not self.validar_ambiente(exigir_widepay=False, exigir_executor=False):
            self.log("INTERFACE: validacao basica falhou")
            return 1
        self.log("INTERFACE: abrindo interface visual")
        abrir_interface()
        return 0

    def atualizar_clientes(self, validar_widepay=True):
        from app.indexador_clientes import indexar_clientes

        result = indexar_clientes(validar_widepay=validar_widepay, log_callback=self.log)
        self.log(f"INDEXACAO: {len(result['registros'])} cliente/lote")
        self.log(f"INDEXACAO_LOG: {result['log']}")
        return 0

    def pesquisar_clientes(self, termo):
        from app.indexador_clientes import carregar_cache
        from app.pesquisa_clientes import filtrar

        resultados = filtrar(carregar_cache(), termo)
        self.log(f"PESQUISA: {len(resultados)} resultado(s) para {termo!r}")
        for item in resultados[:30]:
            print(f"{item.get('cliente')} | Lote {item.get('lote')} | {item.get('status')} | {item.get('contrato')}")
        return 0

    def smoke_test_interface(self):
        from app.interface import smoke_test

        qtd = smoke_test()
        self.log(f"SMOKE_INTERFACE: ok; cache atual com {qtd} registro(s)")
        return 0

    def teste_pipeline(self, termo):
        from app.indexador_clientes import carregar_cache
        from app.pesquisa_clientes import filtrar
        from app.pipeline_runner import executar_lote
        from app.login_navegador import garantir_navegador_conectado, validar_sessao_widepay

        ws_url = garantir_navegador_conectado()
        sessao = validar_sessao_widepay(ws_url)
        if not sessao.get("valida"):
            self.log(f"LOGIN_WIDEPAY_INVALIDO: {sessao.get('url')} | login={sessao.get('login')} | erro={sessao.get('erro')}")
            return 1

        registros = [r for r in filtrar(carregar_cache(), termo) if r.get("contrato") == "Encontrado"]
        if not registros:
            self.log(f"ERRO: nenhum registro com contrato confirmado para {termo!r}")
            return 1
        registro = registros[0]
        self.log(f"TESTE_PIPELINE: {registro.get('cliente')} lote {registro.get('lote')}")
        resultado = executar_lote([registro], grupo="TESTE_PIPELINE", log_callback=self.log)
        self.log(f"TESTE_PIPELINE: resultados={len(resultado['resultados'])} drive={len(resultado['drive'])}")
        for item in resultado["drive"]:
            self.log(f"DRIVE: {item.get('arquivo')} {item.get('status')} {item.get('link')}")
        return 0

    def _menu_consolidado(self):
        print()
        print("Escopo do consolidado:")
        print("1. Todos os clientes cadastrados")
        print("2. Letra inicial")
        print("3. Intervalo de letras")
        escolha = self._ler_input("Escolha o escopo: ").strip().strip('"').strip("'")
        if escolha == "1":
            return ["--todos", "--consolidado"]
        if escolha == "2":
            letra = self._perguntar_obrigatorio("Letra inicial")
            return ["--letra", letra[:1], "--consolidado"] if letra else None
        if escolha == "3":
            letra_ini = self._perguntar_obrigatorio("Letra inicial")
            letra_fim = self._perguntar_obrigatorio("Letra final")
            if letra_ini and letra_fim:
                return ["--letra", letra_ini[:1], "--letra-fim", letra_fim[:1], "--consolidado"]
        print("Escopo invalido.")
        return None

    def _perguntar_obrigatorio(self, rotulo):
        valor = self._ler_input(f"{rotulo}: ").strip().strip('"').strip("'")
        if not valor:
            print(f"{rotulo} e obrigatorio.")
            return None
        return valor

    def _ler_input(self, prompt):
        try:
            return input(prompt)
        except EOFError:
            self.log("MENU: entrada encerrada")
            return "0"

    def _aguardar_enter(self, prompt):
        try:
            input(prompt)
            return True
        except EOFError:
            self.log("MENU: entrada encerrada durante pausa")
            return False


def parse_args():
    parser = argparse.ArgumentParser(description="WideAPP_EXTRA - aplicacao independente")
    parser.add_argument("--validar-ambiente", action="store_true", help="valida .venv, dependencias, precheck e WidePay")
    parser.add_argument("--executar", nargs=argparse.REMAINDER, help="encaminha argumentos para executar_auditoria.py")
    parser.add_argument("--terminal", action="store_true", help="abre o menu antigo em terminal")
    parser.add_argument("--atualizar-clientes", action="store_true", help="atualiza cache local de clientes/contratos")
    parser.add_argument("--sem-widepay", action="store_true", help="na atualizacao, nao valida WidePay/CDP")
    parser.add_argument("--pesquisar", help="pesquisa no cache local de clientes")
    parser.add_argument("--smoke-test-interface", action="store_true", help="testa criacao da interface sem manter janela aberta")
    parser.add_argument("--teste-pipeline", help="executa pipeline real para o primeiro cliente/lote encontrado no cache")
    return parser.parse_args()


def main():
    app = WideApp()
    args = parse_args()
    if args.validar_ambiente:
        return 0 if app.validar_ambiente(exigir_widepay=True) else 1
    if args.executar is not None:
        if not args.executar:
            app.log("ERRO: use --executar seguido dos argumentos de auditoria")
            return 1
        return app.executar_auditoria(args.executar)
    if args.atualizar_clientes:
        return app.atualizar_clientes(validar_widepay=not args.sem_widepay)
    if args.pesquisar:
        return app.pesquisar_clientes(args.pesquisar)
    if args.smoke_test_interface:
        return app.smoke_test_interface()
    if args.teste_pipeline:
        return app.teste_pipeline(args.teste_pipeline)
    if args.terminal:
        return app.menu()
    return app.abrir_interface_visual()


if __name__ == "__main__":
    raise SystemExit(main())
