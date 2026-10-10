/**
 * YouTube Macro & Analyst Trend Intelligence Dashboard
 * Dynamic interaction, Chart.js visualizations, WordCloud2, and AI integration
 */

let currentPeriod = '2026-10';
let customStartDate = null;
let customEndDate = null;
let currentTopic = 'all';
let currentModel = 'qwen3:8b';
let timelineChart = null;
let sentimentChart = null;
let searchTimeout = null;
let availableMonths = [];

// XSS 방어 및 안전한 URL/텍스트 처리 헬퍼
function escapeHTML(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function sanitizeUrl(url) {
  if (!url) return "#";
  const str = String(url).trim();
  if (/^https?:\/\//i.test(str)) {
    return str;
  }
  return "#";
}

function createStanceBadgeElement(stance) {
  const span = document.createElement("span");
  const s = (stance || "Neutral").toLowerCase();
  if (s.includes("bullish") || s.includes("낙관")) {
    span.className = "badge-tag bullish";
    span.textContent = "Bullish 상승";
  } else if (s.includes("caution") || s.includes("신중") || s.includes("경계")) {
    span.className = "badge-tag caution";
    span.textContent = "Caution 경계";
  } else if (s.includes("bearish") || s.includes("비관") || s.includes("하락")) {
    span.className = "badge-tag bearish";
    span.textContent = "Bearish 하락";
  } else {
    span.className = "badge-tag neutral";
    span.textContent = "Neutral 중립";
  }
  return span;
}

// Initialize on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  fetchModels();
  fetchFilterOptions();
  fetchAvailableMonths();
  fetchAllData();
});

function initTheme() {
  const saved = localStorage.getItem("utube_theme");
  if (saved === "light") {
    document.body.classList.add("theme-light");
    updateThemeToggleUI(true);
  } else {
    updateThemeToggleUI(false);
  }
}

function toggleTheme() {
  const isLight = document.body.classList.toggle("theme-light");
  localStorage.setItem("utube_theme", isLight ? "light" : "dark");
  updateThemeToggleUI(isLight);
  if (timelineChart) timelineChart.update();
  if (sentimentChart) sentimentChart.update();
}

function updateThemeToggleUI(isLight) {
  const icon = document.getElementById("theme-toggle-icon");
  const text = document.getElementById("theme-toggle-text");
  if (isLight) {
    icon.textContent = "🌙";
    text.textContent = "다크 모드";
  } else {
    icon.textContent = "☀️";
    text.textContent = "라이트 모드";
  }
}

async function fetchModels() {
  try {
    const res = await fetch("/api/models");
    const data = await res.json();
    const select = document.getElementById("model-select");
    select.innerHTML = "";
    data.models.forEach(m => {
      const opt = document.createElement("option");
      opt.value = m;
      opt.textContent = m;
      if (m === data.default) opt.selected = true;
      select.appendChild(opt);
    });
    currentModel = select.value;
  } catch (e) {
    console.error("Failed to fetch models:", e);
  }
}

function changeModel() {
  const select = document.getElementById("model-select");
  currentModel = select.value;
  showToast(`AI 모델이 ${currentModel}로 변경되었습니다.`);
}

async function fetchFilterOptions() {
  try {
    const res = await fetch("/api/filters");
    const data = await res.json();
    
    const catSelect = document.getElementById("filter-category");
    data.categories.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c;
      opt.textContent = c;
      catSelect.appendChild(opt);
    });

    const analSelect = document.getElementById("filter-analyst");
    data.analysts.forEach(a => {
      const opt = document.createElement("option");
      opt.value = a;
      opt.textContent = a;
      analSelect.appendChild(opt);
    });
  } catch (e) {
    console.error("Failed to load filter options:", e);
  }
}

// Get active date boundary based on custom range or presets
function getActiveDateRange() {
  if (customStartDate && customEndDate) {
    return { startDate: customStartDate, endDate: customEndDate, isCustom: true };
  }
  if (currentPeriod === '2026-10') {
    return { startDate: '2026-10-01', endDate: '2026-10-31', isCustom: false };
  }
  if (currentPeriod === '2026-09') {
    return { startDate: '2026-09-01', endDate: '2026-09-30', isCustom: false };
  }
  if (currentPeriod === '2026-08') {
    return { startDate: '2026-08-01', endDate: '2026-08-31', isCustom: false };
  }
  if (currentPeriod && currentPeriod.length === 7 && currentPeriod[4] === '-') {
    return { startDate: `${currentPeriod}-01`, endDate: `${currentPeriod}-31`, isCustom: false };
  }
  if (currentPeriod === '2026-H1') {
    return { startDate: '2026-01-01', endDate: '2026-06-30', isCustom: false };
  }
  if (currentPeriod === '2024-H2') {
    return { startDate: '2024-07-01', endDate: '2024-12-31', isCustom: false };
  }
  return { startDate: null, endDate: null, isCustom: false };
}

function selectPeriod(period) {
  customStartDate = null;
  customEndDate = null;
  currentPeriod = period;

  // Update tabs active state
  document.querySelectorAll(".period-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.period === period);
  });

  const mDropdown = document.getElementById("month-dropdown");
  if (mDropdown) {
    mDropdown.value = (period.length === 7 && period[4] === '-') ? period : "";
  }

  // Determine user-friendly label
  let labelText = period;
  if (period === 'all') {
    labelText = "전체 기간 (2024~2026)";
  } else if (period === 'recent-3m') {
    labelText = "최근 3개월 통합 분석";
  } else {
    const found = availableMonths.find(m => m.month === period);
    if (found) {
      labelText = `🔥 ${found.label} (최근 수집: ${found.video_count}편)`;
    } else if (period.length === 7 && period[4] === '-') {
      labelText = `${period.split('-')[0]}년 ${parseInt(period.split('-')[1])}월`;
    }
  }
  document.getElementById("surge-period-label").textContent = labelText;

  // Refresh all dashboard metrics
  fetchAllData();
}

