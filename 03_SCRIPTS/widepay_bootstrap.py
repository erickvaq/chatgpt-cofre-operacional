import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def garantir_widepay_real_ou_parar(escopo):
    """Abre o fluxo real do WidePay antes de qualquer consulta local."""
    print("Abrindo Opera dedicado e carregando WidePay real...")
    script_consulta = ROOT_DIR / "03_SCRIPTS" / "consultar_widepay_cdp.py"
    cmd = [sys.executable, str(script_consulta), "--cliente", escopo]
    resultado = subprocess.run(cmd, capture_output=True, text=True)

    if resultado.stdout:
        print(resultado.stdout, end="" if resultado.stdout.endswith("\n") else "\n")
    if resultado.stderr:
        print(resultado.stderr, end="" if resultado.stderr.endswith("\n") else "\n")

    if resultado.returncode != 0:
        print("WIDEPAY REAL NAO ABERTO - EXECUCAO BLOQUEADA. Nao vou consultar arquivos locais antes de abrir o WidePay.")
        sys.exit(resultado.returncode if resultado.returncode else 1)

    return True
