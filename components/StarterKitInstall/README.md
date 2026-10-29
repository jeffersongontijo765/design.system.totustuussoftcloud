# StarterKitInstall

Kit da instalação inicial: o render real de `resources/views/install/index.php` — um formulário único em três blocos (banco de dados, empresa, administrador principal) dentro de `web/layouts/main.php`.

## Quando usar

- Primeira execução de uma instância nova (sem `storage/installed.lock` e sem administrador ativo): `GET /install` mostra o formulário, `POST /install` executa `App\Console\InstallCommand`.
- Ponto de partida para outros formulários de configuração inicial fora do app (ex.: ativar licença, configurar SMTP antes do primeiro login).
- **Não é** um assistente em etapas: o arquivo real é uma página com todos os campos; se precisar de etapas, monte com [Stepper](../Stepper/README.md) dentro deste layout.
- Configuração com o sistema já instalado → páginas de configurações do app ([StarterKitAppShell](../StarterKitAppShell/README.md)). Depois de instalado, `GET` e `POST /install` respondem **403** ("System already installed").

## Anatomia

```
web/layouts/main.php (topbar + navbar fixa do site, rodapé, chat de vendas)
└─ section('content')
   div.min-h-screen.flex.items-center.justify-center.bg-gray-100
   └─ div.max-w-2xl.bg-white.rounded-xl.shadow-lg.p-8
      ├─ h1 [foguete] Instalação do Sistema · "Configure sua empresa em poucos passos"
      ├─ alertas de sessão (error / success)
      └─ form[method=POST][action=/install] + csrf_field()
         ├─ [banco] Configurações do Banco de Dados   db_host · db_port · db_name · db_user · db_pass   (grid md:grid-cols-2)
         ├─ [prédio] Dados da Empresa                  empresa_nome · empresa_razao · empresa_cnpj · empresa_telefone · empresa_email
         ├─ [usuário] Administrador Principal          admin_nome · admin_email · admin_senha · admin_senha_confirm
         └─ botão "Instalar Sistema" (bg-blue-600)
```

| Parte | Origem real | Obrigatório |
|---|---|---|
| Rota GET | `routes/web.php`: se `SystemInstaller::isInstalled()` → 403; se `install.php` existir na raiz ele é servido; senão `view('install::index')` | sim |
| Rota POST | `routes/web.php` → `(new InstallCommand())->run($data, true)`; JSON quando `X-Requested-With: XMLHttpRequest` | sim |
| Layout | `web::layouts/main` (o mesmo do [StarterKitPublicSite](../StarterKitPublicSite/README.md)) | sim |
| Formulário | `install/index.php` com classes Tailwind de `tailwind.web.css` | sim |
| Ícones | `fas fa-rocket`, `fas fa-database` … (peso solid; no DS caem no light servido) | — |

## Variantes / Estados

| Estado | Como | Observação |
|---|---|---|
| Inicial | valores padrão `db_host=127.0.0.1`, `db_port=3306`, `db_name=totustuus`, `db_user=root` | Desktop 1440 |
| Erro | `session()->flash('error')` → caixa vermelha acima do formulário | — |
| Sucesso | `session()->flash('success')` | — |
| Já instalado | `GET` e `POST` → 403 | — |
| ≥ 768px | campos em 2 colunas (`md:grid-cols-2`) | Desktop/Tablet |
| < 768px | 1 coluna | Mobile 390 |
| Tema | **só claro**: a view usa `bg-white`, `text-gray-*` sem variante `dark:`; com o site em escuro o cartão fica branco com rótulos ilegíveis, por isso o kit força o claro (grava `light` em `ttsc-theme`) | — |

Observado no render real: o bloco é centralizado com `min-h-screen` sob o header fixo do site, então o título "Instalação do Sistema" fica parcialmente atrás da navbar até rolar; prefira `pt-44` no contêiner ao copiar.

## API

| Ponto | Efeito |
|---|---|
| `SystemInstaller::isInstalled()` | `storage/installed.lock` → instalado; sem `.env` → não; senão conta administradores ativos (SQL abaixo) |
| `POST /install` (form ou AJAX) | campos `db_*`, `empresa_*`, `admin_*`; resposta JSON `{success, error?}` no AJAX |
| `InstallCommand::run($data, true)` | cria o banco/tabelas, a empresa e o administrador; grava o lock |
| `api/v1/installed` | `{success, installed}` — consultado pelo login para esconder o link de instalação |

## Acessibilidade

- Cada campo com `label` visível; agrupe os três blocos em `fieldset` + `legend` ao reaproveitar (hoje são `h2`).
- Senha do banco pode ficar vazia ("Deixe vazio se não houver senha") — diga isso no `label`/ajuda, não só no placeholder.
- Mensagens de erro do instalador em texto, junto do campo, e foco movido para a primeira mensagem.
- Contraste: com o tema forçado em claro os rótulos `text-gray-700` sobre `bg-white` passam de 7:1.

## Modelos

### HTML

