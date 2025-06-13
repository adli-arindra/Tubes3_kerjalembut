# i. Penjelasan Program
Program ini adalah sebuah aplikasi manajemen CV ATS yang mengimplementasikan KMP, Boyer Moore, Aho-Corasick, dan Regex dalam pemilahan CV yang ditampilkan.

# ii. Requirement Program
1. Memiliki docker
2. Memliki python dan pip
3. Buatlah venv dengan library yang sesuai dengan menuliskan command berikut

```bash
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
```

# iii. Command
Untuk menjalankan program, pertama jalankan dulu daemon docker pada komputer. Lalu pada root folder tuliskan command berikut

```bash
docker compose up -d db
python -m src.main
```

Untuk menghentikan docker, maka tuliskan command berikut

```bash
docker compose down
```

# iv. Author
Program ini dibuat oleh:
- Stefan Mattew Susanto (13523020)
- Muhammad Adli Arindra (18222089)
- Benedictus Nelson (13523150)