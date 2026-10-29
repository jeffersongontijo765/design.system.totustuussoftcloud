# FileManager

Explorador de arquivos de uma pasta: caminho (breadcrumb), lista com ícone por tipo, tamanho, data, situação e ações por arquivo. Usado para documentos de matrícula, certidões, contratos e anexos.

## Quando usar

- Documentos que a secretaria recebe, confere e aprova (certidões, histórico, foto, contrato).
- Quando cada arquivo tem situação própria (em análise, validado, recusado).
- Para arquivos de uma pessoa só. Para a biblioteca geral de mídia, use uma grade (ver [GalleryGrid](../GalleryGrid/README.md)).

## Anatomia

```
Documentos / Matrícula 2027 / Ana Souza
Nome                         Tamanho  Enviado em  Situação     Ações
[📁] Certidões                3 itens  02/12/2026  Completa     [→]
[📄] Certidão de nascimento   1,2 MB   02/12/2026  Validado     [↓][🗑]
```

| Parte | Classe / elemento | Obrigatório |
|---|---|---|
| Caminho | `nav.fm-path` com `aria-label` | sim |
| Tabela | `table.fm-table` com `caption` e `scope` | sim |
| Nome com ícone | `.fm-name` > `.fm-ic` (`.pdf`, `.img`, `.dir`) | sim |
| Situação | `.pill` (`pill-ok`, `pill-warn`, `pill-bad`) | sim |
| Ações | `.fm-acts > button.ib` com `aria-label` | sim |

## Variantes / Estados

- **Pasta:** linha com `.dir`; a ação é entrar na pasta.
- **Arquivo validado / em análise / recusado:** a situação aparece em texto e cor, sempre com o rótulo.
- **Telas pequenas:** tamanho e data somem (`.hide-sm`); nome e situação continuam.

## API

| Atributo | Efeito |
|---|---|
| `aria-label` em cada `.ib` | nome do arquivo na ação ("Baixar Foto 3x4") |
| `.hide-sm` | oculta colunas em telas pequenas |

## Acessibilidade

- O caminho é `nav` com `aria-label`, e a pasta atual não é link.
- Os botões de ação dizem o arquivo em que atuam.
- Ícones de tipo são `aria-hidden`; o tipo também aparece no nome do arquivo (extensão).

## Modelos

### HTML

```html
<nav class="fm-path" aria-label="Caminho da pasta"><a href="#">Documentos</a><span>/</span><span>Ana Souza</span></nav>
<table class="fm-table">
  <thead><tr><th scope="col">Nome</th><th scope="col">Situação</th><th scope="col">Ações</th></tr></thead>
  <tbody>
    <tr>
      <td><span class="fm-name"><span class="fm-ic pdf" aria-hidden="true"><i class="fa-light fa-file-pdf"></i></span>Certidão de nascimento.pdf</span></td>
      <td><span class="pill pill-ok fm-status">Validado</span></td>
      <td><div class="fm-acts"><button class="ib" type="button" aria-label="Baixar Certidão de nascimento"><i class="fa-light fa-download" aria-hidden="true"></i></button></div></td>
    </tr>
  </tbody>
</table>
```

### CSS

Classes `.fm*`, `.pill`, `.ib`. O ícone de tipo usa `--ttsc-danger-text` (PDF), `--ttsc-info-text` (imagem) e `--ttsc-accent-text` (pasta).

### JS

```js
async function baixar(arquivo) {
  const res = await fetch(`/api/v1/documentos/${arquivo.uuid}/download`);
  if (!res.ok) throw new Error('Não foi possível baixar o arquivo');
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement('a'), { href: url, download: arquivo.nome });
  a.click();
  URL.revokeObjectURL(url);
}
```

### SQL

Arquivos de uma pasta da matrícula (origem do documento), com o tamanho em bytes:

```sql
SELECT f.uuid, f.file_name AS nome, f.mime_type, f.size_bytes, f.status, f.created_at
FROM storage_files f
WHERE f.tenant_id = ? AND f.origin_entity_type = 'enrollment' AND f.origin_entity_uuid = ?
  AND f.is_deleted = 0
ORDER BY f.created_at DESC;
```

## Faça / Não faça

- Faça: mostre a situação de cada arquivo e o motivo quando estiver recusado.
- Faça: oriente o envio (formato e tamanho máximo) perto do botão de enviar.
- Não faça: excluir um documento validado sem confirmação e sem registrar quem excluiu.
