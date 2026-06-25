# Procedimento Operacional: Acesso Automatizado WidePay via Google Chrome, WMI e CDP 9333

## 1. O Problema Encontrado Originalmente
Ao executar comandos de automação que abrem navegadores diretamente no terminal da Antigravity IDE, o processo é iniciado dentro de um **Windows Job Object**. Quando a tarefa de terminal termina, o Windows encerra automaticamente o processo pai e todos os seus filhos, matando o navegador dedicado e derrubando a porta do CDP.

## 2. A Solução: Google Chrome (Perfil Dedicado) + WMI
Para evitar o encerramento do processo pelo Job Object da IDE, utilizamos a criação de processos via **WMI (Windows Management Instrumentation)** pelo CIM no PowerShell. Isso spawna o processo do Chrome como filho de `wmiprvse.exe`, desvinculando-o inteiramente da árvore de processos do terminal da IDE.

Usamos a porta `9333` e um perfil de usuário estritamente separado para garantir que o Chrome não se conecte à sessão primária do usuário (que costuma rodar sem CDP e gerar conflitos).

### Parâmetros Oficiais:
* **Navegador:** Google Chrome
* **Porta CDP:** `9333`
* **Host/Endpoint:** `localhost:9333`
* **Perfil Dedicado:** `08_NAVEGADOR_WIDEPAY\ChromeProfile_9333`

---

## 3. Como Testar o CDP
Execute o seguinte comando no terminal para verificar se o CDP está respondendo corretamente na porta `9333`:
```powershell
Invoke-WebRequest http://localhost:9333/json/version -UseBasicParsing
```
O retorno esperado é um JSON contendo a versão do navegador e a `webSocketDebuggerUrl`.

---

## 4. Como Agir se o Login for Necessário
O script de consulta detecta automaticamente se a página atual do WidePay é a tela de login (`/conta/acessar`).
* O preenchimento da senha é **estritamente manual** por questões de segurança.
* Se a página solicitar login, o script irá parar a execução retornando o código de status apropriado, avisando que o usuário deve efetuar o login manualmente na janela do Google Chrome.
* Uma vez efetuado o login, o usuário deve enviar a mensagem informando o sucesso ao agente.

---

## 5. Como Consultar um Cliente no WidePay
Para qualquer busca de cliente (ex: Filinto Queiroz):
1. Limpar filtros anteriores de status selecionando todos os checkboxes na página (Ativo, Cancelado, Finalizado, Pendente) e clicando em "Aplicar" (`id: "jab-1088"`).
2. Digitar o nome no campo de busca (`id: "jab-1036-field"`) e clicar em pesquisar (`id: "jab-1038"`).
3. Varre **todas as páginas de resultados** clicando em próximo (`id: "jab-1023"`) até que o botão esteja desativado.
4. Extrair os dados da tabela (Carnê ID, Cliente, Parcelas, Recebimentos, Valor, Status, Vencimento).
5. Salvar em formato JSON consolidado em `07_DADOS_TEMPORARIOS\WIDEPAY_CONSULTAS\`.

---

## 6. Segurança e Auditoria
* **Somente Leitura:** O WidePay só pode ser usado para consultas passivas. Nunca mude cadastros, boletos ou cobranças.
* **Proibição de Simulação:** Se o CDP falhar ou o WidePay estiver inacessível, não invente ou simule os dados financeiros. Deixe a auditoria marcada como `PENDENTE — AGUARDANDO LOGIN MANUAL`.
