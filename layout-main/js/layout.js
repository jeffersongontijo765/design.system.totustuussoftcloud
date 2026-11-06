// layout.js — entrada do chassi (header | rail | sub-sidebar | container | footer).
//
// Carregue uma vez por página:  <script type="module" src="js/layout.js"></script>
// Cada comportamento é um módulo em js/chassi/ que recebe o DOM pronto e não conhece a
// página (docs/ai/js-architecture.md). Nada de handler inline (R2, R17).
//
//   chassi/theme.js        tema claro/escuro
//   chassi/drawers.js      gavetas do rail e do sub-sidebar abaixo de 1100px
//   chassi/rail.js         fixar o rail expandido; grupos do rail lembram estado
//   chassi/sub-sidebar.js  recolher/expandir, seções sanfona, filtro e atalho "/"
//   chassi/search.js       busca global, Ctrl+K / ⌘K, busca no celular
//   chassi/menus.js        menus do header e seletores de contexto
//   chassi/util.js         preferências (localStorage com try/catch) e utilitários
import { initTheme } from "./chassi/theme.js";
import { initDrawers } from "./chassi/drawers.js";
import { initRailPin, initPortalGroups } from "./chassi/rail.js";
import { initCollapse, initAccordions, initFilter } from "./chassi/sub-sidebar.js";
import { initSearch } from "./chassi/search.js";
import { initMenus } from "./chassi/menus.js";

initTheme();
initDrawers();
initRailPin();
initPortalGroups();
initCollapse();
initAccordions();
initFilter();
initSearch();
initMenus();
