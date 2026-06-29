-- ============================================================
-- Interceptor_M - Supabase Schema
-- Système multi-agents avec gestion des rapports et simulations
-- ============================================================

-- Extensions nécessaires
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- TABLE: agents
-- Définition des agents du système Interceptor_M
-- ============================================================
CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(10) UNIQUE NOT NULL,  -- E1, E2, E3, D1, D2, D3, AM, AC, G1, G2, etc.
    agent_name VARCHAR(100) NOT NULL,
    agent_type VARCHAR(50) NOT NULL,  -- EXPLORATION, DISCRIMINATION, AUTO-MODEL, AUTO-CORRECT, GOUVERNANCE
    description TEXT,
    color VARCHAR(7) DEFAULT '#6B7280',
    icon VARCHAR(10) DEFAULT '🤖',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TABLE: agent_reports
-- Rapports quotidiens des agents [AGENT]|[DATE]|[ACTIONS]|[BLOCAGES]|[BESOINS]
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(10) NOT NULL REFERENCES agents(agent_id) ON DELETE CASCADE,
    report_date DATE NOT NULL,
    actions_taken TEXT NOT NULL,
    blocages TEXT,  -- Blocages courants
    besoins TEXT,   -- Besoins en ressources/assistance
    raw_format TEXT,  -- Format original [AGENT]|[DATE]|[ACTIONS]|[BLOCAGES]|[BESOINS]
    status VARCHAR(20) DEFAULT 'submitted' CHECK (status IN ('draft', 'submitted', 'reviewed', 'archived')),
    submitted_by VARCHAR(100),
    reviewed_by VARCHAR(100),
    review_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Contraintes
    UNIQUE(agent_id, report_date)
);

-- Index pour requêtes fréquentes
CREATE INDEX idx_reports_agent_date ON agent_reports(agent_id, report_date DESC);
CREATE INDEX idx_reports_status ON agent_reports(status);
CREATE INDEX idx_reports_created ON agent_reports(created_at DESC);

-- ============================================================
-- TABLE: simulation_results
-- Résultats des simulations RL/CFD
-- ============================================================
CREATE TABLE IF NOT EXISTS simulation_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    simulation_name VARCHAR(200) NOT NULL,
    simulation_type VARCHAR(50) NOT NULL,  -- RL_TRAINING, CFD, MULTI_PHYSICS
    agent_id VARCHAR(10),  -- Agent responsable (optionnel)
    
    -- Paramètres de simulation
    config JSONB NOT NULL DEFAULT '{}',
    hyperparameters JSONB DEFAULT '{}',
    
    -- Résultats
    metrics JSONB NOT NULL DEFAULT '{}',
    reward_history JSONB DEFAULT '[]',
    loss_history JSONB DEFAULT '[]',
    
    -- Métadonnées
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    duration_seconds INTEGER,
    
    -- Fichiers/assets
    artifacts JSONB DEFAULT '[]',  -- URLs vers les fichiers de sortie
    logs TEXT,
    
    created_by VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour les requêtes de métriques
CREATE INDEX idx_sim_results_type ON simulation_results(simulation_type);
CREATE INDEX idx_sim_results_status ON simulation_results(status);
CREATE INDEX idx_sim_results_agent ON simulation_results(agent_id);
CREATE INDEX idx_sim_results_created ON simulation_results(created_at DESC);

-- ============================================================
-- TABLE: linear_tasks
-- Synchronisation des tâches Linear avec GitHub
-- ============================================================
CREATE TABLE IF NOT EXISTS linear_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    linear_id VARCHAR(50) UNIQUE,  -- ID Linear officiel
    linear_identifier VARCHAR(20),  -- IDENTIFIER ex: INT-123
    github_issue_id INTEGER,
    github_issue_url TEXT,
    
    title VARCHAR(500) NOT NULL,
    description TEXT,
    state VARCHAR(50),
    priority INTEGER DEFAULT 0,
    
    -- Labels
    labels JSONB DEFAULT '[]',
    linear_labels JSONB DEFAULT '[]',
    
    -- Relations
    agent_id VARCHAR(10) REFERENCES agents(agent_id),
    milestone VARCHAR(100),
    
    -- Cycle de vie
    assignee VARCHAR(100),
    due_date DATE,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    
    -- Métadonnées
    source VARCHAR(20) DEFAULT 'linear' CHECK (source IN ('linear', 'github', 'manual')),
    synced_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX idx_linear_tasks_linear_id ON linear_tasks(linear_id);
CREATE INDEX idx_linear_tasks_github_id ON linear_tasks(github_issue_id);
CREATE INDEX idx_linear_tasks_state ON linear_tasks(state);
CREATE INDEX idx_linear_tasks_agent ON linear_tasks(agent_id);

