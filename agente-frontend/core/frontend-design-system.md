# Front-end com design system

Objetivo: toda tela é montada com componentes que já existem no design system do projeto. Não recriar componente catalogado nem criar um estilo paralelo. Quando um componente falta, ele entra no design system primeiro, depois é usado.

## 1. Localizar o design system

Procure no repositório, nesta ordem:
- uma pasta chamada `design-system`, `ds`, `ui` ou `components`, com uma subpasta por componente e um `README.md` em cada uma;
- um pacote de UI (`packages/ui`, `src/components`) com documentação em `README.md` ou `docs/`;
- os tokens (`tokens.json`, `theme.css`, variáveis CSS `--…`, `tailwind.config.*`).

Se não houver design system, diga isso e proponha criar um antes de montar telas.

## 2. Gerar o índice

```bash
python3 scripts/gera_indice.py <pasta-do-design-system> docs/componentes.md
```

O índice dá o nome, a finalidade e o caminho da documentação de cada componente. Regere quando o design system mudar.

## 3. Escolher o componente

1. Procure no índice pelo tipo de necessidade (tabela, KPI, drawer, gráfico, aviso, select, paginação, etc.).
2. Leia o README do componente: API, anatomia, variantes, acessibilidade e o que não fazer.
3. Olhe o exemplo ao vivo (`preview.html`, storybook ou página de demonstração), se existir.
4. Reutilize partials e componentes que o próprio projeto já usa antes de escrever marcação nova.

## 4. Montar a tela

- Use as classes, atributos e slots previstos no README. Não invente nomes.
- Use os tokens do projeto (`var(--…)` ou classes do tema). Não use cor, espaçamento, raio ou sombra literal.
- Não altere a casca do app (cabeçalho, navegação, rodapé, breadcrumb) dentro de uma tela de conteúdo.
- Textos vêm da camada de traduções do projeto, nunca fixos no template.
- Trate estados: carregando, vazio, sem resultado, erro, acesso negado e sucesso. Erro não vira zero, e ausência de dado não vira valor de exemplo.
- Escape de saída, atributos de acessibilidade conforme o README, e funcione no tema claro e no escuro.

## 5. Verificar

- Rode o lint ou o build do projeto nos arquivos alterados.
- Renderize a tela e confira no navegador: console sem erro, largura estreita e larga, tema claro e escuro.
- Compare com uma tela de referência do próprio projeto, quando houver.

## 6. Componente ausente

Não crie um componente novo dentro da tela. Registre a lacuna: nome, uso pretendido e o componente mais próximo. Se for pedido, crie o componente no design system, com README e exemplo, e só então use.

## Entrega

Informe:
- os componentes usados, com o caminho do README de cada um;
- os componentes que faltaram e o que foi feito a respeito;
- as verificações feitas e as que não foram feitas.
