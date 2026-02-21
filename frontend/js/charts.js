let sentimentChart, keywordsChart, timelineChart;

async function loadCharts() {
  try {
    const statsRes = await fetch(`${API_URL}/stats`);
    const stats = await statsRes.json();

    const analysesRes = await fetch(`${API_URL}/analyses?limit=20`);
    const analyses = await analysesRes.json();

    drawSentimentPie(stats.sentiment_distribution);
    drawKeywordsBar(analyses);
    drawTimeline(analyses);
  } catch (err) {
    console.log("Chart yükleme hatası:", err);
  }
}

function drawSentimentPie(distribution) {
  const ctx = document.getElementById("sentimentChart").getContext("2d");
  if (sentimentChart) sentimentChart.destroy();

  sentimentChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: Object.keys(distribution),
      datasets: [
        {
          data: Object.values(distribution),
          backgroundColor: ["#22c55e", "#ef4444", "#eab308"],
        },
      ],
    },
    options: {
      plugins: {
        title: { display: true, text: "Duygu Dağılımı", color: "#e2e8f0" },
        legend: { labels: { color: "#e2e8f0" } },
      },
    },
  });
}

function drawKeywordsBar(analyses) {
  const ctx = document.getElementById("keywordsChart").getContext("2d");
  if (keywordsChart) keywordsChart.destroy();

  const allKw = {};
  analyses.forEach((a) => {
    (a.keywords || []).forEach((k) => {
      allKw[k.word] = (allKw[k.word] || 0) + k.count;
    });
  });
  const sorted = Object.entries(allKw)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  keywordsChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: sorted.map((s) => s[0]),
      datasets: [
        {
          label: "Frekans",
          data: sorted.map((s) => s[1]),
          backgroundColor: "#3b82f6",
        },
      ],
    },
    options: {
      indexAxis: "y",
      plugins: {
        title: { display: true, text: "En Sık Kelimeler", color: "#e2e8f0" },
        legend: { display: false },
      },
      scales: {
        x: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } },
        y: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } },
      },
    },
  });
}

function drawTimeline(analyses) {
  const ctx = document.getElementById("timelineChart").getContext("2d");
  if (timelineChart) timelineChart.destroy();

  const reversed = [...analyses].reverse();

  timelineChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: reversed.map((a, i) => `#${i + 1}`),
      datasets: [
        {
          label: "Duygu Skoru",
          data: reversed.map((a) => a.sentiment_score),
          borderColor: "#8b5cf6",
          backgroundColor: "rgba(139,92,246,0.1)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "Duygu Skoru Zaman Çizelgesi",
          color: "#e2e8f0",
        },
        legend: { labels: { color: "#e2e8f0" } },
      },
      scales: {
        x: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } },
        y: {
          ticks: { color: "#94a3b8" },
          grid: { color: "#334155" },
          min: 0,
          max: 1,
        },
      },
    },
  });
}
