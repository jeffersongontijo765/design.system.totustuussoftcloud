# StarterKitPortalStudent

Kit dos portais de pessoas (aluno, responsável, professor, terceiros): o mesmo `app/layouts/main.php` do shell administrativo, trocando o rail e o sub-sidebar do portal, com a visão KPI real de uma página de cada portal renderizada contra o banco `tenant_test`.

## Quando usar

- Qualquer página de `/student/*`, `/parents/*`, `/teacher/*` ou `/thirdparty/*`: o layout é o mesmo do admin; muda `railKey` (`student`, `guardian`, `teacher`, `third-party`) e o módulo do sub-sidebar.
- Página que mostra só os dados da conta logada (minhas aulas, notas do dependente, entregas do terceirizado) — o escopo vem da sessão (`$_SESSION['user_portal']`, `user_uuid`) e do `PortalDomainDataService`.
- Telas administrativas da instituição → [StarterKitAppShell](../StarterKitAppShell/README.md). Antes do login (escolher portal, `/login-student`) → [StarterKitAuth](../StarterKitAuth/README.md).

## Anatomia

```
header (mesmo header.php; avatar com a inicial do usuário do portal)
rail do portal  │ sub-sidebar do portal (ex.: "Portal do Aluno · Painel do Aluno", grupo ATIVIDADE DIÁRIA)
(railKey)       │ main#main-viewport
                │   cabeçalho "Espaço de Trabalho — Próximas Aulas" + breadcrumb "Portal do Aluno / Próximas Aulas"
                │   banner de contexto ("Banco ativo (2 registros)")
                │   abas KPI · Tabela · Cartões · Kanban · Analytics
                │   #view-kpi: 4 cartões (total, status predominante, requer atenção, atividade) + distribuição + destaques
footer
```

| Portal | Rota do kit | `railKey` | Login | Página inicial |
|---|---|---|---|---|
| Aluno | `/student/next-lessons` | `student` | `/login-student` | `/student/dashboard` |
| Responsável | `/parents/classroom/classes` | `guardian` (aceita `parents`) | `/login-parents` | `/parents/dashboard` |
| Professor | `/teacher/diary/assessments` | `teacher` | `/login-teacher` | `/teacher/dashboard` |
| Terceiros | `/thirdparty/delivery/approvals` | `third-party` (aceita `thirdparty`) | `/login-thirdparty` | `/thirdparty/dashboard` |

(Tabela de `App\Support\PortalNavigation::PORTALS` e `SidebarRouter`.)

| Parte | Origem real | Obrigatório |
|---|---|---|
| Layout | `app/layouts/main.php` | sim |
| Rail do portal | `app/partials/rail.php` com `railKey` do portal (`aria-label="Portal do Aluno"`) | sim |
| Sub-sidebar | `app/partials/sub_sidebar.php`, módulo resolvido por `SidebarRouter::moduleFor()` | sim |
| Corpo | `app/partials/chassis/domain_page.php` (`$pageRoute`, `$pageRail`) | páginas de domínio |
| Dados | `App\Services\Portal\PortalDomainDataService::getDataForRoute($route, $tenantId)` | sim |

## Variantes / Estados

| Variante | Botão no preview | Observação |
|---|---|---|
| Aluno | Aluno | sub-sidebar curto (grupo "Atividade diária"), avatar "S" |
| Responsável | Responsável | sub-sidebar "Ensino e Acadêmico · Dependentes e Acadêmico" com 8 grupos (Sala de aula, Diário escolar, Entradas e saídas, Eventos…) |
| Professor | Professor | Diário (avaliações, atividades, frequência) |
| Terceiros | Terceiros | Entregas, aprovações, evidências |
| Sem dados | — | `PortalDomainDataService` responde `http_status 503` ("Domain data is unavailable") e o chassi mostra o estado indisponível |
| Responsivo | Desktop/Tablet/Mobile | idêntico ao shell: gavetas em ≤ 1099px, abas excedentes em "Mais +N" |

