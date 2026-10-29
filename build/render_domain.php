<?php
// Renderiza resources/views/app/partials/chassis/domain_page.php com registros ilustrativos em memória (nada é gravado no banco).
namespace App\Tenant { class TenantManager { public static function getInstance(){ static $i; return $i ??= new self(); } public function isDedicatedTenantDatabase(): bool { return true; } public function __call($m,$a){ return str_starts_with($m, "get") ? [] : null; } } }
namespace {
define('TTSC_MIGRATION_DATABASE', 'tenant_test');
require 'vendor/autoload.php';
\TotusTuus\Config\Env::load();
foreach (['DB_HOST' => '127.0.0.1', 'DB_USERNAME' => 'app', 'DB_PASSWORD' => 'app', 'APP_LOCALE' => 'pt-br'] as $k => $v) { putenv("$k=$v"); $_ENV[$k] = $v; }
session()->get('tenant_id');
$_SESSION = ['user_uuid' => 'u-admin', 'user_id' => 'u-admin', 'tenant_id' => 't', 'user_portal' => 'admin', 'user' => ['uuid' => 'u-admin', 'tenant_id' => 't', 'name' => 'u-admin']];
$pageRoute = $argv[1];
$out = $argv[2];
$d = \App\Services\Portal\PortalDomainDataService::getDataForRoute($pageRoute, 't');
$explorerColumns = $d['explorerColumns'];
$students = ['Ana Beatriz Souza','Bruno Carvalho','Camila Rocha','Diego Almeida','Elisa Martins','Felipe Duarte','Gabriela Lima','Henrique Souza','Isabela Freitas','João Pereira','Larissa Nunes','Marcos Teixeira','Natália Gomes','Otávio Barros','Paula Ribeiro','Rafael Cardoso','Sofia Mendes','Tiago Costa'];
$courses = [['Ensino Médio','1ª série A'],['Ensino Médio','2ª série B'],['Fundamental II','9º ano A'],['Técnico em Informática','INF-2026-1N'],['Técnico em Enfermagem','ENF-2026-1M']];
$statuses = ['draft','submitted','pending_review','approved','approved','approved','submitted','pending_review'];
$types = ['renewal','renewal','transfer','renewal','course_change'];
$shifts = ['morning','afternoon','night'];
$records = [];
foreach ($students as $i => $name) {
    [$course, $class] = $courses[$i % count($courses)];
    $records[] = ['uuid' => sprintf('00000000-0000-4000-8000-%012d', $i + 1), 'code' => sprintf('REM-2026-%04d', $i + 101),
        'request_type' => $types[$i % count($types)], 'student_name' => $name, 'course_name' => $course, 'class_name' => $class,
        'shift' => $shifts[$i % 3], 'period_name' => '2º semestre de 2026', 'created_at' => date('Y-m-d H:i:s', strtotime('2026-10-20 -' . ($i * 3) . ' days')),
        'status' => $statuses[$i % count($statuses)], 'notes' => $i % 4 === 0 ? 'Aguardando comprovante de residência atualizado.' : null];
}
$totalRecords = count($records);
$statusCounts = array_count_values(array_column($records, 'status'));
$distribution = [];
$kpiCards = $d['kpiCards'];
foreach ($kpiCards as &$k) {
    if ($k['id'] === 'kpi-total') { $k['raw_value'] = $totalRecords; }
    elseif (str_starts_with($k['id'], 'kpi-status-')) { $s = str_replace('-', '_', substr($k['id'], 11)); $k['raw_value'] = $statusCounts[$s] ?? 0; }
    elseif ($k['id'] === 'kpi-recent30') { $k['raw_value'] = count(array_filter($records, fn ($r) => strtotime($r['created_at']) >= strtotime('2026-10-20 -30 days'))); }
    $k['value'] = number_format((float) $k['raw_value'], 0, ',', '.');
}
unset($k);
$sourceTable = $d['table'];
$title = 'Rematrícula'; $icon = 'fa-arrows-rotate'; $description = 'Pedidos de rematrícula do período 2026.2.';
ob_start();
try { include base_path('resources/views/app/partials/chassis/domain_page.php'); }
catch (\Throwable $e) { ob_end_clean(); fwrite(STDERR, get_class($e) . ': ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine() . "\n"); exit(1); }
file_put_contents($out, ob_get_clean());
echo "ok ", filesize($out), "\n";
}
