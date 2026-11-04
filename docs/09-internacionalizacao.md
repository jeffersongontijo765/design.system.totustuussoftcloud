# 09 — Internacionalização e Localização

> Parte do [SDD v2](00-README.md).

---

## 1. Locales

| Código | Idioma | Situação |
|---|---|---|
| `en` | Inglês (canônico) | Fonte de todas as chaves |
| `pt-BR` | Português (Brasil) | Locale padrão do produto |
| `es`, `fr`, `de`, `it`, `zh`, `ja`, `ru`, `ar` | Demais idiomas | Tradução por fornecedor com revisão nativa |

A v1 declara 100% de chaves em dez locales, verificado em 04/08/2026 por testes. **[Declarado]**: a v2 exige que o teste seja executado em CI, e o número é gerado pelo teste, não digitado no SDD.

## 2. Regras

1. Chave canônica em inglês, em `snake.case` com namespace por módulo: `academico.nota.salvar`.
2. Nenhum texto visível fixo no código ou em template.
3. Plural e gênero por ICU MessageFormat. Não concatenar fragmentos de frase.
4. Datas, horas, números e moeda por `Intl` do locale. Moeda do tenant é independente do idioma.
5. Fallback: idioma do usuário → idioma do tenant → `en`. Chave ausente em locale não canônico gera aviso em CI, não erro em produção.
6. Ordem de precedência do locale: preferência do usuário > parâmetro de locale do tenant > cabeçalho `Accept-Language` > padrão do produto.
7. Variável `APP_LOCALE` forçada (uso em instalação dedicada) desativa a troca pelo usuário e deve aparecer no painel de configuração.

## 3. RTL (árabe)

- `dir="rtl"` no elemento `html` quando o locale é `ar`.
- Propriedades lógicas em CSS (`margin-inline-start`, `inline-end`) no lugar de esquerda e direita.
- Ícones direcionais (setas, avanço) espelhados; ícones de marca e de mídia não.
- Teste visual em RTL para cada tela nova.

## 4. Governança de tradução

- Fornecedor de tradução com contrato de confidencialidade. Texto de tela não contém dado pessoal real.
- Glossário por idioma com termos do domínio educacional (matrícula, mantenedora, unidade etc.).
- Revisão nativa antes de publicar. Tradução automática não é publicada sem revisão.
- Mudança de texto em `en` gera tarefa de tradução para os demais locales com prazo.

## 5. Critérios de aceite

- [ ] Teste de paridade: todas as chaves de `en` existem nos dez locales ou têm marca de pendência explícita.
- [ ] Teste de placeholders: mesmos parâmetros em todos os locales.
- [ ] Teste de layout em `ar` em telas de formulário e tabela.
- [ ] Nenhum texto fixo detectado por varredura do código de views.
