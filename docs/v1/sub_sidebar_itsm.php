<?php
$uri = $_SERVER['REQUEST_URI'] ?? '';
$isPat = function($path) use ($uri) { return strpos($uri, $path) !== false; };
$isExact = function($path) use ($uri) {
    return preg_match('#/totustuussoftcloud' . preg_quote($path, '#') . '(\?|$)#', $uri) === 1;
};
?>
<div class="sb-backdrop" id="sb-backdrop" aria-hidden="true" onclick="toggleSubSidebar()"></div>
<aside class="sidebar" id="itsm-sidebar" data-od-id="sidebar" aria-label="IT Service Management navigation">
  <div class="sb-header">
    <div class="sb-header-title">
      <i class="fa-solid fa-server" style="margin-right: 8px; color: var(--accent);"></i>
      <span class="sb-text">ITSM</span>
    </div>
    <button class="sb-close-ttsc-btn" id="sb-close-ttsc-btn" aria-label="Close menu">
      <i class="fa-solid fa-xmark"></i>
    </button>
  </div>

  <div class="sb-search">
    <i class="fa-solid fa-magnifying-glass sb-search-icon"></i>
    <input type="text" id="itsm-sidebar-search" placeholder="Search ITSM pages…" aria-label="Search ITSM pages" />
  </div>

  <div class="sb-content" id="itsm-sidebar-content">

    <div class="sb-section">
      <a class="sb-item <?= $isExact('/admin/itsm') || $isExact('/admin/itsm/dashboard') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm') ?>">
        <i class="fa-solid fa-gauge icon"></i><span class="sb-text">Dashboard</span><span class="pill-tag">home</span>
      </a>
    </div>

    <hr class="sb-divider">

    <div class="sb-section <?= $isPat('/admin/itsm/assets') || $isPat('/admin/itsm/software') || $isPat('/admin/itsm/networks') || $isPat('/admin/itsm/cmdb') ? '' : 'is-collapsed' ?>">
      <button class="sb-section-toggle" type="button"><i class="fa-solid fa-angle-down sb-chevron"></i><i class="fa-solid fa-desktop sb-toggle-icon"></i><span class="sb-text">Inventory</span></button>
      <div class="sb-subsection">
        <a class="sb-item <?= $isPat('/admin/itsm/assets') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/assets') ?>"><i class="fa-solid fa-desktop icon"></i><span class="sb-text">Hardware Assets</span></a>
        <a class="sb-item <?= $isPat('/admin/itsm/software') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/software') ?>"><i class="fa-solid fa-cd icon"></i><span class="sb-text">Software & Licenses</span></a>
        <a class="sb-item <?= $isPat('/admin/itsm/networks') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/networks') ?>"><i class="fa-solid fa-network-wired icon"></i><span class="sb-text">Networks</span></a>
        <a class="sb-item <?= $isPat('/admin/itsm/cmdb') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/cmdb') ?>"><i class="fa-solid fa-diagram-project icon"></i><span class="sb-text">CMDB</span></a>
      </div>
    </div>

    <hr class="sb-divider">

    <div class="sb-section <?= $isPat('/admin/itsm/tickets') || $isPat('/admin/itsm/incidents') || $isPat('/admin/itsm/problems') || $isPat('/admin/itsm/changes') ? '' : 'is-collapsed' ?>">
      <button class="sb-section-toggle" type="button"><i class="fa-solid fa-angle-down sb-chevron"></i><i class="fa-solid fa-ticket sb-toggle-icon"></i><span class="sb-text">Service Desk</span></button>
      <div class="sb-subsection">
        <a class="sb-item <?= $isPat('/admin/itsm/tickets') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/tickets') ?>"><i class="fa-solid fa-ticket icon"></i><span class="sb-text">Tickets</span></a>
        <a class="sb-item <?= $isPat('/admin/itsm/incidents') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/incidents') ?>"><i class="fa-solid fa-triangle-exclamation icon"></i><span class="sb-text">Incidents</span></a>
        <a class="sb-item <?= $isPat('/admin/itsm/problems') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/problems') ?>"><i class="fa-solid fa-magnifying-glass icon"></i><span class="sb-text">Problems</span></a>
        <a class="sb-item <?= $isPat('/admin/itsm/changes') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/changes') ?>"><i class="fa-solid fa-code-pull-request icon"></i><span class="sb-text">Changes</span></a>
      </div>
    </div>

    <hr class="sb-divider">

    <div class="sb-section <?= $isPat('/admin/itsm/contracts') || $isPat('/admin/itsm/slas') || $isPat('/admin/itsm/suppliers') ? '' : 'is-collapsed' ?>">
      <button class="sb-section-toggle" type="button"><i class="fa-solid fa-angle-down sb-chevron"></i><i class="fa-solid fa-file-contract sb-toggle-icon"></i><span class="sb-text">Contracts & SLAs</span></button>
      <div class="sb-subsection">
        <a class="sb-item <?= $isPat('/admin/itsm/contracts') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/contracts') ?>"><i class="fa-solid fa-file-contract icon"></i><span class="sb-text">Contracts</span></a>
        <a class="sb-item <?= $isPat('/admin/itsm/slas') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/slas') ?>"><i class="fa-solid fa-stopwatch icon"></i><span class="sb-text">SLAs</span></a>
        <a class="sb-item <?= $isPat('/admin/itsm/suppliers') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/suppliers') ?>"><i class="fa-solid fa-truck-field icon"></i><span class="sb-text">Suppliers</span></a>
      </div>
    </div>

    <hr class="sb-divider">

    <div class="sb-section <?= $isPat('/admin/itsm/monitoring') || $isPat('/admin/itsm/automations') || $isPat('/admin/itsm/kb') ? '' : 'is-collapsed' ?>">
      <button class="sb-section-toggle" type="button"><i class="fa-solid fa-angle-down sb-chevron"></i><i class="fa-solid fa-tower-broadcast sb-toggle-icon"></i><span class="sb-text">Operations</span></button>
      <div class="sb-subsection">
        <a class="sb-item <?= $isPat('/admin/itsm/monitoring') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/monitoring') ?>"><i class="fa-solid fa-tower-broadcast icon"></i><span class="sb-text">Monitoring</span></a>
        <a class="sb-item <?= $isPat('/admin/itsm/automations') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/automations') ?>"><i class="fa-solid fa-robot icon"></i><span class="sb-text">Automations</span></a>
        <a class="sb-item <?= $isPat('/admin/itsm/kb') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/kb') ?>"><i class="fa-solid fa-book icon"></i><span class="sb-text">Knowledge Base</span></a>
      </div>
    </div>

    <hr class="sb-divider">

    <div class="sb-section">
      <a class="sb-item <?= $isPat('/admin/itsm/reports') ? 'is-active' : '' ?>" href="<?= url('/admin/itsm/reports') ?>">
        <i class="fa-solid fa-chart-pie icon"></i><span class="sb-text">Reports</span>
      </a>
    </div>

  </div>
