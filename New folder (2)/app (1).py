from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tempo.db'
db = SQLAlchemy(app)


meta= db.MetaData()


data = db.Table(
   'College', meta, 
   db.Column('USN', db.String, primary_key = True), 
   db.Column('student_name', db.String),
   db.Column('Gender', db.String),
   db.Column('Entry_type', db.String),
   db.Column('YOA', db.Integer),
   db.Column('migrated', db.Boolean),
   db.Column('Details_of_migration', db.String),
   db.Column('admission_in_separate_division',db.Boolean),
   db.Column('adDetails', db.String),
   db.Column('YOP', db.Integer),
   db.Column('degree_type', db.String),
   db.Column('pu_marks', db.Integer),
   db.Column('entrance_marks', db.Integer),
)
meta.create_all(db.engine)

def create(body):
    conn = db.engine
    sUSN = str(body['USN'])
    sName = str(body['student_name'])
    sGender = str(body['Gender'])
    sEntry_type = str(body['Entry_type'])
    sYearOfAdmission = int(body['YOA'])
    sMigrated = int(body['migrated'])
    sDetails = str(body['Details_of_migration'])
    sadmissionInSepDiv = int(body['admission_in_separate_division'])
    admissionDetails = str(body['adDetails'])
    sYop = int(body['YOP'])
    sDegreeType = str(body['degree_type'])
    sPuMarks = int(body['pu_marks'])
    sEntranceExams = str(body['entrance_marks'])
    entry = db.engine.execute(data.insert(),[
            {'USN' : sUSN, 'student_name' : sName, 'Gender' : sGender, 'Entry_type': sEntry_type,'YOA': sYearOfAdmission, 'migrated': sMigrated,
             'Details_of_migration': sDetails, 'admission_in_separate_division': sadmissionInSepDiv,'adDetails': admissionDetails ,'YOP': sYop, 'degree_type': sDegreeType,
             'pu_marks': sPuMarks, 'entrance_marks': sEntranceExams}
        ])
    result = db.engine.execute('SELECT * FROM College WHERE USN = :val', {'val' : sUSN})               #:val mathod protects ours code from SQL Injection attacks
    db.session.commit()
    for r in result:
        r_dict = dict(r.items())
        print(r_dict)
        if r_dict['USN'] == sUSN:
            return "Added successfully" 
        else: 
            return "Not Saved"
    

def read():
    dataview = data.select()
    result = db.engine.execute(dataview)
    row_list = [] 
    for row in result.fetchall():
        row_list.append(dict(row))
    return jsonify(row_list)


def update(body):
    dict_input = dict(body)
    match = dict_input['USN']
    for key, value in dict_input.items():
        updated = data.update().where(data.c.USN==match).values({key:value})
        result = db.engine.execute.execute(updated)
    return "Updated Successfully"    

def delete(body):
    option = body['USN']
    deleted = data.delete().where(data.c.USN == option)
    result = db.engine.execute(deleted)
    return "Deleted"


@app.route('/newEntries', methods = ['POST'])
def assignment():
    body = request.get_json()
    output = create(body)
    return output


@app.route('/readEntries', methods = ['GET'])
def readingAssignment():
    output = read()
    return output


@app.route('/updateEntries', methods = ['PUT'])
def updatingAssignment():
    body = request.get_json()
    output = update(body)
    return output    

@app.route('/deleteEntries', methods = ['DELETE'])
def deletingAssignment():
    body = request.get_json()
    output = delete(body)
    return output    

if __name__ == '__main__':
    app.run(debug= True, port= 5000)
    