function renderPeriodShortcuts(months) {
  const container = document.getElementById("period-preset-tabs");
  if (!container) return;
  container.innerHTML = "";

  if (!months || months.length === 0) {
    container.innerHTML = `<button class="period-btn active" data-period="all" onclick="selectPeriod('all')">전체 기간</button>`;
    return;
  }

  // 1. Primary Shortcut: Latest collected month
  const latest = months[0];
  const btnLatest = document.createElement("button");
  const isLatestActive = (!customStartDate && currentPeriod === latest.month);
  btnLatest.className = `period-btn ${isLatestActive ? 'active' : ''}`;
  btnLatest.dataset.period = latest.month;
  btnLatest.innerHTML = `🔥 최근 월 (${latest.month})`;
  btnLatest.title = `가장 최근 수집된 데이터: ${latest.label} (${latest.video_count}편 보유)`;
  btnLatest.onclick = () => selectPeriod(latest.month);
  container.appendChild(btnLatest);

  // 2. Secondary Shortcuts: Previous 1~2 months (dynamically from DB)
  for (let i = 1; i < Math.min(3, months.length); i++) {
    const m = months[i];
    const btnM = document.createElement("button");
    const isMActive = (!customStartDate && currentPeriod === m.month);
    btnM.className = `period-btn ${isMActive ? 'active' : ''}`;
    btnM.dataset.period = m.month;
    btnM.textContent = `${m.month}`;
    btnM.title = `${m.label} (${m.video_count}편)`;
    btnM.onclick = () => selectPeriod(m.month);
    container.appendChild(btnM);
  }

  // 3. Smart Range Shortcut: Recent 3 Months
  const btn3M = document.createElement("button");
  btn3M.className = `period-btn ${currentPeriod === 'recent-3m' ? 'active' : ''}`;
  btn3M.dataset.period = "recent-3m";
  btn3M.innerHTML = `📅 최근 3개월`;
  btn3M.title = "최근 3개월간의 트렌드 통합 분석";
  btn3M.onclick = () => selectRecentMonthsRange(3);
  container.appendChild(btn3M);

  // 4. "전체 기간"
  const btnAll = document.createElement("button");
  const isAllActive = (!customStartDate && currentPeriod === 'all');
  btnAll.className = `period-btn ${isAllActive ? 'active' : ''}`;
  btnAll.dataset.period = "all";
  btnAll.textContent = "전체 기간";
  btnAll.onclick = () => selectPeriod('all');
  container.appendChild(btnAll);
}

function selectRecentMonthsRange(numMonths = 3) {
  if (!availableMonths || availableMonths.length === 0) return;
  const latestYm = availableMonths[0].month; // e.g. "2026-10"
  const [ly, lm] = latestYm.split("-").map(Number);
  
  // End date (last day of latest month)
  const lastDay = new Date(ly, lm, 0).getDate();
  const endDate = `${ly}-${String(lm).padStart(2, '0')}-${String(lastDay).padStart(2, '0')}`;
  
  // Start date (first day of N months ago)
  let sm = lm - (numMonths - 1);
  let sy = ly;
  while (sm <= 0) {
    sm += 12;
    sy -= 1;
  }
  const startDate = `${sy}-${String(sm).padStart(2, '0')}-01`;
  
  customStartDate = startDate;
  customEndDate = endDate;
  currentPeriod = 'recent-3m';

  // Update date inputs in picker
  document.getElementById("range-start-date").value = startDate;
  document.getElementById("range-end-date").value = endDate;

  // Update tabs active state
  document.querySelectorAll(".period-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.period === "recent-3m");
  });
  const mDropdown = document.getElementById("month-dropdown");
  if (mDropdown) mDropdown.value = "";

  document.getElementById("surge-period-label").textContent = `최근 ${numMonths}개월 (${startDate} ~ ${endDate})`;

  fetchAllData();
  showToast(`최근 ${numMonths}개월 (${startDate} ~ ${endDate}) 분석으로 전환되었습니다.`);
}

async function quickUpdateLatestMonth() {
  const btn = document.getElementById("btn-quick-refresh");
  const origHtml = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = `<span>⏳</span> <span>수집 중...</span>`;

  const targetMonth = availableMonths && availableMonths.length > 0 ? availableMonths[0].month : "2026-10";

  try {
    const res = await fetch(`/api/pipeline/monthly?month=${targetMonth}`, { method: "POST" });
    const data = await res.json();
    showToast(data.message || `${targetMonth} 최신 영상 수집 및 분석을 시작합니다.`);

    // Refresh after short wait
    setTimeout(async () => {
      await fetchAvailableMonths();
      selectPeriod(targetMonth);
      btn.disabled = false;
      btn.innerHTML = origHtml;
      showToast(`${targetMonth} 최신 데이터가 성공적으로 갱신되었습니다!`);
    }, 4000);
  } catch (e) {
    btn.disabled = false;
    btn.innerHTML = origHtml;
    showToast("최신 데이터 업데이트 중 오류가 발생했습니다.");
  }
}

function applyCustomDateRange() {
  const s = document.getElementById("range-start-date").value;
  const e = document.getElementById("range-end-date").value;
  if (!s || !e) {
    showToast("시작일과 종료일을 모두 입력해주세요.");
    return;
  }
  if (s > e) {
    showToast("시작일은 종료일보다 이전이어야 합니다.");
    return;
  }
  customStartDate = s;
  customEndDate = e;
  currentPeriod = 'custom';

  // Deactivate preset buttons
  document.querySelectorAll(".period-btn").forEach(btn => {
    btn.classList.remove("active");
  });
  const mDropdown = document.getElementById("month-dropdown");
  if (mDropdown) mDropdown.value = "";

  document.getElementById("surge-period-label").textContent = `🗓️ ${s} ~ ${e}`;

  fetchAllData();
  showToast(`분석 기간이 ${s} ~ ${e}로 적용되었습니다.`);
}

