# Stepper

Assistente em etapas (`data-ttsc-stepper`, ttscui) que mostra um passo por vez, marca os passos concluídos e permite validar antes de avançar — ex.: wizard de matrícula (dados do aluno → curso/turma → financeiro → confirmação).

> Também listado em: **Geral › Stepper**.

## Quando usar

- Processos de 3 a 6 etapas com dependência entre elas: nova matrícula, rematrícula, importação de alunos, abertura de período letivo.
- Dentro de [Drawer](../Drawer/README.md) `lg` ou de página dedicada; o envio acontece só no último passo.
- **Não use** para seções independentes que o usuário consulta em qualquer ordem: use [Tabs](../Tabs/README.md).
- **Não use** para mostrar a posição na hierarquia de páginas: use [Breadcrumb](../Breadcrumb/README.md).
- Formulário curto (até ~8 campos): um único [Forms](../Forms/README.md) é mais rápido.

## Anatomia

```
 (✓)────────(2)────────(3)────────(4)
 Dados      Curso e    Financeiro  Confirmação     ← [data-ttsc-stepper-item="#step-…"]
 do aluno   turma                                     .completed / .active / .pending
┌──────────────────────────────────────────────┐
│ conteúdo do passo ativo (#step-course)        │  ← os demais recebem .hidden
└──────────────────────────────────────────────┘
 [Voltar]                         [Avançar] / [Confirmar matrícula]
 data-ttsc-stepper-back           data-ttsc-stepper-next
```

| Parte | Classe / atributo | Obrigatório |
|---|---|---|
| Raiz | `[data-ttsc-stepper="true"]` — recebe `first` / `between` / `last` | sim |
| Indicador do passo | `[data-ttsc-stepper-item="#conteudo"]` — recebe `active` / `completed` / `pending` | sim |
| Número | `[data-ttsc-stepper-number]` dentro do item — o JS escreve 1, 2, 3… | não |
| Conteúdo | elemento apontado pelo item; recebe `hiddenClass` quando inativo | sim |
| Avançar | `[data-ttsc-stepper-next]` (só o **primeiro** encontrado é ligado) | sim (sem ele o JS loga erro) |
| Voltar | `[data-ttsc-stepper-back]` (só o primeiro) | não |
| Concluir | botão `type="submit"` comum, mostrado via `.last` | sim |

## Estados

| Estado | Onde | Visual | Tokens |
|---|---|---|---|
| `pending` | item | círculo vazado, rótulo apagado | borda `ttsc-border-strong`, texto `ttsc-text-muted` |
| `active` | item | círculo preenchido, rótulo forte | fundo `ttsc-accent`, número `ttsc-accent-on`, rótulo `ttsc-text` |
| `completed` | item | círculo com check, linha verde | fundo `ttsc-accent-soft`, ícone `ttsc-accent-text`, linha `ttsc-accent` |
| `first` | raiz | esconde “Voltar” | — |
| `between` | raiz | mostra os dois botões | — |
| `last` | raiz | troca “Avançar” por “Confirmar matrícula” | — |
| Erro no passo | campo | `aria-invalid="true"` + mensagem (ver [Forms](../Forms/README.md)) | `ttsc-danger-text` |

## API

Conferida em `src/components/stepper/stepper.ts`. Opções por `data-ttsc-stepper-<opção>` na raiz ou objeto no construtor.

| Opção | Atributo | Padrão | Descrição |
|---|---|---|---|
| `activeStep` | `data-ttsc-stepper-active-step` | `1` | passo inicial (1-based) |
| `hiddenClass` | `data-ttsc-stepper-hidden-class` | `"hidden"` | classe aplicada aos conteúdos inativos |

| Método | Descrição |
|---|---|
| `ttscStepper.getInstance(el)` / `getOrCreateInstance(el, cfg)` | instância |
| `go(n)` | vai para o passo `n` (dispara `change` cancelável) |
| `goNext()` / `goBack()` / `goFirst()` / `goLast()` | navegação |
| `getStep(itemEl)` | número do passo de um item |
| `getItemElement(n)` / `getItemElements()` / `getTotalSteps()` | consulta (só itens visíveis contam) |
| `isFirst()` | `true` no passo 1 |
| `update()` | reaplica classes (após mostrar/esconder itens) |
| `on('change', fn)` / `on('changed', fn)` | callbacks; `fn(payload)` pode pôr `payload.cancel = true` |

