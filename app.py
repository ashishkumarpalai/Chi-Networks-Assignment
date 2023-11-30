import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from dotenv import load_dotenv
from bson.json_util import dumps
import pkg_resources

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Configure MongoDB connection
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

# Collection for job seekers
job_seekers = mongo.db.job_seekers

# Collection for job postings
job_postings = mongo.db.job_postings

# Collection for skill sets
skill_sets = mongo.db.skill_sets

# Collection for applications
applications = mongo.db.applications

# Assuming you have a collection for Hiring Managers
hiring_managers = mongo.db.hiring_managers

@app.route('/installed-packages')
def show_installed_packages():
    import pkg_resources

    # Get the working set of installed packages
    installed_packages = pkg_resources.working_set

    # Create a sorted list of strings representing each installed package and its version
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])

    # Create a formatted HTML response
    response_html = "<h1>Installed Packages</h1><ul>"
    response_html += "".join(f"<li>{package}</li>" for package in installed_packages_list)
    response_html += "</ul>"

    return response_html

@app.route('/')
def default_routes():
    return '<h1 style="color:blue;text-align:center">Welcome to Intelligent Job Matching System!</h1>'


# List all Job Seekers
@app.route('/job-seekers', methods=['GET'])
def list_job_seekers():
    # Retrieve all dishes from the MongoDB collection
    dishes = list(job_seekers.find())

    for dish in dishes:
        dish['_id'] = str(dish['_id'])
    # Return the dishes as JSON response
    return jsonify(dishes)

# Read Job Seeker Profile


@app.route('/job-seekers/<job_seeker_id>', methods=['GET'])
def read_job_seeker(job_seeker_id):
    job_seeker = job_seekers.find_one(
        {'_id': ObjectId(job_seeker_id)}, {'_id': False})
    if job_seeker:
        return jsonify(job_seeker)
    return jsonify({'message': 'Job Seeker not found'}), 404


# Create Job Seeker Profile
@app.route('/job-seekers', methods=['POST'])
def create_job_seeker():
    data = request.json
    new_job_seeker = {
        'name': data['name'],
        'status': data['status'],
        'skills': data['skills'],
        'experience': data['experience'],
        'bio': data['bio'],
        'availability': data['availability']
    }
    job_seeker_id = job_seekers.insert_one(new_job_seeker).inserted_id
    return jsonify(str(job_seeker_id)), 201


# Update Job Seeker Profile
@app.route('/job-seekers/<string:job_seeker_id>', methods=['PUT'])
def update_job_seeker(job_seeker_id):
    data = request.json
    updated_job_seeker = {
        'name': data['name'],
        'status': data['status'],
        'skills': data['skills'],
        'experience': data['experience'],
        'bio': data['bio'],
        'availability': data['availability']
    }
    job_seekers.update_one({'_id': ObjectId(job_seeker_id)}, {
                           '$set': updated_job_seeker})
    return jsonify({'message': 'Job Seeker updated successfully'})

# Delete Job Seeker Profile


