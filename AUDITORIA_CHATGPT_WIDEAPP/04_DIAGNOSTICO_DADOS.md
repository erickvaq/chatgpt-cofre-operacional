# 04 - Diagnóstico de Dados e Persistência

## Caminhos Exatos das Bases Oficiais
* **JSON Indexado da Instalação Oficial**: `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_V20_ISOLADO\WideAPP_EXTRA\data\clientes_indexados.json`
* **JSON de Cache do WidePay**: `c:\Users\Windows User\Desktop\chatgpt projetos\Relatorio_WidePay_Lotes\WideAPP_EXTRA\data\widepay_boletos_cache.json`
* **Planilha XLSX da Instalação Oficial**: `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_V20_ISOLADO\WideAPP_EXTRA\BANCO_DADOS_WIDEAPP_EXTRA.xlsx`

## Contagem Total de Registros Persistidos
* **Registros em `clientes_indexados.json` (Instalação Oficial)**: 92 registros.
* **Cobranças/Carnês em `widepay_boletos_cache.json`**: 4775 lançamentos brutos.

## Emmanuel Félix da Costa Filho (Confirmação Real de Persistência)
* **Linhas Reais Gravadas no `clientes_indexados.json` da Instalação Oficial**: **2 linhas independentes** (G2 e G18).
* **Registros Gravados no JSON da Instalação Oficial**:
```json
[
  {
    "selecionado": false,
    "cliente": "EMMANUEL FÉLIX DA COSTA FILHO",
    "lote": "G2",
    "quadra": "G",
    "contrato": "Encontrado",
    "contrato_arquivo": "C:\\Users\\Windows User\\Desktop\\AGUA VIVA\\- CONTRATOS AGUA VIVA\\QUADRA G\\Emmanuel Felix G2 G18 Agua Viva Leandro Meirelles\\Emmanuel Felix G2 G18 Agua Viva Leandro Meirelles.docx",
    "origem": "Contrato local",
    "pasta_local": "C:\\Users\\Windows User\\Desktop\\AGUA VIVA\\- CONTRATOS AGUA VIVA\\QUADRA G\\Emmanuel Felix G2 G18 Agua Viva Leandro Meirelles",
    "contrato_modalidade": "parcelado",
    "parcelas_total_contrato": 50,
    "valor_base_parcela": 198.0,
    "valor_total_contratado": 4950.0,
    "entrada_valor": 1000.0,
    "origem_contrato": "Contrato local",
    "origem_dados": "Contrato local + WidePay global",
    "status": "APROVADO",
    "observacoes": "Reconciliacao concluida com sucesso. Sem divergencias encontradas.",
    "data_atualizacao": "2026-07-22T23:14:39",
    "chave_lote_canonica": "G2",
    "parcelas_pagas_identificadas": 31,
    "parcelas_restantes": 19,
    "parcelas_resumo": "31 / 50 pagas",
    "contrato_resumo": "Parcelado",
    "valor_total_pago": 6313.03,
    "ultima_parcela_paga": "lt G2 apart 47 par 99",
    "ultimo_vencimento_pago": "10/06/2026",
    "valor_ultimo_pagamento": "R$ 105,60",
    "ultima_atualizacao_widepay": "2026-07-10T13:25:34",
    "situacao_final": "Em andamento",
    "status_atraso_qtd": 0,
    "status_atraso_cor": "verde",
    "status_atraso_rotulo": "Em dia",
    "status_atraso_origem": "WidePay",
    "divergencias": "",
    "boletos_atrasados": 0,
    "saneamento_acao": "atencao",
    "saneamento_categoria": "ativos",
    "saneamento_origem": "planilha_marcada",
    "saneamento_observacao": "Classificacao manual por cor: atencao",
    "cliente_canonico": "EMMANUEL FELIX DA COSTA FILHO",
    "chave_saneamento": "emmanuel felix da costa filho|G2",
    "quitado_manual": false,
    "bloqueado_removido_manual": false,
    "atencao_manual": true,
    "ignorado_manual": false,
    "ativo_na_lista_principal": true,
    "status_operacional": "Ativo",
    "origem_classificacao": "planilha_marcada",
    "bloqueado_reaparecer": false,
    "motivo_remocao_lista": "Classificacao manual por cor: atencao",
    "pagamentos_recentes_5m": {
      "2025-08": {
        "status": "Sem boleto",
        "texto1": "Sem boleto",
        "texto2": "-"
      },
      "2025-09": {
        "status": "Sem boleto",
        "texto1": "Sem boleto",
        "texto2": "-"
      },
      "2025-10": {
        "status": "Pago",
        "texto1": "R$ 99,00",
        "texto2": "10/10",
        "_evento_id": "4823:2025-10",
        "_origem_evento": "exato"
      },
      "2025-11": {
        "status": "Pago",
        "texto1": "R$ 101,67",
        "texto2": "10/11",
        "_evento_id": "4824:2025-11",
        "_origem_evento": "exato"
      },
      "2025-12": {
        "status": "Pago",
        "texto1": "R$ 99,00",
        "texto2": "10/12",
        "_evento_id": "4825:2025-12",
        "_origem_evento": "exato"
      },
      "2026-01": {
        "status": "Pago",
        "texto1": "R$ 101,21",
        "texto2": "10/01",
        "_evento_id": "4826:2026-01",
        "_origem_evento": "exato"
      },
      "2026-02": {
        "status": "Pago",
        "texto1": "R$ 103,05",
        "texto2": "10/02",
        "_evento_id": "4827:2026-02",
        "_origem_evento": "exato"
      },
      "2026-03": {
        "status": "Pago",
        "texto1": "R$ 101,21",
        "texto2": "10/03",
        "_evento_id": "4828:2026-03",
        "_origem_evento": "exato"
      },
      "2026-04": {
        "status": "Pago",
        "texto1": "R$ 99,00",
        "texto2": "10/04",
        "_evento_id": "4829:2026-04",
        "_origem_evento": "exato"
      },
      "2026-05": {
        "status": "Pago",
        "texto1": "R$ 105,14",
        "texto2": "10/05",
        "_evento_id": "4830:2026-05",
        "_origem_evento": "exato"
      },
      "2026-06": {
        "status": "Pago",
        "texto1": "R$ 105,60",
        "texto2": "10/06",
        "_evento_id": "4831:2026-06",
        "_origem_evento": "exato"
      },
      "2026-07": {
        "status": "Pendente",
        "texto1": "Pendente",
        "texto2": "10/07",
        "_evento_id": "4832:2026-07",
        "_origem_evento": "exato"
      },
      "_enriquecido": true
    }
  },
  {
    "selecionado": false,
    "cliente": "EMMANUEL FÉLIX DA COSTA FILHO",
    "lote": "G18",
    "quadra": "G",
    "contrato": "Encontrado",
    "contrato_arquivo": "C:\\Users\\Windows User\\Desktop\\AGUA VIVA\\- CONTRATOS AGUA VIVA\\QUADRA G\\Emmanuel Felix G2 G18 Agua Viva Leandro Meirelles\\Emmanuel Felix G2 G18 Agua Viva Leandro Meirelles.docx",
    "origem": "Contrato local",
    "pasta_local": "C:\\Users\\Windows User\\Desktop\\AGUA VIVA\\- CONTRATOS AGUA VIVA\\QUADRA G\\Emmanuel Felix G2 G18 Agua Viva Leandro Meirelles",
    "contrato_modalidade": "parcelado",
    "parcelas_total_contrato": 50,
    "valor_base_parcela": 198.0,
    "valor_total_contratado": 4950.0,
    "entrada_valor": 1000.0,
    "origem_contrato": "Contrato local",
    "origem_dados": "Contrato local + WidePay global",
    "status": "APROVADO",
    "observacoes": "Reconciliacao concluida com sucesso. Sem divergencias encontradas.",
    "data_atualizacao": "2026-07-22T23:14:39",
    "chave_lote_canonica": "G18",
    "parcelas_pagas_identificadas": 29,
    "parcelas_restantes": 21,
    "parcelas_resumo": "29 / 50 pagas",
    "contrato_resumo": "Parcelado",
    "valor_total_pago": 5977.07,
    "ultima_parcela_paga": "lt G2 apart 47 par 99",
    "ultimo_vencimento_pago": "10/06/2026",
    "valor_ultimo_pagamento": "R$ 105,60",
    "ultima_atualizacao_widepay": "2026-07-10T13:25:34",
    "situacao_final": "Em andamento",
    "status_atraso_qtd": 0,
    "status_atraso_cor": "verde",
    "status_atraso_rotulo": "Em dia",
    "status_atraso_origem": "WidePay",
    "divergencias": "",
    "boletos_atrasados": 0,
    "saneamento_acao": "atencao",
    "saneamento_categoria": "ativos",
    "saneamento_origem": "planilha_marcada",
    "saneamento_observacao": "Classificacao manual por cor: atencao",
    "cliente_canonico": "EMMANUEL FELIX DA COSTA FILHO",
    "chave_saneamento": "emmanuel felix da costa filho|G2",
    "quitado_manual": false,
    "bloqueado_removido_manual": false,
    "atencao_manual": true,
    "ignorado_manual": false,
    "ativo_na_lista_principal": true,
    "status_operacional": "Ativo",
    "origem_classificacao": "planilha_marcada",
    "bloqueado_reaparecer": false,
    "motivo_remocao_lista": "Classificacao manual por cor: atencao",
    "pagamentos_recentes_5m": {
      "2025-08": {
        "status": "Sem boleto",
        "texto1": "Sem boleto",
        "texto2": "-"
      },
      "2025-09": {
        "status": "Sem boleto",
        "texto1": "Sem boleto",
        "texto2": "-"
      },
      "2025-10": {
        "status": "Pago",
        "texto1": "R$ 99,00",
        "texto2": "10/10",
        "_evento_id": "4847:2025-10",
        "_origem_evento": "exato"
      },
      "2025-11": {
        "status": "Pago",
        "texto1": "R$ 99,00",
        "texto2": "10/11",
        "_evento_id": "4848:2025-11",
        "_origem_evento": "exato"
      },
      "2025-12": {
        "status": "Pago",
        "texto1": "R$ 113,68",
        "texto2": "10/12",
        "_evento_id": "4849:2025-12",
        "_origem_evento": "exato"
      },
      "2026-01": {
        "status": "Pago",
        "texto1": "R$ 99,00",
        "texto2": "10/01",
        "_evento_id": "4850:2026-01",
        "_origem_evento": "exato"
      },
      "2026-02": {
        "status": "Pago",
        "texto1": "R$ 118,77",
        "texto2": "10/02",
        "_evento_id": "4851:2026-02",
        "_origem_evento": "exato"
      },
      "2026-03": {
        "status": "Pago",
        "texto1": "R$ 112,30",
        "texto2": "10/03",
        "_evento_id": "4852:2026-03",
        "_origem_evento": "exato"
      },
      "2026-04": {
        "status": "Pago",
        "texto1": "R$ 105,14",
        "texto2": "10/04",
        "_evento_id": "4853:2026-04",
        "_origem_evento": "exato"
      },
      "2026-05": {
        "status": "Vencido",
        "texto1": "Vencido",
        "texto2": "10/05",
        "_evento_id": "4854:2026-05",
        "_origem_evento": "exato"
      },
      "2026-06": {
        "status": "Vencido",
        "texto1": "Vencido",
        "texto2": "10/06",
        "_evento_id": "4855:2026-06",
        "_origem_evento": "exato"
      },
      "2026-07": {
        "status": "Pendente",
        "texto1": "Pendente",
        "texto2": "10/07",
        "_evento_id": "4856:2026-07",
        "_origem_evento": "exato"
      },
      "_enriquecido": true
    }
  }
]
```

