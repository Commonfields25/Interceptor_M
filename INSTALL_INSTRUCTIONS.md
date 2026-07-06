# Instructions d'installation pour l'intégration Supabase

## 1. Installer les dépendances
Exécutez la commande suivante pour installer les dépendances requises :
```bash
pip install -r requirements.txt
```

## 2. Configurer les variables d'environnement
Le fichier `.env` est déjà configuré avec les valeurs suivantes :
```
SUPABASE_URL=https://mgeuddriuvjxdlzlbjbz.supabase.co
SUPABASE_KEY=sb_publishable_3XIlKagqQG-GbedXcBkJJw_OshHwtbt
```

## 3. Lancer l'application
Exécutez l'application Flask avec la commande :
```bash
python app.py
```

## 4. (Optionnel) Installer les Agent Skills
Pour améliorer l'interaction avec Supabase, vous pouvez ajouter les Agent Skills :
```bash
npx skills add supabase/agent-skills
```
