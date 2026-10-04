USE ELIDEK;


############
# Query 3.1
############
SELECT 
	program.program_id ,program.program_name , p.project_id, p.title 
FROM 
	program JOIN project p 
	ON program.program_id = p.program_id 
	WHERE 1=1 AND 
    p.start_date >= CURRENT_DATE() AND 
    p.duration = 1 AND 
    p.executive_id = 10;


############
# Query 3.3
############

# Steps
# -----
# 1) Select the all the active projects
# 2) Pick the active projects that relate to the popular scienitic field
# 3) Left outer join with the researchers who work on that projects in the last year
# 4) If a researcher is NULL then he worked for the desired project and scientific field
#    in a previous year 

SELECT
	smth.scientific_field_name, smth.project_id, smth.title, smth2.researcher_id
FROM
	(
	(
	SELECT ij1.project_id, ij1.title, ij2.scientific_field_name 
    FROM
	(
	SELECT p.project_id, p.title
    FROM Project p
	WHERE DATEDIFF(end_date, CURRENT_DATE()) > 0 AND DATEDIFF(start_date, CURRENT_DATE()) < 0 		# active projects	
	) AS ij1		# ij1 corresponds to the active projects
	INNER JOIN
    (
    SELECT rel.scientific_field_name, rel.project_id
    FROM Relates rel
    WHERE rel.scientific_field_name = 'Mathematics'
    ) AS ij2		# ij2 corresponds to the projects relate with the popular scientific field
    ON ij1.project_id = ij2.project_id
    ) AS smth		# smth corresponds to the active projects that relate to the popular scientific field
    LEFT OUTER JOIN WorksAtProject wap ON smth.project_id = wap.project_id
    LEFT OUTER JOIN 
    (
    SELECT r.researcher_id
    FROM Researcher r 
    WHERE TIMESTAMPDIFF(YEAR, r.work_starting_date, CURDATE()) < 0 
    ) AS smth2
    ON wap.researcher_id = smth2.researcher_id
    )

     
############
# Query 3.4
############

# Steps
# -----
# 1) Find the number of projects each organization started to manage each year 
#    (only for the years that the organization started to manage a project)	
# 2) Keep only the organizations and the years in which the organizations had 
#    at least 10 projects
# 3) Inner join the above relation with itself and keep only organizations that
#    in a 2-year duration started to manage the same amount of projects each year

# Example
# -------
# Suppose that we want to find the organanizations that in a 2-year duration 
# started to manage the same amount of projects each year and this amount must
# be at least 2 (instead of 10 for simplicity :) )

# Let's sat that the tables look like this (they will not look like this but whatever ...)

# organizationn_id		project_id		start_date
# ----------------		----------		----------
# 		org1				p2			22/10/2001
#		org1 				p3			27/05/2002
#		org1		 		p5			01/03/2005
#		org1	 			p7 			01/04/2005
#		org1				p8			03/07/2006
#		org1 				p4 			04/08/2006
#		org2				p1			20/05/1997
#		org2	 			p9 			21/06/1997


# After Step 1
# ------------
# organizationn_id		year		number_of_projects	
# ----------------		----		------------------
# 		org1			2001				1
#		org1			2002				1
# 		org1 			2005 				2
# 		org1			2006 				2
#		org1 			1997 				2		

# After Step 2
# ------------
# organizationn_id		year		number_of_projects	
# ----------------		----		------------------
# 		org1 			2005 				2
# 		org1			2006 				2
#		org1 			1997 				2

# After Step 3
# ------------
# organizationn_id	
# ----------------	
# 		org1 			
# For this query we made a view that stores the number of projects an organization starts to manage per year
# Our view is called prs_for_orgs_per_year	(projects for organizations per year)
SELECT DISTINCT 
	poy1.organizationn_id
FROM
	prs_for_orgs_per_year poy1
    INNER JOIN prs_for_orgs_per_year poy2 
    ON poy1.organizationn_id = poy2.organizationn_id
WHERE
	ABS(poy1.yearr - poy2.yearr) = 1 AND
	poy1.cc = poy2.cc AND
	poy1.cc > 10;


############
# Query 3.5
############
# 1) Find the scientific field pairs that occur for one project (r1)
# 2) Count the number of time each pair exists and order
# Note1: We know that scientific fields in relates table concern at least one project
# Note2: When we inner join a relation there is a possibility to have duplicates with reversed attributes
#		 For instance, suppose that we only have two tuples for a relation R with A,B attributes and we
#		 inner join R with itself on A
#		 	R	:	A	B			R AS R1 INNER JOIN R AS R2 ON A		:	A	R1.B	R2.B	
#		 			a1  b1  												a1   b1      b1
#		 			a1  b2  												a1   b1      b2
#		 																	a1   b2      b1
#		 																	a1	 b2      b2
# 		 To select only the attributes with differents b's we must demand that b1 > b2. This statement not olny
# 		 discards the tuples with same b's (ex. a1 b1 b1) but also selects the rows with different b's only once
# 		 (a1 b1 b2 without a1 b2 b1)
# 		 That's why we use the '>' operator in the where statement of our query :)

