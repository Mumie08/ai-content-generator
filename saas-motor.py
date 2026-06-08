Python
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
    MEIN_API_KEY = os.environ.get("OPENAI_API_KEY")
    if MEIN_API_KEY:
        strl.sidebar.info("Demo Mode active 💡")

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

strl.title("🚀 AI Multi-Channel Content Generator")
strl.write("Generate high-converting content for your specific brand channels with a single click!")

thema = strl.text_input("What topic do you want to go viral with today?", placeholder="e.g., Why sleep is the ultimate business cheat code")

if strl.button("Generate Content Plan 📅"):
    if not thema.strip():
        strl.error("Please enter a topic first!")
    else:
        with strl.spinner("AI is crafting your custom content... Please wait..."):
            
            # Dynamic prompt engineering based on user selection
            if platform == "LinkedIn":
                prompt = f"Write a {tone.lower()} LinkedIn post about the topic. Use clean line breaks, a highly engaging hook at the beginning, and end with 3 relevant business hashtags."
            elif platform == "Twitter/X":
                prompt = f"Write a {tone.lower()} tweet about the topic. Maximum 250 characters. Be direct, punchy, and do not use hashtags."
            elif platform == "Instagram":
                prompt = f"Write a {tone.lower()} Instagram caption about the topic. Use plenty of relevant emojis and a strong call-to-action at the end."
            elif platform == "YouTube Shorts":
                prompt = f"Write a short, fast-paced, high-retention {tone.lower()} video script for YouTube Shorts about the topic. Include visual cues in brackets like [Show text on screen] and a hook within the first 3 seconds."

            # Call OpenAI with the single dynamic prompt
            ai_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": thema}
                ]
            )
            
            content_text = ai_response.choices[0].message.content
            
            # Display the result to the user
            strl.subheader(f"Your Generated Content ({platform} - {tone})")
            strl.write(content_text)
            
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
            
            # Download Button
            strl.download_button(
                label="📥 Download Content Plan (Excel)",
                data=buffer.getvalue(),
                file_name="ai_content_plan.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )