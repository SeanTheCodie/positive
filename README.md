# Positive Company Signals

A Streamlit prototype for a UK-first company monitoring product.

## Run

```powershell
streamlit run app.py
```

## Raspberry Pi Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Then open `http://<pi-ip-address>:8501` from another device on the same network.

## Companies House API Key

Do not commit your real API key to GitHub.

On the Pi, create this file:

```bash
mkdir -p .streamlit
nano .streamlit/secrets.toml
```

Add your key like this:

```toml
COMPANIES_HOUSE_API_KEY = "paste-your-real-api-key-here"
```

The `.streamlit/secrets.toml` file is ignored by Git so the key stays local to the Pi.

When `COMPANIES_HOUSE_API_KEY` is configured, the search screen uses the live Companies House `/search/companies` endpoint and lets the user add a returned company to the watchlist. If the key is missing or the API call fails, the app falls back to realistic sample UK company data.

## Included MVP Flow

- Search live Companies House company records by company name
- Choose a returned company and add it to a watchlist
- View company profile, director/officer details, PSC/control details, recent accounts filings, and filing documents
- Open Companies House filing documents in a new browser window
- Compare watched companies in a simple table
- Keep the UI bare bones so all text remains visible
