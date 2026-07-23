# 06 - Implantação Oficial e Atalhos

## Pastas do Projeto
* **Pasta do Código de Desenvolvimento**: `c:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes\WideAPP_EXTRA`
* **Pasta Oficial da Instalação do Aplicativo**: `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_V20_ISOLADO\WideAPP_EXTRA`

## Arquivos Sincronizados na Última Etapa (Implantados na Instalação Oficial)
1. `WideAPP_EXTRA/app/widepay_boletos_cache.py` (Lógica de equivalência Emmanuel/Rodrigo e rateio sem centavos)
2. `WideAPP_EXTRA/app/saneamento_clientes.py` (Mapeamento de lote canônico por cliente)
3. `WideAPP_EXTRA/app/indexador_clientes.py` (Normalização e gravação de cache)
4. `WideAPP_EXTRA/data/clientes_indexados.json` (Base indexada contendo G2 e G18 para Emmanuel e F19 e G1/G19 para Rodrigo)
5. `BANCO_DADOS_WIDEAPP_EXTRA.xlsx` (Banco visual consolidado)

## Arquivos Restaurados (Não Modificados)
* Foram preservados integralmente sem cópias desnecessárias todos os demais arquivos de interface (`interface.py`), scripts de execução, `.venv`, logs, backups e configurações do usuário.

## Atalho 1: Área de Trabalho (Desktop)
* **Caminho do Atalho**: `C:\Users\Windows User\Desktop\WideAPP AGUA VIVA.lnk`
* **Target (Executável)**: `C:\Windows\System32\wscript.exe`
* **Arguments**: `"C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_V20_ISOLADO\WideAPP_EXTRA\Abrir_WideAPP_EXTRA.vbs"`
* **WorkingDirectory**: `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_V20_ISOLADO\WideAPP_EXTRA`

## Atalho 2: Menu Iniciar do Windows
* **Caminho do Atalho**: `C:\Users\Windows User\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\WideAPP AGUA VIVA.lnk`
* **Target (Executável)**: `C:\Windows\System32\wscript.exe`
* **Arguments**: `"C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_V20_ISOLADO\WideAPP_EXTRA\Abrir_WideAPP_EXTRA.vbs"`
* **WorkingDirectory**: `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_V20_ISOLADO\WideAPP_EXTRA`

## Unicidade de Instalação
* **Ambos os atalhos apontam exclusivamente para a mesma instalação oficial do programa**:
  `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_V20_ISOLADO\WideAPP_EXTRA`
