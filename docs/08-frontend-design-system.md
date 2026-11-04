# 08 — Frontend e Design System

> Parte do [SDD v2](00-README.md). Segurança de cabeçalhos e CSP em [05](05-seguranca.md).

---

## 1. Abordagem

Interface progressiva: páginas renderizadas no servidor, com melhoria por JavaScript para interações (`fetch()`, filtros, modais). A aplicação funciona com JavaScript desligado nas telas de leitura e de formulário.

## 2. Regras de segurança do frontend

1. **Sem JavaScript inline** e **sem atributos de evento inline** (`onclick`, `onchange`, `onsubmit` etc.). Eventos são ligados em arquivos `.js` externos. (ADR-07.)
2. **Scripts com nonce** gerado por requisição. Sem `unsafe-inline` nem `unsafe-eval`.
3. **Sem tokens em `localStorage` ou `sessionStorage`.** Autenticação por cookie `HttpOnly`.
4. **Requisições** com `credentials: 'same-origin'` (ou `'include'` apenas em domínio de API documentado).
5. **Conteúdo do usuário** é escapado no servidor e, quando inserido pelo cliente, com `textContent` ou sanitizador com lista branca. Nunca `innerHTML` com dado não confiável.
6. **Service worker** (`sw.js`) não cacheia respostas autenticadas nem endpoints de API.
7. **Dependências de terceiros** ficam no próprio domínio (ver seção 4).

## 3. Layout e navegação

- Navegação lateral por contexto: principal (ícones) e sub-navegação por módulo, com busca.
- Telas de lista seguem um padrão único: cabeçalho com ações, barra de filtros, tabela ou cartões, paginação, exportação.
- Visões alternativas (KPIs, tabela, cartões, kanban, gráficos) são opcionais por tela e não podem ocultar dados que a permissão do usuário permite ver.
- Exportação: CSV, XLSX, PDF, JSON. XML, SQL e TXT da v1 **[Declarado]** entram só com requisito de negócio, porque exportar SQL e XML de dados pessoais amplia a superfície de vazamento.
- Exportação de CSV neutraliza células que começam com `=`, `+`, `@`, tabulação ou retorno de carro. Números negativos são exportados como número, sem prefixo (ver [05](05-seguranca.md)).
- Ações destrutivas: confirmação com digitação do nome do objeto, não de uma palavra genérica. Ação de arquivamento não usa a mesma confirmação que exclusão.

## 4. Design system

- Tokens de cor, espaçamento e tipografia em variáveis CSS, com tema claro e escuro.
- Tema da v1 (**[Declarado]**): paleta escura com fundo `#14171c`, superfícies `#1a1d24` e `#242832`, acento `#10b981`. Os valores são tokens de referência, não constantes espalhadas no código.
- Contraste mínimo WCAG 2.2 AA: texto normal 4.5:1, texto grande e componentes de interface 3:1. Verificação automatizada em CI.
- Foco visível em todo controle interativo. Navegação completa por teclado.
- Tamanho mínimo de alvo de toque: 24×24 CSS px (WCAG 2.2 AA, 2.5.8), recomendado 44×44 em telas de uso móvel.

### Ícones (decisão D-01)

A v1 declara Font Awesome Pro 7.2 "Light" em toda a interface e carrega o Font Awesome de CDN (versão gratuita 7.0.0 em `teste.html`). Problemas:

- A licença Pro não permite servir os arquivos a partir de CDN público sem assinatura válida. Licença confirmada pelo autor em 03/11/2026: permite servir os arquivos do próprio domínio.
- A v1 diz "sem bibliotecas externas de runtime" e, ao mesmo tempo, depende de CDN.

Opções para o autor escolher:

| Opção | Mecanismo | Trade-off | Falha quando |
|---|---|---|---|
| (a) Self-host da licença Pro | Arquivos copiados para `assets/vendor/` no build | Mantém o visual atual; exige revisar termos de licença de redistribuição | Licença não cobre uso em aplicação web hospedada por terceiros |
| (b) Biblioteca open source | Ícones SVG locais, licença MIT/ISC | Sem custo recorrente; pode exigir ajuste visual em ícones específicos | Equipe não aceita mudança visual |
| (c) CDN com licença confirmada | `<link>` externo com SRI (`integrity`) | Depende de terceiro; CSP precisa liberar o domínio | Domínio do CDN sai do ar ou a licença expira |

