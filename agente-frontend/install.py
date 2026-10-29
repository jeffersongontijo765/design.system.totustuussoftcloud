"""Instala a skill e o agente de front-end com design system em um projeto, para várias IDEs.

Uso: python3 install.py <pasta-do-projeto> [--ides claude,cursor,copilot,windsurf,codex,jetbrains]

Fonte única: core/frontend-design-system.md. Cada IDE recebe o arquivo no formato que ela lê.
O script de índice (scripts/gera_indice.py) também é copiado para o projeto.
"""
import argparse, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
CORE = open(os.path.join(HERE, 'core', 'frontend-design-system.md'), encoding='utf8').read()
AGENT_BODY = (
    'Você é o especialista em design e front-end deste projeto. Garanta que as telas sejam montadas com os '
    'componentes do design system, sem recriar nada que já existe. Antes de alterar qualquer tela, siga o '
    'processo abaixo, na ordem.\n\n'
)
DESC = 'Especialista em design e front-end. Monta ou melhora telas usando somente os componentes do design system do projeto.'

ADAPTERS = {
    # Claude Code: skill e agente
    'claude': [
        ('.claude/skills/frontend-design-system/SKILL.md', f'---\nname: frontend-design-system\ndescription: "{DESC}"\n---\n\n' + CORE),
        ('.claude/agents/frontend-design-specialist.md', f'---\nname: frontend-design-specialist\ndescription: "{DESC}"\ntools: Read, Grep, Glob, Edit, Write, Bash\n---\n\n' + AGENT_BODY + CORE),
    ],
    # Cursor: regra com frontmatter .mdc (sempre ativa para arquivos de interface)
    'cursor': [
        ('.cursor/rules/frontend-design-system.mdc', f'---\ndescription: {DESC}\nglobs: ["**/*.{{html,php,vue,jsx,tsx,css,scss,blade.php}}"]\nalwaysApply: false\n---\n\n' + CORE),
    ],
    # GitHub Copilot (VS Code, JetBrains, Visual Studio): instruções do repositório
    'copilot': [
        ('.github/copilot-instructions.md', CORE),
    ],
    # Windsurf: regra em .windsurf/rules com trigger por arquivo
    'windsurf': [
        ('.windsurf/rules/frontend-design-system.md', '---\ntrigger: glob\nglobs: "**/*.{html,php,vue,jsx,tsx,css,scss}"\n---\n\n' + CORE),
    ],
    # Codex, Cursor e outras ferramentas que leem AGENTS.md
    'codex': [
        ('AGENTS.md', '# Instruções para agentes\n\n' + CORE),
    ],
    # JetBrains AI Assistant e outras: arquivo de instruções em texto puro
    'jetbrains': [
        ('.aiassistant/rules/frontend-design-system.md', CORE),
    ],
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('projeto')
    p.add_argument('--ides', default='claude,cursor,copilot,windsurf,codex,jetbrains')
    a = p.parse_args()
    for ide in [i.strip() for i in a.ides.split(',') if i.strip()]:
        for rel, text in ADAPTERS[ide]:
            dst = os.path.join(a.projeto, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(dst) and ide == 'codex':
                # AGENTS.md pode já existir: acrescenta a seção em vez de sobrescrever
                with open(dst, 'a', encoding='utf8') as f:
                    f.write('\n\n' + text)
            else:
                open(dst, 'w', encoding='utf8').write(text)
            print('gerado:', rel)
    destino = os.path.join(a.projeto, 'scripts')
    os.makedirs(destino, exist_ok=True)
    shutil.copy(os.path.join(HERE, 'scripts', 'gera_indice.py'), os.path.join(destino, 'gera_indice.py'))
    print('gerado: scripts/gera_indice.py')
    print('pronto')


if __name__ == '__main__':
    main()
