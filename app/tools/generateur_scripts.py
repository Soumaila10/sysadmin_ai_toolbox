"""
Outil 2: Générateur de Scripts Bash/Python
Génère des scripts d'automatisation DevOps
"""

from typing import Optional
from app.utils.llm_client import LLMClient
from app.utils.prompt_loader import PromptLoader


class GenerateurScripts:
    """Générateur de scripts utilisant l'IA"""
    
    def __init__(self, prompt_version: str = "v1"):
        self.llm_client = LLMClient()
        self.prompt_loader = PromptLoader()
        self.prompt_version = prompt_version
    
    def generer(self, besoin: str, prompt_version: Optional[str] = None) -> str:
        """
        Génère un script selon le besoin
        
        Args:
            besoin: Description de la tâche à automatiser
            prompt_version: Version du prompt à utiliser
        
        Returns:
            Script généré avec documentation
        """
        version = prompt_version or self.prompt_version
        
        # Charge le prompt
        prompt_template = self.prompt_loader.load_prompt("generateur_scripts", version)
        
        # Extrait le prompt système et utilisateur
        system_prompt, user_prompt_template = self.prompt_loader.extract_system_prompt(
            prompt_template
        )
        
        # Construit le prompt utilisateur final
        if user_prompt_template:
            user_prompt = user_prompt_template.replace(
                "[Le besoin de l'utilisateur sera inséré ici]",
                besoin
            )
        else:
            user_prompt = f"{prompt_template}\n\n## BESOIN DE L'UTILISATEUR\n\n{besoin}"
            system_prompt = prompt_template
        
        # Génère le script
        try:
            resultat = self.llm_client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.5  # Température plus élevée pour la créativité
            )
            return resultat
        except Exception as e:
            return f"Erreur lors de la génération: {str(e)}"
    
    def test_prompt_injection(self, besoin: str) -> bool:
        """Test simple de prompt injection"""
        injection_patterns = [
            "ignore previous instructions",
            "forget everything",
            "you are now",
            "system:",
            "assistant:",
            "ignore the above"
        ]
        
        besoin_lower = besoin.lower()
        for pattern in injection_patterns:
            if pattern in besoin_lower:
                return True
        return False

