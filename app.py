import streamlit as st
import os
import json
from datetime import datetime, timedelta
import pandas as pd

# Page config
st.set_page_config(
    page_title="MedMe Copilot Demo",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .module-header {
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin-bottom: 2rem;
    }
    .ai-badge {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Check if AI libraries are available
try:
    import openai
    import google.generativeai as genai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

def initialize_ai_clients():
    """Initialize AI clients if API keys are available"""
    clients = {}
    
    # OpenAI client
    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key:
        try:
            openai_key = st.secrets.get('OPENAI_API_KEY', '')
        except:
            openai_key = ''
    
    if openai_key:
        try:
            openai.api_key = openai_key
            clients['openai'] = openai
        except Exception as e:
            st.error(f"OpenAI initialization error: {e}")
    
    # Google Gemini client
    gemini_key = os.getenv('GOOGLE_API_KEY')
    if not gemini_key:
        try:
            gemini_key = st.secrets.get('GOOGLE_API_KEY', '')
        except:
            gemini_key = ''
    
    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            clients['gemini'] = genai
        except Exception as e:
            st.error(f"Google Gemini initialization error: {e}")
    
    return clients

def call_ai(prompt, model="gpt-4"):  # Always try OpenAI first, fallback to Gemini
    """Make AI API call with error handling"""
    try:
        # OpenAI v1.x API usage
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        # Fallback to Gemini if OpenAI fails
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e2:
            st.error(f"AI API error: {e2}")
            return None

def generate_patient_insights_prompt(patient_data):
    """Generate patient insights using real AI"""
    prompt = f"""
    As an AI Copilot for MedMe Health's pharmacy platform, analyze this patient profile and provide actionable clinical recommendations.
    
    Patient Profile:
    - Name: {patient_data['name']}
    - Age: {patient_data['age']}
    - Chronic Conditions: {', '.join(patient_data['conditions'])}
    - Recent Services: {', '.join(patient_data['services'])}
    - Last Visit: {patient_data['last_visit']}
    
    Provide a structured response with:
    1. Clinical Recommendations (medication reviews, immunizations, screenings, etc.)
       - Each recommendation should be a clear, human-readable sentence or short paragraph, suitable for a clinical dashboard. Use bullet points if appropriate.
    2. Patient Engagement Opportunities (follow-ups, education)
    3. Risk Assessment (medication interactions, gaps in care)
    4. Next Steps (specific actions for pharmacy staff)
    5. Reasoning: Briefly explain which patient parameters most influenced your recommendations and why.
    
    Format as JSON with these keys: recommendations, engagement_opportunities, risk_assessment, next_steps, reasoning
    """
    
    return prompt

def parse_structured_response(response):
    """Parse AI response into structured format"""
    try:
        # Try to extract JSON from response
        if '{' in response and '}' in response:
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            return json.loads(json_str)
    except:
        pass
    
    # Fallback: return as text
    return {
        "recommendations": [response],
        "engagement_opportunities": [],
        "risk_assessment": [],
        "next_steps": [],
        "reasoning": ""
    }

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 MedMe Copilot Demo</h1>
        <p>AI-Powered Patient Insight Recommender for Pharmacy Clinical Services</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.title("🤖 Copilot Configuration")
    
    if AI_AVAILABLE:
        st.sidebar.success("✅ AI Libraries Available")
        openai_key = os.getenv('OPENAI_API_KEY')
        gemini_key = os.getenv('GOOGLE_API_KEY')
        if not openai_key:
            try:
                openai_key = st.secrets.get('OPENAI_API_KEY', '')
            except:
                openai_key = ''
        if not gemini_key:
            try:
                gemini_key = st.secrets.get('GOOGLE_API_KEY', '')
            except:
                gemini_key = ''
        if openai_key:
            st.sidebar.info("🔵 OpenAI API Ready")
        if gemini_key:
            st.sidebar.info("🟢 Google Gemini API Ready")
        if not openai_key and not gemini_key:
            st.sidebar.warning("⚠️ No API Keys Found")
            st.sidebar.info("Using fallback responses. Add API keys to .env or Streamlit secrets.")
        use_ai = st.sidebar.checkbox("Enable AI Features", value=True)
    else:
        st.sidebar.warning("⚠️ AI Libraries Not Installed")
        st.sidebar.info("Install with: pip install openai google-generativeai")
        use_ai = False
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Demo Focus")
    st.sidebar.info("🎯 **Patient Insight Recommender** - The core value driver for MedMe's pharmacy platform")
    show_patient_insights(use_ai)

def show_patient_insights(use_ai):
    st.markdown('<h2 class="module-header">🧑‍⚕️ Patient Insight Recommender</h2>', unsafe_allow_html=True)
    if use_ai:
        st.markdown('<span class="ai-badge">🤖 AI-POWERED</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="ai-badge">📋 BASIC</span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="success-box">
        <strong>🎯 Business Impact:</strong> This AI feature helps MedMe's 4,000+ pharmacy partners identify revenue opportunities 
        and improve patient outcomes through proactive clinical service recommendations.
    </div>
    """, unsafe_allow_html=True)
    st.subheader("Select Patient Profile")
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.selectbox(
            "Patient Name:",
            ["John Smith", "Sarah Johnson", "Michael Chen", "Emily Davis", "Robert Wilson"]
        )
        age = st.slider("Age:", 18, 85, 45)
        chronic_conditions = st.multiselect(
            "Chronic Conditions:",
            ["Diabetes", "Hypertension", "Asthma", "Heart Disease", "Arthritis", "None"],
            default=["Diabetes", "Hypertension"]
        )
    with col2:
        last_visit = st.date_input("Last Visit:", value=datetime.now() - timedelta(days=30))
        services_received = st.multiselect(
            "Recent Services:",
            ["Medication Review", "Flu Shot", "Blood Pressure Check", "Diabetes Screening", "None"],
            default=["Medication Review"]
        )
    if st.button("🔍 Generate AI Patient Insights", type="primary"):
        with st.spinner("Analyzing patient profile with AI Copilot..."):
            patient_data = {
                "name": patient_name,
                "age": age,
                "conditions": chronic_conditions,
                "services": services_received,
                "last_visit": last_visit.strftime("%Y-%m-%d")
            }
            if use_ai:
                prompt = generate_patient_insights_prompt(patient_data)
                response = call_ai(prompt)
                if response:
                    insights = parse_structured_response(response)
                else:
                    st.error("Failed to get AI response. Please check your API keys.")
                    return
            else:
                st.error("AI features disabled. Please enable AI features in the sidebar.")
                return
            st.markdown("---")
            st.subheader("📋 AI-Generated Clinical Recommendations")
            if insights.get('recommendations'):
                st.markdown("### 🏥 Clinical Recommendations")
                for rec in insights['recommendations']:
                    st.markdown(f"- {rec}")
            if insights.get('engagement_opportunities'):
                st.markdown("### 🤝 Patient Engagement")
                for eng in insights['engagement_opportunities']:
                    st.markdown(f"- {eng}")
            if insights.get('risk_assessment'):
                st.markdown("### ⚠️ Risk Assessment")
                for risk in insights['risk_assessment']:
                    st.markdown(f"- {risk}")
            if insights.get('next_steps'):
                st.markdown("### 📋 Next Steps")
                for step in insights['next_steps']:
                    st.markdown(f"- {step}")
            if insights.get('reasoning'):
                with st.expander("How did the AI Copilot generate these insights?"):
                    st.markdown(insights['reasoning'])

# Comment out other modules for now
# def show_overview(use_ai, llm_available):
#     pass

# def show_schedule_optimizer(use_ai, use_openai):
#     pass

# def show_message_generator(use_ai, use_openai):
#     pass

# def show_request_triage(use_ai, use_openai):
#     pass

if __name__ == "__main__":
    main() 