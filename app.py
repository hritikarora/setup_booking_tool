# # # import streamlit as st
# # # import pandas as pd
# # # import os
# # # from datetime import datetime, timedelta

# # # BOOKINGS_FILE = "bookings.csv"
# # # SETUPS = ["VM1", "VM2", "Router1", "Router2", "SetupA", "SetupB"]

# # # # Initialize CSV
# # # if not os.path.exists(BOOKINGS_FILE):
# # #     pd.DataFrame(columns=["Setup", "Name", "From", "To"]).to_csv(BOOKINGS_FILE, index=False)

# # # # Load bookings
# # # def load_bookings():
# # #     df = pd.read_csv(BOOKINGS_FILE)
# # #     df["From"] = pd.to_datetime(df["From"]).dt.floor("min")
# # #     df["To"] = pd.to_datetime(df["To"]).dt.floor("min")
# # #     return df


# # # bookings_df = load_bookings()

# # # st.title("🔧 Setup Booking Tool")
# # # st.markdown("Book and manage shared setup reservations within your team.")

# # # # --------- BOOK A SETUP ---------
# # # st.header("📅 Book a Setup")

# # # with st.form("booking_form"):
# # #     name = st.text_input("Your Name", key="name")
# # #     setup = st.selectbox("Select Setup", SETUPS, key="setup_select")

# # #     date = st.date_input("Select Booking Date", value=datetime.now().date(), key="date")
# # #     start_time = st.time_input("From Time", value=datetime.now().time(), key="start")
# # #     end_time = st.time_input("To Time", value=(datetime.now() + timedelta(hours=1)).time(), key="end")

# # #     submit = st.form_submit_button("✅ Book Now")

# # #     if submit:
# # #         # Round to nearest minute (remove seconds and microseconds)
# # #         start_dt = datetime.combine(date, start_time).replace(second=0, microsecond=0)
# # #         end_dt = datetime.combine(date, end_time).replace(second=0, microsecond=0)

# # #         if not name.strip():
# # #             st.warning("⚠️ Please enter your name.")
# # #         elif end_dt <= start_dt:
# # #             st.warning("⚠️ End time must be after start time.")
# # #         else:
# # #             conflicts = bookings_df[
# # #                 (bookings_df["Setup"] == setup) &
# # #                 (
# # #                     ((start_dt >= bookings_df["From"]) & (start_dt < bookings_df["To"])) |
# # #                     ((end_dt > bookings_df["From"]) & (end_dt <= bookings_df["To"])) |
# # #                     ((start_dt <= bookings_df["From"]) & (end_dt >= bookings_df["To"]))
# # #                 )
# # #             ]
# # #             if not conflicts.empty:
# # #                 st.error("❌ This setup is already booked during that time.")
# # #                 st.rerun()
# # #             else:
# # #                 new_entry = pd.DataFrame([{
# # #                     "Setup": setup,
# # #                     "Name": name.strip(),
# # #                     "From": start_dt,
# # #                     "To": end_dt
# # #                 }])
# # #                 updated_df = pd.concat([bookings_df, new_entry], ignore_index=True)
# # #                 updated_df.to_csv(BOOKINGS_FILE, index=False)
# # #                 st.success(f"✅ {setup} booked from {start_dt.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')} on {date.strftime('%d %b %Y')} by {name}.")
# # #                 st.rerun()  # Refresh app after booking

# # # # --------- UPCOMING BOOKINGS ---------
# # # st.header("📋 Current & Upcoming Bookings")
# # # bookings_df = load_bookings()
# # # now = datetime.now()
# # # upcoming_df = bookings_df[bookings_df["To"] > now].sort_values("From")

# # # if upcoming_df.empty:
# # #     st.info("🟢 No upcoming bookings.")
# # # else:
# # #     st.dataframe(upcoming_df, use_container_width=True)

# # # # # --------- UNBOOK A SETUP ---------
# # # st.header("❌ Cancel Your Booking")

