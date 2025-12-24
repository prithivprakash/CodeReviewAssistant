from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

PROVIDERS = {
    "openai" : {
    "class": ChatOpenAI, 
    "model" : "gpt-4o-mini",
    "key_param" : "api_key"
    },

    "gemini": {
        "class" : ChatGoogleGenerativeAI,
        "model" : "gemini-1.5-flash",
        "key_param": "api_key"
    },

    "groq" : {
        "class" : ChatGroq,
        "model" : "llama-3.1-8b-instant",
        "key_param" : "api_key"
    }
}

def get_llm(provider: str, api_key: str):
    provider = provider.lower()

    if provider not in PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider}")
    
    cfg = PROVIDERS[provider]

    return cfg["class"](model=cfg["model"], temperature=0.2, **{cfg["key_param"]: api_key})

