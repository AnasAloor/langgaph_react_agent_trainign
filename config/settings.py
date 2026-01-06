"""
Configuration Settings for ReAct Agent Demo
============================================
Centralized configuration for the Agentic AI application.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMConfig:
    """Configuration for Large Language Model."""
    provider: str = "google"  # google, openai, anthropic
    model_name: str = "gemini-1.5-flash"
    temperature: float = 0.1
    max_tokens: int = 2048
    api_key: Optional[str] = None
    
    def __post_init__(self):
        if self.api_key is None:
            self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")


@dataclass 
class AgentConfig:
    """Configuration for ReAct Agent."""
    max_iterations: int = 5
    verbose: bool = True
    enable_memory: bool = True
    recursion_limit: int = 25


@dataclass
class AppConfig:
    """Main Application Configuration."""
    app_name: str = "ReAct Agent Demo"
    version: str = "1.0.0"
    debug: bool = True
    llm: LLMConfig = None
    agent: AgentConfig = None
    
    def __post_init__(self):
        if self.llm is None:
            self.llm = LLMConfig()
        if self.agent is None:
            self.agent = AgentConfig()


# Default configuration instance
config = AppConfig()
