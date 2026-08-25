import streamlit as st
import pandas as pd
import random
import re
import base64
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="IdeaTrix", layout="wide", page_icon="💡")

# Hide the default Streamlit button and adjust padding
st.markdown(
    """
    <style>
    div[data-testid="stButton"] { position: absolute; left: -9999px; opacity: 0; }
    .block-container { padding-top: 0rem; padding-bottom: 0rem; }
    </style>
    """,
    unsafe_allow_html=True
)

file_path = "Idea-Triggers-Tools_T_Android.csv"
image_path = "ideaTRix_icon.png"

# Helper function to encode local image to base64 for HTML embedding
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""

img_base64 = get_base64_of_bin_file(image_path)
img_tag = f'<img src="data:image/png;base64,{img_base64}" class="logo-img" alt="IdeaTrix Logo">' if img_base64 else '<div class="fallback-logo">i</div>'

try:
    df = pd.read_csv(file_path)
    
    # 2. State Management for Random Clicks & Effects Counter
    if 'click_count' not in st.session_state:
        st.session_state.click_count = 0
        
    if 'current_idx' not in st.session_state:
        st.session_state.current_idx = random.randint(0, len(df) - 1)

    # Detect the hidden button click
    if st.button("HiddenTrigger", key="hidden_trigger"):
        st.session_state.current_idx = random.randint(0, len(df) - 1)
        st.session_state.click_count += 1
        
        # Trigger a random visual effect every 3 clicks
        if st.session_state.click_count > 0 and st.session_state.click_count % 3 == 0:
            effect_choice = random.choice(['balloons', 'snow'])
            if effect_choice == 'balloons':
                st.balloons()
            else:
                st.snow()
    
    # Ensure index is within bounds
    idx = st.session_state.current_idx % len(df)
    
    # Target the text column
    text_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    
    # 3. Text Separation Logic
    raw_text = str(df.iloc[idx][text_col])
    
    parts = re.split(r'\n+[Ee]x\.?\s*:?\s*', raw_text, maxsplit=1)
    raw_theme = parts[0].strip()
    raw_example = parts[1].strip() if len(parts) > 1 else ""
    cleaned_theme = re.sub(r'^\d+\.?\s*', '', raw_theme).strip()

    # 4. Interactive UI Component
    android_ui_html = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+Pro:wght@300;400;600;700&display=swap');

    body {{
        margin: 0; padding: 0;
        background-color: #FFFFFB;
        background-image: radial-gradient(#6750A433 1.5px, transparent 1.5px);
        background-size: 24px 24px;
        font-family: 'Source Sans Pro', sans-serif;
        height: 100vh;
        cursor: pointer;
        user-select: none;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    
    .header {{
        display: flex; align-items: center; padding: 60px 32px 24px 32px; position: relative;
    }}
    
    .logo-img {{
        height: 90px; 
        width: auto;
        object-fit: contain;
        margin-right: 24px;
        display: block;
    }}
    .fallback-logo {{
        width: 60px; height: 90px; background-color: #111; color: white;
        display: flex; align-items: center; justify-content: center;
        font-size: 40px; font-weight: bold; margin-right: 24px; border-radius: 8px;
    }}
    
    .header-text h1 {{ 
        margin: 0; font-size: 42px; color: #1C1B1F; font-weight: 700; letter-spacing: 1px; line-height: 1.1;
    }}
    
    .tagline {{ 
        margin: 6px 0 0 0; font-size: 16px; color: #6750A4; font-weight: 600; 
        letter-spacing: 0.5px; font-style: italic;
        background: linear-gradient(90deg, rgba(103,80,164,0.1), transparent);
        padding: 4px 12px; border-left: 3px solid #6750A4; display: inline-block;
    }}

    /* Tooltip Styling */
    .info-container {{
        margin-left: auto;
        position: relative;
        display: flex;
        align-items: center;
        cursor: help;
    }}
    .info-icon {{
        font-size: 15px;
        color: #6750A4;
        font-weight: 600;
        background: #F3EDF7;
        padding: 8px 18px;
        border-radius: 20px;
        border: 1px solid #CAC4D0;
        transition: background 0.2s ease, transform 0.1s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .info-icon:hover {{
        background: #EADDFF;
        transform: translateY(-1px);
    }}
    .info-tooltip {{
        visibility: hidden;
        opacity: 0;
        width: 380px;
        background-color: #1C1B1F;
        color: #F4F0FF;
        text-align: left;
        border-radius: 12px;
        padding: 20px;
        position: absolute;
        z-index: 10;
        top: 130%;
        right: 0;
        font-size: 15px;
        line-height: 1.6;
        font-weight: 400;
        box-shadow: 0 12px 32px rgba(0,0,0,0.25);
        transition: opacity 0.3s ease, visibility 0.3s ease;
        cursor: default;
    }}
    /* Tooltip Arrow */
    .info-tooltip::after {{
        content: "";
        position: absolute;
        bottom: 100%;
        right: 45px;
        margin-left: -5px;
        border-width: 8px;
        border-style: solid;
        border-color: transparent transparent #1C1B1F transparent;
    }}
    .info-container:hover .info-tooltip {{
        visibility: visible;
        opacity: 1;
    }}

    .card-container {{
        padding: 0 24px; display: flex; justify-content: center; align-items: center; flex-grow: 1;
    }}
    .card {{
        background: #FFFFFF; border: 1px solid #CAC4D0; border-radius: 32px;
        box-shadow: 0 12px 24px rgba(0,0,0,0.08); overflow: hidden;
        max-width: 800px; width: 100%;
    }}
    .card-gradient {{
        height: 8px; width: 100%; background: linear-gradient(90deg, #D0BCFF, #6750A4, #D0BCFF);
    }}
    .card-content {{ padding: 48px 40px; text-align: center; }}
    .pill {{
        display: inline-block; background: #F3EDF7; color: #6750A4;
        font-size: 11px; font-weight: bold; letter-spacing: 1.5px;
        padding: 6px 16px; border-radius: 8px; margin-bottom: 32px;
    }}
    
    .theme-text {{
        font-family: 'Playfair Display', serif; font-size: 36px; font-weight: 700;
        color: #111111; line-height: 1.3; margin: 0 0 24px 0;
    }}
    
    .divider {{
        width: 60px; height: 3px; background-color: #D4AF37; margin: 0 auto 24px auto; border-radius: 2px;
    }}
    
    .example-text {{ font-size: 20px; color: #555555; font-weight: 400; line-height: 1.6; margin: 0; }}
    .ex-label {{ font-weight: 700; color: #111111; letter-spacing: 1px; font-size: 15px; text-transform: uppercase; margin-right: 8px; }}

    .footer {{ text-align: center; padding: 24px; }}
    .footer-tap {{ color: #49454F; font-size: 14px; font-weight: 500; margin-bottom: 16px; }}
    .footer-brand {{ color: #938F99; font-size: 10px; font-weight: bold; letter-spacing: 1.5px; text-transform: uppercase; }}
    .footer-brand {{ color: #938F99; font-size: 10px; font-weight: bold; letter-spacing: 1.5px; text-transform: uppercase; }}
    
  /* --- Mobile Responsiveness --- */
    @media (max-width: 768px) {{
        .header {{ 
            padding: 48px 16px 16px 16px; 
        }}
        .logo-img {{ 
            margin-right: 12px; 
            height: 55px; 
            margin-bottom: 0;
        }}
        .header-text h1 {{ font-size: 26px; }}
        .tagline {{ font-size: 12px; }}
        
        /* Pin the button to the top right corner */
        .info-container {{ 
            position: absolute;
            top: 48px;
            right: 16px;
            margin: 0; 
        }}
        
        /* Shrink the button slightly to prevent overlapping the title */
        .info-icon {{
            padding: 12px 12px;
            font-size: 13px;
        }}
        
        /* Align the popup text box to the right edge */
        .info-tooltip {{ 
            width: 260px; 
            right: 0; 
            left: auto;
        }}
        .info-tooltip::after {{ 
            right: 20px; 
            left: auto;
        }}
        
        /* Shrink card padding and text */
        .card-container {{ padding: 0 16px; }}
        .card-content {{ padding: 32px 20px; }}
        .theme-text {{ font-size: 24px; margin-bottom: 16px; }}
        .example-text {{ font-size: 16px; }}
        .divider {{ margin: 0 auto 16px auto; }}
    }}
    </style>
    </style>

    <script>
    // Transition Logic
    let isTransitioning = false;
    function handleScreenClick() {{
        if (isTransitioning) return;
        isTransitioning = true;
        
        // Instantly hide the content to create a blank screen
        document.body.style.opacity = '0';
        
        // Wait exactly 3 seconds before triggering Streamlit
        setTimeout(() => {{
            window.parent.document.querySelector('div[data-testid="stButton"] button').click();
        }}, 0);
    }}
    </script>

    <div onclick="handleScreenClick()" data-render="{st.session_state.click_count}" style="height: 100%; display: flex; flex-direction: column;">
        <div class="header">
            {img_tag}
            <div class="header-text">
                <h1>IdeaTrix</h1>
                <p class="tagline">Let Ideas  flow at the speed of thoughts</p>
            </div>
            
            <!-- Information Tooltip Badge -->
            <div class="info-container" onclick="event.stopPropagation();">
                <div class="info-icon">ℹ️ How to use</div>
                <div class="info-tooltip">
                    Environment is designed to trigger ideas & inspire flow of creative energy from within you.<br><br> Be Clear on  your system / subsystem / component which needs improvement. Fuel your imagination by keeping the clear schematic in front of you.<br><br>Apply the ideation triggers for your problem one by one. Catch the idea spark, be fluid, don't overthink and enjoy the journey!
                </div>
            </div>
        </div>
        
        <div class="card-container">
            <div class="card">
                <div class="card-gradient"></div>
                <div class="card-content">
                    <div class="pill">IDEATION TRIGGER</div>
                    <div class="theme-text">{cleaned_theme}</div>
                    """

    if raw_example:
        android_ui_html += f"""
                    <div class="divider"></div>
                    <div class="example-text">
                        <span class="ex-label">EX:</span> {raw_example}
                    </div>
        """

    android_ui_html += """
                </div>
            </div>
        </div>

        <div class="footer">
            <div class="footer-tap">Tap anywhere for new inspiration</div>
            <div class="footer-brand">Brought to you by Knowledge-Station</div>
        </div>
    </div>
    """
    
    # 5. Display the custom component
    components.html(android_ui_html, height=800, scrolling=False)

except FileNotFoundError:
    st.error("Error: Could not find the CSV file. Please make sure 'Idea-Triggers-Tools_T_Android.csv' is in the exact same folder as this script.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
