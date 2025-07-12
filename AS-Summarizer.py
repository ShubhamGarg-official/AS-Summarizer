import streamlit as st
from fpdf import FPDF
import io

# ------------------------- Page Setup -------------------------
st.set_page_config(page_title="AS Summarizer for CA Students")
st.title("📘 Accounting Standards (AS) Summarizer")
st.markdown("Get quick summaries of ICAI Accounting Standards (AS). Ask questions like 'Summarize AS 10' or 'Explain AS 12 with example'.")

# ------------------------- AS Summary + Examples Database -------------------------
as_data = {
    "AS 1": {
        "summary": "AS 1: Disclosure of Accounting Policies\nDeals with disclosure of significant accounting policies such as going concern, consistency, and accrual. These must be disclosed clearly in financial statements.",
        "examples": [
            "A company using FIFO method for inventory must disclose it clearly in notes to accounts.",
            "If the entity changes depreciation method from WDV to SLM, it should disclose the change and impact.",
            "Going concern assumption must be disclosed, especially if there is uncertainty.",
            "Accrual basis of accounting must be declared if used as per AS 1."
        ]
    },
    "AS 2": {
        "summary": "AS 2: Valuation of Inventories\nCovers methods for valuing inventory (FIFO, Weighted Average) and mandates inventory should be valued at lower of cost or net realizable value.",
        "examples": [
            "If raw material cost is ₹100 and NRV is ₹90, inventory is valued at ₹90.",
            "A trader using FIFO method must consistently follow it and disclose the method.",
            "Finished goods damaged in warehouse are valued at NRV which may be below cost.",
            "A retailer reduces price of old stock — AS 2 requires valuing such items at reduced NRV."
        ]
    },
    "AS 3": {
        "summary": "AS 3: Cash Flow Statements\nRequires classification of cash flows into Operating, Investing, and Financing activities for better understanding of cash movement.",
        "examples": [
            "Cash received from sale of goods is Operating Activity.",
            "Purchase of machinery is Investing Activity.",
            "Issuing shares for cash is Financing Activity.",
            "Dividend paid is Financing Activity; dividend received is Investing Activity."
        ]
    },
    "AS 4": {
        "summary": "AS 4: Contingencies and Events Occurring After the Balance Sheet Date\nDeals with treatment of contingencies and events (adjusting/non-adjusting) after the balance sheet date but before approval.",
        "examples": [
            "Company declared dividend after balance sheet date but before approval — disclosed as non-adjusting event.",
            "Debtor went bankrupt after year-end — if conditions existed on balance sheet date, it’s an adjusting event.",
            "Court case settled after year-end — if it relates to pre-existing conditions, provisions must be adjusted.",
            "Fire damage after year-end — disclosed as non-adjusting if unrelated to existing conditions."
        ]
    },
    "AS 5": {
        "summary": "AS 5: Net Profit or Loss for the Period, Prior Period Items and Changes in Accounting Policies\nSpecifies how to report unusual items, changes in policies, and prior period adjustments in the financial statements.",
        "examples": [
            "Error found in previous year’s depreciation — treated as prior period item.",
            "Loss from flood shown as extraordinary item separately.",
            "Change in inventory valuation method disclosed and impact shown.",
            "Discontinued operation loss shown separately for clarity."
        ]
    },
    "AS 7": {
        "summary": "AS 7: Construction Contracts\nPrescribes the method of accounting (percentage of completion) and revenue recognition for construction contract work.",
        "examples": [
            "Builder recognizes revenue based on work certified and costs incurred.",
            "Escalation clause results in extra revenue — recorded when reasonably certain.",
            "Loss-making contract identified — full loss provided as per prudence.",
            "Advance received but no work done — revenue not recognized."
        ]
    },
    "AS 9": {
        "summary": "AS 9: Revenue Recognition\nSpecifies when revenue should be recognized from sale of goods, services, interest, royalties, and dividends.",
        "examples": [
            "Sale of goods recorded when risks and rewards are transferred.",
            "Revenue from AMC (Annual Maintenance Contract) spread over contract period.",
            "Royalty income recorded as per agreement terms.",
            "Interest income recognized on time basis, not on receipt basis."
        ]
    },
    "AS 10": {
        "summary": "AS 10: Property, Plant and Equipment\nCovers recognition, depreciation, revaluation, disposal of fixed assets.",
        "examples": [
            "Machinery bought for ₹10 lakhs with ₹50k installation is capitalized at ₹10.5 lakhs.",
            "Company revalues land — increase goes to revaluation reserve.",
            "Old machine sold at profit — gain shown in P&L.",
            "Trial run expenses before commercial production are capitalized."
        ]
    },
    "AS 11": {
        "summary": "AS 11: The Effects of Changes in Foreign Exchange Rates\nDeals with accounting for transactions in foreign currencies and translating financial statements of foreign operations.",
        "examples": [
            "USD invoice recorded at exchange rate on transaction date.",
            "Forex gain/loss on payment shown in P&L.",
            "Monetary items like loan revalued at closing rate.",
            "Branch accounts in US converted at appropriate rates for consolidation."
        ]
    },
    "AS 12": {
        "summary": "AS 12: Government Grants\nSpecifies how government assistance is treated in accounting.",
        "examples": [
            "Capital grant shown as deferred income or deducted from asset.",
            "Revenue grant shown in P&L to match related expense.",
            "Export incentive treated as revenue grant.",
            "Grant refund — asset or liability adjusted accordingly."
        ]
    },
    "AS 13": {
        "summary": "AS 13: Accounting for Investments\nCovers classification (current vs long-term), cost determination, and disposal of investments.",
        "examples": [
            "Investment held for <1 year treated as current.",
            "Long-term investment shown at cost unless permanently impaired.",
            "Interest received post-acquisition adjusted from cost if accrued pre-acquisition.",
            "Sale of investment — profit/loss shown in P&L."
        ]
    },
    "AS 14": {
        "summary": "AS 14: Accounting for Amalgamations\nOutlines pooling of interest and purchase method for amalgamations and treatment of goodwill/reserves.",
        "examples": [
            "Merger between two companies using pooling method — assets and liabilities combined at book values.",
            "Purchase method applied — difference treated as goodwill or capital reserve.",
            "Statutory reserves maintained post-amalgamation as required.",
            "Amalgamation expenses shown separately, not added to purchase consideration."
        ]
    },
    "AS 15": {
        "summary": "AS 15: Employee Benefits\nCovers accounting for short-term, post-employment, and other employee benefits like gratuity and leave encashment.",
        "examples": [
            "Provision for leave encashment made on accrual basis.",
            "Gratuity liability valued using actuarial method.",
            "Bonus provision made even if unpaid at year-end.",
            "Employer's PF contribution expensed as incurred."
        ]
    },
    "AS 16": {
        "summary": "AS 16: Borrowing Costs\nPrescribes capitalisation of borrowing costs directly attributable to acquisition/construction of qualifying assets.",
        "examples": [
            "Interest on loan for factory construction capitalized until ready to use.",
            "General borrowing rate applied proportionally if specific loan not taken.",
            "Capitalisation stops when asset is ready for use.",
            "Interest on loan for working capital not capitalized."
        ]
    },
    "AS 17": {
        "summary": "AS 17: Segment Reporting\nRequires disclosure of segment-wise revenue, expenses, and capital employed based on business/geographical segments.",
        "examples": [
            "Company with IT and Pharma divisions shows segment-wise profit.",
            "Overseas sales shown separately under geographical segments.",
            "Unallocated expenses shown in common head.",
            "Segment assets and liabilities disclosed where material."
        ]
    },
    "AS 18": {
        "summary": "AS 18: Related Party Disclosures\nMandates disclosure of relationships, transactions, and balances with related parties.",
        "examples": [
            "Sales to subsidiary company disclosed separately.",
            "Managerial remuneration to director shown under related party.",
            "Loans given to key management shown with terms.",
            "Joint venture transactions disclosed clearly."
        ]
    },
    "AS 19": {
        "summary": "AS 19: Leases\nSpecifies accounting treatment for finance and operating leases by lessee and lessor.",
        "examples": [
            "Finance lease — asset and liability recorded by lessee.",
            "Operating lease — rent expense shown in P&L.",
            "Lease income for lessor under operating lease recognized on accrual.",
            "Disclosures required for future lease payments."
        ]
    },
    "AS 20": {
        "summary": "AS 20: Earnings Per Share\nDefines methods for calculating and disclosing basic and diluted earnings per share.",
        "examples": [
            "Net profit ₹10 lakhs, 2 lakh shares — EPS = ₹5.",
            "Convertible debentures included in diluted EPS.",
            "Bonus issue adjusted retrospectively.",
            "Disclose both basic and diluted EPS."
        ]
    },
    "AS 21": {
        "summary": "AS 21: Consolidated Financial Statements\nCovers preparation of consolidated financial statements of parent and subsidiaries.",
        "examples": [
            "Parent owns 80% in subsidiary — full consolidation done.",
            "Minority interest shown separately.",
            "Intra-group transactions eliminated.",
            "Consolidation required if control exists even without majority holding."
        ]
    },
    "AS 22": {
        "summary": "AS 22: Accounting for Taxes on Income\nDeals with deferred tax asset/liability due to timing differences between accounting and tax income.",
        "examples": [
            "Depreciation higher in tax books — deferred tax liability created.",
            "Preliminary expenses disallowed now — deferred tax asset created.",
            "DTL and DTA shown net where applicable.",
            "Reviewed for future realisability."
        ]
    },
    "AS 23": {
        "summary": "AS 23: Accounting for Investments in Associates\nPrescribes equity method for accounting investments in associates in consolidated financials.",
        "examples": [
            "Holding 30% in another company — considered associate.",
            "Share of profit/loss added to investment amount.",
            "Dividends reduce carrying amount.",
            "Unrealised profits eliminated to extent of holding."
        ]
    },
    "AS 24": {
        "summary": "AS 24: Discontinuing Operations\nSpecifies disclosures and presentation when a component of the enterprise is being discontinued.",
        "examples": [
            "Company closes retail segment — results shown separately.",
            "Assets/liabilities of discontinued unit shown distinctly.",
            "Disclosure of disposal plan and expected timeline.",
            "Impact on overall business disclosed."
        ]
    },
    "AS 25": {
        "summary": "AS 25: Interim Financial Reporting\nCovers recognition, measurement, and disclosures in financial reports for interim periods.",
        "examples": [
            "Quarterly profit/loss disclosed.",
            "Inventory valued using same principles as annual report.",
            "Taxes estimated and expensed quarterly.",
            "Disclosure of seasonal variations if any."
        ]
    },
    "AS 26": {
        "summary": "AS 26: Intangible Assets\nDeals with recognition and amortization of identifiable non-monetary assets without physical substance.",
        "examples": [
            "Software purchased capitalized and amortized over 3 years.",
            "Self-generated goodwill not recognized.",
            "Research cost expensed, development cost capitalized if criteria met.",
            "Trademark purchased shown as intangible asset."
        ]
    },
    "AS 27": {
        "summary": "AS 27: Financial Reporting of Interests in Joint Ventures\nPrescribes accounting and disclosures for joint ventures and venturer's share.",
        "examples": [
            "Company in 50:50 JV uses proportionate consolidation method.",
            "Jointly controlled operations — only share of income/expenses recorded.",
            "Separate disclosure of JV in notes.",
            "Jointly controlled assets — share of depreciation and income shown."
        ]
    },
    "AS 28": {
        "summary": "AS 28: Impairment of Assets\nSpecifies procedures to ensure assets are not carried at more than their recoverable amount.",
        "examples": [
            "Machinery’s recoverable amount less than book value — impairment loss booked.",
            "Loss shown in P&L and asset written down.",
            "Reversal of impairment allowed in future if recoverable amount increases.",
            "Indicators of impairment tested annually."
        ]
    },
    "AS 29": {
        "summary": "AS 29: Provisions, Contingent Liabilities and Contingent Assets\nDefines recognition criteria and disclosures for provisions and contingencies.",
        "examples": [
            "Provision for warranty made based on past trend.",
            "Court case pending — disclosed as contingent liability if outcome uncertain.",
            "Future reimbursement shown as contingent asset if probable.",
            "Provision reversed if obligation no longer exists."
        ]
    }
}

