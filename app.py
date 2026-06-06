from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Positive Company Signals", page_icon="PCS", layout="wide")

COMPANIES: list[dict[str, Any]] = [
    {
        "number": "11223344",
        "name": "Northstar Renewables Limited",
        "status": "Active",
        "type": "Private limited Company",
        "incorporated": "12 Mar 2017",
        "sic": "35110 - Production of electricity",
        "address": "The Exchange, 2 St John Street, Manchester, M3 4AP",
        "region": "North West",
        "employees": 84,
        "glassdoor": 4.2,
        "next_accounts": "30 Sep 2026",
        "confirmation": "Due 18 Jul 2026",
        "risk": "Low",
        "summary": "Regional renewable energy operator showing steady asset growth and new hiring activity.",
        "financials": [
            {"year": 2021, "turnover": 820, "gross_profit": 176, "ebitda": 62, "cash": 84, "assets": 1240, "liabilities": 520, "net_assets": 720},
            {"year": 2022, "turnover": 1060, "gross_profit": 241, "ebitda": 88, "cash": 116, "assets": 1490, "liabilities": 590, "net_assets": 900},
            {"year": 2023, "turnover": 1390, "gross_profit": 327, "ebitda": 128, "cash": 138, "assets": 1840, "liabilities": 690, "net_assets": 1150},
            {"year": 2024, "turnover": 1710, "gross_profit": 402, "ebitda": 164, "cash": 172, "assets": 2260, "liabilities": 820, "net_assets": 1440},
        ],
        "directors": ["Amelia Price", "Kieran Walsh", "Meera Shah"],
        "shareholders": ["Price Family Holdings 42%", "Greenline Ventures LLP 28%", "Employee option pool 9%"],
        "filings": [("28 May 2026", "Accounts", "Full accounts made up to 30 September 2025", "Info"), ("11 May 2026", "Officer", "Appointment of Meera Shah as director", "Change"), ("02 Apr 2026", "Charge", "New fixed and floating charge registered", "Watch")],
        "signals": [("Company website", "05 Jun 2026", "New battery storage project approved in Cheshire", "Planning consent adds 35MW capacity to the development pipeline.", "https://example.com/northstar-project"), ("LinkedIn", "03 Jun 2026", "Hiring for commercial finance lead", "Finance hiring suggests scaling commercial operations.", "https://www.linkedin.com/"), ("X", "31 May 2026", "Industry event partnership announced", "Company is increasing market visibility in regional renewables.", "https://x.com/")],
        "alerts": [("06 Jun 2026", "Director appointment detected", "Companies House", "Unread"), ("06 Jun 2026", "New news item matched relevance threshold", "News", "Unread")],
    },
    {
        "number": "09876543",
        "name": "Harbour Analytics Group Ltd",
        "status": "Active",
        "type": "Private limited Company",
        "incorporated": "04 Oct 2015",
        "sic": "62020 - Information technology consultancy activities",
        "address": "18 Queen Square, Bristol, BS1 4NH",
        "region": "South West",
        "employees": 126,
        "glassdoor": 3.8,
        "next_accounts": "31 Dec 2026",
        "confirmation": "Due 06 Nov 2026",
        "risk": "Medium",
        "summary": "Data consultancy with strong revenue growth and a recent change in borrowing profile.",
        "financials": [
            {"year": 2021, "turnover": 980, "gross_profit": 392, "ebitda": 82, "cash": 96, "assets": 710, "liabilities": 310, "net_assets": 400},
            {"year": 2022, "turnover": 1240, "gross_profit": 494, "ebitda": 118, "cash": 132, "assets": 860, "liabilities": 390, "net_assets": 470},
            {"year": 2023, "turnover": 1560, "gross_profit": 612, "ebitda": 151, "cash": 120, "assets": 1040, "liabilities": 520, "net_assets": 520},
            {"year": 2024, "turnover": 2010, "gross_profit": 796, "ebitda": 226, "cash": 188, "assets": 1290, "liabilities": 610, "net_assets": 680},
        ],
        "directors": ["Oliver Grant", "Sofia Bennett"],
        "shareholders": ["Grant Bennett Partners 61%", "Southgate Growth Fund 24%"],
        "filings": [("01 Jun 2026", "Charge", "Satisfaction of charge registered", "Change"), ("19 Apr 2026", "Confirmation", "Confirmation statement with updates", "Info")],
        "signals": [("Company website", "04 Jun 2026", "Launch of public-sector analytics practice", "New service line may expand addressable market.", "https://example.com/harbour-public-sector"), ("Glassdoor", "30 May 2026", "Employee review trend improving", "Recent reviews mention better project staffing and clearer promotion paths.", "https://www.glassdoor.co.uk/")],
        "alerts": [("06 Jun 2026", "Charge satisfaction registered", "Companies House", "Unread")],
    },
    {
        "number": "06781234",
        "name": "Cobalt Care Services Ltd",
        "status": "Active",
        "type": "Private limited Company",
        "incorporated": "22 Jan 2010",
        "sic": "87900 - Other residential care activities",
        "address": "Mill House, Station Road, Leeds, LS18 5NT",
        "region": "Yorkshire and the Humber",
        "employees": 244,
        "glassdoor": 3.5,
        "next_accounts": "31 Jan 2027",
        "confirmation": "Due 28 Feb 2027",
        "risk": "Medium",
        "summary": "Care operator with stable assets, margin pressure, and increased social activity around recruitment.",
        "financials": [
            {"year": 2021, "turnover": 2550, "gross_profit": 702, "ebitda": 184, "cash": 210, "assets": 2210, "liabilities": 1180, "net_assets": 1030},
            {"year": 2022, "turnover": 2720, "gross_profit": 694, "ebitda": 159, "cash": 174, "assets": 2290, "liabilities": 1260, "net_assets": 1030},
            {"year": 2023, "turnover": 2910, "gross_profit": 716, "ebitda": 143, "cash": 141, "assets": 2360, "liabilities": 1320, "net_assets": 1040},
            {"year": 2024, "turnover": 3150, "gross_profit": 781, "ebitda": 168, "cash": 156, "assets": 2440, "liabilities": 1360, "net_assets": 1080},
        ],
        "directors": ["Daniel Moore", "Priya Nair"],
        "shareholders": ["Cobalt Holdings Ltd 88%", "Priya Nair 6%"],
        "filings": [("20 May 2026", "Accounts", "Accounts filed with lower EBITDA margin", "Watch"), ("14 Mar 2026", "PSC", "No individual PSC changes", "Info")],
        "signals": [("LinkedIn", "02 Jun 2026", "Recruitment campaign for senior carers", "High hiring activity across Leeds and Wakefield locations.", "https://www.linkedin.com/"), ("X", "25 May 2026", "Local authority contract mentioned", "Relevant procurement signal, still unconfirmed by official records.", "https://x.com/")],
        "alerts": [("06 Jun 2026", "Accounts filed with margin movement", "Financial", "Read")],
    },
    {
        "number": "12121212",
        "name": "Keystone Components PLC",
        "status": "Active",
        "type": "Public limited Company",
        "incorporated": "19 Aug 2008",
        "sic": "29320 - Manufacture of other parts for motor vehicles",
        "address": "Forge Lane Industrial Estate, Coventry, CV6 5AB",
        "region": "West Midlands",
        "employees": 392,
        "glassdoor": 3.2,
        "next_accounts": "30 Jun 2026",
        "confirmation": "Due 21 Sep 2026",
        "risk": "High",
        "summary": "Manufacturing business with higher leverage and fresh customer concentration signals.",
        "financials": [
            {"year": 2021, "turnover": 5100, "gross_profit": 1122, "ebitda": 416, "cash": 310, "assets": 4220, "liabilities": 2810, "net_assets": 1410},
            {"year": 2022, "turnover": 5480, "gross_profit": 1094, "ebitda": 358, "cash": 260, "assets": 4360, "liabilities": 3020, "net_assets": 1340},
            {"year": 2023, "turnover": 5710, "gross_profit": 1038, "ebitda": 291, "cash": 205, "assets": 4480, "liabilities": 3240, "net_assets": 1240},
            {"year": 2024, "turnover": 6040, "gross_profit": 1126, "ebitda": 336, "cash": 232, "assets": 4620, "liabilities": 3330, "net_assets": 1290},
        ],
        "directors": ["Rachel Evans", "Martin Hughes", "Lucy Chen"],
        "shareholders": ["Keystone Employee Trust 31%", "Alderbank Capital 22%", "Public float 47%"],
        "filings": [("03 Jun 2026", "Officer", "Resignation of Martin Hughes as director effective 30 June", "Change"), ("12 May 2026", "Accounts", "Accounts overdue warning within 30 days", "Alert")],
        "signals": [("News", "05 Jun 2026", "Supplier dispute reported by trade press", "Potential working-capital pressure and customer delivery risk.", "https://example.com/keystone-supplier-dispute"), ("Glassdoor", "29 May 2026", "Review trend mentions overtime and plant utilisation", "Employee sentiment points to operational strain.", "https://www.glassdoor.co.uk/")],
        "alerts": [("06 Jun 2026", "Accounts deadline risk approaching", "Companies House", "Unread"), ("06 Jun 2026", "Trade press article matched high relevance", "News", "Unread")],
    },
]


