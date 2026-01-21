import streamlit as st
import datetime
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="First Nutrition App",
    page_icon="🍏",
    layout="centered"
)

# --- 2. التصميم (CSS) ---
# ملاحظة: تم وضع CSS في متغير لضمان عدم تكسر الكود
css_style = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    .stApp {
        direction: rtl;
        text-align: right;
        font-family: 'Tajawal', sans-serif;
    }

    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .logo-container img {
        width: 150px;
    }

    /* إعدادات الطباعة */
    @media print {
        body, .stApp, .block-container {
            visibility: visible !important;
            height: auto !important;
            overflow: visible !important;
            display: block !important;
        }
        header, footer, .no-print, .stButton, button {
            display: none !important;
        }
        .report-box {
            border: 2px solid #2E8B57 !important;
            padding: 20px !important;
            margin: 0 !important;
            width: 100% !important;
            box-shadow: none !important;
        }
    }

    .report-box {
        border: 1px solid #ddd;
        border-radius: 15px;
        padding: 30px;
        background-color: white;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    h1, h2, h3, h4 { text-align: center !important; color: #2E8B57; }
    
    .stat-row {
        display: flex;
        justify-content: space-around;
        background: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        gap: 10px;
    }
    .stat-item { text-align: center; flex: 1; }
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# --- 3. الشعار ---
st.markdown("""
    <div class="logo-container">
        <img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png">
    </div>
    <h3 style="text-align: center; margin-top: -10px;">نظام تحليل الجسم الذكي</h3>
""", unsafe_allow_html=True)

# --- 4. المدخلات ---
with st.container(border=True):
    st.markdown("#### 👤 بيانات العميل")
    c1, c2 = st.columns(2)
    with c1: name = st.text_input("الاسم الكريم", "زائر")
    with c2: gender = st.selectbox("الجنس", ["ذكر", "أنثى"])

    c3, c4, c5 = st.columns(3)
    with c3: age = st.number_input("العمر", 10, 100, 30)
    with c4: weight_val = st.number_input("الوزن (kg)", 30.0, 200.0, 80.0)
    with c5: height_val = st.number_input("الطول (cm)", 100.0, 250.0, 180.0)

    st.markdown("---")
    st.markdown("#### 🎯 النشاط والهدف")
    c6, c7 = st.columns(2)
    with c6:
        activity_map = {"خامل (مكتبي)": 1.2, "نشاط خفيف": 1.375, "متوسط": 1.55, "عالي": 1.725}
        activity = st.selectbox("مستوى النشاط", list(activity_map.keys()))
    with c7:
        goal_map = {"إنقاص الوزن": "loss", "محافظة": "maintain", "زيادة الوزن": "gain"}
        goal = st.selectbox("الهدف", list(goal_map.keys()))

    st.write("") 
    calc_btn = st.button("تحليل البيانات 📊", type="primary", use_container_width=True)

# --- 5. العمليات الحسابية ---
if calc_btn:
    # BMR
    act_val = activity_map[activity]
    if gender == "ذكر":
        bmr = (9.99 * weight_val) + (6.25 * height_val) - (5 * age) + 5
    else:
        bmr = (9.99 * weight_val) + (6.25 * height_val) - (5 * age) - 161
        
    # TDEE + TEF Calculation
    activity_calories = bmr * act_val
    tef = activity_calories * 0.10  # 10% Thermic Effect
    total_tdee = activity_calories + tef

    # Target Calories
    if goal_map[goal] == "loss":
        target = total_tdee - 500
        p_r, c_r, f_r = 0.40, 0.30, 0.30
        rec_supps = "ISO-100, L-Carnitine, Multivitamin"
    elif goal_map[goal] == "gain":
        target = total_tdee + 500
        p_r, c_r, f_r = 0.30, 0.50, 0.20
        rec_supps = "Mass Gainer, Creatine, Pre-Workout"
    else:
        target = total_tdee
        p_r, c_r, f_r = 0.30, 0.40, 0.30
        rec_supps = "Whey Protein, Omega-3"

    p_g = int((target * p_r) / 4)
    c_g = int((target * c_r) / 4)
    f_g = int((target * f_r) / 9)
    
    bmi = weight_val / ((height_val/100)**2)
    if bmi < 18.5: bmi_st = "نحافة"
    elif bmi < 25: bmi_st = "وزن مثالي"
    elif bmi < 30: bmi_st = "زيادة وزن"
    else: bmi_st = "سمنة"

    # --- 6. عرض التقرير (الحل النهائي) ---
    st.markdown("---")
    st.success("✅ تم التحليل بدقة (شاملاً TEF)")

    # قمنا بدمج كود HTML في سطر واحد لمتغيرات النصوص لتجنب مشكلة المسافات
    # هذه الطريقة تمنع ظهور الكود كنص عادي
    
    html_content = f"""
    <div class="report-box">
        <div style="text-align: center;">
            <img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png" width="120">
            <h2 style="color: #2E8B57; margin: 10px 0;">تقرير الحالة الغذائية</h2>
            <p style="color: grey;">التاريخ: {datetime.date.today()}</p>
            <h3 style="color: #333;">العميل: {name}</h3>
        </div>
        <hr style="border: 1px solid #eee;">
        
        <h4 style="text-align: right; color: #2E8B57;">1️⃣ ملخص الجسم</h4>
        <div class="stat-row">
            <div class="stat-item">
                <strong>BMI</strong><br>
                <span style="font-size: 18px; color: #2E8B57;">{bmi:.1f}</span><br>
                <small>{bmi_st}</small>
            </div>
            <div class="stat-item">
                <strong>الاحتياج اليومي</strong><br>
                <span style="font-size: 18px; color: #2E8B57;">{int(target)}</span><br>
                <small>سعرة (شامل TEF)</small>
            </div>
            <div class="stat-item">
                <strong>الماء</strong><br>
                <span style="font-size: 18px; color: #2980b9;">{round(weight_val*0.033, 1)} L</span>
            </div>
        </div>

        <h4 style="text-align: right; color: #2E8B57;">2️⃣ احتياج الماكروز (يومياً)</h4>
        <div class="stat-row">
            <div class="stat-item" style="border: 1px solid #ffcccc; border-radius: 8px;">
                🥩 بروتين<br><b>{p_g}g</b>
            </div>
            <div class="stat-item" style="border: 1px solid #ffffcc; border-radius: 8px;">
                🍞 كارب<br><b>{c_g}g</b>
            </div>
            <div class="stat-item" style="border: 1px solid #ccffcc; border-radius: 8px;">
                🥑 دهون<br><b>{f_g}g</b>
            </div>
        </div>

        <h4 style="text-align: right; color: #2E8B57;">3️⃣ التوصيات</h4>
        <div style="background-color: #e8f5e9; padding: 15px; border-radius: 8px; text-align: center;">
            <p style="margin: 0; font-weight: bold;">لتحقيق هدف ({goal}) ننصح باستخدام:</p>
            <p style="margin: 5px 0; color: #2E8B57; font-size: 18px;">💊 {rec_supps}</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px; font-size: 12px; color: #aaa;">
            © 2026 First Nutrition System
        </div>
    </div>
    """
    
    # هنا يتم تنفيذ كود HTML
    st.markdown(html_content, unsafe_allow_html=True)

    # --- 7. زر الطباعة ---
    components.html(
        """
        <script>
        function printPage() {
            window.print();
        }
        </script>
        <div class="no-print" style="text-align: center; margin-top: 20px;">
            <button onclick="printPage()" style="
                background-color: #2E8B57; color: white; border: none; padding: 12px 25px;
                font-size: 16px; border-radius: 5px; cursor: pointer; font-weight: bold; font-family: sans-serif;">
                🖨️ طباعة التقرير / حفظ كـ PDF
            </button>
        </div>
        """,
        height=100
    )
