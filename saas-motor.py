import os
import openai
import pandas as pd
import streamlit as strl
import io

strl.sidebar.title("⚙️ Einstellungen")

user_key = strl.sidebar.text_input(
    "Dein OpenAI API Key (optional)", 
    type="password",
    help="Wenn du keinen Key hast, nutzt die App die Demo-Version."
)

if user_key:
    MEIN_API_KEY = user_key
    strl.sidebar.success("Eigener API-Key aktiv! 🔑")
else:
    MEIN_API_KEY = os.environ.get("OPENAI_API_KEY")
    if MEIN_API_KEY:
        strl.sidebar.info("Demo-Modus aktiv 💡")

if not MEIN_API_KEY:
    strl.error("❌ API Key missing! Please set the OPENAI_API_KEY environment variable or enter your own.")
    strl.stop()

client = openai.OpenAI(api_key=MEIN_API_KEY)

strl.title("🚀 AI Multi-Channel Content Generator")
strl.write("Generate high-converting content for LinkedIn, Twitter/X, and Instagram with a single click!")

thema = strl.text_input("What topic do you want to go viral with today?", placeholder="e.g., Why sleep is the ultimate business cheat code")

if strl.button("Generate Content Plan ✨"):
    if not thema.strip():
        strl.error("Please enter a topic first!")
    else:
        with strl.spinner("AI is crafting your global content... Please wait..."):
            
            prompt_linkedin = "Write a professional LinkedIn post about the topic. Use clean line breaks, a highly engaging hook at the beginning, and end with 3 relevant business hashtags."
            prompt_twitter = "Write a short, viral tweet about the topic. Maximum 250 characters. Be direct, punchy, and do not use hashtags."
            prompt_instagram = "Write a casual and motivating Instagram caption about the topic. Use plenty of relevant emojis and a strong call-to-action at the end."

            ai_linkedin = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": prompt_linkedin}, {"role": "user", "content": thema}])
            ai_twitter = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": prompt_twitter}, {"role": "user", "content": thema}])
            ai_instagram = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "system", "content": prompt_instagram}, {"role": "user", "content": thema}])

            text_li = ai_linkedin.choices[0].message.content
            text_tw = ai_twitter.choices[0].message.content
            text_ig = ai_instagram.choices[0].message.content

            daten = {
                "Platform": ["LinkedIn", "Twitter/X", "Instagram"],
                "Content-Text": [text_li, text_tw, text_ig],
                "Status": ["Ready to Post", "Ready to Post", "Ready to Post"]
            }
            df = pd.DataFrame(daten)
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Content Plan')
            buffer.seek(0)
            
            strl.success("BOOM! Your content is ready to scale.")
            
            strl.download_button(
                label="📥 Download Excel Report",
                data=buffer,
                file_name=f"content_plan_{thema.lower().replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            strl.markdown("---")
            strl.subheader("📢 LinkedIn Post")
            strl.info(text_li)
            
            strl.subheader("🐦 Twitter Tweet")
            strl.warning(text_tw)
            
            strl.subheader("📸 Instagram Caption")
            strl.success(text_ig)
            
            strl.balloons()