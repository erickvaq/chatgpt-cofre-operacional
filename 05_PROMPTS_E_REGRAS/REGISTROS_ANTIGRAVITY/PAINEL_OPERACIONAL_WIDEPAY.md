# PAINEL OPERACIONAL WIDEPAY — Relatorio_WidePay_Lotes

## Informações Gerais
* **Data da Última Atualização:** 24/06/2026
* **Último Comando Executado:** "Correção de dados, commit e regras do painel operacional"
* **Estado Atual do Processo:** Parcialmente completo. Regras consolidadas, precheck validando 31 regras, e checagem de cobertura A a E em andamento (pendente de validação/busca individual).
* **Último Commit:** cb8c5c8 (Correções de tabelas e segurança do painel)
* **Branch Atual:** main
* **Link GitHub deste Painel:** [PAINEL_OPERACIONAL_WIDEPAY.md](https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md)

> [!IMPORTANT]
> **Segurança e Privacidade (GitHub Público):**
> * Este painel **não contém quaisquer valores financeiros** (valores monetários, parcelas pagas, juros, saldos devedores). Todos os detalhes financeiros sensíveis são mantidos de forma estritamente local em arquivos não sincronizados (`02_RELATORIOS_GERADOS` e `07_DADOS_TEMPORARIOS`).
> * Os nomes completos e lotes estão temporariamente expostos de forma simplificada para fins de mapeamento operacional de cobertura (iniciais A a E), estando a decisão final sobre o mascaramento (ex: iniciais dos nomes ou ocultação parcial de lotes) pendente de decisão/autorização final do usuário.

---

## RESUMO DA EXTRAÇÃO WIDEPAY
* **Data da Extração:** 22/06/2026
* **Áreas Consultadas:** Carnês (`https://www.widepay.com/conta/recebimentos/carnes`) e Cobranças/Boletos (`https://www.widepay.com/conta/recebimentos`)
* **Clientes Encontrados (WidePay):** Adailton Gomes De Jesus, Altamir Do Carmo Cerqueira, Ana Carolina Nery Da S.Borgens, Ana Cleide Dos Santos Dias, Camila De Oliveira Ferrolho, Carla Rocha Lemos, Edmilson Silva Dos Santos, Edna Francisca Dos Santos, Edna Frqncisca Dos Santos, Eliel Hora Santana.
* **Clientes Não Encontrados (WidePay ou dependendo de checagem ativa):** Adalberto Oliveira, Alexandre, Antonio Dias Mota (Filha), Belmiro Santos Pires, Camila Carvalho Sazhyn, Carlos Alberto, Alex Santos de Azevedo, Edmilson, Emanuel, Heron Souza Dias, Daniela Ramos, Debora Cristina Rei, Edelzuito (Desio), Edneia Souza, Emmanuel Felix, Evaniu Dias Macêdo.
* **Clientes com Carnê:** Adailton Gomes De Jesus, Altamir Do Carmo Cerqueira, Ana Carolina Nery Da S.Borgens, Camila De Oliveira Ferrolho, Carla Rocha Lemos, Edmilson Silva Dos Santos, Edna Francisca Dos Santos, Edna Frqncisca Dos Santos, Eliel Hora Santana.
* **Clientes com Cobrança/Boleto:** Ana Cleide Dos Santos Dias.
* **Clientes com Dados Parciais:** Ana Carolina Nery Da S.Borgens (dados coletados, dependendo de validação), Adailton Gomes De Jesus (carnês a partir de determinada parcela).
* **Clientes que precisam de conferência individual:** 21 clientes classificados como Pendente.
* **Erros ou limitações da extração:** Limitações de login ou CDP quando o navegador exige ação manual.
* **Status de Cobertura:** Incompleta (varredura inicial A a E concluída, aguardando validações individuais).

---

## Controle de Clientes (Iniciais A a E)

### 1. Clientes Encontrados no WidePay (Com correspondência financeira ativa ou histórica no sistema)

