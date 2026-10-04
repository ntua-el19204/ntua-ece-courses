DELIMITER $$

/*--------------------------  
    PROJECT TRIGGERS
------------------------- */ 

/*We check if the project has been evaluated before it starts*/
CREATE TRIGGER Evaluation_Date_Check
BEFORE INSERT ON  project
FOR EACH ROW
BEGIN
	declare Evaluation_Date datetime;

	set Evaluation_Date = (select Evaluation.evaluation_date from Evaluation where evaluation_id = new.evaluation_id);
	if (Date(Evaluation_Date) > new.start_date) then
		signal sqlstate '45000' set message_text = 'The project cant start if it has not been evaluated';
	end if;
END$$


/*We check if the project has been evaluated before it starts*/
CREATE TRIGGER Evaluation_Date_Check_On_Update
BEFORE UPDATE ON  project
FOR EACH ROW
BEGIN
	declare Evaluation_Date datetime;

	set Evaluation_Date = (select Evaluation.evaluation_date from Evaluation where evaluation_id = new.evaluation_id);
	if (Date(Evaluation_Date) > new.start_date) then
		signal sqlstate '45000' set message_text = 'The project cant start if it has not been evaluated';
	end if;
END$$





/*After the insert we put the chief at the works at project*/
CREATE TRIGGER Chief_Check									
AFTER INSERT ON  project
FOR EACH ROW
BEGIN
	/*We put our chief in WorksAtProject*/
    declare chief_start_work_date date;
    
    set chief_start_work_date = (select work_starting_date from researcher 
					where (researcher_id = new.chief_id and organizationn_id = new.organizationn_id));
    
    if (chief_start_work_date > new.start_date) then
		signal sqlstate '45004' set message_text = 'The Chief has to work at the organization before the start of the project !';
    end if;
    insert into worksatproject (researcher_id, project_id) values (new.chief_id, new.project_id);
    
END$$

/*If the new chief does not work at the project , we make them work*/
CREATE TRIGGER Check_On_Update_The_Chief		
AFTER UPDATE ON project
FOR EACH ROW
BEGIN
	declare cc int;
    
    set cc = (select count(*) from worksatproject where (researcher_id = new.chief_id));
    
    if(cc = 0)	then
		insert into worksatproject (researcher_id, project_id) values (new.chief_id, new.project_id);
	end if;
END$$

/*We check if he works at project's organization*/
CREATE TRIGGER Check_The_Evaluator                          
BEFORE INSERT ON  project                       
FOR EACH ROW
BEGIN
	declare Org_id int;
    
	/*We find the organization of the evaluator*/
    set Org_id = (select organizationn_id from researcher where researcher_id = new.evaluator_id); 
	
	
    if (Org_id = new.organizationn_id) then
		signal sqlstate '45004' set message_text = 'The evaluator can not work at the project s organization';
	end if;
END$$



/*We check if he works at project's organization*/
CREATE TRIGGER Check_The_Evaluator_On_Update                          
BEFORE UPDATE ON  project                       
FOR EACH ROW
BEGIN
	declare Org_id int;
    
	/*We find the organization of the evaluator*/
    set Org_id = (select organizationn_id from researcher where researcher_id = new.evaluator_id); 
	
	
    if (Org_id = new.organizationn_id) then
		signal sqlstate '45005' set message_text = 'The evaluator can not work at the project s organization';
	end if;
END$$



/*--------------------------  
    WORKS AT PROJECT
------------------------- */ 

/*Checks if the researcher works at the organization of the project*/
CREATE TRIGGER Checks_Org_Of_The_Researcher
BEFORE INSERT ON  worksatproject
FOR EACH ROW
BEGIN
	declare my_Resear_org_id int;
    declare my_Project_org_id int;
    
    set my_Resear_org_id = (select organizationn_id from researcher where researcher_id = new.researcher_id);
    
    set my_Project_org_id = (select organizationn_id from project where project_id = new.project_id);
    
    if (my_Resear_org_id != my_Project_org_id) then
		signal sqlstate '45005' set message_text = 'In this project can only work researchers who work in the project`s organization';
    end if;
END$$

/*Checks if the researcher works at the organization of the project*/
CREATE TRIGGER Checks_Org_Of_The_Researcher_On_Update
BEFORE UPDATE ON  worksatproject
FOR EACH ROW
BEGIN
	declare my_Resear_org_id int;
    declare my_Project_org_id int;
    
    set my_Resear_org_id = (select organizationn_id from researcher where researcher_id = new.researcher_id);
    
    set my_Project_org_id = (select organizationn_id from project where project_id = new.project_id);
    
    if (my_Resear_org_id != my_Project_org_id) then
		signal sqlstate '45005' set message_text = 'In this project can only work researchers who work in the project`s organization';
    end if;
END$$



/*Checks if the researcher is also the evaluator*/
CREATE TRIGGER Checks_Evaluator
BEFORE INSERT ON  worksatproject
FOR EACH ROW
BEGIN
	declare my_evaluator_id int;
    
    set my_evaluator_id = (select evaluator_id from project where project_id = new.project_id);
    
	if (my_evaluator_id = new.researcher_id)	then
		signal sqlstate '45006' set message_text = 'This researcher evaluates the project';
	end if;
END$$

/*Checks if the researcher is also evaluator*/
CREATE TRIGGER Checks_Evaluator_On_Update
BEFORE UPDATE ON  worksatproject
FOR EACH ROW
BEGIN
	declare my_evaluator_id int;
    
    set my_evaluator_id = (select evaluator_id from project where project_id = new.project_id);
    
	if (my_evaluator_id = new.researcher_id)	then
		signal sqlstate '45007' set message_text = 'This researcher evaluates the project';
	end if;