Atenção ao build atual: `goTo(itemEl)` chama a si mesmo (recursão) e `isLast()` compara com `activeStep + 1` — use `go(getStep(item))` e `getTotalSteps() === passoAtual`.

| Evento (DOM, na raiz) | `detail.payload` | Cancelável |
|---|---|---|
| `change` | `{ step, cancel }` — `step` é o destino | sim: `payload.cancel = true` |
| `changed` | `null` | não |

O evento DOM se chama `change` e **borbulha**: `change` de inputs dentro do wizard também chegam à raiz. Filtre por `event.detail?.payload`.

## Acessibilidade

- Indicadores em `<ol aria-label="Etapas da matrícula">`; o item ativo recebe `aria-current="step"` (listener `changed`, ver JS).
- Cada conteúdo é `<section role="group" aria-labelledby>` com o título do passo; ao trocar, mova o foco para esse título (`tabindex="-1"`).
- Erros de validação ficam no próprio passo, com `aria-invalid` e mensagem `role="alert"`; o avanço é cancelado, nunca silencioso.
- Indicadores clicáveis só para passos já concluídos; passos pendentes não são botões.
- Contraste: número ativo `ttsc-accent-on` sobre `ttsc-accent` (9,6:1); rótulos pendentes `ttsc-text-muted` (4,9:1).

## Modelos

### HTML

```html
<form id="enrollment-wizard" method="post" action="/academic/enrollments" data-ttsc-stepper="true" class="ttsc-stepper">
  <input type="hidden" name="_token" value="<?= $this->e($csrf) ?>">

  <ol class="ttsc-stepper-nav" aria-label="Etapas da matrícula">
    <li class="ttsc-stepper-item" data-ttsc-stepper-item="#step-student">
      <span class="ttsc-stepper-dot"><span data-ttsc-stepper-number>1</span><i class="fa-light fa-check"></i></span>
      <span class="ttsc-stepper-label">Dados do aluno</span>
    </li>
    <li class="ttsc-stepper-item" data-ttsc-stepper-item="#step-course">
      <span class="ttsc-stepper-dot"><span data-ttsc-stepper-number>2</span><i class="fa-light fa-check"></i></span>
      <span class="ttsc-stepper-label">Curso e turma</span>
    </li>
    <li class="ttsc-stepper-item" data-ttsc-stepper-item="#step-billing">
      <span class="ttsc-stepper-dot"><span data-ttsc-stepper-number>3</span><i class="fa-light fa-check"></i></span>
      <span class="ttsc-stepper-label">Financeiro</span>
    </li>
    <li class="ttsc-stepper-item" data-ttsc-stepper-item="#step-confirm">
      <span class="ttsc-stepper-dot"><span data-ttsc-stepper-number>4</span><i class="fa-light fa-check"></i></span>
      <span class="ttsc-stepper-label">Confirmação</span>
    </li>
  </ol>

  <section id="step-student" role="group" aria-labelledby="h-student">
    <h3 id="h-student" tabindex="-1">Dados do aluno</h3>
    <div class="ttsc-form-item">
      <label class="ttsc-form-label" for="student_cpf">CPF</label>
      <input class="ttsc-input" id="student_cpf" name="student_cpf" required data-mask="cpf">
      <div class="ttsc-form-message" role="alert">Informe um CPF válido.</div>
    </div>
  </section>
  <section id="step-course" class="hidden" role="group" aria-labelledby="h-course">
    <h3 id="h-course" tabindex="-1">Curso e turma</h3>
    <select class="ttsc-select" name="class_uuid" required>
      <?php foreach ($classes as $cl): ?>
        <option value="<?= $this->e($cl['uuid']) ?>"><?= $this->e($cl['code']) ?> — <?= (int) $cl['seats_left'] ?> vagas</option>
      <?php endforeach ?>
    </select>
  </section>
  <section id="step-billing" class="hidden" role="group" aria-labelledby="h-billing">…</section>
  <section id="step-confirm" class="hidden" role="group" aria-labelledby="h-confirm">…</section>

  <div class="ttsc-form-actions ttsc-stepper-actions">
    <button type="button" class="ttsc-btn ttsc-btn-ghost" data-ttsc-stepper-back><i class="fa-light fa-arrow-left"></i> Voltar</button>
    <button type="button" class="ttsc-btn ttsc-btn-primary" data-ttsc-stepper-next>Avançar <i class="fa-light fa-arrow-right"></i></button>
    <button type="submit" class="ttsc-btn ttsc-btn-primary ttsc-stepper-submit"><i class="fa-light fa-check"></i> Confirmar matrícula</button>
  </div>
</form>
```

