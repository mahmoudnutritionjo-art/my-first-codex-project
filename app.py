import streamlit as st
import datetime

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="First Nutrition App",
    page_icon="🍏",
    layout="centered"
)

# --- كود التصميم (CSS) المعدل ---
st.markdown("""
<style>
    /* 1. الاتجاه العام للصفحة: يمين لليسار */
    .stApp {
        direction: rtl;
    }

    /* 2. العناوين الرئيسية: بالنص (Center) لجمالية التصميم */
    h1, h2, h3, h4, h5 {
        text-align: center !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2E8B57; /* لون أخضر الهوية */
    }

    /* 3. النصوص العادية وتسميات الخانات: يمين (Right) للقراءة الصحيحة */
    p, label, .stTextInput label, .stNumberInput label, .stSelectbox label {
        text-align: right !important;
    }

    /* 4. توسيط الشعار */
    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    div[data-testid="stImage"] img {
        width: 180px !important;
    }

    /* 5. تنسيق زر الطباعة */
    .print-btn {
        display: block;
        margin: 20px auto;
        background-color: #2E8B57;
        color: white; 
        padding: 12px 25px;
        border: none;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        cursor: pointer;
        font-family: sans-serif;
    }
    .print-btn:hover {
        background-color: #1e5e3a;
    }
</style>
""", unsafe_allow_html=True)

# --- الشعار والعنوان ---
st.image("https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png")
st.markdown("<h3>نظام تحليل الجسم الذكي</h3>", unsafe_allow_html=True)

# --- حاوية إدخال البيانات ---
with st.container(border=True):
    # العنوان الفرعي (سيظهر في الوسط الآن)
    st.markdown("#### 👤 بيانات العميل")
    
    # الصف الأول
    c1, c2 = st.columns(2)
    with c1: name = st.text_input("الاسم الكريم", "زائر")
    with c2: gender = st.selectbox("الجنس", ["ذكر", "أنثى"])

    # الصف الثاني
    c3, c4, c5 = st.columns(3)
    with c3: age = st.number_input("العمر", 10, 100, 30)
    with c4: weight_val = st.number_input("الوزن (kg)", 30.0, 200.0, 80.0)
    with c5: height_val = st.number_input("الطول (cm)", 100.0, 250.0, 180.0)

    st.markdown("---")
    st.markdown("#### 🎯 النشاط والهدف")
    
    # الصف الثالث
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

# --- العمليات الحسابية والتقرير ---
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

    # --- عرض التقرير ---
    st.markdown("---")
    st.success("✅ تم التحليل بنجاح!")
    
    with st.container(border=True):
        col_r1, col_r2 = st.columns([1, 3])
        with col_r1:
             st.image("https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png", width=80)
        with col_r2:
            st.markdown(f"### تقرير: {name}")
            st.markdown(f"**التاريخ:** {datetime.date.today()}")
            
        st.markdown("---")

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
        
        st.caption("First Nutrition Expert System ©")

    st.components.v1.html(
        """
        <button onclick="window.print()" class="print-btn">
            🖨️ طباعة التقرير / حفظ كـ PDF
        </button>
        """, 
        height=80
    )
