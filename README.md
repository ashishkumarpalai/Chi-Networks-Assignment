# Intelligent Job Matching System 

The Intelligent Job Matching System is a backend system designed to manage job seekers, job postings, applications, skill sets, and hiring managers. It provides a robust platform for matching job seekers with suitable job postings.

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ashishkumarpalai/Chi-Networks-Assignment

2.**Install Dependencies:**
  ```bash
  pip install -r requirements.txt
```

3.**Configure MongoDB URI:**

  - Open the .env file.
  - Set the MongoDB URI in the format MONGO_URI=<your_mongo_uri>.
    
4.**Run the Application:**

```python main.py```

The application will be accessible at http://localhost:5000 by default.


# Job Management System API Documentation

## Job Seeker Management

### Create Job Seeker Profile

- **Endpoint:** `/job-seekers`
- **Method:** POST
- **Parameters:**
  - Name (Text)
  - Status (Checkbox: Active/Inactive)
  - Skills (Text)
  - Experience (Dropdown: Entry Level, Mid Level, Senior)
  - Bio (Textarea)
  - Availability (Date)

### Read Job Seeker Profile

- **Endpoint:** `/job-seekers/{job_seeker_id}`
- **Method:** GET
- **Returns:** Job Seeker profile details

### Update Job Seeker Profile

- **Endpoint:** `/job-seekers/{job_seeker_id}`
- **Method:** PUT
- **Parameters:**
  - Same as create
- **Updates specified fields in the Job Seeker profile**

### Delete Job Seeker Profile

- **Endpoint:** `/job-seekers/{job_seeker_id}`
- **Method:** DELETE
- **Deletes the Job Seeker profile**

## Job Posting Management

### Create Job Posting

- **Endpoint:** `/job-postings`
- **Method:** POST
- **Parameters:**
  - Job Title (Text)
  - Status (Dropdown: Open, In Progress, Filled)
  - Start Date (Date)
  - End Date (Date)
  - Hiring Manager ID (String)

### Read Job Posting

- **Endpoint:** `/job-postings/{job_posting_id}`
- **Method:** GET
- **Returns:** Job Posting details and associated skill sets

### Update Job Posting

- **Endpoint:** `/job-postings/{job_posting_id}`
- **Method:** PUT
- **Parameters:**
  - Same as create
- **Updates specified fields in the Job Posting**

### Delete Job Posting

- **Endpoint:** `/job-postings/{job_posting_id}`
- **Method:** DELETE
- **Deletes the Job Posting and associated skill sets**

## Application Management

### Submit Application

- **Endpoint:** `/applications`
- **Method:** POST
- **Parameters:**
  - Job Posting ID (String)
  - Job Seeker ID (String)
- **Creates a new application**

### List Applications

- **Endpoint:** `/applications`
- **Method:** GET
- **Returns:** List of applications with Job Posting and Job Seeker details

### Read Application

- **Endpoint:** `/applications/{application_id}`
- **Method:** GET
- **Returns:** Application details with Job Posting and Job Seeker details

### Update Application Status

- **Endpoint:** `/applications/{application_id}`
- **Method:** PUT
- **Parameters:**
  - New Status (Dropdown: Pending, Reviewed, Accepted, Rejected)
- **Updates the status of the application**

### Delete Application

- **Endpoint:** `/applications/{application_id}`
- **Method:** DELETE
- **Deletes the application**

## Skill Set Management

### Associate Skill Set with Job Posting

- **Endpoint:** `/skill-sets`
- **Method:** POST
- **Parameters:**
  - Job Posting ID (String)
  - Skill (Text)
- **Associates a skill set with a job posting**

### List All Skill Sets

- **Endpoint:** `/skill-sets`
- **Method:** GET
- **Returns:** List of all skill sets

### Read Skill Set

- **Endpoint:** `/skill-sets/{skill_set_id}`
- **Method:** GET
- **Returns:** Skill set details

### Update Skill Set

- **Endpoint:** `/skill-sets/{skill_set_id}`
- **Method:** PUT
- **Parameters:**
  - Same as associate
- **Updates the specified skill set**

### Disassociate Skill Set from Job Posting

- **Endpoint:** `/skill-sets/{skill_set_id}`
- **Method:** DELETE
- **Disassociates the skill set from the job posting**

## Hiring Manager Management

### Create Hiring Manager Profile

- **Endpoint:** `/hiring-managers`
- **Method:** POST
- **Parameters:**
  - Name (Text)
  - Email (Text)
  - Add other fields as needed

### Read Hiring Manager Profile

- **Endpoint:** `/hiring-managers/{hiring_manager_id}`
- **Method:** GET
- **Returns:** Hiring Manager profile details

### Update Hiring Manager Profile

- **Endpoint:** `/hiring-managers/{hiring_manager_id}`
- **Method:** PUT
- **Parameters:**
  - Same as create
- **Updates specified fields in the Hiring Manager profile**

### Delete Hiring Manager Profile

- **Endpoint:** `/hiring-managers/{hiring_manager_id}`
- **Method:** DELETE
- **Deletes the Hiring Manager profile**

### List All Hiring Managers

- **Endpoint:** `/hiring-managers`
- **Method:** GET
- **Returns:** List of all hiring managers