**Decisão do autor (02/11/2026): opção (a).** O Font Awesome Pro é servido do próprio domínio a partir de `assets/fonts/fontawesome.v7.2.0/` (já presente no projeto). Nenhum CDN de ícones em produção. Condição: confirmar, nos termos da licença, que ela cobre a hospedagem da aplicação para os tenants. Caso não cubra, a decisão volta para (b).

## 5. Desempenho

- Orçamento: LCP ≤ 2,5 s e INP ≤ 200 ms no percentil 75 em rede 4G simulada para telas de lista.
- Imagens com `width`/`height`, `loading="lazy"` abaixo da dobra e formato moderno quando suportado.
- JavaScript carregado por tela, não global. Sem bibliotecas de runtime que dupliquem recursos nativos.
- Tailwind CSS compilado no build, com somente as classes usadas (purge). Sem CDN do Tailwind em produção.

## 6. Responsividade

- Layout funciona de 320 px de largura sem rolagem horizontal da página. Tabelas largas rolam dentro do próprio componente.
- Teste manual em tela de 320 px, 375 px e 1280 px em cada release de tela nova.

## 7. Telas de referência

A v1 aponta uma página de módulos como referência visual oficial, com endereço de `localhost`. Referências não devem apontar para ambiente local. A v2 mantém um catálogo de telas de referência em homologação, com captura de tela versionada no repositório de design.

## 8. Critérios de aceite de frontend

- [ ] Nenhum `on*=` em HTML e nenhum `<script>` inline (verificação automatizada).
- [ ] Nenhum recurso externo sem SRI e fora da lista de domínios aprovados (lista publicada após a decisão D-01).
- [ ] Contraste verificado por ferramenta em cada tema.
- [ ] Teste de teclado para fluxo de criação e edição.
- [ ] Textos vindos de chaves de i18n, sem texto fixo em PT ou EN no código.
- [ ] Tela testada em 320 px, 375 px e 1280 px.

---

## 9. Template de sala de aula e reunião

Decidido em 03/11/2026 ([40](40-aulas-online-por-portal.md), seção 4.4). A sala usa o template do portal em que a pessoa está, com layout de reunião estilo Zoom. Não há identidade visual própria da sala.

### 9.1 Regiões

| Região | Conteúdo | Comportamento |
|---|---|---|
| Barra superior | Nome da sessão, tempo decorrido, indicador de gravação, sair | Fixa. Indicador de gravação nunca some enquanto ela durar |
| Área de vídeo | Grade de participantes. Quem fala tem destaque | Em telas pequenas, uma coluna. Em telas largas, grade ajustada ao número de participantes |
| Painel lateral | Participantes e chat, em abas alternáveis | Em telas pequenas, vira aba em tela cheia, não coluna |
| Barra de ação | Microfone, câmera, compartilhar tela, levantar a mão, sair | Fixa na parte inferior. Botões com rótulo, não só ícone |

### 9.2 Estados e regras visuais

- Microfone, câmera e gravação têm estado comunicado por ícone **e** texto. Cor não é o único indicador.
- Gravação ativa tem marca visível e textual, e o aviso de gravação aparece ao entrar.
- Estado de aluno com câmera desligada é mostrado como avatar com nome, sem imagem.
- Participante na sala de espera aparece para o moderador com nome e botão de admitir.

### 9.3 Temas e identidade

- Usa os tokens de cor do portal ([08](08-frontend-design-system.md), seção 4), nos temas claro e escuro do portal.
- O estilo escuro com verde-esmeralda da v1 não é obrigatório.
- Textos vêm de chaves de i18n ([09](09-internacionalizacao.md)).

### 9.4 Teclado e acessibilidade

- Atalhos para microfone, câmera e sair, com lista visível de atalhos.
- Ordem de foco: barra superior, área de vídeo, painel lateral, barra de ação.
- Anúncio de entrada e saída de participante para leitor de tela, sem repetir a cada atualização de vídeo.

### 9.5 Critérios de aceite

- [ ] Sala testada em 320 px, 375 px e 1280 px, sem rolagem horizontal.
- [ ] Estado de microfone e câmera legível sem cor (teste de contraste e de leitura por texto).
- [ ] Indicador de gravação visível em todo o período de gravação (teste).
- [ ] Sala usa tokens do portal nos dois temas.
- [ ] Todo o fluxo de entrar, falar e sair funciona só com teclado.
