# 🚀 Crypto Price Forecasting Platform

A modern, real-time cryptocurrency price forecasting application built with machine learning and interactive visualization. This web application uses advanced regression models to predict crypto price movements with a sleek, responsive interface.

## ✨ Features

- **Real-time Data Streaming**: Live cryptocurrency price feeds using CCXT
- **ML-Powered Predictions**: Random Forest models for accurate price forecasting
- **Interactive Visualizations**: Plotly-powered charts for data exploration and predictions
- **Modern UI**: FastHTML with MonsterUI components and Pico CSS styling
- **Production-Ready**: Docker containerization with hot-reload support
- **Database Integration**: SQLAlchemy ORM for persistent data storage

## 🏗️ Architecture

```
crypto_forecasting/
├── backend/
│   ├── data_stream/          # Real-time price data fetching
│   │   ├── stream_prices.py  # CCXT integration
│   │   └── data_charts.py    # Chart data processing
│   └── predict_ml/           # Machine learning pipeline
│       ├── model_service.py  # Model inference
│       ├── runner.py         # Prediction runner
│       └── config/           # Configuration management
├── frontend/                 # FastHTML web interface
│   ├── pages/               # Route handlers
│   └── components/          # Reusable UI components
└── app.py                   # Main application entry point
```

## 🔧 Tech Stack

- **Frontend**: FastHTML, MonsterUI, HTMX, Plotly
- **Backend**: Python, SQLAlchemy, scikit-learn, pandas, numpy
- **Data**: CCXT, pandas, numpy
- **Deployment**: Docker, Docker Compose, uv (Python package manager)

## 📋 Prerequisites

