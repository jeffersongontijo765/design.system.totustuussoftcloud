# LayoutVisaoGeral

Modelo de página para a visão geral acadêmica. Mostra como montar uma tela inteira com os componentes do painel: o cabeçalho com o índice de saúde, o funil de matrícula, os alunos em risco, a frequência por turma, as aprovações pendentes e a fila da secretaria.

## Quando usar

- Como ponto de partida para a página inicial de um portal de gestão (direção, secretaria).
- Como referência de ordem: do mais geral (índice e KPIs) para o mais específico (ações individuais).
- Não é um componente para reaproveitar tal qual: copie a estrutura e troque os dados pelos da página.

## Estrutura

```
┌──────────────────────────────────────────────────────────┐
│ HeroBanner: título, chips, índice de saúde e 4 KPIs      │
├──────────────────────────────┬───────────────────────────┤
│ FunnelBars: funil de matrícula│ RiskList: alunos em risco │
├──────────────────────────────┴───────────────────────────┤
│ HeatmapMatrix: frequência por turma e dia                │
├──────────────────────────────┬───────────────────────────┤
│ ApprovalQueue: aprovações    │ QueueList: fila da secretaria│
└──────────────────────────────┴───────────────────────────┘
```

| Bloco | Componente | Largura |
|---|---|---|
| Cabeçalho | [HeroBanner](../HeroBanner/README.md) | total |
| Funil e risco | [FunnelBars](../FunnelBars/README.md) + [RiskList](../RiskList/README.md) | 2 colunas |
| Frequência | [HeatmapMatrix](../HeatmapMatrix/README.md) | total |
| Ações pendentes | [ApprovalQueue](../ApprovalQueue/README.md) + [QueueList](../QueueList/README.md) | 2 colunas |

## Variantes / Estados

- **Abaixo de 900 px:** as duas colunas viram uma, na mesma ordem.
- **Sem permissão para aprovar:** remova o bloco de aprovações, não os botões.
- **Sem dados:** cada bloco usa o seu próprio estado vazio (ver [EmptyState](../EmptyState/README.md)).

## API

Este modelo não tem API própria. Cada bloco recebe os seus dados pela API do componente correspondente; a página só organiza a ordem e a largura.

| Classe | Papel |
|---|---|
| `.lay` | coluna principal, com espaçamento entre blocos |
| `.lay-2` | grade de duas colunas, em uma coluna no mobile |

## Acessibilidade

- A ordem no HTML é a ordem de leitura: cabeçalho, funil, risco, frequência, aprovações e fila.
- Cada bloco é uma `section` com `aria-labelledby`, então o leitor de tela anuncia o nome de cada área.

## Modelos

### HTML

```html
<div class="lay">
  <!-- HeroBanner -->
  <div class="lay-2">
    <!-- FunnelBars -->
    <!-- RiskList -->
  </div>
  <!-- HeatmapMatrix -->
  <div class="lay-2">
    <!-- ApprovalQueue -->
    <!-- QueueList -->
  </div>
</div>
```

### CSS

```css
.lay { display: grid; gap: 14px; }
.lay-2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
.lay-2 > * { min-width: 0; }
@media (max-width: 900px) { .lay-2 { grid-template-columns: 1fr; } }
```

`min-width: 0` evita que uma tabela ou uma grade largas empurrem a coluna para fora da tela.

### JS

Sem JavaScript próprio. Cada componente carrega os seus dados; a página só chama as funções de cada bloco:

```js
async function carregarVisaoGeral(periodo) {
  const [saude, funil, risco, frequencia, aprovacoes, fila] = await Promise.all([
    fetch(`/api/v1/visao-geral/saude?periodo=${periodo}`).then((r) => r.json()),
    fetch(`/api/v1/visao-geral/funil?periodo=${periodo}`).then((r) => r.json()),
    fetch(`/api/v1/visao-geral/risco?periodo=${periodo}`).then((r) => r.json()),
    fetch(`/api/v1/visao-geral/frequencia?periodo=${periodo}`).then((r) => r.json()),
    fetch('/api/v1/aprovacoes?status=pending').then((r) => r.json()),
    fetch('/api/v1/central/fila?status=aberto').then((r) => r.json()),
  ]);
  // cada resposta alimenta a função de render do seu componente
  return { saude, funil, risco, frequencia, aprovacoes, fila };
}
```

As rotas acima são ilustrativas: confirme as rotas reais em `routes/` antes de usar.

### SQL

Este modelo não tem consulta própria. Cada bloco usa a consulta do seu componente (ver o README de cada um):

- [HeroBanner](../HeroBanner/README.md): matrículas ativas e frequência média.
- [FunnelBars](../FunnelBars/README.md): inscritos, aprovados e matriculados.
- [RiskList](../RiskList/README.md): faltas por matrícula acima do limite.
- [HeatmapMatrix](../HeatmapMatrix/README.md): presença por turma e dia da semana.
- [ApprovalQueue](../ApprovalQueue/README.md): aprovações pendentes.
- [QueueList](../QueueList/README.md): atendimentos em aberto.

## Faça / Não faça

- Faça: mantenha o cabeçalho no topo e os blocos de ação no fim, para que a leitura siga do geral para o específico.
- Faça: use o mesmo período em todos os blocos e mostre-o no cabeçalho.
- Não faça: colocar mais de seis blocos numa página; o resto vai para páginas próprias.
- Não faça: repetir o mesmo número em dois blocos com fontes diferentes.
