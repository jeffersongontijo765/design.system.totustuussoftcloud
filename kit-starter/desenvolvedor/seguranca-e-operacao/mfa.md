# MFA (autenticação multifator)

- Portal: Desenvolvedor (`desenvolvedor.`)
- Área: Segurança e operação
- Domínio: plataforma (banco master), instância separada do módulo das entidades ([31](../../../docs/v2/31-matriz-portais-modulos.md), seção 2.1)
- Status: detalhado a partir do SDD v2 (sem especificação própria na v1)
- Fonte da v1: sem especificação própria (regras no SDD v2, seção 4 desta ficha)

## 1. Regra de leitura
Não há especificação própria na v1. Valem as regras do SDD v2 citadas nesta ficha.

## 2. Objetivo e escopo
Configurar e acompanhar a autenticação multifator de todas as contas, com regra mais forte para contas de plataforma.

## 3. Telas
- **Política de MFA** (configuração): fatores aceitos, obrigatoriedade por tipo de conta e por papel.
- **Painel de MFA** (dashboard): contas com e sem MFA por portal, passkeys cadastradas, contas de plataforma sem passkey.
- **Fatores da conta** (drawer em Acesso): cadastrar, revogar e recuperar fator, com step-up.


## 4. Correções da v2 que prevalecem
- **MFA** conforme o [06](../../../docs/v2/06-identidade-acesso.md), seção 5: fatores, cadastro e recuperação. **SMS não é fator de MFA** ([16](../../../docs/v2/16-integracoes-externas.md), seção 2).
- **Contas de plataforma:** passkey obrigatória; conta sem passkey é desativada no primeiro login após a migração ([06](../../../docs/v2/06-identidade-acesso.md), seção 10).
- **Step-up:** ações sensíveis (exportação, alteração de papel, exclusão, ver segredo de integração) exigem autenticação recente ([78](../../../docs/v2/78-permissoes-e-papeis.md), seção 5).
- A especificação de autenticação da v1 que trata de MFA está absorvida na ficha [acesso.md](acesso.md).

## 5. Decisões por padrão aplicadas
- Nenhuma decisão nova.

## 6. Permissões e papéis
- `platform.security`: política de MFA e painel.
- Cada usuário: os próprios fatores.

## 7. Dados
- Fatores e passkeys no master, cifrados ([05](../../../docs/v2/05-seguranca.md)).

## 8. Integrações
- E-mail transacional para recuperação (D-04).

## 9. Exportação, auditoria e privacidade
- Exportação de listas: CSV, XLSX, PDF e JSON, com permissão de exportação e step-up; CSV com células neutralizadas ([08](../../../docs/v2/08-frontend-design-system.md), seção 3).
- Auditoria conforme [29](../../../docs/v2/29-auditoria.md); dados pessoais conforme [07](../../../docs/v2/07-privacidade-lgpd.md).


## 10. Estados de interface
- Carregando (skeleton), vazio com chamada para ação, sem resultado, erro, acesso negado, registro bloqueado ou baixado (somente leitura).

## 11. Requisitos de frontend
- Sem JavaScript inline nem atributos `on*=`; textos por chave de i18n; tema claro e escuro; WCAG 2.2 AA; 320 px sem rolagem horizontal ([08](../../../docs/v2/08-frontend-design-system.md)).
- Componentes do design system (índice em `docs/design-system/template/components/` no projeto e skill `agente-frontend`).

## 12. Pendências
- Nenhuma além das do [06](../../../docs/v2/06-identidade-acesso.md).

