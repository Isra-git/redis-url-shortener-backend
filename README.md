# ⚡ URL Shortener (Backend)

This is the backend of a Full-Stack URL shortener application. Built with **Python** and **FastAPI**, it provides a blazing-fast REST API to generate, store, and retrieve short links. It uses **Redis** as a cloud database (via Upstash) for ultra-low latency data storage and retrieval.

🔗 **Frontend Repository:** [https://github.com/Isra-git/redis-url-shortener-frontend]
🔗 **Live Frontend Demo:** [https://redis-url-shortener-frontend.netlify.app/](https://redis-url-shortener-frontend.netlify.app/)

## ✨ Key Features

- **FastAPI Framework:** High-performance API built with modern Python type hints.
- **Redis Integration:** Uses Upstash Redis for instant key-value storage of URLs.
- **Collision Prevention:** Implements a `while` loop with Redis `SETNX` to ensure every generated short code is 100% unique.
- **CORS Configured:** Fully configured to accept requests from local development environments and production frontends.
- **Automatic Redirection:** Built-in endpoint to seamlessly redirect users from a short link to the original URL.

## 🛠️ Technologies Used

- **Python 3+**
- **FastAPI:** Main framework for building the API.
- **Uvicorn:** ASGI web server to run FastAPI.
- **Redis (Upstash):** Cloud database for storing the URLs.
- **Pydantic:** Data validation and settings management.
- **python-dotenv:** For managing environment variables securely.

## 🚀 Local Installation & Usage

If you want to clone this project and run it on your local machine, follow these steps:

### 1. Clone the repository

```bash
git clone [https://github.com/Isra-git/redis-url-shortener-backend.git](https://github.com/Isra-git/redis-url-shortener-backend.git)
cd redis-url-shortener-backend
```
