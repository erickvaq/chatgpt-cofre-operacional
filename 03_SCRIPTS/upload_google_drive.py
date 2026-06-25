import os
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
RCLONE_EXE = ROOT_DIR / "ferramentas" / "rclone" / "rclone.exe"

def rodar_comando(cmd):
    """Roda comando rclone e retorna a saída."""
    try:
        resultado = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        return True, resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, f"ERRO: {e.stderr.strip()}"
    except Exception as e:
        return False, f"FALHA: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("Uso: python upload_google_drive.py CAMINHO_DO_ARQUIVO.xlsx")
        sys.exit(1)
        
    arquivo_local = Path(sys.argv[1])
    if not arquivo_local.is_absolute():
        arquivo_local = ROOT_DIR / arquivo_local
        
    if not arquivo_local.exists():
        print(f"ERRO: Arquivo nao encontrado ({arquivo_local})")
        sys.exit(1)

    if not RCLONE_EXE.exists():
        print("ERRO: rclone nao encontrado. Instale via script de configuracao.")
        sys.exit(1)

    nome_arquivo = arquivo_local.name
    # Usando o caminho padrao do drive especificado na regra
    caminho_drive = f"gdrive:Relatorio_WidePay_Lotes/02_RELATORIOS_GERADOS"
    
    print(f"Iniciando upload de: {nome_arquivo}")
    print(f"Destino Drive: {caminho_drive}")
    
    # Executar Upload
    cmd_upload = [str(RCLONE_EXE), "copy", str(arquivo_local), caminho_drive]
    sucesso, msg = rodar_comando(cmd_upload)
    
    if not sucesso:
        print(f"FALHA NO UPLOAD: {msg}")
        sys.exit(1)
        
    print("[OK] Arquivo copiado com sucesso para o Drive.")
    
    # Executar Geração do Link
    # gdrive precisa de 'link' para extrair a url pública
    cmd_link = [str(RCLONE_EXE), "link", f"{caminho_drive}/{nome_arquivo}"]
    sucesso_link, msg_link = rodar_comando(cmd_link)
    
    if sucesso_link and msg_link.startswith("http"):
        print("\n--- RESUMO DA ENTREGA ---")
        print("[REGRA 13] O arquivo completo foi entregue sem bloqueio de sensibilidade.")
        print(f"LINK_DRIVE: {msg_link}")
        print(f"ARQUIVO: {nome_arquivo}")
        print("-------------------------")
        sys.exit(0)
    else:
        print(f"[AVISO] Upload concluido, mas falha ao gerar link publico. Detalhe: {msg_link}")
        sys.exit(1)

if __name__ == "__main__":
    main()