| Cliente | Inicial | Lote | Fonte WidePay | Status WidePay | Relatório | Arquivo local | GitHub | Pendência |
|---|---|---|---|---|---|---|---|---|
| Adailton Gomes De Jesus | A | e22a | carnê | Pendente | Não gerado | Sim | Não enviado — arquivo sensível | Pendente de conferência |
| Altamir Do Carmo Cerqueira | A | G4 | carnê | Pendente | Não gerado | Sim | Não enviado — arquivo sensível | Pendente de conferência |
| Ana Carolina Nery Da S.Borgens | A | E7 | carnê | Pendente | Relatório gerado | Sim | Não enviado — arquivo sensível | Pendente de conferência |
| Ana Cleide Dos Santos Dias | A | E5 | cobrança | Acessado | Relatório gerado | Sim | Não enviado — arquivo sensível | Nenhuma |
| Camila De Oliveira Ferrolho | C | G13 | carnê | Pendente | Não gerado | Sim | Não enviado — arquivo sensível | Pendente de conferência |
| Carla Rocha Lemos | C | Lt F 17 | carnê | Sem evidência financeira | Não gerado | Não | - | Sem evidência financeira ativa |
| Edmilson Silva Dos Santos | E | - | carnê | Sem evidência financeira | Não gerado | Não | - | Sem evidência financeira ativa |
| Edna Francisca Dos Santos | E | lt D6 | carnê | Sem evidência financeira | Não gerado | Não | - | Sem evidência financeira ativa |
| Edna Frqncisca Dos Santos | E | Lt D 06 | carnê | Sem evidência financeira | Não gerado | Não | - | Sem evidência financeira ativa |
| Eliel Hora Santana | E | Lt E 12 | carnê | Sem evidência financeira | Relatório gerado | Sim | Não enviado — arquivo sensível | Sem evidência financeira ativa |

### 2. Contratos Locais Usados Apenas como Apoio (Vinculados a clientes do WidePay)

| Cliente | Inicial | Lote/Quadra | Pasta/Diretório Local | GitHub | Observação |
|---|---|---|---|---|---|
| Adailton Gomes De Jesus | A | e22a (Q.E) | `Adailton Gomes de Jesus e22A Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível | Contrato usado para validar nome e lote |
| Altamir Do Carmo Cerqueira | A | G4 (Q.G) | `Contrato Altamir do carmo cerqueira G4 Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível | Contrato usado para validar nome e lote |
| Ana Carolina Nery Da S.Borgens | A | E7 (Q.E) | `Ana Carolina E7 Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível | Contrato usado para validar parcelas (43) |
| Ana Cleide Dos Santos Dias | A | E5 (Q.E) | `Ana Cleide E5 Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível | Contrato usado para validar pendência financeira |
| Camila De Oliveira Ferrolho | C | G13 (Q.G) | `Camila de Oliveira G13 Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível | Contrato usado para validar parcelas (78) |
| Eliel Hora Santana | E | Lt E 12 | `Contrato Eliel E12 Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível | Contrato local de apoio |

### 3. Pastas Locais Sem Correspondência Financeira no WidePay (Pendente de busca/validação individual)

| Cliente (Normalizado) | Inicial | Lote/Quadra Local | Status de Busca | Pasta/Diretório Local | GitHub |
|---|---|---|---|---|---|
| Adalberto Oliveira | A | A3 (Q.A) | Pendente | `Adalberto Oliveira A3 Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível |
| Alexandre | A | g14 (Q.G) | Pendente | `alexandre g14 Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível |
| Antonio Dias Mota | A | E15, E16, E17 (Q.E) | Pendente | `Antonio Dias Mota E15 E16 E17 Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível |
| Belmiro Santos Pires | B | F6 (Q.F) | Pendente | `Belmiro Santos Pires F6` | Não enviado — arquivo sensível |
| Camila Carvalho Sazhyn | C | D7 (Q.D) | Pendente | `Camila Carvalho Sazhyn D7 - Agua Viva -Leandro Meirelles` | Não enviado — arquivo sensível |
| Carlos Alberto | C | E14 (Q.E) | Pendente | `Carlos Alberto E14 Agua viva` | Não enviado — arquivo sensível |
| Alex Santos de Azevedo | C | B2, B3 (Q.B) | Pendente | `Contrato Alex Santos de Azevedo B2 B3 Agua Viva LÉO` | Não enviado — arquivo sensível |
| Edmilson | C | F05 (Q.F) | Pendente | `Contrato Edmilson F05 Agua Viva LÉO` | Não enviado — arquivo sensível |
| Emanuel | C | F1, F18 (Q.F) | Pendente | `Contrato Emanuel F1 F18 Agua Viva LÉO` | Não enviado — arquivo sensível |
| Heron Souza Dias | C | H5 (Q.H) | Pendente | `Contrato Heron Souza Dias H5 H6a Agua Viva LÉO` | Não enviado — arquivo sensível |
| Heron Souza Dias | C | B4, B5, B6 (Q.B) | Pendente | `Contrato Heron Souza Dias B4 B5 B6 Agua Viva LÉO` | Não enviado — arquivo sensível |
| Daniela Ramos | D | f7, F8 (Q.F) | Pendente | `Daniela Ramos f7 F8  Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível |
| Debora Cristina Rei | D | e22b (Q.E) | Pendente | `Debora Cristina Rei e22B Agua Viva Leandro Meirelles - Cópia` | Não enviado — arquivo sensível |
| Edelzuito (Desio) | E | A1 (Q.A) | Pendente | `Edelzuito (desio) A1 Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível |
| Edneia Souza | E | F16 (Q.F) | Pendente | `Edneia Souza F16 Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível |
| Emmanuel Felix | E | G2, G18 (Q.G) | Pendente | `Emmanuel Felix G2 G18 Agua Viva Leandro Meirelles` | Não enviado — arquivo sensível |
| Evaniu Dias Macêdo | E | F9, F10 (Q.E) | Pendente | `Evaniu Dias Macêdo E22a F9 F10` | Não enviado — arquivo sensível |

