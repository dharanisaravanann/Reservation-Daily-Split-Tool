import os
import streamlit as st
import pandas as pd
from io import BytesIO

st.write("RUNNING FILE:", os.path.abspath(__file__))


def reservation_with_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keeps 1 row per reservation.
    Converts all date columns to Excel DATEVALUE serial numbers.
    Cleans revenue columns.
    """
    df = df.copy()
    df.columns = df.columns.str.strip()

    # Excel DATEVALUE epoch
    EXCEL_EPOCH = pd.Timestamp("1899-12-30")

    # Convert date columns to Excel serial numbers
    for col in ["Arrival", "Departure", "Booking Date"]:
        if col in df.columns:
            df[col] = (
                pd.to_datetime(df[col], dayfirst=True, errors="coerce") - EXCEL_EPOCH
            ).dt.days

    # Revenue-related columns
    revenue_cols = [
        "Base Revenue",
        "Total Revenue",
        "Room Revenue",
        "SC on Room Revenue",
        "VAT on Room Rev",
        "VAT on SC",
        "Cleaning Fees Without VAT",
        "VAT on Cleaning Fees",
        "Tourism Dirham Fees",
        "Cleaning Fees",
    ]

    # Ensure numeric
    for col in revenue_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Rename Channel → Sub Channel
    if "Channel" in df.columns:
        df = df.rename(columns={"Channel": "Sub Channel"})

    desired_cols = [
        "Reservation Number",
        "Apartment",
        "Guest Name",
        "Sub Channel",
        "Arrival",        # Excel serial
        "Departure",      # Excel serial
        "Booking Date",   # Excel serial
        "Base Revenue",
        "Total Revenue",
        "Room Revenue",
        "SC on Room Revenue",
        "VAT on Room Rev",
        "VAT on SC",
        "Cleaning Fees Without VAT",
        "VAT on Cleaning Fees",
        "Tourism Dirham Fees",
        "Cleaning Fees",
    ]

    desired_cols = [c for c in desired_cols if c in df.columns]
    return df[desired_cols]


# ---------------- STREAMLIT APP ----------------

st.title("Reservation Revenue Split Tool")

st.write(
    "Upload a reservations Excel file (.xlsx) and this tool will:\n"
    "- Keep one row per reservation\n"
    "- Convert all date columns to Excel DATEVALUE format\n"
    "- Return an Excel file with two sheets: Original Data + Reservation Revenue Summary"
)

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file is not None:
    try:
        df_input = pd.read_excel(uploaded_file)
        df_input.columns = df_input.columns.str.strip()

        st.subheader("Preview of uploaded data")
        st.dataframe(df_input.head(), use_container_width=True)

        df_output = reservation_with_revenue(df_input)

        st.subheader("Preview of reservation revenue summary")
        st.dataframe(df_output.head(20), use_container_width=True)

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_input.to_excel(writer, sheet_name="Original Data", index=False)
            df_output.to_excel(writer, sheet_name="Reservation Revenue Summary", index=False)

        buffer.seek(0)

        st.download_button(
            label="📥 Download Excel (Original + Revenue Summary)",
            data=buffer,
            file_name="reservation_revenue_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")
else:
    st.info("Please upload an Excel file to begin.")

