"""Executa todo o DDL do SDD v2 num MariaDB ou MySQL e informa tabelas criadas e erros.

Uso: python3 inventario/valida_ddl.py --socket /caminho/mysql.sock
     (servidor com --character-set-server=utf8mb4; cada documento vira um banco de teste `ddl_NN`)
Lê os blocos ```sql com CREATE TABLE de docs/v2/NN-*.md. Sai com código 1 se houver erro.
"""
import argparse, glob, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ap = argparse.ArgumentParser()
ap.add_argument('--socket', required=True)
ap.add_argument('--cliente', default='mariadb')
a = ap.parse_args()
total = criadas = erros = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'docs', 'v2', '[0-9][0-9]-*.md'))):
    blocos = [b for b in re.findall(r'```sql\n(.*?)```', open(f, encoding='utf8').read(), re.S) if 'CREATE TABLE' in b]
    if not blocos:
        continue
    db = 'ddl_' + os.path.basename(f)[:2]
    sql = f'DROP DATABASE IF EXISTS {db}; CREATE DATABASE {db}; USE {db};\n' + '\n'.join(blocos) + f'\nDROP DATABASE {db};'
    r = subprocess.run([a.cliente, '--socket=' + a.socket, '--force', '--default-character-set=utf8mb4'], input=sql.replace(f'\nDROP DATABASE {db};', f'\nSELECT COUNT(*) FROM information_schema.tables WHERE table_schema=\'{db}\';\nDROP DATABASE {db};'), capture_output=True, text=True)
    e = [l for l in r.stderr.splitlines() if l.startswith('ERROR')]
    n = sum(b.count('CREATE TABLE') for b in blocos)
    c = int((re.findall(r'^(\d+)$', r.stdout, re.M) or ['0'])[-1])
    total += n; criadas += c; erros += len(e)
    print(f'{os.path.basename(f)[:48]:48} CREATE {n:3}  criadas {c:3}  erros {len(e)}')
    for x in e[:5]:
        print('    ', x[:200])
print(f'TOTAL: {total} CREATE TABLE, {criadas} criadas, {erros} erros')
sys.exit(1 if erros else 0)
