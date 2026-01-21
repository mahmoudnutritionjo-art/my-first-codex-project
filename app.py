import streamlit as st

# إعدادات الصفحة العامة
st.set_page_config(
    page_title="First Nutrition Calculator",
    page_icon="🍏",
    layout="centered"
)

# --- CSS لتحسين التصميم وجعله عربي (من اليمين لليسار) ---
st.markdown("""
<style>
    /* تغيير اتجاه النصوص للعربية */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* تنسيق العناوين */
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2E8B57; /* لون أخضر مناسب للتغذية */
        text-align: center;
    }
    
    /* توسيط الشعار */
    div[data-testid="stImage"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;
    }
    
    /* تحسين شكل النتائج */
    .metric-box {
        background-color: #f0f8f0;
        border: 2px solid #2E8B57;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* تنسيق الأزرار */
    .stButton>button {
        width: 100%;
        background-color: #2E8B57;
        color: white;
        font-size: 18px;
        border-radius: 8px;
        height: 50px;
    }
    
    /* تنسيق روابط السوشيال ميديا */
    .social-icons {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 20px;
    }
    .social-icons img {
        width: 40px;
        transition: transform 0.2s;
    }
    .social-icons img:hover {
        transform: scale(1.1);
    }
</style>
""", unsafe_allow_html=True)

# --- 1. قسم الشعار (Logo) ---
st.image("https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png", use_container_width=True)

# --- 2. العنوان ---
st.title("نظام حساب السعرات الحرارية")
st.markdown("<h4 style='text-align: center; color: gray;'>أدخل بيانات العميل بدقة للحصول على النتائج</h4>", unsafe_allow_html=True)
st.write("---")

# --- 3. إدخال البيانات (مقسمة لعمودين بشكل مرتب) ---
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
    age = st.number_input("العمر (بالسنوات)", min_value=10, max_value=120, value=30)

with col2:
    weight = st.number_input("الوزن (كغ - KG)", min_value=30.0, max_value=300.0, value=70.0)
    height = st.number_input("الطول (سم - CM)", min_value=100.0, max_value=250.0, value=170.0)

# مسافة فاصلة
st.write("") 

# --- 4. زر الحساب والمنطق البرمجي ---
if st.button("احسب احتياج العميل (BMR)"):
    
    # تعريف المتغيرات
    W = weight
    H = height
    A = age
    
    # معادلة Harris-Benedict
    if gender == "ذكر":
        bmr_harris = 66.5 + (13.75 * W) + (5 * H) - (6.75 * A)
    else:
        bmr_harris = 655.1 + (9.563 * W) + (1.85 * H) - (4.676 * A)

    # معادلة Mifflin-St Jeor (الأدق)
    if gender == "ذكر":
        bmr_mifflin = (9.99 * W) + (6.25 * H) - (5 * A) + 5
    else:
        bmr_mifflin = (9.99 * W) + (6.25 * H) - (5 * A) - 161

    # --- 5. عرض النتائج بشكل جذاب ---
    st.write("---")
    
    # النتيجة الرئيسية داخل صندوق مميز
    st.markdown(f"""
    <div class="metric-box">
        <h3 style="margin-bottom: 0;">النتيجة المعتمدة (الأكثر دقة)</h3>
        <p style="color: #555;">Mifflin-St Jeor Equation</p>
        <h1 style="color: #2E8B57; font-size: 50px; margin: 0;">{round(bmr_mifflin)}</h1>
        <p style="font-weight: bold;">سعرة حرارية / يوم</p>
    </div>
    """, unsafe_allow_html=True)

    # نتيجة المقارنة (اختياري)
    with st.expander("اضغط هنا لمشاهدة النتيجة حسب معادلة Harris-Benedict"):
        st.info(f"النتيجة: **{round(bmr_harris)}** سعرة حرارية / يوم")

# --- 6. تذييل الصفحة (Footer) وروابط السوشيال ميديا ---
st.write("---")
st.markdown("<h5 style='text-align: center;'>تابعونا على منصات التواصل الاجتماعي</h5>", unsafe_allow_html=True)

# روابط الصور والروابط المقصودة
social_html = """
<div class="social-icons">
    <a href="https://www.facebook.com/firstnutritionjordan/" target="_blank">
        <img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/firstnutritionjordan-1-FB-.png" alt="Facebook">
    </a>
    <a href="https://www.instagram.com/firstnutritionjo/" target="_blank">
        <img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/firstnutritionjordan-2-INSTA.png" alt="Instagram">
    </a>
    <a href="https://www.youtube.com/@FirstNutritionofficial" target="_blank">
        <img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/firstnutritionjordan-3YOUTUBE-.png" alt="YouTube">
    </a>
    <a href="https://www.linkedin.com/company/first-nutrition/" target="_blank">
        <img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/firstnutritionjordan-4in-.png" alt="LinkedIn">
    </a>
    <a href="https://www.firstnutrition.com" target="_blank">
        <img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/firstnutritionjordan-5-WEB-1.png" alt="Website">
    </a>
</div>
"""
st.markdown(social_html, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; margin-top: 20px; color: grey; font-size: 12px;'>© 2026 First Nutrition - Sales Team App</p>", unsafe_allow_html=True)
