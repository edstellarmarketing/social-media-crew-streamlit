import streamlit as st
import os
from crewai import Crew, Process
from utils.agents import create_agents
from utils.tasks import create_tasks

st.set_page_config(
    page_title="Social Media Image Search Crew",
    page_icon="🎨",
    layout="wide"
)

# Header
st.title("🎨 Social Media Image Search Crew")
st.markdown("Generate AI-powered social media post suggestions with images")

# Sidebar for inputs
with st.sidebar:
    st.header("Configuration")
    
    topic = st.text_area(
        "Topic",
        value="Leadership Development in Digital Transformation",
        height=100
    )
    
    openai_key = st.text_input("OpenAI API Key", type="password")
    serpapi_key = st.text_input("SerpAPI Key", type="password")
    
    generate_btn = st.button("🚀 Generate Posts", type="primary", use_container_width=True)

# Main content
if generate_btn:
    if not topic.strip():
        st.error("⚠️ Please enter a topic")
    elif not openai_key or not serpapi_key:
        st.error("⚠️ Please provide both API keys")
    else:
        with st.spinner("Generating... This may take 3-5 minutes..."):
            try:
                # Set API keys
                os.environ['OPENAI_API_KEY'] = openai_key
                os.environ['SERPAPI_KEY'] = serpapi_key
                
                # Create agents
                agents = create_agents()
                
                # Create tasks
                tasks = create_tasks(topic, agents)
                
                # Create crew
                crew = Crew(
                    agents=list(agents),
                    tasks=tasks,
                    process=Process.sequential,
                    verbose=True
                )
                
                # Execute
                result = crew.kickoff()
                
                # Display results
                st.success("✅ Generation Complete!")
                st.markdown("---")
                st.markdown(str(result))
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.info("👈 Enter your topic and API keys in the sidebar, then click Generate Posts")
    
    with st.expander("💡 What You'll Get"):
        st.markdown("""
        - 8 platform-specific social media posts
        - Images from Google, Pinterest, SlideShare
        - Ready-to-use captions & hashtags
        - Strategic content calendar
        - A/B testing recommendations
        - Engagement tactics & KPIs
        """)