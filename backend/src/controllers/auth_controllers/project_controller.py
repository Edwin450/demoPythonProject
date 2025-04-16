from flask import request, jsonify
from src.models.auth_models.project_model import Project 
from src import db

# student List
def get_project_controller():
    project = Project.query.all()
    return jsonify([{
        'id': Project.id,
        'name': Project.name,
        'description': Project.description
    }for Project in project])

# new student
def add_project_controller():
    data = request.get_json()

    new_project = Project(
        name=data.get('name'),
        description=data.get('description')
    )

    db.session.add(new_project)
    db.session.commit()

    return jsonify({'message': 'Student added successfully'})

# update student
def update_project_controller(id):
    data = request.get_json()
    project = Project.query.get(id)

    if not project:
        return jsonify({'message': 'Student not found'}), 404

    project.name = data.get('name')
    project.description = data.get('description')

    db.session.commit()

    return jsonify({'message': 'Project updated successfully'})

# delete student
def delete_student_controller(id):
    project = Project.query.get(id)

    if not project:
        return jsonify({'message': 'Project not found'}), 404

    db.session.delete(project)
    db.session.commit()

    return jsonify({'message': 'Project deleted successfully'})

