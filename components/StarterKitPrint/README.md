# StarterKitPrint

Kit de impressão e documento com três modelos: **relatório institucional** (A4 paisagem), **declaração oficial** com número e código de validação (A4 retrato) e a **página do app** com as regras `@media print` reais aplicadas. O repositório não tem layout de impressão dedicado: os modelos seguem o que existe de verdade (colunas do `TabularExportService`, `@media print` do módulo padrão) e devem ser ajustados à view do módulo ao usar.

## Quando usar

- Relatório tabular para arquivar/enviar (lista de matrículas, inadimplência, frequência): variante "Relatório (A4 paisagem)", com o export PDF do servidor (`TabularExportService`, formato `pdf`) como origem dos dados.
- Usuário imprimindo a página do app com Ctrl+P: as regras `@media print` escondem a navegação e deixam o conteúdo em fundo branco — variante "Página do app impressa".
- Documento oficial com timbre, assinatura e numeração (declaração de matrícula, histórico, boletim assinado): variante "Declaração oficial (A4 retrato)". O repositório não tem esse documento; registre-o como view própria do módulo a partir deste modelo.
- Exportações não imprimíveis (CSV, XLSX, JSON, SQL…) → menu "Exportar" do [StarterKitAppShell](../StarterKitAppShell/README.md).

## O que existe no repositório (levantamento)

| Fonte | O que faz |
|---|---|
| `app/Services/TabularExportService.php::toPdf()` | monta HTML mínimo (`h1` verde `#10b981` + tabela 9px com bordas `#ccc`, cabeçalho `#f4f4f5`) e renderiza com dompdf, `setPaper('a4', 'landscape')`, `isRemoteEnabled=false` |
| `app/Services/AcademicTableExportService.php` | delega `pdf`, `csv`, `xlsx`… ao `TabularExportService`; `html` gera uma tabela sem estilo |
| `resources/views/app/pages/standard/module.php` | `@media print { aside, nav, header, .export-dd, .sstd-toolbar { display:none } .ttsc-dashboard-wrapper { padding:0 } }` |
| `assets/css/ttsc.financial-pages.css`, `ttsc.developer-integrations.css` | `@media print { body {background:#fff;color:#000} aside, nav, header, .print\:hidden {display:none} .ttsc-dashboard-wrapper {padding:0; margin:0; width:100%} canvas {max-width:100%; height:auto} }` |
| `assets/js/ttsc.export.js::generatePDF()` | PDF no cliente com jsPDF + autotable carregados de `cdnjs.cloudflare.com` (dependência externa; falha offline/CSP) |
| `window.print()` | nenhuma chamada no repo |

## Anatomia

```
PDF tabular (dompdf, A4 paisagem 297 × 210 mm)          Página do app impressa (@media print)
┌──────────────────────────────────────────────┐        ┌──────────────────────────────────────────────┐
│ Matrículas 2026 — Unidade Centro — 2026-10-22 12:23 │  │ (sem header, rail, sub-sidebar, abas, rodapé)  │
│ ┌──────────┬────────────┬───────┬────────┐   │        │ cabeçalho da página + banner                  │
│ │Matrícula │Aluno       │Turma  │ …      │   │        │ cartões KPI / tabela da visão ativa           │
│ ├──────────┼────────────┼───────┼────────┤   │        │ fundo branco, texto preto, canvas 100%        │
│ │MAT-…0142 │Pedro …     │9º A   │ …      │   │        └──────────────────────────────────────────────┘
└──────────────────────────────────────────────┘
```

| Parte | Origem | Obrigatório |
|---|---|---|
| Título com data | `h1` = `$title . ' — ' . date('Y-m-d H:i')` | sim |
| Tabela | `th` = `$headers`; `td` = valores projetados por cabeçalho, com `antiFormula()` | sim |
| Papel | dompdf `a4` `landscape` | sim |
| Ocultos na impressão | `aside`, `nav`, `header`, `.print:hidden`, `.export-dd`, `.sstd-toolbar` | sim |

## Variantes / Estados

