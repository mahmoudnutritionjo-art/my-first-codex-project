import streamlit as st
import datetime

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="First Nutrition App",
    page_icon="🍏",
    layout="centered"
)

# --- كود التصميم (CSS) لإصلاح الاتجاه والشعار ---
st.markdown("""
<style>
    /* 1. جعل الاتجاه من اليمين لليسار لكل الصفحة */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* 2. توسيط الشعار بدقة (الحل الجذري) */
    div[data-testid="stImage"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    div[data-testid="stImage"] img {
        width: 180px !important; /* حجم متوسط ومناسب */
    }

    /* 3. تنسيق العناوين والنصوص لتكون عاليمين */
    h1, h2, h3, p, .stTextInput label, .stNumberInput label, .stSelectbox label {
        text-align: right !important;
    }
    
    /* 4. تنسيق مدخلات البيانات */
    .stTextInput input, .stNumberInput input {
        text-align: right; 
        direction: rtl;
    }

    /* 5. زر الطباعة */
    .print-btn {
        display: block;
        margin: 0 auto;
        background-color: #2E8B57;
        color: white; 
        padding: 12px 25px;
        text-decoration: none;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        cursor: pointer;
        border: none;
    }
    .print-btn:hover {
        background-color: #1e5e3a;
    }
</style>
""", unsafe_allow_html=True)

# --- الشعار (سيظهر في الوسط بسبب كود CSS أعلاه) ---
st.image("https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png")

st.markdown("<h3 style='text-align: center; color: #2E8B57;'>نظام تحليل الجسم الذكي</h3>", unsafe_allow_html=True)

# --- حاوية إدخال البيانات ---
with st.container(border=True):
    st.markdown("#### 👤 بيانات العميل")
    
    # الصف الأول
    c1, c2 = st.columns(2)
    with c1: # اليمين
        name = st.text_input("الاسم الكريم", "زائر")
    with c2: # اليسار
        gender = st.selectbox("الجنس", ["ذكر", "أنثى"])

    # الصف الثاني
    c3, c4, c5 = st.columns(3)
    with c3:
        age = st.number_input("العمر", 10, 100, 30)
    with c4:
        weight_val = st.number_input("الوزن (kg)", 30.0, 200.0, 80.0)
    with c5:
        height_val = st.number_input("الطول (cm)", 100.0, 250.0, 180.0)

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

    # زر التحليل
    st.write("") # مسافة
    calc_btn = st.button("تحليل البيانات وإصدار التقرير 📊", type="primary", use_container_width=True)

# --- العمليات الحسابية والتقرير ---
if calc_btn:
    # 1. الحسابات
    act_val = activity_map[activity]
    
    if gender == "ذكر":
        bmr = (9.99 * weight_val) + (6.25 * height_val) - (5 * age) + 5
    else:
        bmr = (9.99 * weight_val) + (6.25 * height_val) - (5 * age) - 161
        
    tdee = bmr * act_val
    
    # تعديل السعرات حسب الهدف
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
    
    # BMI
    bmi = weight_val / ((height_val/100)**2)
    if bmi < 18.5: bmi_st, bmi_col = "نحافة", "blue"
    elif bmi < 25: bmi_st, bmi_col = "وزن مثالي", "green"
    elif bmi < 30: bmi_st, bmi_col = "زيادة وزن", "orange"
    else: bmi_st, bmi_col = "سمنة", "red"

    # --- عرض التقرير ---
    st.markdown("---")
    st.success("✅ تم التحليل بنجاح!")
    
    # حاوية التقرير (تصميم فاتورة/تقرير)
    with st.container(border=True):
        # ترويسة التقرير
        col_r1, col_r2 = st.columns([1, 3])
        with col_r1:
             st.image("https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png", width=80)
        with col_r2:
            st.markdown(f"### تقرير: {name}")
            st.markdown(f"**التاريخ:** {datetime.date.today()}")
            
        st.markdown("---")

        # 1. المؤشرات
        st.markdown("#### 1️⃣ ملخص الجسم")
        m1, m2, m3 = st.columns(3)
        m1.metric("مؤشر الكتلة (BMI)", f"{bmi:.1f}", bmi_st)
        m2.metric("السعرات اليومية", f"{int(target)}")
        m3.metric("الماء المقترح", f"{round(weight_val*0.033, 1)} L")
        
        # 2. الماكروز
        st.markdown("#### 2️⃣ احتياج الماكروز (يومياً)")
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.info(f"🥩 **بروتين**\n\n{p_g}g")
        c_m2.warning(f"🍞 **كارب**\n\n{c_g}g")
        c_m3.error(f"🥑 **دهون**\n\n{f_g}g")
        
        # 3. التوصيات
        st.markdown("#### 3️⃣ توصيات الخبراء")
        st.write(f"لتحقيق هدفك **({goal})** ننصح باستخدام:")
        st.success(f"💊 **{rec_supps}**")
        
        st.caption("First Nutrition Expert System ©")

    # --- زر الطباعة (الجافاسكريبت) ---
    # هذا الزر يفتح نافذة الطباعة فوراً عند الضغط عليه
    st.components.v1.html(
        """
        <button onclick="window.print()" class="print-btn" style="
            display: block; margin: 20px auto; background-color: #2E8B57; 
            color: white; padding: 10px 30px; border: none; border-radius: 5px; 
            font-size: 16px; cursor: pointer; font-family: sans-serif;">
            🖨️ طباعة التقرير / حفظ كـ PDF
        </button>
        """, 
        height=80
    )
