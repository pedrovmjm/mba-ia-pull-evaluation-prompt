# Desafio: Pull, Otimização e Avaliação de Prompts


### Stack Utilizada

- Python 3.11+
- Conta no [LangSmith](https://smith.langchain.com/)
- OpenAI (modelos GPT-4o e GPT-4o-mini)


## Técnicas Aplicadas 

### 1. Role Prompting

**O que é:** Definir uma persona específica para o modelo, dando contexto profissional e expertise.

**Por que escolhi:** Um Product Manager sênior tem o conhecimento necessário para transformar bugs técnicos em User Stories orientadas a valor de negócio. A persona traz consistência no tom, formato e profundidade das respostas.

**Como apliquei:** No início do system prompt, defini:
> "Você é um Product Manager sênior com 10 anos de experiência em metodologias ágeis. Sua especialidade é transformar relatos de bugs em User Stories claras, acionáveis e completas."

### 2. Few-shot Learning

**O que é:** Fornecer exemplos concretos de entrada/saída para o modelo aprender o padrão esperado.

**Por que escolhi:** Exemplos práticos são a forma mais eficaz de comunicar o formato e nível de detalhe esperado. Sem exemplos, o modelo pode gerar respostas em formatos inconsistentes.

**Como apliquei:** Incluí 2 exemplos no system prompt:
- **Exemplo 1 (Bug Simples):** "Botão de login não responde ao clicar" → User Story com 5 critérios de aceitação
- **Exemplo 2 (Bug Médio):** Endpoint com erro HTTP 500 → User Story com critérios de aceitação + seção de Contexto Técnico

### 3. Chain of Thought (CoT)

**O que é:** Instruir o modelo a raciocinar passo a passo antes de gerar a resposta final.

**Por que escolhi:** A conversão de bug para User Story requer análise (identificar persona, severidade, componentes afetados) antes da escrita. O CoT garante que o modelo não pule etapas importantes.

**Como apliquei:** Defini um processo explícito de 6 passos:
1. Analise o bug
2. Identifique a persona
3. Formule a User Story
4. Defina Critérios de Aceitação
5. Adicione contexto técnico
6. Sugira tasks técnicas

### 4. Output Structuring (aplicada no PROMPT v2)

**O que é:** Definir regras explícitas de formato de saída por tipo/complexidade de input, garantindo que o modelo produza respostas com estrutura previsível e consistente.

**Por que escolhi:** Na primeira iteração, o modelo gerava respostas com formato inconsistente entre bugs simples, médios e complexos. Definir templates de saída por nível de complexidade aumentou a clareza e o alinhamento com as referências esperadas.

**Como apliquei:** Criei regras de formato por complexidade:
- **Bug Simples:** User Story + 3-5 critérios Given-When-Then
- **Bug Médio:** User Story + 4-7 critérios + subtítulos condicionais (Contexto Técnico, Contexto de Segurança, Exemplo de Cálculo) + seção de Contexto Técnico
- **Bug Complexo:** Seções delimitadas com `=== NOME DA SEÇÃO ===` (USER STORY PRINCIPAL, CRITÉRIOS DE ACEITAÇÃO organizados por letras A/B/C, CRITÉRIOS TÉCNICOS, CONTEXTO DO BUG, TASKS TÉCNICAS SUGERIDAS por sprint)
- Adicionei um 3º exemplo (bug complexo) demonstrando o formato exato com seções `===`

---

## Resultados Finais

### [Relatorio Detalhado das Iteracoes](docs/RELATORIO_ITERACOES.md)

### Comparativo Iteracao 1 vs Iteracao 2

| Métrica        | Iteracao 1 | Iteracao 2 |
|----------------|-----------|-------------|
| Helpfulness    | 0.91      | 0.94        |
| Correctness    | 0.86      | 0.89        |
| F1-Score       | 0.79      | 0.83        |
| Clarity        | 0.89      | 0.92        |
| Precision      | 0.94      | 0.96        |
| **Media**      | **0.8777**| **0.9072**  |
| **Status**     | REPROVADO | APROVADO    |

### Iteracoes

| Iteracao | O que mudou | Resultado |
|----------|-------------|-----------|
| 1 | Prompt v2 inicial com Role Prompting + Few-shot (2 exemplos) + Chain of Thought. Instrucoes gerais de formato. | Media 0.8777 - REPROVADO. F1 (0.79) e Clarity (0.89) abaixo do threshold. |
| 2 | Adicionado Output Structuring: regras de formato por complexidade (simples/medio/complexo), exemplo 3 para bugs complexos com secoes `=== ===`, instrucoes para preservar TODAS as infos tecnicas, personas especificas, subtitulos de criterios, secoes condicionais (Contexto de Seguranca, Exemplo de Calculo, etc). | Media 0.9072 - APROVADO. Clarity subiu de 0.89 para 0.92, F1 de 0.79 para 0.83, Precision de 0.94 para 0.96. |

### O que foi modificado na Iteracao 2

1. **Classificacao de complexidade explícita**: Adicionado passo 2 no processo de raciocinio para classificar o bug como simples/medio/complexo antes de gerar a resposta.

2. **Regras de formato por complexidade**: Substituidas as regras genericas por instrucoes especificas para cada nivel:
   - Simples: User Story + 3-5 criterios
   - Medio: User Story + 4-7 criterios + subtitulos + Contexto Tecnico + secoes condicionais
   - Complexo: Secoes delimitadas com `=== NOME ===` (USER STORY PRINCIPAL, CRITERIOS DE ACEITACAO, CRITERIOS TECNICOS, CONTEXTO DO BUG, TASKS TECNICAS)

3. **Terceiro exemplo (bug complexo)**: Adicionado exemplo mostrando o formato exato com secoes `===`, criterios organizados por letras (A, B, C...), e tasks por sprint.

4. **Regras de conteudo reforçadas**: Instrucao para preservar TODAS as infos tecnicas, incorporar cenarios numericos, usar personas especificas (nunca genericas), e incluir sugestoes de solucao tecnica.

5. **Tecnica adicional**: Output Structuring como 4a tecnica aplicada.

---

## Link para o prompt no LangSmith Hub

https://smith.langchain.com/hub/pedrovmjm/bug_to_user_story_v2

