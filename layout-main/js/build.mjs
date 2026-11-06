// build.mjs — junta os módulos do chassi num script comum (js/layout.bundle.js).
//
// Por quê: navegador não carrega <script type="module"> de file://. Com o bundle,
// o index.html abre com duplo clique, sem servidor. Os módulos em js/chassi/ continuam
// sendo a fonte; rode isto depois de editar qualquer um:  node layout-main/js/build.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const ordem = ["util", "theme", "drawers", "rail", "sub-sidebar", "search", "menus"];

const corpo = ordem.map((nome) => {
  const src = fs.readFileSync(path.join(dir, "chassi", `${nome}.js`), "utf8")
    .replace(/^import .*?;\s*$/gm, "")        // tudo fica no mesmo escopo
    .replace(/^export /gm, "");
  return `// ---- chassi/${nome}.js ----\n${src.trim()}\n`;
}).join("\n");

const init = fs.readFileSync(path.join(dir, "layout.js"), "utf8")
  .split("\n").filter((l) => /^init\w+\(\);$/.test(l)).join("\n  ");

const out = `// layout.bundle.js — GERADO por js/build.mjs a partir de js/chassi/*.js. Não edite aqui.
(function () {
"use strict";
${corpo}
// ---- início (js/layout.js) ----
window.TTSCLayout = { normalize };
  ${init}
})();
`;
fs.writeFileSync(path.join(dir, "layout.bundle.js"), out);
console.log(`gerado: js/layout.bundle.js (${out.length} bytes)`);
