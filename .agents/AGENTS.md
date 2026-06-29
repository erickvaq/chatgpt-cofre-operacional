# Project Custom Rules — Relatorio_WidePay_Lotes

## Regras de Acesso e Resolução de Documentos Externos (Google Docs / Drive / GitHub)
1. **Preferência por Fontes Locais/Sincronizadas**: Não depender de abrir links do Google Docs por meio do navegador automatizado (CDP/Chrome visível) quando o arquivo já existir localmente no projeto, no Google Drive sincronizado ou no repositório GitHub.
2. **Fallback Automático**: Se o arquivo estiver disponível no projeto local ou no Drive sincronizado, ler a cópia local diretamente. Caso falte localmente, buscar via API/urllib ou repositório GitHub.
3. **Isolamento de Automação**: Não misturar a automação de leitura de documentos ou transcrição com o Chrome dedicado do WidePay para evitar conflitos de porta ou perfil.
4. **Resiliência do CDP**: Se o navegador ou CDP falhar, não ficar abrindo novas guias redundantes. Encerrar imediatamente qualquer processo ou aba temporária e registrar no log: `“falha no navegador/CDP, usando arquivo local/GitHub como fallback”`.
5. **Critério de Conclusão**: Não considerar a leitura de um documento como concluída se o acesso ao Google Docs via navegador falhar, disparando o fallback de forma explícita.
