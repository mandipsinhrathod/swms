import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
from PIL import Image
import base64
from io import BytesIO
import time

# Configure page
st.set_page_config(
    page_title="Smart Waste Management - Bhavnagar",
    page_icon="🗑️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Multi-language support
LANGUAGES = {
    'English': {
        'title': 'Smart Waste Management System',
        'subtitle': 'Bhavnagar City - Gyanmanjari Innovative University',
        'login': 'Login',
        'register': 'Register',
        'dashboard': 'Dashboard',
        'schedule': 'Collection Schedule',
        'tracking': 'Live Tracking',
        'recycling': 'Recycling & Rewards',
        'ai_sorting': 'AI Waste Sorting',
        'admin': 'Admin Panel',
        'profile': 'Profile',
        'notifications': 'Notifications',
        'feedback': 'Feedback',
        'chatbot': 'Assistant',
        'waste_collected': 'Waste Collected Today',
        'points_earned': 'Points Earned',
        'recycling_rank': 'Recycling Rank',
        'next_pickup': 'Next Pickup',
        'report_missed': 'Report Missed Pickup',
        'request_service': 'Request Additional Service',
        'play_games': 'Play Games & Earn Points',
        'redeem_rewards': 'Redeem Rewards',
        'welcome': 'Welcome',
        'bronze': 'Bronze Recycler',
        'silver': 'Silver Recycler',
        'gold': 'Gold Recycler'
    },
    'Hindi': {
        'title': 'स्मार्ट कचरा प्रबंधन प्रणाली',
        'subtitle': 'भावनगर शहर - ज्ञानमंजरी इनोवेटिव विश्वविद्यालय',
        'login': 'लॉगिन',
        'register': 'पंजीकरण',
        'dashboard': 'डैशबोर्ड',
        'schedule': 'संग्रह समय सारणी',
        'tracking': 'लाइव ट्रैकिंग',
        'recycling': 'रीसाइक्लिंग और पुरस्कार',
        'ai_sorting': 'AI कचरा छंटाई',
        'admin': 'प्रशासक पैनल',
        'profile': 'प्रोफ़ाइल',
        'notifications': 'सूचनाएं',
        'feedback': 'प्रतिक्रिया',
        'chatbot': 'सहायक',
        'waste_collected': 'आज एकत्र कचरा',
        'points_earned': 'अर्जित अंक',
        'recycling_rank': 'रीसाइक्लिंग रैंक',
        'next_pickup': 'अगला पिकअप',
        'report_missed': 'छूटे पिकअप की रिपोर्ट',
        'request_service': 'अतिरिक्त सेवा का अनुरोध',
        'play_games': 'गेम खेलें और अंक कमाएं',
        'redeem_rewards': 'पुरस्कार भुनाएं',
        'welcome': 'स्वागत',
        'bronze': 'कांस्य रीसाइक्लर',
        'silver': 'रजत रीसाइक्लर',
        'gold': 'स्वर्ण रीसाइक्लर'
    },
    'Gujarati': {
        'title': 'સ્માર્ટ કચરો વ્યવસ્થાપન સિસ્ટમ',
        'subtitle': 'ભાવનગર શહેર - જ્ઞાનમંજરી ઇનોવેટિવ યુનિવર્સિટી',
        'login': 'લૉગિન',
        'register': 'નોંધણી',
        'dashboard': 'ડેશબોર્ડ',
        'schedule': 'કલેક્શન શેડ્યુલ',
        'tracking': 'લાઇવ ટ્રેકિંગ',
        'recycling': 'રિસાયક્લિંગ અને પુરસ્કારો',
        'ai_sorting': 'AI કચરો વિભાજન',
        'admin': 'એડમિન પેનલ',
        'profile': 'પ્રોફાઇલ',
        'notifications': 'સૂચનાઓ',
        'feedback': 'પ્રતિક્રિયા',
        'chatbot': 'સહાયક',
        'waste_collected': 'આજે એકત્ર કચરો',
        'points_earned': 'મેળવેલા પોઇન્ટ્સ',
        'recycling_rank': 'રિસાયક્લિંગ રેન્ક',
        'next_pickup': 'આગામી પિકઅપ',
        'report_missed': 'છૂટી ગયેલી પિકઅપની જાણ',
        'request_service': 'વધારાની સેવાની વિનંતી',
        'play_games': 'ગેમ્સ રમો અને પોઇન્ટ્સ કમાઓ',
        'redeem_rewards': 'પુરસ્કારો રિડીમ કરો',
        'welcome': 'સ્વાગત',
        'bronze': 'બ્રોન્ઝ રિસાયક્લર',
        'silver': 'સિલ્વર રિસાયક્લર',
        'gold': 'ગોલ્ડ રિસાયક્લર'
    }
}

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'notifications' not in st.session_state:
    st.session_state.notifications = []
if 'user_points' not in st.session_state:
    st.session_state.user_points = 150
if 'recycling_rank' not in st.session_state:
    st.session_state.recycling_rank = 'bronze'


# Custom CSS for modern UI
def load_css():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }

    .rank-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        color: white;
        margin: 0.5rem;
    }

    .bronze { background: linear-gradient(45deg, #CD7F32, #A0522D); }
    .silver { background: linear-gradient(45deg, #C0C0C0, #808080); }
    .gold { background: linear-gradient(45deg, #FFD700, #FFA500); }

    .game-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        cursor: pointer;
        transition: transform 0.3s ease;
    }

    .game-card:hover {
        transform: translateY(-5px);
    }

    .notification-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }

    .truck-marker {
        background: #28a745;
        color: white;
        padding: 0.5rem;
        border-radius: 50%;
        font-size: 1.2rem;
    }

    .bin-status {
        display: inline-block;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }

    .bin-empty { background: #28a745; }
    .bin-half { background: #ffc107; }
    .bin-full { background: #dc3545; }

    .chatbot-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }

    .reward-coupon {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #333;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        border: 2px dashed #ff6b6b;
    }
    </style>
    """, unsafe_allow_html=True)


def get_text(key):
    return LANGUAGES[st.session_state.language].get(key, key)


def create_header():
    st.markdown(f"""
    <div class="main-header">
        <h1>🗑️ {get_text('title')}</h1>
        <p>{get_text('subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)


def login_page():
    st.markdown("### 🔐 Login / Register")

    tab1, tab2 = st.tabs([get_text('login'), get_text('register')])

    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button(get_text('login'))

            if submit:
                if email and password:
                    st.session_state.logged_in = True
                    st.session_state.user_data = {
                        'name': email.split('@')[0].title(),
                        'email': email,
                        'phone': '+91 98765 43210',
                        'address': 'Bhavnagar, Gujarat',
                        'join_date': '2024-01-15'
                    }
                    st.rerun()
                else:
                    st.error("Please fill all fields")

    with tab2:
        with st.form("register_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            address = st.text_area("Address")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button(get_text('register'))

            if submit:
                if all([name, email, phone, address, password, confirm_password]):
                    if password == confirm_password:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Passwords don't match")
                else:
                    st.error("Please fill all fields")


def dashboard_page():
    st.markdown(f"## 🏠 {get_text('dashboard')}")

    # User greeting
    st.markdown(f"### {get_text('welcome')}, {st.session_state.user_data['name']}! 👋")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🗑️ {random.randint(5, 15)} kg</h3>
            <p>{get_text('waste_collected')}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⭐ {st.session_state.user_points}</h3>
            <p>{get_text('points_earned')}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        rank_class = st.session_state.recycling_rank
        rank_text = get_text(st.session_state.recycling_rank)
        st.markdown(f"""
        <div class="metric-card">
            <span class="rank-badge {rank_class}">{rank_text}</span>
            <p>{get_text('recycling_rank')}</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        next_pickup = datetime.now() + timedelta(days=2)
        st.markdown(f"""
        <div class="metric-card">
            <h3>📅 {next_pickup.strftime('%d/%m')}</h3>
            <p>{get_text('next_pickup')}</p>
        </div>
        """, unsafe_allow_html=True)

    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(f"📞 {get_text('report_missed')}", use_container_width=True):
            st.success("Missed pickup reported! Our team will contact you soon.")

    with col2:
        if st.button(f"➕ {get_text('request_service')}", use_container_width=True):
            st.success("Additional service requested! We'll schedule it for you.")

    with col3:
        if st.button(f"🎮 {get_text('play_games')}", use_container_width=True):
            st.session_state.show_games = True
            st.rerun()

    # Recent activity
    st.markdown("### 📊 Recent Activity")
    activity_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
        'Waste_Collected': np.random.randint(2, 15, 30),
        'Points_Earned': np.random.randint(5, 25, 30)
    })

    fig = px.line(activity_data, x='Date', y=['Waste_Collected', 'Points_Earned'],
                  title="Monthly Waste Collection & Points Trend")
    st.plotly_chart(fig, use_container_width=True)


def schedule_page():
    st.markdown(f"## 📅 {get_text('schedule')}")

    # Weekly schedule
    schedule_data = pd.DataFrame({
        'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'Organic': ['8:00 AM', '8:00 AM', '8:00 AM', '8:00 AM', '8:00 AM', '8:00 AM', 'Off'],
        'Recyclable': ['10:00 AM', 'Off', '10:00 AM', 'Off', '10:00 AM', 'Off', 'Off'],
        'Hazardous': ['Off', 'Off', 'Off', 'Off', 'Off', '2:00 PM', 'Off']
    })

    st.dataframe(schedule_data, use_container_width=True)

    # Smart bin status
    st.markdown("### 🗑️ Smart Bin Status")
    bin_data = pd.DataFrame({
        'Location': ['Gyanmanjari University', 'Takhteshwar Temple', 'Darbargadh', 'Bhavnagar Port', 'Nilambag Palace'],
        'Bin_ID': ['BIN001', 'BIN002', 'BIN003', 'BIN004', 'BIN005'],
        'Fill_Level': [25, 67, 89, 45, 23],
        'Status': ['Empty', 'Half', 'Full', 'Half', 'Empty']
    })

    for _, row in bin_data.iterrows():
        status_class = f"bin-{row['Status'].lower()}"
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 0.5rem; background: white; margin: 0.5rem 0; border-radius: 5px;">
            <span class="bin-status {status_class}"></span>
            <strong>{row['Location']}</strong> - {row['Bin_ID']} - {row['Fill_Level']}% full
        </div>
        """, unsafe_allow_html=True)


def tracking_page():
    st.markdown(f"## 🚛 {get_text('tracking')}")

    # Simulated truck locations
    truck_data = pd.DataFrame({
        'Truck_ID': ['TRK001', 'TRK002', 'TRK003', 'TRK004'],
        'Driver': ['Rajesh Patel', 'Amit Shah', 'Kiran Modi', 'Suresh Joshi'],
        'Location': ['Near Gyanmanjari University', 'Takhteshwar Temple Area', 'Darbargadh Circle', 'Bhavnagar Port'],
        'Status': ['Collecting', 'En Route', 'Collecting', 'Returning'],
        'ETA': ['15 min', '25 min', '10 min', '45 min'],
        'Lat': [21.7645, 21.7645, 21.7645, 21.7645],
        'Lon': [72.1519, 72.1519, 72.1519, 72.1519]
    })

    # Display truck information
    for _, truck in truck_data.iterrows():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🚛 Truck", truck['Truck_ID'])
        with col2:
            st.metric("👨‍✈️ Driver", truck['Driver'])
        with col3:
            st.metric("📍 Status", truck['Status'])
        with col4:
            st.metric("⏱️ ETA", truck['ETA'])

    # Map would go here (simulated)
    st.markdown("### 🗺️ Live Map")
    st.info("🗺️ Interactive map showing real-time truck locations would be displayed here with GPS integration.")


def recycling_page():
    st.markdown(f"## ♻️ {get_text('recycling')}")

    # User rank and points
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>⭐ {st.session_state.user_points} Points</h2>
            <span class="rank-badge {st.session_state.recycling_rank}">{get_text(st.session_state.recycling_rank)}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Progress to next rank
        progress = min(st.session_state.user_points / 200, 1.0)
        st.progress(progress)
        st.write(f"Progress to next rank: {int(progress * 100)}%")

    # Games section
    st.markdown("### 🎮 Earn Points Through Games")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="game-card">
            <h3>🧠 Recycling Quiz</h3>
            <p>Test your knowledge and earn 10-20 points!</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Play Quiz", key="quiz_btn"):
            play_quiz()

    with col2:
        st.markdown("""
        <div class="game-card">
            <h3>🎯 Lucky Spinner</h3>
            <p>Spin the wheel to win bonus points!</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Spin Wheel", key="spin_btn"):
            play_spinner()

    # Rewards section
    st.markdown("### 🎁 Redeem Rewards")

    rewards = [
        {"name": "₹10 Grocery Voucher", "points": 100, "desc": "Valid at local stores"},
        {"name": "₹25 Fuel Voucher", "points": 200, "desc": "Valid at any petrol pump"},
        {"name": "₹50 Shopping Voucher", "points": 350, "desc": "Valid at major retailers"},
        {"name": "Free Movie Ticket", "points": 150, "desc": "Valid at Bhavnagar cinemas"}
    ]

    for reward in rewards:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{reward['name']}**")
            st.write(reward['desc'])
        with col2:
            st.write(f"**{reward['points']} points**")
        with col3:
            if st.button(f"Redeem", key=f"redeem_{reward['name']}"):
                if st.session_state.user_points >= reward['points']:
                    st.session_state.user_points -= reward['points']
                    generate_coupon(reward['name'])
                    st.rerun()
                else:
                    st.error("Not enough points!")


def play_quiz():
    st.markdown("### 🧠 Recycling Quiz")

    questions = [
        {
            "question": "Which material takes the longest to decompose?",
            "options": ["Paper", "Plastic", "Glass", "Aluminum"],
            "correct": 2,
            "explanation": "Glass can take up to 1 million years to decompose!"
        },
        {
            "question": "What percentage of plastic waste is recycled globally?",
            "options": ["50%", "25%", "9%", "75%"],
            "correct": 2,
            "explanation": "Only about 9% of plastic waste is recycled globally."
        }
    ]

    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
        st.session_state.quiz_score = 0
        st.session_state.current_question = 0

    if not st.session_state.quiz_started:
        if st.button("Start Quiz"):
            st.session_state.quiz_started = True
            st.rerun()
    else:
        if st.session_state.current_question < len(questions):
            q = questions[st.session_state.current_question]
            st.write(f"**Question {st.session_state.current_question + 1}:** {q['question']}")

            answer = st.radio("Choose your answer:", q['options'], key=f"q_{st.session_state.current_question}")

            if st.button("Submit Answer"):
                if q['options'].index(answer) == q['correct']:
                    st.success("Correct! +10 points")
                    st.session_state.quiz_score += 10
                    st.session_state.user_points += 10
                else:
                    st.error(f"Wrong! {q['explanation']}")

                st.session_state.current_question += 1
                time.sleep(1)
                st.rerun()
        else:
            st.balloons()
            st.success(f"Quiz completed! You earned {st.session_state.quiz_score} points!")
            st.session_state.quiz_started = False
            st.session_state.current_question = 0
            st.session_state.quiz_score = 0


def play_spinner():
    st.markdown("### 🎯 Lucky Spinner")

    if st.button("🎯 SPIN THE WHEEL!", key="spin_action"):
        with st.spinner("Spinning..."):
            time.sleep(2)

        points_won = random.choice([5, 10, 15, 20, 25, 30])
        st.session_state.user_points += points_won

        st.balloons()
        st.success(f"🎉 You won {points_won} points!")
        st.rerun()


def generate_coupon(reward_name):
    coupon_code = f"WASTE{random.randint(1000, 9999)}"
    st.markdown(f"""
    <div class="reward-coupon">
        <h3>🎫 Reward Coupon</h3>
        <h4>{reward_name}</h4>
        <p><strong>Coupon Code: {coupon_code}</strong></p>
        <p>Valid until: {(datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y')}</p>
        <p>Present this coupon at participating outlets</p>
    </div>
    """, unsafe_allow_html=True)


def ai_sorting_page():
    st.markdown(f"## 🤖 {get_text('ai_sorting')}")

    st.markdown("### 📸 Upload Waste Image for AI Classification")

    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("🔍 Classify Waste"):
            with st.spinner("AI is analyzing your image..."):
                time.sleep(3)

            # Simulated AI classification
            waste_types = ["Organic", "Recyclable Plastic", "Glass", "Metal", "Paper", "Hazardous"]
            confidence_scores = [random.uniform(0.7, 0.99) for _ in waste_types]

            predicted_type = waste_types[confidence_scores.index(max(confidence_scores))]
            confidence = max(confidence_scores)

            st.success(f"🎯 Prediction: **{predicted_type}**")
            st.info(f"Confidence: {confidence:.2%}")

            # Recycling tips
            tips = {
                "Organic": "🌱 Compost this waste to create nutrient-rich soil!",
                "Recyclable Plastic": "♻️ Clean and put in recyclable bin. Remove caps and labels.",
                "Glass": "🥃 Rinse and recycle. Glass can be recycled indefinitely!",
                "Metal": "🔧 Metal is valuable! Clean and recycle for cash rewards.",
                "Paper": "📄 Keep dry and clean. Paper can be recycled 5-7 times.",
                "Hazardous": "⚠️ Take to special disposal center. Don't put in regular bins!"
            }

            st.markdown(f"### 💡 Recycling Tip")
            st.info(tips.get(predicted_type, "Follow local recycling guidelines."))

            # Award points
            st.session_state.user_points += 5
            st.success("🏆 You earned 5 points for using AI sorting!")


def admin_panel():
    st.markdown("## 👨‍💼 Admin Dashboard")

    # Admin metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Total Users", "1,247", "↗️ +23")
    with col2:
        st.metric("🚛 Active Trucks", "12", "↗️ +2")
    with col3:
        st.metric("🗑️ Waste Collected (Today)", "156 tons", "↗️ +12%")
    with col4:
        st.metric("♻️ Recycling Rate", "68%", "↗️ +5%")

    # Charts
    st.markdown("### 📊 Analytics")

    # Waste collection trend
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    waste_data = pd.DataFrame({
        'Date': dates,
        'Organic': np.random.randint(40, 80, 30),
        'Recyclable': np.random.randint(30, 60, 30),
        'Hazardous': np.random.randint(5, 15, 30)
    })

    fig = px.line(waste_data, x='Date', y=['Organic', 'Recyclable', 'Hazardous'],
                  title="Daily Waste Collection by Type")
    st.plotly_chart(fig, use_container_width=True)

    # User engagement
    engagement_data = pd.DataFrame({
        'Activity': ['App Opens', 'Reports Filed', 'Games Played', 'Rewards Redeemed', 'AI Classifications'],
        'Count': [1247, 89, 234, 67, 156]
    })

    fig2 = px.bar(engagement_data, x='Activity', y='Count', title="User Engagement Metrics")
    st.plotly_chart(fig2, use_container_width=True)

    # Recent reports
    st.markdown("### 📋 Recent Reports")
    reports_data = pd.DataFrame({
        'User': ['Rajesh P.', 'Priya S.', 'Amit K.', 'Neha J.', 'Kiran M.'],
        'Issue': ['Missed Pickup', 'Bin Overflow', 'Additional Service', 'Damaged Bin', 'Schedule Change'],
        'Status': ['Resolved', 'In Progress', 'Pending', 'Resolved', 'In Progress'],
        'Date': ['2024-07-10', '2024-07-10', '2024-07-09', '2024-07-09', '2024-07-08']
    })
    st.dataframe(reports_data, use_container_width=True)


def profile_page():
    st.markdown(f"## 👤 {get_text('profile')}")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Profile Picture")
        uploaded_file = st.file_uploader("Upload Profile Picture", type=['jpg', 'jpeg', 'png'])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, width=200)
        else:
            st.markdown("👤", unsafe_allow_html=True)

    with col2:
        st.markdown("### Personal Information")
        with st.form("profile_form"):
            name = st.text_input("Name", value=st.session_state.user_data.get('name', ''))
            email = st.text_input("Email", value=st.session_state.user_data.get('email', ''))
            phone = st.text_input("Phone", value=st.session_state.user_data.get('phone', ''))
            address = st.text_area("Address", value=st.session_state.user_data.get('address', ''))

            if st.form_submit_button("Update Profile"):
                st.session_state.user_data.update({
                    'name': name, 'email': email, 'phone': phone, 'address': address
                })
                st.success("Profile updated successfully!")

    # Statistics
    st.markdown("### 📊 Your Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Points", st.session_state.user_points)
    with col2:
        st.metric("Waste Recycled", "45.2 kg")
    with col3:
        st.metric("Carbon Saved", "12.3 kg CO₂")


def notifications_page():
    st.markdown(f"## 🔔 {get_text('notifications')}")

    # Add sample notifications if empty
    if not st.session_state.notifications:
        st.session_state.notifications = [
            {"title": "Pickup Scheduled", "message": "Your waste pickup is scheduled for tomorrow at 8:00 AM",
             "time": "2 hours ago", "type": "info"},
            {"title": "Points Earned", "message": "You earned 15 points for recycling!", "time": "1 day ago",
             "type": "success"},
            {"title": "New Reward Available", "message": "You can now redeem a ₹25 voucher!", "time": "2 days ago",
             "type": "reward"},
            {"title": "Bin Full Alert", "message": "Bin near your location is 90% full", "time": "3 days ago",
             "type": "warning"}
        ]

    # Display notifications
    for notification in st.session_state.notifications:
        icon = {"info": "ℹ️", "success": "✅", "reward": "🎁", "warning": "⚠️"}
        st.markdown(f"""
        <div class="notification-item">
            <strong>{icon.get(notification['type'], '📢')} {notification['title']}</strong><br>
            {notification['message']}<br>
            <small style="color: #666;">{notification['time']}</small>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Clear All Notifications"):
        st.session_state.notifications = []
        st.rerun()


def feedback_page():
    st.markdown(f"## 📝 {get_text('feedback')}")

    st.markdown("### Rate Our Service")
    rating = st.slider("Overall Rating", 1, 5, 4)

    # Star display
    stars = "⭐" * rating + "☆" * (5 - rating)
    st.markdown(f"**{stars}**")

    # Feedback categories
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Service Quality")
        pickup_rating = st.slider("Pickup Timeliness", 1, 5, 4)
        driver_rating = st.slider("Driver Courtesy", 1, 5, 5)
        app_rating = st.slider("App Experience", 1, 5, 4)

    with col2:
        st.markdown("### Suggestions")
        feedback_text = st.text_area("Your Feedback", height=150)
        category = st.selectbox("Feedback Category",
                                ["General", "Pickup Service", "App Issues", "Billing", "Other"])

    if st.button("Submit Feedback"):
        st.balloons()
        st.success("Thank you for your feedback! We'll use it to improve our service.")
        # Award points for feedback
        st.session_state.user_points += 10
        st.info("You earned 10 points for providing feedback!")


def chatbot_page():
    st.markdown(f"## 🤖 {get_text('chatbot')}")

    st.markdown("""
    <div class="chatbot-container">
        <h3>🤖 WasteBot Assistant</h3>
        <p>Hello! I'm here to help you with waste management queries.</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**🤖 WasteBot:** {message['content']}")

    # Chat input
    user_input = st.text_input("Ask me anything about waste management:")

    if st.button("Send") and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Simple chatbot responses
        responses = {
            "pickup": "Your next pickup is scheduled for tomorrow at 8:00 AM. You can track the truck live in the tracking section.",
            "points": f"You currently have {st.session_state.user_points} points. Play games or use AI sorting to earn more!",
            "recycling": "Great question! Separate your waste into organic, recyclable, and hazardous categories. Use our AI sorting feature for help!",
            "rewards": "You can redeem rewards with your points! Check the Recycling & Rewards section for available options.",
            "schedule": "Waste collection happens Monday to Saturday. Organic waste is collected daily, recyclables on alternate days.",
            "default": "I'm here to help! You can ask me about pickup schedules, recycling tips, points, rewards, or waste sorting."
        }

        response = responses.get("default", responses["default"])
        for key in responses:
            if key in user_input.lower():
                response = responses[key]
                break

        st.session_state.chat_history.append({"role": "bot", "content": response})
        st.rerun()


def settings_page():
    st.markdown("## ⚙️ Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌐 Language")
        language = st.selectbox("Select Language", list(LANGUAGES.keys()),
                                index=list(LANGUAGES.keys()).index(st.session_state.language))
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()

    with col2:
        st.markdown("### 🎨 Theme")
        theme = st.selectbox("Select Theme", ["Light", "Dark"],
                             index=0 if st.session_state.theme == 'light' else 1)
        if theme.lower() != st.session_state.theme:
            st.session_state.theme = theme.lower()
            st.rerun()

    st.markdown("### 🔔 Notification Preferences")
    st.checkbox("Pickup Reminders", value=True)
    st.checkbox("Point Notifications", value=True)
    st.checkbox("Reward Alerts", value=True)
    st.checkbox("App Updates", value=False)

    st.markdown("### 📊 Data & Privacy")
    if st.button("Download My Data"):
        st.info("Your data export will be sent to your email address.")

    if st.button("Delete Account"):
        st.error("Are you sure? This action cannot be undone.")


def main():
    load_css()

    # Language selector in sidebar
    with st.sidebar:
        st.selectbox("🌐 Language", list(LANGUAGES.keys()),
                     key="language", index=list(LANGUAGES.keys()).index(st.session_state.language))

    # Theme toggle
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
        .stApp { background-color: #1e1e1e; color: white; }
        .metric-card { background-color: #2d2d2d; color: white; }
        </style>
        """, unsafe_allow_html=True)

    if not st.session_state.logged_in:
        create_header()
        login_page()
    else:
        create_header()

        # Navigation
        with st.sidebar:
            st.markdown(f"### {get_text('welcome')}, {st.session_state.user_data['name']}!")

            # Theme toggle
            if st.button("🌓 Toggle Theme"):
                st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
                st.rerun()

            # Navigation menu
            page = st.selectbox("Navigate", [
                get_text('dashboard'),
                get_text('schedule'),
                get_text('tracking'),
                get_text('recycling'),
                get_text('ai_sorting'),
                get_text('admin'),
                get_text('profile'),
                get_text('notifications'),
                get_text('feedback'),
                get_text('chatbot'),
                "Settings"
            ])

            # Logout
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.rerun()

        # Page routing
        if page == get_text('dashboard'):
            dashboard_page()
        elif page == get_text('schedule'):
            schedule_page()
        elif page == get_text('tracking'):
            tracking_page()
        elif page == get_text('recycling'):
            recycling_page()
        elif page == get_text('ai_sorting'):
            ai_sorting_page()
        elif page == get_text('admin'):
            admin_panel()
        elif page == get_text('profile'):
            profile_page()
        elif page == get_text('notifications'):
            notifications_page()
        elif page == get_text('feedback'):
            feedback_page()
        elif page == get_text('chatbot'):
            chatbot_page()
        elif page == "Settings":
            settings_page()


if __name__ == "__main__":
    main()