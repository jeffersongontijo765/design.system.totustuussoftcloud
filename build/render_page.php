<?php
// Renders pages through SectionPageController::renderPath() against tenant_test with a real session per profile.
namespace App\Tenant { class TenantManager { public static function getInstance(){ static $i; return $i ??= new self(); } public function isDedicatedTenantDatabase(): bool { return true; } public function __call($m,$a){ return str_starts_with($m, "get") ? [] : null; } } }
namespace {
define('TTSC_MIGRATION_DATABASE', 'tenant_test');
require 'vendor/autoload.php';
\TotusTuus\Config\Env::load();
foreach (['DB_HOST' => '127.0.0.1', 'DB_USERNAME' => 'app', 'DB_PASSWORD' => 'app', 'APP_LOCALE' => 'pt-br'] as $k => $v) { putenv("$k=$v"); $_ENV[$k] = $v; }
$profiles = ['admin' => ['u-admin', 'admin'], 'teacher' => ['u-teacher', 'teacher'], 'student' => ['u-student', 'student'], 'parents' => ['u-guardian', 'parents'], 'thirdparty' => ['u-third', 'thirdparty']];
$routes = array_slice($argv, 1);
foreach ($routes as $route) {
    $portal = explode('/', trim($route, '/'))[0];
    [$uuid, $p] = $profiles[$portal] ?? $profiles['admin'];
    session()->get('tenant_id');
    \App\Services\Portal\PortalDomainDataService::class;
    $_SESSION = ['user_uuid' => $uuid, 'user_id' => $uuid, 'tenant_id' => 't', 'user_portal' => $p, 'user' => ['uuid' => $uuid, 'tenant_id' => 't', 'name' => $uuid]];
    $_SERVER['REQUEST_URI'] = $route; $_SERVER['REQUEST_METHOD'] = 'GET'; $_SERVER['HTTP_HOST'] = '127.0.0.1';
    try {
        $data = \App\Services\Portal\PortalDomainDataService::getDataForRoute($route, 't');
        $res = \App\Http\Controllers\Portal\SectionPageController::renderPath($route);
        $html = $res->getContent();
        file_put_contents(sys_get_temp_dir() . '/render_' . trim(str_replace('/', '_', $route), '_') . '.html', $html);
        printf("%-48s http=%s data=%s rows=%s html=%dKB unavailable=%s error=%s\n", $route, $data['http_status'], $data['available'] ? 'yes' : 'no',
            $data['totalRecords'] ?? '-', strlen($html) / 1024, substr_count($html, 'KPI unavailable'), preg_match('/Error rendering view|Fatal|Exception/', $html) ? 'YES' : 'no');
        if (!$data['available']) echo "   -> ", $data['message'], "\n";
    } catch (\Throwable $e) {
        printf("%-48s EXCEPTION %s: %s\n", $route, get_class($e), substr($e->getMessage(), 0, 200));
    }
}
}