### CSS

O runtime não traz classes visuais de stepper (só o comportamento); extensão do chassi com tokens:

```css
.ttsc-stepper-nav { display: flex; list-style: none; margin: 0 0 var(--ttsc-space-6); padding: 0; }
.ttsc-stepper-item { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 6px; position: relative; text-align: center; }
.ttsc-stepper-item:not(:last-child)::after {
  content: ""; position: absolute; top: 14px; inset-inline-start: calc(50% + 18px); inset-inline-end: calc(-50% + 18px);
  height: 2px; background: var(--ttsc-border); border-radius: var(--ttsc-radius-pill);
}
.ttsc-stepper-item.completed::after { background: var(--ttsc-accent); }
.ttsc-stepper-dot {
  width: 28px; height: 28px; border-radius: var(--ttsc-radius-pill); display: inline-flex; align-items: center; justify-content: center;
  border: 1.5px solid var(--ttsc-border-strong); background: var(--ttsc-surface); color: var(--ttsc-text-muted); font-size: 12px; font-weight: 600;
}
.ttsc-stepper-dot i { display: none; }
.ttsc-stepper-label { font-size: 12px; color: var(--ttsc-text-muted); }
.ttsc-stepper-item.active .ttsc-stepper-dot { background: var(--ttsc-accent); border-color: var(--ttsc-accent); color: var(--ttsc-accent-on); box-shadow: 0 0 0 4px var(--ttsc-accent-soft); }
.ttsc-stepper-item.active .ttsc-stepper-label { color: var(--ttsc-text); font-weight: 500; }
.ttsc-stepper-item.completed .ttsc-stepper-dot { background: var(--ttsc-accent-soft); border-color: var(--ttsc-accent-border); color: var(--ttsc-accent-text); }
.ttsc-stepper-item.completed .ttsc-stepper-dot i { display: inline; }
.ttsc-stepper-item.completed [data-ttsc-stepper-number] { display: none; }
.ttsc-stepper-item.completed .ttsc-stepper-label { color: var(--ttsc-text-2); cursor: pointer; }
/* Botões conforme a classe de posição da raiz */
.ttsc-stepper.first [data-ttsc-stepper-back],
.ttsc-stepper.last [data-ttsc-stepper-next],
.ttsc-stepper:not(.last) .ttsc-stepper-submit { display: none; }
.ttsc-stepper-actions { justify-content: space-between; }
```

### JS

