USE ELIDEK;

# Query 3.7

# evaluations
insert into evaluation (grade, evaluation_date) values (6, '2021-07-31');
insert into evaluation (grade, evaluation_date) values (3, '2020-12-06');
insert into evaluation (grade, evaluation_date) values (3, '2021-11-15');
insert into evaluation (grade, evaluation_date) values (4, '2021-04-13');
insert into evaluation (grade, evaluation_date) values (9, '2021-10-27');
insert into evaluation (grade, evaluation_date) values (7, '2020-08-20');
insert into evaluation (grade, evaluation_date) values (1, '2022-02-20');
insert into evaluation (grade, evaluation_date) values (7, '2020-08-20');
insert into evaluation (grade, evaluation_date) values (9, '2021-10-05');
insert into evaluation (grade, evaluation_date) values (2, '2022-03-23');

# executives
insert into executive (executive_name) values ('Nikola');
insert into executive (executive_name) values ('Tate');
insert into executive (executive_name) values ('Johannah');
insert into executive (executive_name) values ('Brice');
insert into executive (executive_name) values ('Rod');
insert into executive (executive_name) values ('Rawley');
insert into executive (executive_name) values ('Candy');
insert into executive (executive_name) values ('Tracy');
insert into executive (executive_name) values ('Nikolas');
insert into executive (executive_name) values ('Oliy');

# organizations
insert into Organizationn ( organization_name, abbreviation, postal_code, street, numberr, city, company_budget) values ('Université Henri Poincaré (Nancy I)', 'DC', '20470', 'Holy Cross', '767', 'Washington', '826467062');
insert into Organizationn ( organization_name, abbreviation, postal_code, street, numberr, city, university_budget) values ('Universidad Adventista de Chile', 'NY', '12305', 'Melby', '3', 'Schenectady', '801509051');
insert into Organizationn ( organization_name, abbreviation, postal_code, street, numberr, city, company_budget) values ('St. Johns & St. Terezas Institute of Technology', 'GA', '30336', 'Village Green', '28', 'Atlanta', '487353689');
insert into Organizationn ( organization_name, abbreviation, postal_code, street, numberr, city, company_budget) values ('Tongji University', 'AK', '99709', 'Del Mar', '963', 'Fairbanks', '508531874');
insert into Organizationn ( organization_name, abbreviation, postal_code, street, numberr, city, university_budget) values ('Soran University', 'NY', '10292', 'Alpine', '640', 'New York City', '263309960');

# researchers
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Grady', 'Yandell', 'Male', '1990-02-07', '2018-05-02', 1);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Dinnie', 'Beckworth', 'Female', '1993-04-05', '2017-06-27', 2);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Gilburt', 'Setchell', 'Male', '1991-04-30', '2019-01-17', 4);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Boris', 'Reame', 'Male', '1968-01-21', '2017-10-06', 3);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('August', 'Kubiak', 'Male', '1993-04-03', '2018-03-01', 5);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Jonas', 'McCoughan', 'Male', '1992-01-13', '2018-04-29', 4);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Tommi', 'Scholte', 'Female', '1991-12-29', '2018-03-02', 1);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Mason', 'Mougel', 'Male', '1991-08-27', '2020-02-23', 2);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Riley', 'Tosspell', 'Male', '1991-05-14', '2019-09-13', 3);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Leslie', 'Lawlings', 'Female', '1984-11-06', '2018-01-08', 4);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Anna-diane', 'Longmire', 'Female', '1990-08-12', '2019-11-15', 5);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Doyle', 'Marson', 'Male', '1991-02-13', '2017-12-16', 5);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Connor', 'Daulton', 'Male', '1956-07-21', '2021-03-01', 3);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Findley', 'Leatham', 'Male', '1991-12-25', '2021-08-13', 4);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Joelie', 'Huelin', 'Female', '1991-01-01', '2019-06-12', 4);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Roseline', 'O''Corhane', 'Female', '1991-07-13', '2018-04-12', 2);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Nessy', 'Valentine', 'Female', '1991-03-12', '2020-02-23', 2);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Lia', 'Catonne', 'Female', '1991-09-18', '2018-02-10', 1);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Ursa', 'Cuthill', 'Female', '1991-09-07', '2017-11-17', 4);
insert into Researcher (researcher_name, researcher_surname, sex, birth_date, work_starting_date, organizationn_id) values ('Marni', 'Smalles', 'Female', '1991-06-02', '2017-08-06', 1);