function resetDateRange() {
  customStartDate = null;
  customEndDate = null;
  const latestMonth = availableMonths && availableMonths.length > 0 ? availableMonths[0].month : "2026-10";
  document.getElementById("range-start-date").value = `${latestMonth}-01`;
  document.getElementById("range-end-date").value = "2026-10-10";
  selectPeriod(latestMonth);
  showToast(`최신 월(${latestMonth}) 기본값으로 재설정되었습니다.`);
}

function selectMonthDropdown(ym) {
  if (!ym) return;
  customStartDate = null;
  customEndDate = null;
  currentPeriod = ym;

  document.querySelectorAll(".period-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.period === ym);
  });

  const label = `${ym.substring(0,4)}년 ${parseInt(ym.substring(5,7))}월`;
  document.getElementById("surge-period-label").textContent = label;

  fetchAllData();
  showToast(`${label} 아카이브 데이터로 전환되었습니다.`);
}

async function fetchAvailableMonths() {
  try {
    const res = await fetch("/api/months");
    const months = await res.json();
    availableMonths = months;

    // Set default period to the latest month if initial
    if (months && months.length > 0) {
      if (!currentPeriod || currentPeriod === '2026-10') {
        currentPeriod = months[0].month;
      }
    }

    renderPeriodShortcuts(months);
    populateMonthDropdown(months);
  } catch (e) {
    console.error("Failed to fetch available months:", e);
  }
}

function populateMonthDropdown(months) {
  const sel = document.getElementById("month-dropdown");
  if (sel) {
    sel.innerHTML = '<option value="">🗓️ 전체 월별 아카이브 상세 선택...</option>';
    months.forEach(m => {
      const opt = document.createElement("option");
      opt.value = m.month;
      opt.textContent = `${m.label} (${m.video_count}편)`;
      if (m.month === currentPeriod) opt.selected = true;
      sel.appendChild(opt);
    });
  }

  const collectSel = document.getElementById("collect-quick-months");
  if (collectSel) {
    collectSel.innerHTML = "";
    months.forEach(m => {
      const opt = document.createElement("option");
      opt.value = m.month;
      opt.textContent = `${m.label} (${m.video_count}편 보유)`;
      collectSel.appendChild(opt);
    });
  }
}

async function fetchAllData() {
  await Promise.all([
    loadKPIs(),
    loadPeriodBriefing(),
    loadTimelineChart(),
    loadSurgeKeywords(),
    loadWordCloud(),
    loadSentimentChart(),
    loadAnalystMatrix(),
    loadVideos()
  ]);
}

async function loadKPIs() {
  const { startDate, endDate, isCustom } = getActiveDateRange();
  let url = "/api/summary";
  if (startDate && endDate) {
    url += `?start_date=${startDate}&end_date=${endDate}`;
  }
  try {
    const res = await fetch(url);
    const data = await res.json();

    document.getElementById("stat-total-videos").textContent = `${data.total_videos}건`;
    document.getElementById("stat-total-analysts").textContent = `${data.total_analysts}명`;
    document.getElementById("stat-top-category").textContent = data.top_category || "-";
    document.getElementById("stat-total-views").textContent = (data.total_views || 0).toLocaleString();

    // Sentiment ratio
    const s = data.sentiment_distribution;
    const total = (s.bullish || 0) + (s.caution || 0) + (s.neutral || 0) + (s.bearish || 0);
    const cautionPct = total > 0 ? Math.round(((s.caution + s.bearish) / total) * 100) : 0;
    document.getElementById("stat-consensus-ratio").textContent = `${cautionPct}% 신중`;

    // Update status banner text
    const statusElem = document.getElementById("period-status-text");
    if (statusElem) {
      if (isCustom) {
        if (currentPeriod === 'recent-3m') {
          statusElem.textContent = `📅 최근 3개월 통합 트렌드 (${startDate} ~ ${endDate}, 총 ${data.total_videos}건)`;
        } else {
          statusElem.textContent = `🗓️ 자유 기간: ${startDate} ~ ${endDate} (총 ${data.total_videos}건 분석 중)`;
        }
      } else {
        const found = availableMonths.find(m => m.month === currentPeriod);
        const label = found ? found.label : (currentPeriod === 'all' ? "전체 기간 (2024~2026)" : currentPeriod);
        statusElem.textContent = `🎯 ${label} 데이터 분석 중 (총 ${data.total_videos}건)`;
      }
    }
  } catch (e) {
    console.error("Failed to load KPIs:", e);
  }
}

