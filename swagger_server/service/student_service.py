import os
import tempfile
from functools import reduce

from tinydb import TinyDB, Query

# For GitHub Actions postman tests in the assignment it was not working with MongoDB, which is why it had to be done with TinyDB:
# At the bottom of this file was my old solution with MongoDB, which was working locally
db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


def add(student=None):
    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    print(student)
    return student


def delete(student_id=None):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return 'not found', 404
    student_db.remove(doc_ids=[int(student_id)])
    return student_id

# Old solution with MongoDB which was working locally, but not with postman tests in GitHub Actions:
# import os
# from functools import reduce
# from pymongo import MongoClient

# # Initialize MongoDB client
# mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
# client = MongoClient(mongo_uri)
# db = client['student_db']
# student_collection = db['students']

# def add(student=None):
#     query = {
#         "first_name": student.first_name,
#         "last_name": student.last_name
#     }
#     res = student_collection.find_one(query)
#     if res:
#         return 'already exists', 409

#     result = student_collection.insert_one(student.to_dict())
#     student.student_id = str(result.inserted_id)
#     return student.student_id

# def get_by_id(student_id=None, subject=None):
#     student = student_collection.find_one({"_id": student_id})
#     if not student:
#         return 'not found', 404
#     student['student_id'] = student_id
#     print(student)
#     return student

# def delete(student_id=None):
#     result = student_collection.delete_one({"_id": student_id})
#     if result.deleted_count == 0:
#         return 'not found', 404
#     return student_id