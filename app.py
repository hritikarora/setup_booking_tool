# import streamlit as st
# import pandas as pd
# import os
# from datetime import datetime, timedelta

# BOOKINGS_FILE = "bookings.csv"
# SETUPS = ["VM1", "VM2", "Router1", "Router2", "SetupA", "SetupB"]

# # Initialize CSV
# if not os.path.exists(BOOKINGS_FILE):
#     pd.DataFrame(columns=["Setup", "Name", "From", "To"]).to_csv(BOOKINGS_FILE, index=False)

# # Load bookings
# def load_bookings():
#     df = pd.read_csv(BOOKINGS_FILE)
#     df["From"] = pd.to_datetime(df["From"]).dt.floor("min")
#     df["To"] = pd.to_datetime(df["To"]).dt.floor("min")
#     return df


# bookings_df = load_bookings()

# st.title("🔧 Setup Booking Tool")
# st.markdown("Book and manage shared setup reservations within your team.")

# # --------- BOOK A SETUP ---------
# st.header("📅 Book a Setup")

# with st.form("booking_form"):
#     name = st.text_input("Your Name", key="name")
#     setup = st.selectbox("Select Setup", SETUPS, key="setup_select")

#     date = st.date_input("Select Booking Date", value=datetime.now().date(), key="date")
#     start_time = st.time_input("From Time", value=datetime.now().time(), key="start")
#     end_time = st.time_input("To Time", value=(datetime.now() + timedelta(hours=1)).time(), key="end")

#     submit = st.form_submit_button("✅ Book Now")

#     if submit:
#         # Round to nearest minute (remove seconds and microseconds)
#         start_dt = datetime.combine(date, start_time).replace(second=0, microsecond=0)
#         end_dt = datetime.combine(date, end_time).replace(second=0, microsecond=0)

#         if not name.strip():
#             st.warning("⚠️ Please enter your name.")
#         elif end_dt <= start_dt:
#             st.warning("⚠️ End time must be after start time.")
#         else:
#             conflicts = bookings_df[
#                 (bookings_df["Setup"] == setup) &
#                 (
#                     ((start_dt >= bookings_df["From"]) & (start_dt < bookings_df["To"])) |
#                     ((end_dt > bookings_df["From"]) & (end_dt <= bookings_df["To"])) |
#                     ((start_dt <= bookings_df["From"]) & (end_dt >= bookings_df["To"]))
#                 )
#             ]
#             if not conflicts.empty:
#                 st.error("❌ This setup is already booked during that time.")
#                 st.rerun()
#             else:
#                 new_entry = pd.DataFrame([{
#                     "Setup": setup,
#                     "Name": name.strip(),
#                     "From": start_dt,
#                     "To": end_dt
#                 }])
#                 updated_df = pd.concat([bookings_df, new_entry], ignore_index=True)
#                 updated_df.to_csv(BOOKINGS_FILE, index=False)
#                 st.success(f"✅ {setup} booked from {start_dt.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')} on {date.strftime('%d %b %Y')} by {name}.")
#                 st.rerun()  # Refresh app after booking

# # --------- UPCOMING BOOKINGS ---------
# st.header("📋 Current & Upcoming Bookings")
# bookings_df = load_bookings()
# now = datetime.now()
# upcoming_df = bookings_df[bookings_df["To"] > now].sort_values("From")

# if upcoming_df.empty:
#     st.info("🟢 No upcoming bookings.")
# else:
#     st.dataframe(upcoming_df, use_container_width=True)

# # # --------- UNBOOK A SETUP ---------
# st.header("❌ Cancel Your Booking")

# with st.form("unbook_form"):
#     unbook_name = st.text_input("Enter Your Name to View Your Bookings")

#     # Submit button for the form (must be inside `with st.form`)
#     cancel_button = st.form_submit_button("🔍 Show My Bookings")

# if cancel_button:
#     bookings_df = load_bookings()
#     my_bookings = bookings_df[(bookings_df["Name"].str.lower() == unbook_name.strip().lower())]

