"""
Outil 5: Générateur de Documentation Infra (Mermaid)
Génère de la documentation d'infrastructure avec diagrammes Mermaid
"""

from typing import Optional
from app.utils.llm_client import LLMClient
from app.utils.prompt_loader import PromptLoader


class GenerateurDocInfra:
    """Générateur de documentation infrastructure utilisant l'IA"""
    
    def __init__(self, prompt_version: str = "v1"):
        self.llm_client = LLMClient()
        self.prompt_loader = PromptLoader()
        self.prompt_version = prompt_version
    
    def generer(self, informations: str, prompt_version: Optional[str] = None) -> str:
        """
        Génère de la documentation d'infrastructure
        
        Args:
            informations: Informations sur l'infrastructure à documenter
            prompt_version: Version du prompt à utiliser
        
        Returns:
            Documentation générée avec diagrammes Mermaid
        """
        version = prompt_version or self.prompt_version
        
        # Charge le prompt
        prompt_template = self.prompt_loader.load_prompt("generateur_doc_infra", version)
        
        # Extrait le prompt système et utilisateur
        system_prompt, user_prompt_template = self.prompt_loader.extract_system_prompt(
            prompt_template
        )
        
        # Construit le prompt utilisateur final
        if user_prompt_template:
            user_prompt = user_prompt_template.replace(
                "[Les informations de l'utilisateur seront insérées ici]",
                informations
            )
        else:
            user_prompt = f"{prompt_template}\n\n## INFORMATIONS SUR L'INFRASTRUCTURE\n\n{informations}"
            system_prompt = prompt_template
        
        # Génère la documentation
        try:
            resultat = self.llm_client.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.4  # Température modérée pour équilibrer créativité et précision
            )
            return resultat
        except Exception as e:
            return f"Erreur lors de la génération: {str(e)}"
    
    def test_prompt_injection(self, informations: str) -> bool:
        """Test simple de prompt injection"""
        injection_patterns = [
            "ignore previous instructions",
            "forget everything",
            "you are now",
            "system:",
            "assistant:",
            "ignore the above"
        ]
        
        informations_lower = informations.lower()
        for pattern in injection_patterns:
            if pattern in informations_lower:
                return True
        return False




