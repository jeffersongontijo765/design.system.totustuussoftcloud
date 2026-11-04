"""Confere o DDL do SDD v2 contra as convenções da própria v2 e lista o que diverge.

Uso: python3 inventario/lint_ddl.py [--detalhe]
Regras verificadas (fonte entre parênteses):
  R1  tabela principal tem `uuid` (convenção do 51)
  R2  tabela principal tem `unidade_uuid`, ou é filha de outra (coluna *_uuid que aponta para o pai) (03, D-16)
  R3  tabela principal sem `deleted_at` (informativo: pelo DP-09 do 80, ela não aceita exclusão; o owner decide se precisa)
  R4  ENGINE=InnoDB e CHARSET=utf8mb4 (convenção do 51)
  R5  valor monetário em centavos inteiros (BIGINT ... _centavos), não DECIMAL (20, seção 4; convenção do 51)
  R6  horário em DATETIME(3), em UTC (convenção do 51)
Tabela "filha" = sem `uuid` próprio ou com chave primária composta: R1 e R3 não se aplicam.
É um apoio à revisão do owner: cada aviso precisa de leitura humana antes de mudar o DDL.
"""
import glob, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DINHEIRO = re.compile(r'(valor|preco|preço|total|salario|salário|orcamento|gasto|custo|tarifa|multa|juros|desconto|saldo)', re.I)


def tabelas():
    for f in sorted(glob.glob(os.path.join(ROOT, 'docs', 'v2', '[0-9][0-9]-*.md'))):
        texto = open(f, encoding='utf8').read()
        for bloco in re.findall(r'```sql\n(.*?)```', texto, re.S):
            for m in re.finditer(r'CREATE TABLE\s+(\w+)\s*\((.*?)\n\)\s*([^;]*);', bloco, re.S):
                yield os.path.basename(f)[:2], m.group(1), m.group(2), m.group(3)


def colunas(corpo):
    cols = {}
    for linha in corpo.splitlines():
        linha = linha.split('--')[0].strip().rstrip(',')
        m = re.match(r'^(\w+)\s+([A-Z]+(?:\([^)]*\))?)', linha)
        if m and m.group(1).upper() not in ('PRIMARY', 'UNIQUE', 'INDEX', 'KEY', 'CONSTRAINT', 'FOREIGN', 'CHECK'):
            cols[m.group(1)] = m.group(2)
    return cols


def main():
    detalhe = '--detalhe' in sys.argv
    avisos = {}
    total = 0
    for doc, nome, corpo, opcoes in tabelas():
        total += 1
        cols = colunas(corpo)
        filha = 'uuid' not in cols or bool(re.search(r'PRIMARY KEY\s*\(\s*\w+\s*,', corpo))
        pai = [c for c in cols if (c.endswith('_uuid') or c.endswith('_id')) and c not in ('unidade_uuid', 'id')]
        regra = []
        if not filha and 'uuid' not in cols:
            regra.append('R1')
        if 'unidade_uuid' not in cols and not pai and 'unidade_id' not in cols:
            regra.append('R2')
        so_inclusao = re.search(r'(evento|versao|versoes|acesso|log|historico|ledger|resposta|outbox|processed|fragmento|scan|derivative|exportac|erro|rejeic|digitaliz|entrega|doacao|movimenta|marcac|partida|itens?$|apurac|retenc)', nome)
        if not filha and 'deleted_at' not in cols and not so_inclusao:
            regra.append('R3')
        if 'InnoDB' not in opcoes or 'utf8mb4' not in opcoes:
            regra.append('R4')
        for c, t in cols.items():
            if DINHEIRO.search(c) and t.startswith('DECIMAL') and not re.search(r'(pct|percent|nota|score|peso|referencia|aliquota|taxa|valor_numero)', c) and not nome.startswith(('dia_notas', 'cpf_')):
                regra.append(f'R5:{c}')
            if t == 'DATETIME':
                regra.append(f'R6:{c}')
        if regra:
            avisos[(doc, nome)] = regra
    por_regra = {}
    for (doc, nome), rs in avisos.items():
        for r in rs:
            por_regra.setdefault(r.split(':')[0], []).append(f'{doc}:{nome}' + (f'.{r.split(":")[1]}' if ':' in r else ''))
    print(f'tabelas lidas: {total} | tabelas com aviso: {len(avisos)} (R3 é informativo, coberto pelo DP-09)')
    for r in sorted(por_regra):
        print(f'{r}: {len(por_regra[r])}')
        if detalhe:
            for x in por_regra[r]:
                print('   ', x, flush=True)


if __name__ == '__main__':
    main()
