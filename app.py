import streamlit as st
import datetime

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="First Nutrition Pro",
    page_icon="💪",
    layout="centered"
)

# --- تفعيل اللغة العربية (يمين لليسار) ---
st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    /* تحسين شكل الجداول */
    .stTable { width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# --- الشعار ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.image("https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png", use_container_width=True)

st.title("نظام تحليل الجسم - First Nutrition")

# --- 1. إدخال البيانات ---
with st.expander("📝 بيانات العميل (اضغط للتعديل)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("اسم العميل", "زائر")
    with col2:
        gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
    
    col3, col4, col5 = st.columns(3)
    with col3: age = st.number_input("العمر", 10, 100, 30)
    with col4: weight = st.number_input("الوزن (KG)", 30.0, 200.0, 80.0)
    with col5: height = st.number_input("الطول (CM)", 100.0, 250.0, 180.0)

    col6, col7 = st.columns(2)
    with col6:
        activity_map = {"خامل (1.2)": 1.2, "نشاط خفيف (1.375)": 1.375, "نشاط متوسط (1.55)": 1.55, "نشيط جداً (1.725)": 1.725}
        activity = st.selectbox("مستوى النشاط", list(activity_map.keys()))
    with col7:
        goal_map = {"إنقاص الوزن": "loss", "محافظة": "maintain", "زيادة الوزن": "gain"}
        goal = st.selectbox("الهدف", list(goal_map.keys()))

    calc_btn = st.button("تحليل وإصدار التقرير 📊", type="primary")

# --- منطق الحساب والنتيجة ---
if calc_btn:
    # الحسابات
    if gender == "ذكر":
        bmr = (9.99 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (9.99 * weight) + (6.25 * height) - (5 * age) - 161
        
    tdee = bmr * activity_map[activity]
    
    # مؤشر الكتلة BMI
    bmi = weight / ((height/100) ** 2)
    if bmi < 18.5: bmi_status = "نحافة 🔵"
    elif 18.5 <= bmi < 24.9: bmi_status = "وزن مثالي ✅"
    elif 25 <= bmi < 29.9: bmi_status = "زيادة وزن 🟡"
    else: bmi_status = "سمنة 🔴"

    # الماء والسعرات
    water = (weight * 33) / 1000
    target_cal = tdee
    
    if goal_map[goal] == "loss":
        target_cal -= 500
        rec_supps = "ISO-100, L-Carnitine, Multivitamin"
        p_ratio, c_ratio, f_ratio = 0.40, 0.30, 0.30
    elif goal_map[goal] == "gain":
        target_cal += 500
        rec_supps = "Mass Gainer, Creatine, Pre-Workout"
        p_ratio, c_ratio, f_ratio = 0.30, 0.50, 0.20
    else:
        rec_supps = "Whey Protein, Omega-3"
        p_ratio, c_ratio, f_ratio = 0.30, 0.40, 0.30

    p_g = int((target_cal * p_ratio) / 4)
    c_g = int((target_cal * c_ratio) / 4)
    f_g = int((target_cal * f_ratio) / 9)

    # --- عرض التقرير (أدوات أصلية - لا تخطئ أبداً) ---
    st.markdown("---")
    
    # عنوان التقرير داخل إطار
    with st.container(border=True):
        st.header(f"📋 تقرير الحالة الغذائية: {name}")
        st.caption(f"التاريخ: {datetime.date.today()}")
        
        # الصف الأول: المؤشرات الرئيسية
        st.subheader("1️⃣ مؤشرات الجسم")
        m1, m2, m3 = st.columns(3)
        m1.metric("مؤشر الكتلة (BMI)", f"{bmi:.1f}", bmi_status)
        m2.metric("الاحتياج اليومي", f"{int(target_cal)} سعرة")
        m3.metric("احتياج الماء", f"{water:.1f} لتر", "يومياً")
        
        st.markdown("---")
        
        # الصف الثاني: الماكروز
        st.subheader("2️⃣ توزيع السعرات (الماكروز)")
        c1, c2, c3 = st.columns(3)
        c1.info(f"🥩 **بروتين:**\n\n {p_g} جرام")
        c2.warning(f"🍞 **كارب:**\n\n {c_g} جرام")
        c3.error(f"🥑 **دهون:**\n\n {f_g} جرام")
        
        st.markdown("---")
        
        # الصف الثالث: التوصيات
        st.subheader("3️⃣ التوصيات والمكملات")
        st.success(f"💡 لتحقيق هدفك ({goal}) ننصح باستخدام باقة: **{rec_supps}**")
        
        # جدول المصادر
        st.markdown("**جدول مصادر مقترحة:**")
        st.table({
            "العنصر": ["البروتين", "الكاربوهيدرات", "الدهون الصحية"],
            "أمثلة من الطعام": ["دجاج، سمك، بيض", "أرز، شوفان، بطاطا", "زيت زيتون، مكسرات"],
            "مكملات First Nutrition": [rec_supps.split(',')[0], "Carb Powder / Vitargo", "Omega-3"]
        })
        
        st.caption("© First Nutrition Expert System")

# --- تذييل الصفحة ---
st.markdown("---")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1: st.link_button("🌐 الموقع الرسمي", "https://www.firstnutrition.com")
with col_s2: st.link_button("📸 انستقرام", "https://www.instagram.com/firstnutritionjo/")
with col_s3: st.link_button("📘 فيسبوك", "https://www.facebook.com/firstnutritionjordan/")
