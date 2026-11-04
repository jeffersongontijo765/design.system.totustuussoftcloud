# 11 — Governança, Qualidade e Processo de Entrega

> Parte do [SDD v2](00-README.md).

---

## 1. Processo de entrega (EGM)

O processo segue o Elephant-Goldfish Model (plugin `egm`, marketplace `google/elephant-goldfish-model`):

1. **Brief** — problema, objetivos, restrições e alternativas descartadas, em linguagem simples. Saída: `concepts_brief.md`.
2. **Rascunho** — documento de design com problema, objetivos e não objetivos, plano técnico, alternativas e plano de testes. Saída: `design_draft.md` ou o documento da seção do SDD.
3. **Revisão por leitores sem contexto** — pelo menos dois leitores com contexto limpo, que recebem só o documento e o código referenciado. Procuram suposições não declaradas e lacunas. Saída: relatório de achados.
4. **Decisão humana** — o autor resolve trade-offs e aprova. Achados resolvidos ou aceitos com justificativa.
5. **Implementação** — só depois da aprovação.
6. **Verificação** — testes automatizados e revisão de código. Leitores sem contexto não substituem testes.

Regras:

- Decisões com mais de uma alternativa defensável são apresentadas ao autor com mecanismo, trade-offs e condições de falha. Não são escolhidas pelo agente.
- Todo documento de decisão tem data, autor e status.
- Afirmação de estado sem evidência é marcada como **[Declarado]** (ver [00](00-README.md)).

## 2. Definition of Done

Uma história ou tarefa só é concluída quando:

- [ ] Critério de aceite do requisito atendido e testado.
- [ ] Testes unitários e de integração adicionados para o caminho feliz e para os dois principais erros.
- [ ] Isolamento de tenant e autorização cobertos quando a mudança toca dados.
- [ ] Sem `on*=` nem script inline em HTML novo.
- [ ] Textos em chaves de i18n com `en` e `pt-BR` preenchidos.
- [ ] Logs sem PII.
- [ ] Documentação de API atualizada quando o contrato muda.
- [ ] Revisão de código aprovada por pessoa diferente do autor.
- [ ] Mudança em autenticação, autorização, cripto, upload ou pagamento revisada por pessoa com perfil de segurança.

## 3. Gates

| Gate | Quando | Critério |
|---|---|---|
| G1 — Arquitetura | Antes de módulo novo | ADR aprovado; leitores sem contexto revisaram o design |
| G2 — Acesso | Antes de módulo com dados pessoais | Permissões definidas; matriz de isolamento escrita |
| G3 — Homologação | Antes de publicar em homologação | Pipeline verde; DAST sem achado médio ou superior não tratado |
| G4 — Produção | Antes de publicar em produção | Checklist de go-live ([10](10-implantacao-operacao.md), seção 9) completo; aprovação de responsável de segurança |

## 4. Registro de decisões (ADR)

- Arquivo `adr/NNNN-titulo.md` no repositório de código ou nesta pasta, conforme o caso.
- Campos: contexto, decisão, alternativas, consequências, status (proposta, aceita, substituída).
- Mudança de decisão aceita cria novo ADR que substitui o anterior. ADR antigo não é apagado.

## 5. Papéis

| Papel | Responsabilidade |
|---|---|
| Autor do produto | Aprova escopo, decisões em aberto da seção 5 do [00](00-README.md) |
| Responsável técnico | Arquitetura, ADRs, gates G1 a G4 |
| Responsável de segurança | Revisões da seção 1 de [05](05-seguranca.md), resposta a incidentes |
| Encarregado de dados (DPO) | Relatório de impacto, incidentes, direitos do titular |
| Equipe de desenvolvimento | Implementação, testes, documentação |

Nomes das pessoas ficam no registro de responsáveis privado, não neste SDD. A v1 tinha tabela RAI com nomes; a v2 mantém apenas os papéis.

## 6. Uso de ferramentas de IA no desenvolvimento

- Ferramentas de agentes (por exemplo o plugin `egm`, o `fable-method` ou o `oh-my-opencode-slim`, citados na v1) são ferramentas de **processo**. Não são requisito do produto.
- Instalação com versão fixada, após leitura do código de instalação. Sem `@latest`. O plugin `egm` é instalado a partir de `google/elephant-goldfish-model` em commit fixo, com SHA registrado no repositório de código antes do uso.
- Agentes trabalham com permissão mínima no repositório. Não recebem credenciais de produção.
- Código gerado passa pelo mesmo Definition of Done que código escrito à mão.
- Conteúdo de ferramentas externas (páginas, documentos, saídas de ferramenta) é tratado como dado não confiável.

## 7. Qualidade de código

- Limite de referência: controller com até 500 linhas. Acima disso, abrir tarefa de extração. (A v1 cita controllers com mais de 5.000 linhas.)
- Análise estática em CI com nível acordado e aumentado a cada trimestre.
- Cobertura: código novo com cobertura mínima de 80% das linhas de serviço. Meta global a definir após medição.
- Revisão de documentação: SDD revisado a cada release e, no mínimo, a cada trimestre.

## 8. Backlog priorizado (próximas entregas)

| Prioridade | Item | Referência | Dono |
|---|---|---|---|
| Alta | Remover `scratch/` e scripts de sessão do artefato e do repositório | [05](05-seguranca.md), seção 3 | Responsável técnico |
| Alta | Eliminar `on*=` nas views e ativar CSP com nonce | [08](08-frontend-design-system.md) | Frontend |
| Alta | Implementar `TotusTuus\Vault` e definir onde fica a chave-mestra | D-02, ADR-05 | Responsável técnico |
| Alta | Separar `JWT_SECRET` do segredo de proteção de ativos | [05](05-seguranca.md), seção 2 | Backend |
| Média | Implementar token de dispositivo (D-03) | [06](06-identidade-acesso.md), seção 7 | Backend |
| Média | Licença Font Awesome Pro para hospedagem: confirmada pelo autor em 03/11/2026 | D-01, [08](08-frontend-design-system.md) | Autor |
| Alta | Confirmar uso de `JWT_SECRET` e remover HS256 | [05](05-seguranca.md) | Backend |
| Alta | Substituir bloqueio de conta por atraso progressivo | [06](06-identidade-acesso.md), seção 6 | Backend |
| Média | Passkey obrigatória para contas de plataforma | [06](06-identidade-acesso.md), seção 10 | Segurança |
| Média | Remover exigência de rotação periódica de senha | [06](06-identidade-acesso.md), seção 3 | Produto |
| Média | ROPA completo, prazos de retenção aprovados, parecer de legítimo interesse (LIA) e fluxo de consentimento de menores. Prazo: 30 dias antes do go-live | [07](07-privacidade-lgpd.md) | DPO |
| Média | Gerar SBOM e assinar artefato | [10](10-implantacao-operacao.md) | DevOps |
| Média | Consolidar documentos duplicados da v1 | [12](12-catalogo-modulos.md) | Produto |
| Baixa | Reduzir tamanho de controllers | seção 7 | Backend |
