# ⚖️ eCourts India Scraper

A Python-based web application built with Streamlit to fetch court listings from the [eCourts India](https://services.ecourts.gov.in/ecourtindia_v6/) portal.

## 📋 Features

- **Multiple Search Methods**
  - Search by CNR (Case Number Record)
  - Search by Case Details (Type, Number, Year)

- **Smart Date Filtering**
  - Check if case is listed today
  - Check if case is listed tomorrow
  - View both days at once

- **Comprehensive Results**
  - Display serial number in court listing
  - Show court name and room details
  - View listing date
  - Export results as JSON

- **PDF Downloads**
  - Download individual case PDFs
  - Professional PDF formatting with case details

- **Cause List Management**
  - Download entire cause list for any date
  - View cause list in tabular format
  - Export cause list as JSON

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/Manjupatat/ecourts_scraper
   cd ecourts_scraper
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the application**
   - The app will automatically open in your browser
   - Default URL: `http://localhost:8501`

## 📦 Dependencies

Create a `requirements.txt` file with:

```
streamlit>=1.28.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
reportlab>=4.0.0
pandas>=2.0.0
```

## 🎯 Usage

### Search by CNR Number

1. Select **"CNR Number"** in the sidebar
2. Enter your 16-digit CNR (e.g., `DLCT01001234567890`)
3. Choose date filter (Today/Tomorrow/Both)
4. Click **"🔎 Search"**
5. View results with serial numbers and court names
6. Download PDFs for individual cases

### Search by Case Details

1. Select **"Case Details"** in the sidebar
2. Fill in the form:
   - **Case Type**: CS, CRL, WP, FAO, MAC, MISC
   - **Case Number**: e.g., `123`
   - **Case Year**: e.g., `2024`
3. Choose date filter
4. Click **"🔎 Search"**
5. View and download results

### Download Cause List

1. Check **"Download Full Cause List"** in sidebar
2. Select the date using the date picker
3. Click **"📥 Download Cause List"**
4. View the table and download JSON

## 📊 Sample Inputs

**For Testing CNR Search:**
- CNR: `DLCT01001234567890` (any 16+ character string)

**For Testing Case Details:**
- Case Type: `CS`
- Case Number: `123`
- Case Year: `2024`

## 🗂️ Project Structure

```
ecourts_scraper/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # This file

```

## 📝 Output Files

### JSON Results Format
```json
{
  "search_timestamp": "2024-10-19T10:30:00",
  "total_results": 2,
  "listings": [
    {
      "serial_number": "23",
      "court_name": "District Court, Patiala House",
      "listing_date": "2024-10-19",
      "case_details": "CNR: DLCT01001234567890"
    }
  ]
}
```

### Cause List Format
```json
{
  "date": "2024-10-19",
  "cause_list": [
    {
      "serial_no": "1",
      "case_number": "CS/123/2024",
      "parties": "ABC Pvt Ltd vs XYZ Corp",
      "court_room": "Court Room 1",
      "time": "10:30 AM"
    }
  ]
}
```


```

### Testing
```bash
# Run with demo data
streamlit run app.py

```

## 📜 License

This project is for educational purposes. Ensure compliance with eCourts India's terms of service before using for production.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Check eCourts documentation: https://services.ecourts.gov.in

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Data source: [eCourts India](https://services.ecourts.gov.in/ecourtindia_v6/)

---
