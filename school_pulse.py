import streamlit as st
import pandas as pd
import base64
from datetime import datetime

st.set_page_config(
    page_title="School Pulse",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- Teacher names and passwords ----------------
TEACHERS = [
    "sreevani", "umarani", "poojitha", "kanaka durga", "murugun",
    "pavani", "sai ram", "satya rao", "bagya lakshmi", "kalyani",
    "abin", "anoienter", "naga jyothi", "sudheshna", "srujana",
    "ravi kumar", "ruma", "sneha", "allen", "sravan",
    "b lakshmi", "sridevi", "aruna", "sirisha", "gokul",
    "imna", "L jyothi", "payal", "varsha", "anuja",
    "Bv lakshmi", "ravi", "renuka", "koteswararao", "gopi chand",
    "tirumaleswara rao", "shiva", "bhanu"
]

TEACHER_PASSWORDS = {
    teacher: f"t{i + 1}098"
    for i, teacher in enumerate(TEACHERS)
}

ADMIN_PASSWORDS = {
    "Admin 1": "a1d2m3i4n5",
    "Admin 2": "a2d3m4i5n6",
    "Admin 3": "a3d4m5i6n7"
}

DIRECTOR_PASSWORD = "director@123098"

# ---------------- Session state ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = ""
if "teacher_name" not in st.session_state:
    st.session_state.teacher_name = ""
if "admin_name" not in st.session_state:
    st.session_state.admin_name = ""
if "records" not in st.session_state:
    st.session_state.records = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

# ---------------- Background and styling ----------------
def set_background(color1, color2):
    css = f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, {color1}, {color2});
        background-attachment: fixed;
    }}

    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    .login-card {{
        background: rgba(255, 255, 255, 0.96);
        padding: 35px 40px;
        border-radius: 25px;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.25);
        max-width: 520px;
        margin: auto;
    }}

    .school-title {{
        font-size: 60px;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        text-shadow: 3px 4px 12px rgba(0, 0, 0, 0.55);
        margin-bottom: 8px;
    }}

    .school-subtitle {{
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        text-shadow: 2px 3px 8px rgba(0, 0, 0, 0.55);
        margin-bottom: 30px;
    }}

    .red-label {{
        color: #d40000;
        font-weight: 900;
        font-size: 20px;
        margin-bottom: 5px;
    }}

    .role-title {{
        font-size: 48px;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        text-shadow: 3px 4px 10px rgba(0, 0, 0, 0.55);
        margin-bottom: 20px;
    }}

    .director-title {{
        font-size: 58px;
        font-weight: 900;
        color: #ffe600;
        font-family: 'Brush Script MT', cursive;
        text-align: center;
        text-shadow: 3px 4px 12px rgba(0, 0, 0, 0.65);
        margin-bottom: 25px;
    }}

    .bright-heading {{
        font-size: 30px;
        font-weight: 900;
        color: #ffffff;
        background: linear-gradient(90deg, #ff0066, #ff8a00);
        padding: 14px 22px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 18px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.30);
    }}

    .dark-stat {{
        font-size: 28px;
        font-weight: 900;
        color: #111111;
        background: #ffffff;
        padding: 18px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
    }}

    .teacher-card {{
        background: rgba(255, 255, 255, 0.96);
        border-radius: 22px;
        padding: 25px;
        box-shadow: 0 14px 35px rgba(0, 0, 0, 0.25);
        margin-bottom: 22px;
    }}

    .stButton > button {{
        width: 100%;
        font-weight: 800;
        border-radius: 12px;
        padding: 13px;
        font-size: 17px;
    }}

    .stTextInput input, .stTextArea textarea {{
        border-radius: 10px;
        font-size: 16px;
    }}

    .stSelectbox > div > div {{
        border-radius: 10px;
        font-size: 16px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---------------- Login screen ----------------
def login_screen():
    set_background("#1e3c72", "#2a5298")

    st.markdown('<div class="school-title">🏫 School Pulse</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="school-subtitle">Student Problem Solving and Performance System</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="red-label">LOGIN</div>', unsafe_allow_html=True)

    role = st.selectbox(
        "Select Role",
        ["Teacher", "Director", "Admin"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="red-label">Select Teacher</div>', unsafe_allow_html=True)

    teacher_name = ""
    admin_name = ""

    if role == "Teacher":
        teacher_name = st.selectbox(
            "Teacher Name",
            TEACHERS,
            label_visibility="collapsed"
        )
    elif role == "Admin":
        admin_name = st.selectbox(
            "Admin Name",
            list(ADMIN_PASSWORDS.keys()),
            label_visibility="collapsed"
        )

    st.markdown('<div class="red-label">Password</div>', unsafe_allow_html=True)
    password = st.text_input("Password", type="password", label_visibility="collapsed")

    if st.button("LOGIN", use_container_width=True):
        if role == "Teacher":
            if password == TEACHER_PASSWORDS[teacher_name]:
                st.session_state.logged_in = True
                st.session_state.role = "Teacher"
                st.session_state.teacher_name = teacher_name
                st.rerun()
            else:
                st.error("Invalid teacher password. Please enter the password assigned to your name.")
        elif role == "Director":
            if password == DIRECTOR_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.role = "Director"
                st.rerun()
            else:
                st.error("Invalid Director password. Please enter: director@123098")
        else:
            if password == ADMIN_PASSWORDS[admin_name]:
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.session_state.admin_name = admin_name
                st.rerun()
            else:
                st.error("Invalid admin password.")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Teacher screen ----------------
def teacher_screen():
    set_background("#f6d365", "#fda085")

    st.markdown('<div class="role-title">👩‍🏫 Teacher Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="bright-heading">Welcome, {st.session_state.teacher_name}</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="bright-heading">Submit Student Problem / Help Provided</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="teacher-card">', unsafe_allow_html=True)

        problem = st.text_area(
            "Describe the student problem or the help you provided",
            height=150
        )

        photo = st.file_uploader(
            "Upload photo proof",
            type=["jpg", "jpeg", "png"]
        )

        if st.button("SUBMIT", use_container_width=True):
            if problem.strip() == "":
                st.error("Please write what help you provided.")
            else:
                photo_data = None
                if photo is not None:
                    photo_data = base64.b64encode(photo.getvalue()).decode()

                st.session_state.records.append({
                    "id": st.session_state.next_id,
                    "teacher": st.session_state.teacher_name,
                    "problem": problem,
                    "photo": photo_data,
                    "status": "Pending",
                    "director_message": "",
                    "coins": 0,
                    "time": datetime.now().strftime("%d-%m-%Y %I:%M %p")
                })
                st.session_state.next_id += 1
                st.success("Your submission was sent to the Director.")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="bright-heading">My Submissions, Feedback and Coins</div>', unsafe_allow_html=True)

    my_records = [
        record for record in st.session_state.records
        if record["teacher"] == st.session_state.teacher_name
    ]

    if not my_records:
        st.info("You have not submitted any student problems yet.")
    else:
        for record in reversed(my_records):
            with st.container():
                st.markdown('<div class="teacher-card">', unsafe_allow_html=True)

                st.markdown(f"**Submission ID:** {record['id']}")
                st.markdown(f"**Date and time:** {record['time']}")
                st.markdown(f"**Help provided:** {record['problem']}")
                st.markdown(f"**Status:** {record['status']}")
                st.markdown(f"**Coins:** {record['coins']}")

                if record["photo"]:
                    st.image(
                        base64.b64decode(record["photo"]),
                        caption="Photo proof",
                        use_container_width=True
                    )

                if record["director_message"]:
                    st.success(f"Director feedback: {record['director_message']}")

                st.markdown('</div>', unsafe_allow_html=True)

    if st.button("LOGOUT", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.role = ""
        st.session_state.teacher_name = ""
        st.rerun()

# ---------------- Director screen ----------------
def director_screen():
    set_background("#0f2027", "#2c5364")

    st.markdown('<div class="director-title">Director Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="bright-heading">Welcome Director. You can review teacher help, photos, and award coins.</div>',
        unsafe_allow_html=True
    )

    total = len(st.session_state.records)
    solved = len([record for record in st.session_state.records if record["status"] == "Solved"])
    pending = len([record for record in st.session_state.records if record["status"] == "Pending"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="dark-stat">Total Problems<br>{total}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="dark-stat">Solved Problems<br>{solved}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="dark-stat">Pending Problems<br>{pending}</div>', unsafe_allow_html=True)

    st.markdown('<div class="bright-heading">Problems Graph</div>', unsafe_allow_html=True)

    if total == 0:
        st.info("No teacher submissions are available yet.")
    else:
        graph_data = pd.DataFrame({
            "Status": ["Solved Problems", "Pending Problems"],
            "Number": [solved, pending]
        })
        st.bar_chart(graph_data.set_index("Status"))

    st.markdown('<div class="bright-heading">Teacher Proof and Complaints</div>', unsafe_allow_html=True)

    if not st.session_state.records:
        st.info("No teacher submissions yet.")
    else:
        for record in reversed(st.session_state.records):
            with st.container():
                st.markdown('<div class="teacher-card">', unsafe_allow_html=True)

                st.markdown(f"### Teacher: {record['teacher']}")
                st.markdown(f"**Submission ID:** {record['id']}")
                st.markdown(f"**Date and time:** {record['time']}")
                st.markdown(f"**Help provided:** {record['problem']}")
                st.markdown(f"**Current status:** {record['status']}")
                st.markdown(f"**Coins awarded:** {record['coins']}")

                if record["photo"]:
                    st.image(
                        base64.b64decode(record["photo"]),
                        caption="Photo proof",
                        use_container_width=True
                    )
                else:
                    st.warning("No photo proof uploaded.")

                new_message = st.text_area(
                    f"Director feedback for Submission {record['id']}",
                    value=record["director_message"],
                    key=f"message_{record['id']}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("Mark Solved", key=f"solved_{record['id']}"):
                        record["status"] = "Solved"
                        record["director_message"] = new_message
                        record["coins"] += 1
                        st.success("Marked as solved and 1 coin awarded.")
                        st.rerun()

                with col2:
                    if st.button("Keep Pending", key=f"pending_{record['id']}"):
                        record["status"] = "Pending"
                        record["director_message"] = new_message
                        st.success("Submission kept pending.")
                        st.rerun()

                with col3:
                    if st.button("Send Red Warning", key=f"warning_{record['id']}"):
                        record["status"] = "Pending"
                        record["director_message"] = "RED WARNING: Please improve the student problem-solving work."
                        st.error("Red warning sent to the teacher.")
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="bright-heading">Teacher Leaderboard</div>', unsafe_allow_html=True)

    if not st.session_state.records:
        st.info("No coins have been awarded yet.")
    else:
        leaderboard = {}

        for record in st.session_state.records:
            leaderboard[record["teacher"]] = leaderboard.get(record["teacher"], 0) + record["coins"]

        leaderboard_df = pd.DataFrame(
            sorted(leaderboard.items(), key=lambda item: item[1], reverse=True),
            columns=["Teacher Name", "Coins"]
        )

        st.dataframe(leaderboard_df, use_container_width=True)

    if st.button("LOGOUT", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.role = ""
        st.rerun()

# ---------------- Admin screen ----------------
def admin_screen():
    set_background("#4b6cb7", "#182848")

    st.markdown('<div class="role-title">🛡️ Admin Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="bright-heading">Welcome, {st.session_state.admin_name}</div>',
        unsafe_allow_html=True
    )

    total = len(st.session_state.records)
    solved = len([record for record in st.session_state.records if record["status"] == "Solved"])
    pending = len([record for record in st.session_state.records if record["status"] == "Pending"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="dark-stat">Total Problems<br>{total}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="dark-stat">Solved Problems<br>{solved}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="dark-stat">Pending Problems<br>{pending}</div>', unsafe_allow_html=True)

    st.markdown('<div class="bright-heading">Teacher Proof and Complaints</div>', unsafe_allow_html=True)

    if not st.session_state.records:
        st.info("No teacher submissions yet.")
    else:
        for record in reversed(st.session_state.records):
            with st.container():
                st.markdown('<div class="teacher-card">', unsafe_allow_html=True)

                st.markdown(f"### Teacher: {record['teacher']}")
                st.markdown(f"**Submission ID:** {record['id']}")
                st.markdown(f"**Date and time:** {record['time']}")
                st.markdown(f"**Help provided:** {record['problem']}")
                st.markdown(f"**Status:** {record['status']}")
                st.markdown(f"**Coins awarded:** {record['coins']}")

                if record["photo"]:
                    st.image(
                        base64.b64decode(record["photo"]),
                        caption="Photo proof",
                        use_container_width=True
                    )
                else:
                    st.warning("No photo proof uploaded.")

                st.markdown('</div>', unsafe_allow_html=True)

    if st.button("LOGOUT", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.role = ""
        st.session_state.admin_name = ""
        st.rerun()

# ---------------- Main app ----------------
if not st.session_state.logged_in:
    login_screen()
elif st.session_state.role == "Teacher":
    teacher_screen()
elif st.session_state.role == "Director":
    director_screen()
else:
    admin_screen()
