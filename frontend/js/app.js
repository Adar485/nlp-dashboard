const API_URL = "http://localhost:8000/api";

async function analyzeText() {
  const text = document.getElementById("textInput").value.trim();
  if (!text) return alert("Lütfen bir metin girin!");

  const btn = document.getElementById("analyzeBtn");
  btn.innerHTML = '<span class="spinner"></span>Analiz ediliyor...';
  btn.disabled = true;

  try {
    const res = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    displayResult(data);
    await loadCharts();
  } catch (err) {
    alert("Hata: " + err.message);
  } finally {
    btn.innerHTML = "Analiz Et";
    btn.disabled = false;
  }
}

async function analyzeFile() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  if (!file) return;

  document.getElementById("fileName").innerHTML =
    '<span class="spinner"></span>' + file.name + " analiz ediliyor...";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_URL}/analyze-file`, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();

    if (res.ok) {
      document.getElementById("fileName").textContent = file.name + " ✅";
      displayResult(data);
      await loadCharts();
    } else {
      document.getElementById("fileName").textContent = file.name + " ❌";
      alert("Hata: " + data.detail);
    }
  } catch (err) {
    document.getElementById("fileName").textContent = file.name + " ❌";
    alert("Hata: " + err.message);
  }

  fileInput.value = "";
}

function displayResult(data) {
  document.getElementById("result").style.display = "grid";

  const label = document.getElementById("sentimentLabel");
  label.textContent = data.sentiment_label.toUpperCase();
  label.className = `sentiment-${data.sentiment_label}`;

  document.getElementById("sentimentScore").textContent =
    `Güven: %${(data.sentiment_score * 100).toFixed(1)}`;

  document.getElementById("langLabel").textContent =
    `Dil: ${data.language === "tr" ? "🇹🇷 Türkçe" : "🇬🇧 İngilizce"}`;

  const entList = document.getElementById("entitiesList");
  entList.innerHTML = data.entities.length
    ? data.entities
        .map(
          (e) =>
            `<li><strong>${e.word}</strong> → ${e.entity} (${e.score})</li>`,
        )
        .join("")
    : "<li>Varlık bulunamadı</li>";

  const kwList = document.getElementById("keywordsList");
  kwList.innerHTML = data.keywords
    .map((k) => `<li>${k.word} (${k.count})</li>`)
    .join("");
}

window.addEventListener("DOMContentLoaded", loadCharts);
