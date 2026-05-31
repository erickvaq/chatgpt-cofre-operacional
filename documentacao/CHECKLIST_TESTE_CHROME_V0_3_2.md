# Checklist de Teste Chrome - v0.3.2

Este checklist serve para testar a extensao v0.3.2 sem substituir a pasta ativa do Chrome.

## Regra de seguranca

- Nao alterar `C:\Users\Windows User\Documents\Chrome_Extensoes\ChatBridge`.
- Nao copiar a v0.3.2 para a pasta ativa.
- Nao publicar no GitHub.
- Se o Chrome impedir o carregamento duplicado no mesmo perfil, usar um perfil temporario de teste ou parar e pedir confirmacao antes de qualquer mudanca estrutural.

## Caminho de teste

Workspace de teste:

`C:\Users\Windows User\Desktop\chatgpt projetos\CHAT_BRIDGE_CODEX_ANTIGRAVITY\WORKSPACE_CHATBRIDGE_V0_3_2\chat_bridge_ext_v0_3_2`

## Passo a passo

1. Abrir `chrome://extensions`.
2. Confirmar que a extensao ativa atual continua intacta.
3. Carregar temporariamente a pasta do workspace v0.3.2 como extensao de teste, somente se o Chrome aceitar sem substituir a ativa.
4. Abrir abas de teste para ChatGPT, Codex e Antigravity.
5. Marcar os papeis nas abas:
   - ChatGPT como fonte.
   - Codex como destino.
   - Antigravity como destino.
6. Testar `Enviar para Codex`.
7. Testar `Enviar para Antigravity`.
8. Testar bloqueio de payload ativo e envio duplicado.
9. Testar `Capturar resposta`.
10. Testar `Retornar ao ChatGPT`.
11. Confirmar que a janela de origem nao recebe colagem na aba errada.
12. Confirmar que o estado visual muda entre livre, preparado, enviado, executando, resposta capturada, aguardando auditoria, auditado, bloqueado e erro.
13. Registrar o resultado final da bateria.

## Resultado esperado

- Um unico payload por vez.
- Origem e destino separados.
- Nenhum envio automatico destrutivo.
- Nenhuma sobrescrita da pasta ativa.
- Resposta capturada volta para ChatGPT para auditoria.

## Campos para registrar

- Data do teste:
- Perfil de Chrome usado:
- Extensao de teste carregada em:
- Resultado de `Enviar para Codex`:
- Resultado de `Enviar para Antigravity`:
- Resultado do bloqueio de payload ativo:
- Resultado de `Capturar resposta`:
- Resultado de `Retornar ao ChatGPT`:
- Observacoes de erro:
- Decisao final:

## Critério de liberacao para o passo seguinte

Somente avancar para promocao ou empacotamento se:

- o fluxo basico funcionou;
- o bloqueio de payload ativo funcionou;
- a captura e o retorno ao ChatGPT funcionaram;
- a pasta ativa continuou intocada;
- a v0.3.1 permaneceu intacta;
- nao houve erro critico de Chrome.
