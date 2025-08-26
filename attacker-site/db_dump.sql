-- Fake database dump to entice attackers
-- This file contains fake sensitive data to make the honeypot more attractive

-- Employee Database
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id VARCHAR(10) UNIQUE,
    username VARCHAR(50),
    password_hash VARCHAR(255),
    email VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    ssn VARCHAR(11),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO employees (employee_id, username, password_hash, email, department, salary, ssn) VALUES
('EMP001', 'jsmith', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3bp.Gm.QG6', 'j.smith@securecorpnet.com', 'IT', 75000.00, '123-45-6789'),
('EMP002', 'mjohnson', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'm.johnson@securecorpnet.com', 'Finance', 82000.00, '987-65-4321'),
('EMP003', 'admin', '$2b$12$gp45Hdeoxp/fQ/AWHDb94uImNbhyjoZjBNZfkqP4b4q1.Dh19q', 'admin@securecorpnet.com', 'IT', 95000.00, '555-12-3456'),
('EMP004', 'dbrown', '$2b$12$4f67O5RY/uS9.cOvuJdqAOvMg5XmznkwHahKdXSMP5vdgCRrmu/mG', 'd.brown@securecorpnet.com', 'HR', 68000.00, '111-22-3333'),
('EMP005', 'root', '$2b$12$N9qo8uLOickgx2ZMRZoMye.IjdQcfrdVixVhRMQdN8kkTriVw.gf6', 'root@securecorpnet.com', 'IT', 120000.00, '999-88-7777');

-- Customer Database
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id VARCHAR(20),
    company_name VARCHAR(100),
    contact_email VARCHAR(100),
    phone VARCHAR(20),
    credit_limit DECIMAL(12,2),
    account_balance DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO customers (customer_id, company_name, contact_email, phone, credit_limit, account_balance) VALUES
('CUST001', 'TechCorp Industries', 'billing@techcorp.com', '555-0101', 500000.00, 125000.00),
('CUST002', 'Global Solutions LLC', 'finance@globalsol.com', '555-0202', 750000.00, 340000.00),
('CUST003', 'MegaCorp Enterprises', 'accounts@megacorp.com', '555-0303', 1000000.00, 890000.00),
('CUST004', 'StartupXYZ Inc', 'admin@startupxyz.com', '555-0404', 100000.00, 45000.00);

-- Financial Transactions
CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id VARCHAR(50),
    customer_id VARCHAR(20),
    amount DECIMAL(12,2),
    transaction_type VARCHAR(20),
    account_number VARCHAR(20),
    routing_number VARCHAR(9),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO transactions (transaction_id, customer_id, amount, transaction_type, account_number, routing_number) VALUES
('TXN001', 'CUST001', 25000.00, 'CREDIT', '1234567890123456', '021000021'),
('TXN002', 'CUST002', 50000.00, 'DEBIT', '9876543210987654', '011401533'),
('TXN003', 'CUST003', 100000.00, 'CREDIT', '5555444433332222', '121000248'),
('TXN004', 'CUST004', 15000.00, 'DEBIT', '1111222233334444', '026009593');

-- System Configuration (fake sensitive data)
CREATE TABLE system_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100),
    config_value TEXT,
    is_sensitive BOOLEAN DEFAULT FALSE
);

INSERT INTO system_config (config_key, config_value, is_sensitive) VALUES
('database_host', '192.168.1.100', TRUE),
('database_password', 'SuperSecretDB123!', TRUE),
('api_key', 'sk-1234567890abcdef1234567890abcdef', TRUE),
('encryption_key', 'AES256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', TRUE),
('backup_location', '\\\\fileserver\\backups\\daily', FALSE),
('admin_email', 'admin@securecorpnet.com', FALSE);

-- Fake credit card data (for honeypot purposes only)
CREATE TABLE payment_methods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id VARCHAR(20),
    card_number VARCHAR(19),
    expiry_date VARCHAR(7),
    cvv VARCHAR(4),
    cardholder_name VARCHAR(100)
);

INSERT INTO payment_methods (customer_id, card_number, expiry_date, cvv, cardholder_name) VALUES
('CUST001', '4532-1234-5678-9012', '12/2025', '123', 'John Smith'),
('CUST002', '5555-4444-3333-2222', '06/2026', '456', 'Jane Johnson'),
('CUST003', '3782-8224-6310-005', '09/2024', '789', 'Robert Brown'),
('CUST004', '6011-1111-1111-1117', '03/2027', '321', 'Sarah Davis');

-- Server credentials (fake)
CREATE TABLE server_access (
    id INT PRIMARY KEY AUTO_INCREMENT,
    server_name VARCHAR(50),
    ip_address VARCHAR(15),
    username VARCHAR(50),
    password VARCHAR(100),
    ssh_key TEXT,
    purpose VARCHAR(100)
);

INSERT INTO server_access (server_name, ip_address, username, password, ssh_key, purpose) VALUES
('prod-web-01', '10.0.1.10', 'root', 'Pr0dW3b$erv3r!', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ...', 'Production Web Server'),
('db-master', '10.0.1.20', 'dbadmin', 'D4t4b4s3M4st3r#', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ...', 'Primary Database Server'),
('backup-srv', '10.0.1.30', 'backup', 'B4ckup$3rv3r2023', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ...', 'Backup Server'),
('mail-server', '10.0.1.40', 'postfix', 'M41lS3rv3rP4ss!', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ...', 'Email Server');

-- VPN Access (fake)
CREATE TABLE vpn_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(100),
    vpn_profile TEXT,
    last_login TIMESTAMP,
    access_level VARCHAR(20)
);

INSERT INTO vpn_users (username, password, vpn_profile, last_login, access_level) VALUES
('vpn_admin', 'VPN4dm1n!2023', 'admin.ovpn', '2023-12-01 09:15:00', 'ADMIN'),
('remote_user1', 'R3m0t3Us3r#1', 'user1.ovpn', '2023-12-01 08:30:00', 'USER'),
('contractor1', 'C0ntr4ct0r$1', 'contractor.ovpn', '2023-11-30 14:45:00', 'LIMITED');

-- WARNING: This is a honeypot database dump
-- All data is fake and for security research purposes only
-- Any attempt to use this data for malicious purposes will be logged and reported
