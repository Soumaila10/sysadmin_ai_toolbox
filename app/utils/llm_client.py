"""
Client abstrait pour les LLM (OpenAI et Claude)
Permet de changer facilement de fournisseur via la configuration
"""

from typing import Optional, List, Dict, Any
from app.config.config import Config, LLMProvider


class LLMClient:
    """Client abstrait pour interagir avec les LLM"""
    
    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        self.api_key = Config.get_api_key()
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialise le client selon le fournisseur configuré"""
        if self.provider == LLMProvider.OPENAI.value:
            try:
                import openai
                self._client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("Le package 'openai' n'est pas installé. Installez-le avec: pip install openai")
        
        elif self.provider == LLMProvider.CLAUDE.value:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError("Le package 'anthropic' n'est pas installé. Installez-le avec: pip install anthropic")
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Génère une réponse à partir d'un prompt
        
        Args:
            prompt: Le prompt utilisateur
            system_prompt: Prompt système (persona, instructions)
            temperature: Température de génération (0.0-1.0)
            max_tokens: Nombre maximum de tokens
            **kwargs: Arguments additionnels spécifiques au fournisseur
        
        Returns:
            La réponse générée par le LLM
        """
        temperature = temperature or Config.TEMPERATURE
        max_tokens = max_tokens or Config.MAX_TOKENS
        
        if self.provider == LLMProvider.OPENAI.value:
            return self._generate_openai(prompt, system_prompt, temperature, max_tokens, **kwargs)
        elif self.provider == LLMProvider.CLAUDE.value:
            return self._generate_claude(prompt, system_prompt, temperature, max_tokens, **kwargs)
    
    def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Génère une réponse via OpenAI"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self._client.chat.completions.create(
            model=kwargs.get("model", Config.OPENAI_MODEL),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **{k: v for k, v in kwargs.items() if k != "model"}
        )
        
        return response.choices[0].message.content
    
    def _generate_claude(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Génère une réponse via Claude (Anthropic)"""
        system_message = system_prompt or ""
        
        response = self._client.messages.create(
            model=kwargs.get("model", Config.CLAUDE_MODEL),
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_message,
            messages=[
                {"role": "user", "content": prompt}
            ],
            **{k: v for k, v in kwargs.items() if k != "model"}
        )
        
        return response.content[0].text