</aside>

<script nonce="<?= \App\Security\CspNonce::get() ?>">
function toggleSubSidebar() {
  var sidebar = document.getElementById('itsm-sidebar');
  var backdrop = document.getElementById('sb-backdrop');
  if (sidebar) sidebar.classList.toggle('is-mobile-open');
  if (backdrop) backdrop.classList.toggle('is-open');
}
document.addEventListener('DOMContentLoaded', function() {
  var pinBtn = document.getElementById('btn-pin');
  if (pinBtn) pinBtn.addEventListener('click', function(e) { e.stopPropagation(); toggleSubSidebar(); });
  var closeBtn = document.getElementById('sb-close-ttsc-btn');
  if (closeBtn) closeBtn.addEventListener('click', toggleSubSidebar);
  var backdrop = document.getElementById('sb-backdrop');
  if (backdrop) backdrop.addEventListener('click', toggleSubSidebar);
  var toggles = document.querySelectorAll('.sb-section-toggle');
  toggles.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var section = btn.closest('.sb-section');
      if (section) section.classList.toggle('is-collapsed');
    });
  });

  // Sidebar search: filter items live, auto-expand matching sections
  var content = document.getElementById('itsm-sidebar-content');
  var searchInput = document.getElementById('itsm-sidebar-search');
  if (content && searchInput) {
    var sections = content.querySelectorAll('.sb-section');
    sections.forEach(function(section) {
      section.dataset.wasCollapsed = section.classList.contains('is-collapsed') ? '1' : '0';
    });

    searchInput.addEventListener('input', function(e) {
      var q = e.target.value.trim().toLowerCase();

      sections.forEach(function(section) {
        var divider = section.previousElementSibling;
        var isDivider = divider && divider.classList.contains('sb-divider');

        if (!q) {
          section.style.display = '';
          if (isDivider) divider.style.display = '';
          section.querySelectorAll('.sb-item').forEach(function(item) { item.style.display = ''; });
          section.classList.toggle('is-collapsed', section.dataset.wasCollapsed === '1');
          return;
        }

        var anyMatch = false;
        section.querySelectorAll('.sb-item').forEach(function(item) {
          var label = (item.querySelector('.sb-text') || item).textContent.toLowerCase();
          var match = label.indexOf(q) !== -1;
          item.style.display = match ? '' : 'none';
          if (match) anyMatch = true;
        });

        section.style.display = anyMatch ? '' : 'none';
        if (isDivider) divider.style.display = anyMatch ? '' : 'none';
        if (anyMatch) section.classList.remove('is-collapsed');
      });
    });
  }
});
</script>
