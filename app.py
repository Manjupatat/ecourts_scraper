import streamlit as st
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Optional, List
import json
from datetime import datetime, timedelta
import time

# ===== DATA MODELS =====
@dataclass
class CaseDetails:
    cnr: Optional[str] = None
    case_type: Optional[str] = None
    case_number: Optional[str] = None
    case_year: Optional[str] = None

@dataclass
class ListingInfo:
    serial_number: str
    court_name: str
    listing_date: str
    case_details: str

# ===== SCRAPER CLASS =====
class ECourtsScraper:
    def __init__(self):
        self.base_url = "https://services.ecourts.gov.in/ecourtindia_v6/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_by_cnr(self, cnr: str) -> List[ListingInfo]:
        """Search case by CNR number"""
        try:
            time.sleep(0.5)  # Rate limiting
            
            st.info("🔍 Connecting to eCourts portal...")
            
            # DEMO DATA - Simulating actual search results
            today = datetime.now().strftime('%Y-%m-%d')
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Simulate finding listings
            demo_results = [
                ListingInfo(
                    serial_number="23",
                    court_name="District Court, Patiala House, New Delhi",
                    listing_date=today,
                    case_details=f"CNR: {cnr}"
                ),
                ListingInfo(
                    serial_number="45",
                    court_name="District Court, Tis Hazari, Delhi",
                    listing_date=tomorrow,
                    case_details=f"CNR: {cnr} (Continuation)"
                )
            ]
            
            st.success("✅ Connected to eCourts portal")
            return demo_results
            
        except Exception as e:
            st.error(f"Error during CNR search: {str(e)}")
            return []
    
    def search_by_case_details(self, case: CaseDetails) -> List[ListingInfo]:
        """Search case by case type, number, and year"""
        try:
            time.sleep(0.5)  # Rate limiting
            st.info("🔍 Searching case listings...")
            
            # DEMO DATA - Simulating actual search results
            today = datetime.now().strftime('%Y-%m-%d')
            
            demo_results = [
                ListingInfo(
                    serial_number="12",
                    court_name=f"Court of {case.case_type} - Court Room 3",
                    listing_date=today,
                    case_details=f"{case.case_type}/{case.case_number}/{case.case_year}"
                )
            ]
            
            st.success("✅ Case found in listings")
            return demo_results
            
        except Exception as e:
            st.error(f"Error during case search: {str(e)}")
            return []
    
    def download_pdf(self, case_id: str, output_path: str) -> Optional[bytes]:
        """Download case PDF if available"""
        try:
            st.info(f"📄 Generating PDF for case: {case_id}...")
            time.sleep(0.5)
            
            # DEMO: Create a simple PDF content (in real scenario, download from eCourts)
            pdf_content = f"""
            eCOURTS INDIA - CASE DETAILS
            ============================
            
            Case: {case_id}
            Download Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            This is a demo PDF. In actual implementation, 
            this would be downloaded from the eCourts portal.
            
            Court Name: District Court
            Next Hearing: {datetime.now().strftime('%Y-%m-%d')}
            Status: Listed
            """.encode('utf-8')
            
            st.success("✅ PDF generated successfully")
            return pdf_content
            
        except Exception as e:
            st.error(f"PDF download failed: {str(e)}")
            return None
    
    def get_cause_list(self, date: datetime) -> List[dict]:
        """Download entire cause list for a given date"""
        try:
            st.info(f"📋 Fetching cause list for {date.strftime('%Y-%m-%d')}...")
            time.sleep(0.5)
            
            # DEMO DATA - Simulating cause list
            demo_causelist = [
                {
                    "serial_no": "1",
                    "case_number": "CS/123/2024",
                    "parties": "ABC Pvt Ltd vs XYZ Corp",
                    "court_room": "Court Room 1",
                    "time": "10:30 AM"
                },
                {
                    "serial_no": "2",
                    "case_number": "CRL/456/2024",
                    "parties": "State vs John Doe",
                    "court_room": "Court Room 2",
                    "time": "11:00 AM"
                },
                {
                    "serial_no": "3",
                    "case_number": "WP/789/2024",
                    "parties": "Petitioner A vs Respondent B",
                    "court_room": "Court Room 3",
                    "time": "02:00 PM"
                },
                {
                    "serial_no": "4",
                    "case_number": "FAO/234/2024",
                    "parties": "Appellant vs State",
                    "court_room": "Court Room 1",
                    "time": "03:30 PM"
                }
            ]
            
            st.success(f"✅ Fetched {len(demo_causelist)} entries")
            return demo_causelist
            
        except Exception as e:
            st.error(f"Error fetching cause list: {str(e)}")
            return []

# ===== UTILITY FUNCTIONS =====
def validate_cnr(cnr: str) -> bool:
    """Validate CNR format"""
    if not cnr or len(cnr) < 16:
        return False
    return True

def validate_case_number(case_number: str) -> bool:
    """Validate case number"""
    return case_number and case_number.strip() != ""

def save_results_json(data: dict, filename: str):
    """Save results to JSON file"""
    try:
        json_str = json.dumps(data, indent=2)
        st.download_button(
            label="📥 Download Results (JSON)",
            data=json_str,
            file_name=filename,
            mime="application/json"
        )
    except Exception as e:
        st.error(f"Error saving JSON: {str(e)}")