# program
insert into Program (program_id, program_name, address) values (1, 'Pennie', 'Marketing');
insert into Program (program_id, program_name, address) values (2, 'Sly', 'Legal');
insert into Program (program_id, program_name, address) values (3, 'Courtney', 'Research and Development');
insert into Program (program_id, program_name, address) values (4, 'Bastian', 'Legal');
insert into Program (program_id, program_name, address) values (5, 'Aube', 'Legal');
insert into Program (program_id, program_name, address) values (6, 'Lannie', 'Product Management');
insert into Program (program_id, program_name, address) values (7, 'Zitella', 'Marketing');
insert into Program (program_id, program_name, address) values (8, 'Colene', 'Training');
insert into Program (program_id, program_name, address) values (9, 'Casi', 'Sales');

# project
insert into Project (title, summary, start_date, end_date, amount, organizationn_id, executive_id, program_id, evaluation_id, evaluator_id, chief_id) values ('Cardguard', 'Multi-channelled incremental encryption', '2020-10-13', '2023-07-23', 919331, 1, 1, 1, 1, 1, 1);
insert into Project (title, summary, start_date, end_date, amount, organizationn_id, executive_id, program_id, evaluation_id, evaluator_id, chief_id) values ('Holdlamis', 'Cross-group local service-desk', '2019-07-08', '2022-05-14', 336493, 1, 1, 2, 2, 2, 2);
insert into Project (title, summary, start_date, end_date, amount, organizationn_id, executive_id, program_id, evaluation_id, evaluator_id, chief_id) values ('Zamit', 'User-centric user-facing emulation', '2019-05-11', '2023-11-05', 220979, 1, 2, 3, 3, 3, 3);
insert into Project (title, summary, start_date, end_date, amount, organizationn_id, executive_id, program_id, evaluation_id, evaluator_id, chief_id) values ('Hatity', 'Balanced optimal interface', '2020-02-21', '2023-10-30', 161501, 3, 2, 4, 4, 4, 4);
insert into Project (title, summary, start_date, end_date, amount, organizationn_id, executive_id, program_id, evaluation_id, evaluator_id, chief_id) values ('Flexidy', 'Open-source maximized time-frame', '2020-01-31', '2024-04-08', 629775, 3, 7, 5, 5, 5, 5);
insert into Project (title, summary, start_date, end_date, amount, organizationn_id, executive_id, program_id, evaluation_id, evaluator_id, chief_id) values ('Andalax', 'Visionary global methodology', '2021-09-02', '2023-03-07', 425631, 3, 2, 6, 6, 6, 6);
insert into Project (title, summary, start_date, end_date, amount, organizationn_id, executive_id, program_id, evaluation_id, evaluator_id, chief_id) values ('Cardguard', 'Innovative 24 hour contingency', '2021-06-23', '2025-07-12', 100749, 3, 5, 7, 7, 7, 7);
insert into Project (title, summary, start_date, end_date, amount, organizationn_id, executive_id, program_id, evaluation_id, evaluator_id, chief_id) values ('Biodex', 'Grass-roots exuding capability', '2020-10-20', '2023-03-10', 534312, 1, 4, 8, 8, 8, 8);
insert into Project (title, summary, start_date, end_date, amount, organizationn_id, executive_id, program_id, evaluation_id, evaluator_id, chief_id) values ('Latlux', 'Expanded human-resource secured line', '2019-01-30', '2020-02-25', 361843, 1, 3, 9, 9, 9, 9);
insert into Project (title, summary, start_date, end_date, amount, organizationn_id, executive_id, program_id, evaluation_id, evaluator_id, chief_id) values ('Gembucket', 'Compatible directional data-warehouse', '2020-12-13', '2023-11-24', 667056, 1, 2, 9, 10, 10, 10);

