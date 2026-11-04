# 80 — Decisões tomadas por padrão (delegadas pelo autor)

> Parte do [SDD v2](00-README.md). Em 04/11/2026 o autor delegou as decisões em aberto: "sempre a melhor prática, mais segura, completa", sem bloquear o trabalho para perguntar.
> **Regra:** antes de decidir, o assunto é buscado em todo o SDD (v2 e [anexo-v1/](anexo-v1/)). Só entra aqui o que não está decidido em nenhum documento. Cada decisão tem motivo, alternativa descartada e onde se aplica. O autor pode revisar qualquer item; revisão vira nova linha, sem apagar a anterior.

## 1. Critérios usados

1. **Segurança e conformidade primeiro:** na dúvida, a opção que expõe menos dado, exige aprovação ou bloqueia o erro.
2. **Completude:** na dúvida entre incluir e excluir um recurso previsto na v1, incluir.
3. **Não inventar valor legal ou contábil:** prazo, alíquota, taxa e texto jurídico não são inventados. Ficam como parâmetro obrigatório, configurado pelo responsável, e o sistema bloqueia o uso enquanto não forem configurados.
4. **Separação de funções:** quem opera não aprova a própria operação ([78](78-permissoes-e-papeis.md), seção 2.2).

## 2. Decisões

| # | Assunto | Decisão | Motivo | Alternativa descartada | Onde se aplica |
|---|---|---|---|---|---|
| DP-01 | Frotas nesta versão (pendência do autor em [45](45-pendencias-consolidadas.md), seção 2) | **Entra nesta versão**, para a empresa e para as entidades | Completude; a especificação da v1 é completa e o transporte escolar é uso real | Deixar para versão futura | Portal do desenvolvedor (operações internas) e portal de gestão |
| DP-02 | Regra de depreciação por categoria (lacuna L-18 do [19](19-regras-modulos-3.md)) | Cada categoria de ativo tem método e taxa **aprovados pelo contábil**. Categoria sem regra aprovada **não deprecia** e aparece como pendência no painel | Critério 3: não inventar taxa contábil; não deixar ativo sem controle | Taxa padrão do sistema para todas as categorias | Patrimônio (empresa e entidade) |
| DP-03 | Papéis de patrimônio e frotas (não definidos no [22](22-crm-canais-e-papeis.md), seção 5) | Operador (nível 1) e aprovador (nível 2) separados, para patrimônio e para frotas. Compras, almoxarifado e aprovador de compras seguem o [22](22-crm-canais-e-papeis.md), seção 5 | Critério 4; mesmo padrão dos papéis departamentais já aprovados | Um único papel por módulo | [78](78-permissoes-e-papeis.md), seção 4.1 (plataforma) |
