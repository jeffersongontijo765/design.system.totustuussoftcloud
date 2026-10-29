# Agente e skill de front-end (design system)

Agente e skill para criar ou melhorar telas usando somente os componentes do design system. Funciona com as IDEs abaixo, a partir da mesma instrução (`core/frontend-design-system.md`).

## Instalar em um projeto

```bash
python3 <caminho-deste-diretorio>/install.py <pasta-do-projeto>
```

Gera, dentro do projeto:

| IDE | Arquivo |
|---|---|
| Claude Code | `.claude/skills/frontend-design-system/SKILL.md` e `.claude/agents/frontend-design-specialist.md` |
| Cursor | `.cursor/rules/frontend-design-system.mdc` |
| VS Code, JetBrains e Visual Studio com GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurf/rules/frontend-design-system.md` |
| Codex e outras que leem `AGENTS.md` | `AGENTS.md` |
| JetBrains AI Assistant | `.aiassistant/rules/frontend-design-system.md` |

Escolha as IDEs com `--ides claude,cursor,copilot,windsurf,codex,jetbrains`.

Também copia `scripts/gera_indice.py`. Para gerar o índice de componentes:

```bash
python3 scripts/gera_indice.py <pasta-do-design-system> docs/componentes.md
```

## Atenção

- Rodar o instalador de novo acrescenta o conteúdo de `AGENTS.md` outra vez (duplica). Apague a seção antiga antes de reinstalar.
- O agente existe como agente só no Claude Code. As outras IDEs recebem as mesmas instruções como regra.
- Não foi testado dentro de cada IDE; confirme que a IDE carrega o arquivo gerado.

## Conteúdo

- `core/frontend-design-system.md`: a instrução única (localizar o design system, escolher componente, montar, verificar, registrar lacuna).
- `scripts/gera_indice.py`: gera o índice a partir dos READMEs de um design system.
- `install.py`: gera o arquivo de cada IDE.
