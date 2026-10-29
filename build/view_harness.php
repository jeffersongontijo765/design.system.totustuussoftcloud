<?php
// Renderiza views avulsas (auth/errors/web/install) pelo PlatesEngine real do app.
// Uso (a partir do REPO): php view_harness.php <uri> <view> <out.html> [json-data]
namespace {
define('TTSC_MIGRATION_DATABASE', 'tenant_test');
require 'vendor/autoload.php';
\TotusTuus\Config\Env::load();
foreach (['DB_HOST' => '127.0.0.1', 'DB_USERNAME' => 'app', 'DB_PASSWORD' => 'app', 'APP_LOCALE' => 'pt-br'] as $k => $v) { putenv("$k=$v"); $_ENV[$k] = $v; }
[$_, $uri, $view, $out] = $argv; $data = isset($argv[4]) ? json_decode($argv[4], true) : [];
// objetos (ex.: customer) via chave "__obj"
foreach ($data as $k => $v) if (is_array($v) && isset($v['__obj'])) { unset($v['__obj']); $data[$k] = (object) $v; }
if (isset($data['tickets'])) $data['tickets'] = array_map(fn($t) => (object) $t, $data['tickets']);
$_SERVER['REQUEST_URI'] = $uri; $_SERVER['REQUEST_METHOD'] = 'GET'; $_SERVER['HTTP_HOST'] = '127.0.0.1';
if (str_starts_with($view, 'errors::')) { $data['exception'] = new \RuntimeException('x'); }
$html = view($view, $data)->getContent();
file_put_contents($out, $html);
printf("%s -> %s %dKB err=%s\n", $view, $out, strlen($html)/1024, preg_match('/Error rendering view|Fatal error|Warning:|Uncaught/', $html) ? 'YES' : 'no');
}
