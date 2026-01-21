import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="First Nutrition App",
    page_icon="🍏",
    layout="centered"
)

# --- تنسيق RTL وتوسيط الشعار ---
st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    /* توسيط الصور بدقة */
    div[data-testid="stImage"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 150px; /* التحكم بحجم الشعار */
    }
    /* تحسين الأزرار */
    .stButton button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- دالة إنشاء PDF (بسيطة ومضمونة) ---
def create_pdf(name, age, weight, height, goal, calories, protein, carbs, fats, recs):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height_page = A4
    
    # ملاحظة: ReportLab العربي يحتاج خطوط خاصة، 
    # للتبسيط سنكتب التقرير بالإنجليزية التقنية المفهومة أو نحتاج رفع ملف خط عربي
    # هنا سنستخدم حيلة كتابة الأرقام والمصطلحات الإنجليزية لضمان عدم تكسر الحروف
    # أو نعتمد على المتصفح للطباعة وهو الحل الأضمن للعربي
    
    # سأترك دالة الـ PDF فارغة للآن وسنعتمد زر الطباعة المباشر 
    # لأنه الأفضل للغة العربية بدون تعقيد رفع خطوط
    return buffer

# --- الشعار (صغير وفي الوسط) ---
st.image("https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png", width=150)

st.markdown("<h2 style='text-align: center; color: #2E8B57;'>نظام تحليل الجسم الذكي</h2>", unsafe_allow_html=True)

# --- المدخلات ---
with st.container(border=True):
    st.markdown("### 👤 بيانات العميل")
    col_name, col_gender = st.columns(2)
    with col_name: name = st.text_input("الاسم", "زائر")
    with col_gender: gender = st.radio("الجنس", ["ذكر", "أنثى"], horizontal=True)

    col1, col2, col3 = st.columns(3)
    with col1: age = st.number_input("العمر", 10, 100, 30)
    with col2: weight_val = st.number_input("الوزن (kg)", 30.0, 200.0, 80.0)
    with col3: height_val = st.number_input("الطول (cm)", 100.0, 250.0, 180.0)

    st.markdown("### 🎯 النشاط والهدف")
    activity = st.selectbox("مستوى النشاط", [
        "خامل (1.2)", "نشاط خفيف (1.375)", 
        "نشاط متوسط (1.55)", "نشيط جداً (1.725)"
    ])
    
    goal = st.selectbox("الهدف", [
        "إنقاص الوزن (تنشيف)", 
        "محافظة على الوزن", 
        "زيادة الوزن (تضخيم)"
    ])

    btn = st.button("تحليل البيانات وإصدار التقرير 📊", type="primary")

# --- العمليات ---
if btn:
    # الحسابات
    act_val = float(activity.split('(')[1].replace(')', ''))
    
    if gender == "ذكر":
        bmr = (9.99 * weight_val) + (6.25 * height_val) - (5 * age) + 5
    else:
        bmr = (9.99 * weight_val) + (6.25 * height_val) - (5 * age) - 161
        
    tdee = bmr * act_val
    
    # تعديل السعرات حسب الهدف
    if "إنقاص" in goal:
        target = tdee - 500
        p_r, c_r, f_r = 0.40, 0.30, 0.30
        recs_txt = "ISO-100, L-Carnitine"
    elif "زيادة" in goal:
        target = tdee + 500
        p_r, c_r, f_r = 0.30, 0.50, 0.20
        recs_txt = "Mass Gainer, Creatine"
    else:
        target = tdee
        p_r, c_r, f_r = 0.30, 0.40, 0.30
        recs_txt = "Whey Protein, Omega-3"

    p_g = int((target * p_r) / 4)
    c_g = int((target * c_r) / 4)
    f_g = int((target * f_r) / 9)
    
    # حساب BMI
    bmi = weight_val / ((height_val/100)**2)
    if bmi < 18.5: bmi_st = "نحافة"
    elif bmi < 25: bmi_st = "وزن مثالي"
    elif bmi < 30: bmi_st = "زيادة وزن"
    else: bmi_st = "سمنة"

    # --- عرض التقرير (تصميم نظيف) ---
    st.markdown("---")
    st.success("✅ تم التحليل بنجاح!")
    
    # حاوية التقرير
    with st.container(border=True):
        col_h1, col_h2 = st.columns([3,1])
        with col_h1:
            st.markdown(f"### تقرير: {name}")
            st.caption(f"التاريخ: {datetime.date.today()}")
        with col_h2:
            st.image("https://www.firstnutrition.com/wp-content/uploads/2026/01/logo.png", width=60)
            
        st.markdown("#### 1️⃣ ملخص الجسم")
        c_res1, c_res2, c_res3 = st.columns(3)
        c_res1.metric("BMI", f"{bmi:.1f}", bmi_st)
        c_res2.metric("السعرات اليومية", f"{int(target)}")
        c_res3.metric("الماء المقترح", f"{round(weight_val*0.033, 1)} L")
        
        st.markdown("#### 2️⃣ احتياج الماكروز (يومياً)")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.info(f"🥩 بروتين: {p_g}g")
        col_m2.warning(f"🍞 كارب: {c_g}g")
        col_m3.error(f"🥑 دهون: {f_g}g")
        
        st.markdown("#### 3️⃣ التوصيات")
        st.write(f"لتحقيق هدفك **({goal})**، نوصي بـ:")
        st.markdown(f"##### 💊 {recs_txt}")
        
        st.markdown("---")
        st.caption("First Nutrition Expert System ©")

    # --- زر الطباعة الذكي ---
    # هذا الكود يستخدم جافاسكريبت لفتح نافذة الطباعة فوراً
    # وهو أفضل حل للغة العربية لأن المتصفح يحافظ على التنسيق 100%
    st.components.v1.html(
        """
        <script>
        function printReport() {
            window.print();
        }
        </script>
        <div style="text-align: center; margin-top: 20px;">
            <button onclick="printReport()" style="
                background-color: #2E8B57; 
                color: white; 
                padding: 10px 20px; 
                border: none; 
                border-radius: 5px; 
                font-size: 16px; 
                cursor: pointer;
                font-family: sans-serif;
                font-weight: bold;">
                🖨️ طباعة / حفظ كـ PDF
            </button>
        </div>
        """, 
        height=80
    )

import datetime