async function loadPeriodBriefing() {
  const summaryElem = document.getElementById("briefing-summary");
  const debatesElem = document.getElementById("briefing-debates");
  const themesElem = document.getElementById("briefing-themes");

  const { startDate, endDate, isCustom } = getActiveDateRange();
  let query = "";
  if (isCustom) {
    query = `period=custom&start_date=${startDate}&end_date=${endDate}`;
  } else if (startDate && endDate) {
    query = `period=${currentPeriod}&start_date=${startDate}&end_date=${endDate}`;
  } else {
    query = `period=${currentPeriod}`;
  }

  summaryElem.innerHTML = `<span style="opacity: 0.6;">⚡ AI가 ${isCustom ? `${startDate}~${endDate}` : currentPeriod} 기간의 분석가 컨센서스를 분석 중입니다...</span>`;

  try {
    const res = await fetch(`/api/intelligence/period?${query}&model=${currentModel}`);
    const data = await res.json();

    document.getElementById("briefing-title").textContent = data.period_title || "시장 컨센서스 AI 브리핑";
    summaryElem.textContent = data.market_consensus_summary || "";

    // Debates
    debatesElem.innerHTML = "";
    (data.key_debates || []).forEach((deb, idx) => {
      const box = document.createElement("div");
      box.className = "debate-box";
      box.innerHTML = `
        <div class="debate-title">📌 핵심 쟁점 #${idx + 1}</div>
        <div class="debate-text">${deb}</div>
      `;
      debatesElem.appendChild(box);
    });

    // Themes
    themesElem.innerHTML = "";
    (data.top_themes || []).forEach(t => {
      const chip = document.createElement("span");
      chip.className = "theme-chip";
      chip.textContent = `#${t}`;
      themesElem.appendChild(chip);
    });
  } catch (e) {
    summaryElem.textContent = "AI 브리핑을 불러오는 중 오류가 발생했습니다.";
  }
}

function refreshPeriodBriefing() {
  loadPeriodBriefing();
  showToast("AI 브리핑 재분석을 요청했습니다.");
}

async function loadTimelineChart() {
  try {
    const res = await fetch("/api/timeline");
    const data = await res.json();

    const ctx = document.getElementById("timelineChart").getContext("2d");
    if (timelineChart) timelineChart.destroy();

    const colors = [
      { border: "#38bdf8", bg: "rgba(56, 189, 248, 0.15)" },
      { border: "#a855f7", bg: "rgba(168, 85, 247, 0.15)" },
      { border: "#10b981", bg: "rgba(16, 185, 129, 0.15)" },
      { border: "#f59e0b", bg: "rgba(245, 158, 11, 0.15)" },
      { border: "#f43f5e", bg: "rgba(244, 63, 94, 0.15)" }
    ];

    const datasets = data.datasets.map((ds, idx) => ({
      label: ds.label,
      data: ds.data,
      borderColor: colors[idx % colors.length].border,
      backgroundColor: colors[idx % colors.length].bg,
      borderWidth: 2.5,
      tension: 0.35,
      pointRadius: 4,
      pointHoverRadius: 6,
      fill: true
    }));

    timelineChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: data.labels,
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: {
            position: "top",
            labels: { color: "#94a3b8", font: { size: 11, weight: "600" } }
          }
        },
        scales: {
          x: {
            grid: { color: "rgba(255, 255, 255, 0.05)" },
            ticks: { color: "#94a3b8" }
          },
          y: {
            grid: { color: "rgba(255, 255, 255, 0.05)" },
            ticks: { color: "#94a3b8" }
          }
        }
      }
    });
  } catch (e) {
    console.error("Timeline error:", e);
  }
}

