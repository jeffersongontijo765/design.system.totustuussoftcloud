# Spec: Refatoração do Sub-Sidebar — Módulo Privacidade & LGPD

**Projeto:** TotusTuusSoftCloud  
**Módulo:** Privacy Compliance  
**Componente:** Sub-Sidebar de Navegação  
**Template Base:** Supabase Design System (`ui-patterns/InnerSideMenu`)  
**Versão:** 1.0.0  
**Status:** Draft  
**Autor:** Spec gerado para revisão técnica  
**Data:** Junho 2026

- Language Standard: Global English
---

## 1. Contexto e Problema

O sub-sidebar atual do módulo de Privacidade & LGPD apresenta os seguintes problemas estruturais:

- **Hierarquia visual fraca:** títulos de grupo têm pouco contraste em relação aos itens, dificultando a escaneabilidade
- **Ordem não segue o fluxo operacional:** o usuário não consegue navegar na sequência lógica (ver → configurar → operar → governar → publicar)
- **Itens faltantes:** DPIA, Transferências Internacionais e Incidentes de Privacidade estão previstos na spec do módulo mas ausentes do menu
- **Redundância de dashboards:** "Dashboard", "Tenant Dashboard" e "Master Dashboard" aparecem como itens paralelos, quando deveriam ser contextos do mesmo painel
- **Estado ativo inconsistente:** o último item "Dashboard" do grupo LGPD Masking usa estilo diferente do padrão do template
- **Largura insuficiente:** itens como "Preferências de Cookies" ficam visualmente comprimidos

---

## 2. Padrão de Referência — Supabase InnerSideMenu

O template Supabase utiliza os seguintes componentes de `ui-patterns/InnerSideMenu`:

| Componente | Uso |
|---|---|
| `InnerSideMenuCollapsible` | Wrapper de grupo colapsável |
| `InnerSideMenuCollapsibleTrigger` | Título clicável do grupo com chevron |
| `InnerSideMenuCollapsibleContent` | Container dos itens do grupo |
| `InnerSideMenuItem` | Item de navegação individual |
| `InnerSideMenuSeparator` | Linha divisória entre grupos |
| `InnerSideBarTitle` | Título estático (não colapsável) |
| `InnerSideBarFilters` + `InnerSideBarFilterSearchInput` | Campo de busca no topo |
| `InnerSideMenuItemLoading` | Skeleton de carregamento |
| `InnerSideBarEmptyPanel` | Estado vazio do menu |

### Regras do padrão

- `defaultOpen={true}` apenas nos 2–3 grupos mais utilizados operacionalmente
- Demais grupos iniciam fechados (`defaultOpen={false}`) para reduzir altura total
- O campo de busca usa `InnerSideBarFilterSearchInput` — não um `<input>` customizado
- `InnerSideMenuSeparator` substitui bordas horizontais CSS manuais entre grupos
- Item ativo é controlado pelo componente via `isActive` prop ou rota ativa — **não** via classe CSS manual

---

## 3. Arquitetura de Grupos e Ordem

A nova estrutura deve seguir o fluxo operacional: **ver → configurar → operar → governar → publicar**.

### 3.1 Estrutura Completa

```
[Campo de busca — InnerSideBarFilterSearchInput]
  placeholder: "Buscar páginas de privacidade..."

────────────────────────────────────────────

VISÃO GERAL  (InnerSideBarTitle — estático, não colapsável)
  └─ Dashboard                          /admin/privacy/dashboard

[InnerSideMenuSeparator]

CONFORMIDADE LEGAL  (defaultOpen: true)
  ├─ Catálogo de Leis                   /admin/privacy/laws
  └─ Leis Aplicáveis                    /admin/privacy/applicability

[InnerSideMenuSeparator]

INVENTÁRIO & DIREITOS  (defaultOpen: true)
  ├─ RoPA                               /admin/privacy/ropa
  ├─ DSR                                /admin/privacy/dsr
  ├─ DPIA / Avaliações de Impacto       /admin/privacy/dpia       ← NOVO
  └─ DPO / Encarregado                  /admin/privacy/dpo

[InnerSideMenuSeparator]

CONSENTIMENTOS  (defaultOpen: true)
  ├─ Consentimentos                     /admin/privacy/consents
  ├─ Preferências de Cookies            /admin/privacy/cookies
  └─ Gerenciar Sessões                  /admin/privacy/sessions

[InnerSideMenuSeparator]

TRANSFERÊNCIAS & INCIDENTES  (defaultOpen: false)
  ├─ Transferências Internacionais      /admin/privacy/transfers   ← NOVO
  └─ Incidentes de Privacidade          /admin/privacy/incidents   ← NOVO

[InnerSideMenuSeparator]

POLÍTICAS  (defaultOpen: false)
  ├─ Políticas de Privacidade           /admin/privacy/policies
  └─ Policy Builder                     /admin/privacy/policy-builder

[InnerSideMenuSeparator]

LGPD MASKING  (defaultOpen: false)
  └─ Dashboard                          /admin/privacy/masking/dashboard
```

