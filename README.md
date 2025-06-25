# MedMe Copilot Demo

## Overview

This is a focused, AI-powered Patient Insight Recommender designed for MedMe Health's pharmacy platform. The app demonstrates how AI can help pharmacy staff proactively identify clinical opportunities and deliver personalized patient care at scale.

**Key Features:**
- Clean, business-friendly UI
- No insurance field, no revenue metrics, no LLM/provider selection
- Only the following patient profile fields: Name, Age, Chronic Conditions, Recent Services, Last Visit
- Generates clear, actionable clinical recommendations, patient engagement suggestions, risk assessments, and next steps
- Includes an "AI Reasoning" expander to show how the AI generated its insights

## How It Works
1. **Select Patient Profile:**
   - Name (dropdown)
   - Age (slider)
   - Chronic Conditions (multi-select)
   - Recent Services (multi-select)
   - Last Visit (date)
2. **Click "Generate AI Patient Insights"**
3. **Review Results:**
   - Clinical Recommendations (bulleted, human-readable)
   - Patient Engagement suggestions
   - Risk Assessment
   - Next Steps
   - "How did the AI Copilot generate these insights?" expander for transparency

## Why This Feature Matters for MedMe

> We built the AI-Powered Patient Insight Recommender to help MedMe's pharmacy partners proactively identify clinical opportunities and deliver more personalized patient care at scale. By analyzing key patient data—such as age, chronic conditions, recent services, and visit history—our feature generates actionable, context-aware recommendations for follow-up, risk management, and patient engagement.
>
> This tool directly supports MedMe's mission to streamline pharmacy workflows, improve patient outcomes, and unlock new clinical service revenue. It empowers pharmacy staff to move from reactive to proactive care, ensuring that no patient falls through the cracks and that every clinical opportunity is surfaced at the right time.

## Setup

1. Clone this repo and `cd` into the project directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your OpenAI and/or Google Gemini API keys to `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "sk-..."
   GOOGLE_API_KEY = "..."
   ```
4. Run the app:
   ```bash
   streamlit run app.py --server.port 8505
   ```

## Demo Workflow
- Change patient parameters and click the button to see how the AI adapts its recommendations.
- Use the "How did the AI Copilot generate these insights?" expander to show the AI's reasoning and context-awareness.

## Notes
- No insurance, revenue, or business impact metrics are shown.
- No LLM/provider selection is exposed to the user; the backend handles all AI logic.
- The app is designed for a quick, business-focused demo for product and hiring managers at MedMe.

## 🎯 Overview

This demo showcases intelligent automation features that enhance pharmacy efficiency and patient care through LLM-powered insights:

- **Patient Insight Recommender**: Identifies patients due for clinical follow-ups
- **Schedule Optimizer**: Maximizes revenue through strategic appointment scheduling
- **Message Generator**: Creates personalized patient communications
- **Request Triage**: Intelligently routes and prioritizes patient inquiries

## 🚀 Features

### 🤖 LLM-Powered Intelligence
- **Minimal Code Maintenance**: LLMs handle the complex reasoning
- **Clinical Knowledge**: Built-in medical guidelines and best practices
- **Natural Language Understanding**: Intelligent analysis of patient data and messages
- **Personalization**: Context-aware recommendations and messaging

### 📊 Key Modules

1. **Patient Insights**
   - Age and condition-based recommendations
   - Revenue impact analysis
   - Clinical priority scoring
   - Insurance-specific suggestions

2. **Schedule Optimization**
   - Revenue-maximizing slot allocation
   - Service upgrade recommendations
   - Time investment analysis
   - Strategic reasoning

3. **Message Generation**
   - Personalized patient communications
   - Tone and urgency adaptation
   - Clinical context integration
   - Multi-channel support

4. **Request Triage**
   - Natural language understanding
   - Sentiment and urgency analysis
   - Intelligent action recommendations
   - Auto-routing capabilities

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd medme_copilot_demo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🎮 Quick Start

### Mac/Linux
```bash
chmod +x run_demo.sh
./run_demo.sh
```

### Windows
```bash
run_demo.bat
```

The app will be available at `http://localhost:8501`

## 📋 Requirements

- Python 3.8+
- Streamlit 1.28.0+
- Pandas 2.0.0+
- **No external API keys required!**

## 🏗️ Architecture

```
medme_copilot_demo/
├── app.py                 # Main Streamlit application with LLM prompts
├── requirements.txt       # Minimal Python dependencies
├── README.md             # This file
├── run_demo.sh           # Mac/Linux startup script
└── run_demo.bat          # Windows startup script
```

## 🧠 LLM-Powered Features

### Intelligent Prompting
- **Clinical Reasoning**: LLM-style analysis of patient data
- **Revenue Optimization**: Strategic scheduling recommendations
- **Message Analysis**: Natural language understanding
- **Personalization**: Context-aware recommendations

### Key Capabilities
- **Risk Scoring**: Patient risk assessment algorithms
- **Revenue Optimization**: Strategic scheduling recommendations
- **Message Analysis**: Natural language understanding
- **Clinical Reasoning**: Evidence-based recommendations

## 🎯 Demo Scenarios

### For Product Managers
1. **Patient Insights**: Show how LLMs identify revenue opportunities
2. **Schedule Optimization**: Demonstrate revenue impact of intelligent scheduling
3. **Message Generation**: Highlight personalized communication capabilities
4. **Request Triage**: Showcase operational efficiency improvements

### Business Impact
- **Revenue Growth**: $2,340 potential impact demonstrated
- **Time Savings**: 4.2 hours saved per week
- **Patient Engagement**: Personalized communication strategies
- **Operational Efficiency**: Intelligent workflow automation

## 🔧 Configuration

The demo uses a simplified LLM-powered approach:

- **LLM Intelligence**: Always available, no setup required
- **Minimal Maintenance**: LLMs handle complex reasoning
- **Demo Data**: Realistic patient and scheduling scenarios
- **Customizable Prompts**: Easy to modify for different use cases

## 📈 Performance Metrics

The demo includes realistic performance indicators:
- Patient analysis throughput
- Recommendation accuracy
- Revenue impact calculations
- Time savings estimates

## 🚀 Production Ready

This approach is designed for easy production deployment:

1. **Replace LLM Simulation**: Connect to real LLM APIs (OpenAI, Anthropic, etc.)
2. **Add Real Data**: Integrate with pharmacy systems
3. **Scale Prompts**: Expand prompt library for more use cases
4. **Monitor Performance**: Track LLM response quality and costs

## 🤝 Contributing

This is a demonstration application. For production use, consider:
- Integration with real pharmacy systems
- HIPAA compliance measures
- LLM API cost optimization
- Additional clinical validations

## 📄 License

This demo is for evaluation purposes. Please contact MedMe Health for commercial licensing.

---

**Built for MedMe Health Product Manager Evaluation** 🏥 