Os painéis `/<portal>/dashboard` usam `app/partials/portal/dashboard_workspace.php`, que espera `$dashboard` do controller do painel (`StudentDashboardController` etc.); pelo harness de render (sem controller) eles não montam, por isso o kit usa páginas de domínio de cada portal. Rotas como `/parents/family-overview` ou `/teacher/today` aparecem no `SidebarRouter` mas devolvem 404 do manifesto de páginas.

## API

| Ponto | Efeito |
|---|---|
| `$_SESSION['user_portal']` ∈ `admin`, `developer`, `teacher`, `student`, `parents`, `thirdparty` | escopo do `PortalDomainDataService` e do `PerPageKpiController` (rail → portal, senão 403) |
| `layout('app::layouts/main', ['railKey' => 'student'])` | rail do portal |
| `PortalDomainDataService::getDataForRoute($route, $tenantId)` | array com `available`, `http_status`, `message`, `totalRecords`, `records`, `kpiCards`, `statusCounts` |
| `switchDomainTab(tab)` + evento `ttsc:domain-tab` | igual ao shell |
| Seletor de dependente (responsável) | os dados do portal do responsável são filtrados pelos alunos de `guardians_associations` |

## Acessibilidade

- O rail anuncia o portal (`aria-label="Portal do Aluno"`), e o breadcrumb começa pelo nome do portal — o usuário sabe em que portal está.
- Linguagem do público: rótulos curtos ("Próximas Aulas", "Avisos Recentes"); números grandes com rótulo textual, nunca só cor (os chips de status trazem texto: "2 Manhã", "0 Tarde").
- Para responsáveis com mais de um dependente, o nome do aluno ativo precisa estar visível no cabeçalho, não só no seletor.
- Alvos de toque de 44px no mobile (≤ 767px) — portais de aluno e responsável são majoritariamente usados no celular.

## Modelos

### HTML

```php
<?php
// resources/views/app/pages/student/boletim.php — página do portal do aluno
$pageRoute = '/student/report-card';
$pageRail = 'student';
$pageModule = 'Portal do Aluno';
$title = 'Boletim — 1º Bimestre';
$description = 'Notas e frequência por componente curricular.';
$icon = 'fa-light fa-file-certificate';
$breadcrumb = [
    ['label' => 'Portal do Aluno', 'url' => url('/student/dashboard')],
    ['label' => 'Boletim', 'url' => url('/student/report-card')],
];
$this->layout('app::layouts/main', [
    'title' => $title, 'description' => $description, 'icon' => $icon, 'breadcrumb' => $breadcrumb,
    'pageHasHeader' => true,
    'railKey' => 'student',
]);
include base_path('resources/views/app/partials/chassis/domain_page.php');
```

Responsável com dependente ativo no banner (dentro de `section('content')`):

```html
<div class="bg-emerald-50/70 border border-emerald-200/80 rounded-2xl p-4 flex items-center justify-between gap-3">
  <div class="flex items-center gap-3 min-w-0">
    <span class="w-10 h-10 rounded-xl bg-white border border-emerald-200 flex items-center justify-center text-emerald-700 font-semibold" aria-hidden="true">PA</span>
    <div class="min-w-0">
      <h2 class="text-base font-semibold text-slate-800">Pedro Albuquerque · 9º ano A</h2>
      <p class="text-xs text-slate-500">Matrícula MAT-2026-0142 · Ensino Fundamental II · Manhã</p>
    </div>
  </div>
  <button type="button" class="ttsc-btn ttsc-btn-outline ttsc-btn-sm" data-drawer-trigger="drawer-dependents">
    <i class="fa-light fa-arrows-repeat text-xs" aria-hidden="true"></i><span>Trocar dependente</span>
  </button>
</div>
```

### CSS

