import os
from functools import reduce
from pymongo import MongoClient

# Initialize MongoDB client
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(mongo_uri)
db = client['student_db']
student_collection = db['students']

def add(student=None):
    query = {
        "first_name": student.first_name,
        "last_name": student.last_name
    }
    res = student_collection.find_one(query)
    if res:
        return 'already exists', 409

    result = student_collection.insert_one(student.to_dict())
    student.student_id = str(result.inserted_id)
    return student.student_id

def get_by_id(student_id=None, subject=None):
    student = student_collection.find_one({"_id": student_id})
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    print(student)
    return student

def delete(student_id=None):
    result = student_collection.delete_one({"_id": student_id})
    if result.deleted_count == 0:
        return 'not found', 404
    return student_id