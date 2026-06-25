# WideAPP_EXTRA - Instruções de Teste Local

Este pacote contém a versão de teste da ferramenta **WideAPP_EXTRA**, desenvolvida para auditoria financeira de recebíveis, cruzamento com contratos de loteamentos e automação de extração do WidePay.

## 🚀 Como Iniciar o Programa

1. Certifique-se de extrair todo o conteúdo deste arquivo ZIP para uma pasta local.
2. Dê dois cliques no arquivo **`INICIAR_TESTE_WIDEAPP_EXTRA.bat`** (localizado na raiz do pacote extraído).
3. O script irá:
   - Verificar se há um ambiente virtual Python configurado (`.venv`). Se não houver, ele fornecerá instruções para criar e instalar as dependências necessárias.
   - Executar a validação do precheck de integridade das regras do projeto.
   - Iniciar a interface visual baseada em **Tkinter**.

---

## 🖥️ O que já funciona de forma imediata (sem login no WidePay)
Você pode testar as seguintes funcionalidades utilizando apenas a base de dados local:
* **Filtros e Busca Dinâmica:** Digite nomes no campo de busca ou filtre por status ("Ativo", "Pendente validação WidePay", "Com divergência", etc.).
* **Seleção Múltipla:** Marque múltiplos clientes na listagem para processamento em lote.
* **Abertura de Pastas e Relatórios Existentes:** Acesso rápido à pasta de saídas e visualização de documentos gerados anteriormente.

---

## 🔒 O que depende de Login Ativo no WidePay
Para executar o fluxo completo de auditoria financeira (que extrai dados direto da plataforma WidePay):
1. O seu navegador Chrome dedicado deve estar aberto no modo de depuração na porta `9333`.
2. Você deve estar logado no painel de recebimentos do WidePay.
3. Se esses requisitos forem atendidos, a interface visual conseguirá automatizar a extração das tabelas paginadas de boletos de cada cliente selecionado, calculando parcelas pagas, amortizações e gerando os arquivos XLSX, PDF e HTML consolidados.

---

## 📁 Estrutura do Pacote
* `INICIAR_TESTE_WIDEAPP_EXTRA.bat` - Atalho para iniciar a aplicação a partir da raiz do pacote.
* `WideAPP_EXTRA/main.py` - Ponto de entrada principal do código Python.
* `WideAPP_EXTRA/INICIAR_WIDEAPP_EXTRA.bat` - Script de execução secundário.
* `WideAPP_EXTRA/COMO_USAR.md` - Guia detalhado de uso do sistema.
* `WideAPP_EXTRA/requirements.txt` - Lista de dependências Python necessárias para rodar o app.
* `WideAPP_EXTRA/app/` - Módulos internos da aplicação (interface, extratores, geradores de relatórios).
