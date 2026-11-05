#!/usr/bin/env node
/**
 * ds-check.mjs — validador do design system (R1–R19 de docs/ai/rules.md).
 *
 * Uso:
 *   node scripts/ds-check.mjs paginas/referencia/*.html
 *   node scripts/ds-check.mjs paginas/referencia
 *   node scripts/ds-check.mjs --all --report   (mede dívida, sempre exit 0)
 *
 * Exit 1 quando há erro. Avisos não derrubam o build.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const REPORT = args.includes("--report");
const ALL = args.includes("--all") || REPORT;
const targets = args.filter((a) => !a.startsWith("--"));

const ARCHETYPES = new Set(["dashboard", "records", "detail", "settings", "calendar", "auth", "catalog"]);
const DENSITIES = new Set(["compact", "comfortable", "spacious"]);
const PALETTE =
  /\b(?:bg|text|border|ring|from|to|via|divide|placeholder|fill|stroke|shadow|outline|decoration|accent|caret)-(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-(?:50|[1-9]00)\b/;
const PRIMITIVES = /\bttsc-(?:container|stack|grid|split|toolbar)\b/;

function tableHasWrapperAncestor(html, tableAt) {
  const tags = [...html.slice(0, tableAt).matchAll(/<\/?([a-z][\w-]*)(?:\s[^<>]*?)?>/gi)];
  const stack = [];
  for (const match of tags) {
    const tag = match[1].toLowerCase();
    if (match[0].startsWith("</")) {
      for (let i = stack.length - 1; i >= 0; i--) {
        if (stack[i].tag === tag) { stack.length = i; break; }
      }
    } else if (!/^(?:meta|link|img|input|br|hr|source|area|base|col|embed|param|track|wbr)$/i.test(tag)) {
      stack.push({ tag, isWrapper: /\bclass=["'][^"']*\bttsc-table-wrapper\b/.test(match[0]) });
    }
  }
  return stack.some((node) => node.isWrapper);
}

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (e.name === ".git" || e.name === "node_modules") continue;
      walk(p, out);
    } else if (e.name.endsWith(".html") || e.name.endsWith(".js")) out.push(p);
  }
  return out;
}

function expand(arg) {
  const abs = path.resolve(ROOT, arg);
  if (!fs.existsSync(abs)) {
    // glob simples: dir/*.html
    if (arg.includes("*")) {
      const dir = path.resolve(ROOT, path.dirname(arg));
      const re = new RegExp("^" + path.basename(arg).replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*") + "$");
      return fs.existsSync(dir)
        ? fs.readdirSync(dir).filter((f) => re.test(f)).map((f) => path.join(dir, f))
        : [];
    }
    return [];
  }
  const st = fs.statSync(abs);
  return st.isDirectory() ? walk(abs) : [abs];
}

let files = [];
if (ALL) files = walk(path.join(ROOT, "paginas"));
else for (const t of targets) files.push(...expand(t));

if (!files.length) {
  console.error("nenhum arquivo HTML para validar. Passe um caminho ou use --all.");
  process.exit(2);
}

const results = [];
const archetypeVariants = new Map();

for (const file of files) {
  const rel = path.relative(ROOT, file).replace(/\\/g, "/");
  const html = fs.readFileSync(file, "utf8");
  const errors = [];
  const warnings = [];
  const add = (id, msg) => errors.push(`${id} ${msg}`);
  const warn = (id, msg) => warnings.push(`${id} ${msg}`);

  // Arquivos .js: só o orçamento do controller (R19)
  if (file.endsWith(".js")) {
    const bytes = Buffer.byteLength(html, "utf8");
    if (bytes > 8 * 1024 && /paginas[\\/]/.test(file)) add("R19", `controller de página com ${Math.round(bytes / 1024)} KB (limite 8 KB)`);
    results.push({ rel, bytes, errors, warnings, cssText: "", classes: "", html: "" });
    continue;
  }

  // R1 viewport
  if (!/<meta[^>]+name=["']viewport["'][^>]*>/i.test(html)) add("R1", "sem <meta name=viewport>");
  else if (!/width=device-width/i.test(html)) add("R1", "viewport sem width=device-width");

  // R2 eventos inline
  if (/\son[a-z]+\s*=\s*["']/i.test(html)) add("R2", "evento inline (on*=) encontrado");

  // R3 cores literais em style attr/<style>
  const styleBlocks = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)].map((m) => m[1]).join("\n");
  const styleAttrs = [...html.matchAll(/\sstyle=["']([^"']*)["']/gi)].map((m) => m[1]).join("\n");
  const cssText = styleBlocks + "\n" + styleAttrs;
  const literal = cssText.match(/#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(/g);
  if (literal) add("R3", `cor literal em estilo: ${[...new Set(literal)].slice(0, 4).join(", ")}`);

  // R4 utilitário de cor Tailwind
  const classes = [...html.matchAll(/\sclass=["']([^"']*)["']/gi)].map((m) => m[1]).join(" ");
  const palette = classes.match(new RegExp(PALETTE.source, "g"));
  if (palette) add("R4", `utilitário de cor cru: ${[...new Set(palette)].slice(0, 5).join(", ")}`);

  // R5 largura fixa
  const widths = [...cssText.matchAll(/(?:^|[;"'\s])(?:min-)?width\s*:\s*(\d{3,})px/gi)]
    .map((m) => Number(m[1]))
    .filter((n) => n > 240);
  if (widths.length) add("R5", `largura fixa: ${[...new Set(widths)].join(", ")}px`);

  // R6 page-spec
  let spec = null;
  const specMatch = html.match(/<!--\s*page-spec\s*(\{[\s\S]*?\})\s*-->/i);
  if (!specMatch) {
    add("R6", "page-spec ausente");
  } else {
    try {
      spec = JSON.parse(specMatch[1]);
      if (!ARCHETYPES.has(spec.archetype)) add("R6", `archetype inválido: ${spec.archetype}`);
      if (!spec.variant) add("R6", "variant ausente");
      if (!DENSITIES.has(spec.density)) add("R6", `density inválida: ${spec.density}`);
      if (!spec.intent || String(spec.intent).length < 10) add("R6", "intent ausente/curto");
      if (spec.archetype && spec.variant) {
        const key = spec.archetype;
        const list = archetypeVariants.get(key) || [];
        list.push({ variant: spec.variant, file: rel });
        archetypeVariants.set(key, list);
      }
    } catch {
      add("R6", "page-spec não é JSON válido");
    }
  }

  // R8 orçamento
  const bytes = Buffer.byteLength(html, "utf8");
  if (bytes > 80 * 1024) add("R8", `página com ${Math.round(bytes / 1024)} KB (limite 80 KB)`);

  // R9 tabela dentro do wrapper
  let idx = html.indexOf("<table");
  while (idx !== -1) {
    if (!tableHasWrapperAncestor(html, idx)) {
      add("R9", "<table> fora de .ttsc-table-wrapper");
      break;
    }
    idx = html.indexOf("<table", idx + 1);
  }

  // R10 primitivos de layout
  if (!PRIMITIVES.test(classes)) warn("R10", "nenhum primitivo de layout (ttsc-container/stack/grid/split/toolbar)");

  // R11 a11y de imagem/ícone
  for (const m of html.matchAll(/<img\b[^>]*>/gi)) {
    if (!/\balt\s*=/.test(m[0])) add("R11", "<img> sem alt");
  }
  for (const m of html.matchAll(/<button\b([^>]*)>([\s\S]*?)<\/button>/gi)) {
    const attrs = m[1];
    const inner = m[2].replace(/<[^>]+>/g, "").trim();
    const onlyIcon = /<(?:i|svg)\b/.test(m[2]) && inner === "";
    if (onlyIcon && !/aria-label\s*=/.test(attrs)) add("R11", "botão só com ícone sem aria-label");
  }

  // R12 type em button
  for (const m of html.matchAll(/<button\b[^>]*>/gi)) {
    if (!/\btype\s*=/.test(m[0])) {
      add("R12", "<button> sem type");
      break;
    }
  }

  // R13 ids duplicados
  const ids = [...html.matchAll(/\sid=["']([^"']+)["']/g)].map((m) => m[1]);
  const dupes = ids.filter((v, i) => ids.indexOf(v) !== i);
  if (dupes.length) add("R13", `id duplicado: ${[...new Set(dupes)].slice(0, 3).join(", ")}`);

  // R14 estados (páginas de catálogo/documentação não têm ciclo de dados)
  if (spec?.archetype !== "catalog") {
    const hasEmpty = /ttsc-empty-state|data-state=["']empty["']/.test(html);
    const hasLoading = /ttsc-skeleton|data-state=["']loading["']/.test(html);
    const hasError = /data-state=["']error["']|ttsc-alert-destructive/.test(html);
    const missing = [!hasEmpty && "vazio", !hasLoading && "carregando", !hasError && "erro"].filter(Boolean);
    if (missing.length) add("R14", `sem estado(s): ${missing.join(", ")}`);
  }

  // R16 renderizador genérico de páginas (atributo, não texto explicativo)
  if (/\sdata-model(?:-[a-z]+)?\s*=/.test(html)) add("R16", "renderizador genérico (data-model*=) proibido");

  // R17 script inline
  if (/<script(?![^>]*\bsrc=)[^>]*>[\s\S]*?<\/script>/i.test(html)) add("R17", "<script> inline com código");

  // R18 script de página como módulo
  for (const m of html.matchAll(/<script\b[^>]*>/gi)) {
    const tag = m[0];
    const src = (tag.match(/\bsrc=["']([^"']+)["']/i) || [])[1];
    if (src && !/bundle\.js$/.test(src) && !/type=["']module["']/i.test(tag)) {
      warn("R18", `script sem type=module: ${src}`);
    }
  }

  results.push({ rel, bytes, errors, warnings, cssText, classes, html });
}

// R7 anti-sameness
for (const [archetype, list] of archetypeVariants) {
  const seen = new Map();
  for (const item of list) {
    if (seen.has(item.variant)) {
      const other = seen.get(item.variant);
      for (const r of results) {
        if (r.rel === item.file || r.rel === other) {
          r.errors.push(`R7 variante "${item.variant}" repetida no arquétipo ${archetype} (${item.file} e ${other})`);
        }
      }
    } else seen.set(item.variant, item.file);
  }
}

// Relatório
const totalErrors = results.reduce((n, r) => n + r.errors.length, 0);
const totalWarnings = results.reduce((n, r) => n + r.warnings.length, 0);

if (REPORT) {
  const noSpec = results.filter((r) => r.errors.some((e) => e.startsWith("R6"))).length;
  const literal = results.filter((r) => r.errors.some((e) => e.startsWith("R3"))).length;
  const palette = results.filter((r) => r.errors.some((e) => e.startsWith("R4"))).length;
  const big = results.filter((r) => r.bytes > 80 * 1024).length;
  const noWrapper = results.filter((r) => r.errors.some((e) => e.startsWith("R9"))).length;
  console.log(`\nDívida do design system — ${results.length} páginas\n`);
  console.log(`  sem page-spec ............ ${noSpec}`);
  console.log(`  cor literal .............. ${literal}`);
  console.log(`  utilitário de cor cru .... ${palette}`);
  console.log(`  tabela sem wrapper ....... ${noWrapper}`);
  console.log(`  acima de 80 KB ........... ${big}`);
  console.log(`  erros totais ............. ${totalErrors}`);
  console.log(`  avisos ................... ${totalWarnings}`);
  const top = [...results].sort((a, b) => b.bytes - a.bytes).slice(0, 5);
  console.log("\n  maiores páginas:");
  for (const r of top) console.log(`    ${(r.bytes / 1024).toFixed(0).padStart(5)} KB  ${r.rel}`);
  console.log("");
  process.exit(0);
}

let failed = 0;
for (const r of results) {
  if (!r.errors.length && !r.warnings.length) {
    console.log(`✔ ${r.rel}`);
    continue;
  }
  if (r.errors.length) failed++;
  console.log(`\n${r.errors.length ? "✖" : "⚠"} ${r.rel}  (${(r.bytes / 1024).toFixed(1)} KB)`);
  for (const e of r.errors) console.log(`   ✖ ${e}`);
  for (const w of r.warnings) console.log(`   ⚠ ${w}`);
}

console.log(
  `\n${results.length} arquivo(s): ${failed} reprovado(s), ${totalErrors} erro(s), ${totalWarnings} aviso(s).`
);
process.exit(failed ? 1 : 0);
