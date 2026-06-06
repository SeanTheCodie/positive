from __future__ import annotations

from datetime import date
import os
from typing import Any

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Positive Company Signals", page_icon="PCS", layout="centered")

COMPANIES: list[dict[str, Any]] = [
    {
        "number": "11223344",
        "name": "Northstar Renewables Limited",
        "status": "Active",
        "type": "Private limited company",
        "incorporated": "12 Mar 2017",
        "sic": "35110 - Production of electricity",
        "address": "The Exchange, 2 St John Street, Manchester, M3 4AP",
        "risk": "Low",
        "employees": 84,
        "glassdoor": 4.2,
        "summary": "Regional renewable energy operator showing steady asset growth and new hiring activity.",
        "financials": [
            {"year": 2021, "turnover": 820, "gross_profit": 176, "ebitda": 62, "cash": 84, "assets": 1240, "liabilities": 520, "net_assets": 720},
            {"year": 2022, "turnover": 1060, "gross_profit": 241, "ebitda": 88, "cash": 116, "assets": 1490, "liabilities": 590, "net_assets": 900},
            {"year": 2023, "turnover": 1390, "gross_profit": 327, "ebitda": 128, "cash": 138, "assets": 1840, "liabilities": 690, "net_assets": 1150},
            {"year": 2024, "turnover": 1710, "gross_profit": 402, "ebitda": 164, "cash": 172, "assets": 2260, "liabilities": 820, "net_assets": 1440},
        ],
        "directors": ["Amelia Price", "Kieran Walsh", "Meera Shah"],
        "shareholders": ["Price Family Holdings 42%", "Greenline Ventures LLP 28%", "Employee option pool 9%"],
        "filings": ["28 May 2026: Full accounts filed", "11 May 2026: Appointment of Meera Shah as director", "02 Apr 2026: New fixed and floating charge registered"],
        "signals": ["Company website: New battery storage project approved in Cheshire", "LinkedIn: Hiring for commercial finance lead", "X: Industry event partnership announced"],
        "alerts": ["Director appointment detected", "New news item matched relevance threshold"],
    },
    {
        "number": "09876543",
        "name": "Harbour Analytics Group Ltd",
        "status": "Active",
        "type": "Private limited company",
        "incorporated": "04 Oct 2015",
        "sic": "62020 - Information technology consultancy activities",
        "address": "18 Queen Square, Bristol, BS1 4NH",
        "risk": "Medium",
        "employees": 126,
        "glassdoor": 3.8,
        "summary": "Data consultancy with strong revenue growth and a recent change in borrowing profile.",
        "financials": [
            {"year": 2021, "turnover": 980, "gross_profit": 392, "ebitda": 82, "cash": 96, "assets": 710, "liabilities": 310, "net_assets": 400},
            {"year": 2022, "turnover": 1240, "gross_profit": 494, "ebitda": 118, "cash": 132, "assets": 860, "liabilities": 390, "net_assets": 470},
            {"year": 2023, "turnover": 1560, "gross_profit": 612, "ebitda": 151, "cash": 120, "assets": 1040, "liabilities": 520, "net_assets": 520},
            {"year": 2024, "turnover": 2010, "gross_profit": 796, "ebitda": 226, "cash": 188, "assets": 1290, "liabilities": 610, "net_assets": 680},
        ],
        "directors": ["Oliver Grant", "Sofia Bennett"],
        "shareholders": ["Grant Bennett Partners 61%", "Southgate Growth Fund 24%"],
        "filings": ["01 Jun 2026: Satisfaction of charge registered", "19 Apr 2026: Confirmation statement with updates"],
        "signals": ["Company website: Launch of public-sector analytics practice", "Glassdoor: Employee review trend improving"],
        "alerts": ["Charge satisfaction registered"],
    },
    {
        "number": "06781234",
        "name": "Cobalt Care Services Ltd",
        "status": "Active",
        "type": "Private limited company",
        "incorporated": "22 Jan 2010",
        "sic": "87900 - Other residential care activities",
        "address": "Mill House, Station Road, Leeds, LS18 5NT",
        "risk": "Medium",
        "employees": 244,
        "glassdoor": 3.5,
        "summary": "Care operator with stable assets, margin pressure, and increased social activity around recruitment.",
        "financials": [
            {"year": 2021, "turnover": 2550, "gross_profit": 702, "ebitda": 184, "cash": 210, "assets": 2210, "liabilities": 1180, "net_assets": 1030},
            {"year": 2022, "turnover": 2720, "gross_profit": 694, "ebitda": 159, "cash": 174, "assets": 2290, "liabilities": 1260, "net_assets": 1030},
            {"year": 2023, "turnover": 2910, "gross_profit": 716, "ebitda": 143, "cash": 141, "assets": 2360, "liabilities": 1320, "net_assets": 1040},
            {"year": 2024, "turnover": 3150, "gross_profit": 781, "ebitda": 168, "cash": 156, "assets": 2440, "liabilities": 1360, "net_assets": 1080},
        ],
        "directors": ["Daniel Moore", "Priya Nair"],
        "shareholders": ["Cobalt Holdings Ltd 88%", "Priya Nair 6%"],
        "filings": ["20 May 2026: Accounts filed with lower EBITDA margin", "14 Mar 2026: No individual PSC changes"],
        "signals": ["LinkedIn: Recruitment campaign for senior carers", "X: Local authority contract mentioned"],
        "alerts": ["Accounts filed with margin movement"],
    },
    {
        "number": "12121212",
        "name": "Keystone Components PLC",
        "status": "Active",
        "type": "Public limited company",
        "incorporated": "19 Aug 2008",
        "sic": "29320 - Manufacture of other parts for motor vehicles",
        "address": "Forge Lane Industrial Estate, Coventry, CV6 5AB",
        "risk": "High",
        "employees": 392,
        "glassdoor": 3.2,
        "summary": "Manufacturing business with higher leverage and fresh customer concentration signals.",
        "financials": [
            {"year": 2021, "turnover": 5100, "gross_profit": 1122, "ebitda": 416, "cash": 310, "assets": 4220, "liabilities": 2810, "net_assets": 1410},
            {"year": 2022, "turnover": 5480, "gross_profit": 1094, "ebitda": 358, "cash": 260, "assets": 4360, "liabilities": 3020, "net_assets": 1340},
            {"year": 2023, "turnover": 5710, "gross_profit": 1038, "ebitda": 291, "cash": 205, "assets": 4480, "liabilities": 3240, "net_assets": 1240},
            {"year": 2024, "turnover": 6040, "gross_profit": 1126, "ebitda": 336, "cash": 232, "assets": 4620, "liabilities": 3330, "net_assets": 1290},
        ],
        "directors": ["Rachel Evans", "Martin Hughes", "Lucy Chen"],
        "shareholders": ["Keystone Employee Trust 31%", "Alderbank Capital 22%", "Public float 47%"],
        "filings": ["03 Jun 2026: Director resignation effective 30 June", "12 May 2026: Accounts deadline risk approaching"],
        "signals": ["News: Supplier dispute reported by trade press", "Glassdoor: Reviews mention overtime and plant utilisation"],
        "alerts": ["Accounts deadline risk approaching", "Trade press article matched high relevance"],
    },
]


