# Especificação Completa — Gestão de Documentos Acadêmicos + Builder Universal de Documentos

Documento funcional e técnico para criação, configuração, versionamento, renderização, emissão e validação de qualquer documento acadêmico, administrativo, financeiro ou contratual, com suporte a builder visual, layout de impressão avançado, múltiplos tamanhos de papel, cabeçalho, rodapé, margens, identação, paginação e regras de negócio.

- Language Standard: Global English
Baseado na tela observada em **Secretaria > Modelos de documentos**, com filtros por período letivo, unidade, turma e aluno, e agrupamento por tipo documental como aditivo, contratos e declarações. [cite:1]

[image:1]

## 1. Visão geral

O módulo deve permitir que a instituição crie, mantenha e emita documentos padronizados a partir de modelos reutilizáveis, parametrizados e versionados. A tela atual indica um catálogo de modelos por tipo documental com contexto acadêmico por período, unidade, turma e aluno, o que exige um motor de geração contextual e rastreável. [cite:1]

O objetivo não é apenas armazenar arquivos, mas prover uma plataforma de **Document Template Management + Document Builder + Rendering Engine + Issuance Workflow**, capaz de atender desde uma declaração simples até contratos complexos com assinatura, QR code, múltiplas páginas e requisitos formais de impressão.

## 2. Objetivos do módulo

- Padronizar todos os documentos institucionais.
- Eliminar edição manual repetitiva em Word, LibreOffice ou editores externos.
- Permitir criação de modelos com baixa dependência técnica.
- Garantir versionamento, aprovação e trilha de auditoria.
- Possibilitar emissão individual ou em lote.
- Suportar layout profissional de impressão e PDF.
- Adaptar o mesmo builder para qualquer formato de papel.
- Atender cenários multiunidade, multicurso e multientidade.

## 3. Escopo funcional

O módulo deve cobrir:

- Tipos documentais.
- Modelos documentais.
- Versionamento de modelos.
- Builder visual e técnico.
- Biblioteca de variáveis.
- Regras condicionais.
- Pré-visualização responsiva e de impressão.
- Emissão individual.
- Emissão em lote.
- Geração de PDF.
- Cabeçalho e rodapé configuráveis.
- Assinatura e autenticação.
- Validação pública.
- Revogação e reemissão.
- Auditoria completa.

## 4. Tipos documentais suportados

A lista inicial deve incluir, no mínimo, os tipos mostrados na tela atual, como aditivo, contratos, declaração de conclusão de curso, declaração de frequência, declaração de matrícula, declaração de quitação, declaração de transferência e etiqueta do aluno. [cite:1]

Também deve aceitar expansão para:

- Termos de responsabilidade.
- Requerimentos.
- Autorizações.
- Boletos acompanhados de instruções.
- Comunicados institucionais.
- Certificados.
- Atas.
- Relatórios acadêmicos.
- Fichas cadastrais.
- Dossiês do aluno.
- Declarações personalizadas.

## 5. Arquitetura conceitual

O módulo deve ser dividido em componentes independentes:

- **Document Type Service**: cadastro e política por tipo documental.
- **Template Catalog Service**: cadastro de modelos e escopos.
- **Template Version Service**: snapshots, histórico, rollback e comparação.
- **Document Builder Service**: edição visual/técnica do layout.
- **Rendering Engine**: interpretação do template e geração final.
- **Rule Engine**: validação de elegibilidade e lógica condicional.
- **Issuance Service**: emissão, protocolo e fila de processamento.
- **Signature Service**: integração com assinatura eletrônica/digital.
- **Validation Service**: consulta pública por QR/token/código.
- **Audit Service**: trilha completa de eventos.
- **Storage Service**: persistência dos arquivos gerados e seus checksums.

## 6. Builder universal de documentos

O builder é o núcleo do módulo. Ele deve ser capaz de construir qualquer documento institucional sem depender de edição externa, usando composição visual por blocos e modo avançado por markup/template.

### 6.1 Modos do builder

O builder deve possuir dois modos interoperáveis:

1. **Modo visual**
   - Edição por blocos.
   - Arrastar e soltar.
   - Painel de propriedades.
   - Guias visuais para margens e grid.
   - Preview imediato.

2. **Modo técnico**
   - HTML/CSS controlado.
   - DSL/template engine com variáveis.
   - Regras condicionais.
   - Estruturas de repetição.
   - CSS de impressão avançado.

3. **Modo híbrido**
   - Usuário monta no visual.
   - Usuário técnico refina no markup.
   - Sistema mantém estrutura sem perda de compatibilidade.

### 6.2 Blocos base do builder

O builder deve oferecer blocos reutilizáveis:

- Título.
- Subtítulo.
- Parágrafo.
- Texto rico.
- Lista ordenada.
- Lista não ordenada.
- Tabela.
- Linha horizontal.
- Espaçador.
- Quebra de página.
- Imagem.
- Logo.
- QR code.
- Código de barras.
- Assinatura.
- Carimbo.
- Selo.
- Caixa de destaque.
- Campo variável.
- Grupo condicional.
- Repetidor.
- Colunas.
- Bloco de identificação institucional.
- Bloco de identificação do aluno.
- Rodapé institucional.
- Cabeçalho institucional.
- Bloco livre HTML.

### 6.3 Áreas estruturais do documento

Cada documento deve ser composto por zonas independentes:

- Área da página.
- Cabeçalho.
- Corpo.
- Rodapé.
- Margem superior.
- Margem inferior.
- Margem esquerda.
- Margem direita.
- Área imprimível.
- Área de notas internas não impressas.

### 6.4 Camadas do layout

O builder deve suportar camadas lógicas:

- Fundo.
- Conteúdo principal.
- Elementos fixos.
- Elementos repetidos por página.
- Marcas de segurança.
- Marca d’água.
- Overlay de preview.

## 7. Suporte universal a tamanhos de papel

O builder deve permitir configurar qualquer formato de papel, com presets e modo customizado.

### 7.1 Presets obrigatórios

- A0
- A1
- A2
- A3
- A4
- A5
- A6
- Carta (Letter)
- Ofício
- Legal
- Executivo
- Tabloide
- Envelope padrões institucionais
- Etiquetas personalizadas

### 7.2 Configuração de papel

Campos obrigatórios:

- Nome do preset.
- Largura.
- Altura.
- Unidade de medida.
- Orientação: retrato ou paisagem.
- Sangria opcional.
- Área segura.
- Escala de renderização.
- DPI de preview.
- DPI de exportação.

### 7.3 Unidades de medida aceitas

- mm
- cm
- in
- px
- pt

### 7.4 Requisitos funcionais do motor de página

- Converter qualquer unidade para uma base interna padronizada.
- Preservar proporção e posicionamento no preview.
- Separar preview de tela do layout real de impressão.
- Permitir presets por modelo e por versão.
- Suportar documentos de página única e multipágina.

### 7.5 Exemplo de configuração JSON

```json
{
  "page": {
    "size": "A4",
    "width": 210,
    "height": 297,
    "unit": "mm",
    "orientation": "portrait",
    "bleed": 0,
    "safeArea": 5,
    "dpiPreview": 96,
    "dpiExport": 300
  }
}
```

## 8. Margens, recuos, alinhamento e identação

O builder deve permitir controle fino de composição tipográfica e de impressão.

### 8.1 Configuração de margens da página

Campos:

- Margem superior.
- Margem inferior.
- Margem esquerda.
- Margem direita.
- Margem espelhada para frente e verso.
- Margem específica da primeira página.
- Margem específica de páginas pares/ímpares.

### 8.2 Configuração de recuos e identação

Campos:

- Recuo do primeiro parágrafo.
- Recuo esquerdo do bloco.
- Recuo direito do bloco.
- Espaçamento antes.
- Espaçamento depois.
- Entrelinha.
- Alinhamento horizontal.
- Alinhamento vertical do bloco.
- Controle de hifenização.
- Justificado, esquerda, centro, direita.

