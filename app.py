"""
Application principale - AI-Powered Dev Toolkit
Interface Streamlit pour les 5 outils IA DevOps
"""

import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

from app.config.config import Config
from app.tools.analyseur_logs import AnalyseurLogs
from app.tools.generateur_scripts import GenerateurScripts
from app.tools.architecte_docker_k8s import ArchitecteDockerK8s
from app.tools.troubleshooting_reseau import TroubleshootingReseau
from app.tools.generateur_doc_infra import GenerateurDocInfra
from app.utils.prompt_loader import PromptLoader


# Configuration de la page
st.set_page_config(
    page_title="AI-Powered Dev Toolkit",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🤖 AI-Powered Dev Toolkit")
st.markdown("**Boîte à outils IA pour Administrateurs Système et DevOps**")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Sélection du fournisseur LLM
    providers = ["openai", "claude", "google"]
    try:
        default_index = providers.index(Config.LLM_PROVIDER) if Config.LLM_PROVIDER in providers else 0
    except (ValueError, AttributeError):
        default_index = 0
    
    llm_provider = st.selectbox(
        "Fournisseur LLM",
        providers,
        index=default_index
    )
    
    # Vérification des clés API
    if llm_provider == "openai":
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=Config.OPENAI_API_KEY or "",
            help="Définissez OPENAI_API_KEY dans les variables d'environnement"
        )
    elif llm_provider == "claude":
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            value=Config.ANTHROPIC_API_KEY or "",
            help="Définissez ANTHROPIC_API_KEY dans les variables d'environnement"
        )
    else:
        api_key = st.text_input(
            "Google AI (Gemini) API Key",
            type="password",
            value=Config.GOOGLE_API_KEY or "",
            help="Définissez GOOGLE_API_KEY dans les variables d'environnement"
        )

    # Appliquer les choix de la sidebar à la configuration globale
    # (permet d'utiliser le fournisseur et la clé sélectionnés sans redémarrer)
    Config.LLM_PROVIDER = llm_provider
    if llm_provider == "openai":
        Config.OPENAI_API_KEY = api_key or Config.OPENAI_API_KEY
    elif llm_provider == "claude":
        Config.ANTHROPIC_API_KEY = api_key or Config.ANTHROPIC_API_KEY
    else:
        Config.GOOGLE_API_KEY = api_key or Config.GOOGLE_API_KEY
    
    st.divider()
    
    # Navigation vers les outils
    st.header("🛠️ Outils disponibles")
    tool_selected = st.radio(
        "Sélectionnez un outil",
        [
            "1. Analyseur de Logs",
            "2. Générateur de Scripts",
            "3. Architecte Docker/K8s",
            "4. Troubleshooting Réseau",
            "5. Générateur de Documentation"
        ]
    )