END$$

/*Checks if the researcher`s StartWorkingDate < End of the project*/
CREATE TRIGGER Checks_Researchers_Start_Working_Date
BEFORE INSERT ON  worksatproject
FOR EACH ROW
BEGIN
	declare Work_Start_Date date;
    declare End_of_program date;
    
    set Work_Start_Date = (select work_starting_date from researcher where researcher_id = new.researcher_id);
    set End_of_program  = (select end_date from project where project_id = new.project_id);
    
    if ( Work_Start_Date >= End_of_program) then 
		signal sqlstate '45007' set message_text = 'This Resarcher start to work in the organization after the end of the project';
    end if;
    
END$$

/*Checks if the researcher`s StartWorkingDate < End of the project*/
CREATE TRIGGER Checks_Researchers_Start_Working_Date_On_Update
BEFORE UPDATE ON  worksatproject
FOR EACH ROW
BEGIN
	declare Work_Start_Date date;
    declare End_of_program date;
    
    set Work_Start_Date = (select work_starting_date from researcher where researcher_id = new.researcher_id);
    set End_of_program  = (select end_date from project where project_id = new.project_id);
    
    if ( Work_Start_Date >= End_of_program) then 
		signal sqlstate '45007' set message_text = 'This Resarcher start to work in the organization after the end of the project';
    end if;
    
END$$

/*--------------------------  
       Deliverable
------------------------- */ 

/*Checks if delivery_date > project.end_date , if yes we raise an error*/
CREATE TRIGGER Check_Delivery_Date
BEFORE INSERT ON  deliverable
FOR EACH ROW
BEGIN
	declare end_of_project_date date;
    
    set end_of_project_date = (select end_date from project where project_id = new.project_id);
    
    if (new.delivery_date > end_of_project_date) then
		signal sqlstate '45008' set message_text = 'The delivery date can not be after the end of the project';
	end if;

END$$

/*Checks if delivery_date > project.end_date , if yes we raise an error*/
CREATE TRIGGER Check_Delivery_Date_On_Update
BEFORE UPDATE ON  deliverable
FOR EACH ROW
BEGIN
	declare end_of_project_date date;
    
    set end_of_project_date = (select end_date from project where project_id = new.project_id);
    
    if (new.delivery_date > end_of_project_date) then
		signal sqlstate '45009' set message_text = 'The delivery date can not be after the end of the project';
	end if;

END$$


/*--------------------------  
   ORGANIZATION TRIGGERS
------------------------- */ 
/*Checks what is the org*/
CREATE TRIGGER What_is_the_org
BEFORE INSERT ON organizationn
FOR EACH ROW
BEGIN
       if (new.company_budget is NULL) then
        set new.company_budget=0;
    end if;

    if (new.university_budget is NULL) then
        set new.university_budget=0;
    end if;

    if (new.research_center_budget is NULL) then
        set new.research_center_budget=0;
    end if;

	if (new.company_budget = 0 and new.university_budget =0 and new.research_center_budget =0 ) then
	    	signal sqlstate '45000' set message_text = 'You have to put a budget !';
	end if;

	if(  (new.company_budget + new.university_budget + new.research_center_budget !=  new.company_budget) and
		 (new.company_budget + new.university_budget + new.research_center_budget !=  new.university_budget) and
         (new.company_budget + new.university_budget + new.research_center_budget !=  new.research_center_budget)
	) then
		signal sqlstate '45000' set message_text = 'The organization has to be one thing (Company or Uni or Center)';
    end if;
   
END$$
/*Checks what is the org*/
CREATE TRIGGER What_is_the_org_up
BEFORE UPDATE ON organizationn
FOR EACH ROW
BEGIN
       if (new.company_budget is NULL) then
        set new.company_budget=0;
    end if;

    if (new.university_budget is NULL) then
        set new.university_budget=0;
    end if;

    if (new.research_center_budget is NULL) then
        set new.research_center_budget=0;
    end if;

	if (new.company_budget = 0 and new.university_budget =0 and new.research_center_budget =0 ) then
	    	signal sqlstate '45001' set message_text = 'You have to put a budget !';
	end if;

	if(  (new.company_budget + new.university_budget + new.research_center_budget !=  new.company_budget) and
		 (new.company_budget + new.university_budget + new.research_center_budget !=  new.university_budget) and
         (new.company_budget + new.university_budget + new.research_center_budget !=  new.research_center_budget)
	) then
		signal sqlstate '45000' set message_text = 'The organization has to be one thing (Company or Uni or Center)';
    end if;
END$$

/*--------------------------  
    RESEARCHER TRIGGERS
------------------------- */ 

/*Checks if a researcher is valid, considering his age. A researcher cannot work before he is 22 y.o.*/
CREATE TRIGGER Age_of_Researcher
BEFORE INSERT ON researcher
FOR EACH ROW
BEGIN
	declare diff int;
	set diff = DATEDIFF(new.work_starting_date, new.birth_date) / 365;
	if (diff < 22) then
		signal sqlstate '45000' set message_text = 'The person is not old enough to be a researcher... Maybe in a couple of years?';
	end if;
END$$

/*Checks if a researcher is valid, considering his age. A researcher cannot work before he is 22 y.o.*/
CREATE TRIGGER Age_of_Researcher_On_Update
BEFORE UPDATE ON researcher
FOR EACH ROW
BEGIN
	declare diff int;
	set diff = DATEDIFF(new.work_starting_date, new.birth_date) / 365;
	if (diff < 22) then
		signal sqlstate '45000' set message_text = 'The person is not old enough to be a researcher... Maybe in a couple of years?';
	end if;
END$$

/*The following line has to be at the end of the file*/
DELIMITER ;