@app.route('/job-seekers/<string:job_seeker_id>', methods=['DELETE'])
def delete_job_seeker(job_seeker_id):
    result = job_seekers.delete_one({'_id': ObjectId(job_seeker_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Job Seeker deleted successfully'})
    return jsonify({'message': 'Job Seeker not found'}), 404

# ==========================================================================================

# List all Job Postings

# List all Job Postings with Skills and Hiring Manager details
@app.route('/job-postings', methods=['GET'])
def list_job_postings_with_details():
    try:
        postings = list(job_postings.find())
        postings_list = []

        for posting in postings:
            posting['_id'] = str(posting['_id'])
            skills = [skill['skill'] for skill in skill_sets.find(
                {'job_posting_id': ObjectId(posting['_id'])})]
            posting['skills'] = skills

            # Fetch details about the hiring manager
            hiring_manager_id = posting.get('hiring_manager_id')
            hiring_manager = hiring_managers.find_one(
                {'_id': hiring_manager_id}, {'_id': False})
            posting['hiring_manager'] = hiring_manager

            postings_list.append(posting)

        return dumps(postings_list)

    except Exception as e:
        return jsonify({'message': f'Error listing job postings: {str(e)}'}), 500

# Read Job Posting
@app.route('/job-postings/<job_posting_id>', methods=['GET'])
def read_job_posting(job_posting_id):
    try:
        job_posting = job_postings.find_one(
            {'_id': ObjectId(job_posting_id)}, {'_id': False})

        if job_posting:
            skills = [skill['skill'] for skill in skill_sets.find(
                {'job_posting_id': ObjectId(job_posting_id)})]
            job_posting['skills'] = skills

            # Fetch details about the hiring manager
            hiring_manager_id = job_posting.get('hiring_manager_id')
            hiring_manager = hiring_managers.find_one(
                {'_id': hiring_manager_id}, {'_id': False})
            job_posting['hiring_manager'] = hiring_manager

            return dumps(job_posting)

        return jsonify({'message': 'Job Posting not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error reading job posting: {str(e)}'}), 500


# Create Job Posting


@app.route('/job-postings', methods=['POST'])
def create_job_posting():
    data = request.json
    new_job_posting = {
        'job_title': data['job_title'],
        'status': data['status'],
        'start_date': data['start_date'],
        'end_date': data['end_date'],
        'hiring_manager_id': ObjectId(data['hiring_manager_id'])
    }
    job_posting_id = job_postings.insert_one(new_job_posting).inserted_id

    if 'skills' in data:
        for skill in data['skills']:
            skill_sets.insert_one({
                'job_posting_id': job_posting_id,
                'skill': skill
            })

    return jsonify(str(job_posting_id)), 201


# Update Job Posting
@app.route('/job-postings/<string:job_posting_id>', methods=['PUT'])
def update_job_posting(job_posting_id):
    data = request.json
    updated_job_posting = {
        'job_title': data['job_title'],
        'status': data['status'],
        'start_date': data['start_date'],
        'end_date': data['end_date'],
        'hiring_manager_id': ObjectId(data['hiring_manager_id'])
    }
    job_postings.update_one({'_id': ObjectId(job_posting_id)}, {
                            '$set': updated_job_posting})

    if 'skills' in data:
        skill_sets.delete_many({'job_posting_id': ObjectId(job_posting_id)})
        for skill in data['skills']:
            skill_sets.insert_one({
                'job_posting_id': ObjectId(job_posting_id),
                'skill': skill
            })

    return jsonify({'message': 'Job Posting updated successfully'})


# Delete Job Posting
@app.route('/job-postings/<string:job_posting_id>', methods=['DELETE'])
def delete_job_posting(job_posting_id):
    result = job_postings.delete_one({'_id': ObjectId(job_posting_id)})

    skill_sets.delete_many({'job_posting_id': ObjectId(job_posting_id)})

    if result.deleted_count > 0:
        return jsonify({'message': 'Job Posting deleted successfully'})
    return jsonify({'message': 'Job Posting not found'}), 404


# =============================================================================Applications

# Submit Application
@app.route('/applications', methods=['POST'])
def submit_application():
    data = request.json
    new_application = {
        'job_posting_id': ObjectId(data['job_posting_id']),
        'job_seeker_id': ObjectId(data['job_seeker_id']),
        'status': 'Pending'  # Default status when submitting
        # Add other fields as needed
    }
    application_id = applications.insert_one(new_application).inserted_id
    return jsonify(str(application_id)), 201


# List all Applications with Job Posting and Job Seeker details
@app.route('/applications', methods=['GET'])
def list_applications():
    try:
        application_list = list(applications.find())

        if application_list:
            applications_details = []

            for application in application_list:
                # Fetch details about the job posting
                application['_id'] = str(application['_id'])
                id=application['_id']
                job_posting_id = application.get('job_posting_id')
                job_posting = job_postings.find_one(
                    {'_id': job_posting_id}, {'_id': False})

                if job_posting:
                    # Fetch details about the hiring manager
                    hiring_manager_id = job_posting.get('hiring_manager_id')
                    hiring_manager = hiring_managers.find_one(
                        {'_id': hiring_manager_id}, {'_id': False})
                    job_posting['hiring_manager'] = hiring_manager

                # Fetch details about the job seeker
                job_seeker_id = application.get('job_seeker_id')
                job_seeker = job_seekers.find_one(
                    {'_id': job_seeker_id}, {'_id': False})

                # Include job posting and job seeker details in the application
                application_details = {
                    '_id':id,
                    'job_posting': job_posting,
                    'job_seeker': job_seeker,
                    'status': application.get('status')
                }

                applications_details.append(application_details)

            # Use bson.json_util for serialization
            return dumps(applications_details)
        return jsonify({'message': 'No applications found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error listing applications: {str(e)}'}), 500


# Read Application# Read Application with Job Posting and Job Seeker details
@app.route('/applications/<string:application_id>', methods=['GET'])
def read_application(application_id):
    try:
        application = applications.find_one(
            {'_id': ObjectId(application_id)}, {'_id': False})

        if application:
            # Fetch details about the job posting
            job_posting_id = application.get('job_posting_id')
            job_posting = job_postings.find_one(
                {'_id': job_posting_id}, {'_id': False})

            if job_posting:
                # Fetch details about the hiring manager
                hiring_manager_id = job_posting.get('hiring_manager_id')
                hiring_manager = hiring_managers.find_one(
                    {'_id': hiring_manager_id}, {'_id': False})
                job_posting['hiring_manager'] = hiring_manager

            # Fetch details about the job seeker
            job_seeker_id = application.get('job_seeker_id')
            job_seeker = job_seekers.find_one(
                {'_id': job_seeker_id}, {'_id': False})

            # Include job posting and job seeker details in the application
            application_details = {
                'job_posting': job_posting,
                'job_seeker': job_seeker,
                'status': application.get('status')
            }

            # Use bson.json_util for serialization
            return dumps(application_details)
        return jsonify({'message': 'Application not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error reading application: {str(e)}'}), 500


# Update Application Status

@app.route('/applications/<string:application_id>', methods=['PUT'])
def update_application_status(application_id):
    data = request.json
    new_status = data.get('status')
    if new_status and new_status in ['Pending', 'Reviewed', 'Accepted', 'Rejected']:
        applications.update_one({'_id': ObjectId(application_id)}, {
                                '$set': {'status': new_status}})
        return jsonify({'message': 'Application status updated successfully'})
    return jsonify({'message': 'Invalid status provided'}), 400


# Delete Application
@app.route('/applications/<string:application_id>', methods=['DELETE'])
def delete_application(application_id):
    result = applications.delete_one({'_id': ObjectId(application_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Application deleted successfully'})
    return jsonify({'message': 'Application not found'}), 404


# =============================================================================skills 


# Associate Skill Set with Job Posting
@app.route('/skill-sets', methods=['POST'])
def associate_skill_set():
    data = request.json
    new_skill_set = {
        'job_posting_id': ObjectId(data['job_posting_id']),
        'skill': data['skill']
    }
    skill_set_id = skill_sets.insert_one(new_skill_set).inserted_id
    return jsonify(str(skill_set_id)), 201

# List all Skill Sets
@app.route('/skill-sets', methods=['GET'])
def list_all_skill_sets():
    try:
        all_skill_sets = skill_sets.find()
        skill_sets_list = []

        for skill_set in all_skill_sets:
            # Exclude '_id' field from the response
            skill_set['_id'] = str(skill_set['_id'])
            skill_sets_list.append(skill_set)

        # Use bson.json_util for serialization
        return dumps(skill_sets_list)
    except Exception as e:
        return jsonify({'message': f'Error listing skill sets: {str(e)}'}), 500
    
# Read Skill Set
@app.route('/skill-sets/<string:skill_set_id>', methods=['GET'])
def read_skill_set(skill_set_id):
    skill_set = skill_sets.find_one({'_id': ObjectId(skill_set_id)}, {'_id': False})
    if skill_set:
        return dumps(skill_set)
    return jsonify({'message': 'Skill Set not found'}), 404

# Update Skill Set
@app.route('/skill-sets/<string:skill_set_id>', methods=['PUT'])
def update_skill_set(skill_set_id):
    data = request.json
    updated_skill_set = {
        'job_posting_id': ObjectId(data['job_posting_id']),
        'skill': data['skill']
    }
    skill_sets.update_one({'_id': ObjectId(skill_set_id)}, {'$set': updated_skill_set})
    return jsonify({'message': 'Skill Set updated successfully'})

# Disassociate Skill Set from Job Posting
@app.route('/skill-sets/<string:skill_set_id>', methods=['DELETE'])
def disassociate_skill_set(skill_set_id):
    result = skill_sets.delete_one({'_id': ObjectId(skill_set_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Skill Set disassociated successfully'})
    return jsonify({'message': 'Skill Set not found'}), 404

# =================================highering manager

# Hiring Manager Management
# Create Hiring Manager Profile
@app.route('/hiring-managers', methods=['POST'])
def create_hiring_manager():
    data = request.json
    new_hiring_manager = {
        'name': data['name'],
        'email': data['email'],
        # Add other fields as needed
    }
    hiring_manager_id = hiring_managers.insert_one(new_hiring_manager).inserted_id
    return jsonify(str(hiring_manager_id)), 201

# Read Hiring Manager Profile
@app.route('/hiring-managers/<hiring_manager_id>', methods=['GET'])
def read_hiring_manager(hiring_manager_id):
    hiring_manager = hiring_managers.find_one({'_id': ObjectId(hiring_manager_id)}, {'_id': False})
    if hiring_manager:
        return jsonify(hiring_manager)
    return jsonify({'message': 'Hiring Manager not found'}), 404

# Update Hiring Manager Profile
@app.route('/hiring-managers/<string:hiring_manager_id>', methods=['PUT'])
def update_hiring_manager(hiring_manager_id):
    data = request.json
    updated_hiring_manager = {
        'name': data['name'],
        'email': data['email'],
        # Update other fields as needed
    }
    hiring_managers.update_one({'_id': ObjectId(hiring_manager_id)}, {'$set': updated_hiring_manager})
    return jsonify({'message': 'Hiring Manager updated successfully'})

# Delete Hiring Manager Profile
@app.route('/hiring-managers/<string:hiring_manager_id>', methods=['DELETE'])
def delete_hiring_manager(hiring_manager_id):
    result = hiring_managers.delete_one({'_id': ObjectId(hiring_manager_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Hiring Manager deleted successfully'})
    return jsonify({'message': 'Hiring Manager not found'}), 404

# List all Hiring Managers
@app.route('/hiring-managers', methods=['GET'])
def list_hiring_managers():
    all_hiring_managers = hiring_managers.find()
    hiring_managers_list = []
    for hiring_manager in all_hiring_managers:
        hiring_manager['_id'] = str(hiring_manager['_id'])
        hiring_managers_list.append(hiring_manager)
    return dumps(hiring_managers_list)


# if __name__ == '__main__':
#     app.run(debug=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)