### 8.3 Regras tipográficas

- Permitir estilo por bloco e por classe.
- Permitir herança de estilo institucional.
- Permitir tabulações.
- Permitir grid de baseline opcional.
- Permitir controle de órfãs e viúvas em impressão.
- Permitir evitar quebra dentro de blocos críticos.

### 8.4 Exemplo de estilo do corpo

```json
{
  "contentStyle": {
    "fontFamily": "Times New Roman",
    "fontSize": 12,
    "lineHeight": 1.5,
    "textAlign": "justify",
    "firstLineIndent": 1.25,
    "indentUnit": "cm",
    "spacingBefore": 0,
    "spacingAfter": 0.25,
    "spacingUnit": "cm"
  }
}
```

## 9. Cabeçalho e rodapé

O sistema deve oferecer builder específico para cabeçalho e rodapé, desacoplado do corpo do documento.

### 9.1 Capacidades do cabeçalho

- Logo institucional.
- Nome da instituição.
- CNPJ.
- Endereço.
- Unidade emissora.
- Linha decorativa.
- Título da seção.
- Número do documento.
- Data de emissão.
- Cabeçalho diferente na primeira página.
- Cabeçalho diferente em páginas pares/ímpares.

### 9.2 Capacidades do rodapé

- Texto institucional.
- Endereço/contato.
- Autenticação e QR code.
- Número da página.
- Total de páginas.
- Código de validação.
- Rodapé legal.
- Assinatura institucional.
- Observação de validade.

### 9.3 Campos configuráveis

- Altura do cabeçalho.
- Altura do rodapé.
- Distância da margem.
- Repetir em todas as páginas.
- Mostrar apenas na primeira página.
- Mostrar apenas na última página.
- Mostrar em páginas pares/ímpares.
- Sobrepor ou reservar área fixa.

### 9.4 Placeholders de paginação

- `{{ page.number }}`
- `{{ page.total }}`
- `{{ document.validation_code }}`
- `{{ document.issue_date }}`

### 9.5 Regras de layout

- Cabeçalho e rodapé devem reservar espaço real na área imprimível.
- O corpo não pode colidir com cabeçalho/rodapé.
- O preview deve mostrar claramente a caixa útil da página.

## 10. Configuração avançada de impressão

O módulo precisa suportar impressão profissional e PDF confiável.

### 10.1 Recursos obrigatórios

- CSS de impressão por template.
- `@page` configurável.
- Quebra de página manual e automática.
- Evitar quebra dentro de tabela ou assinatura.
- Repetição de cabeçalho de tabela.
- Marcas de corte opcionais.
- Escala de impressão controlada.
- Modo frente e verso.
- Margens espelhadas.
- Página inicial distinta.

### 10.2 Propriedades a suportar

- `page-break-before`
- `page-break-after`
- `page-break-inside`
- `break-before`
- `break-after`
- `break-inside`
- `orphans`
- `widows`
- `@page`

### 10.3 Exemplo conceitual

```css
@page {
  size: A4 portrait;
  margin: 20mm 15mm 25mm 20mm;
}

.section-no-break {
  break-inside: avoid;
}

.signature-block {
  page-break-inside: avoid;
}
```

## 11. Biblioteca de variáveis e placeholders

O builder deve expor variáveis organizadas por domínio de negócio.

### 11.1 Grupos mínimos

- Instituição.
- Mantenedora.
- Unidade.
- Curso.
- Turma.
- Período letivo.
- Aluno.
- Matrícula.
- Contrato.
- Financeiro.
- Responsável.
- Documento.
- Usuário emissor.
- Data/hora.
- Assinaturas.
- Configurações customizadas.

### 11.2 Exemplos

- `{{ instituicao.nome }}`
- `{{ unidade.nome }}`
- `{{ aluno.nome_completo }}`
- `{{ aluno.cpf }}`
- `{{ matricula.numero }}`
- `{{ curso.nome }}`
- `{{ turma.nome }}`
- `{{ periodo_letivo.descricao }}`
- `{{ contrato.numero }}`
- `{{ financeiro.saldo_aberto }}`
- `{{ document.protocol }}`
- `{{ document.validation_code }}`
- `{{ issuer.nome }}`

