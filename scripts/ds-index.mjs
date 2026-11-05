#!/usr/bin/env node
/**
 * ds-index.mjs — gera docs/ai/catalog.json e docs/ai/CATALOG.md a partir dos
 * README.md de components/. Fonte da verdade = README do componente.
 *
 * Uso: node scripts/ds-index.mjs [--check]
 *   --check  falha (exit 1) se o catálogo estiver desatualizado.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const COMPONENTS = path.join(ROOT, "components");
const OUT_JSON = path.join(ROOT, "docs", "ai", "catalog.json");
const OUT_MD = path.join(ROOT, "docs", "ai", "CATALOG.md");
const CHECK = process.argv.includes("--check");

const ARCHETYPES = ["dashboard", "records", "detail", "settings", "calendar", "auth", "catalog"];

const clean = (s) =>
  s
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/[`*_>#]/g, "")
    .replace(/\s+/g, " ")
    .trim();

function section(md, name) {
  const re = new RegExp(`^##\\s+${name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\s*$`, "im");
  const m = md.match(re);
  if (!m) return "";
  const rest = md.slice(m.index + m[0].length);
  const end = rest.search(/^##\s+/m);
  return end === -1 ? rest : rest.slice(0, end);
}

function bullets(text) {
  return text
    .split(/\r?\n/)
    .filter((l) => /^\s*[-*]\s+/.test(l))
    .map((l) => clean(l.replace(/^\s*[-*]\s+/, "")))
    .filter(Boolean);
}

function tableRows(text) {
  const rows = text
    .split(/\r?\n/)
    .filter((l) => l.trim().startsWith("|"))
    .map((l) => l.trim().replace(/^\||\|$/g, "").split("|").map((c) => clean(c)));
  return rows.filter((r) => !r.every((c) => /^-+$/.test(c) || c === ""));
}

function firstParagraph(md) {
  const body = md.replace(/^#\s+.+\n/, "");
  for (const block of body.split(/\n\s*\n/)) {
    const b = block.trim();
    if (!b) continue;
    if (/^(#|>|<|```|\||-|\*|\d+\.)/.test(b)) continue;
    return clean(b).slice(0, 240);
  }
  return "";
}

function categorize(id) {
  if (/^(Page|StarterKit|Layout|Widgets|Widget[A-Z])/.test(id)) return "modelos";
  if (
    /^(AmCharts|ApexCharts|ApexChartsAdvanced|ChartKit|CKEditor|Quill|TinyMCE|DataTablesNet|FullCalendar|Select2|Flatpickr|NoUiSlider|TempusDominus|Tagify|SweetAlert|Toastr|JsTree|Lozad|Recaptcha|Clipboard|Autosize|CountUp|SmoothScroll|Scrollspy|Scrollto|Scrolltop|Sticky|Hover|Underline|Rotate|Swapper|ThirdPartyPlugin|Autosize)/.test(
      id
    )
  )
    return "terceiros";
  if (/(Chart|Analytics|Heatmap|Sankey|Funnel|Gauge|Quadrant|Kpi|KPI|Ranked|Bullet|GeoMap|Bundle|Summary|Trend|Balance|Portfolio|Convertion|Conversion)/.test(id))
    return "graficos";
  if (/(Input|Textarea|Select|Checkbox|Radio|Switch|Toggle|Slider|Picker|Mask|Dropzone|File|Upload|Form|Password|Pin|Rating|ColorPicker|Repeater|Cropper|Segmented|Stepper)/.test(id))
    return "formularios";
  if (/(Alert|Toast|Modal|Drawer|Tooltip|Popover|Skeleton|EmptyState|Progress|BlockUI|Overlay|Banner|Cookie|Dismiss|Pulse|Ribbon|Indicator|Badge)/.test(id))
    return "feedback";
  if (/(Menu|Breadcrumb|Tabs|Pagination|Navigation|Nav|Scroll|Swapper|ThemeSwitch|QuickSearch)/.test(id))
    return "navegacao";
  if (/(Table|Kanban|Timeline|Tree|List|Queue|Records|Record|Card|Invoice|Order|Gallery|Carousel|Lightbox|FileManager|OrgChart|Chat|Comment|Review|Testimonial|Profile|Team|Article|Pricing|Checklist|Unit|Score|Risk|Scenario|Insight|Approval|History|Meta|Goal)/.test(id))
    return "dados";
  if (/(Button|Link|Avatar|Separator|Kbd|Symbol|Helpers|Utilities|Bullets|Textarea|Cover|Sticky)/.test(id))
    return "fundacao";
  return "outros";
}

const components = [];
for (const entry of fs.readdirSync(COMPONENTS, { withFileTypes: true })) {
  if (!entry.isDirectory()) continue;
  const dir = path.join(COMPONENTS, entry.name);
  const readmePath = path.join(dir, "README.md");
  if (!fs.existsSync(readmePath)) continue;
  const md = fs.readFileSync(readmePath, "utf8");
  const title = (md.match(/^#\s+(.+)$/m) || [, entry.name])[1].trim();
  const whenToUse = bullets(section(md, "Quando usar")).slice(0, 6);
  const variants = tableRows(section(md, "Variantes"))
    .map((r) => ({ name: r[0], class: (r[1] || "").replace(/[`]/g, "") }))
    .filter((v) => v.name && !/variante/i.test(v.name))
    .slice(0, 12);
  const states = tableRows(section(md, "Estados"))
    .map((r) => r[0])
    .filter(Boolean)
    .slice(0, 8);
  const a11y = bullets(section(md, "Acessibilidade")).slice(0, 6);
  const responsive = /responsiv|breakpoint|mobile|largura estreita/i.test(md);
  const hasPreview = fs.existsSync(path.join(dir, "preview.html"));

  components.push({
    id: entry.name,
    title,
    category: categorize(entry.name),
    purpose: firstParagraph(md),
    whenToUse,
    variants,
    states,
    a11y,
    responsive,
    files: {
      readme: `components/${entry.name}/README.md`,
      preview: hasPreview ? `components/${entry.name}/preview.html` : null,
    },
    tags: [...new Set(`${entry.name} ${title} ${whenToUse.join(" ")}`.toLowerCase().match(/[a-zà-ú0-9]{4,}/g) || [])].slice(0, 8),
  });
}

components.sort((a, b) => a.id.localeCompare(b.id, "pt-BR"));

const byCategory = {};
for (const c of components) byCategory[c.category] = (byCategory[c.category] || 0) + 1;

const catalog = {
  generatedAt: new Date().toISOString(),
  source: "components/*/README.md",
  count: components.length,
  archetypes: ARCHETYPES,
  categories: byCategory,
  responsiveDocumented: components.filter((c) => c.responsive).length,
  components,
};

