import streamlit as st
import datetime

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="First Nutrition Expert",
    page_icon="🍏",
    layout="centered"
)

# --- تنسيق التصميم (CSS) ---
st.markdown("""
<style>
    /* استيراد خط تجوال العربي */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    .stApp { direction: rtl; text-align: right; font-family: 'Tajawal', sans-serif; }
    
    /* إخفاء العناصر عند الطباعة */
    @media print {
        .stButton, .stSelectbox, .stNumberInput, header, footer, .no-print { display: none !important; }
        .report-container { border: none !important; box-shadow: none !important; }
    }
    
    /* تصميم بطاقة التقرير */
    .report-container {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #2E8B57;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .header-box { text-align: center; border-bottom: 2px solid #f0f0f0; padding-bottom: 15px; margin-bottom: 20px; }
    .client-title { font-size: 22px; color: #2E8B57; font-weight: bold; margin: 10px 0; }
    
    /* صناديق الأرقام */
    .stat-grid { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; }
    .stat-box { 
        flex: 1; 
        background: #f8fff8; 
        padding: 15px; 
        border-radius: 10px; 
        text-align: center; 
        border: 1px solid #dcdcdc;
    }
    .stat-val { font-size: 20px; font-weight: bold; color: #2E8B57; display: block; }
    .stat-label { font-size: 14px; color: #555; }
    
    /* الجداول */
    .styled-table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; }
    .styled-table th { background-color: #2E8B57; color: white; padding: 10px; border: 1px solid #2E8B57; }
    .styled-table td { border: 1px solid #ddd; padding: 10px; text-align: center; }
    
    /* السوشيال ميديا */
    .social-icons { display: flex; justify-content: center; gap: 15px; margin-top: 25px; }
    .social-icons img { width: 35px; transition: 0.3s; }
    .social-icons img:hover { transform: scale(1.1); }
</style>
""", unsafe_allow_html=True)

# --- الشعار ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png", use_container_width=True)

st.markdown("<h3 style='text-align: center; color: #2E8B57;'>نظام تحليل الجسم والتغذية</h3>", unsafe_allow_html=True)