### 11.3 Requisitos

- Autocomplete por grupo.
- Descrição funcional da variável.
- Tipo da variável.
- Exemplo de valor.
- Indicação de campo sensível.
- Validação de placeholder inexistente.
- Aviso quando a variável não existir no contexto selecionado.

## 12. Condicionais, repetições e lógica de template

O builder deve suportar lógica suficiente para compor documentos complexos.

### 12.1 Condicionais

Exemplos:

```twig
{% if matricula.status == 'ATIVA' %}
<p>O aluno encontra-se regularmente matriculado.</p>
{% endif %}
```

### 12.2 Repetições

```twig
{% for disciplina in historico.disciplinas %}
<tr>
  <td>{{ disciplina.nome }}</td>
  <td>{{ disciplina.carga_horaria }}</td>
  <td>{{ disciplina.nota_final }}</td>
</tr>
{% endfor %}
```

### 12.3 Regras obrigatórias

- Comparações simples e compostas.
- Operadores lógicos.
- Formatação de datas, números e moeda.
- Funções auxiliares seguras.
- Blocos ocultos quando vazios.
- Fallbacks de valor.

## 13. Componentes reutilizáveis

O sistema deve permitir biblioteca de componentes reutilizáveis por tenant.

### Exemplos

- Cabeçalho institucional padrão.
- Rodapé de autenticação padrão.
- Bloco de assinatura da secretaria.
- Bloco de contrato financeiro.
- Tabela padrão de disciplinas.
- Caixa legal de LGPD.
- Termo padrão de ciência.

Cada componente deve ter:

- Nome.
- Categoria.
- Versão.
- HTML/estrutura.
- Estilos.
- Variáveis esperadas.
- Dependências.
- Escopo.

## 14. Regras de negócio para emissão

Como a tela atual permite filtrar por período letivo, unidade, turma e aluno, a emissão precisa ser contextual e dirigida por dados acadêmicos antes da geração do documento. [cite:1]

### Exemplos de elegibilidade

- Declaração de matrícula apenas para matrícula ativa.
- Declaração de frequência apenas com vínculo vigente.
- Declaração de quitação apenas sem débitos vencidos.
- Aditivo apenas com contrato vigente.
- Transferência apenas com solicitação deferida.
- Etiqueta do aluno apenas com vínculo válido ou cadastro ativo.

### Severidades

- Bloqueante.
- Alerta.
- Informativa.

## 15. Fluxos do usuário

### 15.1 Criar tipo documental

1. Acessar Secretaria > Modelos de documentos. [cite:1]
2. Clicar em Cadastrar. [cite:1]
3. Informar nome, categoria, escopo e políticas.
4. Salvar o tipo.

### 15.2 Criar modelo

1. Selecionar o tipo documental.
2. Criar novo modelo.
3. Definir escopo, vigência e formato de papel.
4. Abrir builder.
5. Montar cabeçalho, corpo e rodapé.
6. Inserir variáveis.
7. Configurar regras.
8. Salvar rascunho.

### 15.3 Publicar modelo

1. Enviar para revisão.
2. Aprovador revisa layout e regras.
3. Publicar versão.
4. Modelo passa a ficar disponível para emissão.

### 15.4 Emitir documento individual

1. Selecionar período, unidade, turma e aluno. [cite:1]
2. Selecionar o tipo documental desejado. [cite:1]
3. Sistema resolve o modelo aplicável.
4. Executa regras de elegibilidade.
5. Exibe preview.
6. Confirma emissão.
7. Gera PDF e protocolo.
8. Registra auditoria.

### 15.5 Emitir em lote

1. Selecionar turma, unidade, curso ou filtro customizado.
2. Selecionar tipo documental.
3. Executar validações.
4. Enfileirar processamento.
5. Gerar resultado com sucessos e falhas.

## 16. Estrutura da interface do builder