- **Python 3.14+** (for local development)
- **Docker & Docker Compose** (for containerized setup)
- **uv** (modern Python package manager - install from [astral.sh/uv](https://astral.sh/uv))

---

## 🚀 Quick Start

### Option 1: Local Development with `uv` (Recommended)

The fastest way to get up and running locally.

#### Install `uv`

If you don't have `uv` installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on Windows with PowerShell:

```powershell
powershell -c "irm https://astral.sh/uv/install.sh | iex"
```

#### Clone & Setup

```bash
# Clone the repository
git clone https://github.com/magdy288/crypto_forecasting.git
cd crypto_forecasting

# Install dependencies (creates virtual environment automatically)
uv sync

# Run the application
uv run python app.py
```

The app will be available at **http://localhost:8000**

#### Additional `uv` Commands

```bash
# Run a specific module
uv run python -m backend.predict_ml.runner

# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Update dependencies
uv sync
```

---

### Option 2: Docker Containerization

Run the entire application in a containerized environment with automatic hot-reload.

#### Prerequisites
- Docker Desktop installed and running

#### Build & Run

```bash
# Build and start the application
docker compose up --build

# Run in detached mode (background)
docker compose up -d --build

# View logs
docker compose logs -f web

# Stop the application
docker compose down
```

The app will be available at **http://localhost:8000**

#### Docker Features

- **Hot-reload**: Changes to Python files automatically trigger reloads
- **Frozen dependencies**: `uv.lock` ensures reproducible builds
- **Multi-stage optimization**: Lightweight final image

#### Useful Docker Commands

```bash
# Rebuild the image
docker compose build --no-cache

# Interactive shell in container
docker compose exec web bash

# Clean up all containers and volumes
docker compose down -v

# View resource usage
docker stats
```

---

## 🔄 Workflow Comparison

| Operation | `uv` | Docker |
|-----------|------|--------|
| **Setup** | `uv sync` | `docker compose up --build` |
| **Run** | `uv run python app.py` | `docker compose up` |
| **Dependencies** | `uv add package-name` | Edit `pyproject.toml`, rebuild |
| **Debugging** | IDE breakpoints, direct logs | `docker compose logs` |
| **Isolation** | System-wide Python | Containerized environment |
| **Production** | ✅ Suitable | ✅ Recommended |

---

## 📚 Project Structure

### Backend

- **`data_stream/`**: Real-time cryptocurrency data fetching
  - `stream_prices.py` - CCXT exchange integration
  - `data_charts.py` - Chart data preparation

- **`predict_ml/`**: Machine learning pipeline
  - `model_service.py` - Model loading and inference
  - `runner.py` - Prediction orchestration
  - `config/` - Database, logging, and model configuration
  - `db/` - Database models and ORM
  - `model/models/` - Trained models (e.g., `rf_v1`)
  - `pipeline/` - Feature engineering and model pipeline

### Frontend

- **`pages/`**: Route handlers
  - `home_page.py` - Live price streaming and charts
  - `pred_page.py` - Prediction display and analysis

- **`components/`**: Reusable UI components
  - `layout.py` - Base layout and navigation
  - `crypto_cards.py` - Crypto display cards
  - `pred_table.py` - Prediction results table

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=sqlite:///crypto_forecasting.db

# Logging
LOG_LEVEL=INFO
LOG_DIR=backend/predict_ml/logs

# Exchange API (optional)
EXCHANGE_API_KEY=your_key_here
EXCHANGE_API_SECRET=your_secret_here
```

---

## 🧪 Testing & Development

### Run Tests

```bash
uv run pytest
```

### Format Code

```bash
# Format with black
uv run black .

# Check with flake8
uv run flake8 .
```

### Generate Logs

Logs are automatically saved to `backend/predict_ml/logs/` with rotation and filtering.

---

## 📦 Deployment Guide for End Users

### Step 1: Get the Application

**Option A: Download from GitHub (Recommended for most users)**

1. Visit [https://github.com/magdy288/crypto_forecasting](https://github.com/magdy288/crypto_forecasting)
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Extract the ZIP file to your desired location
5. Open the extracted folder

**Option B: Clone with Git (for developers)**

```bash
git clone https://github.com/magdy288/crypto_forecasting.git
cd crypto_forecasting
```

---

### Step 2: Install Docker (One-time Setup)

The easiest way to run the application is with Docker. Follow these steps based on your system:

#### 🪟 Windows
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Run the installer and follow the setup wizard
3. Restart your computer
4. Open PowerShell and verify: `docker --version`

#### 🍎 macOS
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. Open the `.dmg` file and drag Docker to Applications
3. Launch Docker from Applications
4. Verify in Terminal: `docker --version`

#### 🐧 Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER
# Restart terminal or run: newgrp docker
```

---

### Step 3: Launch the Application

Navigate to your application folder and run:

```bash
docker compose up
```

**That's it!** The application will start automatically.

---

### Step 4: Access the Application

Open your web browser and go to:

```
http://localhost:8000
```

You should see the Crypto Forecasting Platform interface!

---

### 🛑 Stopping the Application

To stop the application, use one of these methods:

**Method 1: Terminal**
- Press `Ctrl + C` in the terminal where you ran `docker compose up`

**Method 2: Background Mode**
If you started with `docker compose up -d`, stop it with:
```bash
docker compose down
```

---

### ⚙️ Configuration (Optional)

If you need to customize the application, create a `.env` file in the application folder:

```env
DATABASE_URL=sqlite:///crypto_forecasting.db
LOG_LEVEL=INFO
```

Then restart the application.

---

### 🔧 Common Troubleshooting

| Issue | Solution |
|-------|----------|
| **"Port 8000 already in use"** | Close other applications using port 8000, or stop the app and restart |
| **"Docker not found"** | Restart your computer after installing Docker, or reinstall Docker Desktop |
| **"Application won't start"** | Make sure Docker Desktop is running. Check the notification area for Docker icon |
| **"Connection refused"** | Wait 10-15 seconds for the app to fully start, then refresh your browser |
| **"Blank page in browser"** | Try clearing browser cache (Ctrl+Shift+Delete) and refresh |

---

### 📱 Accessing from Other Devices

To access the application from another computer on your network:

1. Find your computer's IP address:
   - **Windows**: Open Command Prompt and type `ipconfig` (look for "IPv4 Address")
   - **Mac/Linux**: Open Terminal and type `ifconfig` (look for "inet")

2. On the other device, open your browser and go to:
   ```
   http://<your-computer-ip>:8000
   ```

---

### 📊 Monitoring the Application

To see what the application is doing:

```bash
# View logs in real-time
docker compose logs -f

# View logs of the last 50 lines
docker compose logs --tail 50
```

---

### 🔄 Updating the Application

When we release updates:

```bash
# Stop the current application
docker compose down

# Download the latest version
# (Re-download from GitHub or: git pull)

# Start the updated application
docker compose up
```

---

## 🐛 Troubleshooting

### `uv` Issues

| Problem | Solution |
|---------|----------|
| `uv: command not found` | Add `~/.local/bin` to PATH: `export PATH="$HOME/.local/bin:$PATH"` |
| `Python 3.14+ required` | Install via `uv python install 3.14` |
| Dependency conflicts | Run `uv sync --refresh` to update lock file |

### Docker Issues

| Problem | Solution |
|---------|----------|
| Port 8000 in use | `docker compose down` or use `docker run -p 9000:8000 ...` |
| Build fails | `docker compose build --no-cache` and check logs |
| Hot-reload not working | Verify `compose.yaml` watch section and file permissions |

### Application Issues

| Problem | Solution |
|---------|----------|
| Database not found | Check `DATABASE_URL` in `.env` |
| Model not loading | Verify model exists in `backend/predict_ml/model/models/rf_v1/` |
| Port 8000 already in use | Change port in `app.py` or Docker config |

---

## 📖 Documentation Links

- [FastHTML Docs](https://www.fastht.ml/)
- [CCXT Documentation](https://docs.ccxt.com/)
- [scikit-learn Guide](https://scikit-learn.org/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [uv Package Manager](https://docs.astral.sh/uv/)
- [Docker Documentation](https://docs.docker.com/)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Contact

For questions or support, reach out via GitHub Issues or contact the maintainer directly.

---

**Happy Trading! 📈**