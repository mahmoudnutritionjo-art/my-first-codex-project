import streamlit as st
import datetime

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="First Nutrition Expert",
    page_icon="🍏",
    layout="centered"
)

# --- CSS للتصميم والطباعة ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    .stApp { direction: rtl; text-align: right; font-family: 'Tajawal', sans-serif; }
    
    /* تنسيق العناوين والتقرير */
    .report-container {
        border: 2px solid #2E8B57;
        padding: 30px;
        border-radius: 15px;
        background-color: white;
        margin-top: 20px;
    }
    
    .report-header {
        text-align: center;
        border-bottom: 2px solid #eee;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    .client-name {
        color: #2E8B57;
        font-size: 24px;
        font-weight: bold;
    }
    
    .stat-box {
        background-color: #f8fff8;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
        border: 1px solid #dcdcdc;
    }
    
    /* إخفاء العناصر غير الضرورية عند الطباعة */
    @media print {
        .stButton, .stSelectbox, .stNumberInput, header, footer { display: none !important; }
        .report-container { border: none; }
    }
    
    /* تنسيق الجداول */
    .food-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
        font-size: 14px;
    }
    .food-table th { background-color: #2E8B57; color: white; padding: 8px; }
    .food-table td { border: 1px solid #ddd; padding: 8px; text-align: center; }

</style>
""", unsafe_allow_html=True)

# --- الشعار ---
col_logo1, col_logo2, col_logo3 = st.columns([1,2,1])
with col_logo2:
    st.image("https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png", width=200)

st.markdown("<h2 style='text-align: center;'>نظام تحليل الجسم والتغذية</h2>", unsafe_allow_html=True)

# --- إدخال البيانات ---
with st.expander("📝 إدخال بيانات العميل (اضغط لفتح/إغلاق)", expanded=True):
    # 1. المعلومات الشخصية
    c1, c2 = st.columns(2)
    with c1:
        title = st.selectbox("اللقب", ["السيد", "السيدة", "الآنسة", "الكابتن"])
        client_name = st.text_input("اسم العميل", "زائر")
    with c2:
        gender = st.selectbox("الجنس", ["ذكر", "أنثى"])
        age = st.number_input("العمر", 10, 100, 30)

    # 2. القياسات
    c3, c4 = st.columns(2)
    with c3:
        weight = st.number_input("الوزن (KG)", 30.0, 200.0, 80.0)
    with c4:
        height = st.number_input("الطول (CM)", 100.0, 250.0, 180.0)

    # 3. النشاط والهدف
    activity_options = {"خامل (1.2)": 1.2, "نشاط خفيف (1.375)": 1.375, "نشاط متوسط (1.55)": 1.55, "نشيط جداً (1.725)": 1.725}
    activity = st.selectbox("مستوى النشاط", list(activity_options.keys()))
    
    goal_options = {"إنقاص الوزن": "loss", "محافظة": "maintain", "زيادة الوزن": "gain"}
    goal = st.selectbox("الهدف", list(goal_options.keys()))

    calc_btn = st.button("تحليل وإصدار التقرير الرسمي 📄")

# --- منطق الحساب والتقرير ---
if calc_btn:
    # 1. الحسابات الرياضية
    if gender == "ذكر":
        bmr = (9.99 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (9.99 * weight) + (6.25 * height) - (5 * age) - 161
        
    tdee = bmr * activity_options[activity]
    
    # حساب BMI
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    if bmi < 18.5: bmi_status = "نحافة"
    elif 18.5 <= bmi < 24.9: bmi_status = "وزن مثالي ✅"
    elif 25 <= bmi < 29.9: bmi_status = "زيادة وزن"
    else: bmi_status = "سمنة ⚠️"

    # حساب الماء (الوزن * 33 مل)
    water_need = (weight * 33) / 1000

    # حساب السعرات والماكروز
    target_calories = tdee
    if goal_options[goal] == "loss":
        target_calories -= 500
        macros = {"p": 0.40, "f": 0.30, "c": 0.30}
        rec_products = ["ISO-100", "L-Carnitine", "Multivitamin"]
    elif goal_options[goal] == "gain":
        target_calories += 500
        macros = {"p": 0.30, "f": 0.20, "c": 0.50}
        rec_products = ["Mass Gainer", "Creatine", "Pre-Workout"]
    else:
        macros = {"p": 0.30, "f": 0.30, "c": 0.40}
        rec_products = ["Whey Protein", "Omega 3", "Vitamins"]

    p_g = (target_calories * macros["p"]) / 4
    f_g = (target_calories * macros["f"]) / 9
    c_g = (target_calories * macros["c"]) / 4

    # --- عرض التقرير (Container) ---
    st.markdown("---")
    
    # بداية التقرير القابل للطباعة
    with st.container():
        st.markdown(f"""
        <div class="report-container">
            <div class="report-header">
                <h3>تقرير الحالة الغذائية - First Nutrition</h3>
                <p>التاريخ: {datetime.date.today()}</p>
            </div>
            
            <div style="text-align: center; margin-bottom: 20px;">
                <span class="client-name">العميل: {title} {client_name}</span>
            </div>

            <h4>1️⃣ تحليل الجسم والمؤشرات:</h4>
            <div style="display: flex; gap: 10px; justify-content: center;">
                <div class="stat-box" style="flex:1;">
                    <b>مؤشر الكتلة (BMI)</b><br>
                    <span style="font-size: 18px; color: #2E8B57;">{round(bmi, 1)}</span><br>
                    <small>{bmi_status}</small>
                </div>
                <div class="stat-box" style="flex:1;">
                    <b>الاحتياج اليومي</b><br>
                    <span style="font-size: 18px; color: #2E8B57;">{int(target_calories)}</span><br>
                    <small>سعرة حرارية</small>
                </div>
                <div class="stat-box" style="flex:1;">
                    <b>احتياج الماء</b><br>
                    <span style="font-size: 18px; color: blue;">{round(water_need, 1)}</span><br>
                    <small>لتر يومياً</small>
                </div>
            </div>

            <h4>2️⃣ الاحتياج الغذائي (الماكروز):</h4>
            <div style="display: flex; gap: 10px; justify-content: center;">
                <div class="stat-box" style="flex:1; border-color: #ffcccc;">
                    🥩 بروتين<br><b>{int(p_g)}g</b>
                </div>
                <div class="stat-box" style="flex:1; border-color: #ffffcc;">
                    🍞 كاربوهيدرات<br><b>{int(c_g)}g</b>
                </div>
                <div class="stat-box" style="flex:1; border-color: #ccffcc;">
                    🥑 دهون صحية<br><b>{int(f_g)}g</b>
                </div>
            </div>

            <h4>3️⃣ مصادر مقترحة لتغطية احتياجك:</h4>
            <table class="food-table">
                <tr>
                    <th>المصدر الغذائي</th>
                    <th>خيارات من الطعام</th>
                    <th>خيارات من المكملات (First Nutrition)</th>
                </tr>
                <tr>
                    <td><b>البروتين</b></td>
                    <td>صدور دجاج، سمك، بيض، لحم بقري</td>
                    <td>{rec_products[0]}</td>
                </tr>
                <tr>
                    <td><b>الكاربوهيدرات</b></td>
                    <td>أرز، شوفان، بطاطا، فواكه</td>
                    <td>Vitargo / Carb Powder</td>
                </tr>
                <tr>
                    <td><b>الدهون الصحية</b></td>
                    <td>زيت زيتون، مكسرات، أفوكادو</td>
                    <td>{rec_products[1] if 'Omega' in str(rec_products) else 'Omega-3'}</td>
                </tr>
            </table>

            <br>
            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;">
                <b>💊 التوصيات الخاصة:</b> نوصي باستخدام <b>{', '.join(rec_products)}</b> لتحقيق أفضل النتائج.
            </div>

            <hr>
            <p style="text-align: center; font-size: 12px; color: grey;">
                تم التحليل بواسطة نظام First Nutrition الذكي - {datetime.date.today().year}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("💡 لحفظ التقرير: اضغط بزر الماوس اليمين واختر 'Print' ثم احفظه كـ 'Save as PDF'.")

# --- روابط التواصل ---
st.markdown("---")
st.markdown("""
<div class="social-icons" style="text-align: center;">
    <a href="https://www.facebook.com/firstnutritionjordan/"><img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/firstnutritionjordan-1-FB-.png" width="30"></a>
    <a href="https://www.instagram.com/firstnutritionjo/"><img src="https://www.firstnutrition.com/wp-content/uploads/2026/01/firstnutritionjordan-2-INSTA.png" width="30"></a>
</div>
""", unsafe_allow_html=True)
