
CREATE DATABASE ELIDEK;

/* =====================
	CREATE ENTITIES 
======================*/
USE ELIDEK;


CREATE TABLE IF NOT EXISTS Project(
	project_id int PRIMARY KEY AUTO_INCREMENT not null, 
	title VARCHAR (40), 
	summary VARCHAR (40), 
	start_date DATE not null,
	end_date DATE not null,
	CONSTRAINT chk_dates CHECK((start_date < end_date) AND (start_date >= '1994-01-01')),
	amount INT,
	duration INT AS (DATEDIFF(end_date, start_date) / 365),	#duration is a derived attribute.
    CONSTRAINT CHK_Date CHECK (duration IN (1,2,3,4)),
    organizationn_id INT,
    executive_id INT ,
    program_id INT,
    evaluation_id INT unique,    #unique
    evaluator_id INT,
    chief_id INT 
);


CREATE TABLE IF NOT EXISTS Organizationn(
	organizationn_id INT PRIMARY KEY auto_increment NOT NULL,
    organization_name VARCHAR(50),
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
	CONSTRAINT CHK_birth_date CHECK (birth_date <= '1993-12-31' and birth_date >= '1955-5-24'),
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
	CONSTRAINT CHK_Grade CHECK (grade IN (1,2,3,4,5,6,7,8,9,10)),
    evaluation_date DATE
    );

CREATE TABLE IF NOT EXISTS Executive(
	executive_id INT PRIMARY KEY AUTO_INCREMENT,
    executive_name varchar(20)
);

CREATE TABLE IF NOT EXISTS Phones(
	phone DECIMAL(10,0),
    organizationn_id INT,
	PRIMARY KEY (phone,organizationn_id)
);


/* =====================
	CREATE RELATIONS
======================*/

CREATE TABLE IF NOT EXISTS Relates(
	scientific_field_name VARCHAR(30),  
    project_id INT,
    PRIMARY KEY (scientific_field_name,project_id),
    FOREIGN KEY(scientific_field_name) REFERENCES Scientific_Field(scientific_field_name) ON DELETE CASCADE,
    FOREIGN KEY(scientific_field_name) REFERENCES Scientific_Field(scientific_field_name) ON UPDATE CASCADE,
    FOREIGN KEY(project_id) REFERENCES Project(project_id) ON DELETE CASCADE,
	FOREIGN KEY(project_id) REFERENCES Project(project_id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS WorksAtProject(
	researcher_id INT,
    project_id INT,
    PRIMARY KEY (researcher_id, project_id),
    FOREIGN KEY(researcher_id) REFERENCES Researcher(researcher_id) ON DELETE CASCADE,
    FOREIGN KEY(researcher_id) REFERENCES Researcher(researcher_id) ON UPDATE CASCADE,
    FOREIGN KEY(project_id) REFERENCES Project(project_id) ON DELETE CASCADE,
    FOREIGN KEY(project_id) REFERENCES Project(project_id) ON UPDATE CASCADE
);

/* =====================
	ADD FOREIGN KEYS
======================*/

/*On delete*/

# Project
# --------
ALTER TABLE Project ADD  CONSTRAINT Project_program_id_FK FOREIGN KEY (program_id) REFERENCES Program(program_id) ON DELETE cascade;
ALTER TABLE Project ADD  CONSTRAINT Project_evaluation_id_FK FOREIGN KEY(evaluation_id) REFERENCES Evaluation(evaluation_id) ON DELETE cascade;
ALTER TABLE Project ADD CONSTRAINT Project_executive_id_FK FOREIGN KEY (executive_id) REFERENCES Executive(executive_id) ON DELETE cascade;
ALTER TABLE Project ADD  CONSTRAINT Project_evaluator_id_FK FOREIGN KEY (evaluator_id) REFERENCES Researcher(researcher_id) ON DELETE cascade;
ALTER TABLE Project ADD  CONSTRAINT Project_chief_id_FK FOREIGN KEY (chief_id) REFERENCES Researcher(researcher_id) ON DELETE cascade;
ALTER TABLE Project ADD  CONSTRAINT Project_organizationn_id_FK FOREIGN KEY (organizationn_id) REFERENCES Organizationn(organizationn_id) ON DELETE cascade;

# Deliverable
# ------------
ALTER TABLE Deliverable ADD  CONSTRAINT Deliverable_project_id_FK FOREIGN KEY (project_id) REFERENCES Project(project_id) ON DELETE CASCADE;

# Researcher
# ----------
ALTER TABLE Researcher ADD  CONSTRAINT Researcher_researcher_id_FK FOREIGN KEY (organizationn_id) REFERENCES Organizationn(organizationn_id) ON DELETE CASCADE;

# Phones
# -------
ALTER TABLE Phones ADD  CONSTRAINT Phones_organizationn_id_FK FOREIGN KEY (organizationn_id) REFERENCES Organizationn(organizationn_id) ON DELETE CASCADE;

/*On update*/

# Project
# --------
ALTER TABLE Project ADD  CONSTRAINT Project_program_id_FK_1 FOREIGN KEY (program_id) REFERENCES Program(program_id) ON UPDATE cascade;
ALTER TABLE Project ADD  CONSTRAINT Project_evaluation_id_FK_1 FOREIGN KEY(evaluation_id) REFERENCES Evaluation(evaluation_id) ON UPDATE cascade;
ALTER TABLE Project ADD CONSTRAINT Project_executive_id_FK_1 FOREIGN KEY (executive_id) REFERENCES Executive(executive_id) ON UPDATE cascade;
ALTER TABLE Project ADD  CONSTRAINT Project_evaluator_id_FK_1 FOREIGN KEY (evaluator_id) REFERENCES Researcher(researcher_id) ON UPDATE cascade;
ALTER TABLE Project ADD  CONSTRAINT Project_chief_id_FK_1 FOREIGN KEY (chief_id) REFERENCES Researcher(researcher_id) ON UPDATE cascade;
ALTER TABLE Project ADD  CONSTRAINT Project_organizationn_id_FK_1 FOREIGN KEY (organizationn_id) REFERENCES Organizationn(organizationn_id) ON UPDATE cascade;

# Deliverable
# ------------
ALTER TABLE Deliverable ADD  CONSTRAINT Deliverable_project_id_FK_1 FOREIGN KEY (project_id) REFERENCES Project(project_id) ON UPDATE CASCADE;

# Researcher
# ----------
ALTER TABLE Researcher ADD  CONSTRAINT Researcher_researcher_id_FK_1 FOREIGN KEY (organizationn_id) REFERENCES Organizationn(organizationn_id) ON UPDATE cascade;

# Phones
# -------
ALTER TABLE Phones ADD  CONSTRAINT Phones_organizationn_id_FK_1 FOREIGN KEY (organizationn_id) REFERENCES Organizationn(organizationn_id) ON UPDATE CASCADE;




