# MEMÓRIA OPERACIONAL DO CODEX — Relatorio_WidePay_Lotes

## Padrão obrigatório para artefatos

Sempre que eu gerar, alterar ou citar um arquivo relevante, devo:

* salvar o arquivo dentro do projeto;
* confirmar que ele existe;
* conferir tamanho;
* incluir no Git;
* criar commit;
* fazer push;
* devolver caminho local e link GitHub real.

## Padrão obrigatório para entregas visuais (PADRAO_ENTREGA_CLIENTE_SEM_BAT)

Sempre gerar HTML + PDF juntos na mesma pasta final de entrega.
Não criar arquivos `.bat` automaticamente por padrão para entregas de cliente.
Abrir a pasta final no Windows Explorer para conferência.
Os arquivos devem ter data e versão.
Nunca sobrescrever versão anterior.

## Padrão obrigatório para arquivos auxiliares do Antigravity

Se o Antigravity criar arquivos fora do projeto, como:

* `implementation_plan.md`
* `task.md`
* `walkthrough.md`

em pastas do tipo:
`.gemini/antigravity-ide/brain/...`

devo copiar esses arquivos para dentro do projeto antes do commit, preferencialmente em:
`05_PROMPTS_E_REGRAS/REGISTROS_ANTIGRAVITY/`

Depois devo subir esses arquivos ao GitHub e devolver os links reais.

## Proibição

Não inventar link do GitHub.
Não dizer que subiu sem push confirmado.
Não deixar artefato importante apenas como caminho local.
Não salvar tokens, senhas, credenciais ou chaves de API.

## Regra contra timers repetidos e esperas infinitas (REGRA 28)

Sempre que uma tarefa, script ou extração do WidePay demorar, a IA não deve criar timers repetidos de 30 ou 40 segundos nem enviar mensagens sucessivas de espera. Seguir estritamente o comportamento obrigatório e o padrão de resposta da REGRA 28 para garantir economia de tokens e controle operacional.

