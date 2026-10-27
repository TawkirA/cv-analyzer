import os
from typing import Dict, Any, Tuple
from dotenv import load_dotenv

from src.schemas.report_schema import CVAnalysisReport

load_dotenv()

# Model options for each supported provider
PROVIDER_MODELS = {
    "Google Gemini": {
        "models": [
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-2.5-flash-lite",
            "gemini-3.5-flash",
            "gemini-3.5-flash-lite",
            "gemini-3.8-flash"
        ],
        "default": "gemini-2.5-flash",
        "env_var": "GEMINI_API_KEY",
        "fallback_env_vars": ["GOOGLE_API_KEY"],
        "key_label": "Google Gemini API Key",
        "key_placeholder": "AIzaSy..."
    },
    "OpenAI": {
        "models": [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ],
        "default": "gpt-4o",
        "env_var": "OPENAI_API_KEY",
        "fallback_env_vars": [],
        "key_label": "OpenAI API Key",
        "key_placeholder": "sk-proj-..."
    },
    "Anthropic": {
        "models": [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229"
        ],
        "default": "claude-3-5-sonnet-20241022",
        "env_var": "ANTHROPIC_API_KEY",
        "fallback_env_vars": [],
        "key_label": "Anthropic API Key",
        "key_placeholder": "sk-ant-api03-..."
    },
    "IBM watsonx": {
        "models": [
            "ibm/granite-3-8b-instruct",
            "ibm/granite-13b-chat-v2",
            "meta-llama/llama-3-3-70b-instruct",
            "meta-llama/llama-3-1-8b-instruct",
            "ibm/granite-20b-multilingual"
        ],
        "default": "ibm/granite-3-8b-instruct",
        "env_var": "WATSONX_APIKEY",
        "fallback_env_vars": ["IBM_WATSONX_APIKEY"],
        "key_label": "IBM watsonx API Key",
        "key_placeholder": "Your IBM Cloud IAM / Watsonx API Key"
    }
}


def get_default_api_key(provider: str) -> str:
    """Retrieves API key from environment variables if present."""
    config = PROVIDER_MODELS.get(provider, {})
    primary_env = config.get("env_var", "")
    if primary_env and os.getenv(primary_env):
        return os.getenv(primary_env)
    
    for fallback in config.get("fallback_env_vars", []):
        if os.getenv(fallback):
            return os.getenv(fallback)
    return ""


def validate_llm_config(llm_config: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validates that necessary provider, model, and API keys are specified.
    """
    if not llm_config:
        return False, "Model configuration is missing. Please configure model provider and API key."
    
    provider = llm_config.get("provider", "Google Gemini")
    if provider not in PROVIDER_MODELS:
        return False, f"Unsupported provider: '{provider}'. Supported: {', '.join(PROVIDER_MODELS.keys())}"
    
    api_key = (llm_config.get("api_key") or "").strip()
    if not api_key:
        api_key = get_default_api_key(provider)
        
    if not api_key:
        return False, f"API key is required for {provider}. Please provide your API key in the Model Configuration panel."
    
    if provider == "IBM watsonx":
        project_id = (llm_config.get("project_id") or os.getenv("WATSONX_PROJECT_ID", "")).strip()
        if not project_id:
            return False, "IBM watsonx requires a Project ID (or WATSONX_PROJECT_ID environment variable)."
            
    return True, ""


def get_structured_llm(llm_config: Dict[str, Any] = None, schema=CVAnalysisReport):
    """
    Instantiates and returns a structured LLM based on user configuration.
    """
    if not llm_config:
        llm_config = {
            "provider": "Google Gemini",
            "model_name": "gemini-2.5-flash",
            "api_key": get_default_api_key("Google Gemini")
        }
        
    provider = llm_config.get("provider", "Google Gemini")
    model_name = llm_config.get("model_name") or PROVIDER_MODELS.get(provider, {}).get("default")
    api_key = (llm_config.get("api_key") or "").strip()
    
    if not api_key:
        api_key = get_default_api_key(provider)
        
    if not api_key:
        raise ValueError(
            f"No API key provided for {provider}. Please provide your API key in the configuration panel."
        )

    # Provider SDKs are imported lazily: importing all four at startup is slow
    # and only the selected provider is ever needed.
    if provider == "Google Gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0
        )
    elif provider == "OpenAI":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            model=model_name,
            api_key=api_key,
            temperature=0
        )
    elif provider == "Anthropic":
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(
            model=model_name,
            api_key=api_key,
            temperature=0
        )
    elif provider == "IBM watsonx":
        from langchain_ibm import ChatWatsonx

        project_id = (llm_config.get("project_id") or os.getenv("WATSONX_PROJECT_ID", "")).strip()
        url = (llm_config.get("watsonx_url") or os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")).strip()
        if not project_id:
            raise ValueError("IBM watsonx requires a Project ID.")
        llm = ChatWatsonx(
            model_id=model_name,
            apikey=api_key,
            url=url,
            project_id=project_id,
            params={"decoding_method": "greedy", "max_new_tokens": 4000}
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")
        
    return llm.with_structured_output(schema)