```php
<?php $this->layout('web::layouts/main', ['title' => 'Instalação']) ?>
<?php $this->start('content') ?>
<div class="pt-44 pb-16 flex justify-center bg-gray-100 px-4">
  <div class="max-w-2xl w-full bg-white rounded-xl shadow-lg p-8">
    <h1 class="text-3xl font-bold text-gray-900 mb-2 text-center">
      <i class="fa-light fa-rocket text-emerald-600 mr-2" aria-hidden="true"></i>Instalação do Sistema
    </h1>
    <p class="text-gray-600 text-center mb-8">Configure sua instituição em poucos passos</p>
    <?php if (session()->has('error')): ?>
      <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6" role="alert"><?= $this->e(session()->flash('error')) ?></div>
    <?php endif; ?>
    <form method="POST" action="<?= url('/install') ?>" class="space-y-6" id="installForm">
      <?= csrf_field() ?>
      <fieldset class="border-b pb-6">
        <legend class="text-lg font-semibold text-gray-800 mb-4"><i class="fa-light fa-database mr-2" aria-hidden="true"></i>Banco de dados</legend>
        <div class="grid md:grid-cols-2 gap-4">
          <label class="block text-sm font-medium text-gray-700">Host
            <input type="text" name="db_host" value="127.0.0.1" required class="mt-1 w-full px-3 py-2 border rounded-lg"></label>
          <label class="block text-sm font-medium text-gray-700">Porta
            <input type="number" name="db_port" value="3306" required class="mt-1 w-full px-3 py-2 border rounded-lg"></label>
        </div>
      </fieldset>
      <fieldset>
        <legend class="text-lg font-semibold text-gray-800 mb-4"><i class="fa-light fa-school mr-2" aria-hidden="true"></i>Instituição</legend>
        <label class="block text-sm font-medium text-gray-700">Nome fantasia
          <input type="text" name="empresa_nome" placeholder="Colégio Santa Clara" required class="mt-1 w-full px-3 py-2 border rounded-lg"></label>
      </fieldset>
      <button type="submit" class="w-full py-3 rounded-lg bg-emerald-600 text-white font-semibold">Instalar</button>
    </form>
  </div>
</div>
<?php $this->stop() ?>
```

### CSS

Mesma pilha do site (`tailwind.web.css`, `web-layout.css`, `ttsc.rtl.css`). Extensão para um estado "verificando conexão" com tokens:

```css
.install-check { display: flex; align-items: center; gap: var(--ttsc-space-2); font-size: 13px; color: var(--ttsc-text-2); }
.install-check[data-state="ok"]    { color: var(--ttsc-accent-text); }
.install-check[data-state="error"] { color: var(--ttsc-danger-text); }
.install-check i { width: 16px; text-align: center; }
```

### JS

```js
// Envio por AJAX com retorno JSON do POST /install (o handler responde JSON quando há X-Requested-With)
(function () {
  var form = document.getElementById('installForm');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var senha = form.elements.admin_senha, conf = form.elements.admin_senha_confirm;
    if (senha && conf && senha.value !== conf.value) { conf.setCustomValidity('As senhas não conferem.'); conf.reportValidity(); return; }
    var btn = form.querySelector('[type="submit"]'); btn.disabled = true; btn.textContent = 'Instalando…';
    fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (!res.success) throw new Error(res.error || 'Falha na instalação.');
        location.href = form.action.replace(/install$/, 'login');
      })
      .catch(function (err) { btn.disabled = false; btn.textContent = 'Instalar'; alert(err.message); });
  });
})();
```

### SQL

```sql
-- SystemInstaller::checkInstallation() (depois de verificar storage/installed.lock e .env)
SELECT COUNT(*) AS count FROM users WHERE type = 'admin' AND status = 'active';

-- Diagnóstico antes de instalar: tabelas centrais, tenants ativos e versão do servidor
SELECT (SELECT COUNT(*) FROM information_schema.TABLES
         WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME IN ('users', 'tenants', 'units')) AS core_tables,
       (SELECT COUNT(*) FROM tenants WHERE status = 'active') AS active_tenants,
       VERSION() AS server_version;
```

`count > 0` faz `GET` e `POST /install` responderem 403; o diagnóstico pode alimentar um aviso no topo do formulário ("banco já contém tabelas do sistema").

## Como começar um projeto a partir do kit

1. **Arquivos do kit**: `kit.html` + `assets/css/{tailwind.web.css, web-layout.css, ttsc.rtl.css}`, `assets/js/consent-cookie.js`, `assets/media/` e `assets/fa.css`; gerado por `$SPD/dsh/gen_kits.py` a partir de `php $SPD/app/view_harness.php /install install::index …`.
2. **No repo**: formulários de configuração inicial vivem em `resources/views/install/` e são registrados com a pasta `install` do `PlatesEngine` (`install::nome`).
3. **Outro projeto**: copie `install/index.php`, as rotas GET/POST de `/install`, `App\Support\SystemInstaller` e `App\Console\InstallCommand`, mais os arquivos do [StarterKitPublicSite](../StarterKitPublicSite/README.md#como-começar-um-projeto-a-partir-do-kit).

## Faça / Não faça

- **Faça:** bloqueie a rota depois de instalado (lock + 403) e exija CSRF no POST.
- **Faça:** confirme a senha do administrador no cliente e no servidor.
- **Não faça:** deixar `install.php` na raiz em produção — a rota o serve antes da view.
- **Não faça:** usar esta página com o site em tema escuro sem antes dar variantes `dark:` às classes `bg-white`/`text-gray-*`.
