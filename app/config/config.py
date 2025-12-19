"""
Configuration de l'application AI-Powered Dev Toolkit
Gère les variables d'environnement et la configuration des LLM
"""

import os
from typing import Optional
from enum import Enum


class LLMProvider(str, Enum):
    """Fournisseurs de LLM supportés"""
    OPENAI = "openai"
    CLAUDE = "claude"


class Config:
    """Classe de configuration centralisée"""
    
    # Configuration LLM
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", LLMProvider.OPENAI.value)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Modèles par défaut
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    
    # Paramètres de génération
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.3"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4000"))
    
    # Chemins des fichiers
    PROMPTS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "prompts")
    DOCS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs")
    
    @classmethod
    def validate(cls) -> bool:
        """Valide la configuration"""
        if cls.LLM_PROVIDER == LLMProvider.OPENAI.value:
            if not cls.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY doit être définie dans les variables d'environnement")
        elif cls.LLM_PROVIDER == LLMProvider.CLAUDE.value:
            if not cls.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY doit être définie dans les variables d'environnement")
        else:
            raise ValueError(f"Fournisseur LLM non supporté: {cls.LLM_PROVIDER}")
        return True
    
    @classmethod
    def get_api_key(cls) -> str:
        """Retourne la clé API appropriée"""
        if cls.LLM_PROVIDER == LLMProvider.OPENAI.value:
            return cls.OPENAI_API_KEY
        elif cls.LLM_PROVIDER == LLMProvider.CLAUDE.value:
            return cls.ANTHROPIC_API_KEY
        raise ValueError("Aucune clé API configurée")