## Rodrigo Monteiro de Melo (Confirmação Real de Persistência)
* **Linhas Reais Gravadas no `clientes_indexados.json` da Instalação Oficial**: **2 linhas** (F19 e G1/G19).
* **Registros Gravados no JSON da Instalação Oficial**:
```json
[
  {
    "selecionado": false,
    "cliente": "RODRIGO MONTEIRO",
    "lote": "F19",
    "quadra": "F",
    "contrato": "Encontrado",
    "contrato_arquivo": "C:\\Users\\Windows User\\Desktop\\AGUA VIVA\\- CONTRATOS AGUA VIVA\\QUADRA F\\Rodrigo Monteiro F19 agua viva Leandro Meirelles\\REF 01-06-25 F19 R$227 atrazo rodrigo-monteiro-de-melo.pdf",
    "origem": "Contrato local",
    "pasta_local": "C:\\Users\\Windows User\\Desktop\\AGUA VIVA\\- CONTRATOS AGUA VIVA\\QUADRA F\\Rodrigo Monteiro F19 agua viva Leandro Meirelles",
    "contrato_modalidade": "parcelado",
    "parcelas_total_contrato": 0,
    "valor_base_parcela": 0.0,
    "valor_total_contratado": 0.0,
    "entrada_valor": 0.0,
    "origem_contrato": "Contrato local",
    "origem_dados": "Contrato local + WidePay global",
    "status": "ERRO",
    "observacoes": "Relatorio bloqueado | BLOQUEIO: Contrato local nao localizado ou nao contem parcelas/valores confirmados.",
    "data_atualizacao": "2026-07-10T13:25:33",
    "chave_lote_canonica": "F19",
    "parcelas_pagas_identificadas": 47,
    "parcelas_restantes": "",
    "parcelas_resumo": "47 / ? pagas",
    "contrato_resumo": "Parcelado",
    "valor_total_pago": 11457.31,
    "ultima_parcela_paga": "f19 apart.36",
    "ultimo_vencimento_pago": "01/07/2026",
    "valor_ultimo_pagamento": "R$ 227,00",
    "ultima_atualizacao_widepay": "2026-07-10T13:25:33",
    "situacao_final": "Bloqueado",
    "status_atraso_qtd": 6,
    "status_atraso_cor": "vermelho",
    "status_atraso_rotulo": "Atraso leve",
    "status_atraso_origem": "WidePay",
    "divergencias": "",
    "boletos_atrasados": 6,
    "saneamento_acao": "atencao",
    "saneamento_categoria": "ativos",
    "saneamento_origem": "planilha_marcada",
    "saneamento_observacao": "Classificacao manual por cor: atencao",
    "cliente_canonico": "RODRIGO MONTEIRO DE MELO",
    "chave_saneamento": "rodrigo monteiro de melo|F19",
    "quitado_manual": false,
    "bloqueado_removido_manual": false,
    "atencao_manual": true,
    "ignorado_manual": false,
    "ativo_na_lista_principal": true,
    "status_operacional": "Ativo",
    "origem_classificacao": "planilha_marcada",
    "bloqueado_reaparecer": false,
    "motivo_remocao_lista": "Classificacao manual por cor: atencao",
    "pagamentos_recentes_5m": {
      "2025-08": {
        "status": "Pago",
        "texto1": "R$ 233,66",
        "texto2": "01/08",
        "_evento_id": "4021:2025-08",
        "_origem_evento": "exato"
      },
      "2025-09": {
        "status": "Pago",
        "texto1": "R$ 227,00",
        "texto2": "01/09",
        "_evento_id": "4022:2025-09",
        "_origem_evento": "exato"
      },
      "2025-10": {
        "status": "Pago",
        "texto1": "R$ 227,00",
        "texto2": "01/10",
        "_evento_id": "4023:2025-10",
        "_origem_evento": "exato"
      },
      "2025-11": {
        "status": "Pago",
        "texto1": "R$ 227,00",
        "texto2": "01/11",
        "_evento_id": "4024:2025-11",
        "_origem_evento": "exato"
      },
      "2025-12": {
        "status": "Pago",
        "texto1": "R$ 232,07",
        "texto2": "01/12",
        "_evento_id": "4025:2025-12",
        "_origem_evento": "exato"
      },
      "2026-01": {
        "status": "Pago avulso",
        "texto1": "R$ 227,00",
        "texto2": "Avulso",
        "origem": "boleto_avulso_recebido",
        "_evento_id": "5293:2026-01",
        "_origem_evento": "exato"
      },
      "2026-02": {
        "status": "Pago avulso",
        "texto1": "R$ 227,00",
        "texto2": "Avulso",
        "origem": "boleto_avulso_recebido",
        "_evento_id": "5293:2026-02",
        "_origem_evento": "exato"
      },
      "2026-03": {
        "status": "Pago avulso",
        "texto1": "R$ 227,00",
        "texto2": "Avulso",
        "origem": "boleto_avulso_recebido",
        "_evento_id": "5293:2026-03",
        "_origem_evento": "exato"
      },
      "2026-04": {
        "status": "Pago avulso",
        "texto1": "R$ 227,00",
        "texto2": "Avulso",
        "origem": "boleto_avulso_recebido",
        "_evento_id": "5293:2026-04",
        "_origem_evento": "exato"
      },
      "2026-05": {
        "status": "Vencido",
        "texto1": "Vencido",
        "texto2": "01/05",
        "_evento_id": "4030:2026-05",
        "_origem_evento": "exato"
      },
      "2026-06": {
        "status": "Pago",
        "texto1": "R$ 227,00",
        "texto2": "01/06",
        "_evento_id": "4031:2026-06",
        "_origem_evento": "exato"
      },
      "2026-07": {
        "status": "Pago",
        "texto1": "R$ 227,00",
        "texto2": "01/07",
        "_evento_id": "4032:2026-07",
        "_origem_evento": "exato"
      },
      "_enriquecido": true
    }
  },
  {
    "selecionado": false,
    "cliente": "RODRIGO MONTEIRO DE MELO",
    "lote": "01",
    "quadra": "G",
    "contrato": "Encontrado",
    "contrato_arquivo": "C:\\Users\\Windows User\\Desktop\\AGUA VIVA\\- CONTRATOS AGUA VIVA\\QUADRA G\\Rodrigo Monteiro de Melo - G1 G19 -  Agua Viva Leandro Meirelles\\Rodrigo Monteiro de Melo - G1 G19 -  Agua Viva Leandro Meirelles.docx",
    "origem": "Contrato local",
    "pasta_local": "C:\\Users\\Windows User\\Desktop\\AGUA VIVA\\- CONTRATOS AGUA VIVA\\QUADRA G\\Rodrigo Monteiro de Melo - G1 G19 -  Agua Viva Leandro Meirelles",
    "contrato_modalidade": "parcelado",
    "parcelas_total_contrato": 100,
    "valor_base_parcela": 190.0,
    "valor_total_contratado": 20200.0,
    "entrada_valor": 1200.0,
    "origem_contrato": "Contrato local",
    "origem_dados": "Contrato local + WidePay global",
    "status": "APROVADO",
    "observacoes": "Reconciliacao concluida com sucesso. Sem divergencias encontradas.",
    "data_atualizacao": "2026-07-10T13:25:35",
    "chave_lote_canonica": "G1/G19",
    "parcelas_pagas_identificadas": 100,
    "parcelas_restantes": 0,
    "parcelas_resumo": "100 / 100 quitado",
    "contrato_resumo": "Parcelado",
    "valor_total_pago": 20975.0,
    "ultima_parcela_paga": "g1 g19 apart.42",
    "ultimo_vencimento_pago": "10/08/2026",
    "valor_ultimo_pagamento": "R$ 199,00",
    "ultima_atualizacao_widepay": "2026-07-10T13:25:35",
    "situacao_final": "Em andamento",
    "status_atraso_qtd": 10,
    "status_atraso_cor": "vermelho",
    "status_atraso_rotulo": "Atraso critico",
    "status_atraso_origem": "WidePay",
    "divergencias": "",
    "boletos_atrasados": 10,
    "saneamento_acao": "atencao",
    "saneamento_categoria": "ativos",
    "saneamento_origem": "planilha_marcada",
    "saneamento_observacao": "Classificacao manual por cor: atencao",
    "cliente_canonico": "RODRIGO MONTEIRO DE MELO",
    "chave_saneamento": "rodrigo monteiro de melo|G1/G19",
    "quitado_manual": false,
    "bloqueado_removido_manual": false,
    "atencao_manual": true,
    "ignorado_manual": false,
    "ativo_na_lista_principal": true,
    "status_operacional": "Ativo",
    "origem_classificacao": "planilha_marcada",
    "bloqueado_reaparecer": false,
    "motivo_remocao_lista": "Classificacao manual por cor: atencao",
    "pagamentos_recentes_5m": {
      "2025-08": {
        "status": "Pago",
        "texto1": "R$ 233,66",
        "texto2": "01/08",
        "_evento_id": "4021:2025-08",
        "_origem_evento": "exato"
      },
      "2025-09": {
        "status": "Pago",
        "texto1": "R$ 232,69",
        "texto2": "10/09",
        "_evento_id": "3998:2025-09",
        "_origem_evento": "exato"
      },
      "2025-10": {
        "status": "Pago",
        "texto1": "R$ 227,00",
        "texto2": "01/10",
        "_evento_id": "4023:2025-10",
        "_origem_evento": "exato"
      },
      "2025-11": {
        "status": "Pago",
        "texto1": "R$ 204,37",
        "texto2": "10/11",
        "_evento_id": "4000:2025-11",
        "_origem_evento": "exato"
      },
      "2025-12": {
        "status": "Pago",
        "texto1": "R$ 232,07",
        "texto2": "01/12",
        "_evento_id": "4025:2025-12",
        "_origem_evento": "exato"
      },
      "2026-01": {
        "status": "Pago",
        "texto1": "R$ 228,03",
        "texto2": "25/01",
        "_evento_id": "5141:2026-01",
        "_origem_evento": "exato"
      },
      "2026-02": {
        "status": "Pago",
        "texto1": "R$ 236,31",
        "texto2": "25/02",
        "_evento_id": "5142:2026-02",
        "_origem_evento": "exato"
      },
      "2026-03": {
        "status": "Pago avulso",
        "texto1": "R$ 190,00",
        "texto2": "Avulso",
        "origem": "boleto_avulso_recebido",
        "_evento_id": "5293:2026-03",
        "_origem_evento": "exato"
      },
      "2026-04": {
        "status": "Pago avulso",
        "texto1": "R$ 190,00",
        "texto2": "Avulso",
        "origem": "boleto_avulso_recebido",
        "_evento_id": "5293:2026-04",
        "_origem_evento": "exato"
      },
      "2026-05": {
        "status": "Vencido",
        "texto1": "Vencido",
        "texto2": "10/05",
        "_evento_id": "4006:2026-05",
        "_origem_evento": "exato"
      },
      "2026-06": {
        "status": "Pago",
        "texto1": "R$ 227,00",
        "texto2": "01/06",
        "_evento_id": "4031:2026-06",
        "_origem_evento": "exato"
      },
      "2026-07": {
        "status": "Pago",
        "texto1": "R$ 227,00",
        "texto2": "01/07",
        "_evento_id": "4032:2026-07",
        "_origem_evento": "exato"
      },
      "_enriquecido": true
    }
  }
]
```

## Confirmação de Leitura da Interface do Usuário
* Ao iniciar o aplicativo, a interface lê `clientes_indexados.json` da instalação oficial.
* Foram confirmadas **duas linhas independentes para Emmanuel (G2 e G18)** e **duas linhas independentes para Rodrigo (F19 e G1/G19)** carregadas diretamente no `self.registros` e exibidas no grid da aba Ativ. Recentes.