#     if not my_bookings.empty:
#         selected_option = st.selectbox(
#             "Select a Booking to Cancel",
#             [
#                 f"{row['Setup']} | {row['From'].strftime('%d-%b %I:%M %p')} → {row['To'].strftime('%I:%M %p')}"
#                 for _, row in my_bookings.iterrows()
#             ]
#         )
#         confirm_cancel = st.button("❌ Cancel Selected Booking")

#         if confirm_cancel:
#             idx = [
#                 f"{row['Setup']} | {row['From'].strftime('%d-%b %I:%M %p')} → {row['To'].strftime('%I:%M %p')}"
#                 for _, row in my_bookings.iterrows()
#             ].index(selected_option)
#             booking_to_cancel = my_bookings.iloc[idx]

#             bookings_df = bookings_df[
#                 ~(
#                     (bookings_df["Setup"] == booking_to_cancel["Setup"]) &
#                     (bookings_df["From"] == booking_to_cancel["From"]) &
#                     (bookings_df["To"] == booking_to_cancel["To"]) &
#                     (bookings_df["Name"] == booking_to_cancel["Name"])
#                 )
#             ]
#             bookings_df.to_csv(BOOKINGS_FILE, index=False)
#             st.success("✅ Booking cancelled successfully.")
#             st.rerun()
#     else:
#         st.info("No bookings found under that name.")

import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta, time

BOOKINGS_FILE = "bookings.csv"
SETUPS = ["VM1", "VM2", "Router1", "Router2", "SetupA", "SetupB"]

# Initialize CSV
if not os.path.exists(BOOKINGS_FILE):
    pd.DataFrame(columns=["Setup", "Name", "From", "To"]).to_csv(BOOKINGS_FILE, index=False)

# Load bookings
def load_bookings():
    df = pd.read_csv(BOOKINGS_FILE)
    df["From"] = pd.to_datetime(df["From"]).dt.floor("min")
    df["To"] = pd.to_datetime(df["To"]).dt.floor("min")
    return df


bookings_df = load_bookings()

st.title("🔧 Setup Booking Tool")
st.markdown("Book and manage shared setup reservations within your team.")

# --------- BOOK A SETUP ---------
st.header("📅 Book a Setup")

# Utility: Round up current time to next 15-minute interval
def next_15_min_interval():
    now = datetime.now()
    rounded = (now + timedelta(minutes=15)).replace(second=0, microsecond=0)
    minutes_to_add = 15 - (rounded.minute % 15) if rounded.minute % 15 != 0 else 0
    return (rounded + timedelta(minutes=minutes_to_add)).time()

with st.form("booking_form"):
    name = st.text_input("Your Name", key="name")
    setup = st.selectbox("Select Setup", SETUPS, key="setup_select")

    date = st.date_input("Select Booking Date", value=datetime.now().date(), key="date")

    # Time selection with 15-min intervals
    default_time = next_15_min_interval()
    time_options = [time(hour=h, minute=m) for h in range(24) for m in range(0, 60, 15)]

    start_time = st.selectbox("From Time", time_options, index=time_options.index(default_time), key="start")
    end_time = st.selectbox("To Time", time_options, index=min(len(time_options)-1, time_options.index(default_time)+4), key="end")

    submit = st.form_submit_button("✅ Book Now")

    if submit:
        start_dt = datetime.combine(date, start_time)
        end_dt = datetime.combine(date, end_time)

        if not name.strip():
            st.warning("⚠️ Please enter your name.")
        elif end_dt <= start_dt:
            st.warning("⚠️ End time must be after start time.")
        else:
            conflicts = bookings_df[
                (bookings_df["Setup"] == setup) &
                (
                    ((start_dt >= bookings_df["From"]) & (start_dt < bookings_df["To"])) |
                    ((end_dt > bookings_df["From"]) & (end_dt <= bookings_df["To"])) |
                    ((start_dt <= bookings_df["From"]) & (end_dt >= bookings_df["To"]))
                )
            ]
            if not conflicts.empty:
                st.error("❌ This setup is already booked during that time.")
                time.sleep(2)  # Optional: Add a slight delay for user experience
                st.rerun()
            else:
                new_entry = pd.DataFrame([{
                    "Setup": setup,
                    "Name": name.strip(),
                    "From": start_dt,
                    "To": end_dt
                }])
                updated_df = pd.concat([bookings_df, new_entry], ignore_index=True)
                updated_df.to_csv(BOOKINGS_FILE, index=False)
                st.success(f"✅ {setup} booked from {start_dt.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')} on {date.strftime('%d %b %Y')} by {name}.")
                time.sleep(2)  # Optional: Add a slight delay for user experience
                st.rerun()

