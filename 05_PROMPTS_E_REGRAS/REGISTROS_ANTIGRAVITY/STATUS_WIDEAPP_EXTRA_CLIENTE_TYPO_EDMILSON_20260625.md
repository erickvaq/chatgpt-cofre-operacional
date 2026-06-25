# Registro de Correção - Unificação de Contas e Correção de Typos (Edmilson/Edimson) - 2026-06-25

## 📝 Objetivo da Alteração
Atender à solicitação do usuário para integrar de forma transparente na base de cálculos da auditoria os boletos e carnês pagos de um mesmo cliente que possuam erros de digitação de nome no WidePay (ex: registros sob o nome `"Edimson silva dos santis"` e `"EDMILSON SILVA DOS SANTOS"`).

---

## 📋 Melhorias e Correções Realizadas

1. **Correção de Bloqueio por Erro RPP (coletor_tabelas_paginadas.py):**
   - Ajustada a função `wideappValidarMetaColeta` no código JS injetado.
   - **Regra de Flexibilidade:** Se o total de registros coletados for igual ou maior ao total exibido pelo WidePay (`totalColetadoUnico >= totalWidePay.total`), a auditoria **NÃO é bloqueada** pelo erro de seleção do controle de registros por página (`'Registros por pagina nao foi localizado/selecionado'`). Isso evita falhas de pipeline quando todos os dados já foram obtidos com sucesso por paginação.

2. **Filtro Seguro de Nomes na Raspagem (extrator_widepay.py):**
   - Adicionada a função helper `wideappNormalizarBusca` no template JS injetado em ambas as telas (Carnes e Cobranças).
   - Implementada a validação do nome no loop de extração (`foundRows.forEach`). Agora, cada linha capturada no DOM passa por uma checagem rigorosa para garantir que o campo cliente corresponda a um dos termos de busca (ex: `"edmilson"`, `"edimson"`, `"edjinson"`).
   - **Benefício:** Evita a captura e mistura acidental de registros de outros clientes que possuem apenas prefixos de nome semelhantes (ex: `"Edna"` ou `"Edvaldo"` ao pesquisar `"ed"`).

3. **Homologação e Cópia Isolada:**
   - As alterações foram validadas localmente e versionadas no repositório GitHub via commit `f8831cd`.
   - Os arquivos atualizados foram copiados com sucesso para a pasta de execução isolada do usuário no Desktop:
     `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\WideAPP_EXTRA\app\coletor_tabelas_paginadas.py`
     `C:\Users\Windows User\Desktop\TESTE_WIDEAPP_EXTRA_ISOLADO\WideAPP_EXTRA\app\extrator_widepay.py`

---

## 🔍 Próximo Passo Recomendado
Solicitar ao usuário que reabra a interface Tkinter através do `RODAR_INTERFACE_ISOLADA.bat` (ou executável correspondente) e gere o relatório para o cliente **`Edmilson Leo` (lote F05)**. Os boletos sob `"Edimson silva dos santis"` e `"EDMILSON SILVA DOS SANTOS"` serão unificados de forma 100% transparente nos relatórios e nos cálculos.