# # # with st.form("unbook_form"):
# # #     unbook_name = st.text_input("Enter Your Name to View Your Bookings")

# # #     # Submit button for the form (must be inside `with st.form`)
# # #     cancel_button = st.form_submit_button("🔍 Show My Bookings")

# # # if cancel_button:
# # #     bookings_df = load_bookings()
# # #     my_bookings = bookings_df[(bookings_df["Name"].str.lower() == unbook_name.strip().lower())]

# # #     if not my_bookings.empty:
# # #         selected_option = st.selectbox(
# # #             "Select a Booking to Cancel",
# # #             [
# # #                 f"{row['Setup']} | {row['From'].strftime('%d-%b %I:%M %p')} → {row['To'].strftime('%I:%M %p')}"
# # #                 for _, row in my_bookings.iterrows()
# # #             ]
# # #         )
# # #         confirm_cancel = st.button("❌ Cancel Selected Booking")

# # #         if confirm_cancel:
# # #             idx = [
# # #                 f"{row['Setup']} | {row['From'].strftime('%d-%b %I:%M %p')} → {row['To'].strftime('%I:%M %p')}"
# # #                 for _, row in my_bookings.iterrows()
# # #             ].index(selected_option)
# # #             booking_to_cancel = my_bookings.iloc[idx]

# # #             bookings_df = bookings_df[
# # #                 ~(
# # #                     (bookings_df["Setup"] == booking_to_cancel["Setup"]) &
# # #                     (bookings_df["From"] == booking_to_cancel["From"]) &
# # #                     (bookings_df["To"] == booking_to_cancel["To"]) &
# # #                     (bookings_df["Name"] == booking_to_cancel["Name"])
# # #                 )
# # #             ]
# # #             bookings_df.to_csv(BOOKINGS_FILE, index=False)
# # #             st.success("✅ Booking cancelled successfully.")
# # #             st.rerun()
# # #     else:
# # #         st.info("No bookings found under that name.")

# # import streamlit as st
# # import pandas as pd
# # import os
# # from datetime import datetime, timedelta, time

# # BOOKINGS_FILE = "bookings.csv"
# # SETUPS = ["VM1", "VM2", "Router1", "Router2", "SetupA", "SetupB"]

# # # Initialize CSV
# # if not os.path.exists(BOOKINGS_FILE):
# #     pd.DataFrame(columns=["Setup", "Name", "From", "To"]).to_csv(BOOKINGS_FILE, index=False)

# # # Load bookings
# # def load_bookings():
# #     df = pd.read_csv(BOOKINGS_FILE)
# #     df["From"] = pd.to_datetime(df["From"]).dt.floor("min")
# #     df["To"] = pd.to_datetime(df["To"]).dt.floor("min")
# #     return df


# # bookings_df = load_bookings()

# # st.title("🔧 Setup Booking Tool")
# # st.markdown("Book and manage shared setup reservations within your team.")

# # # --------- BOOK A SETUP ---------
# # st.header("📅 Book a Setup")

# # # Utility: Round up current time to next 15-minute interval
# # def next_15_min_interval():
# #     now = datetime.now()
# #     rounded = (now + timedelta(minutes=15)).replace(second=0, microsecond=0)
# #     minutes_to_add = 15 - (rounded.minute % 15) if rounded.minute % 15 != 0 else 0
# #     return (rounded + timedelta(minutes=minutes_to_add)).time()

# # with st.form("booking_form"):
# #     name = st.text_input("Your Name", key="name")
# #     setup = st.selectbox("Select Setup", SETUPS, key="setup_select")

# #     date = st.date_input("Select Booking Date", value=datetime.now().date(), key="date")

# #     # Time selection with 15-min intervals
# #     default_time = next_15_min_interval()
# #     time_options = [time(hour=h, minute=m) for h in range(24) for m in range(0, 60, 15)]

