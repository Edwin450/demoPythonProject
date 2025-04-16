from flask import Blueprint # type: ignore
from src.controllers.auth_controllers.project_controller import *

project_bp = Blueprint('todos',__name__, url_prefix='/todos')

@project_bp.route('/projectList', methods=['GET'])
def get_todos():
    return get_project_controller()

@project_bp.route('/addProject', methods=['POST'])
def add_student():
    return add_project_controller()

@project_bp.route('/updateProject/<int:id>', methods=['PUT'])
def update_student(id):
    return update_project_controller(id)

@project_bp.route('/deleteProject/<int:id>', methods=['DELETE'])
def delete_student(id):
    return delete_student_controller(id)


