# Reservation-Daily-Split-Tool-with-Revenue

## Overview
This Streamlit application converts reservation-level booking data and seperates it
night-level data. Each booking is expanded into one row per night stayed,
and all revenue and fee values are evenly distributed across nights.

This allows for accurate daily analysis of revenue, occupancy, and fees.

---

## Features
- Converts reservation data into nightly rows
- Automatically generates stay dates from Arrival and Departure
- Splits all revenue and fee columns per night
- Handles missing or invalid dates safely
- Outputs a clean Excel file with:
  - Original reservation data
  - Night-level split data

---

## Input Requirements
The uploaded Excel file must contain at least:
- Reservation Number
- Arrival
- Departure
- Booking Date

Additional columns such as revenue and fees are handled automatically if present.

---
## How to Run

### Option 1: Use the Deployed App
1. Open the Streamlit app link
2. Upload a reservations Excel file (.xlsx)
3. Preview the processed data
4. Download the output Excel file

No installation or setup is required.

---

## Output
The downloaded Excel file contains:
- **Original Data**: Cleaned reservation-level data
- **Reservations Daily Split**: One row per night with per-night revenue values

---

## Built With
- Python
- Pandas
- Streamlit

---

## Author
Dharani Saravanan