async function loadSurgeKeywords() {
  const { startDate, endDate, isCustom } = getActiveDateRange();
  let query = `top_n=10`;
  if (isCustom) {
    query += `&period=custom&start_date=${startDate}&end_date=${endDate}`;
  } else if (startDate && endDate) {
    query += `&period=${currentPeriod}&start_date=${startDate}&end_date=${endDate}`;
  } else {
    query += `&period=${currentPeriod}`;
  }

  try {
    const res = await fetch(`/api/surge?${query}`);
    const list = await res.json();

    const tbody = document.getElementById("surge-tbody");
    tbody.innerHTML = "";

    list.forEach(item => {
      const tr = document.createElement("tr");
      const rankClass = item.rank === 1 ? "top1" : item.rank === 2 ? "top2" : item.rank === 3 ? "top3" : "";
      tr.innerHTML = `
        <td class="surge-rank ${rankClass}">${item.rank}</td>
        <td class="surge-kw">${item.keyword}</td>
        <td style="text-align: center; color: var(--text-secondary); font-weight: 600;">${item.count}</td>
        <td>
          <div style="display: flex; align-items: center; gap: 0.4rem;">
            <div class="surge-bar-bg">
              <div class="surge-bar-fill" style="width: ${item.surge_score}%;"></div>
            </div>
            <span style="font-size: 0.72rem; color: var(--accent-cyan); font-weight: 700;">${item.surge_score}</span>
          </div>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error("Surge error:", e);
  }
}

async function loadWordCloud() {
  const { startDate, endDate, isCustom } = getActiveDateRange();
  let query = `top_n=45`;
  if (isCustom) {
    query += `&period=custom&start_date=${startDate}&end_date=${endDate}`;
  } else if (startDate && endDate) {
    query += `&period=${currentPeriod}&start_date=${startDate}&end_date=${endDate}`;
  } else {
    query += `&period=${currentPeriod}`;
  }

  try {
    const res = await fetch(`/api/keywords/top?${query}`);
    const data = await res.json();

    const canvas = document.getElementById("wordCloudCanvas");
    const list = data.map(item => [item.text, item.size * 5 + 12]);

    const isLight = document.body.classList.contains("theme-light");
    const colors = isLight
      ? ["#2563eb", "#4f46e5", "#0284c7", "#059669", "#d97706", "#7c3aed"]
      : ["#38bdf8", "#818cf8", "#34d399", "#fbbf24", "#f472b6", "#a78bfa", "#67e8f9"];

    WordCloud(canvas, {
      list: list,
      gridSize: 8,
      weightFactor: 1,
      fontFamily: "Pretendard, Inter, sans-serif",
      color: () => colors[Math.floor(Math.random() * colors.length)],
      backgroundColor: "transparent",
      rotateRatio: 0.15,
      rotationSteps: 2,
      minSize: 12
    });
  } catch (e) {
    console.error("Wordcloud error:", e);
  }
}

async function loadSentimentChart() {
  const { startDate, endDate } = getActiveDateRange();
  let url = "/api/summary";
  if (startDate && endDate) {
    url += `?start_date=${startDate}&end_date=${endDate}`;
  }
  try {
    const res = await fetch(url);
    const data = await res.json();
    const s = data.sentiment_distribution;

    const ctx = document.getElementById("sentimentChart").getContext("2d");
    if (sentimentChart) sentimentChart.destroy();

    sentimentChart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["낙관 (Bullish)", "경계 (Caution)", "중립 (Neutral)", "비관 (Bearish)"],
        datasets: [{
          data: [s.bullish || 0, s.caution || 0, s.neutral || 0, s.bearish || 0],
          backgroundColor: ["#10b981", "#f59e0b", "#38bdf8", "#ef4444"],
          borderColor: "rgba(18, 28, 50, 0.8)",
          borderWidth: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "right",
            labels: { color: "#cbd5e1", font: { size: 11, weight: "600" } }
          }
        },
        cutout: "68%"
      }
    });
  } catch (e) {
    console.error("Sentiment error:", e);
  }
}

function filterAnalystTopic(topic) {
  currentTopic = topic;
  const container = document.getElementById("topic-filter-tabs");
  container.querySelectorAll(".period-btn").forEach(btn => {
    btn.classList.toggle("active", btn.textContent.trim() === (topic === "all" ? "전체 주제" : topic));
  });
  loadAnalystMatrix();
}

async function loadAnalystMatrix() {
  const { startDate, endDate, isCustom } = getActiveDateRange();
  let query = `topic=${encodeURIComponent(currentTopic)}`;
  if (isCustom) {
    query += `&period=custom&start_date=${startDate}&end_date=${endDate}`;
  } else if (startDate && endDate) {
    query += `&period=${encodeURIComponent(currentPeriod)}&start_date=${startDate}&end_date=${endDate}`;
  } else {
    query += `&period=${encodeURIComponent(currentPeriod)}`;
  }

  try {
    const res = await fetch(`/api/analysts/matrix?${query}`);
    const data = await res.json();

    const grid = document.getElementById("analysts-grid");
    grid.innerHTML = "";

    if (data.length === 0) {
      grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 2rem;">선택된 조건에 해당하는 분석가 의견이 없습니다.</div>`;
      return;
    }

    data.forEach(item => {
      const card = document.createElement("div");
      card.className = "analyst-card";

      const topDiv = document.createElement("div");

      const header = document.createElement("div");
      header.className = "analyst-header";

      const profile = document.createElement("div");
      profile.className = "analyst-profile";

      const avatar = document.createElement("div");
      avatar.className = "analyst-avatar";
      avatar.textContent = (item.analyst_name || "?").slice(0, 1);

      const nameBox = document.createElement("div");

      const nameEl = document.createElement("div");
      nameEl.className = "analyst-name";
      nameEl.textContent = item.analyst_name || "";

      const chEl = document.createElement("div");
      chEl.className = "analyst-channel";
      chEl.textContent = item.channel_title || "";

      nameBox.appendChild(nameEl);
      nameBox.appendChild(chEl);

      profile.appendChild(avatar);
      profile.appendChild(nameBox);

      header.appendChild(profile);
      header.appendChild(createStanceBadgeElement(item.stance));

      const topicSpan = document.createElement("span");
      topicSpan.className = "opinion-topic";
      topicSpan.textContent = item.topic || "";

      const coreArg = document.createElement("div");
      coreArg.className = "core-argument";
      coreArg.textContent = item.core_argument || "";

      topDiv.appendChild(header);
      topDiv.appendChild(topicSpan);
      topDiv.appendChild(coreArg);

      if (item.key_quote) {
        const quoteDiv = document.createElement("div");
        quoteDiv.className = "quote-bubble";
        quoteDiv.textContent = `"${item.key_quote}"`;
        topDiv.appendChild(quoteDiv);
      }

      const footer = document.createElement("div");
      footer.className = "analyst-card-footer";

      const dateSpan = document.createElement("span");
      dateSpan.textContent = `📅 ${item.published_at || ""}`;

      const fBtnGroup = document.createElement("div");
      fBtnGroup.style.display = "flex";
      fBtnGroup.style.gap = "0.4rem";
      fBtnGroup.style.alignItems = "center";

      const ytBtn = document.createElement("a");
      ytBtn.href = sanitizeUrl(getSafeYouTubeUrl(item));
      ytBtn.target = "_blank";
      ytBtn.rel = "noopener noreferrer";
      ytBtn.className = "btn-yt-link";
      ytBtn.style.padding = "0.3rem 0.6rem";
      ytBtn.style.fontSize = "0.75rem";
      ytBtn.title = "유튜브 실제 영상 재생";
      ytBtn.textContent = "▶ 유튜브";

      const detailBtn = document.createElement("button");
      detailBtn.className = "btn-detail";
      detailBtn.textContent = "AI 심층 요약 ↗";
      detailBtn.addEventListener("click", () => openVideoDetail(item.video_id));

      fBtnGroup.appendChild(ytBtn);
      fBtnGroup.appendChild(detailBtn);

      footer.appendChild(dateSpan);
      footer.appendChild(fBtnGroup);

      card.appendChild(topDiv);
      card.appendChild(footer);

      grid.appendChild(card);
    });
  } catch (e) {
    console.error("Analyst matrix error:", e);
  }
}

function getSafeYouTubeUrl(video) {
  if (!video) return "https://www.youtube.com";
  const url = video.video_url || "";
  
  // If url has valid 11-char YouTube ID (e.g. watch?v=XXXXXXXXXXX)
  const match = url.match(/[?&]v=([a-zA-Z0-9_-]{11})(?:[&?]|$)/);
  if (match) {
    const vid = match[1];
    if (!vid.includes("_202") && !vid.startsWith("OGY_") && !vid.startsWith("YSH_") && !vid.startsWith("KIK_") && !vid.startsWith("LSY_") && !vid.startsWith("PSJ_") && !vid.startsWith("HCW_") && !vid.startsWith("SYK_") && !vid.startsWith("KHK_") && !vid.startsWith("USR_")) {
      return `https://www.youtube.com/watch?v=${vid}`;
    }
  }

  // If url is already an official search URL
  if (url.includes("youtube.com/results?search_query=")) {
    return url;
  }

  // If video_id itself is a real 11-char ID
  if (video.video_id && /^[a-zA-Z0-9_-]{11}$/.test(video.video_id) && !video.video_id.includes("_202")) {
    return `https://www.youtube.com/watch?v=${video.video_id}`;
  }

  // Fallback: Direct YouTube search for exact title and analyst name
  const query = `${video.title || ''} ${video.analyst_name || ''}`.trim();
  return `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`;
}

function getStanceBadge(stance) {
  const s = (stance || "Neutral").toLowerCase();
  if (s.includes("bullish") || s.includes("낙관")) {
    return `<span class="badge-tag bullish">Bullish 상승</span>`;
  } else if (s.includes("caution") || s.includes("신중") || s.includes("경계")) {
    return `<span class="badge-tag caution">Caution 경계</span>`;
  } else if (s.includes("bearish") || s.includes("비관") || s.includes("하락")) {
    return `<span class="badge-tag bearish">Bearish 하락</span>`;
  }
  return `<span class="badge-tag neutral">Neutral 중립</span>`;
}

function onSearchInput() {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(loadVideos, 300);
}

async function loadVideos() {
  const search = document.getElementById("video-search-input").value.trim();
  const cat = document.getElementById("filter-category").value;
  const analyst = document.getElementById("filter-analyst").value;
  const sentiment = document.getElementById("filter-sentiment").value;

  const { startDate, endDate } = getActiveDateRange();
  let url = `/api/videos?limit=50`;
  if (startDate) url += `&start_date=${startDate}`;
  if (endDate) url += `&end_date=${endDate}`;

  if (search) url += `&search=${encodeURIComponent(search)}`;
  if (cat && cat !== "all") url += `&category=${encodeURIComponent(cat)}`;
  if (analyst && analyst !== "all") url += `&analyst=${encodeURIComponent(analyst)}`;
  if (sentiment && sentiment !== "all") url += `&sentiment=${encodeURIComponent(sentiment)}`;

  try {
    const res = await fetch(url);
    const videos = await res.json();

    const grid = document.getElementById("video-grid");
    grid.innerHTML = "";

    if (videos.length === 0) {
      grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem;">일치하는 영상이 없습니다.</div>`;
      return;
    }

    videos.forEach(v => {
      const card = document.createElement("div");
      card.className = "video-card";

      // 1. Thumbnail wrap
      const thumbWrap = document.createElement("div");
      thumbWrap.className = "thumbnail-wrap";

      const img = document.createElement("img");
      img.src = sanitizeUrl(v.thumbnail_url || "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=640");
      img.alt = v.title || "";
      img.className = "thumbnail-img";
      img.loading = "lazy";
      img.onerror = () => { img.src = "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=640"; };

      const catBadge = document.createElement("span");
      catBadge.className = "category-badge-overlay";
      catBadge.textContent = v.category || "";

      const analystBadge = document.createElement("span");
      analystBadge.className = "duration-badge-overlay";
      analystBadge.textContent = v.analyst_name || "";

      thumbWrap.appendChild(img);
      thumbWrap.appendChild(catBadge);
      thumbWrap.appendChild(analystBadge);

      // 2. Video content
      const content = document.createElement("div");
      content.className = "video-content";

      const topSection = document.createElement("div");

      const metaTop = document.createElement("div");
      metaTop.className = "video-meta-top";

      const chSpan = document.createElement("span");
      chSpan.textContent = v.channel_title || "";

      const pubSpan = document.createElement("span");
      pubSpan.textContent = v.published_at || "";

      metaTop.appendChild(chSpan);
      metaTop.appendChild(pubSpan);

      const titleEl = document.createElement("h3");
      titleEl.className = "video-title";
      titleEl.title = v.title || "";
      titleEl.textContent = v.title || "";

      const summaryEl = document.createElement("p");
      summaryEl.className = "video-summary-preview";
      summaryEl.textContent = v.summary_text || "분석 텍스트 준비 중...";

      topSection.appendChild(metaTop);
      topSection.appendChild(titleEl);
      topSection.appendChild(summaryEl);

      // 3. Actions
      const actions = document.createElement("div");
      actions.className = "video-actions";

      const stanceBadge = createStanceBadgeElement(v.sentiment_label);

      const btnGroup = document.createElement("div");
      btnGroup.style.display = "flex";
      btnGroup.style.gap = "0.5rem";
      btnGroup.style.alignItems = "center";

      const ytLink = document.createElement("a");
      ytLink.href = sanitizeUrl(getSafeYouTubeUrl(v));
      ytLink.target = "_blank";
      ytLink.rel = "noopener noreferrer";
      ytLink.className = "btn-yt-link";
      ytLink.title = "유튜브 실제 영상 재생";
      ytLink.textContent = "▶ 유튜브";

      const aiBtn = document.createElement("button");
      aiBtn.className = "btn-ai-summary";
      aiBtn.textContent = "🤖 AI 요약";
      aiBtn.addEventListener("click", () => openVideoDetail(v.video_id));

      btnGroup.appendChild(ytLink);
      btnGroup.appendChild(aiBtn);

      actions.appendChild(stanceBadge);
      actions.appendChild(btnGroup);

      content.appendChild(topSection);
      content.appendChild(actions);

      card.appendChild(thumbWrap);
      card.appendChild(content);

      grid.appendChild(card);
    });
  } catch (e) {
    console.error("Load videos error:", e);
  }
}

async function openVideoDetail(videoId) {
  const modal = document.getElementById("video-modal");
  const modalBody = document.getElementById("modal-body");
  modal.classList.add("open");

  modalBody.innerHTML = `
    <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
      <div style="font-size: 2rem; margin-bottom: 1rem;">⏳</div>
      <div>Ollama (${currentModel}) AI가 3줄 요약 및 투자 시사점을 생성 중입니다...</div>
    </div>
  `;

  try {
    const [videoRes, aiRes] = await Promise.all([
      fetch(`/api/videos/${videoId}`),
      fetch(`/api/videos/${videoId}/summarize?model=${currentModel}`, { method: "POST" })
    ]);

    const video = await videoRes.json();
    const ai = await aiRes.json();

    document.getElementById("modal-title").textContent = video.title;

    const pointsHtml = (ai.key_points || [])
      .map(pt => `<li>${escapeHTML(pt)}</li>`)
      .join("");

    const assetsHtml = (ai.mentioned_assets || [])
      .map(a => `<span class="badge-tag neutral" style="margin-right: 0.35rem; margin-bottom: 0.35rem;">${escapeHTML(a)}</span>`)
      .join("");

    modalBody.innerHTML = `
      <div>
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
          <div style="font-size: 0.88rem; color: var(--text-secondary);">
            📺 <strong>${escapeHTML(video.channel_title)}</strong> | 분석가: <strong>${escapeHTML(video.analyst_name)}</strong> | 발행일: ${escapeHTML(video.published_at)}
          </div>
          <div style="display: flex; gap: 0.5rem; align-items: center;">
            ${getStanceBadge(ai.analyst_stance || video.sentiment_label)}
            <a href="${sanitizeUrl(getSafeYouTubeUrl(video))}" target="_blank" rel="noopener noreferrer" class="btn-primary" style="padding: 0.35rem 0.8rem; font-size: 0.78rem;" title="유튜브 실제 영상 재생">
              유튜브 원본 열기 ↗
            </a>
          </div>
        </div>

        <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--accent-cyan); margin-bottom: 0.6rem;">
          🎯 3줄 핵심 요약 & 주장
        </h4>
        <ul class="ai-points-list">
          ${pointsHtml}
        </ul>
      </div>

      <div class="insight-grid">
        <div class="insight-box">
          <div class="insight-box-title">💡 투자 시사점 & 대응 전략</div>
          <div style="font-size: 0.86rem; color: var(--text-primary); line-height: 1.6;">
            ${escapeHTML(ai.investment_implication || "매크로 변곡점 관망 및 방어적 분산투자 권고")}
          </div>
        </div>

        <div class="insight-box">
          <div class="insight-box-title">⚠️ 주요 리스크 요인</div>
          <div style="font-size: 0.86rem; color: var(--text-primary); line-height: 1.6;">
            ${escapeHTML(ai.risk_factors || "통화정책 변동성 및 지정학적 리스크")}
          </div>
        </div>
      </div>

      <div>
        <div style="font-size: 0.82rem; font-weight: 700; color: var(--text-secondary); margin-bottom: 0.4rem;">
          🏷️ 언급된 핵심 자산 / 종목
        </div>
        <div style="display: flex; flex-wrap: wrap;">
          ${assetsHtml || '<span style="color: var(--text-muted); font-size: 0.82rem;">정보 없음</span>'}
        </div>
      </div>

      <div class="transcript-collapse">
        <details>
          <summary style="font-size: 0.84rem; font-weight: 700; color: var(--text-secondary); cursor: pointer;">
            📜 전문 스크립트 / 자막 보기 (클릭하여 펼치기)
          </summary>
          <div class="transcript-text">${escapeHTML(video.transcript_text || "자막 텍스트가 없습니다.")}</div>
        </details>
      </div>
    `;
  } catch (e) {
    modalBody.innerHTML = `<div style="color: var(--accent-red); padding: 2rem; text-align: center;">상세 정보를 불러오는 중 오류가 발생했습니다.</div>`;
  }
}

function closeModal(modalId) {
  if (modalId) {
    const m = document.getElementById(modalId);
    if (m) m.classList.remove("open");
  } else {
    document.querySelectorAll(".modal-overlay").forEach(m => m.classList.remove("open"));
  }
}

function closeModalOnBackdrop(e) {
  if (e.target.classList.contains("modal-overlay")) {
    e.target.classList.remove("open");
  }
}

async function openTimelineModal() {
  const modal = document.getElementById("timeline-modal");
  modal.classList.add("open");
  filterTimelineAnalyst('all');
}

async function filterTimelineAnalyst(analystName) {
  const container = document.getElementById("timeline-analyst-tabs");
  container.querySelectorAll(".period-btn").forEach(btn => {
    btn.classList.toggle("active", btn.textContent.trim() === (analystName === "all" ? "전체" : analystName));
  });

  const content = document.getElementById("timeline-modal-content");
  content.innerHTML = `<div style="text-align: center; padding: 2rem; color: var(--text-muted);">시각 변화 데이터를 불러오는 중...</div>`;

  try {
    let url = "/api/analysts/timeline";
    if (analystName && analystName !== "all") {
      url += `?analyst=${encodeURIComponent(analystName)}`;
    }
    const res = await fetch(url);
    const groups = await res.json();

    content.innerHTML = "";
    if (groups.length === 0) {
      content.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 2rem;">해당 전문가의 시각 기록이 없습니다.</div>`;
      return;
    }

    groups.forEach(g => {
      const groupCard = document.createElement("div");
      groupCard.className = "timeline-analyst-group";

      const streamHtml = g.timeline.map(item => `
        <div class="timeline-point">
          <span class="timeline-date-tag">📅 ${escapeHTML(item.published_at)} (${escapeHTML(item.period_label)})</span>
          <div class="timeline-opinion-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem; flex-wrap: wrap; gap: 0.3rem;">
              <strong style="color: var(--text-heading); font-size: 0.9rem;">${escapeHTML(item.title)}</strong>
              <div style="display: flex; gap: 0.4rem; align-items: center;">
                ${getStanceBadge(item.stance)}
                <a href="${sanitizeUrl(getSafeYouTubeUrl(item))}" target="_blank" rel="noopener noreferrer" class="btn-yt-link" style="padding: 0.2rem 0.5rem; font-size: 0.72rem;" title="유튜브 실제 영상 재생">
                  ▶ 원본
                </a>
              </div>
            </div>
            <div style="font-size: 0.85rem; color: var(--text-primary); margin-bottom: 0.4rem;">
              <span class="opinion-topic" style="margin-right: 0.4rem;">${escapeHTML(item.topic)}</span>
              ${escapeHTML(item.core_argument)}
            </div>
            ${item.key_quote ? `<div class="quote-bubble" style="margin-bottom: 0.3rem;">"${escapeHTML(item.key_quote)}"</div>` : ""}
          </div>
        </div>
      `).join("");

      groupCard.innerHTML = `
        <div class="timeline-analyst-name">
          <span class="analyst-avatar" style="width: 32px; height: 32px; font-size: 0.9rem;">${escapeHTML(g.analyst_name.slice(0, 1))}</span>
          ${escapeHTML(g.analyst_name)} 전문가의 시간별 뷰 변화
        </div>
        <div class="timeline-stream">
          ${streamHtml}
        </div>
      `;
      content.appendChild(groupCard);
    });
  } catch (e) {
    content.innerHTML = `<div style="color: var(--accent-red); padding: 2rem; text-align: center;">데이터 로드 중 오류가 발생했습니다.</div>`;
  }
}


function openCreateModal() {
  document.getElementById("create-modal").classList.add("open");
}

async function handleCreateVideo(e) {
  e.preventDefault();
  const analyst = document.getElementById("form-analyst").value.trim();
  const date = document.getElementById("form-date").value;
  const title = document.getElementById("form-title").value.trim();
  const category = document.getElementById("form-category").value;
  const stance = document.getElementById("form-stance").value;
  const url = document.getElementById("form-url").value.trim();
  const summary = document.getElementById("form-summary").value.trim();
  const quote = document.getElementById("form-quote").value.trim();

  try {
    const res = await fetch("/api/videos/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        analyst_name: analyst,
        published_at: date,
        title: title,
        category: category,
        sentiment_label: stance.toLowerCase(),
        stance: stance,
        video_url: url,
        summary_text: summary,
        core_argument: summary,
        key_quote: quote,
        period_label: date.startsWith("2026-10") ? "2026-10" : (date.startsWith("2026") ? "2026-H2" : "2024-H2")
      })
    });
    const result = await res.json();
    if (res.ok) {
      showToast(result.message || "새로운 의견이 성공적으로 등록되었습니다!");
      closeModal('create-modal');
      document.getElementById("create-video-form").reset();
      fetchAllData();
    } else {
      showToast(result.detail || "등록 중 오류가 발생했습니다.");
    }
  } catch (err) {
    showToast("서버 통신 중 오류가 발생했습니다.");
  }
}


