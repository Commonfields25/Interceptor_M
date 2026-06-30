-- Schéma pour Supabase : Stockage des données des agents et des simulations

-- 1. Table des Agents
CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    namespace TEXT NOT NULL,
    workspace TEXT NOT NULL,
    status TEXT DEFAULT 'OPERATIONAL',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Table des Milestones
CREATE TABLE IF NOT EXISTS milestones (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    due_date TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Table des Rapports Quotidiens des Agents
CREATE TABLE IF NOT EXISTS agent_reports (
    id SERIAL PRIMARY KEY,
    agent_id TEXT NOT NULL REFERENCES agents(id),
    date DATE NOT NULL,
    actions TEXT NOT NULL,
    blockages TEXT,
    needs TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Table des Résultats de Simulation
CREATE TABLE IF NOT EXISTS simulation_results (
    id SERIAL PRIMARY KEY,
    agent_id TEXT NOT NULL REFERENCES agents(id),
    simulation_name TEXT NOT NULL,
    parameters JSONB,
    results JSONB,
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Table des Blocages
CREATE TABLE IF NOT EXISTS blockages (
    id SERIAL PRIMARY KEY,
    agent_id TEXT NOT NULL REFERENCES agents(id),
    issue_title TEXT NOT NULL,
    issue_description TEXT,
    start_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_time TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'OPEN',
    severity TEXT DEFAULT 'LOW'
);

-- 6. Table des Alertes
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    agent_id TEXT REFERENCES agents(id),
    message TEXT NOT NULL,
    type TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved BOOLEAN DEFAULT FALSE
);

-- 7. Table des Logs d'Exécution
CREATE TABLE IF NOT EXISTS execution_logs (
    id SERIAL PRIMARY KEY,
    agent_id TEXT NOT NULL REFERENCES agents(id),
    action TEXT NOT NULL,
    details JSONB,
    status TEXT DEFAULT 'SUCCESS',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour optimiser les requêtes
CREATE INDEX IF NOT EXISTS idx_agent_reports_agent_id ON agent_reports(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_reports_date ON agent_reports(date);
CREATE INDEX IF NOT EXISTS idx_simulation_results_agent_id ON simulation_results(agent_id);
CREATE INDEX IF NOT EXISTS idx_blockages_agent_id ON blockages(agent_id);
CREATE INDEX IF NOT EXISTS idx_blockages_status ON blockages(status);
CREATE INDEX IF NOT EXISTS idx_alerts_agent_id ON alerts(agent_id);
CREATE INDEX IF NOT EXISTS idx_alerts_resolved ON alerts(resolved);

-- Trigger pour mettre à jour updated_at dans la table agents
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_agents_updated_at
    BEFORE UPDATE ON agents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Fonction pour vérifier les blocages > 2h
CREATE OR REPLACE FUNCTION check_long_blockages()
RETURNS TRIGGER AS $$
DECLARE
    blockage_duration INTERVAL;
BEGIN
    IF NEW.status = 'OPEN' THEN
        blockage_duration = NOW() - NEW.start_time;
        IF blockage_duration > INTERVAL '2 hours' THEN
            INSERT INTO alerts (agent_id, message, type)
            VALUES (NEW.agent_id, 
                    'Blocage > 2h détecté pour l'agent ' || NEW.agent_id || ': ' || NEW.issue_title,
                    'BLOCKAGE');
        END IF;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_check_long_blockages
    AFTER INSERT OR UPDATE ON blockages
    FOR EACH ROW
    EXECUTE FUNCTION check_long_blockages();
