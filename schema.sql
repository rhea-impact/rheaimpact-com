-- Rhea Impact volunteer signup schema
-- Run against rhea_apps database on pg-rhea

CREATE SCHEMA IF NOT EXISTS rheaimpact;

CREATE TABLE IF NOT EXISTS rheaimpact.volunteers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    location VARCHAR(255),
    reason TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    ip_hash VARCHAR(16),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_volunteers_email ON rheaimpact.volunteers(email);
CREATE INDEX IF NOT EXISTS idx_volunteers_created_at ON rheaimpact.volunteers(created_at);