| Variante (botão) | Arquivo do kit | Observação |
|---|---|---|
| Relatório (A4 paisagem) | `kit.html` | cabeçalho com marca e emissor, chips de filtros aplicados, faixa de 4 indicadores, tabela com cabeçalho repetido, status com texto e cor, total e assinaturas; rodapé com "Página X de Y" no `@page` |
| Declaração oficial (A4 retrato) | `kit-declaracao.html` | timbre, número e data, texto de declaração, dados em duas colunas, assinatura, bloco de validação com código e QR |
| Página do app impressa | `kit-app.html` | shell real com a visão KPI e as regras de impressão aplicadas como CSS de tela (`body.kit-print-preview`) dentro de uma folha de 297 mm |
| Tema | — | papel é sempre claro: os dois arquivos ignoram o tema do preview |
| Larguras | Tela 1440 / Tela 1024 | a folha mantém 297 mm e encolhe com `max-width: 100%` |

## API

| Ponto | Efeito |
|---|---|
| `(new TabularExportService())->build('pdf', $rows, $headers, ['title' => …, 'filename' => …])` | `['content' => binário PDF, 'filename' => slug-AAAAmmdd-HHiiss.pdf, 'mime' => 'application/pdf']` |
| `TabularExportService::FORMATS` | `csv`, `xlsx`, `pdf`, `json`, `xml`, `sql`, `txt` |
| `AcademicTableExportService::FORMATS` | os anteriores + `docx`, `html`, `md`, `tsv`, `yaml`, `ods`, `rtf`, `zip` |
| `TTSCExport.run('pdf', data, {columns, headers, pdfTitle})` (`ttsc.export.js`) | PDF no navegador (jsPDF via CDN) |
| classe `.print:hidden` | esconde qualquer bloco na impressão (nas páginas que carregam as folhas acima) |

## Acessibilidade

- PDF: título textual (não imagem), cabeçalhos de coluna em `th`; dompdf não gera PDF marcado (tagged) — para documentos oficiais acessíveis, ofereça também a versão HTML.
- Impressão: não dependa de cor para status (imprime em P&B) — mantenha o rótulo ("Ativa", "Trancada").
- Tamanho mínimo legível: 9px no PDF paisagem é o piso; documentos para pais/alunos devem usar 11–12px.

## Modelos

### HTML

Documento oficial a partir da folha do kit (view nova, renderizada pelo dompdf com `isRemoteEnabled=false` — imagens em `data:`):

```php
<?php // resources/views/app/documents/declaracao-matricula.php — usado com $engine->render(...) e Dompdf::loadHtml() ?>
<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<style>
  @page { size: A4 portrait; margin: 18mm 16mm; }
  body { font-family: DejaVu Sans, sans-serif; font-size: 11px; color: #111; }
  h1 { font-size: 15px; color: #10b981; margin: 0 0 4mm; }
  .timbre { border-bottom: 1px solid #ccc; padding-bottom: 4mm; margin-bottom: 8mm; }
  table { width: 100%; border-collapse: collapse; } th, td { border: 1px solid #ccc; padding: 3px 5px; text-align: left; } th { background: #f4f4f5; }
  .assinatura { margin-top: 24mm; text-align: center; } .assinatura span { display: inline-block; border-top: 1px solid #111; padding-top: 2mm; min-width: 70mm; }
</style></head>
<body>
  <div class="timbre"><strong><?= $this->e($escola['nome']) ?></strong> · CNPJ <?= $this->e($escola['cnpj']) ?> · <?= $this->e($unidade['nome']) ?></div>
  <h1>Declaração de Matrícula</h1>
  <p>Declaramos que <strong><?= $this->e($aluno['nome']) ?></strong> está regularmente matriculado(a) na turma
     <strong><?= $this->e($matricula['turma']) ?></strong> (<?= $this->e($matricula['curso']) ?>), turno <?= $this->e($matricula['turno']) ?>, no ano letivo de <?= (int) $periodo['ano'] ?>.</p>
  <table><tr><th>Matrícula</th><td><?= $this->e($matricula['codigo']) ?></td><th>Situação</th><td><?= $this->e($matricula['situacao']) ?></td></tr></table>
  <div class="assinatura"><span>Secretaria Escolar</span></div>
</body></html>
```