-- ============================================================
-- TABLE: milestones
-- Milestones du projet Interceptor_M
-- ============================================================
CREATE TABLE IF NOT EXISTS milestones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    milestone_name VARCHAR(200) NOT NULL,
    milestone_code VARCHAR(20) UNIQUE,  -- M1, M2, M3...
    description TEXT,
    target_date DATE,
    
    -- Statut
    status VARCHAR(20) DEFAULT 'planning' CHECK (status IN ('planning', 'active', 'completed', 'cancelled')),
    completion_date DATE,
    
    -- Relations
    parent_milestone VARCHAR(20),  -- Pour les sous-milestones
    linear_milestone_id VARCHAR(50),
    
    -- Métadonnées
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_milestones_status ON milestones(status);
CREATE INDEX idx_milestones_target ON milestones(target_date);

-- ============================================================
-- TABLE: agent_logs
-- Logs détaillés des actions des agents
-- ============================================================
CREATE TABLE IF NOT EXISTS agent_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(10) NOT NULL REFERENCES agents(agent_id) ON DELETE CASCADE,
    
    -- Action
    action_type VARCHAR(50) NOT NULL,  -- EXPLORE, DISCRIMINATE, TRAIN, CORRECT, GOVERN
    action_description TEXT,
    raw_log TEXT,
    
    -- Contexte
    context JSONB DEFAULT '{}',
    parent_action_id UUID REFERENCES agent_logs(id),
    
    -- Résultats
    result JSONB DEFAULT '{}',
    success BOOLEAN,
    error_message TEXT,
    
    -- Timestamps
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    duration_ms INTEGER
);

-- Index pour requêtes analytiques
CREATE INDEX idx_logs_agent_action ON agent_logs(agent_id, action_type);
CREATE INDEX idx_logs_started ON agent_logs(started_at DESC);
CREATE INDEX idx_logs_success ON agent_logs(success);

-- ============================================================
-- TABLE: alerts
-- Alertes pour blocages et événements critiques
-- ============================================================
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_type VARCHAR(50) NOT NULL,  -- BLOCKAGE, METRIC_THRESHOLD, TASK_OVERDUE
    severity VARCHAR(20) DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    
    title VARCHAR(200) NOT NULL,
    message TEXT,
    
    -- Source
    source_type VARCHAR(20),  -- AGENT, SIMULATION, LINEAR, MANUAL
    source_id VARCHAR(100),
    agent_id VARCHAR(10),
    
    -- Statut
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'acknowledged', 'resolved', 'archived')),
    acknowledged_by VARCHAR(100),
    acknowledged_at TIMESTAMPTZ,
    resolved_by VARCHAR(100),
    resolved_at TIMESTAMPTZ,
    
    -- Canaux de notification
    notify_slack BOOLEAN DEFAULT false,
    notify_email BOOLEAN DEFAULT false,
    slack_channel VARCHAR(100),
    
    -- Métadonnées
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_alerts_agent ON alerts(agent_id);
CREATE INDEX idx_alerts_created ON alerts(created_at DESC);

-- ============================================================
-- VUES pour analytics et reporting
-- ============================================================

-- Vue: Statut des agents aujourd'hui
CREATE OR REPLACE VIEW v_agent_daily_status AS
SELECT 
    a.agent_id,
    a.agent_name,
    a.agent_type,
    a.color,
    a.icon,
    COALESCE(r.actions_taken, 'Pas de rapport') as last_report,
    COALESCE(r.blocages, 'Aucun') as current_blocages,
    r.report_date,
    r.status as report_status,
    CASE 
        WHEN r.report_date = CURRENT_DATE THEN 'reported_today'
        WHEN r.report_date = CURRENT_DATE - INTERVAL '1 day' THEN 'reported_yesterday'
        ELSE 'no_recent_report'
    END as report_freshness
FROM agents a
LEFT JOIN agent_reports r ON a.agent_id = r.agent_id 
    AND r.report_date = (
        SELECT MAX(report_date) 
        FROM agent_reports 
        WHERE agent_id = a.agent_id
    )
WHERE a.is_active = true
ORDER BY a.agent_type, a.agent_id;

-- Vue: Tâches actives par agent
CREATE OR REPLACE VIEW v_active_tasks AS
SELECT 
    lt.linear_identifier,
    lt.title,
    lt.state,
    lt.priority,
    lt.agent_id,
    lt.assignee,
    lt.due_date,
    a.agent_name,
    a.agent_type,
    a.color
FROM linear_tasks lt
LEFT JOIN agents a ON lt.agent_id = a.agent_id
WHERE lt.state NOT IN ('completed', 'cancelled', 'done')
ORDER BY lt.priority DESC, lt.due_date ASC;

-- Vue: Blocages actifs (> 2 heures)
CREATE OR REPLACE VIEW v_active_blocages AS
SELECT 
    ar.agent_id,
    a.agent_name,
    a.agent_type,
    ar.actions_taken,
    ar.blocages,
    ar.report_date,
    ar.created_at,
    EXTRACT(EPOCH FROM (NOW() - ar.created_at))/3600 as hours_old
