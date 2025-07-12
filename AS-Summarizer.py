import streamlit as st
from fpdf import FPDF
import io

# ------------------------- Page Setup -------------------------
st.set_page_config(page_title="AS Summarizer for CA Students")
st.title("📘 Accounting Standards (AS) Summarizer")
st.markdown("Get quick summaries of ICAI Accounting Standards (AS). Ask questions like 'Summarize AS 10' or 'Explain AS 12 with example'.")

# ------------------------- AS Summary Database -------------------------
as_data = {
    "AS 1": "AS 1: Disclosure of Accounting Policies\nDeals with disclosure of significant accounting policies such as going concern, consistency, and accrual. These must be disclosed clearly in financial statements.",
    "AS 2": "AS 2: Valuation of Inventories\nCovers methods for valuing inventory (FIFO, Weighted Average) and mandates inventory should be valued at lower of cost or net realizable value.",
    "AS 3": "AS 3: Cash Flow Statements\nRequires classification of cash flows into Operating, Investing, and Financing activities for better understanding of cash movement.",
    "AS 4": "AS 4: Contingencies and Events Occurring After the Balance Sheet Date\nDeals with treatment of contingencies and events (adjusting/non-adjusting) after the balance sheet date but before approval.",
    "AS 5": "AS 5: Net Profit or Loss for the Period, Prior Period Items and Changes in Accounting Policies\nSpecifies how to report unusual items, changes in policies, and prior period adjustments in the financial statements.",
    "AS 6": "AS 6: (Withdrawn and merged with AS 10)",
    "AS 7": "AS 7: Construction Contracts\nPrescribes the method of accounting (percentage of completion) and revenue recognition for construction contract work.",
    "AS 8": "AS 8: (Withdrawn and replaced by AS 26)",
    "AS 9": "AS 9: Revenue Recognition\nSpecifies when revenue should be recognized from sale of goods, services, interest, royalties, and dividends.",
    "AS 10": "AS 10: Property, Plant and Equipment\nCovers recognition, depreciation, revaluation, disposal of fixed assets.\nExample: Machinery purchased for ₹10 lakhs is capitalized and depreciated as per AS 10.",
    "AS 11": "AS 11: The Effects of Changes in Foreign Exchange Rates\nDeals with accounting for transactions in foreign currencies and translating financial statements of foreign operations.",
    "AS 12": "AS 12: Government Grants\nSpecifies how government assistance is treated in accounting.\nExample: A ₹2 lakh subsidy for plant purchase is either deferred income or deducted from asset cost.",
    "AS 13": "AS 13: Accounting for Investments\nCovers classification (current vs long-term), cost determination, and disposal of investments.",
    "AS 14": "AS 14: Accounting for Amalgamations\nOutlines pooling of interest and purchase method for amalgamations and treatment of goodwill/reserves.",
    "AS 15": "AS 15: Employee Benefits\nCovers accounting for short-term, post-employment, and other employee benefits like gratuity and leave encashment.",
    "AS 16": "AS 16: Borrowing Costs\nPrescribes capitalisation of borrowing costs directly attributable to acquisition/construction of qualifying assets.",
    "AS 17": "AS 17: Segment Reporting\nRequires disclosure of segment-wise revenue, expenses, and capital employed based on business/geographical segments.",
    "AS 18": "AS 18: Related Party Disclosures\nMandates disclosure of relationships, transactions, and balances with related parties.",
    "AS 19": "AS 19: Leases\nSpecifies accounting treatment for finance and operating leases by lessee and lessor.",
    "AS 20": "AS 20: Earnings Per Share\nDefines methods for calculating and disclosing basic and diluted earnings per share.",
    "AS 21": "AS 21: Consolidated Financial Statements\nCovers preparation of consolidated financial statements of parent and subsidiaries.",
    "AS 22": "AS 22: Accounting for Taxes on Income\nDeals with deferred tax asset/liability due to timing differences between accounting and tax income.",
    "AS 23": "AS 23: Accounting for Investments in Associates\nPrescribes equity method for accounting investments in associates in consolidated financials.",
    "AS 24": "AS 24: Discontinuing Operations\nSpecifies disclosures and presentation when a component of the enterprise is being discontinued.",
    "AS 25": "AS 25: Interim Financial Reporting\nCovers recognition, measurement, and disclosures in financial reports for interim periods.",
    "AS 26": "AS 26: Intangible Assets\nDeals with recognition and amortization of identifiable non-monetary assets without physical substance.",
    "AS 27": "AS 27: Financial Reporting of Interests in Joint Ventures\nPrescribes accounting and disclosures for joint ventures and venturer's share.",
    "AS 28": "AS 28: Impairment of Assets\nSpecifies procedures to ensure assets are not carried at more than their recoverable amount.",
    "AS 29": "AS 29: Provisions, Contingent Liabilities and Contingent Assets\nDefines recognition criteria and disclosures for provisions and contingencies."
}

# ------------------------- Search Function -------------------------
def fetch_as_summary(query):
    for code, summary in as_data.items():
        if code.lower() in query.lower():
            return code, summary
    return None, "⚠️ Sorry, I couldn't find a summary for that AS. Please check your query."

# ------------------------- UI -------------------------
st.subheader("🔍 Search or Select an Accounting Standard")
user_input = st.text_input("Type an AS query:", placeholder="e.g. Summarize AS 10 or Explain AS 2")
dropdown = st.selectbox("Or select from list:", ["Select an AS"] + list(as_data.keys()))

summary = ""
selected_as = ""

if st.button("🧠 Get Summary"):
    if user_input:
        selected_as, summary = fetch_as_summary(user_input)
    elif dropdown != "Select an AS":
        selected_as = dropdown
        summary = as_data.get(dropdown, "⚠️ No summary found.")
    else:
        summary = "⚠️ Please enter a query or select an AS."

    st.markdown("---")
    st.markdown(f"**{selected_as}**\n\n{summary}")

    # ------------------------- Download as PDF -------------------------
    if selected_as and summary and "⚠️" not in summary:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"{selected_as}\n\n{summary}")

        buffer = io.BytesIO()
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        buffer.write(pdf_bytes)

        st.download_button(
            label="📄 Download Summary as PDF",
            data=buffer.getvalue(),
            file_name=f"{selected_as.replace(':','').replace(' ','_')}_Summary.pdf",
            mime="application/pdf"
        )

# ------------------------- Footer -------------------------
st.markdown("---")
st.caption("Made for CA Students | Phase 1: AS Summarizer | 100% Free Version | Ind AS & Comparisons coming soon")
