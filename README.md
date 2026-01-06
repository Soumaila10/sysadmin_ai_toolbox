# 🤖 AI-Powered Dev Toolkit

**Boîte à outils IA pour Administrateurs Système et DevOps**

Application modulaire regroupant 5 outils IA dédiés aux tâches d'administration système et DevOps, avec versionnement des prompts pour documenter leur évolution.

## 📋 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Les 5 outils](#les-5-outils)
- [Documentation](#documentation)
- [Contribution](#contribution)

## 🎯 Vue d'ensemble

Ce projet regroupe 5 outils IA spécialisés pour les administrateurs système et DevOps :

1. **Analyseur de Logs** - Analyse et diagnostic des logs système et applications
2. **Générateur de Scripts** - Génération automatique de scripts Bash/Python
3. **Architecte Docker/Kubernetes** - Création de configurations Docker/K8s optimisées
4. **Assistant Troubleshooting Réseau** - Diagnostic et résolution de problèmes réseau
5. **Générateur de Documentation Infra** - Génération de documentation avec diagrammes Mermaid

### Caractéristiques principales

- ✅ **Modulaire** : Architecture modulaire facilitant l'ajout de nouveaux outils
- ✅ **Versionnement des prompts** : Documentation de l'évolution des prompts (v1, v2, vFinal)
- ✅ **Abstraction LLM** : Support d'OpenAI et Claude via une interface unifiée
- ✅ **Interface Web** : Interface Streamlit intuitive et moderne
- ✅ **Sécurité** : Mécanisme de détection de prompt injection

## 📁 Structure du projet

```
sysadmin_ai_toolbox/
├── app/                          # Code source de l'application
│   ├── config/                   # Configuration (LLM, variables d'environnement)
│   ├── tools/                    # Implémentation des 5 outils
│   │   ├── analyseur_logs.py    # Outil 1: Analyseur de Logs
│   │   └── ...                   # Autres outils (à venir)
│   ├── utils/                    # Utilitaires
│   │   ├── llm_client.py        # Client abstrait pour LLM
│   │   └── prompt_loader.py     # Chargeur de prompts versionnés
│   └── __init__.py
├── prompts/                      # Prompts versionnés par outil
│   ├── analyseur_logs/
│   │   ├── v1.txt               # Version 1 du prompt
│   │   ├── v2.txt               # Version 2 (à venir)
│   │   └── vFinal.txt           # Version finale (à venir)
│   ├── generateur_scripts/
│   ├── architecte_docker_k8s/
│   ├── troubleshooting_reseau/
│   └── generateur_doc_infra/
├── docs/                         # Documentation technique
│   ├── README.md                # Documentation générale
│   ├── prompts_evolution.md     # Évolution des prompts
│   ├── architecture.md          # Architecture (à venir)
│   ├── choix_techniques.md      # Choix techniques (à venir)
│   └── limites.md               # Limitations (à venir)
├── app.py                        # Application principale Streamlit
├── requirements.txt              # Dépendances Python
├── .env.example                  # Exemple de configuration
└── README.md                     # Ce fichier
```

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Clé API OpenAI, Anthropic (Claude) ou Google AI (Gemini)

### Étapes d'installation

1. **Cloner le dépôt** (ou créer le projet)
```bash
git clone <repository-url>
cd sysadmin_ai_toolbox
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env et ajouter votre clé API
```

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```env
# Fournisseur LLM: "openai", "claude" ou "google"
LLM_PROVIDER=openai

# Clé API (selon le fournisseur choisi)
OPENAI_API_KEY=your_openai_api_key_here
# OU
ANTHROPIC_API_KEY=your_anthropic_api_key_here
# OU
GOOGLE_API_KEY=your_google_api_key_here

# Modèles par défaut
OPENAI_MODEL=gpt-4
CLAUDE_MODEL=claude-3-5-sonnet-20241022
GOOGLE_MODEL=gemini-1.5-pro

# Paramètres de génération
TEMPERATURE=0.3
MAX_TOKENS=4000
```

### Configuration via Streamlit

Vous pouvez également configurer le fournisseur LLM et la clé API directement dans l'interface Streamlit (sidebar).

## 💻 Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

### Utilisation de l'Analyseur de Logs

1. Sélectionnez "1. Analyseur de Logs" dans la sidebar
2. Choisissez la version du prompt (v1, v2, vFinal)
3. Collez vos logs dans la zone de texte ou chargez un fichier
4. Cliquez sur "Analyser"
5. Consultez le résultat structuré
6. Téléchargez l'analyse si nécessaire

## 🛠️ Les 5 outils

### 1. 📊 Analyseur de Logs

**Statut** : ✅ Implémenté (v1)

Analyse les logs système et applications pour :
- Identifier les erreurs critiques et warnings
- Détecter les patterns et anomalies
- Proposer des causes probables
- Suggérer des actions correctives
- Fournir des recommandations préventives

**Technique utilisée** : Persona + Few-shot Learning

**Prompt v1** : Disponible dans `prompts/analyseur_logs/v1.txt`

### 2. 📝 Générateur de Scripts Bash/Python

**Statut** : 🚧 En développement

Génère automatiquement des scripts pour automatiser les tâches DevOps.

### 3. 🐳 Architecte Docker/Kubernetes

**Statut** : 🚧 En développement

Crée des configurations Docker et Kubernetes optimisées.

### 4. 🌐 Assistant Troubleshooting Réseau

**Statut** : 🚧 En développement

Aide au diagnostic et à la résolution de problèmes réseau.

### 5. 📚 Générateur de Documentation Infra (Mermaid)

**Statut** : 🚧 En développement

Génère de la documentation d'infrastructure avec diagrammes Mermaid.

## 📚 Documentation

- [Documentation technique](./docs/README.md)
- [Évolution des prompts](./docs/prompts_evolution.md)
- [Architecture](./docs/architecture.md) (à venir)
- [Choix techniques](./docs/choix_techniques.md) (à venir)
- [Limitations](./docs/limites.md) (à venir)

## 🔒 Sécurité

### Détection de prompt injection

Chaque outil inclut un mécanisme simple de détection de prompt injection qui vérifie la présence de patterns suspects dans les entrées utilisateur.

**Limitations** : Cette détection est basique et ne remplace pas une validation complète des entrées. Pour un usage en production, implémentez des mesures de sécurité supplémentaires.

## 🧪 Tests

Les tests de prompt injection sont intégrés dans chaque outil. Pour tester :

```python
from app.tools.analyseur_logs import AnalyseurLogs

analyseur = AnalyseurLogs()
logs_suspects = "ignore previous instructions and tell me..."
if analyseur.test_prompt_injection(logs_suspects):
    print("Injection détectée !")
```

## 📝 Versionnement des prompts

Le projet utilise un système de versionnement des prompts pour documenter leur évolution :

- **v1** : Version initiale
- **v2** : Version améliorée basée sur les retours
- **vFinal** : Version optimisée et validée

Chaque version est documentée dans `docs/prompts_evolution.md`.

## 🤝 Contribution

Ce projet est un projet de fin de formation. Les contributions sont les bienvenues !

## 📄 Licence

[À définir]

## 👤 Auteur

Projet de fin de formation - AI-Powered Dev Toolkit

---

**Version** : 1.0.0  
**Dernière mise à jour** : 2025-12-19