---

## 4. Tratamento do Contexto de Dashboard (Tenant / Master)

O menu atual expõe três itens de dashboard separados:
- Dashboard
- Tenant Dashboard
- Master Dashboard

**Decisão de design:** esses três itens representam o **mesmo Dashboard** em contextos diferentes de visão, não três páginas distintas. A solução correta no padrão Supabase é um **seletor de contexto** acima do menu, e não itens paralelos no sidebar.

### Implementação recomendada

Acima do `InnerSideMenuCollapsible` da seção "Visão Geral", adicionar um `<Select>` ou segmented control com as opções:

```
[Contexto: ▾]  ○ Meu Tenant   ○ Tenant Selecionado   ○ Master (Global)
```

O item "Dashboard" no menu aponta para a mesma rota `/admin/privacy/dashboard`, mas a view renderizada muda conforme o contexto selecionado via query param ou store global (`?context=master`).

---

## 5. Itens Novos a Implementar

Os itens abaixo estão especificados na `privacy-compliance-spec.md` porém **ausentes do menu atual**:

| Item | Grupo | Rota | Permissão |
|---|---|---|---|
| DPIA / Avaliações de Impacto | Inventário & Direitos | `/admin/privacy/dpia` | `privacy:dpia:read` |
| Transferências Internacionais | Transferências & Incidentes | `/admin/privacy/transfers` | `privacy:transfers:manage` |
| Incidentes de Privacidade | Transferências & Incidentes | `/admin/privacy/incidents` | `privacy:incidents:read` |

---

## 6. Especificação de Estado dos Grupos

| Grupo | `defaultOpen` | Justificativa |
|---|---|---|
| Visão Geral | estático (sem collapsible) | Dashboard é o ponto de entrada — sempre visível |
| Conformidade Legal | `true` | Configuração frequente em implantação inicial |
| Inventário & Direitos | `true` | Operação diária principal (DSR, RoPA) |
| Consentimentos | `true` | Operação diária frequente |
| Transferências & Incidentes | `false` | Uso eventual — abre quando necessário |
| Políticas | `false` | Uso eventual — geração e publicação de docs |
| LGPD Masking | `false` | Subproduto separado — uso específico |

---

## 7. Ícones

Manter os ícones existentes onde já definidos. Para os itens novos, usar ícones do conjunto já adotado no projeto (Lucide ou similar):

| Item Novo | Ícone sugerido |
|---|---|
| DPIA / Avaliações de Impacto | `shield-alert` |
| Transferências Internacionais | `arrow-right-left` |
| Incidentes de Privacidade | `triangle-alert` |

---

## 8. Implementação em Código — Estrutura JSX

```jsx
import {
  InnerSideMenuCollapsible,
  InnerSideMenuCollapsibleContent,
  InnerSideMenuCollapsibleTrigger,
  InnerSideMenuItem,
  InnerSideMenuSeparator,
  InnerSideBarTitle,
  InnerSideBarFilters,
  InnerSideBarFilterSearchInput,
} from 'ui-patterns/InnerSideMenu'

export function PrivacySidebarMenu({ currentPath }) {
  return (
    <Card className="min-w-60 bg-dash-sidebar py-4 flex flex-col gap-4 h-full">

      {/* Campo de busca */}
      <div className="px-3">
        <InnerSideBarFilters>
          <InnerSideBarFilterSearchInput
            name="privacy-search"
            placeholder="Buscar páginas de privacidade..."
            aria-labelledby="Buscar páginas"
          />
        </InnerSideBarFilters>
      </div>

      {/* VISÃO GERAL — estático */}
      <div className="px-3">
        <InnerSideBarTitle>Visão Geral</InnerSideBarTitle>
        <div className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/dashboard" isActive={currentPath === '/admin/privacy/dashboard'}>
            Dashboard
          </InnerSideMenuItem>
        </div>
      </div>

      <InnerSideMenuSeparator />

      {/* CONFORMIDADE LEGAL */}
      <InnerSideMenuCollapsible defaultOpen>
        <InnerSideMenuCollapsibleTrigger title="Conformidade Legal" />
        <InnerSideMenuCollapsibleContent className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/laws">Catálogo de Leis</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/applicability">Leis Aplicáveis</InnerSideMenuItem>
        </InnerSideMenuCollapsibleContent>
      </InnerSideMenuCollapsible>

      <InnerSideMenuSeparator />

      {/* INVENTÁRIO & DIREITOS */}
      <InnerSideMenuCollapsible defaultOpen>
        <InnerSideMenuCollapsibleTrigger title="Inventário & Direitos" />
        <InnerSideMenuCollapsibleContent className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/ropa">RoPA</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/dsr">DSR</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/dpia">DPIA / Avaliações de Impacto</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/dpo">DPO / Encarregado</InnerSideMenuItem>
        </InnerSideMenuCollapsibleContent>
      </InnerSideMenuCollapsible>

      <InnerSideMenuSeparator />

      {/* CONSENTIMENTOS */}
      <InnerSideMenuCollapsible defaultOpen>
        <InnerSideMenuCollapsibleTrigger title="Consentimentos" />
        <InnerSideMenuCollapsibleContent className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/consents">Consentimentos</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/cookies">Preferências de Cookies</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/sessions">Gerenciar Sessões</InnerSideMenuItem>
        </InnerSideMenuCollapsibleContent>
      </InnerSideMenuCollapsible>

      <InnerSideMenuSeparator />

      {/* TRANSFERÊNCIAS & INCIDENTES */}
      <InnerSideMenuCollapsible defaultOpen={false}>
        <InnerSideMenuCollapsibleTrigger title="Transferências & Incidentes" />
        <InnerSideMenuCollapsibleContent className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/transfers">Transferências Internacionais</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/incidents">Incidentes de Privacidade</InnerSideMenuItem>
        </InnerSideMenuCollapsibleContent>
      </InnerSideMenuCollapsible>

      <InnerSideMenuSeparator />

      {/* POLÍTICAS */}
      <InnerSideMenuCollapsible defaultOpen={false}>
        <InnerSideMenuCollapsibleTrigger title="Políticas" />
        <InnerSideMenuCollapsibleContent className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/policies">Políticas de Privacidade</InnerSideMenuItem>
          <InnerSideMenuItem href="/admin/privacy/policy-builder">Policy Builder</InnerSideMenuItem>
        </InnerSideMenuCollapsibleContent>
      </InnerSideMenuCollapsible>

      <InnerSideMenuSeparator />

      {/* LGPD MASKING */}
      <InnerSideMenuCollapsible defaultOpen={false}>
        <InnerSideMenuCollapsibleTrigger title="LGPD Masking" />
        <InnerSideMenuCollapsibleContent className="mt-1">
          <InnerSideMenuItem href="/admin/privacy/masking/dashboard">Dashboard</InnerSideMenuItem>
        </InnerSideMenuCollapsibleContent>
      </InnerSideMenuCollapsible>

    </Card>
  )
}
```

