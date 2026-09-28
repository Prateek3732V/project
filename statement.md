
# ** Problem Statement**
Traditional warehouse operations often struggle with manual stock tracking, lack of transactional visibility, and weak role-based security. Without a centralized database, businesses face frequent inventory discrepancies, untracked stock movements, delayed reorder responses due to unmonitored low stock, and unauthorized access to administrative controls.

There is a need for a centralized, database-driven Warehouse Management System that segregates operational duties across user roles (Admins, Managers, Sales Persons), automates transactional logging for inbound and outbound inventory movements, provides real-time stock valuation and threshold reporting, and manages supplier relationships efficiently.

## ** Scope of Project**
In-Scope
Database Integration: Direct connection and automated table initialization using MySQL relational database (warehouse_management).

Role-Based Access Control (RBAC): Tiered authentication system enforcing distinct menu interfaces and privileges for Sales Persons, Managers, and Admins.

Supplier Management: Functionalities to add, view, and remove supplier records linked directly to inventory items.

Product Catalog Operations: Dynamic searching (by name, ID, or full display), product insertion with pricing, and catalog deletion.

Stock Movement & Auditing: Real-time stock inward (receiving) and outward (issuing) actions, accompanied by automated timestamped transaction logs in a dedicated ledger (stock_movements).

Inventory Control & Reporting: Manual stock adjustments, custom low-stock threshold queries, and total inventory financial valuation calculation.

User Account Management: CRUD operations for system credentials across all administrative and staff user tiers.

Out-of-Scope
Graphical User Interface (GUI) or web/mobile interface (currently strictly CLI/terminal-based).

Advanced cryptographic password hashing (currently processes plain text credentials).

Automated email notifications or automated purchase order generation for low-stock items.

Barcode/RFID hardware scanning integrations.

### ** Target Users**
Warehouse Administrators: System managers responsible for user account management (creating, editing, and deleting Admin, Manager, and Sales Person credentials) and overarching platform control.

Warehouse Managers: Operational supervisors who manage supplier relationships, add/remove product inventory, perform manual stock adjustments, monitor movement history logs, evaluate low-stock alerts, and calculate financial stock valuation.

Sales Persons: Counter/sales staff tasked with checking item availability, searching catalog details, and processing outgoing stock transactions against customer orders.

#### ** High-Level Features**
1. Multi-Tier Authentication & Access Control
Role-Based Workspaces: Context-aware user menus tailored specifically to the credentials entered during login:

Sales Person Menu: Restricted to product search and stock issuing.

Manager Menu: Access to supplier management, inventory updates, movement history, and financial metrics.

Admin Menu: Full access to all managerial tasks plus complete system user administration.

Credential Verification: Database lookup matching User ID, Username, and Password across role-specific database tables (sales_person, managers, admins).

2. Supplier Management Module
Supplier Onboarding: Register new suppliers with unique IDs, names, and contact details.

Supplier Registry: Display complete lists of registered suppliers to ensure relational integrity before attaching products.

Supplier Deletion: Remove inactive suppliers from the database.

3. Product Catalog & Search
Flexible Search Engine: Search product catalog by partial product name (fuzzy search via SQL LIKE), exact product ID, or full inventory dump.

Product Registration: Add new inventory items linked to verified Supplier IDs, complete with descriptions, unit prices, and initial stock quantities.

Product Maintenance: Delete obsolete product entries from the system database.

4. Real-Time Stock Transaction Logging
Stock Inward (Receive): Increase product stock quantity upon receiving shipments from suppliers.

Stock Outward (Issue): Deduct product stock quantity upon sales or distribution.

Automated Audit Ledger: Automatically records every IN/OUT transaction in the stock_movements table, tracking movement ID, product ID, transaction type, quantity, and exact database timestamp (NOW()).

Movement History Report: View complete historic logs of all incoming and outgoing inventory changes.

5. Inventory Analytics & Control
Stock Adjustment Override: Manually set exact stock quantities to resolve physical audit discrepancies.

Low-Stock Alerting: Generate reports listing products falling below a user-defined threshold quantity to prevent stockouts.

Stock Valuation Engine: Dynamically calculate and report the total monetary value of current warehouse assets using the formula:

Total Valuation=∑(Price×Stock Quantity)
6. System User Administration (Admin Only)
Account Lifecycle Management: Add, edit (username/password updates), or remove user profiles across all three operational tiers (admins, managers, sales_person).