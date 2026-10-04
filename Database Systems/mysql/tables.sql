CREATE DATABASE ELIDEK;

/* =====================
	CREATE ENTITIES 
======================*/
USE ELIDEK;


CREATE TABLE IF NOT EXISTS Project(
	project_id int PRIMARY KEY AUTO_INCREMENT, 
	title VARCHAR (40), 
	summary VARCHAR (40), 
	start_date DATE,
	end_date DATE, 
	amount INT,
	duration INT AS (DATEDIFF(end_date, start_date) / 365), 		# duration is a derived attribute
    CHECK (duration IN (1,2,3,4)),
    organizationn_id INT,
    executive_id INT,
    program_id INT,
    evaluation_id INT,
    researcher_id INT
);


CREATE TABLE IF NOT EXISTS Organizationn(
	organizationn_id INT PRIMARY KEY AUTO_INCREMENT,
    organization_name VARCHAR(40),
    abbreviation VARCHAR(10),
    postal_code INT,
    street VARCHAR(30),
    numberr INT,
    city VARCHAR(30),
    company_budget INT,
    university_budget INT,
    research_center_budget INT
);

CREATE TABLE IF NOT EXISTS Researcher(
	researcher_id INT PRIMARY KEY AUTO_INCREMENT,
    researcher_name VARCHAR(20),
    researcher_surname VARCHAR(20),
    sex VARCHAR(10),
    birth_date DATE,
    work_starting_date DATE,
    organizationn_id INT
);

CREATE TABLE IF NOT EXISTS Deliverable(
	title VARCHAR(50) PRIMARY KEY,
    summary VARCHAR(50),
    delivery_date DATE,
    project_id INT
);

CREATE TABLE IF NOT EXISTS Program(
	program_id INT PRIMARY KEY AUTO_INCREMENT,
    program_name VARCHAR(40),
    address VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS Scientific_Field(
	scientific_field_name varchar(30) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Evaluation(
	evaluation_id INT PRIMARY KEY AUTO_INCREMENT,
    grade INT, 
    evaluation_date DATE
);

CREATE TABLE IF NOT EXISTS Executive(
	executive_id INT PRIMARY KEY AUTO_INCREMENT,
    executive_name varchar(20)
);

CREATE TABLE IF NOT EXISTS Phones(
	phone DECIMAL(10,0),
    organizationn_id INT
);


/* =====================
	CREATE RELATIONS
======================*/

CREATE TABLE IF NOT EXISTS Relates(
	scientific_field_name VARCHAR(30),  
    project_id INT,
    FOREIGN KEY(scientific_field_name) REFERENCES Scientific_Field(scientific_field_name) ON DELETE SET NULL,
    FOREIGN KEY(project_id) REFERENCES Project(project_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS WorksAtProject(
	researcher_id INT,
    project_id INT,
    FOREIGN KEY(researcher_id) REFERENCES Researcher(researcher_id) ON DELETE CASCADE,
    FOREIGN KEY(project_id) REFERENCES Project(project_id) ON DELETE SET NULL
);

/* =====================
	ADD FOREIGN KEYS
======================*/

# Project
# --------
ALTER TABLE Project ADD  CONSTRAINT Project_program_id_FK FOREIGN KEY (program_id) REFERENCES Program(program_id) ON DELETE SET NULL;
ALTER TABLE Project ADD  CONSTRAINT Project_evaluation_id_FK FOREIGN KEY(evaluation_id) REFERENCES Evaluation(evaluation_id) ON DELETE SET NULL;
ALTER TABLE Project ADD CONSTRAINT Project_executive_id_FK FOREIGN KEY (executive_id) REFERENCES Executive(executive_id) ON DELETE SET NULL;
ALTER TABLE Project ADD  CONSTRAINT Project_researcher_id_FK FOREIGN KEY (researcher_id) REFERENCES Researcher(researcher_id) ON DELETE SET NULL;
ALTER TABLE Project ADD  CONSTRAINT Project_organizationn_id_FK FOREIGN KEY (organizationn_id) REFERENCES Organizationn(organizationn_id) ON DELETE SET NULL;

# Deliverable
# ------------
ALTER TABLE Deliverable ADD  CONSTRAINT Deliverable_project_id_FK FOREIGN KEY (project_id) REFERENCES Project(project_id) ON DELETE SET NULL;

# Researcher
# ----------
ALTER TABLE Researcher ADD  CONSTRAINT Researcher_researcher_id_FK FOREIGN KEY (organizationn_id) REFERENCES Organizationn(organizationn_id) ON DELETE SET NULL;

# Phones
# -------
ALTER TABLE Phones ADD  CONSTRAINT Phones_organizationn_id_FK FOREIGN KEY (organizationn_id) REFERENCES Organizationn(organizationn_id) ON DELETE SET NULL;