# worksatproject
insert into WorksAtProject (researcher_id, project_id) values (1, 5);
insert into WorksAtProject (researcher_id, project_id) values (2, 4);
insert into WorksAtProject (researcher_id, project_id) values (3, 6);
insert into WorksAtProject (researcher_id, project_id) values (4, 7);
insert into WorksAtProject (researcher_id, project_id) values (5, 3);
insert into WorksAtProject (researcher_id, project_id) values (6, 2);
insert into WorksAtProject (researcher_id, project_id) values (7, 8);
insert into WorksAtProject (researcher_id, project_id) values (8, 9);
insert into WorksAtProject (researcher_id, project_id) values (9, 1);
insert into WorksAtProject (researcher_id, project_id) values (10, 10);
insert into WorksAtProject (researcher_id, project_id) values (1, 6);
insert into WorksAtProject (researcher_id, project_id) values (1, 7);
insert into WorksAtProject (researcher_id, project_id) values (2, 8);
insert into WorksAtProject (researcher_id, project_id) values (3, 1);
insert into WorksAtProject (researcher_id, project_id) values (3, 2);
insert into WorksAtProject (researcher_id, project_id) values (3, 3);
insert into WorksAtProject (researcher_id, project_id) values (3, 4);
insert into WorksAtProject (researcher_id, project_id) values (3, 5);
insert into WorksAtProject (researcher_id, project_id) values (3, 10);
insert into WorksAtProject (researcher_id, project_id) values (4, 8);

# scientific field
insert into Scientific_Field (scientific_field_name) values ('Natural Sciences');
insert into Scientific_Field (scientific_field_name) values ('Engineering and Technology');
insert into Scientific_Field (scientific_field_name) values ('Life Sciences');
insert into Scientific_Field (scientific_field_name) values ('Agricultural Sciences');
insert into Scientific_Field (scientific_field_name) values ('Mathematics');
insert into Scientific_Field (scientific_field_name) values ('Social Sciences');
insert into Scientific_Field (scientific_field_name) values ('Humanity Sciences and Art');
insert into Scientific_Field (scientific_field_name) values ('Environment and Energy');
insert into Scientific_Field (scientific_field_name) values ('Business and Management Administration');

# relates
insert into Relates (scientific_field_name, project_id) values ('Mathematics', 1);
insert into Relates (scientific_field_name, project_id) values ('Environment and Energy', 1);
insert into Relates (scientific_field_name, project_id) values ('Environment and Energy', 4);
insert into Relates (scientific_field_name, project_id) values ('Environment and Energy', 8);
insert into Relates (scientific_field_name, project_id) values ('Mathematics', 2);
insert into Relates (scientific_field_name, project_id) values ('Humanity Sciences and Art', 4);
insert into Relates (scientific_field_name, project_id) values ('Environment and Energy', 5);
insert into Relates (scientific_field_name, project_id) values ('Environment and Energy', 3);
insert into Relates (scientific_field_name, project_id) values ('Mathematics', 6);
insert into Relates (scientific_field_name, project_id) values ('Mathematics', 8);
insert into Relates (scientific_field_name, project_id) values ('Natural Sciences', 7);
insert into Relates (scientific_field_name, project_id) values ('Business and Management Administration', 9);
insert into Relates (scientific_field_name, project_id) values ('Humanity Sciences and Art', 8);
insert into Relates (scientific_field_name, project_id) values ('Environment and Energy', 6);
insert into Relates (scientific_field_name, project_id) values ('Business and Management Administration', 4);
insert into Relates (scientific_field_name, project_id) values ('Business and Management Administration', 7);
insert into Relates (scientific_field_name, project_id) values ('Humanity Sciences and Art', 6);
insert into Relates (scientific_field_name, project_id) values ('Mathematics', 4);


