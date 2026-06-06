from __future__ import annotations

import base64
from datetime import date
import html
import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Positive Company Signals",
    page_icon="PCS",
    layout="centered",
)

COMPANIES_HOUSE_BASE_URL = "https://api.company-information.service.gov.uk"

SAMPLE_COMPANIES: list[dict[str, Any]] = [
    {
        "number": "11223344",
        "name": "Northstar Renewables Limited",
        "status": "Active",
        "type": "Private limited company",
        "incorporated": "12 Mar 2017",
        "sic": "35110 - Production of electricity",
        "address": "Manchester",
        "source": "Sample data",
    },
    {
        "number": "09876543",
        "name": "Harbour Analytics Group Ltd",
        "status": "Active",
        "type": "Private limited company",
        "incorporated": "04 Oct 2015",
        "sic": "62020 - Information technology consultancy activities",
        "address": "Bristol",
        "source": "Sample data",
    },
    {
        "number": "06781234",
        "name": "Cobalt Care Services Ltd",
        "status": "Active",
        "type": "Private limited company",
        "incorporated": "22 Jan 2010",
        "sic": "87900 - Other residential care activities",
        "address": "Leeds",
        "source": "Sample data",
    },
]


def init_state() -> None:
    st.session_state.setdefault("watchlist", [])
    st.session_state.setdefault("company_cache", {})
    st.session_state.setdefault("last_search_error", "")


def companies_house_api_key() -> str:
    return "192c9ef2-ccf3-40f8-82b8-e7dcef5a5d5d"

