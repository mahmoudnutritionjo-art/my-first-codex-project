import streamlit as st
import datetime
import streamlit.components.v1 as components

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="First Nutrition App",
    page_icon="🍏",
    layout="centered"
)

# --- كود CSS القوي جداً (الحل النهائي) ---
st.markdown("""
<style>
    /* 1. إعدادات الاتجاه العام والخطوط */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    .stApp {
        direction: rtl;
        text-align: right;
        font-family: 'Tajawal', sans-serif;
    }

    /* 2. حل مشكلة الشعار (توسيط إجباري) */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 20px;
    }
    .logo-container img {
        width: 150px; /* حجم الشعار */
        max-width: 100%;
    }

    /* 3. حل مشكلة الطباعة (الصفحة البيضاء) */
    @media print {
        /* إظهار المحتوى المخفي */
        body, .stApp, .block-container {
            visibility: visible !important;
            height: auto !important;
            overflow: visible !important;
            display: block !important;
        }
        
        /* إخفاء العناصر غير الضرورية */
        header, footer, .no-print, .stButton, button {
            display: none !important;
        }

        /* تحسين شكل التقرير في الورقة */
        .report-box {
            border: 2px solid #2E8B57 !important;
            box-shadow: none !important;
            padding: 20px !important;
            margin: 0 !important;
            page-break-inside: avoid;
        }
    }

    /* 4. تنسيق النصوص */
    h1, h2, h3, h4 { text-align: center !important; color: #2E8B57; }
    p, label, .stMarkdown { text-align: right !important; }
    
    /* 5. تنسيق الحاوية (البوكس) */
    .report-box {
        border: 1px solid #ddd;
        border-radius: 15px;
        padding: 25px;
        background-color: white;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- الشعار (HTML مباشر لضمان التوسيط) ---
st.markdown("""
    <div class="logo-container">
        <img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png">
    </div>
    <h3 style="text-align: center; margin-top: -10px;">نظام تحليل الجسم الذكي</h3>
""", unsafe_allow_html=True)

# --- إدخال البيانات ---
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

# --- الحسابات والتقرير ---
if calc_btn:
    # الحسابات
    act_val = activity_map[activity]
    if gender == "ذكر":
        bmr = (9.99 * weight_val) + (6.25 * height_val) - (5 * age) + 5
    else:
        bmr = (9.99 * weight_val) + (6.25 * height_val) - (5 * age) - 161
        
    tdee = bmr * act_val
    
    if goal_map[goal] == "loss":
        target = tdee - 500
        p_r, c_r, f_r = 0.40, 0.30, 0.30
        rec_supps = "ISO-100, L-Carnitine, Multivitamin"
    elif goal_map[goal] == "gain":
        target = tdee + 500
        p_r, c_r, f_r = 0.30, 0.50, 0.20
        rec_supps = "Mass Gainer, Creatine, Pre-Workout"
    else:
        target = tdee
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

    # --- التقرير (داخل حاوية HTML مخصصة للطباعة) ---
    st.markdown("---")
    st.success("✅ تم التحليل! اضغط زر الطباعة في الأسفل.")

    # نستخدم HTML و CSS مخصص للتقرير لضمان شكله عند الطباعة
    report_html = f"""
    <div class="report-box">
        <div style="text-align: center;">
            <img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png" width="120">
            <h2 style="color: #2E8B57; margin-bottom: 5px;">تقرير الحالة الغذائية</h2>
            <p style="color: grey; font-size: 14px;">التاريخ: {datetime.date.today()}</p>
            <h3 style="color: #333;">العميل: {name}</h3>
        </div>
        <hr style="border: 1px solid #eee;">
        
        <h4 style="text-align: right; color: #2E8B57;">1️⃣ ملخص الجسم</h4>
        <div style="display: flex; justify-content: space-around; background: #f9f9f9; padding: 15px; border-radius: 10px;">
            <div style="text-align: center;">
                <strong>BMI</strong><br>
                <span style="font-size: 18px; color: #2E8B57;">{bmi:.1f}</span><br>
                <small>{bmi_st}</small>
            </div>
            <div style="text-align: center;">
                <strong>السعرات</strong><br>
                <span style="font-size: 18px; color: #2E8B57;">{int(target)}</span>
            </div>
            <div style="text-align: center;">
                <strong>الماء</strong><br>
                <span style="font-size: 18px; color: #2980b9;">{round(weight_val*0.033, 1)} L</span>
            </div>
        </div>

        <h4 style="text-align: right; color: #2E8B57;">2️⃣ احتياج الماكروز (يومياً)</h4>
        <div style="display: flex; gap: 10px;">
            <div style="flex: 1; text-align: center; border: 1px solid #ffcccc; padding: 10px; border-radius: 8px;">
                🥩 بروتين<br><b>{p_g}g</b>
            </div>
            <div style="flex: 1; text-align: center; border: 1px solid #ffffcc; padding: 10px; border-radius: 8px;">
                🍞 كارب<br><b>{c_g}g</b>
            </div>
            <div style="flex: 1; text-align: center; border: 1px solid #ccffcc; padding: 10px; border-radius: 8px;">
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
    st.markdown(report_html, unsafe_allow_html=True)

    # --- زر الطباعة (الجافاسكريبت) ---
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
                font-size: 16px; border-radius: 5px; cursor: pointer; font-weight: bold;">
                🖨️ طباعة التقرير / حفظ كـ PDF
            </button>
        </div>
        """,
        height=100
    )
