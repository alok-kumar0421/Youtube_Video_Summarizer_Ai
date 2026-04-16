import streamlit as st
from youtube_analyzer import build_youtube_agent

# ✅ PDF imports
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(
    page_title="YouTube Analyzer AI",
    layout="wide",
    page_icon="🎥"
)

# 🎯 Header
st.title("🎥 YouTube Analyzer Studio (AI Powered)")
st.markdown("Get insights, timestamps & summaries from any YouTube video 🚀")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    show_raw = st.checkbox("Show Raw Output", value=False)
    st.markdown("---")
    st.info("📌 Paste a YouTube link and click Analyze")

# ✅ PDF function
def create_pdf(content):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = []
    for line in content.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

# Cache agent
@st.cache_resource
def get_agent():
    return build_youtube_agent()

agent = get_agent()

# 🎥 Input Section
st.markdown("## 🔗 Enter YouTube Video URL")

video_url = st.text_input(
    "Paste URL here",
    placeholder="https://www.youtube.com/watch?v=..."
)

analyze_btn = st.button("🚀 Analyze Video")

# 🎬 Video Preview
if video_url:
    st.video(video_url)

# 🔍 Analysis
if analyze_btn:
    if not video_url:
        st.warning("⚠️ Please enter a valid YouTube URL")
    else:
        with st.spinner("🤖 Analyzing video... Please wait"):
            response = agent.run(f"Analyze this video: {video_url}")

        st.success("✅ Analysis Complete!")

        # Tabs
        tab1, tab2 = st.tabs(["📊 Analysis Report", "📄 Raw Output"])

        with tab1:
            st.markdown("### 📊 Detailed Analysis")
            st.markdown(response.content)

            # ✅ PDF Download
            pdf_file = create_pdf(response.content)

            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_file,
                file_name="youtube_analysis.pdf",
                mime="application/pdf"
            )

        with tab2:
            if show_raw:
                st.code(response.content)
            else:
                st.info("Enable 'Show Raw Output' from sidebar")

# Footer
st.markdown("---")
st.caption("Built with ❤️ by Alok Kumar using Streamlit + AI Agents")