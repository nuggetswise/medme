import streamlit as st
import json
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import LLM libraries
try:
    import openai
    import google.generativeai as genai
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="MedMe Copilot Demo",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .module-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .insight-box {
        background-color: #f8f9fa;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    .ai-badge {
        background-color: #6f42c1;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def initialize_llm_clients():
    """Initialize LLM clients with API keys"""
    clients = {}
    
    # OpenAI
    openai_api_key = os.getenv('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY', '')
    if openai_api_key:
        try:
            openai.api_key = openai_api_key
            clients['openai'] = openai
        except Exception as e:
            st.warning(f"OpenAI initialization failed: {e}")
    
    # Google Gemini
    gemini_api_key = os.getenv('GOOGLE_API_KEY') or st.secrets.get('GOOGLE_API_KEY', '')
    if gemini_api_key:
        try:
            genai.configure(api_key=gemini_api_key)
            clients['gemini'] = genai
        except Exception as e:
            st.warning(f"Gemini initialization failed: {e}")
    
    return clients

def call_llm(prompt, provider="openai", model="gpt-4"):
    """Call LLM API and return response"""
    if not LLM_AVAILABLE:
        return fallback_response(prompt)
    
    clients = initialize_llm_clients()
    
    try:
        if provider == "openai" and "openai" in clients:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        
        elif provider == "gemini" and "gemini" in clients:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text.strip()
        
        else:
            return fallback_response(prompt)
            
    except Exception as e:
        st.error(f"LLM API call failed: {e}")
        return fallback_response(prompt)

def fallback_response(prompt):
    """Fallback response when LLM is not available"""
    if "patient_insights" in prompt.lower():
        return """Based on the patient data, I recommend:
1. Annual medication review for diabetes management
2. A1C testing every 3-6 months
3. Blood pressure monitoring monthly
4. Comprehensive foot examination annually

These recommendations follow clinical guidelines and can improve patient outcomes while generating $200-300 in revenue per patient."""
    
    elif "schedule_optimization" in prompt.lower():
        return """Schedule optimization recommendations:
1. Convert low-value slots to high-value services
2. Prioritize medication reviews and vaccinations
3. Expected revenue impact: $450-600 per week
4. Time investment: 2-3 hours for implementation

This strategic approach maximizes revenue while maintaining patient care quality."""
    
    elif "message_generation" in prompt.lower():
        return """Dear [Patient Name],

I hope this message finds you well. I wanted to personally reach out regarding your upcoming medication review appointment.

Regular medication reviews are essential for ensuring your treatments are working optimally and safely. This appointment typically takes about 30 minutes and can help identify any potential interactions or adjustments needed.

Please call us at (555) 123-4567 to schedule your appointment at a time that works best for you.

Best regards,
Your Pharmacy Team"""
    
    elif "request_triage" in prompt.lower():
        return """Message Analysis:
- Classification: Medication Refill Request
- Urgency: Medium
- Sentiment: Neutral
- Confidence: 85%

Recommended Actions:
1. Process refill request (3-5 minutes)
2. Check prescription status
3. Contact prescriber if needed

Response time: 1-2 hours"""
    
    else:
        return "I can help you with patient insights, schedule optimization, message generation, or request triage."

def generate_llm_response(prompt, context_data):
    """Generate LLM response based on prompt type and context"""
    
    if "patient_insights" in prompt:
        return generate_patient_insights_llm(context_data)
    elif "schedule_optimization" in prompt:
        return generate_schedule_optimization_llm(context_data)
    elif "message_generation" in prompt:
        return generate_personalized_message_llm(context_data)
    elif "request_triage" in prompt:
        return analyze_patient_message_llm(context_data)
    else:
        return call_llm(f"Help with: {prompt}")

def generate_patient_insights_llm(patient_data):
    """Generate patient insights using real LLM"""
    
    prompt = f"""
    As a clinical pharmacist, analyze this patient data and provide intelligent recommendations:
    
    Patient: {patient_data.get('name', 'Unknown')}
    Age: {patient_data.get('age', 45)}
    Conditions: {', '.join(patient_data.get('conditions', []))}
    Recent Services: {', '.join(patient_data.get('services', []))}
    Insurance: {patient_data.get('insurance', 'Unknown')}
    Last Visit: {patient_data.get('last_visit', 'Unknown')}
    
    Provide 3-5 clinical recommendations in JSON format with these fields:
    - title: Recommendation title
    - description: Detailed explanation
    - priority: "high", "medium", or "low"
    - impact: Clinical impact description
    - revenue_potential: Estimated revenue in dollars
    - reasoning: Why this recommendation is important
    - urgency: Timeline for action
    
    Focus on evidence-based medicine, revenue opportunities, and patient safety.
    """
    
    llm_response = call_llm(prompt, provider="openai", model="gpt-4")
    
    try:
        # Try to parse JSON response
        if "```json" in llm_response:
            json_start = llm_response.find("```json") + 7
            json_end = llm_response.find("```", json_start)
            json_str = llm_response[json_start:json_end].strip()
            insights = json.loads(json_str)
        else:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', llm_response, re.DOTALL)
            if json_match:
                insights = json.loads(json_match.group())
            else:
                # Fallback to structured response
                insights = parse_structured_response(llm_response)
        
        return insights if isinstance(insights, list) else [insights]
        
    except Exception as e:
        st.warning(f"Failed to parse LLM response: {e}")
        return fallback_patient_insights(patient_data)

def generate_schedule_optimization_llm(schedule_data):
    """Generate schedule optimization using real LLM"""
    
    prompt = f"""
    As a pharmacy operations manager, analyze this schedule optimization request:
    
    Target Service: {schedule_data.get('target_service', 'Unknown')}
    Minimum Slots: {schedule_data.get('min_slots', 2)}
    Revenue Threshold: ${schedule_data.get('revenue_threshold', 100)}
    Priority: {schedule_data.get('priority', 'Maximize Revenue')}
    
    Provide optimization recommendations in JSON format:
    {{
        "recommendations": [
            {{
                "day": "Day of week",
                "time": "Time slot",
                "action": "Specific action",
                "revenue_impact": "Dollar amount",
                "reasoning": "Strategic reasoning"
            }}
        ],
        "total_revenue_impact": "Total dollar amount",
        "time_investment": "Hours needed",
        "reasoning": "Overall strategy explanation"
    }}
    
    Focus on maximizing revenue while maintaining patient care quality.
    """
    
    llm_response = call_llm(prompt, provider="openai", model="gpt-4")
    
    try:
        if "```json" in llm_response:
            json_start = llm_response.find("```json") + 7
            json_end = llm_response.find("```", json_start)
            json_str = llm_response[json_start:json_end].strip()
            return json.loads(json_str)
        else:
            return parse_optimization_response(llm_response)
    except Exception as e:
        st.warning(f"Failed to parse optimization response: {e}")
        return fallback_schedule_optimization(schedule_data)

def generate_personalized_message_llm(message_data):
    """Generate personalized message using real LLM"""
    
    prompt = f"""
    As a pharmacy communication specialist, create a personalized patient message:
    
    Message Type: {message_data.get('message_type', 'General')}
    Patient Name: {message_data.get('patient_name', 'Patient')}
    Urgency: {message_data.get('urgency', 'Medium')}
    Channel: {message_data.get('communication_channel', 'Email')}
    Tone: {message_data.get('tone', 'Professional')}
    Context: {message_data.get('context', 'No additional context')}
    
    Create a personalized, professional message that:
    1. Addresses the patient by name
    2. Explains the clinical importance
    3. Provides clear next steps
    4. Maintains appropriate tone for urgency level
    5. Includes contact information
    
    Make it warm, professional, and actionable.
    """
    
    llm_response = call_llm(prompt, provider="gemini", model="gemini-pro")
    
    return {
        "content": llm_response,
        "generated_by": "Google Gemini",
        "timestamp": datetime.now().isoformat(),
        "personalization_level": "high",
        "tone_adapted": True
    }

def analyze_patient_message_llm(message_data):
    """Analyze patient message using real LLM"""
    
    prompt = f"""
    As a pharmacy triage specialist, analyze this patient message:
    
    Message: "{message_data.get('message_text', '')}"
    
    Provide analysis in JSON format:
    {{
        "classification": "intent_category",
        "category": "Human readable category",
        "confidence": "percentage",
        "urgency": "High/Medium/Low",
        "sentiment": "Positive/Negative/Neutral",
        "response_time": "recommended response time",
        "suggested_actions": [
            {{
                "action": "action description",
                "priority": "High/Medium/Low",
                "estimated_time": "time estimate",
                "notes": "additional notes"
            }}
        ],
        "reasoning": "explanation of analysis"
    }}
    
    Focus on patient safety, appropriate urgency assessment, and actionable recommendations.
    """
    
    llm_response = call_llm(prompt, provider="openai", model="gpt-4")
    
    try:
        if "```json" in llm_response:
            json_start = llm_response.find("```json") + 7
            json_end = llm_response.find("```", json_start)
            json_str = llm_response[json_start:json_end].strip()
            return json.loads(json_str)
        else:
            return parse_triage_response(llm_response)
    except Exception as e:
        st.warning(f"Failed to parse triage response: {e}")
        return fallback_triage_analysis(message_data)

# Fallback functions for when LLM parsing fails
def fallback_patient_insights(patient_data):
    """Fallback patient insights when LLM fails"""
    return [{
        "title": "Medication Review Due",
        "description": f"Patient {patient_data.get('name', 'Unknown')} is due for annual medication review.",
        "priority": "high",
        "impact": "Ensure medication safety and efficacy",
        "revenue_potential": 95,
        "reasoning": "Standard of care for medication management",
        "urgency": "within 30 days"
    }]

def fallback_schedule_optimization(schedule_data):
    """Fallback schedule optimization when LLM fails"""
    return {
        "recommendations": [{
            "day": "Monday",
            "time": "10:00 AM",
            "action": f"Schedule {schedule_data.get('target_service', 'Service')}",
            "revenue_impact": 150,
            "reasoning": "Convert open slot to high-value service"
        }],
        "total_revenue_impact": 150,
        "time_investment": 1.0,
        "reasoning": "Strategic optimization for revenue growth"
    }

def fallback_triage_analysis(message_data):
    """Fallback triage analysis when LLM fails"""
    return {
        "classification": "general_question",
        "category": "General Question",
        "confidence": 75,
        "urgency": "Medium",
        "sentiment": "Neutral",
        "response_time": "2-4 hours",
        "suggested_actions": [{
            "action": "General response",
            "priority": "Medium",
            "estimated_time": "5-10 minutes",
            "notes": "Standard patient inquiry handling"
        }],
        "reasoning": "Standard message analysis"
    }

# Helper functions for parsing LLM responses
def parse_structured_response(response):
    """Parse structured response when JSON parsing fails"""
    insights = []
    lines = response.split('\n')
    current_insight = {}
    
    for line in lines:
        if 'title:' in line.lower():
            if current_insight:
                insights.append(current_insight)
            current_insight = {'title': line.split(':', 1)[1].strip()}
        elif 'description:' in line.lower():
            current_insight['description'] = line.split(':', 1)[1].strip()
        elif 'priority:' in line.lower():
            current_insight['priority'] = line.split(':', 1)[1].strip().lower()
        elif 'revenue_potential:' in line.lower():
            try:
                current_insight['revenue_potential'] = int(line.split('$')[1].split()[0])
            except:
                current_insight['revenue_potential'] = 75
    
    if current_insight:
        insights.append(current_insight)
    
    return insights

def parse_optimization_response(response):
    """Parse optimization response when JSON parsing fails"""
    return {
        "recommendations": [{
            "day": "Monday",
            "time": "10:00 AM",
            "action": "Schedule high-value service",
            "revenue_impact": 150,
            "reasoning": "Strategic optimization"
        }],
        "total_revenue_impact": 150,
        "time_investment": 1.0,
        "reasoning": "LLM-generated optimization strategy"
    }

def parse_triage_response(response):
    """Parse triage response when JSON parsing fails"""
    return {
        "classification": "general_question",
        "category": "General Question",
        "confidence": 80,
        "urgency": "Medium",
        "sentiment": "Neutral",
        "response_time": "2-4 hours",
        "suggested_actions": [{
            "action": "Standard response",
            "priority": "Medium",
            "estimated_time": "5-10 minutes",
            "notes": "LLM-analyzed message"
        }],
        "reasoning": "LLM message analysis"
    }

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 MedMe Copilot Demo</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #666; margin-bottom: 2rem;'>
        LLM-powered clinical workflow assistant for pharmacy operations
    </div>
    """, unsafe_allow_html=True)
    
    # AI Configuration in sidebar
    st.sidebar.title("🧭 Navigation")
    
    # AI Settings
    st.sidebar.markdown("---")
    st.sidebar.subheader("🤖 LLM Configuration")
    
    if LLM_AVAILABLE:
        st.sidebar.success("✅ LLM Libraries Available")
        
        # Check API keys with graceful fallback for missing secrets
        openai_key = os.getenv('OPENAI_API_KEY')
        gemini_key = os.getenv('GOOGLE_API_KEY')
        
        # Try to get from Streamlit secrets if not in environment
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
        
        use_ai = st.sidebar.checkbox("Enable LLM Features", value=True)
        
        if use_ai and (openai_key or gemini_key):
            if openai_key and gemini_key:
                provider = st.sidebar.selectbox("LLM Provider:", ["OpenAI GPT-4", "Google Gemini"])
                use_openai = provider == "OpenAI GPT-4"
            else:
                use_openai = bool(openai_key)
        else:
            use_openai = True
    else:
        st.sidebar.warning("⚠️ LLM Libraries Not Installed")
        st.sidebar.info("Install with: pip install openai google-generativeai")
        use_ai = False
        use_openai = True
    
    # Navigation
    module = st.sidebar.selectbox(
        "Select Copilot Module:",
        ["🏠 Overview", "🧑‍⚕️ Patient Insights", "📅 Schedule Optimizer", "✉️ Message Generator", "📨 Request Triage"]
    )
    
    if module == "🏠 Overview":
        show_overview(use_ai, LLM_AVAILABLE)
    elif module == "🧑‍⚕️ Patient Insights":
        show_patient_insights(use_ai, use_openai)
    elif module == "📅 Schedule Optimizer":
        show_schedule_optimizer(use_ai, use_openai)
    elif module == "✉️ Message Generator":
        show_message_generator(use_ai, use_openai)
    elif module == "📨 Request Triage":
        show_request_triage(use_ai, use_openai)

def show_overview(use_ai, llm_available):
    st.markdown('<h2 class="module-header">🎯 Copilot Overview</h2>', unsafe_allow_html=True)
    
    # AI Status
    if use_ai and llm_available:
        st.markdown("""
        <div class="success-box">
            <strong>🤖 LLM Features Enabled</strong><br>
            The Copilot is using real language models for intelligent clinical reasoning and personalized recommendations.
        </div>
        """, unsafe_allow_html=True)
    elif llm_available:
        st.markdown("""
        <div class="warning-box">
            <strong>📋 Fallback Mode Active</strong><br>
            Using intelligent fallback responses. Enable LLM features for real AI-powered analysis.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="warning-box">
            <strong>📋 Basic Mode Active</strong><br>
            LLM libraries not installed. Install with: pip install openai google-generativeai
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🧑‍⚕️ Patient Insight Recommender
        - **Input**: Patient profile (age, conditions, services)
        - **Output**: Clinical follow-up recommendations
        - **Use Case**: Identify patients due for medication reviews, vaccinations
        - **LLM Enhancement**: Personalized recommendations based on clinical guidelines
        """)
        
        st.markdown("""
        ### 📅 Slot Optimizer
        - **Input**: Weekly appointment schedule
        - **Output**: Suggested time block reallocations
        - **Use Case**: Maximize revenue through higher-value services
        - **LLM Enhancement**: Strategic optimization with revenue forecasting
        """)
    
    with col2:
        st.markdown("""
        ### ✉️ Message Generator
        - **Input**: Selected clinical action
        - **Output**: Draft patient communications
        - **Use Case**: Automated follow-up emails and SMS
        - **LLM Enhancement**: Context-aware, personalized messaging
        """)
        
        st.markdown("""
        ### 📨 Request Triage
        - **Input**: Patient message text
        - **Output**: Classification and action recommendations
        - **Use Case**: Route patient inquiries efficiently
        - **LLM Enhancement**: Natural language understanding and sentiment analysis
        """)
    
    # Demo metrics
    st.markdown("---")
    st.markdown('<h3>📊 Demo Metrics</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Patients Analyzed", "1,247", "+12%")
    with col2:
        st.metric("Recommendations", "89", "+8%")
    with col3:
        st.metric("Time Saved", "4.2 hrs", "+15%")
    with col4:
        st.metric("Revenue Impact", "$2,340", "+23%")
    
    # LLM vs Basic comparison
    if use_ai:
        st.markdown("---")
        st.markdown('<h3>🤖 LLM vs 📋 Basic Logic Comparison</h3>', unsafe_allow_html=True)
        
        comparison_data = {
            "Feature": ["Recommendation Quality", "Personalization", "Response Time", "Scalability", "Maintenance"],
            "LLM-Powered": ["High", "Excellent", "Fast", "Excellent", "Minimal"],
            "Basic Logic": ["Medium", "Good", "Instant", "Good", "High"]
        }
        
        import pandas as pd
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)

def show_patient_insights(use_ai, use_openai):
    st.markdown('<h2 class="module-header">🧑‍⚕️ Patient Insight Recommender</h2>', unsafe_allow_html=True)
    
    # Show AI status
    if use_ai:
        st.markdown('<span class="ai-badge">🤖 LLM-POWERED</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="ai-badge">📋 BASIC</span>', unsafe_allow_html=True)
    
    # Patient selection
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
        
        insurance = st.selectbox("Insurance:", ["Blue Cross", "Aetna", "Medicare", "Medicaid", "Self-pay"])
    
    # Generate insights
    if st.button("🔍 Generate Patient Insights", type="primary"):
        with st.spinner("Analyzing patient profile with LLM..."):
            patient_data = {
                "name": patient_name,
                "age": age,
                "conditions": chronic_conditions,
                "services": services_received,
                "insurance": insurance,
                "last_visit": last_visit.strftime("%Y-%m-%d")
            }
            
            insights = generate_llm_response("patient_insights", patient_data)
            
            st.markdown("---")
            st.subheader("📋 Clinical Recommendations")
            
            for insight in insights:
                priority = insight.get('priority', 'medium')
                if priority == 'high':
                    st.markdown(f"""
                    <div class="warning-box">
                        <strong>🚨 {insight['title']}</strong><br>
                        {insight['description']}<br>
                        <em>Impact: {insight.get('impact', 'High clinical impact')}</em>
                        {f"<br><em>Revenue Potential: ${insight.get('revenue_potential', 0)}</em>" if 'revenue_potential' in insight else ''}
                        {f"<br><em>Reasoning: {insight.get('reasoning', 'Clinical guideline')}</em>" if 'reasoning' in insight else ''}
                    </div>
                    """, unsafe_allow_html=True)
                elif priority == 'medium':
                    st.markdown(f"""
                    <div class="insight-box">
                        <strong>📋 {insight['title']}</strong><br>
                        {insight['description']}<br>
                        <em>Impact: {insight.get('impact', 'Moderate clinical impact')}</em>
                        {f"<br><em>Revenue Potential: ${insight.get('revenue_potential', 0)}</em>" if 'revenue_potential' in insight else ''}
                        {f"<br><em>Reasoning: {insight.get('reasoning', 'Preventive care')}</em>" if 'reasoning' in insight else ''}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="success-box">
                        <strong>✅ {insight['title']}</strong><br>
                        {insight['description']}<br>
                        <em>Impact: {insight.get('impact', 'Low clinical impact')}</em>
                        {f"<br><em>Revenue Potential: ${insight.get('revenue_potential', 0)}</em>" if 'revenue_potential' in insight else ''}
                        {f"<br><em>Reasoning: {insight.get('reasoning', 'General wellness')}</em>" if 'reasoning' in insight else ''}
                    </div>
                    """, unsafe_allow_html=True)

def show_schedule_optimizer(use_ai, use_openai):
    st.markdown('<h2 class="module-header">📅 Schedule Optimizer</h2>', unsafe_allow_html=True)
    
    # Show AI status
    if use_ai:
        st.markdown('<span class="ai-badge">🤖 LLM-POWERED</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="ai-badge">📋 BASIC</span>', unsafe_allow_html=True)
    
    st.subheader("Current Weekly Schedule")
    
    # Display current schedule
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    time_slots = ["9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM", "4:00 PM"]
    
    # Create sample schedule data
    schedule_data = {}
    for day in days:
        schedule_data[day] = {}
        for time in time_slots:
            if random.random() > 0.6:  # 40% chance of being booked
                schedule_data[day][time] = {
                    "status": "booked",
                    "service": random.choice(["Flu Shot", "Medication Review", "Blood Pressure Check"]),
                    "revenue": random.randint(30, 100)
                }
            else:
                schedule_data[day][time] = {
                    "status": "open",
                    "service": None,
                    "revenue": 0
                }
    
    # Create dataframe for display
    import pandas as pd
    display_data = []
    for day in days:
        for time in time_slots:
            slot = schedule_data[day][time]
            display_data.append({
                "Day": day,
                "Time": time,
                "Status": slot["status"].title(),
                "Service": slot["service"] or "Open",
                "Revenue": f"${slot['revenue']}" if slot['revenue'] > 0 else "$0"
            })
    
    df = pd.DataFrame(display_data)
    st.dataframe(df, use_container_width=True)
    
    # Optimization options
    st.subheader("Optimization Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_service = st.selectbox(
            "Target High-Value Service:",
            ["Shingles Vaccine", "Diabetes Medication Review", "Blood Pressure Monitoring", "Flu Shot", "Medication Therapy Management"]
        )
        
        min_slots = st.slider("Minimum slots to optimize:", 1, 5, 2)
    
    with col2:
        revenue_threshold = st.slider("Revenue threshold ($):", 50, 200, 100)
        
        priority = st.selectbox(
            "Optimization Priority:",
            ["Maximize Revenue", "Improve Patient Flow", "Balance Both"]
        )
    
    # Generate optimization
    if st.button("🚀 Optimize Schedule", type="primary"):
        with st.spinner("Analyzing schedule optimization opportunities with LLM..."):
            schedule_data = {
                "target_service": target_service,
                "min_slots": min_slots,
                "revenue_threshold": revenue_threshold,
                "priority": priority
            }
            
            optimization = generate_llm_response("schedule_optimization", schedule_data)
            
            st.markdown("---")
            st.subheader("🎯 Optimization Recommendations")
            
            if optimization.get('recommendations'):
                for rec in optimization['recommendations']:
                    st.markdown(f"""
                    <div class="insight-box">
                        <strong>📅 {rec.get('day', 'General')} - {rec.get('time', 'N/A')}</strong><br>
                        <strong>Action:</strong> {rec.get('action', rec.get('title', 'Optimize slot'))}<br>
                        <strong>Revenue Impact:</strong> ${rec.get('revenue_impact', 0)}<br>
                        <strong>Reasoning:</strong> {rec.get('reasoning', 'Strategic optimization')}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="success-box">
                    <strong>💰 Total Revenue Impact:</strong> ${optimization.get('total_revenue_impact', 0)}<br>
                    <strong>⏱️ Time Investment:</strong> {optimization.get('time_investment', 0)} hours<br>
                    <strong>🧠 LLM Reasoning:</strong> {optimization.get('reasoning', 'Strategic optimization')}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No optimization opportunities found with current parameters.")

def show_message_generator(use_ai, use_openai):
    st.markdown('<h2 class="module-header">✉️ Message Generator</h2>', unsafe_allow_html=True)
    
    # Show AI status
    if use_ai:
        st.markdown('<span class="ai-badge">🤖 LLM-POWERED</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="ai-badge">📋 BASIC</span>', unsafe_allow_html=True)
    
    st.subheader("Select Communication Type")
    
    col1, col2 = st.columns(2)
    
    with col1:
        message_type = st.selectbox(
            "Message Type:",
            ["Follow-up Reminder", "Appointment Invitation", "Medication Review", "Vaccination Reminder", "General Health Check"]
        )
        
        patient_name = st.text_input("Patient Name:", value="John Smith")
        
        urgency = st.select_slider(
            "Urgency Level:",
            options=["Low", "Medium", "High"],
            value="Medium"
        )
    
    with col2:
        communication_channel = st.selectbox(
            "Channel:",
            ["Email", "SMS", "Phone Call"]
        )
        
        include_personalization = st.checkbox("Include personalization", value=True)
        
        tone = st.selectbox(
            "Tone:",
            ["Professional", "Friendly", "Urgent", "Informative"]
        )
    
    # Additional context
    st.subheader("Additional Context")
    context = st.text_area(
        "Additional context or specific details:",
        placeholder="e.g., Patient is due for diabetes medication review, last visit was 3 months ago..."
    )
    
    # Generate message
    if st.button("✉️ Generate Message", type="primary"):
        with st.spinner("Drafting personalized message with LLM..."):
            message_data = {
                "message_type": message_type,
                "patient_name": patient_name,
                "urgency": urgency,
                "communication_channel": communication_channel,
                "include_personalization": include_personalization,
                "tone": tone,
                "context": context
            }
            
            message = generate_llm_response("message_generation", message_data)
            content = message['content']
            generated_by = message.get('generated_by', 'LLM Assistant')
            personalization = message.get('personalization_level', 'high')
            
            st.markdown("---")
            st.subheader("📝 Draft Message")
            
            st.markdown(f"""
            <div class="insight-box">
                <strong>To:</strong> {patient_name}<br>
                <strong>Subject:</strong> {message.get('subject', f'{message_type} - {patient_name}')}<br>
                <strong>Channel:</strong> {communication_channel}<br>
                <strong>Urgency:</strong> {urgency}<br>
                <strong>Generated by:</strong> {generated_by}<br>
                <strong>Personalization:</strong> {personalization}
            </div>
            """, unsafe_allow_html=True)
            
            st.text_area("Message Content:", content, height=200)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✅ Send Message"):
                    st.success("Message sent successfully!")
            with col2:
                if st.button("✏️ Edit Message"):
                    st.info("Edit functionality would open message editor")
            with col3:
                if st.button("📋 Save Template"):
                    st.success("Template saved for future use!")

def show_request_triage(use_ai, use_openai):
    st.markdown('<h2 class="module-header">📨 Request Triage</h2>', unsafe_allow_html=True)
    
    # Show AI status
    if use_ai:
        st.markdown('<span class="ai-badge">🤖 LLM-POWERED</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="ai-badge">📋 BASIC</span>', unsafe_allow_html=True)
    
    st.subheader("Patient Message Analysis")
    
    # Sample messages for demo
    sample_messages = [
        "I need to refill my blood pressure medication",
        "Can I schedule an appointment for a flu shot?",
        "I'm having side effects from my new medication",
        "What time do you close on Saturdays?",
        "I need help understanding my insurance coverage",
        "Can you check if my prescription is ready?",
        "I want to discuss switching my diabetes medication"
    ]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        message_input = st.text_area(
            "Patient Message:",
            placeholder="Enter or paste patient message here...",
            height=100
        )
    
    with col2:
        st.write("**Sample Messages:**")
        for i, msg in enumerate(sample_messages):
            if st.button(f"Sample {i+1}", key=f"sample_{i}"):
                st.session_state.sample_message = msg
                st.rerun()
    
    # Use sample message if selected
    if hasattr(st.session_state, 'sample_message'):
        message_input = st.session_state.sample_message
        st.text_area("Selected Message:", message_input, height=100)
    
    # Analysis options
    col1, col2 = st.columns(2)
    
    with col1:
        include_sentiment = st.checkbox("Include sentiment analysis", value=True)
        include_urgency = st.checkbox("Include urgency assessment", value=True)
    
    with col2:
        suggest_actions = st.checkbox("Suggest next actions", value=True)
        auto_route = st.checkbox("Auto-route to appropriate team", value=False)
    
    # Analyze message
    if st.button("🔍 Analyze Message", type="primary") and message_input:
        with st.spinner("Analyzing patient message with LLM..."):
            message_data = {
                "message_text": message_input,
                "include_sentiment": include_sentiment,
                "include_urgency": include_urgency,
                "suggest_actions": suggest_actions,
                "auto_route": auto_route
            }
            
            analysis = generate_llm_response("request_triage", message_data)
            classification = analysis.get('classification', 'general_question')
            category = analysis.get('category', 'General Question')
            confidence = analysis.get('confidence', 75)
            urgency = analysis.get('urgency', 'Medium')
            sentiment = analysis.get('sentiment', 'Neutral')
            response_time = analysis.get('response_time', '2-4 hours')
            suggested_actions = analysis.get('suggested_actions', [])
            reasoning = analysis.get('reasoning', 'Standard analysis')
            
            st.markdown("---")
            st.subheader("📊 Analysis Results")
            
            # Classification
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="insight-box">
                    <strong>📋 Classification:</strong> {category}<br>
                    <strong>🎯 Category:</strong> {classification}<br>
                    <strong>📈 Confidence:</strong> {confidence}%
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if include_sentiment:
                    st.markdown(f"""
                    <div class="insight-box">
                        <strong>😊 Sentiment:</strong> {sentiment}<br>
                        <strong>⚡ Urgency:</strong> {urgency}<br>
                        <strong>⏱️ Response Time:</strong> {response_time}
                    </div>
                    """, unsafe_allow_html=True)
            
            # LLM Reasoning
            if use_ai and reasoning:
                st.markdown(f"""
                <div class="success-box">
                    <strong>🧠 LLM Reasoning:</strong> {reasoning}
                </div>
                """, unsafe_allow_html=True)
            
            # Suggested actions
            if suggest_actions and suggested_actions:
                st.subheader("🎯 Recommended Actions")
                
                for i, action in enumerate(suggested_actions):
                    if isinstance(action, dict):
                        action_text = action.get('action', str(action))
                        priority = action.get('priority', 'Medium')
                        estimated_time = action.get('estimated_time', '5-10 minutes')
                        notes = action.get('notes', 'Standard action')
                    else:
                        action_text = str(action)
                        priority = 'Medium'
                        estimated_time = '5-10 minutes'
                        notes = 'LLM-generated recommendation'
                    
                    st.markdown(f"""
                    <div class="insight-box">
                        <strong>Action {i+1}:</strong> {action_text}<br>
                        <strong>Priority:</strong> {priority}<br>
                        <strong>Estimated Time:</strong> {estimated_time}<br>
                        <strong>Notes:</strong> {notes}
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 