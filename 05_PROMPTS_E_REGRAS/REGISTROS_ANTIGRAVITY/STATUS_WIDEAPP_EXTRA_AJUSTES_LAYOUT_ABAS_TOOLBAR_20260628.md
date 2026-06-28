# Status Registry — Ajustes de Layout, Abas, Toolbar e Auditoria na WideAPP_EXTRA

**Date**: 2026-06-28  
**Author**: Antigravity AI  

---

## 1. O que foi Removido
* **Navegação Lateral Duplicada**: O frame lateral `sidebar_panel` e seus métodos associados (`_montar_sidebar`, `_selecionar_sidebar`, `_atualizar_sidebar_ativo`) foram 100% removidos. A aba de conteúdos Notebook ocupa agora toda a largura útil.
* **Barra de Rolagem Horizontal**: Removidos os objetos `scroll_x` e o bind `xscrollcommand` da Treeview. As colunas foram configuradas para redimensionamento e esticamento automático (`stretch=True`), cabendo confortavelmente em qualquer resolução a partir de 1280px.
* **Código Legado Duplicado**: Removida a primeira definição morta do método `_montar` (linhas 289-429) que causava riscos de regressão.

## 2. O que foi Mantido
* **Caixa "Andamento da Atualização"**: Mantida no cabeçalho superior direito com a barra de progresso verde neon (`#22C55E`), etapa atual, porcentagem e logs em tempo real intocados.
* **Abas do Notebook**: Mantidas na mesma posição (Clientes, Banco de dados, Logs, Resumo / status, Auditoria).
* **Botão Azul**: Mantido e visível (`Visualizar banco de dados` com estilo `Info.Toolbar.TButton` azul).
* **Ordenação por Clique**: Mantida e preservada nos cabeçalhos.

## 3. O que foi Compactado
* **Toolbar Principal**: Consolidada de 4 linhas para exatamente **2 linhas de botões**:
  * **Linha 1**: `Atualizar clientes` (Verde), `Visualizar banco de dados` (Azul), `Atualizar WidePay`, `Parar captura`, `Abrir XLSX`, `Abrir pasta local`, `Abrir Drive`.
  * **Linha 2**: `Gerar relatorio selecionados`, `Gerar clientes ativos`, `Abrir HTML`, `Abrir PDF` | `Planilhas recentes` (Combobox de largura adaptada).
* **Padding e Fonte**: Reduzido o padding vertical de `10` para `4` e o tamanho de fonte de `10` para `9pt` em todos os estilos de botão (`Toolbar.TButton`, `Primary.Toolbar.TButton`, etc.).

## 4. Como ficou a Tabela
* **Coluna Observações Oculta**: A coluna `observacoes` continua ativa no cache do sistema, nos relatórios gerados e nos backups XLSX, mas está **oculta por padrão** na tabela principal por meio da configuração da propriedade `displaycolumns` da Treeview.
* **Rolagem Vertical**: Preservada por completo por meio de `scroll_y`.

## 5. Como funciona o Arrastar Colunas (Drag & Drop)
* **Prevenção de Conflitos**: Foram adicionados binds de baixo nível (`<ButtonPress-1>`, `<B1-Motion>` e `<ButtonRelease-1>`) e a opção `command` nativa dos cabeçalhos foi removida.
* **Detecção de Movimento**:
  * Se o usuário der um clique simples (ou segurar sem mover mais de 12 pixels), ao soltar, o sistema realiza a **Ordenação por Clique** da coluna correspondente.
  * Se o usuário arrastar o cabeçalho além de 12 pixels de distância, o sistema reordena a coluna visualmente no release e salva a nova preferência de exibição no arquivo `data/colunas_config.json`. Ao reabrir o app, a ordem personalizada é recarregada automaticamente.

## 6. Como ficou a aba Auditoria
* A aba deixou de ser um texto fixo explicativo e passou a ser um **Painel de Conformidade Financeira Funcional** que compila dinamicamente:
  * Total de reconciliações com sucesso.
  * Divergências financeiras e matemáticas ativas encontradas pelo validador.
  * Clientes sem contrato físico confirmado na pasta local.
  * Clientes com falhas críticas ou pendências cadastrais no WidePay.
* O painel é atualizado em tempo real na inicialização e após qualquer filtragem ou atualização de dados.

## 7. Testes Executados
* **Smoke Test do Workspace**: `python main.py --smoke-test-interface` passou com sucesso (`SMOKE_INTERFACE: ok; cache atual com 92 registro(s)`).
* **Smoke Test no Ambiente Isolado**: passou com sucesso (`SMOKE_INTERFACE: ok; cache atual com 87 registro(s)`).

## 8. Histórico de Commits GitHub
* **Ajuste Fino de Layout, Abas, Drag e Auditoria**:
  * Hash: `b2ccaae807490ab1cdcb96c4295ef85675e4e0b0`
  * Link: [b2ccaae](https://github.com/erickvaq/chatgpt-cofre-operacional/commit/b2ccaae807490ab1cdcb96c4295ef85675e4e0b0)

## 9. Pendências
* Nenhuma pendência restante.