# #     start_time = st.selectbox("From Time", time_options, index=time_options.index(default_time), key="start")
# #     end_time = st.selectbox("To Time", time_options, index=min(len(time_options)-1, time_options.index(default_time)+4), key="end")

# #     submit = st.form_submit_button("✅ Book Now")

# #     if submit:
# #         start_dt = datetime.combine(date, start_time)
# #         end_dt = datetime.combine(date, end_time)

# #         if not name.strip():
# #             st.warning("⚠️ Please enter your name.")
# #         elif end_dt <= start_dt:
# #             st.warning("⚠️ End time must be after start time.")
# #         else:
# #             conflicts = bookings_df[
# #                 (bookings_df["Setup"] == setup) &
# #                 (
# #                     ((start_dt >= bookings_df["From"]) & (start_dt < bookings_df["To"])) |
# #                     ((end_dt > bookings_df["From"]) & (end_dt <= bookings_df["To"])) |
# #                     ((start_dt <= bookings_df["From"]) & (end_dt >= bookings_df["To"]))
# #                 )
# #             ]
# #             if not conflicts.empty:
# #                 st.error("❌ This setup is already booked during that time.")
# #                 time.sleep(2)  # Optional: Add a slight delay for user experience
# #                 st.rerun()
# #             else:
# #                 new_entry = pd.DataFrame([{
# #                     "Setup": setup,
# #                     "Name": name.strip(),
# #                     "From": start_dt,
# #                     "To": end_dt
# #                 }])
# #                 updated_df = pd.concat([bookings_df, new_entry], ignore_index=True)
# #                 updated_df.to_csv(BOOKINGS_FILE, index=False)
# #                 st.success(f"✅ {setup} booked from {start_dt.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')} on {date.strftime('%d %b %Y')} by {name}.")
# #                 time.sleep(2)  # Optional: Add a slight delay for user experience
# #                 st.rerun()

# # # --------- UPCOMING BOOKINGS ---------
# # st.header("📋 Current & Upcoming Bookings")
# # bookings_df = load_bookings()
# # now = datetime.now()
# # upcoming_df = bookings_df[bookings_df["To"] > now].sort_values(by="From")

# # if upcoming_df.empty:
# #     st.info("🟢 No upcoming bookings.")
# # else:
# #     st.dataframe(upcoming_df, use_container_width=True, hide_index=True)

# # # --------- UNBOOK A SETUP ---------
# # # st.subheader("❌ Cancel a Booking")
# # # if not bookings_df.empty:
# # #     # Create a unique label for each booking
# # #     bookings_df["Label"] = bookings_df.apply(
# # #         lambda row: f'{row["Setup"]} booked by {row["Name"]} from {row["From"].strftime("%Y-%m-%d %H:%M")} to {row["To"].strftime("%Y-%m-%d %H:%M")}',
# # #         axis=1
# # #     )
# # #     cancel_label = st.selectbox("Select booking to cancel", bookings_df["Label"].tolist())
    
# # #     with st.form("cancel_form"):
# # #         cancel_submit = st.form_submit_button("Cancel Booking")
# # #         if cancel_submit:
# # #             # Find the row matching the selected label
# # #             updated_df = bookings_df[bookings_df["Label"] != cancel_label].drop(columns=["Label"])
# # #             updated_df.to_csv(BOOKINGS_FILE, index=False)
# # #             st.success("✅ Booking cancelled successfully.")
# # #             time.sleep(2)
# # #             st.rerun()
# # # else:
# # #     st.info("ℹ️ No bookings found.")

# # # --------- UNBOOK A SETUP ---------
# # # st.header("❌ Cancel Your Booking")

# # # with st.form("unbook_form"):
# # #     unbook_name = st.text_input("Enter Your Name to View Your Bookings")
# # #     cancel_button = st.form_submit_button("🔍 Show My Bookings")