# --- قسم إدخال البيانات ---
with st.expander("📝 إدخال بيانات العميل (اضغط هنا)", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        title = st.selectbox("اللقب", ["السيد", "السيدة", "الكابتن", "الآنسة"])
        name = st.text_input("الاسم", "زائر")
    with c2:
        gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
        age = st.number_input("العمر", 10, 100, 30)

    c3, c4 = st.columns(2)
    with c3: weight = st.number_input("الوزن (KG)", 30.0, 200.0, 80.0)
    with c4: height = st.number_input("الطول (CM)", 100.0, 250.0, 180.0)

    activity_map = {"خامل (1.2)": 1.2, "نشاط خفيف (1.375)": 1.375, "نشاط متوسط (1.55)": 1.55, "نشيط جداً (1.725)": 1.725}
    activity = st.selectbox("مستوى النشاط", list(activity_map.keys()))
    
    goal_map = {"إنقاص الوزن": "loss", "محافظة": "maintain", "زيادة الوزن": "gain"}
    goal = st.selectbox("الهدف", list(goal_map.keys()))

    calculate = st.button("تحليل وإصدار التقرير 📊")

# --- العمليات الحسابية ---
if calculate:
    # 1. BMR & TDEE
    if gender == "ذكر":
        bmr = (9.99 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (9.99 * weight) + (6.25 * height) - (5 * age) - 161
    
    tdee = bmr * activity_map[activity]
    
    # 2. BMI
    bmi = weight / ((height/100) ** 2)
    if bmi < 18.5: bmi_status, bmi_color = "نحافة", "#3498db"
    elif 18.5 <= bmi < 24.9: bmi_status, bmi_color = "وزن مثالي ✅", "#2ecc71"
    elif 25 <= bmi < 29.9: bmi_status, bmi_color = "زيادة وزن", "#f1c40f"
    else: bmi_status, bmi_color = "سمنة ⚠️", "#e74c3c"

    # 3. الماء والسعرات
    water = (weight * 33) / 1000
    
    target_cal = tdee
    if goal_map[goal] == "loss":
        target_cal -= 500
        macros = {"p": 0.40, "c": 0.30, "f": 0.30}
        rec_supps = "ISO-100, L-Carnitine, Multivitamin"
    elif goal_map[goal] == "gain":
        target_cal += 500
        macros = {"p": 0.30, "c": 0.50, "f": 0.20}
        rec_supps = "Mass Gainer, Creatine, Pre-Workout"
    else:
        macros = {"p": 0.30, "c": 0.40, "f": 0.30}
        rec_supps = "Whey Protein, Omega-3"

    p_g = int((target_cal * macros["p"]) / 4)
    c_g = int((target_cal * macros["c"]) / 4)
    f_g = int((target_cal * macros["f"]) / 9)

    # --- عرض التقرير (HTML جاهز) ---
    st.markdown("---")
    
    html_report = f"""
    <div class="report-container">
        <div class="header-box">
            <h3>First Nutrition Report</h3>
            <p>التاريخ: {datetime.date.today()}</p>
            <div class="client-title">العميل: {title} {name}</div>
        </div>

        <h4 style="color:#2E8B57;">1️⃣ مؤشرات الجسم (Body Stats)</h4>
        <div class="stat-grid">
            <div class="stat-box">
                <span class="stat-label">مؤشر الكتلة (BMI)</span><br>
                <span class="stat-val" style="color: {bmi_color};">{round(bmi, 1)}</span>
                <small>{bmi_status}</small>
            </div>
            <div class="stat-box">
                <span class="stat-label">الاحتياج اليومي</span><br>
                <span class="stat-val">{int(target_cal)}</span>
                <small>سعرة حرارية</small>
            </div>
            <div class="stat-box">
                <span class="stat-label">احتياج الماء</span><br>
                <span class="stat-val" style="color: #3498db;">{round(water, 1)}</span>
                <small>لتر</small>
            </div>
        </div>

        <h4 style="color:#2E8B57;">2️⃣ تقسيم الماكروز (Macros)</h4>
        <div class="stat-grid">
            <div class="stat-box" style="border-color: #ffcccc;">
                🥩 بروتين<br><span class="stat-val">{p_g}g</span>
            </div>
            <div class="stat-box" style="border-color: #ffffcc;">
                🍞 كارب<br><span class="stat-val">{c_g}g</span>
            </div>
            <div class="stat-box" style="border-color: #ccffcc;">
                🥑 دهون<br><span class="stat-val">{f_g}g</span>
            </div>
        </div>

        <h4 style="color:#2E8B57;">3️⃣ التوصيات والمصادر</h4>
        <table class="styled-table">
            <tr>
                <th>العنصر</th>
                <th>مصادر طبيعية مقترحة</th>
                <th>مكملات First Nutrition</th>
            </tr>
            <tr>
                <td><b>البروتين</b></td>
                <td>دجاج، سمك، لحم، بيض</td>
                <td>{rec_supps.split(',')[0]}</td>
            </tr>
            <tr>
                <td><b>الكاربوهيدرات</b></td>
                <td>أرز، بطاطا، شوفان، فواكه</td>
                <td>Vitargo / Carb Powder</td>
            </tr>
            <tr>
                <td><b>الدهون</b></td>
                <td>زيت زيتون، مكسرات، أفوكادو</td>
                <td>Omega-3</td>
            </tr>
        </table>
        
        <div style="margin-top: 20px; padding: 15px; background: #fff3cd; border-radius: 8px;">
            <b>💊 التوصية الخاصة:</b> ننصح باستخدام المجموعة التالية لتحقيق هدفك:<br>
            <span style="color: #d35400; font-weight: bold;">{rec_supps}</span>
        </div>

        <hr style="margin-top: 30px;">
        <div style="text-align: center; font-size: 12px; color: #777;">
            © 2026 First Nutrition - Expert System
        </div>
    </div>
    """
    
    st.markdown(html_report, unsafe_allow_html=True)
    st.success("✅ تم إصدار التقرير بنجاح! يمكنك طباعته الآن (Ctrl+P).")

# --- الفوتر ---
st.markdown("---")
st.markdown("""
<div class="social-icons">
    <a href="https://www.facebook.com/firstnutritionjordan/" target="_blank"><img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/firstnutritionjordan-1-FB-.png"></a>
    <a href="https://www.instagram.com/firstnutritionjo/" target="_blank"><img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/firstnutritionjordan-2-INSTA.png"></a>
    <a href="https://www.firstnutrition.com" target="_blank"><img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/firstnutritionjordan-5-WEB-1.png"></a>
</div>
""", unsafe_allow_html=True)
