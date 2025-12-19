"""
Chargeur de prompts depuis les fichiers texte
Gère le versionnement des prompts (v1, v2, vFinal)
"""

import os
from pathlib import Path
from typing import Optional, Tuple
from app.config.config import Config


class PromptLoader:
    """Charge et gère les prompts versionnés"""
    
    def __init__(self, prompts_dir: Optional[str] = None):
        self.prompts_dir = Path(prompts_dir or Config.PROMPTS_DIR)
    
    def load_prompt(self, tool_name: str, version: str = "v1") -> str:
        """
        Charge un prompt depuis un fichier
        
        Args:
            tool_name: Nom de l'outil (ex: "analyseur_logs")
            version: Version du prompt (ex: "v1", "v2", "vFinal")
        
        Returns:
            Le contenu du prompt
        
        Raises:
            FileNotFoundError: Si le fichier de prompt n'existe pas
        """
        prompt_file = self.prompts_dir / tool_name / f"{version}.txt"
        
        if not prompt_file.exists():
            raise FileNotFoundError(
                f"Prompt non trouvé: {prompt_file}\n"
                f"Vérifiez que le fichier existe dans {self.prompts_dir / tool_name}"
            )
        
        with open(prompt_file, "r", encoding="utf-8") as f:
            return f.read()
    
    def list_available_versions(self, tool_name: str) -> list:
        """
        Liste les versions disponibles pour un outil
        
        Args:
            tool_name: Nom de l'outil
        
        Returns:
            Liste des versions disponibles
        """
        tool_dir = self.prompts_dir / tool_name
        
        if not tool_dir.exists():
            return []
        
        versions = []
        for file in tool_dir.glob("*.txt"):
            version = file.stem
            versions.append(version)
        
        return sorted(versions)
    
    def extract_system_prompt(self, prompt_content: str) -> Tuple[str, str]:
        """
        Extrait le prompt système (persona) et le prompt utilisateur
        
        Args:
            prompt_content: Contenu complet du prompt
        
        Returns:
            Tuple (system_prompt, user_prompt)
        """
        # Le prompt système correspond à tout le contenu jusqu'à "## LOGS À ANALYSER"
        # ou similaire. Pour l'instant, on retourne tout comme système.
        # Cette méthode peut être améliorée selon la structure des prompts.
        
        # Recherche du marqueur de fin du prompt système
        markers = [
            "## LOGS À ANALYSER",
            "## INPUT UTILISATEUR",
            "## DONNÉES À TRAITER"
        ]
        
        system_prompt = prompt_content
        user_prompt = ""
        
        for marker in markers:
            if marker in prompt_content:
                parts = prompt_content.split(marker, 1)
                system_prompt = parts[0].strip()
                user_prompt = parts[1].strip() if len(parts) > 1 else ""
                break
        
        return system_prompt, user_prompt

