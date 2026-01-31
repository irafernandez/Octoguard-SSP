import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard # Run: pip install st-copy-to-clipboard
from modules.password_generator import generate_secure_password, hash_password
from modules.password_assessor import assess_password_strength
from modules.form_validator import FormValidator
from modules.form_sanitizer import FormSanitizer

# --- PAGE SETUP ---
st.set_page_config(page_title="OctoGuard", page_icon="🐙", layout="wide")

# --- STYLE ---
st.markdown("""
<style>

/* ---- GLOBAL ---- */
html, body, [class*="css"] {
    background-color: #0e0e11 !important;
    color: #eaeaea !important;
    font-family: 'Inter', sans-serif;
}

/* ---- MAIN AREA ---- */
.main {
    background: radial-gradient(circle at top, #151515 0%, #0e0e11 60%);
}

/* ---- SIDEBAR ---- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b0b0f, #111118);
    border-right: 1px solid #1f1f2e;
}

section[data-testid="stSidebar"] h1 {
    letter-spacing: 1px;
}

/* ---- HEADERS ---- */
h1, h2, h3 {
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* ---- CONTAINERS (CARDS) ---- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(20, 20, 28, 0.85);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 0 30px rgba(0,0,0,0.4);
    backdrop-filter: blur(12px);
}

/* ---- INPUTS ---- */
input, textarea {
    background-color: #0f0f15 !important;
    border: 1px solid #2a2a3d !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}

/* ---- BUTTONS ---- */
.stButton>button {
    background: linear-gradient(135deg, #ff4b4b, #ff8c00);
    color: black !important;
    font-weight: 700;
    border-radius: 999px;
    padding: 0.6em 1.6em;
    border: none;
    transition: all 0.25s ease;
    box-shadow: 0 8px 20px rgba(255,75,75,0.35);
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(255,140,0,0.45);
}

/* ---- RADIO BUTTONS ---- */
div[role="radiogroup"] > label {
    background-color: #12121a;
    border-radius: 12px;
    padding: 10px 14px;
    margin-bottom: 6px;
    transition: all 0.2s ease;
}

div[role="radiogroup"] > label:hover {
    background-color: #1a1a28;
}

/* ---- ACCENT LINE ---- */
.accent-line {
    height: 3px;
    width: 50px;
    background: linear-gradient(90deg, #ff4b4b, #ff8c00);
    border-radius: 999px;
    margin-top: 6px;
}

/* ---- CODE BLOCK ---- */
pre {
    background-color: #0c0c12 !important;
    border-radius: 14px;
    border: 1px solid #1f1f2e;
}

/* ---- TOAST ---- */
div[data-testid="stToast"] {
    background-color: #151520;
    border: 1px solid #2a2a3d;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-bottom:40px;">
    <h1 style="font-size:3rem; margin-bottom:0;">🐙 OctoGuard</h1>
    <p style="color:#aaa; font-size:1.1rem;">
        All-in-one security toolkit for modern web apps
    </p>
</div>
""", unsafe_allow_html=True)


# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color: #FF4B4B;'>🐙 OCTOGUARD</h1>", unsafe_allow_html=True)
    st.caption("Swiss Knife Of Web Security")
    st.markdown("---")
    page = st.radio("TOOLS", ["Password Generator", "Password Assessor", "Form Validator"])

    st.markdown("---")
    st.markdown("""
        <div style="position: fixed; bottom: 20px; left: 20px;">
            <p style="color: #666; font-size: 14px; margin-bottom: 0;">© Milestone 1</p>
            <p style="color: #999; font-size: 12px;">Built by <b>Gino and Ira</b></p>
        </div>
    """, unsafe_allow_html=True)

# --- TAB 1: PASSWORD GENERATOR ---
if page == "Password Generator":
    st.markdown("## Password Generator <span style='font-size:12px; color:#00C853;'>● READY</span>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("### Configuration <div class='accent-line'></div>", unsafe_allow_html=True)
        length = st.number_input("Password Length (8-16 CHARACTERS)", 8, 16, 12)
        generate_clicked = st.button("Generate Password")

    if generate_clicked:
        pwd = generate_secure_password(length)
        st.session_state['current_pwd'] = pwd

    if 'current_pwd' in st.session_state:
        current_p = st.session_state['current_pwd']
        with st.container(border=True):
            st.markdown("### Generated Output <div class='accent-line'></div>", unsafe_allow_html=True)
            
            # 1. The Password Display
            st.text_input("Password", value=current_p)
            
            # 2. THE COPY BUTTON
            if st.button("Copy Password"):
                
                st.markdown(f"""
                    <script>
                        navigator.clipboard.writeText('{current_p}');
                    </script>
                """, unsafe_allow_html=True)
                st.toast("Password copied to clipboard!")

            # 3. The Hash Display
            st.text_input("SHA-256 Hash", value=hash_password(current_p))

# --- TAB 2: PASSWORD ASSESSOR ---
elif page == "Password Assessor":
    st.markdown("## Password Strength Assessor <span style='font-size:12px; color:#00CCFF;'>● ANALYZING</span>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("### Input Password <div class='accent-line'></div>", unsafe_allow_html=True)
        input_pwd = st.text_input("Enter Password to Analyze", type="password")
        
        analyze_btn = st.button("Analyze Strength")

    if analyze_btn and input_pwd:
        rating, color, feedback = assess_password_strength(input_pwd)
        with st.container(border=True):
            st.markdown("### Security Analysis <div class='accent-line'></div>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align:center; color:{color};'>{rating}</h1>", unsafe_allow_html=True)
            st.markdown("#### Security Recommendations")
            
            # These must be indented inside the 'with' block
            for item in feedback:
                if item.startswith("+"):
                    st.success(item)
                elif item.startswith("-"):
                    st.error(item)
                else:
                    st.info(item)

# --- TAB 3: FORM VALIDATOR ---
elif page == "Form Validator":
    st.markdown("## Form Input Validator <span style='font-size:12px; color:#FFA500;'>● VALIDATING</span>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    
    with col_l:
        with st.container(border=True):
            st.markdown("### Form Inputs <div class='accent-line'></div>", unsafe_allow_html=True)
            name = st.text_input("Full Name", value="John Doe")
            email = st.text_input("Email Address", value="john@example.com")
            user = st.text_input("Username", value="johndoe123")
            msg = st.text_area("Message", value="Hello, I would like to...")
            if st.button("Validate & Sanitize"):
                st.session_state['run_val'] = True

    with col_r:
        with st.container(border=True):
            st.markdown("### Validation Results <div class='accent-line'></div>", unsafe_allow_html=True)
            if st.session_state.get('run_val'):
                f_data = {'full_name': name, 'email': email, 'username': user, 'message': msg}
                v_res = FormValidator.validate_all(f_data)
                s_res = FormSanitizer.sanitize_all(f_data)
                
                # Perfect Text Formatting
                out = "VALIDATION RESULTS\n" + "─"*50 + "\n\n"
                for f in ['full_name', 'email', 'username', 'message']:
                    status = "✓ Valid" if v_res[f][0] else f"✗ {v_res[f][1]}"
                    out += f"{f.replace('_',' ').title()}: {status}\n"
                
                out += "\nSANITIZED OUTPUT\n" + "─"*50 + "\n\n"
                for f in ['full_name', 'email', 'username', 'message']:
                    out += f"{f.replace('_',' ').title()}: {s_res[f]['sanitized']}\n\n"
                
                out += "─"*50 + "\nProcess Complete."
                st.code(out, language="text")