FROM agent_reports ar
JOIN agents a ON ar.agent_id = a.agent_id
WHERE ar.blocages IS NOT NULL 
    AND ar.blocages != ''
    AND ar.created_at < NOW() - INTERVAL '2 hours'
    AND ar.status != 'archived'
ORDER BY hours_old DESC;

-- Vue: Progression des milestones
CREATE OR REPLACE VIEW v_milestone_progress AS
SELECT 
    m.milestone_code,
    m.milestone_name,
    m.target_date,
    m.status,
    m.progress,
    COUNT(lt.id) as total_tasks,
    COUNT(CASE WHEN lt.state IN ('completed', 'done') THEN 1 END) as completed_tasks,
    COUNT(CASE WHEN lt.state NOT IN ('completed', 'done', 'cancelled') THEN 1 END) as pending_tasks,
    ROUND(
        COUNT(CASE WHEN lt.state IN ('completed', 'done') THEN 1 END)::NUMERIC / 
        NULLIF(COUNT(lt.id), 0) * 100, 
        1
    ) as completion_percentage
FROM milestones m
LEFT JOIN linear_tasks lt ON lt.milestone = m.milestone_code
GROUP BY m.id, m.milestone_code, m.milestone_name, m.target_date, m.status, m.progress
ORDER BY m.target_date;

-- ============================================================
-- FONCTIONS et TRIGGERS
-- ============================================================

-- Fonction: Mise à jour automatique updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers pour updated_at automatique
CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_reports_updated_at BEFORE UPDATE ON agent_reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_simulation_results_updated_at BEFORE UPDATE ON simulation_results
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_linear_tasks_updated_at BEFORE UPDATE ON linear_tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_milestones_updated_at BEFORE UPDATE ON milestones
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_alerts_updated_at BEFORE UPDATE ON alerts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Fonction: Créer une alerte pour blocages
CREATE OR REPLACE FUNCTION create_blocage_alert()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.blocages IS NOT NULL AND NEW.blocages != '' 
        AND (OLD.blocages IS NULL OR OLD.blocages = '' OR OLD.blocages != NEW.blocages) THEN
        
        INSERT INTO alerts (alert_type, severity, title, message, source_type, source_id, agent_id)
        VALUES (
            'BLOCKAGE',
            'high',
            'Nouveau blocage détecté - Agent ' || NEW.agent_id,
            'L''agent ' || NEW.agent_id || ' a signalé un blocage:\n\n' || NEW.blocages,
            'AGENT',
            NEW.id::TEXT,
            NEW.agent_id
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_blocage_alert
AFTER INSERT OR UPDATE ON agent_reports
FOR EACH ROW EXECUTE FUNCTION create_blocage_alert();

-- Fonction: Statistiques globales
CREATE OR REPLACE FUNCTION get_project_stats()
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'total_agents', (SELECT COUNT(*) FROM agents WHERE is_active = true),
        'active_blocages', (SELECT COUNT(*) FROM agent_reports WHERE blocages IS NOT NULL AND blocages != '' AND created_at > NOW() - INTERVAL '24 hours'),
        'pending_tasks', (SELECT COUNT(*) FROM linear_tasks WHERE state NOT IN ('completed', 'done', 'cancelled')),
        'running_simulations', (SELECT COUNT(*) FROM simulation_results WHERE status = 'running'),
        'active_milestones', (SELECT COUNT(*) FROM milestones WHERE status = 'active'),
        'alerts_open', (SELECT COUNT(*) FROM alerts WHERE status = 'active'),
        'reports_today', (SELECT COUNT(*) FROM agent_reports WHERE report_date = CURRENT_DATE),
        'last_sync', (SELECT MAX(synced_at) FROM linear_tasks)
    ) INTO result;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================

ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE simulation_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE linear_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE milestones ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

-- Politiques par défaut (à adapter selon vos besoins)
CREATE POLICY "Public read for all authenticated users" ON agents
    FOR SELECT USING (true);

CREATE POLICY "Public read for all authenticated users" ON agent_reports
    FOR SELECT USING (true);

CREATE POLICY "Public read for all authenticated users" ON simulation_results
    FOR SELECT USING (true);

CREATE POLICY "Public read for all authenticated users" ON linear_tasks
    FOR SELECT USING (true);

CREATE POLICY "Public read for all authenticated users" ON milestones
    FOR SELECT USING (true);

CREATE POLICY "Public read for all authenticated users" ON agent_logs
    FOR SELECT USING (true);

CREATE POLICY "Public read for all authenticated users" ON alerts
    FOR SELECT USING (true);

-- INSERT/UPDATE policies (à affiner)
CREATE POLICY "Users can insert their own reports" ON agent_reports
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update reports" ON agent_reports
    FOR UPDATE USING (true);

-- ============================================================
-- GRANT (à adapter)
-- ============================================================
-- GRANT USAGE ON SCHEMA public TO authenticated;
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
-- GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- ============================================================
-- SEED DATA: Agents
-- ============================================================
-- Voir supabase_seed_data.json pour les données initiales
