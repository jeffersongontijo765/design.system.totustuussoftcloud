# 30 — Cache: Camadas, Chaves, Validade e Invalidação

> Parte do [SDD v2](00-README.md). Isolamento por entidade e unidade em [03](03-dominio-tenancy.md). Sessão e vínculos em [06](06-identidade-acesso.md), seção 12. Filas em [14](14-integracao-modulos.md). Infraestrutura em [10](10-implantacao-operacao.md).
> **Status:** especificação proposta. Os valores de validade são iniciais e devem ser medidos em homologação.

---

## 1. Princípio

Cache é uma cópia derivada, nunca uma fonte de verdade. Duas regras definem tudo o que vem depois:

1. **Nenhum dado de cache pode mostrar informação de outro contexto.** A chave sempre inclui o contexto que o dado pertence.
2. **Dado de decisão de segurança ou financeira não é cacheado** ou é lido com validade mínima e revalidado antes da ação.

---

## 2. Camadas

| Camada | Onde | O que guarda | Validade padrão |
|---|---|---|---|
| Cache de aplicação | Redis (ou equivalente), por ambiente | Leituras de catálogo, configuração, contadores | Ver seção 4 |
| Cache de consulta | Dentro do banco da unidade | Resultados agregados de relatório | Ver seção 4 |
| Cache de borda | CDN | Apenas arquivos públicos e recursos estáticos versionados | Até a próxima versão |
| Cache de navegador | Navegador | Recursos estáticos com versão no nome | Longa, por versão |

Não existe cache de navegador para HTML autenticado nem para resposta de API autenticada ([08](08-frontend-design-system.md), seção 2).

---

## 3. Chaves

Formato obrigatório:

```
{ambiente}:{entidade_uuid}:{unidade_uuid}:{classe}:{identificador}[:{escopo}]
```

| Componente | Regra |
|---|---|
| `ambiente` | `prod`, `hml`, `dev`. Chave de um ambiente não é lida por outro. |
| `entidade_uuid`, `unidade_uuid` | Obrigatórios para dado de unidade. Para dado de plataforma, usar `plataforma`. |
| `classe` | Ver seção 4 |
| `identificador` | Chave do objeto |
| `escopo` | Papel ou conta, quando a resposta depende de permissão. Ex.: `escopo=papel:coordenador`. |

Regras adicionais:

- Resposta que depende de permissão inclui o escopo na chave. Resposta sem escopo não depende de quem consulta.
- Chave sem entidade ou unidade é recusada pela biblioteca de cache. Não há exceção.
- Nenhum CPF, e-mail ou telefone aparece em chave. Usar hash HMAC.

---

## 4. Classes e validade

| Classe | Exemplo | Validade | Invalidação |
|---|---|---|---|
| Catálogo | Cursos, séries, locales, papéis padrão | 1 h | Por evento de alteração do catálogo |
| Configuração | Parâmetros do tenant, política de MFA | 5 min | Imediata ao alterar |
| Permissão | Vínculos e papéis da conta | 30 s | Imediata ao alterar vínculo ([06](06-identidade-acesso.md), seção 12.4) |
| Contador | Quantidade de vagas, saldo de quota | Não cacheado ou 5 s | Por transação |
| Relatório agregado | Painel de indicadores | 5 min | Por evento do módulo de origem |
| Busca | Índice e resultados recentes | Conforme [21](21-busca-e-armazenamento.md) | Por evento de indexação |
| Arquivo público | Imagem institucional | Até a próxima versão | Por nova versão |
| Sessão | Token e sessão | **Não é cache.** Fica na tabela de sessão ou no armazenamento de sessão. | Por revogação |

### 4.1 Nunca cacheado

- Dado de pagamento, saldo de conta, status de cobrança antes da ação de pagamento ([20](20-pagamentos-seguranca.md)).
- Cadastro civil de pessoa ([14](14-integracao-modulos.md), seção 3), exceto a referência `person_id`.
- Resposta autenticada de API ou de tela.
- Resultado de consulta por CPF ([21](21-busca-e-armazenamento.md), seção 6.8). Cada consulta é nova e auditada.
- Dado de saúde.
- Segredo, token e credencial ([05](05-seguranca.md)).

---

## 5. Invalidação

- **Por evento:** a alteração publica evento no fluxo de [14](14-integracao-modulos.md). Consumidor de cache remove as chaves afetadas.
- **Por versão:** chave inclui uma versão do objeto. Alterar o objeto incrementa a versão. A chave antiga expira sozinha.
- **Por tempo:** validade mínima sempre. Nenhuma chave é permanente.
- **Limite de propagação:** invalidação chega em até 5 s. Para permissão, a regra da seção 4 (30 s) vale no pior caso, e a cópia do token é revalidada com `mv` ([06](06-identidade-acesso.md), seção 12.4).

---

## 6. Proteção

| Ameaça | Controle |
|---|---|
| Vazamento entre contextos | Chave com entidade e unidade. Teste de regressão. |
| Envenenamento de cache | Só o próprio serviço grava. Dado externo não entra no cache sem validação. |
| Estouro de cache (stampede) | Recomputação com trava por chave. Validade com variação aleatória de até 10%. |
| Dado sensível em memória | Redis com autenticação, TLS e rede privada. Sem persistência em disco para classes com dado pessoal. |
| Cache de erro | Erro não é cacheado, salvo erro de "não encontrado" com validade de 30 s. |
| Chave previsível | Chave de dado de unidade inclui o UUID da unidade. Acesso por identificador adivinhado é negado pela autorização. |

---

## 7. Operação

- Métricas: taxa de acerto por classe, memória por ambiente, latência, invalidações por minuto.
- Alerta: taxa de acerto abaixo de 60% em classe de catálogo; uso de memória acima de 80%.
- Limpeza: nenhum comando de limpeza total em produção sem aprovação registrada.
- Ambientes: cache de homologação nunca é o de produção. Teste de isolamento roda com cache ligado.

---

## 8. Testes obrigatórios

- Dado da unidade A não aparece na consulta da unidade B, mesmo com identificador igual.
- Dado com escopo de papel não aparece para papel sem permissão.
- Alteração de vínculo reflete em até 30 s, e a requisição com token antigo é revalidada.
- Consulta por CPF nunca retorna do cache.
- Dado de saúde não entra em nenhuma chave de cache (varredura).
- Stampede: 1.000 requisições simultâneas em chave expirada geram uma recomputação.

---

## 9. Lacunas

| # | Lacuna | Dono |
|---|---|---|
| CAC-01 | Dimensionamento do Redis por ambiente e entidade. **Decisão do autor (03/11/2026):** dimensionar em homologação antes de produção. | Operação |
| CAC-02 | Validades medidas em homologação. **Decisão do autor (03/11/2026):** medir em homologação; os valores da seção 4 são o ponto de partida. | Responsável técnico |
| CAC-03 | Escolha do provedor de CDN | Operação |

---

## 10. Critérios de aceite

- [ ] Toda chave segue o formato da seção 3, validado pela biblioteca.
- [ ] Classes da seção 4.1 não são cacheadas (teste automatizado).
- [ ] Invalidação por evento testada para catálogo, configuração e permissão.
- [ ] Testes da seção 8 passando em CI.
- [ ] CAC-01 e CAC-02 medidas e registradas em homologação antes de produção.