SELECT r1.sc1, r1.sc2, COUNT(*) AS cc 
FROM(
	SELECT
		rel1.scientific_field_name AS sc1, rel2.scientific_field_name AS sc2
	FROM
		Relates rel1
		INNER JOIN Relates rel2 ON rel1.project_id = rel2.project_id
	WHERE 
		rel1.scientific_field_name > rel2.scientific_field_name	# 2 or more scientific fields
	) r1 
GROUP BY r1.sc1, r1.sc2
ORDER BY cc DESC 			# decreasing order
LIMIT 3						# top 3

    
############
# Query 3.6
############
# 1) Find the young (age < 40) researchers that work at active projects (r1)
# 2) Inner Join with WorksAtProject
# 3) Inner Join with active projects
# 4) Count the active projects each young researchers works on

SELECT
	smth.researcher_id, COUNT(smth.project_id) AS Number_Of_Active_Projects	# smth.project_id
FROM
	(
    SELECT r1.researcher_id, wap.project_id
    FROM
    (
	(
	SELECT r1.researcher_id			# , TIMESTAMPDIFF(YEAR, r1.birth_date, CURDATE()) AS age
    FROM Researcher r1
    WHERE TIMESTAMPDIFF(YEAR, r1.birth_date, CURDATE()) < 40
    ) AS r1
    INNER JOIN WorksAtProject wap ON r1.researcher_id = wap.researcher_id
    INNER JOIN
    (
    SELECT p.project_id
    FROM Project p
    WHERE DATEDIFF(p.end_date, CURRENT_DATE()) > 0 AND 	# active projects
		  DATEDIFF(start_date, CURRENT_DATE()) < 0		# ###############	
    ) p1
    ON wap.project_id = p1.project_id
    )  
	) AS smth
# ORDER BY smth.researcher_id ASC
GROUP BY smth.researcher_id
ORDER BY Number_Of_Active_Projects DESC;


############
# Query 3.7
############
# 1) Find the executives that work for a company (which is a case of an organization, see relational model)
# 	 and the corresponding amounts, order them and keep the top 5	 
# Note: An executive can work for multiple projects, all of which are connected with the same organization. 
#		In that case, we must add the project.amounts for that pair of executive - organization
# Note_Example
# ------------
# executive_id		project_id		organization_id							  ------> p1
# -------------    ------------	    ----------------					 	 /			 \
#		1				1				  1				==========> 	ex_1			  ----> org1
#		1 				2 				  1									 \			 /
#																			  ------> p2
# Result (of query)
# -----------------
# executive_id		Total_Funding_Amount
# ------------- 	---------------------	
#		1	 		p1.amount + p2.amount				
# Question: what if an executive appears in the result 2 times because he has funded money to two different companies??
SELECT 
	ex.executive_name, org.organization_name, SUM(p.amount) AS Total_Funding_Amount
FROM
	Executive ex 
    INNER JOIN Project p ON ex.executive_id = p.executive_id
    INNER JOIN
    (
    SELECT org0.organizationn_id, org0.organization_name
	FROM Organizationn org0
	WHERE org0.company_budget IS NOT NULL	# the organization is a company
	) AS org	
    ON p.organizationn_id = org.organizationn_id
GROUP BY ex.executive_id, org.organizationn_id
ORDER BY Total_Funding_Amount DESC
LIMIT 5;


############
# Query 3.8
############
# 1) Find the (acitve) projects that have no deliverables using EXCEPT operator (r1)
# 2) Find the number of valid (active with no deliverables) projects each researcher works (r2) from r1
# 3) Pick only the researchers with more than 5 valid (active with no deliverables) projects from r2 (r3)

SELECT *
FROM
(
SELECT wap.researcher_id, COUNT(out1.project_id) AS Number_of_Valid_Projects
FROM(
    (
	SELECT p.project_id
	FROM Project p
    WHERE 	DATEDIFF(p.end_date, CURRENT_DATE) > 0 AND		# active proejcts
			DATEDIFF(p.start_date, CURRENT_DATE) < 0		# ############### 
    EXCEPT
    SELECT d.project_id
    FROM Deliverable d
    ) AS out1		# out1 corresponds to the valid projects (active with no deliverables)
    INNER JOIN WorksAtProject wap ON out1.project_id = wap.project_id    
)
GROUP BY wap.researcher_id
) AS r
WHERE r.Number_of_Valid_Projects > 4;