# # # if cancel_button:
# # #     bookings_df = load_bookings()
# # #     my_bookings = bookings_df[(bookings_df["Name"].str.lower() == unbook_name.strip().lower())]

# # #     if not my_bookings.empty:
# # #         selected_option = st.selectbox(
# # #             "Select a Booking to Cancel",
# # #             [
# # #                 f"{row['Setup']} | {row['From'].strftime('%d-%b %I:%M %p')} → {row['To'].strftime('%I:%M %p')}"
# # #                 for _, row in my_bookings.iterrows()
# # #             ]
# # #         )
# # #         confirm_cancel = st.button("❌ Cancel Selected Booking")

# # #         if confirm_cancel:
# # #             idx = [
# # #                 f"{row['Setup']} | {row['From'].strftime('%d-%b %I:%M %p')} → {row['To'].strftime('%I:%M %p')}"
# # #                 for _, row in my_bookings.iterrows()
# # #             ].index(selected_option)
# # #             booking_to_cancel = my_bookings.iloc[idx]

# # #             bookings_df = bookings_df[
# # #                 ~(
# # #                     (bookings_df["Setup"] == booking_to_cancel["Setup"]) &
# # #                     (bookings_df["From"] == booking_to_cancel["From"]) &
# # #                     (bookings_df["To"] == booking_to_cancel["To"]) &
# # #                     (bookings_df["Name"] == booking_to_cancel["Name"])
# # #                 )
# # #             ]
# # #             bookings_df.to_csv(BOOKINGS_FILE, index=False)
# # #             st.success("✅ Booking cancelled successfully.")
# # #             st.rerun()
# # #     else:
# # #         st.info("No bookings found under that name.")


# import streamlit as st
# import pandas as pd
# import json
# from datetime import datetime, timedelta, time
# import time as time_module
# from streamlit.components.v1 import html

# CSV_FILE = "bookings.csv"
# st.set_page_config(layout="wide")
# st.title("🔧 Setup Booking Tool")
# st.markdown("Book and manage shared setup reservations within your team.")

# # --- Ensure CSV Exists ---
# try:
#     df = pd.read_csv(CSV_FILE)
# except FileNotFoundError:
#     df = pd.DataFrame(columns=["id", "title", "setup", "start", "end"])
#     df.to_csv(CSV_FILE, index=False)

# # --- Load/Save Bookings ---
# def load_bookings():
#     return pd.read_csv(CSV_FILE)

# def save_booking(new_booking):
#     df = load_bookings()
#     df = pd.concat([df, pd.DataFrame([new_booking])], ignore_index=True)
#     df.to_csv(CSV_FILE, index=False)

# # --- Create Event JSON ---
# def create_event_data(df):
#     events = []
#     for _, row in df.iterrows():
#         events.append({
#             "title": row["title"],
#             "start": row["start"],
#             "end": row["end"],
#             "extendedProps": {
#                 "description": f"{row['title']} from {row['start']} - {row['end']}"
#             }
#         })
#     return events

# # --- Get booking slot from calendar click ---
# clicked_slot = st.query_params
# prefill_start = clicked_slot.get("start", [None])[0]
# prefill_end = clicked_slot.get("end", [None])[0]

# # --- Render FullCalendar ---
# df = load_bookings()
# events_json = json.dumps(create_event_data(df))

# calendar_code = f"""
# <div id='calendar'></div>
# <div id='tooltip' class='tooltip'></div>

# <script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.8/index.global.min.js'></script>
# <style>
#   #calendar {{
#     max-width: 1600px;
#     margin: 20px auto;
#     background-color: white;
#     color: black;
#     padding: 20px;
#     border-radius: 10px;
#   }}
#   .tooltip {{
#     position: absolute;
#     z-index: 10001;
#     background-color: #333;
#     color: #fff;
#     padding: 6px 10px;
#     border-radius: 5px;
#     font-size: 13px;
#     display: none;
#     white-space: nowrap;
#   }}
#   .fc-event:hover {{
#     cursor: pointer;
#   }}
# </style>

