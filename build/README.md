# Build do design system

Fonte do template **TotusTuus SoftCloud** publicado como artefato Design System. As páginas (`../components/<Comp>/README.md` + `preview.html`), os tokens (`../tokens.json`), o brand book (`../README.md`) e o inventário (`../Inventario.md`) ficam versionados aqui. O que é gerado ou vendorizado fica fora do git.

| Arquivo do artefato | Como é gerado |
|---|---|
| `paginas/**/*.html` | `python3 gen_paginas.py`. Uma página por tela das fichas do kit-starter (seção 3). Cada página carrega `components/bundle.js` e chama `TTSCModelKit.render` com uma especificação no formato de `models/academico.json`: campos, status, KPIs, Kanban, Analytics, gaveta e formulário, com os campos do domínio do módulo. Precisa de `components/__tokens.css` e de `fonts/fa-light-300.woff2` (fora do git). |
| `components/bundle.css` | `python3 build_bundle.py <repo> <projeto>`. A camada REAL do app na ordem de `resources/views/app/layouts/main.php` (`assets/css/ttsc.*.css`, Font Awesome, DataTables) mais Kanban, Analytics e `extra.css`. |
| `components/bundle.js` | Mesmo comando. Leva o ttscui (só para as páginas que o documentam; **o app não carrega o ttscui**), Chart.js, `ttsc.chart-defaults/kanban-board/analytics-panels` e os motores do shell (`ttsc.js`, `events`, `tabs-overflow`, `sidebar`, `drawer`, `select`, `pagination`, `datepicker`, `notifications`, `overlays`, `shell`, `workspace-search`). No app esses motores ficam no fim do `<body>`; no frame o bundle está no `<head>`, então eles rodam no `DOMContentLoaded` (eval global) e os listeners de `DOMContentLoaded` que registram são chamados em seguida. Também lê o `TTSCModelKit` de `vendor/app/app.js` (gerado por `build_app.py`). |
| `fonts/fa-light-300.woff2` | Cópia de `assets/fonts/fontawesome.v7.2.0/webfonts/`. |
| `vendor/**` | Pacotes originais do npm nas versões do repo. **ApexCharts 4.7.0, TinyMCE 8.3.2, FullCalendar 6.1.20, DataTables 2.3.7 e Dropzone 5.9.3 NÃO podem ser copiados de `assets/vendors/`**: a troca global `kt`→`ttsc` corrompeu essas cópias (ex.: `isDesktop` → `isDesttscop`, "Identifier 'ttsc' has already been declared"). |

## Modelos aprovados, widgets e site de documentação

| Peça | Como é gerada |
|---|---|
| `vendor/app/app.js` (entrada do `build_bundle.py`) | `python3 build_app.py <repo> <saida>/vendor/app`. Os previews não carregam mais `vendor/app`; o conteúdo entrou no `bundle`. CSS e JS reais do app (`assets/css`, `assets/js`), na ordem de `docs/model/app/developer.html`, mais `TTSCModelKit`. O kit traz os renderizadores de `docs/model/app/_assets/model-page.js` sem shell e sem rota, com os rótulos em pt-BR do `dashboard.php`. |
| `vendor/app/widgets/` | Cópia de `docs/model/widgets/{widgets.css,widgets.js}`. |
| `models/academico.json` | Ficha de página no formato de `docs/model/app/specs`. Alimenta os modelos e os arquétipos. |
| `components/{PageModel,…,KanbanBoard,…}/preview.html` | `python3 gen_models.py <saida>`. |
| `components/Widget*/preview.html` | `python3 gen_widgets.py <repo> <saida> 'Nome\|w:widget\|t:subtítulo' …`. Cada página carrega o catálogo inteiro, porque `widgets.js` atualiza todos os widgets, e mostra só o próprio widget. |
| Site de documentação (`../site/index.html` + `docs.json`) | `python3 gen_site.py <projeto> <saida>`. Gera um preview por página e o `docs.json` com as abas Visão geral, HTML, CSS, JS, API e SQL, extraídas de cada README. |

## Páginas a partir de renders reais

| Peça | Como é gerada |
|---|---|
| `components/Navigation/{preview.html, shell.html}` | `php build/render_page.php /academic/enrollment/re-enrollment` (na raiz do repo) e `python3 gen_nav.py /tmp/render_academic_enrollment_re-enrollment.html <projeto>/components/Navigation/preview.html`. O `shell.html` é o header, o rail e o sub-sidebar de `main.php`; o preview o mostra numa largura real (1440, 1024, 390) porque abaixo de 1100px o sub-sidebar vira gaveta. |
| `components/StarterKit*/` | `DS_WORK=<pasta> python3 gen_kits.py [Kit …]`. Renders reais de `app/layouts/main.php` (`render_page.php` em `/academic/enrollment/re-enrollment`, `/student/next-lessons`, `/parents/classroom/classes`, `/teacher/diary/assessments`, `/thirdparty/delivery/approvals`, copiados para `$DS_WORK/kits/r_shell_<rota>.html`), `auth`, `errors`, `web` e `install` (`view_harness.php`, pelo motor de views do app, em `$DS_WORK/kits/r_*.html`) e de e-mails e PDF (`mail_print_harness.php`). |
| Render do `domain_page` (diagnóstico) | `php build/render_domain.php <rota> <saida.html>` e `gen_real.py`. Registros ilustrativos só em memória; nada é gravado no banco. |

## Verificação

`build_frames.py` monta, para cada `preview.html`, um frame igual ao do artefato: `tokens.css` compilado de `tokens.json`, `bundle.css`, `bundle.js`, temas `light` e `dark`. `shoot.js` (Playwright/Chromium) abre cada frame, registra erros de JS, falhas de rede e respostas 4xx, e salva screenshots. Uma página só entra no sistema com zero erros nos dois temas.
