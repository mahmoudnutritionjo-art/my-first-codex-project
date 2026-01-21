import streamlit as st

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="First Nutrition Pro",
    page_icon="💪",
    layout="centered"
)

# --- CSS للتصميم الاحترافي واللغة العربية ---
st.markdown("""
<style>
    .stApp { direction: rtl; text-align: right; }
    h1, h2, h3 { color: #2E8B57; font-family: 'Segoe UI', sans-serif; text-align: center; }
    
    /* تنسيق بطاقات النتائج */
    .result-card {
        background-color: #f8fff8;
        border: 2px solid #2E8B57;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .big-number { font-size: 36px; font-weight: bold; color: #2E8B57; }
    .label-text { font-size: 16px; color: #555; font-weight: bold; }
    
    /* تنسيق الماكروز */
    .macro-box {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
    }
    
    /* تنسيق التوصيات */
    .rec-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin-top: 20px;
    }
    
    .stButton>button { background-color: #2E8B57; color: white; height: 50px; font-size: 18px; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- الشعار ---
st.image("https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png", use_container_width=True)
st.title("نظام تحليل الجسم الذكي")

# --- 1. إدخال البيانات الأساسية ---
st.subheader("1️⃣ بيانات العميل")
col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
    age = st.number_input("العمر", 10, 100, 30)
with col2:
    weight = st.number_input("الوزن (KG)", 30.0, 200.0, 80.0)
    height = st.number_input("الطول (CM)", 100.0, 250.0, 180.0)

# --- 2. مستوى النشاط والهدف (الإضافات الجديدة) ---
st.subheader("2️⃣ نمط الحياة والهدف")
activity_options = {
    "خامل (عمل مكتبي، لا رياضة)": 1.2,
    "نشاط خفيف (رياضة 1-3 أيام)": 1.375,
    "نشاط متوسط (رياضة 3-5 أيام)": 1.55,
    "نشيط جداً (رياضة 6-7 أيام)": 1.725,
    "رياضي محترف (تمارين قاسية يومياً)": 1.9
}
activity = st.selectbox("مستوى النشاط اليومي", list(activity_options.keys()))

goal_options = {
    "إنقاص الوزن (تنشيف)": "loss",
    "محافظة على الوزن": "maintain",
    "زيادة الوزن (تضخيم)": "gain"
}
goal = st.selectbox("الهدف من البرنامج", list(goal_options.keys()))

# --- زر التحليل ---
if st.button("تحليل احتياج العميل وإصدار التقرير 📊"):
    
    # 1. حساب BMR (Mifflin-St Jeor)
    if gender == "ذكر":
        bmr = (9.99 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (9.99 * weight) + (6.25 * height) - (5 * age) - 161

    # 2. حساب TDEE (السعرات للمحافظة)
    tdee = bmr * activity_options[activity]

    # 3. حساب سعرات الهدف
    target_calories = tdee
    if goal_options[goal] == "loss":
        target_calories = tdee - 500
        macros_ratio = {"p": 0.40, "f": 0.30, "c": 0.30} # بروتين عالي للتنشيف
        rec_text = "نوصي بمنتجات حرق الدهون + بروتين المعزول (Iso) للحفاظ على العضلات."
        rec_products = ["ISO-100 / Whey Isolate", "L-Carnitine / Fat Burner", "Multivitamin"]
    elif goal_options[goal] == "gain":
        target_calories = tdee + 500
        macros_ratio = {"p": 0.30, "f": 0.20, "c": 0.50} # كارب عالي للتضخيم
        rec_text = "نوصي بمنتجات زيادة الوزن (Gainer) والكرياتين لزيادة القوة والحجم."
        rec_products = ["Mass Gainer", "Creatine Monohydrate", "Pre-Workout"]
    else:
        macros_ratio = {"p": 0.30, "f": 0.30, "c": 0.40} # متوازن
        rec_text = "نوصي بالواي بروتين والملتي فيتامين للصحة العامة والاستشفاء."
        rec_products = ["Whey Protein Gold", "Omega 3", "Daily Vitamins"]

    # 4. حساب الماكروز (الجرامات)
    protein_g = (target_calories * macros_ratio["p"]) / 4
    fat_g = (target_calories * macros_ratio["f"]) / 9
    carbs_g = (target_calories * macros_ratio["c"]) / 4

    # --- عرض النتائج ---
    st.markdown("---")
    st.header("📋 تقرير First Nutrition")
    
    # بطاقة السعرات الرئيسية
    st.markdown(f"""
    <div class="result-card">
        <p class="label-text">احتياجك اليومي لتحقيق هدفك ({goal})</p>
        <div class="big-number">{int(target_calories)} سعرة حرارية</div>
        <p style="font-size: 12px; color: grey;">(معدل الأيض الأساسي BMR: {int(bmr)})</p>
    </div>
    """, unsafe_allow_html=True)

    # عرض الماكروز
    st.subheader("🍽️ تقسيم العناصر الغذائية (الماكروز)")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""<div class="macro-box">🥩 بروتين<br><b>{int(protein_g)}g</b></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="macro-box">🍞 كارب<br><b>{int(carbs_g)}g</b></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="macro-box">🥑 دهون<br><b>{int(fat_g)}g</b></div>""", unsafe_allow_html=True)

    # --- التوصيات الذكية (للبيع) ---
    st.markdown("---")
    st.subheader("💊 توصيات الخبراء (Supplements)")
    
    st.info(f"💡 نصيحة: {rec_text}")
    
    st.write("المنتجات المقترحة لك:")
    r1, r2, r3 = st.columns(3)
    for i, prod in enumerate(rec_products):
        if i == 0: r1.success(f"✅ {prod}")
        if i == 1: r2.success(f"✅ {prod}")
        if i == 2: r3.success(f"✅ {prod}")

    # ملاحظة للطباعة
    st.markdown("---")
    st.caption("يمكنك طباعة هذا التقرير أو حفظه كـ PDF من خيارات المتصفح (Print -> Save as PDF).")

# --- الفوتر ---
st.markdown("---")
# Social Media Links (نفس الروابط السابقة)
social_html = """
<div style="display: flex; justify-content: center; gap: 10px;">
    <a href="https://www.facebook.com/firstnutritionjordan/" target="_blank">فيسبوك</a> | 
    <a href="https://www.instagram.com/firstnutritionjo/" target="_blank">انستقرام</a> | 
    <a href="https://www.firstnutrition.com" target="_blank">الموقع الرسمي</a>
</div>
<p style='text-align: center; color: grey; font-size: 12px; margin-top: 10px;'>© 2026 First Nutrition</p>
"""
st.markdown(social_html, unsafe_allow_html=True)
