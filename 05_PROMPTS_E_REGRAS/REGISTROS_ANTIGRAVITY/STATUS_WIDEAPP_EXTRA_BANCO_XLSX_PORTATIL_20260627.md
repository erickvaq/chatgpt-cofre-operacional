# Status Registry — Portable Visual Database (XLSX) and Dynamic Path Resolution

**Date**: 2026-06-27  
**Author**: Antigravity AI  

---

## 1. Objetivo da Mudança
Implementar uma arquitetura portátil de gerenciamento de caminhos e geração do banco de dados visual XLSX (`BANCO_DADOS_WIDEAPP_EXTRA.xlsx`) na raiz da aplicação, permitindo que a aplicação seja movida, copiada ou executada de qualquer pasta sem depender de caminhos absolutos fixos como `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\`.

## 2. Problema do Caminho Fixo
A codificação de caminhos absolutos em arquivos de configuração ou módulos de processamento quebra a portabilidade do aplicativo em outros computadores ou pastas, impossibilitando execuções em modo autônomo/portátil (.exe compilado) ou em diretórios clonados alternativos.

## 3. Solução por Raiz Dinâmica
Criação do módulo `WideAPP_EXTRA/app/paths.py` com detecção dinâmica e inteligente baseada no estado de execução (`sys.frozen` para binários empacotados e análise recursiva de pais para script Python). Isso permite isolar a infraestrutura de caminhos em uma única camada.

## 4. Funções Criadas para Resolver Caminhos
As seguintes funções foram disponibilizadas no módulo [paths.py](file:///c:/Users/Windows User/Desktop/chatgpt projetos/Relatorio_WidePay_Lotes/WideAPP_EXTRA/app/paths.py):
* `get_app_root()`: Identifica dinamicamente a pasta raiz da aplicação.
* `get_visual_database_path()`: Resolve o caminho para `BANCO_DADOS_WIDEAPP_EXTRA.xlsx` diretamente na raiz detectada.
* `get_backups_dir()`: Resolve e garante a existência da pasta `backups/`.
* `get_internal_data_dir()`: Resolve e garante a pasta técnica de cache interno `WideAPP_EXTRA/data/`.

## 5. Caminhos Detectados
* **Cenário A — App Isolado**:
  * Caminho: `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\`
  * Raiz Detectada: `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO`
* **Cenário B — Projeto Principal**:
  * Caminho: `C:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes\`
  * Raiz Detectada: `C:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes`

## 6. Caminho do Banco XLSX Gerado
* `C:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes\BANCO_DADOS_WIDEAPP_EXTRA.xlsx`

## 7. Botão Criado
* **Botão**: `Visualizar banco de dados` adicionado à barra de ferramentas de arquivos abertos (`tb_open`).
* **Comportamento**: Verifica a existência de `BANCO_DADOS_WIDEAPP_EXTRA.xlsx`. Se não existir, exibe um aviso informando que o banco de dados deve ser gerado primeiro. Se existir, abre-o utilizando o visualizador padrão do sistema (`os.startfile`).

## 8. Testes Executados e Resultados
* **Execução Direta por CLI**: Gerou o arquivo `BANCO_DADOS_WIDEAPP_EXTRA.xlsx` na raiz do projeto principal com sucesso.
* **Teste de Backup Consecutivo**: Uma segunda execução gerou o backup timestamped em `backups/BANCO_DADOS_WIDEAPP_EXTRA_ANTES_YYYYMMDD_HHMMSS.xlsx` antes de sobrescrever o arquivo original.
* **Smoke Test de Compilação**: Todos os scripts modificados (`paths.py`, `config.py`, `indexador_clientes.py`, `interface.py`) foram compilados sem erros.

## 9. Pendências
* Nenhuma pendência de path resolution detectada.

## 10. Commit GitHub
* commit: `git commit -m "feat: adicionar banco xlsx portatil na raiz do app"`