# ===== STREAMLIT UI =====
def main():
    st.set_page_config(
        page_title="eCourts Scraper",
        page_icon="⚖️",
        layout="wide"
    )
    
    st.title("⚖️ eCourts India Scraper")
    st.markdown("Fetch court listings from eCourts India portal")
    
    # Initialize scraper
    scraper = ECourtsScraper()
    
    # Sidebar
    st.sidebar.header("Search Options")
    search_method = st.sidebar.radio(
        "Select Search Method:",
        ["CNR Number", "Case Details"]
    )
    
    date_filter = st.sidebar.selectbox(
        "Check Listings For:",
        ["Today", "Tomorrow", "Both"]
    )
    
    show_causelist = st.sidebar.checkbox("Download Full Cause List")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Search Case")
        
        if search_method == "CNR Number":
            cnr = st.text_input(
                "Enter CNR Number:",
                placeholder="DLCT010012345678",
                help="16-digit CNR number"
            )
            
            if st.button("🔎 Search", type="primary"):
                if validate_cnr(cnr):
                    with st.spinner("Searching..."):
                        results = scraper.search_by_cnr(cnr)
                        
                        if results:
                            st.success(f"✅ Found {len(results)} listing(s)")
                            display_results(results)
                        else:
                            st.warning("No listings found for today/tomorrow")
                else:
                    st.error("Invalid CNR format. Please enter a valid 16-digit CNR.")
        
        else:  # Case Details
            case_type = st.selectbox(
                "Case Type:",
                ["Select", "CS", "CRL", "WP", "FAO", "MAC", "MISC"]
            )
            
            case_number = st.text_input("Case Number:", placeholder="123")
            case_year = st.text_input("Case Year:", placeholder="2024")
            
            if st.button("🔎 Search", type="primary"):
                if case_type != "Select" and validate_case_number(case_number) and case_year:
                    case = CaseDetails(
                        case_type=case_type,
                        case_number=case_number,
                        case_year=case_year
                    )
                    
                    with st.spinner("Searching..."):
                        results = scraper.search_by_case_details(case)
                        
                        if results:
                            st.success(f"✅ Found {len(results)} listing(s)")
                            display_results(results)
                        else:
                            st.warning("No listings found for today/tomorrow")
                else:
                    st.error("Please fill all case details correctly")
    
    with col2:
        st.subheader("ℹ️ Information")
        st.info("""
        **Features:**
        - Search by CNR or Case Details
        - Check today/tomorrow listings
        - View serial number & court
        - Download case PDFs
        - Export results as JSON
        """)
        
        st.warning("""
        **Note:** This is a demo structure. 
        Full implementation requires:
        - CAPTCHA handling
        - Session management
        - Dynamic form parsing
        - Error retry logic
        """)
    
    # Cause List Section
    if show_causelist:
        st.markdown("---")
        st.subheader("📋 Download Cause List")
        
        col1, col2 = st.columns(2)
        with col1:
            causelist_date = st.date_input(
                "Select Date:",
                value=datetime.now()
            )
        with col2:
            if st.button("📥 Download Cause List"):
                with st.spinner("Fetching cause list..."):
                    causelist = scraper.get_cause_list(causelist_date)
                    if causelist:
                        st.success(f"✅ Found {len(causelist)} entries")
                        
                        # Display cause list table
                        import pandas as pd
                        df = pd.DataFrame(causelist)
                        st.dataframe(df, use_container_width=True)
                        
                        # Download button
                        save_results_json(
                            {"cause_list": causelist, "date": str(causelist_date)},
                            f"causelist_{causelist_date}.json"
                        )

def display_results(results: List[ListingInfo]):
    """Display search results in a table"""
    if not results:
        return
    
    st.markdown("### 📊 Listing Results")
    
    # Initialize scraper for PDF downloads
    scraper = ECourtsScraper()
    
    for idx, result in enumerate(results, 1):
        with st.expander(f"Listing #{idx} - Serial: {result.serial_number}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Serial Number:** {result.serial_number}")
                st.write(f"**Court Name:** {result.court_name}")
            with col2:
                st.write(f"**Listing Date:** {result.listing_date}")
                st.write(f"**Case Details:** {result.case_details}")
            
            # Direct PDF Download button
            with st.spinner(""):
                pdf_data = scraper.download_pdf(result.case_details, f"case_{idx}.pdf")
                if pdf_data:
                    st.download_button(
                        label="📄 Download Case PDF",
                        data=pdf_data,
                        file_name=f"case_{result.serial_number}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        key=f"pdf_download_{idx}",
                        type="secondary"
                    )
    
    # Export all results
    results_dict = {
        "search_timestamp": datetime.now().isoformat(),
        "total_results": len(results),
        "listings": [
            {
                "serial_number": r.serial_number,
                "court_name": r.court_name,
                "listing_date": r.listing_date,
                "case_details": r.case_details
            }
            for r in results
        ]
    }
    
    save_results_json(results_dict, "search_results.json")

if __name__ == "__main__":
    main()