# -*- coding: utf-8 -*-
"""
Utilitário para abertura de arquivos no aplicativo padrão do Windows externamente.
"""
import os
import subprocess
import sys
from pathlib import Path

def abrir_externo(caminho):
    """
    Abre um arquivo ou pasta usando o aplicativo padrão associado no Windows.
    """
    abs_path = os.path.abspath(caminho)
    if not os.path.exists(abs_path):
        print(f"Erro: O caminho nao existe: {abs_path}")
        return False
        
    print(f"Abrindo externamente: {abs_path}")
    try:
        os.startfile(abs_path)
        return True
    except AttributeError:
        # Fallback para ambientes que não sejam Windows (ou caso ocorra erro)
        try:
            if sys.platform == "win32":
                subprocess.Popen(["cmd", "/c", "start", "", abs_path], shell=True)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", abs_path])
            else:
                subprocess.Popen(["xdg-open", abs_path])
            return True
        except Exception as e:
            print(f"Falha ao abrir arquivo: {e}")
            return False
    except Exception as e:
        print(f"Erro ao abrir arquivo via startfile: {e}")
        return False

def abrir_via_bat(caminho_relativo):
    """
    Chama o atalho/lançador universal do projeto (ABRIR_ARQUIVO_EXTERNO.bat)
    """
    projeto_root = Path(__file__).resolve().parent.parent.parent
    bat_path = projeto_root / "ABRIR_ARQUIVO_EXTERNO.bat"
    
    if not bat_path.exists():
        print(f"Erro: Bat lancador nao encontrado em {bat_path}")
        return False
        
    try:
        subprocess.Popen([str(bat_path), caminho_relativo], shell=True)
        return True
    except Exception as e:
        print(f"Erro ao chamar bat lancador: {e}")
        return False