# Contenu principal selon l'outil sélectionné
if tool_selected == "1. Analyseur de Logs":
    st.header("📊 Analyseur de Logs")
    st.markdown("Analysez vos logs système et applications pour identifier les erreurs et problèmes")
    
    # Sélection de la version du prompt
    prompt_loader = PromptLoader()
    versions = prompt_loader.list_available_versions("analyseur_logs")
    
    # Descriptions des versions
    version_descriptions = {
        "v1": "Version initiale - Persona + Few-shot Learning",
        "v2": "Version améliorée - Chain of Thought + Analyse temporelle",
        "v3": "Version avancée - Contexte technique + Patterns complexes",
        "v4": "Version optimisée - Multi-format + Analyse de performance",
        "vFinal": "Version finale - Consolidation de toutes les meilleures pratiques"
    }
    
    if versions:
        # Trouve l'index de vFinal si disponible, sinon v4, sinon v3, etc.
        default_index = 0
        if "vFinal" in versions:
            default_index = versions.index("vFinal")
        elif "v4" in versions:
            default_index = versions.index("v4")
        elif "v3" in versions:
            default_index = versions.index("v3")
        elif "v2" in versions:
            default_index = versions.index("v2")
        
        # Crée les labels avec descriptions
        version_options = []
        for v in versions:
            desc = version_descriptions.get(v, "")
            if desc:
                version_options.append(f"{v} - {desc}")
            else:
                version_options.append(v)
        
        prompt_version = st.selectbox(
            "Version du prompt",
            versions,
            index=default_index,
            format_func=lambda x: f"{x} - {version_descriptions.get(x, '')}" if version_descriptions.get(x) else x,
            help="Sélectionnez la version du prompt à utiliser. vFinal est recommandée pour une analyse complète."
        )
        
        # Affiche la description de la version sélectionnée
        if prompt_version in version_descriptions:
            st.info(f"ℹ️ **{prompt_version}** : {version_descriptions[prompt_version]}")
    else:
        prompt_version = "v1"
        st.warning("⚠️ Aucune version de prompt trouvée. Utilisation de v1 par défaut.")
    
    # Zone de saisie des logs
    st.subheader("Entrez vos logs")
    logs_input = st.text_area(
        "Logs à analyser",
        height=300,
        placeholder="Collez vos logs ici...\n\nExemple:\n[2025-12-19 10:23:45] ERROR: Database connection failed\n[2025-12-19 10:23:46] WARN: Retry attempt failed"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        analyser_btn = st.button("🔍 Analyser", type="primary", use_container_width=True)
    
    with col2:
        if st.button("📄 Charger depuis un fichier", use_container_width=True):
            uploaded_file = st.file_uploader("Choisissez un fichier de logs", type=["txt", "log"])
            if uploaded_file:
                logs_input = uploaded_file.read().decode("utf-8")
                st.rerun()
    
    # Analyse des logs
    if analyser_btn and logs_input:
        # Test de prompt injection
        analyseur = AnalyseurLogs(prompt_version=prompt_version)
        
        if analyseur.test_prompt_injection(logs_input):
            st.error("⚠️ Tentative de prompt injection détectée ! Veuillez vérifier vos logs.")
        else:
            with st.spinner("Analyse en cours..."):
                try:
                    # Validation de la configuration
                    Config.validate()
                    
                    # Analyse
                    resultat = analyseur.analyser(logs_input, prompt_version=prompt_version)
                    
                    # Affichage du résultat
                    st.subheader("📋 Résultat de l'analyse")
                    st.markdown(f"**Version utilisée** : `{prompt_version}`")
                    st.markdown("---")
                    st.markdown(resultat)
                    
                    # Informations supplémentaires
                    with st.expander("ℹ️ Informations sur l'analyse"):
                        st.write(f"- **Version du prompt** : {prompt_version}")
                        st.write(f"- **Nombre de lignes analysées** : {len(logs_input.splitlines())}")
                        st.write(f"- **Taille des logs** : {len(logs_input)} caractères")
                    
                    # Bouton de téléchargement
                    col_dl1, col_dl2 = st.columns([1, 1])
                    with col_dl1:
                        st.download_button(
                            label="💾 Télécharger l'analyse (Markdown)",
                            data=resultat,
                            file_name=f"analyse_logs_{prompt_version}_{st.session_state.get('analysis_count', 1)}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    with col_dl2:
                        st.download_button(
                            label="📄 Télécharger les logs originaux",
                            data=logs_input,
                            file_name=f"logs_originaux_{st.session_state.get('analysis_count', 1)}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    # Incrémente le compteur d'analyses
                    if 'analysis_count' not in st.session_state:
                        st.session_state.analysis_count = 1
                    else:
                        st.session_state.analysis_count += 1
                    
                except ValueError as e:
                    st.error(f"❌ Erreur de configuration: {e}")
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'analyse: {e}")
    
    elif analyser_btn and not logs_input:
        st.warning("⚠️ Veuillez entrer des logs à analyser")

elif tool_selected == "2. Générateur de Scripts":
    st.header("📝 Générateur de Scripts Bash/Python")
    st.markdown("Générez des scripts Bash ou Python pour automatiser vos tâches DevOps")
    
    # Sélection de la version du prompt
    prompt_loader = PromptLoader()
    versions = prompt_loader.list_available_versions("generateur_scripts")
    
    version_descriptions = {
        "v1": "Version initiale - Persona + Few-shot Learning",
        "v2": "Version améliorée - Chain of Thought + Validation avancée",
        "v3": "Version avancée - Gestion d'erreurs robuste + Logging",
        "v4": "Version optimisée - Multi-langages + Tests intégrés",
        "vFinal": "Version finale - Consolidation des meilleures pratiques"
    }
    
    if versions:
        default_index = 0
        if "vFinal" in versions:
            default_index = versions.index("vFinal")
        elif "v4" in versions:
            default_index = versions.index("v4")
        
        prompt_version = st.selectbox(
            "Version du prompt",
            versions,
            index=default_index,
            format_func=lambda x: f"{x} - {version_descriptions.get(x, '')}" if version_descriptions.get(x) else x,
            help="Sélectionnez la version du prompt à utiliser"
        )
        
        if prompt_version in version_descriptions:
            st.info(f"ℹ️ **{prompt_version}** : {version_descriptions[prompt_version]}")
    else:
        prompt_version = "v1"
        st.warning("⚠️ Aucune version de prompt trouvée. Utilisation de v1 par défaut.")
    
    # Zone de saisie
    st.subheader("Décrivez votre besoin")
    besoin_input = st.text_area(
        "Tâche à automatiser",
        height=200,
        placeholder="Exemple: Script pour sauvegarder un dossier vers S3 avec rotation des backups..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        generer_btn = st.button("🚀 Générer", type="primary", use_container_width=True)
    
    # Génération du script
    if generer_btn and besoin_input:
        generateur = GenerateurScripts(prompt_version=prompt_version)
        
        if generateur.test_prompt_injection(besoin_input):
            st.error("⚠️ Tentative de prompt injection détectée !")
        else:
            with st.spinner("Génération en cours..."):
                try:
                    Config.validate()
                    resultat = generateur.generer(besoin_input, prompt_version=prompt_version)
                    
                    st.subheader("📋 Script généré")
                    st.markdown(f"**Version utilisée** : `{prompt_version}`")
                    st.markdown("---")
                    st.markdown(resultat)
                    
                    st.download_button(
                        label="💾 Télécharger le script",
                        data=resultat,
                        file_name=f"script_{prompt_version}.sh",
                        mime="text/plain",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Erreur lors de la génération: {e}")
    
    elif generer_btn and not besoin_input:
        st.warning("⚠️ Veuillez décrire votre besoin")

elif tool_selected == "3. Architecte Docker/K8s":
    st.header("🐳 Architecte Docker/Kubernetes")
    st.markdown("Générez des configurations Docker et Kubernetes optimisées et sécurisées")
    
    # Sélection de la version du prompt
    prompt_loader = PromptLoader()
    versions = prompt_loader.list_available_versions("architecte_docker_k8s")
    
    version_descriptions = {
        "v1": "Version initiale - Persona + Few-shot Learning",
        "v2": "Version améliorée - Chain of Thought + Optimisation avancée",
        "v3": "Version avancée - Sécurité renforcée + HPA/PDB",
        "v4": "Version optimisée - Multi-environnements + CI/CD",
        "vFinal": "Version finale - Consolidation des meilleures pratiques"
    }
    
    if versions:
        default_index = 0
        if "vFinal" in versions:
            default_index = versions.index("vFinal")
        elif "v4" in versions:
            default_index = versions.index("v4")
        
        prompt_version = st.selectbox(
            "Version du prompt",
            versions,
            index=default_index,
            format_func=lambda x: f"{x} - {version_descriptions.get(x, '')}" if version_descriptions.get(x) else x,
            help="Sélectionnez la version du prompt à utiliser"
        )
        
        if prompt_version in version_descriptions:
            st.info(f"ℹ️ **{prompt_version}** : {version_descriptions[prompt_version]}")
    else:
        prompt_version = "v1"
        st.warning("⚠️ Aucune version de prompt trouvée. Utilisation de v1 par défaut.")
    
    # Zone de saisie
    st.subheader("Décrivez vos besoins")
    besoins_input = st.text_area(
        "Besoins de l'application",
        height=200,
        placeholder="Exemple: Application Flask Python avec base de données PostgreSQL, besoin de scalabilité..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        generer_btn = st.button("🚀 Générer", type="primary", use_container_width=True)
    
    # Génération des configurations
    if generer_btn and besoins_input:
        architecte = ArchitecteDockerK8s(prompt_version=prompt_version)
        
        if architecte.test_prompt_injection(besoins_input):
            st.error("⚠️ Tentative de prompt injection détectée !")
        else:
            with st.spinner("Génération en cours..."):
                try:
                    Config.validate()
                    resultat = architecte.generer(besoins_input, prompt_version=prompt_version)
                    
                    st.subheader("📋 Configurations générées")
                    st.markdown(f"**Version utilisée** : `{prompt_version}`")
                    st.markdown("---")
                    st.markdown(resultat)
                    
                    st.download_button(
                        label="💾 Télécharger les configurations",
                        data=resultat,
                        file_name=f"docker_k8s_{prompt_version}.yaml",
                        mime="text/yaml",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Erreur lors de la génération: {e}")
    
    elif generer_btn and not besoins_input:
        st.warning("⚠️ Veuillez décrire vos besoins")

elif tool_selected == "4. Troubleshooting Réseau":
    st.header("🌐 Assistant Troubleshooting Réseau")
    st.markdown("Diagnostiquez et résolvez vos problèmes réseau de manière méthodique")
    
    # Sélection de la version du prompt
    prompt_loader = PromptLoader()
    versions = prompt_loader.list_available_versions("troubleshooting_reseau")
    
    version_descriptions = {
        "v1": "Version initiale - Persona + Few-shot Learning",
        "v2": "Version améliorée - Chain of Thought + Diagnostic étape par étape",
        "v3": "Version avancée - Analyse approfondie + Outils avancés",
        "v4": "Version optimisée - Multi-protocoles + Performance",
        "vFinal": "Version finale - Consolidation des meilleures pratiques"
    }
    
    if versions:
        default_index = 0
        if "vFinal" in versions:
            default_index = versions.index("vFinal")
        elif "v4" in versions:
            default_index = versions.index("v4")
        
        prompt_version = st.selectbox(
            "Version du prompt",
            versions,
            index=default_index,
            format_func=lambda x: f"{x} - {version_descriptions.get(x, '')}" if version_descriptions.get(x) else x,
            help="Sélectionnez la version du prompt à utiliser"
        )
        
        if prompt_version in version_descriptions:
            st.info(f"ℹ️ **{prompt_version}** : {version_descriptions[prompt_version]}")
    else:
        prompt_version = "v1"
        st.warning("⚠️ Aucune version de prompt trouvée. Utilisation de v1 par défaut.")
    
    # Zone de saisie
    st.subheader("Décrivez votre problème réseau")
    probleme_input = st.text_area(
        "Problème à résoudre",
        height=200,
        placeholder="Exemple: Je ne peux pas me connecter à un serveur distant, timeout sur les requêtes..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        diagnostiquer_btn = st.button("🔍 Diagnostiquer", type="primary", use_container_width=True)
    
    # Diagnostic
    if diagnostiquer_btn and probleme_input:
        troubleshooting = TroubleshootingReseau(prompt_version=prompt_version)
        
        if troubleshooting.test_prompt_injection(probleme_input):
            st.error("⚠️ Tentative de prompt injection détectée !")
        else:
            with st.spinner("Diagnostic en cours..."):
                try:
                    Config.validate()
                    resultat = troubleshooting.diagnostiquer(probleme_input, prompt_version=prompt_version)
                    
                    st.subheader("📋 Diagnostic et solutions")
                    st.markdown(f"**Version utilisée** : `{prompt_version}`")
                    st.markdown("---")
                    st.markdown(resultat)
                    
                    st.download_button(
                        label="💾 Télécharger le diagnostic",
                        data=resultat,
                        file_name=f"diagnostic_reseau_{prompt_version}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Erreur lors du diagnostic: {e}")
    
    elif diagnostiquer_btn and not probleme_input:
        st.warning("⚠️ Veuillez décrire votre problème")

elif tool_selected == "5. Générateur de Documentation":
    st.header("📚 Générateur de Documentation Infra (Mermaid)")
    st.markdown("Générez de la documentation d'infrastructure complète avec diagrammes Mermaid")
    
    # Sélection de la version du prompt
    prompt_loader = PromptLoader()
    versions = prompt_loader.list_available_versions("generateur_doc_infra")
    
    version_descriptions = {
        "v1": "Version initiale - Persona + Few-shot Learning",
        "v2": "Version améliorée - Chain of Thought + Diagrammes avancés",
        "v3": "Version avancée - Multi-diagrammes + Documentation enrichie",
        "v4": "Version optimisée - Templates + Export multi-formats",
        "vFinal": "Version finale - Consolidation des meilleures pratiques"
    }
    
    if versions:
        default_index = 0
        if "vFinal" in versions:
            default_index = versions.index("vFinal")
        elif "v4" in versions:
            default_index = versions.index("v4")
        
        prompt_version = st.selectbox(
            "Version du prompt",
            versions,
            index=default_index,
            format_func=lambda x: f"{x} - {version_descriptions.get(x, '')}" if version_descriptions.get(x) else x,
            help="Sélectionnez la version du prompt à utiliser"
        )
        
        if prompt_version in version_descriptions:
            st.info(f"ℹ️ **{prompt_version}** : {version_descriptions[prompt_version]}")
    else:
        prompt_version = "v1"
        st.warning("⚠️ Aucune version de prompt trouvée. Utilisation de v1 par défaut.")
    
    # Zone de saisie
    st.subheader("Décrivez votre infrastructure")
    infra_input = st.text_area(
        "Informations sur l'infrastructure",
        height=200,
        placeholder="Exemple: Architecture microservices avec API Gateway, 3 services backend, base de données PostgreSQL, cache Redis..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        generer_btn = st.button("🚀 Générer", type="primary", use_container_width=True)
    
    # Génération de la documentation
    if generer_btn and infra_input:
        generateur = GenerateurDocInfra(prompt_version=prompt_version)
        
        if generateur.test_prompt_injection(infra_input):
            st.error("⚠️ Tentative de prompt injection détectée !")
        else:
            with st.spinner("Génération en cours..."):
                try:
                    Config.validate()
                    resultat = generateur.generer(infra_input, prompt_version=prompt_version)
                    
                    st.subheader("📋 Documentation générée")
                    st.markdown(f"**Version utilisée** : `{prompt_version}`")
                    st.markdown("---")
                    st.markdown(resultat)
                    
                    st.download_button(
                        label="💾 Télécharger la documentation",
                        data=resultat,
                        file_name=f"doc_infra_{prompt_version}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Erreur lors de la génération: {e}")
    
    elif generer_btn and not infra_input:
        st.warning("⚠️ Veuillez décrire votre infrastructure")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>AI-Powered Dev Toolkit v1.0.0 | Projet de fin de formation</p>
    </div>
    """,
    unsafe_allow_html=True
)