Nada novo: os portais usam o mesmo CSS do shell (lista no [StarterKitAppShell](../StarterKitAppShell/README.md#css)). Extensão para o cartão do dependente com tokens:

```css
.portal-dependent { display: flex; align-items: center; gap: var(--ttsc-space-3); padding: var(--ttsc-space-4);
  background: var(--ttsc-accent-soft); border: 1px solid var(--ttsc-accent-border); border-radius: var(--ttsc-radius-surface); }
.portal-dependent__name { color: var(--ttsc-text); font-weight: 600; }
.portal-dependent__meta { color: var(--ttsc-text-muted); font-size: 12px; }
@media (max-width: 767px) { .portal-dependent { flex-wrap: wrap; } .portal-dependent .ttsc-btn { min-height: 44px; width: 100%; } }
```

### JS

```js
// Troca do dependente ativo (portal do responsável): grava na sessão e recarrega a página do portal
(function () {
  document.addEventListener('click', function (e) {
    var item = e.target.closest('[data-dependent-uuid]');
    if (!item) return;
    e.preventDefault();
    item.setAttribute('aria-busy', 'true');
    fetch(document.querySelector('base').href + 'parents/api/active-dependent', {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content },
      body: JSON.stringify({ student_uuid: item.dataset.dependentUuid })
    })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); location.reload(); })
      .catch(function (err) {
        item.removeAttribute('aria-busy');
        window.showToast && window.showToast('Não foi possível trocar o dependente: ' + err.message, 'error', 'Portal do Responsável');
      });
  });
})();
```

O endpoint `parents/api/active-dependent` é o contrato sugerido para a troca; o kit não o chama.

### SQL

Banco do **tenant**. O PHP põe o resultado na sessão (dependente ativo) e no banner; o `PortalDomainDataService` filtra as consultas da página pelo aluno ativo.

```sql
-- 1) Dependentes do responsável logado (seletor do portal do responsável)
SELECT ga.student_user_uuid, s.name AS student_name, ga.relationship, ga.is_primary
  FROM guardians_associations ga
  JOIN users s ON s.uuid = ga.student_user_uuid AND s.deleted_at IS NULL AND s.status = 'active'
 WHERE ga.guardian_user_uuid = :guardian_uuid
   AND ga.status = 'active'
 ORDER BY ga.is_primary DESC, s.name;

-- 2) Matrícula vigente do aluno (cabeçalho/banner do portal do aluno e do responsável)
SELECT e.uuid, e.code, e.status, e.shift, e.enrollment_date, e.class_uuid, e.course_uuid, p.name AS period_name
  FROM enrollments e
  LEFT JOIN academic_periods p ON p.uuid = e.period_uuid AND p.deleted_at IS NULL
 WHERE e.student_uuid = :student_uuid
   AND e.deleted_at IS NULL
 ORDER BY (p.is_current = 1) DESC, e.enrollment_date DESC
 LIMIT 1;
```

Header, unidades, período e selo de notificações: as mesmas consultas do [StarterKitAppShell](../StarterKitAppShell/README.md#sql).

## Como começar um projeto a partir do kit

1. **Arquivos do kit**: `kit.html` (aluno), `kit-parents.html`, `kit-teacher.html`, `kit-thirdparty.html` + `preview.html`; gerados por `$SPD/dsh/gen_kits.py` a partir de `php $SPD/app/render_harness.php /student/next-lessons /parents/classroom/classes /teacher/diary/assessments /thirdparty/delivery/approvals` (o harness abre uma sessão por portal pelo primeiro segmento da rota).
2. **Nova página de portal**: view em `resources/views/app/pages/<student|parents|teacher|thirdparty>/…`, entrada no manifesto de páginas e item no sub-sidebar do portal; `railKey` do portal.
3. **Outro projeto**: os mesmos arquivos do [StarterKitAppShell](../StarterKitAppShell/README.md#como-começar-um-projeto-a-partir-do-kit), mais `App\Support\PortalNavigation` (mapa portal → login/home/banco) e `SidebarRouter` (prefixo da URL → rail).

## Faça / Não faça

- **Faça:** um único layout para todos os portais; diferencie por `railKey`, sub-sidebar e dados.
- **Faça:** derive o escopo (aluno, dependente, terceiro) da sessão no servidor — nunca de um parâmetro da URL.
- **Faça:** trate `available = false` (503) com o estado indisponível do chassi, sem esconder a página.
- **Não faça:** reutilizar páginas do admin no portal com CSS escondendo colunas — crie a página do portal.
- **Não faça:** mostrar dados de outro dependente ou de outra turma por cache de página compartilhado entre usuários.
