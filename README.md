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

The app uses realistic sample UK company data so the Companies House search and watchlist flow works without API keys. The code is structured so live Companies House, news, social, and Glassdoor providers can be connected later.

## Included MVP Flow

- Search Companies House-style records by company name and add companies to a saved watchlist
- Company overview with Companies House-style facts, financials, filings, officers, shareholders, news, social, and Glassdoor signals
- In-app alerts for company record and content changes
- Four-company comparison across P&L, balance sheet, and recent activity
- Weekly email preview for the Saturday monitoring cycle
