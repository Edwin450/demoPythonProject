from src import db

class Project(db.Model):
    __tablename__= 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Project {self.name}>'
