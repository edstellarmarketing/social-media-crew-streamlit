import os
import gradio as gr
from crewai import Crew, Process
from datetime import datetime
from utils.agents import create_agents
from utils.tasks import create_tasks

# Topic suggestions
TOPIC_SUGGESTIONS = [
    "Leadership Development in Digital Transformation",
    "AI and Machine Learning for Corporate Training",
    "Effective Communication Skills for Executives",
    "Change Management in Uncertain Times",
    "Building High-Performance Teams",
    "Executive Coaching and Leadership Development",
    "Data-Driven Decision Making for Leaders",
    "Emotional Intelligence in Leadership",
    "Innovation and Creativity in Corporate Culture",
    "Strategic Planning for Business Growth",
    "Remote Team Management and Collaboration",
    "Diversity and Inclusion in the Workplace",
    "Agile Leadership and Transformation",
    "Employee Engagement and Retention Strategies",
    "Crisis Management and Business Continuity"
]

def generate_social_media_posts(topic, openai_key, serpapi_key, progress=gr.Progress()):
    """
    Main function to generate social media posts
    """
    if not topic or not topic.strip():
        return "⚠️ Please enter a topic"
    
    if not openai_key or not serpapi_key:
        return "⚠️ Please provide both OpenAI and SerpAPI keys"
    
    # Set API keys
    os.environ['OPENAI_API_KEY'] = openai_key
    os.environ['SERPAPI_KEY'] = serpapi_key
    
    try:
        progress(0, desc="Initializing agents...")
        
        # Create agents
        agents = create_agents()
        
        progress(0.2, desc="Creating tasks...")
        
        # Create tasks
        tasks = create_tasks(topic, agents)
        
        progress(0.3, desc="Setting up crew...")
        
        # Create crew
        crew = Crew(
            agents=list(agents),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        progress(0.4, desc="Executing crew (this may take 3-5 minutes)...")
        
        # Execute
        result = crew.kickoff()
        
        progress(1.0, desc="Complete!")
        
        # Format result
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_result = f"""
# Social Media Post Suggestions
**Topic:** {topic}
**Generated:** {timestamp}

---

{str(result)}

---

## Next Steps
1. Review the 8 post suggestions above
2. Customize captions for your brand voice
3. Download images from the provided URLs
4. Schedule posts according to the recommended calendar
5. Track engagement metrics as suggested
"""
        
        return formatted_result
        
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nPlease check your API keys and try again."

# Custom CSS
custom_css = """
.gradio-container {
    font-family: 'Arial', sans-serif;
}
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
.info-box {
    background-color: #f0f7ff;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #667eea;
    margin: 10px 0;
}
"""

# Create Gradio interface
with gr.Blocks(css=custom_css, title="Social Media Image Search Crew") as demo:
    
    gr.HTML("""
        <div class="main-header">
            <h1>🎨 Social Media Image Search Crew</h1>
            <p>Generate AI-powered social media post suggestions with images from multiple platforms</p>
        </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML("""
                <div class="info-box">
                    <h3>📋 How It Works</h3>
                    <ol>
                        <li>Enter your topic or select from suggestions</li>
                        <li>Provide your API keys (required)</li>
                        <li>Click "Generate Posts"</li>
                        <li>Wait 3-5 minutes for AI agents to work</li>
                        <li>Get 8 complete social media posts with images!</li>
                    </ol>
                </div>
            """)
            
            topic_input = gr.Dropdown(
                choices=TOPIC_SUGGESTIONS,
                label="📝 Select or Enter Topic",
                allow_custom_value=True,
                value=TOPIC_SUGGESTIONS[0],
                info="Choose a suggestion or type your own topic"
            )
            
            with gr.Accordion("🔑 API Configuration", open=True):
                openai_key = gr.Textbox(
                    label="OpenAI API Key",
                    type="password",
                    placeholder="sk-...",
                    info="Get your key from: https://platform.openai.com/api-keys"
                )
                
                serpapi_key = gr.Textbox(
                    label="SerpAPI Key",
                    type="password",
                    placeholder="Your SerpAPI key",
                    info="Get free key from: https://serpapi.com/manage-api-key"
                )
            
            submit_btn = gr.Button(
                "🚀 Generate Posts",
                variant="primary",
                size="lg"
            )
            
            gr.HTML("""
                <div class="info-box">
                    <h3>💡 What You'll Get</h3>
                    <ul>
                        <li>8 platform-specific social media posts</li>
                        <li>Images from Google, Pinterest, SlideShare</li>
                        <li>Ready-to-use captions & hashtags</li>
                        <li>Strategic content calendar</li>
                        <li>A/B testing recommendations</li>
                        <li>Engagement tactics & KPIs</li>
                    </ul>
                </div>
            """)
    
        with gr.Column(scale=2):
            output = gr.Markdown(
                label="📊 Results",
                value="Your results will appear here...",
                height=600
            )
    
    submit_btn.click(
        fn=generate_social_media_posts,
        inputs=[topic_input, openai_key, serpapi_key],
        outputs=output
    )
    
    gr.HTML("""
        <div style='text-align: center; margin-top: 20px; padding: 20px; background-color: #f5f5f5; border-radius: 8px;'>
            <h3>🔒 Privacy & Security</h3>
            <p>Your API keys are only used during this session and are never stored or logged.</p>
            <p>Built with ❤️ using CrewAI • Powered by OpenAI & SerpAPI</p>
        </div>
    """)

if __name__ == "__main__":
    demo.launch()