```js
TTSC.init();

const form = document.getElementById('enrollment-wizard');
const stepper = ttscStepper.getOrCreateInstance(form);
let current = 1;

function invalidFields(section) {
  return [...section.querySelectorAll('input, select, textarea')].filter((el) => {
    const ok = el.checkValidity();
    el.setAttribute('aria-invalid', ok ? 'false' : 'true');
    return !ok;
  });
}

// Valida o passo atual antes de AVANÇAR (voltar é sempre livre)
form.addEventListener('change', (event) => {
  const payload = event.detail?.payload;
  if (!payload) return; // change de input comum, não do stepper
  if (payload.step < current) return;
  const section = document.querySelector(stepper.getItemElement(current).dataset.ttscStepperItem);
  const bad = invalidFields(section);
  if (bad.length) { payload.cancel = true; bad[0].focus(); }
});

form.addEventListener('changed', () => {
  stepper.getItemElements().forEach((item, i) => {
    const active = item.classList.contains('active');
    if (active) { current = i + 1; item.setAttribute('aria-current', 'step'); }
    else item.removeAttribute('aria-current');
  });
  document.querySelector(stepper.getItemElement(current).dataset.ttscStepperItem).querySelector('h3')?.focus();
});

// Voltar para um passo concluído clicando no indicador
form.querySelector('.ttsc-stepper-nav').addEventListener('click', (event) => {
  const item = event.target.closest('[data-ttsc-stepper-item].completed');
  if (item) stepper.go(stepper.getStep(item));
});

// Envio final com fetch + CSRF; 422 volta ao passo do campo com erro
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
  if (res.status === 422) {
    const { errors } = await res.json();
    const field = form.querySelector(`[name="${Object.keys(errors)[0]}"]`);
    const section = field.closest('section');
    stepper.go(stepper.getStep(form.querySelector(`[data-ttsc-stepper-item="#${section.id}"]`)));
    field.setAttribute('aria-invalid', 'true');
    return;
  }
  location.href = (await res.json()).redirect;
});
```

### SQL

Passo 2 lista só turmas com vaga; passo 3 lê a regra financeira do curso; o envio grava a matrícula em transação, travando a turma para não estourar `max_students`:

```sql
-- Passo 2: turmas do curso no período com vaga
SELECT cl.uuid, cl.code, cl.shift, cl.max_students, COUNT(e.id) AS enrolled,
       cl.max_students - COUNT(e.id) AS seats_left
  FROM classes cl
  LEFT JOIN enrollments e ON e.class_uuid = cl.uuid AND e.deleted_at IS NULL AND e.status = 'active'
 WHERE cl.course_uuid = :course_uuid AND cl.period_uuid = :period_uuid
   AND cl.deleted_at IS NULL AND cl.is_active = 1
 GROUP BY cl.uuid, cl.code, cl.shift, cl.max_students
HAVING cl.max_students IS NULL OR COUNT(e.id) < cl.max_students;

-- Passo 3: regra financeira vigente do curso
SELECT enrollment_fee, monthly_tuition, due_day, payment_method
  FROM academic_billing_rules
 WHERE course_uuid = :course_uuid AND status = 'active'
 ORDER BY created_at DESC LIMIT 1;

-- Envio (passo 4): tudo ou nada
START TRANSACTION;
SELECT id FROM classes WHERE uuid = :class_uuid AND deleted_at IS NULL FOR UPDATE;   -- trava a turma
SELECT COUNT(*) AS dup
  FROM enrollments
 WHERE student_uuid = :student_uuid AND course_uuid = :course_uuid
   AND status = 'active' AND deleted_at IS NULL;                                      -- 0, senão 422
INSERT INTO enrollments (uuid, code, student_uuid, course_uuid, class_uuid, curriculum_uuid, period_uuid,
                         type, status, enrollment_date, shift, modality, unit_uuid, notes)
VALUES (:uuid, :code, :student_uuid, :course_uuid, :class_uuid, :curriculum_uuid, :period_uuid,
        'regular', 'active', CURRENT_DATE, :shift, :modality, :unit_uuid, :notes);
COMMIT;
```

O controller roda os três passos no mesmo `PDO::beginTransaction()`; se a recontagem de vagas ou a duplicidade falhar, faz `rollBack()` e devolve 422 com `errors.class_uuid`, que o JS usa para voltar ao passo 2. `code` segue `uk_enrollment_unit_code` (único por unidade).

## Faça / Não faça

- **Faça:** validar no `change` do stepper e cancelar com `payload.cancel = true`.
- **Faça:** gravar só no último passo, em transação; os passos anteriores não persistem nada.
- **Não faça:** mais de 6 passos — agrupe ou divida o processo.
- **Não faça:** usar `goTo()` do build atual (recursão infinita); use `go(n)`.