async function triggerPipeline() {
  const btn = document.getElementById("btn-pipeline");
  const icon = document.getElementById("pipeline-icon");
  const text = document.getElementById("pipeline-text");

  btn.disabled = true;
  icon.textContent = "⏳";
  text.textContent = "수집 및 Kiwi 형태소 분석 중...";

  try {
    const res = await fetch("/api/pipeline/run", { method: "POST" });
    const data = await res.json();
    showToast(data.message);

    setTimeout(async () => {
      await fetchAllData();
      btn.disabled = false;
      icon.textContent = "⚡";
      text.textContent = "유튜브 최신 수집 & 분석";
      showToast("데이터 갱신이 완료되었습니다!");
    }, 4000);
  } catch (e) {
    btn.disabled = false;
    icon.textContent = "⚡";
    text.textContent = "유튜브 최신 수집 & 분석";
    showToast("파이프라인 실행 중 오류가 발생했습니다.");
  }
}

function openMonthlyCollectModal() {
  const modal = document.getElementById("monthly-collect-modal");
  if (modal) modal.classList.add("open");
}

async function handleStartMonthlyCollection() {
  const targetMonth = document.getElementById("collect-target-month").value;
  const limit = document.getElementById("collect-limit-per-channel").value || 5;

  if (!targetMonth) {
    showToast("수집 대상 연-월을 선택해주세요.");
    return;
  }

  try {
    const res = await fetch(`/api/pipeline/monthly?month=${targetMonth}`, { method: "POST" });
    const data = await res.json();
    showToast(data.message || `${targetMonth} 수집 파이프라인이 시작되었습니다.`);
    closeModal('monthly-collect-modal');

    // After 4 seconds, refresh month list and select the newly collected month
    setTimeout(async () => {
      await fetchAvailableMonths();
      selectMonthDropdown(targetMonth);
      showToast(`${targetMonth} 데이터가 갱신되었습니다!`);
    }, 4000);
  } catch (e) {
    showToast("월간 수집 요청 중 오류가 발생했습니다.");
  }
}

function showToast(msg) {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = msg;
  container.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 3500);
}
