---
name: widepay-publicacao-segura
description: Use quando o pedido envolver salvar, sincronizar, publicar, subir para GitHub, subir para Google Drive, cofre, pacote leve, handoff, relatorio operacional, regras, prompts, documentacao ou evidencias do projeto WidePay. Aplica a preferencia persistente do usuario: pacotes leves publicaveis devem ser enviados ao GitHub/Drive sem pedir nova autorizacao e devem ficar acessiveis publicamente quando o destino permitir, separando automaticamente conteudo sensivel para versao sanitizada ou local.
---

# WidePay Publicacao Segura

Aplicar esta skill quando um resultado do projeto `Relatorio_WidePay_Lotes` gerar material sincronizavel: regras, prompts, handoffs, documentacao, logs operacionais sem dados sensiveis, manifestos, relatorios tecnicos leves, mapas, evidencias e arquivos de continuidade.

## Regra persistente do usuario

Nao pedir nova autorizacao para subir ao GitHub ou Google Drive quando o material for pacote leve, publicavel, dentro do escopo do projeto e ja classificado como sincronizavel.

Esta regra vale como autorizacao operacional permanente para publicacao/sincronizacao de pacotes leves publicaveis do projeto.

## Acessibilidade publica

O pacote publicado deve ser acessivel publicamente quando o destino permitir. Preferir:

- repositorio GitHub publico ou caminho publico ja usado no cofre;
- link Drive compartilhavel/publico quando o arquivo for adequado para Drive;
- link real verificado depois da publicacao.

Nao tratar GitHub/Drive como arquivo escondido se o usuario pediu continuidade publica. O resultado publicavel deve poder ser aberto por link, sem depender do Antigravity.

## Separacao automatica de conteudo nao publicavel

Nao publicar no pacote publico itens com:

- senha, token, cookie, chave ou credencial;
- dados pessoais/financeiros brutos de clientes;
- prints privados, navegador logado ou informacao de sessao;
- arquivo pesado, cache, perfil de navegador, banco local ou binario desnecessario;
- destino GitHub/Drive incerto;
- sobrescrita destrutiva ou conflito com versao existente;
- acao fora do escopo do projeto WidePay;
- duvida real sobre exposicao de dados.

Nesses casos, separar automaticamente para uma destas saidas:

- versao sanitizada publicavel;
- manifesto indicando que o item ficou somente local;
- proxima acao segura para transformar em pacote publico.

## Fluxo

1. Classificar o material como `PACOTE_PUBLICAVEL`, `SANITIZAR_ANTES_DE_PUBLICAR` ou `SOMENTE_LOCAL_POR_SEGURANCA`.
2. Para `PACOTE_PUBLICAVEL`, preparar sincronizacao sem pedir nova autorizacao.
3. Publicar somente arquivos necessarios ao cofre/GitHub ou Drive.
4. Confirmar publicacao com evidencia real: caminho local, destino, commit/link/id quando existir.
5. Nunca inventar link antes da publicacao real.

## Padrao de resposta

Relatar:

- o que ficou local;
- o que foi classificado como pacote leve;
- o que foi publicado no GitHub/Drive;
- o que foi separado ou sanitizado por seguranca;
- links reais somente depois de confirmados;
- proxima acao segura.
