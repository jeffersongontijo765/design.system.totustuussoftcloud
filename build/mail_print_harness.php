<?php
// Renderiza (1) os e-mails reais de resources/views/emails pelo mesmo include+extract do Mailer/SacNotificationService
// e (2) o HTML que TabularExportService::toPdf() entrega ao dompdf (captura via stub de Dompdf, sem gerar PDF).
// Uso (a partir do REPO): php mail_print_harness.php <outdir>
namespace Dompdf { class Dompdf { public static string $html = ''; public function __construct($o = []) {} public function loadHtml($h) { self::$html = $h; } public function setPaper($a, $b) {} public function render() {} public function output() { return ''; } } }
namespace {
require 'vendor/autoload.php';
\TotusTuus\Config\Env::load();
$out = $argv[1];
function tpl(string $template, array $data): string { $file = resource_path('views/emails/' . $template . '.php'); extract($data, EXTR_SKIP); ob_start(); include $file; return ob_get_clean(); }
// SAC: layout + corpo (mesma composição de SacNotificationService::notifyNewMessage / notifySlaBreach)
$common = ['companyName' => 'Colégio Santa Clara', 'actionUrl' => '#', ];
file_put_contents("$out/r_mail_new_message.html", tpl('sac/layout', $common + [
  'moduleName' => 'Suporte — Nova mensagem', 'actionLabel' => 'Ver mensagem', 'subject' => '[SAC-2026-00412] Nova mensagem de Mariana Albuquerque',
  'bodyContent' => tpl('sac/new_message', ['ticketNumber' => 'SAC-2026-00412', 'ticketSubject' => 'Boleto da mensalidade de outubro não chegou', 'senderName' => 'Mariana Albuquerque', 'customerName' => 'Mariana Albuquerque', 'ticketStatus' => 'Em atendimento', 'messagePreview' => 'Bom dia. O boleto de outubro da matrícula do Pedro (9º ano A) ainda não chegou no e-mail cadastrado. Podem reenviar?'])]));
file_put_contents("$out/r_mail_sla_breach.html", tpl('sac/layout', $common + [
  'moduleName' => 'Suporte — Alerta de SLA', 'actionLabel' => 'Ver ticket', 'subject' => 'SLA de resposta violado — SAC-2026-00398',
  'bodyContent' => tpl('sac/sla_breach', ['ticketNumber' => 'SAC-2026-00398', 'ticketSubject' => 'Ajuste de frequência na turma 9º A', 'slaType' => 'Resposta', 'customerName' => 'Ricardo Menezes', 'priorityName' => 'Alta', 'priorityColor' => '#f59e0b', 'slaDeadline' => '21/10/2026 17:00'])]));
file_put_contents("$out/r_mail_dsr.html", tpl('dsr_notification', ['companyName' => 'Colégio Santa Clara', 'protocol' => 'DSR-2026-000187', 'requestTypeLabel' => 'Acesso aos dados', 'lawCode' => 'LGPD', 'subjectName' => 'Juliana Prado', 'subjectEmail' => 'juliana.prado@example.com', 'subjectDocument' => '***.482.***-**', 'receivedAt' => '20/10/2026 10:42', 'deadlineAt' => '04/11/2026', 'description' => 'Solicito cópia dos dados pessoais do meu filho, aluno do 6º ano B, mantidos pela escola.', 'actionUrl' => '#']));
// PDF tabular (dompdf) — mesmo HTML do export real
$svc = new \App\Services\TabularExportService();
$rows = [
 ['Matrícula' => 'MAT-2026-0142', 'Aluno' => 'Pedro Albuquerque', 'Turma' => '9º ano A', 'Curso' => 'Ensino Fundamental II', 'Situação' => 'Ativa', 'Data' => '2026-01-28'],
 ['Matrícula' => 'MAT-2026-0143', 'Aluno' => 'Lívia Nascimento', 'Turma' => '9º ano A', 'Curso' => 'Ensino Fundamental II', 'Situação' => 'Ativa', 'Data' => '2026-01-29'],
 ['Matrícula' => 'MAT-2026-0151', 'Aluno' => 'Gabriel Teixeira', 'Turma' => '8º ano B', 'Curso' => 'Ensino Fundamental II', 'Situação' => 'Trancada', 'Data' => '2026-02-03'],
 ['Matrícula' => 'MAT-2026-0158', 'Aluno' => 'Helena Duarte', 'Turma' => '1ª série EM', 'Curso' => 'Ensino Médio', 'Situação' => 'Ativa', 'Data' => '2026-02-05'],
 ['Matrícula' => 'MAT-2026-0163', 'Aluno' => 'Rafael Moura', 'Turma' => '1ª série EM', 'Curso' => 'Ensino Médio', 'Situação' => 'Pendente', 'Data' => '2026-02-09'],
 ['Matrícula' => 'MAT-2026-0170', 'Aluno' => 'Beatriz Campos', 'Turma' => '6º ano B', 'Curso' => 'Ensino Fundamental II', 'Situação' => 'Ativa', 'Data' => '2026-02-11'],
];
$svc->build('pdf', $rows, array_keys($rows[0]), ['title' => 'Matrículas 2026 — Unidade Centro']);
file_put_contents("$out/r_print_pdf.html", \Dompdf\Dompdf::$html);
echo "ok\n";
}
