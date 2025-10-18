# 🌐 Eden's Personal URL Shortener

A lightweight URL shortener built with **Python (aiohttp + SQLite)** and a simple **HTML frontend**.  
Designed for personal use, not for production or multi-user environments.

---

## ⚙️ Features

- Simple HTML interface (`Short.html`)
- Shortens URLs into readable word combinations  
  e.g. `pen-odd-surf-bunny-nip-cad`
- Stores shortened URLs locally in a SQLite database  
- Auto-deletes entries older than **3 months**
- Local rate limiting (3 requests per IP per minute)
- Basic Base85 encoding (not encryption, just to avoid plain text storage)
- Built-in redirect handler
- Frontend includes:
  - Live server status indicator  
  - Simple rate limit (3 seconds between requests per client)  
  - Copy-to-clipboard button  

---
Using Github so cloudflare forwards traffic to it from my domain:

https://shorten.call-your.dad/

--- 