def init_state() -> None:
    st.session_state.setdefault("watchlist", [COMPANIES[0]["number"], COMPANIES[1]["number"]])


def companies_house_api_key() -> str:
    return "192c9ef2-ccf3-40f8-82b8-e7dcef5a5d5d"


def company_by_number(company_number: str) -> dict[str, Any]:
    return next(company for company in COMPANIES if company["number"] == company_number)


def company_by_name(company_name: str) -> dict[str, Any]:
    return next(company for company in COMPANIES if company["name"] == company_name)


def watched_companies() -> list[dict[str, Any]]:
    return [company_by_number(number) for number in st.session_state.watchlist]


def financial_frame(company: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(company["financials"]).set_index("year")


def money(value: float) -> str:
    return f"GBP {value:,.0f}k"


def search_companies(query: str) -> list[dict[str, Any]]:
    term = query.strip().lower()
    if not term:
        return []
    return [company for company in COMPANIES if term in company["name"].lower() or term in company["number"] or term in company["sic"].lower()]


def add_company(company_number: str) -> None:
    if company_number not in st.session_state.watchlist:
        st.session_state.watchlist.append(company_number)


def remove_company(company_number: str) -> None:
    st.session_state.watchlist = [number for number in st.session_state.watchlist if number != company_number]


def show_company_summary(company: dict[str, Any]) -> None:
    latest = financial_frame(company).iloc[-1]
    st.write(f"**{company['name']}**")
    st.write(f"Company number: {company['number']}")
    st.write(f"Status: {company['status']}")
    st.write(f"Type: {company['type']}")
    st.write(f"SIC: {company['sic']}")
    st.write(f"Risk: {company['risk']}")
    st.write(f"Turnover: {money(latest['turnover'])}")
    st.write(f"Net assets: {money(latest['net_assets'])}")


def page_watchlist() -> None:
    st.title("Positive Company Signals")
    st.write("Search Companies House by company name and add companies to your watchlist.")
    st.subheader("Search Companies House")
    query = st.text_input("Company name", placeholder="Try Northstar, Harbour, Cobalt, or Keystone")
    results = search_companies(query)
    if query and not results:
        st.warning("No matching sample company records found.")
    for company in results:
        with st.container(border=True):
            show_company_summary(company)
            already_watched = company["number"] in st.session_state.watchlist
            if already_watched:
                st.button("Already in watchlist", disabled=True, use_container_width=True)
            elif st.button("Add company to watchlist", key=f"add-{company['number']}", use_container_width=True):
                add_company(company["number"])
                st.success(f"Added {company['name']} to the watchlist.")
                st.rerun()
    st.divider()
    st.subheader("Your watchlist")
    watched = watched_companies()
    if not watched:
        st.info("Your watchlist is empty.")
    for company in watched:
        with st.container(border=True):
            show_company_summary(company)
            if st.button("Remove from watchlist", key=f"remove-{company['number']}", use_container_width=True):
                remove_company(company["number"])
                st.rerun()


def page_company() -> None:
    watched = watched_companies()
    if not watched:
        st.warning("Add a company to your watchlist first.")
        return
    selected_name = st.selectbox("Choose a watched company", [company["name"] for company in watched])
    company = company_by_name(selected_name)
    latest = financial_frame(company).iloc[-1]
    st.title(company["name"])
    st.write(company["summary"])
    st.subheader("Company record")
    st.write(f"Company number: {company['number']}")
    st.write(f"Status: {company['status']}")
    st.write(f"Type: {company['type']}")
    st.write(f"Incorporated: {company['incorporated']}")
    st.write(f"SIC: {company['sic']}")
    st.write(f"Registered office: {company['address']}")
    st.subheader("Latest financials")
    for label in ["turnover", "gross_profit", "ebitda", "cash", "assets", "liabilities", "net_assets"]:
        st.write(f"{label.replace('_', ' ').title()}: {money(latest[label])}")
    st.subheader("Financial trend")
    st.line_chart(financial_frame(company)[["assets", "liabilities", "net_assets"]])
    st.subheader("Directors")
    for director in company["directors"]:
        st.write(f"- {director}")
    st.subheader("Shareholders")
    for shareholder in company["shareholders"]:
        st.write(f"- {shareholder}")
    st.subheader("Recent filings")
    for filing in company["filings"]:
        st.write(f"- {filing}")
    st.subheader("News and social signals")
    for signal in company["signals"]:
        st.write(f"- {signal}")


def page_alerts() -> None:
    st.title("Alerts")
    watched = watched_companies()
    if not watched:
        st.info("No companies are currently watched.")
        return
    st.write("Last checked: Saturday 6 June 2026")
    st.write("Next check: Saturday 13 June 2026")
    for company in watched:
        st.subheader(company["name"])
        for alert in company["alerts"] or ["No alerts."]:
            st.write(f"- {alert}")


def page_compare() -> None:
    st.title("Compare watched companies")
    watched = watched_companies()
    if len(watched) < 2:
        st.warning("Add at least two companies to compare.")
        return
    selected = st.multiselect("Choose up to four companies", [company["name"] for company in watched], default=[company["name"] for company in watched[: min(4, len(watched))]], max_selections=4)
    if not selected:
        st.info("Choose at least one company.")
        return
    rows = []
    for name in selected:
        company = company_by_name(name)
        latest = financial_frame(company).iloc[-1]
        rows.append({"Company": company["name"], "Risk": company["risk"], "Turnover": latest["turnover"], "Gross profit": latest["gross_profit"], "EBITDA": latest["ebitda"], "Cash": latest["cash"], "Assets": latest["assets"], "Liabilities": latest["liabilities"], "Net assets": latest["net_assets"]})
    st.dataframe(pd.DataFrame(rows), use_container_width=True)


def main() -> None:
    init_state()
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Go to", ["Search and watchlist", "Company details", "Alerts", "Compare"])
    st.sidebar.write("UK-first prototype")
    st.sidebar.write(f"Session date: {date(2026, 6, 6).strftime('%d %b %Y')}")
    if companies_house_api_key():
        st.sidebar.success("Companies House API key configured")
    else:
        st.sidebar.warning("Companies House API key not configured")
    if page == "Search and watchlist":
        page_watchlist()
    elif page == "Company details":
        page_company()
    elif page == "Alerts":
        page_alerts()
    else:
        page_compare()


if __name__ == "__main__":
    main()
