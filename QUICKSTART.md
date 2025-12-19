# 🚀 Guide de démarrage rapide

## Installation rapide

1. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

2. **Configurer les variables d'environnement**

Créez un fichier `.env` à la racine :
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=votre_cle_api_ici
```

Ou pour Claude :
```env
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=votre_cle_api_ici
```

3. **Lancer l'application**
```bash
streamlit run app.py
```

## Test rapide de l'Analyseur de Logs

1. Ouvrez l'application dans votre navigateur (http://localhost:8501)
2. Sélectionnez "1. Analyseur de Logs" dans la sidebar
3. Collez cet exemple de logs :
```
[2025-12-19 10:23:45] ERROR: Database connection failed: Connection timeout after 30s
[2025-12-19 10:23:46] ERROR: Retry attempt 1/3 failed
[2025-12-19 10:23:47] ERROR: Retry attempt 2/3 failed
[2025-12-19 10:23:48] ERROR: All retry attempts exhausted
[2025-12-19 10:23:50] WARN: Service degraded, falling back to cache
```
4. Cliquez sur "Analyser"
5. Consultez le résultat structuré !

## Structure des prompts

Les prompts sont versionnés dans `prompts/[nom_outil]/v1.txt` (puis v2.txt, vFinal.txt).

Pour modifier un prompt :
1. Éditez le fichier dans `prompts/[nom_outil]/v1.txt`
2. Ou créez une nouvelle version (v2.txt)
3. L'application détectera automatiquement les nouvelles versions

## Prochaines étapes

- Implémenter les 4 autres outils
- Tester et améliorer les prompts (v2, vFinal)
- Documenter l'architecture et les choix techniques

