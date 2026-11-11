# Data Mining 2024 — Web Scraping

Praktikum **Data Mining**: mengambil data dari halaman web dinamis menggunakan
Selenium (Firefox headless) dan BeautifulSoup, lalu menyimpannya sebagai JSON.

| Skrip | Sumber | Output |
|---|---|---|
| `Prak1(scrap Web).py` | Daftar kelas Dicoding Academy | `dicoding_data.json` |
| `ScappWeb.py` | IMDb Top 250 Movies | `Imdb_data2.json` |

Field IMDb: `movie_name`, `movie_rate`, `movie_year`, `movie_duration`, `movie_age`, `total_review`.

## Cara menjalankan
Prasyarat: Python 3, Firefox, dan [geckodriver](https://github.com/mozilla/geckodriver/releases) di PATH.
```bash
pip install -r requirements.txt
python ScappWeb.py
```

> Struktur HTML situs sumber bisa berubah sewaktu-waktu, sehingga selektor di skrip
> mungkin perlu diperbarui.