# --------- UPCOMING BOOKINGS ---------
st.header("📋 Current & Upcoming Bookings")
bookings_df = load_bookings()
now = datetime.now()
upcoming_df = bookings_df[bookings_df["To"] > now].sort_values(by="From")

if upcoming_df.empty:
    st.info("🟢 No upcoming bookings.")
else:
    st.dataframe(upcoming_df, use_container_width=True, hide_index=True)

# --------- UNBOOK A SETUP ---------
# st.subheader("❌ Cancel a Booking")
# if not bookings_df.empty:
#     # Create a unique label for each booking
#     bookings_df["Label"] = bookings_df.apply(
#         lambda row: f'{row["Setup"]} booked by {row["Name"]} from {row["From"].strftime("%Y-%m-%d %H:%M")} to {row["To"].strftime("%Y-%m-%d %H:%M")}',
#         axis=1
#     )
#     cancel_label = st.selectbox("Select booking to cancel", bookings_df["Label"].tolist())
    
#     with st.form("cancel_form"):
#         cancel_submit = st.form_submit_button("Cancel Booking")
#         if cancel_submit:
#             # Find the row matching the selected label
#             updated_df = bookings_df[bookings_df["Label"] != cancel_label].drop(columns=["Label"])
#             updated_df.to_csv(BOOKINGS_FILE, index=False)
#             st.success("✅ Booking cancelled successfully.")
#             time.sleep(2)
#             st.rerun()
# else:
#     st.info("ℹ️ No bookings found.")

# --------- UNBOOK A SETUP ---------
# st.header("❌ Cancel Your Booking")

# with st.form("unbook_form"):
#     unbook_name = st.text_input("Enter Your Name to View Your Bookings")
#     cancel_button = st.form_submit_button("🔍 Show My Bookings")

# if cancel_button:
#     bookings_df = load_bookings()
#     my_bookings = bookings_df[(bookings_df["Name"].str.lower() == unbook_name.strip().lower())]

#     if not my_bookings.empty:
#         selected_option = st.selectbox(
#             "Select a Booking to Cancel",
#             [
#                 f"{row['Setup']} | {row['From'].strftime('%d-%b %I:%M %p')} → {row['To'].strftime('%I:%M %p')}"
#                 for _, row in my_bookings.iterrows()
#             ]
#         )
#         confirm_cancel = st.button("❌ Cancel Selected Booking")

#         if confirm_cancel:
#             idx = [
#                 f"{row['Setup']} | {row['From'].strftime('%d-%b %I:%M %p')} → {row['To'].strftime('%I:%M %p')}"
#                 for _, row in my_bookings.iterrows()
#             ].index(selected_option)
#             booking_to_cancel = my_bookings.iloc[idx]

#             bookings_df = bookings_df[
#                 ~(
#                     (bookings_df["Setup"] == booking_to_cancel["Setup"]) &
#                     (bookings_df["From"] == booking_to_cancel["From"]) &
#                     (bookings_df["To"] == booking_to_cancel["To"]) &
#                     (bookings_df["Name"] == booking_to_cancel["Name"])
#                 )
#             ]
#             bookings_df.to_csv(BOOKINGS_FILE, index=False)
#             st.success("✅ Booking cancelled successfully.")
#             st.rerun()
#     else:
#         st.info("No bookings found under that name.")
