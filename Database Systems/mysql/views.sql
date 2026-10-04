USE Elidek;

# The following view stores stores the number of projects an organization starts to manage per year
CREATE VIEW  prs_for_orgs_per_year
AS
SELECT
	r.organizationn_id, r.yearr, COUNT(r.project_id) AS cc
FROM(
	SELECT
		org1.organizationn_id, p1.project_id, YEAR(p1.start_date) AS yearr
	FROM
		Organizationn org1
		INNER JOIN Project p1 ON org1.organizationn_id = p1.organizationn_id
	) r
GROUP BY r.organizationn_id, r.yearr;


# The following view stores the projects each researcher works
CREATE VIEW prs_per_res			# projects per researcher
AS
SELECT *
FROM WorksAtProject wap
ORDER BY wap.researcher_id;