### CSS

Regras de impressão reais (copie para a folha do módulo) + extensão com tokens para a pré-visualização:

```css
@media print {
  body { background: #fff !important; color: #000 !important; }
  aside, nav, header, .print\:hidden, .export-dd, .sstd-toolbar { display: none !important; }
  .ttsc-dashboard-wrapper { padding: 0 !important; margin: 0 !important; width: 100% !important; }
  canvas { max-width: 100% !important; height: auto !important; }
  #main-viewport { overflow: visible !important; }           /* o shell rola por dentro: libere na impressão */
  .tb-card, #view-kpi .rounded-2xl { break-inside: avoid; }
}
/* pré-visualização na tela (como no kit-app.html) */
.print-sheet { width: 297mm; max-width: 100%; min-height: 210mm; margin: var(--ttsc-space-4) auto; padding: 12mm;
  background: #fff; color: #000; box-shadow: var(--ttsc-shadow-md); }
```

### JS

```js
// Botão "Imprimir" da página: abre a visão tabela, espera o layout e chama a impressão do navegador
(function () {
  document.addEventListener('click', function (e) {
    if (!e.target.closest('[data-action="print-page"]')) return;
    if (typeof window.switchDomainTab === 'function') window.switchDomainTab('table');
    document.documentElement.classList.add('is-printing');
    requestAnimationFrame(function () { setTimeout(function () { window.print(); }, 50); });
  });
  window.addEventListener('afterprint', function () { document.documentElement.classList.remove('is-printing'); });
})();
```

Para PDF, prefira o servidor (`TabularExportService`) ao `ttsc.export.js`, que depende do CDN do jsPDF.

### SQL

Exemplo das linhas que alimentam o PDF de matrículas (banco do **tenant**); os aliases viram os cabeçalhos da tabela:

```sql
SELECT e.code AS `Matrícula`, s.name AS `Aluno`, c.name AS `Turma`, co.name AS `Curso`,
       e.status AS `Situação`, e.enrollment_date AS `Data`
  FROM enrollments e
  LEFT JOIN users s    ON s.uuid = e.student_uuid
  LEFT JOIN classes c  ON c.uuid = e.class_uuid AND c.deleted_at IS NULL
  LEFT JOIN courses co ON co.uuid = e.course_uuid AND co.deleted_at IS NULL
 WHERE e.deleted_at IS NULL
   AND e.unit_uuid = :unit_uuid
 ORDER BY c.name, s.name;
```

O controller faz `fetchAll(PDO::FETCH_ASSOC)`, passa `array_keys($rows[0])` como `$headers` e devolve `build('pdf', …)['content']` com `Content-Type: application/pdf` e `Content-Disposition` pelo `filename` já higienizado. Como diz o próprio serviço, "callers must re-fetch and authorize their own domain projection": refaça a consulta com o escopo do usuário, nunca exporte o que veio do navegador.

## Como começar um projeto a partir do kit

1. **Arquivos do kit**: `kit.html` (HTML real do dompdf + moldura A4) e `kit-app.html` (shell real + `PRINT_SCREEN_CSS`); gerados por `$SPD/dsh/gen_kits.py`; o HTML do PDF vem de `php $SPD/app/mail_print_harness.php <saída>`.
2. **No repo**: relatórios tabulares → `TabularExportService::build('pdf', …)`; documentos com timbre → view nova + dompdf (`vendor/dompdf`), `isRemoteEnabled=false`.
3. **Outro projeto**: `composer require dompdf/dompdf`, copie `TabularExportService` (inclui `antiFormula()` e `slug()`) e as regras `@media print` acima para o CSS global.

## Faça / Não faça

- **Faça:** gere PDF no servidor com dados reconsultados e autorizados.
- **Faça:** marque com `.print:hidden` tudo que é controle (filtros, botões, paginação).
- **Não faça:** depender de CDN para gerar PDF (`ttsc.export.js` hoje carrega jsPDF de `cdnjs`).
- **Não faça:** imprimir o shell com `#main-viewport` rolando por dentro — sem `overflow: visible` só a primeira tela sai no papel.
