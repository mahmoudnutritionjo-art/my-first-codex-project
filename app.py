import streamlit as st
import datetime
import streamlit.components.v1 as components

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="First Nutrition App",
    page_icon="🍏",
    layout="centered"
)

# --- كود التصميم الجذري (CSS) ---
st.markdown("""
<style>
    /* 1. إعدادات الاتجاه العام */
    .stApp {
        direction: rtl;
        text-align: right;
    }

    /* 2. إخفاء العناصر غير المرغوبة عند الطباعة (الحل السحري) */
    @media print {
        /* إخفاء الزر نفسه */
        .print-btn-container { display: none !important; }
        /* إخفاء شريط أدوات Streamlit العلوي */
        header { display: none !important; }
        /* إخفاء الفوتر */
        footer { display: none !important; }
        /* إخفاء أي عناصر تحكم أخرى */
        .stButton { display: none !important; }
        
        /* تحسين شكل التقرير عند الطباعة */
        .report-box { border: 1px solid #2E8B57 !important; }
    }

    /* 3. تنسيق العناوين (تمركز) */
    h1, h2, h3, h4 {
        text-align: center !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2E8B57;
    }

    /* 4. تنسيق النصوص التوضيحية (يمين) */
    p, label, .stTextInput label, .stNumberInput label, .stSelectbox label {
        text-align: right !important;
    }
    
    /* 5. تنسيق زر الطباعة ليظهر بشكل جميل على الشاشة */
    .print-btn {
        background-color: #2E8B57;
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .print-btn:hover {
        background-color: #1e5e3a;
        transform: scale(1.02);
    }
    .print-btn-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 40px;
    }
    
    /* 6. حاوية الشعار (توسيط إجباري) */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .logo-container img {
        width: 160px;
        height: auto;
    }
</style>
""", unsafe_allow_html=True)

# --- عرض الشعار (HTML مباشر لضمان التوسيط) ---
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
        activity_map = {
            "خامل (مكتبي)": 1.2, 
            "نشاط خفيف (1-3 أيام)": 1.375, 
            "متوسط (3-5 أيام)": 1.55, 
            "عالي (6-7 أيام)": 1.725
        }
        activity = st.selectbox("مستوى النشاط", list(activity_map.keys()))
    with c7:
        goal_map = {
            "إنقاص الوزن (تنشيف)": "loss", 
            "محافظة على الوزن": "maintain", 
            "زيادة الوزن (تضخيم)": "gain"
        }
        goal = st.selectbox("الهدف", list(goal_map.keys()))

    st.write("") 
    calc_btn = st.button("تحليل البيانات وإصدار التقرير 📊", type="primary", use_container_width=True)

# --- الحسابات والتقرير ---
if calc_btn:
    # المنطق الحسابي
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

    # --- عرض التقرير ---
    st.markdown("---")
    st.success("✅ تم التحليل بنجاح!")
    
    # حاوية التقرير
    with st.container(border=True):
        # ترويسة التقرير (HTML لضمان التنسيق عند الطباعة)
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png" width="100">
                <h3>تقرير الحالة الغذائية</h3>
                <p><strong>العميل:</strong> {name} | <strong>التاريخ:</strong> {datetime.date.today()}</p>
            </div>
            <hr>
        """, unsafe_allow_html=True)

        st.markdown("#### 1️⃣ ملخص الجسم")
        m1, m2, m3 = st.columns(3)
        m1.metric("مؤشر الكتلة (BMI)", f"{bmi:.1f}", bmi_st)
        m2.metric("السعرات اليومية", f"{int(target)}")
        m3.metric("الماء المقترح", f"{round(weight_val*0.033, 1)} L")
        
        st.markdown("#### 2️⃣ احتياج الماكروز (يومياً)")
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.info(f"🥩 **بروتين**\n\n{p_g}g")
        c_m2.warning(f"🍞 **كارب**\n\n{c_g}g")
        c_m3.error(f"🥑 **دهون**\n\n{f_g}g")
        
        st.markdown("#### 3️⃣ توصيات الخبراء")
        st.markdown(f"لتحقيق هدفك **({goal})** ننصح باستخدام:")
        st.success(f"💊 **{rec_supps}**")
        
        st.caption("© 2026 First Nutrition Expert System")

    # --- زر الطباعة (مخفي عند الطباعة) ---
    components.html(
        """
        <div class="print-btn-container">
            <button onclick="window.print()" class="print-btn">
                🖨️ طباعة التقرير / حفظ كـ PDF
            </button>
        </div>
        """,
        height=100
    )
