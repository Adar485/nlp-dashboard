# 📊 NLP Metin Analiz Dashboard

Metin ve dosya (TXT/PDF) üzerinde duygu analizi, isimli varlık tanıma (NER) ve anahtar kelime çıkarma yapan, sonuçları Chart.js ile görselleştiren full-stack bir web uygulaması.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Redis](https://img.shields.io/badge/Redis-7-red)
![Chart.js](https://img.shields.io/badge/Chart.js-4-orange)

---

## 🚀 Özellikler

- **Duygu Analizi** — Türkçe ve İngilizce metin desteği
- **İsimli Varlık Tanıma (NER)** — Kişi, yer, organizasyon tespiti
- **Anahtar Kelime Çıkarma** — Metin içindeki önemli kelimelerin frekans analizi
- **Otomatik Dil Algılama** — Türkçe / İngilizce otomatik tespit
- **Dosya Yükleme** — TXT ve PDF dosya analizi
- **Redis Cache** — Tekrarlayan analizlerde hızlı yanıt
- **Görselleştirme** — Doughnut, bar ve line chart ile interaktif grafikler
- **Responsive Tasarım** — Mobil uyumlu arayüz

---

## 🏗️ Teknik Mimari
```
┌─────────────┐     ┌──────────────────┐     ┌────────────┐
│  Frontend    │────▶│  FastAPI Backend  │────▶│ PostgreSQL │
│  (Chart.js)  │◀────│  + NLP Pipeline   │     └────────────┘
└─────────────┘     │                  │────▶┌────────────┐
                    └──────────────────┘     │   Redis    │
                                             └────────────┘
```

---

## 🛠️ Kullanılan Teknolojiler

| Katman | Teknoloji |
|--------|-----------|
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Veritabanı | PostgreSQL 16 |
| Cache | Redis 7 |
| NLP | HuggingFace Transformers, PyTorch |
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Konteyner | Docker, Docker Compose |

---

## 🤖 NLP Modelleri

| Model | Görev | Dil |
|-------|-------|-----|
| `nlptown/bert-base-multilingual-uncased-sentiment` | Duygu Analizi | İngilizce |
| `savasy/bert-base-turkish-sentiment-cased` | Duygu Analizi | Türkçe |
| `dbmdz/bert-large-cased-finetuned-conll03-english` | NER | İngilizce |

---

## 📦 Kurulum

### Gereksinimler

- Python 3.10+
- Docker Desktop
- Git

### 1. Repoyu klonla
```bash
git clone https://github.com/Adar485/nlp-dashboard.git
cd nlp-dashboard
```

### 2. PostgreSQL ve Redis'i başlat
```bash
docker-compose up -d
```

### 3. Python sanal ortamı oluştur ve bağımlılıkları kur
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install torch --index-url https://download.pytorch.org/whl/cpu --timeout 300
pip install -r requirements.txt
```

### 4. Backend'i başlat
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Frontend'i başlat (yeni terminal)
```bash
cd frontend
python -m http.server 3000
```

### 6. Tarayıcıda aç

- **Dashboard:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs

---

## 📡 API Endpoint'leri

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | `/api/analyze` | Metin analizi |
| POST | `/api/analyze-file` | Dosya analizi (TXT/PDF) |
| GET | `/api/analyses` | Tüm analizleri listele |
| GET | `/api/stats` | İstatistikleri getir |

---

## 📸 Ekran Görüntüsü

> Dashboard'u çalıştırdıktan sonra ekran görüntüsü ekleyebilirsiniz.

---

## 📄 Lisans

Bu proje MIT lisansı ile lisanslanmıştır.