---

## 9. Checklist de Implementação

- [ ] Substituir `<input>` de busca customizado por `InnerSideBarFilterSearchInput`
- [ ] Substituir bordas CSS manuais entre grupos por `InnerSideMenuSeparator`
- [ ] Remover "Tenant Dashboard" e "Master Dashboard" do menu; implementar seletor de contexto acima
- [ ] Mover "Catálogo de Leis" para antes de "Leis Aplicáveis" no grupo Conformidade Legal
- [ ] Adicionar item **DPIA / Avaliações de Impacto** em Inventário & Direitos
- [ ] Mover **DPO** para depois de DPIA (final do grupo Inventário & Direitos)
- [ ] Criar grupo **Transferências & Incidentes** com os dois itens novos
- [ ] Garantir que `defaultOpen` seja `false` nos grupos: Transferências & Incidentes, Políticas, LGPD Masking
- [ ] Padronizar estado ativo via prop `isActive` ou detecção de rota — remover CSS manual de estado ativo
- [ ] Adicionar ícones nos itens novos: `shield-alert`, `arrow-right-left`, `triangle-alert`
- [ ] Verificar largura mínima do sub-sidebar para acomodar "Preferências de Cookies" sem truncamento
- [ ] Testar em dark mode (padrão Supabase)
- [ ] Testar collapse/expand de todos os grupos
- [ ] Verificar acessibilidade: `aria-label` nos ícones, navegação por teclado, foco visível

---

## 10. Rotas e Permissões por Item

| Item | Rota | Permissão |
|---|---|---|
| Dashboard | `/admin/privacy/dashboard` | `privacy:dashboard:read` |
| Catálogo de Leis | `/admin/privacy/laws` | `privacy:laws:read` |
| Leis Aplicáveis | `/admin/privacy/applicability` | `privacy:applicability:manage` |
| RoPA | `/admin/privacy/ropa` | `privacy:ropa:manage` |
| DSR | `/admin/privacy/dsr` | `privacy:dsr:read` |
| DPIA / Avaliações de Impacto | `/admin/privacy/dpia` | `privacy:dpia:read` |
| DPO / Encarregado | `/admin/privacy/dpo` | `privacy:dpo:manage` |
| Consentimentos | `/admin/privacy/consents` | `privacy:consents:read` |
| Preferências de Cookies | `/admin/privacy/cookies` | `privacy:consents:manage` |
| Gerenciar Sessões | `/admin/privacy/sessions` | `privacy:consents:manage` |
| Transferências Internacionais | `/admin/privacy/transfers` | `privacy:transfers:manage` |
| Incidentes de Privacidade | `/admin/privacy/incidents` | `privacy:incidents:read` |
| Políticas de Privacidade | `/admin/privacy/policies` | `privacy:policies:manage` |
| Policy Builder | `/admin/privacy/policy-builder` | `privacy:policies:manage` |
| LGPD Masking — Dashboard | `/admin/privacy/masking/dashboard` | `privacy:masking:read` |