def add_style() -> None:
    st.markdown("""
    <style>
    .stApp { background: #f6f8fb; color: #102033; }
    section[data-testid="stSidebar"] { background: #fff; border-right: 1px solid #d9e2ec; }
    div[data-testid="stMetric"], .pcs-card, .pcs-header { background: #fff; border: 1px solid #d9e2ec; border-radius: 8px; }
    div[data-testid="stMetric"] { padding: 12px 14px; min-height: 108px; }
    .pcs-header { padding: 18px 20px; margin-bottom: 14px; }
    .pcs-title { font-size: 30px; font-weight: 700; margin: 0 0 4px 0; letter-spacing: 0; }
    .pcs-subtitle, .pcs-muted { color: #5f6f82; }
    .pcs-subtitle { margin: 0; font-size: 14px; }
    .pcs-card { padding: 16px; margin-bottom: 14px; }
    .pcs-section-title { font-size: 18px; font-weight: 700; margin: 0 0 10px 0; }
    .pcs-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; }
    .pcs-fact { border-bottom: 1px solid #edf2f7; padding: 9px 0; }
    .pcs-label { color: #5f6f82; font-size: 12px; text-transform: uppercase; letter-spacing: .02em; }
    .pcs-value { font-size: 15px; font-weight: 650; margin-top: 2px; overflow-wrap: anywhere; }
    .pcs-chip { display: inline-flex; border-radius: 999px; padding: 3px 9px; font-size: 12px; font-weight: 700; border: 1px solid #d9e2ec; margin-right: 6px; }
    .pcs-chip.info { background: #eef6ff; border-color: #bddcff; color: #004b87; }
    .pcs-chip.change { background: #ecfdf5; border-color: #a7f3d0; color: #047857; }
    .pcs-chip.watch { background: #fffbeb; border-color: #fde68a; color: #92400e; }
    .pcs-chip.alert { background: #fef2f2; border-color: #fecaca; color: #b91c1c; }
    .pcs-item { border-top: 1px solid #edf2f7; padding: 11px 0; }
    .pcs-item:first-of-type { border-top: 0; padding-top: 0; }
    .pcs-item-title { font-weight: 700; margin-bottom: 2px; }
    .pcs-muted { font-size: 13px; }
    .stButton > button { min-height: 42px; white-space: normal; text-align: center; line-height: 1.2; padding: 8px 12px; }
    div[role="radiogroup"] label, div[data-baseweb="select"] { white-space: normal; }
    a { color: #0065b3 !important; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)


def header(title: str, subtitle: str) -> None:
    st.markdown(f'<div class="pcs-header"><div class="pcs-title">{title}</div><p class="pcs-subtitle">{subtitle}</p></div>', unsafe_allow_html=True)


def open_card(title: str) -> None:
    st.markdown(f'<div class="pcs-card"><div class="pcs-section-title">{title}</div>', unsafe_allow_html=True)


def close_card() -> None:
    st.markdown('</div>', unsafe_allow_html=True)


def facts(items: list[tuple[str, str]]) -> None:
    html = '<div class="pcs-grid">'
    for label, value in items:
        html += f'<div class="pcs-fact"><div class="pcs-label">{label}</div><div class="pcs-value">{value}</div></div>'
    st.markdown(html + '</div>', unsafe_allow_html=True)


def item_line(chip: str, chip_class: str, meta: str, title: str, body: str = '') -> None:
    st.markdown(f'<div class="pcs-item"><span class="pcs-chip {chip_class}">{chip}</span><span class="pcs-muted">{meta}</span><div class="pcs-item-title">{title}</div><div class="pcs-muted">{body}</div></div>', unsafe_allow_html=True)


def css_class(value: str) -> str:
    return {"Low": "info", "Medium": "watch", "High": "alert", "Info": "info", "Change": "change", "Watch": "watch", "Alert": "alert", "Unread": "change", "Read": "info"}.get(value, "info")


def money(value: float) -> str:
    return f"GBP {value:,.0f}k"


def company_by_name(name: str) -> dict[str, Any]:
    return next(company for company in COMPANIES if company["name"] == name)


def company_by_number(number: str) -> dict[str, Any]:
    return next(company for company in COMPANIES if company["number"] == number)


def financials(company: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(company["financials"]).set_index("year")


def init_watchlist() -> None:
    st.session_state.setdefault("watchlist", [COMPANIES[0]["number"], COMPANIES[1]["number"]])


def watched_companies() -> list[dict[str, Any]]:
    init_watchlist()
    return [company_by_number(number) for number in st.session_state.watchlist]


def search_companies(query: str) -> list[dict[str, Any]]:
    cleaned = query.strip().lower()
    if not cleaned:
        return []
    return [company for company in COMPANIES if cleaned in company["name"].lower() or cleaned in company["number"] or cleaned in company["sic"].lower() or cleaned in company["region"].lower()]


def add_to_watchlist(number: str) -> None:
    init_watchlist()
    if number not in st.session_state.watchlist:
        st.session_state.watchlist.append(number)


def remove_from_watchlist(number: str) -> None:
    init_watchlist()
    st.session_state.watchlist = [item for item in st.session_state.watchlist if item != number]


def watchlist() -> None:
    init_watchlist()
    header("Positive Company Signals", "Search Companies House by company name, add the right business to your watchlist, then monitor changes.")
    watched = watched_companies()
    unread = sum(1 for company in watched for alert in company["alerts"] if alert[3] == "Unread")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Watchlist companies", len(watched))
    c2.metric("Unread alerts", unread)
    c3.metric("Last Saturday check", "6 Jun 2026")
    c4.metric("Search source", "Companies House")

    query = st.text_input("Search Companies House by company name", placeholder="Example: Northstar, Harbour, Cobalt, Keystone")
    results = search_companies(query)

    open_card("Companies House search results")
    if not query.strip():
        st.info("Enter a company name to search Companies House sample records.")
    elif not results:
        st.warning("No matching Companies House records found in the sample data.")
    for company in results:
        latest = financials(company).iloc[-1]
        item_line(css_class(company["risk"]).title(), css_class(company["risk"]), f'{company["number"]} - {company["region"]}', company["name"], f'{company["type"]} - {company["sic"]}<br>Turnover {money(latest["turnover"])} - Net assets {money(latest["net_assets"])}')
        already_watched = company["number"] in st.session_state.watchlist
        label = "Already in watchlist" if already_watched else "Add company to watchlist"
        if st.button(label, key=f'add_{company["number"]}', disabled=already_watched, use_container_width=True):
            add_to_watchlist(company["number"])
            st.success(f'{company["name"]} added to your watchlist.')
            st.rerun()
    close_card()

    list_view = st.selectbox("Watchlist view", ["All watched companies", "Competitors", "Acquisition targets", "M&A prospects"])
    open_card("Your watchlist")
    if not watched:
        st.info("Your watchlist is empty. Search Companies House above and add a company.")
    for company in watched:
        latest = financials(company).iloc[-1]
        left, right = st.columns([4, 1])
        with left:
            item_line(f'{company["risk"]} risk', css_class(company["risk"]), f'{company["number"]} - {list_view}', company["name"], f'{company["summary"]}<br>Turnover {money(latest["turnover"])} - Net assets {money(latest["net_assets"])} - Glassdoor {company["glassdoor"]}/5')
        with right:
            if st.button("Remove", key=f'remove_{company["number"]}', use_container_width=True):
                remove_from_watchlist(company["number"])
                st.rerun()
    close_card()


def overview() -> None:
    companies = watched_companies() or COMPANIES
    company = company_by_name(st.selectbox("Company", [company["name"] for company in companies]))
    df = financials(company)
    latest, previous = df.iloc[-1], df.iloc[-2]
    header(company["name"], company["summary"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Turnover", money(latest["turnover"]), f'{latest["turnover"] - previous["turnover"]:,.0f}k')
    c2.metric("EBITDA", money(latest["ebitda"]), f'{latest["ebitda"] - previous["ebitda"]:,.0f}k')
    c3.metric("Net assets", money(latest["net_assets"]), f'{latest["net_assets"] - previous["net_assets"]:,.0f}k')
    c4.metric("Glassdoor", f'{company["glassdoor"]}/5', f'{company["employees"]} employees')
    left, right = st.columns([1.08, 0.92])
    with left:
        open_card("Company record")
        facts([("Company number", company["number"]), ("Status", company["status"]), ("Company type", company["type"]), ("Incorporated", company["incorporated"]), ("SIC code", company["sic"]), ("Registered office", company["address"]), ("Next accounts", company["next_accounts"]), ("Confirmation statement", company["confirmation"])])
        close_card()
        open_card("Financial trend")
        st.line_chart(df[["assets", "liabilities", "net_assets"]].rename(columns={"assets": "Total assets", "liabilities": "Total liabilities", "net_assets": "Net assets"}), color=["#14b8a6", "#5aa9e6", "#172033"], height=310)
        st.caption("Values shown in GBP thousands from filed accounts sample data.")
        close_card()
    with right:
        open_card("Recent filings and status changes")
        for filing_date, filing_type, detail, severity in company["filings"]:
            item_line(severity, css_class(severity), f"{filing_date} - {filing_type}", detail)
        close_card()
        open_card("Directors and shareholders")
        facts([("Current directors", ", ".join(company["directors"])), ("Shareholders", "; ".join(company["shareholders"]))])
        close_card()
    open_card("News, social and employer signals")
    for source, signal_date, title, summary, url in company["signals"]:
        item_line(source, "info", signal_date, title, f'{summary} <a href="{url}" target="_blank">Open source</a>')
    close_card()


def compare() -> None:
    companies = watched_companies() or COMPANIES
    header("Compare companies", "Compare up to four watched UK companies across financials, balance sheet movement, filings, and content signals.")
    default = [company["name"] for company in companies[: min(3, len(companies))]]
    selected = st.multiselect("Companies", [company["name"] for company in companies], default=default, max_selections=4)
    if not selected:
        st.warning("Choose at least one company to compare.")
        return
    rows = []
    for name in selected:
        company = company_by_name(name)
        latest = financials(company).iloc[-1]
        rows.append({"Company": name, "Risk": company["risk"], "Turnover": latest["turnover"], "Gross profit": latest["gross_profit"], "EBITDA": latest["ebitda"], "Cash": latest["cash"], "Total assets": latest["assets"], "Total liabilities": latest["liabilities"], "Net assets": latest["net_assets"], "Unread alerts": sum(1 for alert in company["alerts"] if alert[3] == "Unread"), "Recent signals": len(company["signals"])})
    table = pd.DataFrame(rows).set_index("Company")
    open_card("Financial comparison")
    st.dataframe(table, use_container_width=True)
    close_card()
    open_card("Turnover and EBITDA")
    st.bar_chart(table[["Turnover", "EBITDA"]], color=["#0065b3", "#14b8a6"], height=320)
    close_card()


def alerts() -> None:
    companies = watched_companies() or COMPANIES
    header("Alerts", "In-app notifications from the Saturday monitoring cycle, plus a weekly email preview.")
    rows = [{"Company": company["name"], "date": alert[0], "message": alert[1], "type": alert[2], "status": alert[3]} for company in companies for alert in company["alerts"]]
    unread = [row for row in rows if row["status"] == "Unread"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Unread", len(unread))
    c2.metric("Companies changed", len({row["Company"] for row in rows}))
    c3.metric("Weekly email", "Monday 08:00")
    left, right = st.columns([1.1, 0.9])
    with left:
        open_card("Alert feed")
        for row in rows:
            item_line(row["status"], css_class(row["status"]), f'{row["date"]} - {row["type"]}', f'{row["Company"]}: {row["message"]}')
        close_card()
    with right:
        open_card("Weekly email preview")
        st.markdown(f'**Subject:** {len(unread)} company signal updates are ready')
        st.write("Your tracked UK companies were checked on Saturday 6 June 2026. Open your account to review filings, news, social posts, and employer signals.")
        for row in unread[:5]:
            st.markdown(f'- **{row["Company"]}**: {row["message"]}')
        close_card()


def settings() -> None:
    header("Monitoring settings", "Configure the relevance layer, alert types, and future live integrations.")
    left, right = st.columns(2)
    with left:
        open_card("Alert rules")
        st.toggle("Companies House changes", value=True)
        st.toggle("News stories", value=True)
        st.toggle("LinkedIn and X mentions", value=True)
        st.toggle("Glassdoor employer movement", value=True)
        st.slider("News relevance threshold", 0, 100, 68)
        st.selectbox("Saturday check time", ["06:00", "08:00", "10:00"], index=1)
        close_card()
    with right:
        open_card("Integration readiness")
        facts([("Companies House", "Public API adapter ready"), ("News", "Provider pending licensing"), ("LinkedIn / X", "Approved API provider required"), ("Glassdoor", "Provider and compliance review required"), ("Authentication", "Streamlit prototype mode")])
        close_card()


def main() -> None:
    add_style()
    st.session_state.setdefault("run_date", date(2026, 6, 6))
    with st.sidebar:
        st.title("Positive")
        st.caption("Company Signals")
        page = st.radio("Navigate", ["Watchlist", "Company overview", "Compare", "Alerts", "Settings"], label_visibility="collapsed")
        st.divider()
        st.caption("Saturday monitor")
        st.write("Last checked: 6 Jun 2026")
        st.write("Next check: 13 Jun 2026")
        st.divider()
        st.caption("UK-first MVP")
    {"Watchlist": watchlist, "Company overview": overview, "Compare": compare, "Alerts": alerts, "Settings": settings}[page]()


if __name__ == "__main__":
    main()
