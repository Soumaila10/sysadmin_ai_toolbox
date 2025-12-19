"""
Outil 1: Analyseur de Logs
Analyse les logs système et applications pour identifier les erreurs et problèmes
"""

from typing import Optional
from app.utils.llm_client import LLMClient
from app.utils.prompt_loader import PromptLoader


class AnalyseurLogs:
    """Analyseur de logs utilisant l'IA"""
    
    def __init__(self, prompt_version: str = "v1"):
        self.llm_client = LLMClient()
        self.prompt_loader = PromptLoader()
        self.prompt_version = prompt_version
    
    def analyser(self, logs: str, prompt_version: Optional[str] = None) -> str:
        """
        Analyse les logs fournis
        
        Args:
            logs: Contenu des logs à analyser
            prompt_version: Version du prompt à utiliser (par défaut: celle de l'instance)
        
        Returns:
            Analyse structurée des logs
        """
        version = prompt_version or self.prompt_version
        
        # Charge le prompt
        prompt_template = self.prompt_loader.load_prompt("analyseur_logs", version)
        
        # Extrait le prompt système et utilisateur
        system_prompt, user_prompt_template = self.prompt_loader.extract_system_prompt(
            prompt_template
        )
        
        # Construit le prompt utilisateur final
        if user_prompt_template:
            user_prompt = user_prompt_template.replace(
                "[Les logs de l'utilisateur seront insérés ici]",
                logs
            )
        else:
            # Si pas de marqueur, on ajoute les logs à la fin
            user_prompt = f"{prompt_template}\n\n## LOGS À ANALYSER\n\n{logs}"
            system_prompt = prompt_template
        
        # Génère l'analyse
        try:
            analyse = self.llm_client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3  # Température basse pour une analyse précise
            )
            return analyse
        except Exception as e:
            return f"Erreur lors de l'analyse: {str(e)}"
    
    def test_prompt_injection(self, logs: str) -> bool:
        """
        Test simple de prompt injection
        Détecte des tentatives basiques d'injection
        
        Args:
            logs: Contenu des logs à tester
        
        Returns:
            True si injection détectée, False sinon
        """
        # Patterns basiques de prompt injection
        injection_patterns = [
            "ignore previous instructions",
            "forget everything",
            "you are now",
            "system:",
            "assistant:",
            "user:",
            "ignore the above",
            "disregard",
            "new instructions:"
        ]
        
        logs_lower = logs.lower()
        for pattern in injection_patterns:
            if pattern in logs_lower:
                return True
        
        return False