### 16.1 Layout da tela

A interface deve conter:

- Barra superior com ações.
- Painel esquerdo de blocos.
- Área central de canvas/página.
- Painel direito de propriedades.
- Barra inferior de zoom, grade e páginas.
- Alternância entre preview tela e preview impressão.

### 16.2 Barra superior

- Salvar.
- Salvar versão.
- Validar.
- Pré-visualizar.
- Testar com aluno.
- Aprovar.
- Publicar.
- Duplicar.
- Exportar definição.
- Importar definição.

### 16.3 Painel esquerdo

- Blocos.
- Variáveis.
- Componentes reutilizáveis.
- Estrutura do documento.
- Páginas.

### 16.4 Painel direito

Propriedades contextuais do elemento selecionado:

- Dimensões.
- Posição.
- Fonte.
- Cor.
- Borda.
- Margem.
- Padding.
- Recuo.
- Quebra.
- Visibilidade condicional.
- Fonte de dados.
- Repetição.

## 17. Modelo de dados

### 17.1 Entidades principais

- `document_types`
- `document_models`
- `document_model_versions`
- `document_layout_definitions`
- `document_layout_blocks`
- `document_layout_assets`
- `document_variables_catalog`
- `document_rules`
- `document_approvals`
- `document_issuances`
- `document_issuance_files`
- `document_validation_tokens`
- `document_revocations`
- `document_audit_logs`
- `document_components_library`

### 17.2 Campos sugeridos para layout versionado

#### document_layout_definitions

- id
- model_version_id
- page_size
- page_width
- page_height
- unit
- orientation
- margin_top
- margin_right
- margin_bottom
- margin_left
- mirrored_margins
- header_height
- footer_height
- content_schema_json
- print_css
- preview_css
- builder_schema_json
- created_at

#### document_layout_blocks

- id
- layout_definition_id
- parent_block_id nullable
- block_type
- zone
- sort_order
- x
- y
- width
- height
- style_json
- content_json
- visibility_rule_json
- repeat_rule_json

## 18. API sugerida

### Tipos

- `GET /api/document-types`
- `POST /api/document-types`
- `PUT /api/document-types/{id}`

### Modelos

- `GET /api/document-models`
- `POST /api/document-models`
- `GET /api/document-models/{id}`
- `PUT /api/document-models/{id}`
- `POST /api/document-models/{id}/version`
- `POST /api/document-models/{id}/publish`

### Builder

- `GET /api/document-models/{id}/builder`
- `PUT /api/document-models/{id}/builder`
- `POST /api/document-models/{id}/validate-layout`
- `POST /api/document-models/{id}/preview`
- `POST /api/document-models/{id}/preview-print`

### Emissão

- `POST /api/documents/issue`
- `POST /api/documents/issue-batch`
- `GET /api/documents/issuances`
- `GET /api/documents/issuances/{id}`
- `POST /api/documents/issuances/{id}/revoke`

### Validação pública

- `GET /public/document-validation/{code}`

## 19. Segurança, LGPD e governança

O módulo deve tratar documentos acadêmicos e cadastrais, o que exige governança forte sobre acesso, visualização e emissão, especialmente porque a tela atual é contextualizada por aluno e unidade. [cite:1]

### Requisitos obrigatórios

- RBAC por ação e escopo.
- Separação por tenant.
- Restrição por unidade.
- Logs imutáveis.
- Hash do documento emitido.
- Máscara de dados sensíveis em telas públicas.
- Criptografia de dados sensíveis em repouso.
- Registro de base legal e finalidade, quando aplicável.
- Política de retenção e descarte.

## 20. Auditoria

Toda ação deve ser registrada:

- criação de tipo;
- criação de modelo;
- edição de versão;
- aprovação;
- publicação;
- preview;
- emissão;
- reemissão;
- revogação;
- validação pública;
- download;
- alteração de regras.

Campos mínimos:

- entidade;
- id da entidade;
- ação;
- usuário;
- data/hora;
- IP;
- before/after;
- unidade;
- tenant;
- correlation id.