# <script>
# document.addEventListener('DOMContentLoaded', function() {{
#     var tooltip = document.getElementById('tooltip');
#     var calendarEl = document.getElementById('calendar');
#     var calendar = new FullCalendar.Calendar(calendarEl, {{
#         initialView: 'timeGridWeek',
#         selectable: true,
#         editable: false,
#         nowIndicator: true,
#         allDaySlot: false,
#         slotDuration: '00:15:00',
#         events: {events_json},
#         select: function(info) {{
#             const start = encodeURIComponent(info.startStr);
#             const end = encodeURIComponent(info.endStr);
#             window.location.search = '?start=' + start + '&end=' + end;
#         }},
#         eventDidMount: function(info) {{
#             info.el.addEventListener('mouseover', function(e) {{
#                 tooltip.innerHTML = info.event.extendedProps.description;
#                 tooltip.style.display = 'block';
#                 tooltip.style.left = e.pageX + 10 + 'px';
#                 tooltip.style.top = e.pageY + 10 + 'px';
#             }});
#             info.el.addEventListener('mousemove', function(e) {{
#                 tooltip.style.left = e.pageX + 10 + 'px';
#                 tooltip.style.top = e.pageY + 10 + 'px';
#             }});
#             info.el.addEventListener('mouseout', function() {{
#                 tooltip.style.display = 'none';
#             }});
#         }}
#     }});
#     calendar.render();
# }});
# </script>
# """

# # Display the calendar
# # html(calendar_code, height=1300)
# col1, col2 = st.columns([2, 1])  # Calendar takes 2/3, Form takes 1/3

# with col1:
#     html(calendar_code, height=1000)

# with col2:
#     st.header("📅 Book a Setup")


# # --------- BOOK A SETUP ---------
# # st.header("📅 Book a Setup")

#     SETUPS = ["Setup12", "Setup18", "Setup19", "Setup24", "Setup30", "Setup36", "Setup42", "Setup48"]
#     # Utility: Round up current time to next 15-minute interval
#     def next_15_min_interval():
#         now = datetime.now()
#         rounded = (now + timedelta(minutes=15)).replace(second=0, microsecond=0)
#         minutes_to_add = 15 - (rounded.minute % 15) if rounded.minute % 15 != 0 else 0
#         return (rounded + timedelta(minutes=minutes_to_add)).time()

#     with st.form("booking_form"):
#         name = st.text_input("Your Name", key="name")
#         setup = st.selectbox("Select Setup", SETUPS, key="setup_select")

#         date = st.date_input("Select Booking Date", value=datetime.now().date(), key="date")

#         # Time selection with 15-min intervals
#         default_time = next_15_min_interval()
#         time_options = [time(hour=h, minute=m) for h in range(24) for m in range(0, 60, 15)]

#         start_time = st.selectbox("From Time", time_options, index=time_options.index(default_time), key="start")
#         end_time = st.selectbox("To Time", time_options, index=min(len(time_options)-1, time_options.index(default_time)+4), key="end")

#         submit = st.form_submit_button("✅ Book Now")

#         if submit:
#             start_dt = datetime.combine(date, start_time)
#             end_dt = datetime.combine(date, end_time)

