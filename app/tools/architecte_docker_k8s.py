"""
Outil 3: Architecte Docker/Kubernetes
Génère des configurations Docker et Kubernetes optimisées
"""

from typing import Optional
from app.utils.llm_client import LLMClient
from app.utils.prompt_loader import PromptLoader


class ArchitecteDockerK8s:
    """Architecte Docker/Kubernetes utilisant l'IA"""
    
    def __init__(self, prompt_version: str = "v1"):
        self.llm_client = LLMClient()
        self.prompt_loader = PromptLoader()
        self.prompt_version = prompt_version
    
    def generer(self, besoins: str, prompt_version: Optional[str] = None) -> str:
        """
        Génère des configurations Docker et Kubernetes
        
        Args:
            besoins: Description des besoins de l'utilisateur
            prompt_version: Version du prompt à utiliser
        
        Returns:
            Configurations générées
        """
        version = prompt_version or self.prompt_version
        
        # Charge le prompt
        prompt_template = self.prompt_loader.load_prompt("architecte_docker_k8s", version)
        
        # Extrait le prompt système et utilisateur
        system_prompt, user_prompt_template = self.prompt_loader.extract_system_prompt(
            prompt_template
        )
        
        # Construit le prompt utilisateur final
        if user_prompt_template:
            user_prompt = user_prompt_template.replace(
                "[Les besoins de l'utilisateur seront insérés ici]",
                besoins
            )
        else:
            user_prompt = f"{prompt_template}\n\n## BESOINS DE L'UTILISATEUR\n\n{besoins}"
            system_prompt = prompt_template
        
        # Génère les configurations
        try:
            resultat = self.llm_client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.4  # Température légèrement plus élevée pour la créativité
            )
            return resultat
        except Exception as e:
            return f"Erreur lors de la génération: {str(e)}"
    
    def test_prompt_injection(self, besoins: str) -> bool:
        """Test simple de prompt injection"""
        injection_patterns = [
            "ignore previous instructions",
            "forget everything",
            "you are now",
            "system:",
            "assistant:",
            "ignore the above"
        ]
        
        besoins_lower = besoins.lower()
        for pattern in injection_patterns:
            if pattern in besoins_lower:
                return True
        return False