# ------------------------- Search Function -------------------------
def fetch_as_summary(query):
    for code, content in as_data.items():
        if code.lower() in query.lower():
            return code, content["summary"], content.get("examples", [])
    return None, "⚠️ Sorry, I couldn't find a summary for that AS.", []

# ------------------------- UI -------------------------
st.subheader("🔍 Search or Select an Accounting Standard")
user_input = st.text_input("Type an AS query:", placeholder="e.g. Summarize AS 10 or Explain AS 2")
dropdown = st.selectbox("Or select from list:", ["Select an AS"] + list(as_data.keys()))

summary = ""
examples = []
selected_as = ""

if st.button("🧠 Get Summary"):
    if user_input:
        selected_as, summary, examples = fetch_as_summary(user_input)
    elif dropdown != "Select an AS":
        selected_as = dropdown
        summary = as_data[selected_as]["summary"]
        examples = as_data[selected_as].get("examples", [])
    else:
        summary = "⚠️ Please enter a query or select an AS."

    st.markdown("---")
    st.markdown(f"**{selected_as}**\n\n{summary}")

    if examples:
        with st.expander("📌 Show Real-life Examples"):
            for i, ex in enumerate(examples, 1):
                st.markdown(f"**Example {i}:** {ex}")

    # ------------------------- Download as PDF -------------------------
    if selected_as and summary and "⚠️" not in summary:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"{selected_as}\n\n{summary}\n")
        if examples:
            pdf.multi_cell(0, 10, "\nReal-life Examples:")
            for i, ex in enumerate(examples, 1):
                pdf.multi_cell(0, 10, f"Example {i}: {ex}")

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
st.caption("Made for CA Students | AS Summarizer with Real-life Examples | Ind AS & Comparison Coming Soon")