---

## PEDIDO DO USUÁRIO X ENTREGA

| Pedido do usuário | Entregue? | Arquivo/resultado | Status | Pendência |
| :--- | :--- | :--- | :--- | :--- |
| Relatórios de teste | Parcial | 3 relatórios de teste locais | Parcial | Gerados para 3 clientes (Ana Cleide, Ana Carolina, Eliel) |
| Relatórios completos A a E | Não | Nenhum | Pendente | Ainda não entregues |
| Cobertura A a E | Parcial | [CHECAGEM_COBERTURA_A_E.md](file:///c:/Users/Windows%20User/Desktop/chatgpt%20projetos/Relatorio_WidePay_Lotes/07_DADOS_TEMPORARIOS/CHECAGEM_COBERTURA_A_E.md) | Parcial | Pendente de correção/validação individual dos clientes pendentes |
| Painel operacional | Sim | [PAINEL_OPERACIONAL_WIDEPAY.md](https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md) | Pronto | Criado e funcionando com regras sanitizadas |
| Registrar regras de login e navegação segura | Sim | [REGRAS_PERSISTENTES_DO_PROJETO.md](https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md) (REGRAS 27 e 29) | Pronto | Nenhuma |

---

## Arquivos Locais Sensíveis (Não enviados ao GitHub)

| Arquivo | Cliente/Lote | Caminho local | Sensível | GitHub | Observação |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `PLANILHA_TESTE_VALIDACAO_A_E_20260622.xlsx` | Lotes A a E | `03_PLANILHAS/PLANILHA_TESTE_VALIDACAO_A_E_20260622.xlsx` | Sim | Não enviado — arquivo sensível | Planilha local de validação de teste |
| `RESUMO_FINANCEIRO_ANA_CLEIDE_DOS_SANTOS_DIAS_CORRIGIDO_V3_PREVIA.html` | Ana Cleide Dias (E5) | `02_RELATORIOS_GERADOS/RESUMO_FINANCEIRO_ANA_CLEIDE_DOS_SANTOS_DIAS_CORRIGIDO_V3_PREVIA.html` | Sim | Não enviado — arquivo sensível | Prévia HTML local |
| `RESUMO_FINANCEIRO_ANA_CAROLINA_NERY_DA_S_BORGENS_CORRIGIDO_V3_PREVIA.html` | Ana Carolina Borgens (E7) | `02_RELATORIOS_GERADOS/RESUMO_FINANCEIRO_ANA_CAROLINA_NERY_DA_S_BORGENS_CORRIGIDO_V3_PREVIA.html` | Sim | Não enviado — arquivo sensível | Prévia HTML local |
| `RESUMO_FINANCEIRO_ELIEL_HORA_SANTANA_CORRIGIDO_V3_PREVIA.html` | Eliel Santana (E12) | `02_RELATORIOS_GERADOS/RESUMO_FINANCEIRO_ELIEL_HORA_SANTANA_CORRIGIDO_V3_PREVIA.html` | Sim | Não enviado — arquivo sensível | Prévia HTML local |
| `CONFERENCIA_CALCULOS_ANA_CLEIDE_DOS_SANTOS_DIAS.md` | Ana Cleide Dias (E5) | `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_ANA_CLEIDE_DOS_SANTOS_DIAS.md` | Sim | Não enviado — arquivo sensível | Arquivo de conferência local |
| `CONFERENCIA_CALCULOS_ANA_CAROLINA_NERY_DA_S_BORGENS.md` | Ana Carolina Borgens (E7) | `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_ANA_CAROLINA_NERY_DA_S_BORGENS.md` | Sim | Não enviado — arquivo sensível | Arquivo de conferência local |
| `CONFERENCIA_CALCULOS_ELIEL_HORA_SANTANA.md` | Eliel Santana (E12) | `07_DADOS_TEMPORARIOS/CONFERENCIA_CALCULOS_ELIEL_HORA_SANTANA.md` | Sim | Não enviado — arquivo sensível | Arquivo de conferência local |

---

## Arquivos Enviados ao GitHub (Sem dados sensíveis)

| Arquivo | Tipo | Link GitHub | Commit | Data |
| :--- | :--- | :--- | :--- | :--- |
| `05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md` | Regras do Projeto | [Link](https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGRAS_PERSISTENTES_DO_PROJETO.md) | cb8c5c8 | 24/06/2026 |
| `05_PROMPTS_E_REGRAS/REGRA-BASE — RELATÓRIOS FINANCEIROS WIDEPAY — PROCESSO EFICIENTE E REPLICÁVEL.md` | Regra-Base | [Link](https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGRA-BASE%20%E2%80%94%20RELAT%C3%93RIOS%20FINANCEIROS%20WIDEPAY%20%E2%80%94%20PROCESSO%20EFICIENTE%20E%20REPLIC%C3%81VEL.md) | cb8c5c8 | 24/06/2026 |
| `00_SISTEMA_PRECHECK/precheck_regras.py` | Script de Validação | [Link](https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/00_SISTEMA_PRECHECK/precheck_regras.py) | cb8c5c8 | 24/06/2026 |
| `scratch/extrair_tudo_cobertura.py` | Script de Extração | [Link](https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/scratch/extrair_tudo_cobertura.py) | cb8c5c8 | 24/06/2026 |
| `07_DADOS_TEMPORARIOS/RESUMO_EXECUCAO_ATUAL.md` | Resumo de Execução | [Link](https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/07_DADOS_TEMPORARIOS/RESUMO_EXECUCAO_ATUAL.md) | cb8c5c8 | 24/06/2026 |
| `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md` | Painel Operacional | [Link](https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/PAINEL_OPERACIONAL_WIDEPAY.md) | cb8c5c8 | 24/06/2026 |
| `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/implementation_plan.md` | Plano de Ação | [Link](https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/implementation_plan.md) | cb8c5c8 | 24/06/2026 |
| `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/task.md` | Lista de Tarefas | [Link](https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/task.md) | cb8c5c8 | 24/06/2026 |
| `05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/walkthrough.md` | Registro de Alterações | [Link](https://github.com/erickvaq/chatgpt-cofre-operacional/blob/main/05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/walkthrough.md) | cb8c5c8 | 24/06/2026 |

---

## ERROS CRÍTICOS QUE NÃO PODEM SE REPETIR

1. Não confundir iniciais dos nomes com quadras;
2. `A a E` significa iniciais dos nomes dos clientes, não quadras;
3. Não usar contratos locais como fonte principal;
4. Não acessar `Configurações > Contatos`;
5. Usar apenas `Carnês` e `Cobranças/Boletos` no WidePay;
6. Não criar timers repetidos;
7. Não gerar arquivos finais sem autorização;
8. Não enviar dados financeiros sensíveis ao GitHub sem autorização;
9. Não calcular total pago geral usando apenas um carnê quando houver vários;
10. Não inventar valores, datas, parcelas, clientes ou lotes.

---

## Próximo Passo Recomendado

1. Iniciar a auditoria dos clientes pendentes listados na tabela de pendências individuais (A a E) mediante autorização ou solicitação do usuário.
