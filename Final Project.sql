-- Tony Sax
-- Mark Raymond Jr.
-- CS 2300 Fall 2016

CREATE TABLE `university` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `uploader` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uploader_email` (`email`)
);


CREATE TABLE `rating` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `relevant_yes` int(11) NOT NULL,
  `useful_yes` int(11) NOT NULL,
  `total_useful_votes` int(11) NOT NULL,
  `total_relevance_votes` int(11) NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `school_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_school_id` (`school_id`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`school_id`) REFERENCES `university` (`id`)
);



CREATE TABLE `user_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `semester` varchar(255) NOT NULL,
  `server_name` varchar(255) NOT NULL,
  `date_uploaded` varchar(255) NOT NULL,
  `grade` varchar(255) NOT NULL,
  `uploaded_by` varchar(255) NOT NULL,
  `rating_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_file_rating_id` (`rating_id`),
  KEY `user_file_course_id` (`course_id`),
  CONSTRAINT `user_file_ibfk_1` FOREIGN KEY (`rating_id`) REFERENCES `rating` (`id`),
  CONSTRAINT `user_file_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`)
);


INSERT INTO `studybuddy`.`uploader` (`id`, `username`, `email`, `password`) 
	VALUES ('1', 'Mark', 'mark@mst.edu', 'password');
INSERT INTO `studybuddy`.`uploader` (`id`, `username`, `email`, `password`) 
	VALUES ('2', 'Tony', 'tony@mst.edu', 'password');

INSERT INTO `studybuddy`.`university` (`id`, `name`) 
	VALUES ('1', 'Missouri University of Science and Technology');

INSERT INTO `studybuddy`.`university` (`id`, `name`) 
	VALUES ('2', 'University of Missouri Saint Louis');

INSERT INTO `studybuddy`.`university` (`id`, `name`) 
	VALUES ('3', 'University of Missouri Kansas City');

INSERT INTO `studybuddy`.`university` (`id`, `name`) 
	VALUES ('4', 'Missouri State University Springfield');

INSERT INTO `studybuddy`.`university` (`id`, `name`) 
	VALUES ('5', 'University of Missouri Columbia');

INSERT INTO `studybuddy`.`course` (`id`, `name`, `subject`, `school_id`) 
	VALUES ('1', 'Discrete Mathematics', 'Computer Science', '1');
    
INSERT INTO `studybuddy`.`course` (`id`, `name`, `subject`, `school_id`) 
	VALUES ('2', 'Intro to File Structures and Databases', 'Computer Science', '1');
    
INSERT INTO `studybuddy`.`course` (`id`, `name`, `subject`, `school_id`) 
	VALUES ('3', 'Introduction to Geothermal Processes', 'Geology', '4');

INSERT INTO `studybuddy`.`course` (`id`, `name`, `subject`, `school_id`) 
	VALUES ('4', 'Introduction to Geothermal Processes', 'Geology', '2');

INSERT INTO `studybuddy`.`course` (`id`, `name`, `subject`, `school_id`) 
  VALUES ('5', 'Calculus 1 For Engineers', 'Math', '1');

INSERT INTO `studybuddy`.`course` (`id`, `name`, `subject`, `school_id`) 
  VALUES ('6', 'Calculus 2', 'Math', '4');

INSERT INTO `studybuddy`.`course` (`id`, `name`, `subject`, `school_id`) 
  VALUES ('7', 'Advanced Domain Exploration and Innovation Methods', 'Economics', '1');

INSERT INTO `studybuddy`.`user_file` (`id`, `name`, `semester`, `server_name`, `date_uploaded`, `grade`, `uploaded_by`, `rating_id`, `course_id`) 
	VALUES ('1', 'Discrete Math Exam 1', 'Fall 2016', 'Discrete_Exam_1_Mark.pdf', '5-10-2016', 'A', 'mark@mst.edu', '1', '1');

INSERT INTO `studybuddy`.`rating` (`id`, `relevant_yes`, `useful_yes`, `total_useful_votes`, `total_relevance_votes`) 
	VALUES ('1', '12', '9', '12', '12');

