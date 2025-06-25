# LLM Setup Guide

This demo now uses real LLM APIs to generate authentic, intelligent responses!

## 🚀 Quick Setup

### Option 1: Environment Variables (Recommended)
Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### Option 2: Streamlit Secrets
Create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your_openai_api_key_here"
GOOGLE_API_KEY = "your_google_api_key_here"
```

## 🔑 Getting API Keys

### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to "API Keys"
4. Create a new API key
5. Copy and paste into your config

### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Paste into your config

## 🎯 Features

With LLM APIs enabled, you'll get:
- **Real AI-generated responses** instead of simulations
- **Varied and intelligent** recommendations
- **Context-aware** messaging
- **Natural language understanding** for patient messages

## 💰 Cost Estimate

- **OpenAI GPT-4**: ~$0.03 per request
- **Google Gemini**: ~$0.001 per request (much cheaper!)
- **Demo usage**: ~$0.50-1.00 for full demo session

## 🔧 Fallback Mode

If no API keys are provided, the app will use intelligent fallback responses that still demonstrate the capabilities.

## 🚀 Ready to Demo!

Once you add your API keys, the app will automatically use real LLMs for:
- Patient insights and recommendations
- Schedule optimization strategies
- Personalized patient messages
- Intelligent message triage

The responses will be genuinely AI-generated and showcase the true power of LLMs in pharmacy operations!

## 🎯 Provider Selection

The app supports both providers:
- **OpenAI GPT-4**: Excellent for structured analysis and reasoning
- **Google Gemini**: Great for creative messaging and cost-effective processing

You can choose your preferred provider in the sidebar when both are available. 