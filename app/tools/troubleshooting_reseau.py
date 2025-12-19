"""
Outil 4: Assistant Troubleshooting Réseau
Aide au diagnostic et résolution de problèmes réseau
"""

from typing import Optional
from app.utils.llm_client import LLMClient
from app.utils.prompt_loader import PromptLoader


class TroubleshootingReseau:
    """Assistant troubleshooting réseau utilisant l'IA"""
    
    def __init__(self, prompt_version: str = "v1"):
        self.llm_client = LLMClient()
        self.prompt_loader = PromptLoader()
        self.prompt_version = prompt_version
    
    def diagnostiquer(self, probleme: str, prompt_version: Optional[str] = None) -> str:
        """
        Diagnostique un problème réseau
        
        Args:
            probleme: Description du problème réseau
            prompt_version: Version du prompt à utiliser
        
        Returns:
            Diagnostic et solutions proposées
        """
        version = prompt_version or self.prompt_version
        
        # Charge le prompt
        prompt_template = self.prompt_loader.load_prompt("troubleshooting_reseau", version)
        
        # Extrait le prompt système et utilisateur
        system_prompt, user_prompt_template = self.prompt_loader.extract_system_prompt(
            prompt_template
        )
        
        # Construit le prompt utilisateur final
        if user_prompt_template:
            user_prompt = user_prompt_template.replace(
                "[Le problème de l'utilisateur sera inséré ici]",
                probleme
            )
        else:
            user_prompt = f"{prompt_template}\n\n## PROBLÈME RÉSEAU À RÉSOUDRE\n\n{probleme}"
            system_prompt = prompt_template
        
        # Génère le diagnostic
        try:
            resultat = self.llm_client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3  # Température basse pour un diagnostic précis
            )
            return resultat
        except Exception as e:
            return f"Erreur lors du diagnostic: {str(e)}"
    
    def test_prompt_injection(self, probleme: str) -> bool:
        """Test simple de prompt injection"""
        injection_patterns = [
            "ignore previous instructions",
            "forget everything",
            "you are now",
            "system:",
            "assistant:",
            "ignore the above"
        ]
        
        probleme_lower = probleme.lower()
        for pattern in injection_patterns:
            if pattern in probleme_lower:
                return True
        return False

