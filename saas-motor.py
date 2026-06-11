
import streamlit as strl
import openai
import os
import pandas as pd
import io

# 1. Sidebar for settings
strl.sidebar.title("⚙️ Settings")

# 2. Input field for the user's own key
user_key = strl.sidebar.text_input(
    "Your OpenAI API Key (optional)", 
    type="password",
    help="If you don't have a key, the app will run in Demo Mode with limitations."
)

# 3. Logic: Which key is being used?
if user_key:
    MEIN_API_KEY = user_key
    strl.sidebar.success("Custom API Key active! 🔑")
else:
    # Holt deinen Key direkt aus den sicheren Streamlit-Secrets
    try:
        MEIN_API_KEY = strl.secrets["OPENAI_API_KEY"]
        strl.sidebar.info("Demo Mode active 💡")
    except Exception:
        MEIN_API_KEY = None
# 4. Error handling if no key is available at all
if not MEIN_API_KEY:
    strl.error("❌ API Key missing! Please set the OPENAI_API_KEY environment variable or enter your own.")
    strl.stop()

# 5. Start the client with the correct key
client = openai.OpenAI(api_key=MEIN_API_KEY)

# 6. Sidebar Selection Boxes
strl.sidebar.write("---")
platform = strl.sidebar.selectbox(
    "Target Platform",
    ["LinkedIn", "Twitter/X", "Instagram", "YouTube Shorts"]
)

tone = strl.sidebar.selectbox(
    "Tone of Voice",
    ["Professional", "Casual & Funny", "Aggressive & Viral", "Motivational"]
)

# Haupt-Branding & Titel
strl.title("🚀 AI Multi-Channel Content Generator")
strl.markdown("### *Scale your social media presence with data-driven AI solutions.*")
strl.write("---")

# Eine Willkommens- und Info-Box für ein Premium-Gefühl
strl.info(
    "💡 **How it works:** Enter your topic below, choose your target platform and tone of voice in the sidebar, "
    "and let the AI generate high-converting content instantly. You can export your final plan directly to Excel!"
)

# Wir erstellen zwei Spalten: Spalte 1 für den Input, Spalte 2 für den Output
col_input, col_output = strl.columns([1, 1.2], gap="large")

# --- LINKE SPALTE: EINGABE ---
with col_input:
    strl.subheader("📝 Content Strategy")
    thema = strl.text_input(
        "What topic do you want to go viral with today?", 
        placeholder="e.g., Why sleep is the ultimate business cheat code",
        help="Type in a core idea, a title, or a question."
    )
    
    # Der Button wird in der linken Spalte platziert
    generate_btn = strl.button("Generate Content Plan 📅", use_container_width=True)

# --- RECHTE SPALTE: ERGEBNIS & EXPORT ---
with col_output:
    strl.subheader("✨ Generated Masterpiece")
    
    if generate_btn:
        if not thema.strip():
            strl.error("Please enter a topic first!")
        else:
            with strl.spinner("AI is crafting your custom content... Please wait..."):
                
                # 1. Base Prompt Engineering based on platform
                if platform == "LinkedIn":
                    prompt = f"Write a {tone.lower()} LinkedIn post about the topic. Use clean line breaks, a highly engaging hook at the beginning, and end with 3 relevant business hashtags."
                elif platform == "Twitter/X":
                    prompt = f"Write a {tone.lower()} tweet about the topic. Maximum 250 characters. Be direct, punchy, and do not use hashtags."
                elif platform == "Instagram":
                    prompt = f"Write a {tone.lower()} Instagram caption about the topic. Use plenty of relevant emojis and a strong call-to-action at the end."
                elif platform == "YouTube Shorts":
                    prompt = f"Write a short, fast-paced, high-retention {tone.lower()} video script for YouTube Shorts about the topic. Include visual cues in brackets like [Show text on screen] and a hook within the first 3 seconds."

                # 2. BUDGET PROTECTION LOGIC (Check if custom key or demo key is used)
                demo_limit_active = False
                if not user_key:  # If the input field in the sidebar is empty
                    demo_limit_active = True
                    # We inject a restriction into the prompt to save your money!
                    prompt += " IMPORTANT: Since this is a short demo, you MUST limit your response to a maximum of 40 words and keep it very brief."

                # Call OpenAI with the prompt
                ai_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": thema}
                    ]
                )
                
                content_text = ai_response.choices[0].message.content
                
                # 3. Display Results & Warnings
                strl.markdown(f"**Target:** `{platform}` | **Tone:** `{tone}`")
                
                if demo_limit_active:
                    strl.warning("⚠️ **Demo Mode Limit Active:** The response was shortened to save API budget. To unlock unlimited length, please enter your own OpenAI API Key in the sidebar!")
                
                strl.info(content_text)
                # Create Excel structure
                daten = {
                    "Platform": [platform],
                    "Tone": [tone],
                    "Content-Text": [content_text],
                    "Status": ["Ready to Post"]
                }
                
                df = pd.DataFrame(daten)
                
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Content Plan')
                
                # Download Button direkt unter dem Text in der rechten Spalte
                strl.download_button(
                    label="📥 Download Content Plan (Excel)",
                    data=buffer.getvalue(),
                    file_name="ai_content_plan.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
    else:
        # Platzhalter-Nachricht, wenn noch kein Text generiert wurde
        strl.write("Your generated content and the Excel export link will appear here once you hit the generate button.")