#             if not name.strip():
#                 st.warning("⚠️ Please enter your name.")
#             elif end_dt <= start_dt:
#                 st.warning("⚠️ End time must be after start time.")
#             else:
#                 df["start"] = pd.to_datetime(df["start"]).dt.floor("min")
#                 df["end"] = pd.to_datetime(df["end"]).dt.floor("min")
#                 conflicts = df[
#                     (df["setup"] == setup) &
#                     (
#                         ((start_dt >= df["start"]) & (start_dt < df["end"])) |
#                         ((end_dt > df["start"]) & (end_dt <= df["end"])) |
#                         ((start_dt <= df["start"]) & (end_dt >= df["end"]))
#                     )
#                 ]
#                 if not conflicts.empty:
#                     st.error("❌ This setup is already booked during that time.")
#                     time_module.sleep(2)  # Optional: Add a slight delay for user experience
#                     st.rerun()
#                 else:
#                     new_entry = pd.DataFrame([{
#                         "setup": setup,
#                         "title": name.strip()+" booked "+setup,
#                         "start": start_dt,
#                         "end": end_dt
#                     }])
#                     updated_df = pd.concat([df, new_entry], ignore_index=True)
#                     updated_df.to_csv(CSV_FILE, index=False)
#                     st.success(f"✅ {setup} booked from {start_dt.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')} on {date.strftime('%d %b %Y')} by {name}.")
#                     time_module.sleep(2)  # Optional: Add a slight delay for user experience
#                     st.rerun()
import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta, time
import time as time_module
from streamlit.components.v1 import html
import streamlit.components.v1 as components

import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# st.markdown(
#     """
#     <style>
#         body {
#             background-color: #FFFFFF;
#         }
#         .stApp {
#             background-color: #FDF5E6;
#         }
#         /* Card-like panel effect for forms and sidebar */
#         div[data-testid="stForm"] {
#             background-color: #f9f6f2;
#             padding: 20px;
#             margin: 15px 0;
#             border-radius: 12px;
#             border: 1px solid #c0b6ae;
#             box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#         }
#         label, .stTextInput > label, .stSelectbox > label, .stDateInput > label , .stHeader > h1, .stHeader > h2 {
#             color: #444444 !important;
#             font-weight: 500;
#         }
#         .form-label {
#             color: #333333;
#             font-size: 16px;
#             font-weight: 600;
#             margin-bottom: 8px;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )



CSV_FILE = "bookings.csv"
SETUPS_CSV_FILE = "vm_links.csv"
st.set_page_config(layout="wide")


image_path = "cisco.png"  # or your local PNG file
encoded_image = get_base64_image(image_path)