const payload = JSON.stringify(catalog, null, 2) + "\n";

if (!CHECK) {
  fs.mkdirSync(path.dirname(OUT_JSON), { recursive: true });
  fs.writeFileSync(OUT_JSON, payload, "utf8");
}

const CATEGORY_LABEL = {
  fundacao: "Fundação",
  formularios: "Formulários",
  dados: "Dados e conteúdo",
  feedback: "Feedback e sobreposição",
  navegacao: "Navegação",
  graficos: "Gráficos e análise",
  modelos: "Modelos de página",
  terceiros: "Plugins de terceiros",
  outros: "Outros",
};

const md = [
  "# Catálogo de componentes",
  "",
  `> Gerado por \`scripts/ds-index.mjs\` a partir de ${components.length} READMEs. Não editar à mão.`,
  `> Consulte \`catalog.json\` para dados estruturados (variantes, estados, acessibilidade).`,
  "",
  `Arquétipos: ${ARCHETYPES.map((a) => `\`${a}\``).join(" · ")}`,
  `Componentes com responsividade documentada: ${catalog.responsiveDocumented}/${components.length}`,
  "",
];

for (const [cat, count] of Object.entries(byCategory).sort((a, b) => b[1] - a[1])) {
  md.push(`## ${CATEGORY_LABEL[cat] || cat} (${count})`, "");
  md.push("| Componente | Para que serve | Responsivo | README |");
  md.push("|---|---|---|---|");
  for (const c of components.filter((x) => x.category === cat)) {
    const purpose = (c.purpose || c.whenToUse[0] || "").slice(0, 150).replace(/\|/g, "/");
    md.push(`| **${c.title}** | ${purpose} | ${c.responsive ? "sim" : "—"} | [abrir](${c.files.readme}) |`);
  }
  md.push("");
}

const markdown = md.join("\n");

if (CHECK) {
  const current = fs.existsSync(OUT_JSON) ? fs.readFileSync(OUT_JSON, "utf8") : "";
  const strip = (s) => (s ? JSON.parse(s) : {});
  const a = strip(current);
  const b = JSON.parse(payload);
  delete a.generatedAt;
  delete b.generatedAt;
  const currentMarkdown = fs.existsSync(OUT_MD) ? fs.readFileSync(OUT_MD, "utf8") : "";
  if (JSON.stringify(a) !== JSON.stringify(b) || currentMarkdown !== markdown) {
    console.error("catálogo desatualizado. Rode: node scripts/ds-index.mjs");
    process.exit(1);
  }
  console.log(`catálogo em dia (${components.length} componentes).`);
  process.exit(0);
}

fs.writeFileSync(OUT_MD, markdown, "utf8");
console.log(`catálogo gerado: ${components.length} componentes -> docs/ai/catalog.json e docs/ai/CATALOG.md`);
for (const [cat, n] of Object.entries(byCategory).sort((a, b) => b[1] - a[1])) {
  console.log(`  ${String(n).padStart(3)} ${CATEGORY_LABEL[cat] || cat}`);
}