def companies_house_get(endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    api_key = companies_house_api_key()
    if not api_key:
        raise RuntimeError("Companies House API key is not configured.")

    query_string = f"?{urlencode(params)}" if params else ""
    url = f"{COMPANIES_HOUSE_BASE_URL}{endpoint}{query_string}"
    token = base64.b64encode(f"{api_key}:".encode("utf-8")).decode("ascii")
    request = Request(url, headers={"Authorization": f"Basic {token}"})

    try:
        with urlopen(request, timeout=12) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Companies House returned {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach Companies House: {exc.reason}") from exc


def normalise_search_result(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "number": item.get("company_number", ""),
        "name": item.get("title", "Unnamed company"),
        "status": item.get("company_status", "Unknown"),
        "type": item.get("company_type", "Unknown"),
        "incorporated": item.get("date_of_creation", "Unknown"),
        "sic": item.get("description", "SIC not shown in search result"),
        "address": item.get("address_snippet", "Address not shown in search result"),
        "source": "Companies House search",
    }


def normalise_profile(profile: dict[str, Any]) -> dict[str, Any]:
    address = profile.get("registered_office_address", {})
    address_text = ", ".join(str(value) for value in address.values() if value)
    sic_codes = profile.get("sic_codes", [])
    return {
        "number": profile.get("company_number", ""),
        "name": profile.get("company_name", "Unnamed company"),
        "status": profile.get("company_status", "Unknown"),
        "type": profile.get("type", "Unknown"),
        "incorporated": profile.get("date_of_creation", "Unknown"),
        "sic": ", ".join(sic_codes) if sic_codes else "No SIC codes returned",
        "address": address_text or "No registered office returned",
        "source": "Companies House profile",
    }


def format_address(address: dict[str, Any] | None) -> str:
    if not address:
        return "No address returned"
    fields = ["premises", "address_line_1", "address_line_2", "locality", "region", "postal_code", "country"]
    return ", ".join(str(address.get(field)) for field in fields if address.get(field))


def format_month_year(value: dict[str, Any] | None) -> str:
    if not value:
        return "Not shown"
    month = value.get("month")
    year = value.get("year")
    if month and year:
        return f"{int(month):02d}/{year}"
    return str(year or "Not shown")


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        year, month, day = value.split("-")
        return date(int(year), int(month), int(day))
    except ValueError:
        return None


def public_document_url(company_number: str, filing: dict[str, Any]) -> str:
    transaction_id = filing.get("transaction_id")
    if not transaction_id:
        return ""
    encoded_transaction_id = quote(str(transaction_id), safe="")
    return (
        "https://find-and-update.company-information.service.gov.uk"
        f"/company/{company_number}/filing-history/{encoded_transaction_id}"
        "/document?format=pdf&download=0"
    )


def fetch_officers(company_number: str) -> list[dict[str, Any]]:
    data = companies_house_get(f"/company/{company_number}/officers", {"items_per_page": 100})
    return data.get("items", [])


def fetch_pscs(company_number: str) -> list[dict[str, Any]]:
    data = companies_house_get(f"/company/{company_number}/persons-with-significant-control", {"items_per_page": 100})
    return data.get("items", [])


def fetch_filing_history(company_number: str) -> list[dict[str, Any]]:
    filings: list[dict[str, Any]] = []
    start_index = 0
    items_per_page = 100
    while start_index < 1000:
        data = companies_house_get(
            f"/company/{company_number}/filing-history",
            {"items_per_page": items_per_page, "start_index": start_index},
        )
        items = data.get("items", [])
        filings.extend(items)
        total_count = data.get("total_count", len(filings))
        if not items or len(filings) >= total_count:
            break
        start_index += items_per_page
    return filings


def filing_description(filing: dict[str, Any]) -> str:
    description = filing.get("description", "Document filed")
    values = filing.get("description_values", {})
    if values:
        parts = [f"{key}: {value}" for key, value in values.items()]
        return f"{description} ({', '.join(parts)})"
    return description


def accounts_filings_for_last_five_years(filings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    oldest_year = date.today().year - 5
    accounts = []
    for filing in filings:
        if filing.get("category") != "accounts":
            continue
        filing_date = parse_date(filing.get("date"))
        if filing_date and filing_date.year >= oldest_year:
            accounts.append(filing)
    return accounts


def search_companies(query: str) -> list[dict[str, Any]]:
    term = query.strip()
    st.session_state.last_search_error = ""
    if not term:
        return []

    if companies_house_api_key():
        try:
            data = companies_house_get("/search/companies", {"q": term, "items_per_page": 100})
            return [normalise_search_result(item) for item in data.get("items", []) if item.get("company_number")]
        except RuntimeError as exc:
            st.session_state.last_search_error = str(exc)

    lower_term = term.lower()
    return [
        company
        for company in SAMPLE_COMPANIES
        if lower_term in company["name"].lower()
        or lower_term in company["number"]
        or lower_term in company["sic"].lower()
    ]


def fetch_company(company_number: str) -> dict[str, Any]:
    if company_number in st.session_state.company_cache:
        return st.session_state.company_cache[company_number]

    for company in SAMPLE_COMPANIES:
        if company["number"] == company_number:
            st.session_state.company_cache[company_number] = company
            return company

    company = normalise_profile(companies_house_get(f"/company/{company_number}"))
    st.session_state.company_cache[company_number] = company
    return company


def watched_companies() -> list[dict[str, Any]]:
    companies = []
    for company_number in st.session_state.watchlist:
        try:
            companies.append(fetch_company(company_number))
        except RuntimeError:
            companies.append(
                {
                    "number": company_number,
                    "name": f"Company {company_number}",
                    "status": "Unable to load",
                    "type": "Unknown",
                    "incorporated": "Unknown",
                    "sic": "Unknown",
                    "address": "Unable to load from Companies House",
                    "source": "Watchlist",
                }
            )
    return companies


def add_to_watchlist(company: dict[str, Any]) -> None:
    company_number = company["number"]
    st.session_state.company_cache[company_number] = company
    if company_number not in st.session_state.watchlist:
        st.session_state.watchlist.append(company_number)


def remove_from_watchlist(company_number: str) -> None:
    st.session_state.watchlist = [number for number in st.session_state.watchlist if number != company_number]


def show_company(company: dict[str, Any]) -> None:
    st.write(f"**{company['name']}**")
    st.write(f"Company number: {company['number']}")
    st.write(f"Status: {company['status']}")
    st.write(f"Type: {company['type']}")
    st.write(f"Incorporated: {company['incorporated']}")
    st.write(f"SIC: {company['sic']}")
    st.write(f"Address: {company['address']}")
    st.write(f"Source: {company['source']}")


def page_search() -> None:
    st.title("Positive Company Signals")
    st.write("Search Companies House by company name and add a company to your watchlist.")

    query = st.text_input("Company name", placeholder="Enter a company name or part of a name")
    results = search_companies(query)

    if st.session_state.last_search_error:
        st.error(st.session_state.last_search_error)
        st.info("Showing sample records instead.")

    if query and not results:
        st.warning("No matching companies found.")

    if results:
        st.subheader("Search results")

    for company in results:
        with st.container(border=True):
            show_company(company)
            already_watched = company["number"] in st.session_state.watchlist
            if already_watched:
                st.button("Already in watchlist", disabled=True, use_container_width=True)
            elif st.button("Add this company to watchlist", key=f"add-{company['number']}", use_container_width=True):
                add_to_watchlist(company)
                st.success(f"Added {company['name']} to the watchlist.")
                st.rerun()

    st.divider()
    st.subheader("Watchlist")
    companies = watched_companies()

    if not companies:
        st.info("No companies in the watchlist yet.")

    for company in companies:
        with st.container(border=True):
            show_company(company)
            if st.button("Remove from watchlist", key=f"remove-{company['number']}", use_container_width=True):
                remove_from_watchlist(company["number"])
                st.rerun()


def page_company_details() -> None:
    companies = watched_companies()
    if not companies:
        st.warning("Add a company to your watchlist first.")
        return

    company_names = [company["name"] for company in companies]
    selected_name = st.selectbox("Choose a company", company_names)
    selected = next(company for company in companies if company["name"] == selected_name)

    st.title(selected["name"])
    show_company(selected)

    if not companies_house_api_key():
        st.warning("Add a Companies House API key to load live details, officers, PSCs, and filings.")
        return

    if st.button("Refresh company profile from Companies House", use_container_width=True):
        refreshed = normalise_profile(companies_house_get(f"/company/{selected['number']}"))
        st.session_state.company_cache[selected["number"]] = refreshed
        st.rerun()

    try:
        officers = fetch_officers(selected["number"])
        pscs = fetch_pscs(selected["number"])
        filings = fetch_filing_history(selected["number"])
    except RuntimeError as exc:
        st.error(str(exc))
        return

    st.subheader("Five years of financial filings")
    financial_filings = accounts_filings_for_last_five_years(filings)
    if not financial_filings:
        st.write("No accounts filings found in the last five years.")
    for filing in financial_filings:
        st.write(f"Date submitted: {filing.get('date', 'Unknown')}")
        st.write(f"Type: {filing.get('type', 'Unknown')}")
        st.write(f"Description: {filing_description(filing)}")
        url = public_document_url(selected["number"], filing)
        if url:
            st.markdown(f'<a href="{html.escape(url)}" target="_blank">Open accounts document in new window</a>', unsafe_allow_html=True)
        st.divider()

    st.subheader("Director and officer details")
    if not officers:
        st.write("No officers returned.")
    for officer in officers:
        st.write(f"Name: {officer.get('name', 'Unknown')}")
        st.write(f"Role: {officer.get('officer_role', 'Unknown')}")
        st.write(f"Appointed: {officer.get('appointed_on', 'Unknown')}")
        st.write(f"Resigned: {officer.get('resigned_on', 'Current')}")
        st.write(f"Occupation: {officer.get('occupation', 'Not shown')}")
        st.write(f"Nationality: {officer.get('nationality', 'Not shown')}")
        st.write(f"Country of residence: {officer.get('country_of_residence', 'Not shown')}")
        st.write(f"Date of birth: {format_month_year(officer.get('date_of_birth'))}")
        st.write(f"Address: {format_address(officer.get('address'))}")
        st.divider()

    st.subheader("Shareholder and control details")
    st.write("Companies House public data shows PSC/control information rather than a full shareholder register.")
    if not pscs:
        st.write("No persons with significant control returned.")
    for psc in pscs:
        st.write(f"Name: {psc.get('name', 'Unknown')}")
        st.write(f"Kind: {psc.get('kind', 'Unknown')}")
        st.write(f"Notified: {psc.get('notified_on', 'Unknown')}")
        st.write(f"Ceased: {psc.get('ceased_on', 'Current')}")
        st.write(f"Country of residence: {psc.get('country_of_residence', 'Not shown')}")
        st.write(f"Nationality: {psc.get('nationality', 'Not shown')}")
        st.write(f"Address: {format_address(psc.get('address'))}")
        natures = psc.get("natures_of_control", [])
        if natures:
            st.write("Nature of control:")
            for nature in natures:
                st.write(f"- {nature}")
        st.divider()

    st.subheader("All Companies House documents")
    if not filings:
        st.write("No filing history documents returned.")
    for filing in filings:
        st.write(f"Date submitted: {filing.get('date', 'Unknown')}")
        st.write(f"Type: {filing.get('type', 'Unknown')}")
        st.write(f"Category: {filing.get('category', 'Unknown')}")
        st.write(f"Description: {filing_description(filing)}")
        url = public_document_url(selected["number"], filing)
        if url:
            st.markdown(f'<a href="{html.escape(url)}" target="_blank">Open document in new window</a>', unsafe_allow_html=True)
        else:
            st.write("No public document link available for this filing.")
        st.divider()


def page_compare() -> None:
    st.title("Compare watchlist")
    companies = watched_companies()
    if not companies:
        st.info("No companies in the watchlist yet.")
        return

    rows = [
        {
            "Company": company["name"],
            "Number": company["number"],
            "Status": company["status"],
            "Type": company["type"],
            "Incorporated": company["incorporated"],
            "SIC": company["sic"],
        }
        for company in companies
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)


def page_alerts() -> None:
    st.title("Alerts")
    st.write("Company change alerts will be created from future Companies House snapshot comparisons.")
    st.write("Last checked: not yet run")


def main() -> None:
    init_state()

    st.sidebar.title("Menu")
    page = st.sidebar.radio("Go to", ["Search and watchlist", "Company details", "Compare", "Alerts"])
    st.sidebar.write("UK-first prototype")
    st.sidebar.write(f"Session date: {date.today().strftime('%d %b %Y')}")

    if companies_house_api_key():
        st.sidebar.success("Companies House API key configured")
    else:
        st.sidebar.warning("Companies House API key not configured")

    if page == "Search and watchlist":
        page_search()
    elif page == "Company details":
        page_company_details()
    elif page == "Compare":
        page_compare()
    else:
        page_alerts()


if __name__ == "__main__":
    main()