## 21. Requisitos não funcionais

### Performance

- Preview individual em até 2 segundos em cenários comuns.
- Geração síncrona simples em até 5 segundos.
- Emissão em lote assíncrona.
- Layout com paginação estável.

### Confiabilidade

- Idempotência na emissão.
- Retry seguro em tarefas assíncronas.
- Não duplicar protocolo.
- Snapshot completo do payload usado na emissão.

### Escalabilidade

- Filas para geração de lote.
- Storage desacoplado.
- Cache de variáveis institucionais.
- Render workers horizontais.

## 22. Critérios de aceite do builder

O builder será considerado pronto quando:

- Permitir criar modelo sem ferramenta externa.
- Suportar A0, A1, A2, A3, A4, A5, Carta e formatos customizados.
- Permitir configurar orientação, margens e área imprimível.
- Permitir cabeçalho e rodapé independentes.
- Permitir identação, recuo, entrelinha e alinhamento por bloco.
- Permitir preview fiel do papel.
- Permitir quebras de página controladas.
- Permitir PDF multipágina estável.
- Permitir variáveis, condicionais e repetições.
- Permitir salvar e versionar layouts.
- Permitir emissão real por aluno/unidade/período.
- Permitir validação e auditoria completas.

## 23. Roadmap recomendado

### Fase 1

- Cadastro de tipos.
- Cadastro de modelos.
- Builder básico com A4/A3/Carta.
- Variáveis.
- Preview.
- Geração de PDF.
- Emissão individual.

### Fase 2

- Versionamento avançado.
- Cabeçalho e rodapé por página.
- Condicionais e repetições.
- Emissão em lote.
- Validação pública.
- Revogação.

### Fase 3

- Assinatura digital.
- Componentes reutilizáveis avançados.
- Editor técnico completo.
- Frentes e versos com margens espelhadas.
- Templates institucionais compartilhados entre unidades.

## 24. Recomendação de implementação

Para um SaaS educacional multiunidade, a melhor abordagem é manter o documento emitido como artefato imutável, o template como ativo versionado e o builder como uma definição estruturada serializável em JSON, separada da renderização final.

A implementação recomendada é:

- Builder salvo em `builder_schema_json`.
- Estilo salvo em `style_json` por bloco.
- Template lógico salvo em `content_schema_json`.
- Exportação final em HTML de impressão + PDF.
- Render service isolado com fila para lote.
- Snapshot integral do payload da emissão.

## 25. Exemplo de definição serializada do builder

```json
{
  "document": {
    "type": "DECLARACAO_MATRICULA",
    "version": "3.0.0"
  },
  "page": {
    "size": "A4",
    "orientation": "portrait",
    "unit": "mm",
    "width": 210,
    "height": 297,
    "margins": {
      "top": 20,
      "right": 15,
      "bottom": 25,
      "left": 20
    },
    "header": {
      "enabled": true,
      "height": 25,
      "repeatEveryPage": true
    },
    "footer": {
      "enabled": true,
      "height": 18,
      "repeatEveryPage": true
    }
  },
  "content": [
    {
      "type": "paragraph",
      "style": {
        "fontSize": 12,
        "textAlign": "justify",
        "firstLineIndent": 12.5,
        "lineHeight": 1.5
      },
      "value": "Declaramos que {{ aluno.nome_completo }} está regularmente matriculado(a)..."
    }
  ]
}
```

## 26. Fechamento técnico

A tela observada já aponta corretamente para um catálogo de modelos documentais por tipo, mas a evolução ideal é transformar esse ponto em um subsistema completo de **gestão documental com builder universal**, suportando documentos simples, formais, extensos, multipágina e institucionalmente validados. [cite:1]

O grande diferencial do módulo deve ser unir três camadas no mesmo produto: governança do modelo, liberdade de composição visual e confiabilidade de emissão/impressão. Isso permite que a secretaria opere documentos do dia a dia, enquanto jurídico, financeiro e administração mantêm controle formal sobre versões, layout e validade.
