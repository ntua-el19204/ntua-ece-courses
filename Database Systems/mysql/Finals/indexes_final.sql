# To create the indexes we need to count the number of times each column 
# appears in WHERE or INNER JOIN ON (critical) statements, and pick the 
# ones that appear more frequently and their corresponding columns have 
# multiple values to choose from. For instance, the column scinetific_field_name
# appears multiple times in our queries but will not have too many values
# compared to project_id

USE ELIDEK;

##########
# Indexes
##########

# p.project_id
# -------------
ALTER TABLE Project ADD INDEX p_project_id_index (project_id);

# p.start_date
# ----------
ALTER TABLE Project ADD INDEX project_start_date_index (start_date);

# p.end_date
# ----------
ALTER TABLE Project ADD INDEX project_end_date_index (end_date);

# p.organizationn_id
# ------------------
ALTER TABLE Project ADD INDEX p_organizationn_id_index (organizationn_id);

# org.organizationn_id
# --------------------
ALTER TABLE Organizationn ADD INDEX org_organizationn_id_index (organizationn_id);

# wap.project_id
# --------------
ALTER TABLE WorksAtProject ADD INDEX wap_project_index (project_id);

# Note that we have 3 indexes at Project, 1 index at Organizationn,
# and 1 index at WorksAtProject tables