st.markdown(
    f"""
    <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 10px;">
        <div style="display: flex; flex-direction: column; align-items: center; padding: 20px 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <img src="data:image/png;base64,{encoded_image}" style="width:120px; height:70px; margin-bottom: 20px; ">
            <h1 style="margin: 0; color: #5DADE2; font-size: 50px;">Setup Booking Tool</h1>
            <p style="margin: 8px 0 0; color: #8B6F47; font-size: 16px; text-align: center;">
                Effortless booking and management of shared setups across Dev/QA.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Ensure CSV Exists ---
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=["id", "title", "setup", "start", "end"])
    df.to_csv(CSV_FILE, index=False)

try:
    setups_df = pd.read_csv(SETUPS_CSV_FILE)
except FileNotFoundError:
    setups_df = pd.DataFrame(columns=["setup", "url"])
    setups_df.to_csv(SETUPS_CSV_FILE, index=False)

# --- Load/Save Bookings ---
def load_bookings():
    return pd.read_csv(CSV_FILE)

def save_booking(new_booking):
    df = load_bookings()
    df = pd.concat([df, pd.DataFrame([new_booking])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# --- Create Event JSON ---
def create_event_data(df):
    events = []
    for _, row in df.iterrows():
        events.append({
            "title": row["title"],
            "start": row["start"],
            "end": row["end"],
            "extendedProps": {
                "description": f"{row['title']} from {row['start']} - {row['end']}"
            }
        })
    return events

# --- Get booking slot from calendar click ---
clicked_slot = st.query_params
prefill_start = clicked_slot.get("start", [None])[0]
prefill_end = clicked_slot.get("end", [None])[0]

# --- Render FullCalendar ---
df = load_bookings()
events_json = json.dumps(create_event_data(df))

calendar_code = f"""
<div id='calendar'></div>
<div id='tooltip' class='tooltip'></div>

<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.8/index.global.min.js'></script>
<style>
  #calendar {{
    max-width: 1600px;
    margin: 20px auto;
    background-color: white;
    color: black;
    padding: 20px;
    border-radius: 10px;
  }}
  .tooltip {{
    position: absolute;
    z-index: 10001;
    background-color: #333;
    color: #fff;
    padding: 6px 10px;
    border-radius: 5px;
    font-size: 13px;
    display: none;
    white-space: nowrap;
  }}
  .fc-event:hover {{
    cursor: pointer;
  }}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {{
    var tooltip = document.getElementById('tooltip');
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {{
        initialView: 'timeGridWeek',
        selectable: true,
        editable: false,
        nowIndicator: true,
        allDaySlot: false,
        slotDuration: '00:15:00',
        events: {events_json},
        select: function(info) {{
            const start = encodeURIComponent(info.startStr);
            const end = encodeURIComponent(info.endStr);
            window.location.search = '?start=' + start + '&end=' + end;
        }},
        eventDidMount: function(info) {{
            info.el.addEventListener('mouseover', function(e) {{
                tooltip.innerHTML = info.event.extendedProps.description;
                tooltip.style.display = 'block';
                tooltip.style.left = e.pageX + 10 + 'px';
                tooltip.style.top = e.pageY + 10 + 'px';
            }});
            info.el.addEventListener('mousemove', function(e) {{
                tooltip.style.left = e.pageX + 10 + 'px';
                tooltip.style.top = e.pageY + 10 + 'px';
            }});
            info.el.addEventListener('mouseout', function() {{
                tooltip.style.display = 'none';
            }});
        }}
    }});
    calendar.render();
}});
</script>
"""

col1, col2 = st.columns([2, 1])  # Calendar takes 2/3, Form takes 1/3

with col1:
    # Display the calendar
    html(calendar_code, height=1000)

with col2:
# --------- BOOK A SETUP ---------
    st.header("📅 Book a Setup")

    SETUPS = ["Setup12", "Setup18", "Setup19", "Setup24", "Setup30", "Setup36", "Setup42", "Setup48"]
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
                df["start"] = pd.to_datetime(df["start"]).dt.floor("min")
                df["end"] = pd.to_datetime(df["end"]).dt.floor("min")
                conflicts = df[
                    (df["setup"] == setup) &
                    (
                        ((start_dt >= df["start"]) & (start_dt < df["end"])) |
                        ((end_dt > df["start"]) & (end_dt <= df["end"])) |
                        ((start_dt <= df["start"]) & (end_dt >= df["end"]))
                    )
                ]
                if not conflicts.empty:
                    st.error("❌ This setup is already booked during that time.")
                    time_module.sleep(2)  # Optional: Add a slight delay for user experience
                    st.rerun()
                else:
                    new_entry = pd.DataFrame([{
                        "setup": setup,
                        "title": name.strip()+" booked "+setup,
                        "start": start_dt,
                        "end": end_dt
                    }])
                    updated_df = pd.concat([df, new_entry], ignore_index=True)
                    updated_df.to_csv(CSV_FILE, index=False)
                    st.success(f"✅ {setup} booked from {start_dt.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')} on {date.strftime('%d %b %Y')} by {name}.")
                    time_module.sleep(2)  # Optional: Add a slight delay for user experience
                    st.rerun()
    # --------- END BOOK A SETUP ---------
    # Load CSV
    vm_df = pd.read_csv(SETUPS_CSV_FILE)

    # Section Title
    st.markdown("---")
    st.subheader("🔗 View Setup Details")

    # Dropdown to select setup
    selected_vm = st.selectbox("Select a setup", vm_df["setup"])

    vm_url = vm_df.loc[vm_df["setup"] == selected_vm, "url"].values[0]
        
    if st.button("Open VM Details"):
        components.html(f"""<script>window.open("{vm_url}", "_blank")</script>""", height=0)
# --- End of app.py ---
