from flask import redirect
from flask import Flask, render_template, request, url_for
from flask import request
import json
import mysql.connector


application = Flask(__name__)

def getMysqlConnection():
    return mysql.connector.connect(user='root',host='localhost',port=3306,password ='',database='kuliah')

@application.route('/')
@application.route('/index')
def index(): 
    return render_template('portofolio.html')

@application.route('/login')
def login():
    return render_template('login.html')

@application.route('/dashboard')
def dashboard(): 
    return render_template('dashboard.html')

@application.route('/index2')
def index2():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from kelas"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
       db.close()
    return render_template('index2.html',kalimat=output_json)

@application.route('/course')
def course():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from mata_kuliah"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
       db.close()
    return render_template('course.html',kalimat=output_json)


@application.route('/profile')
def profile(): 
    return render_template('users-profile.html')

@application.route('/insert')
def insert():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from task"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
       db.close()
    return render_template('insert.html',kalimat=output_json)


@application.route('/task', methods=['GET','POST'])
def task():
    print(request.method)
    if request.method == 'GET':
        return render_template('insert.html')
    else: 
        request.method == 'POST'
        id_matkul = request.form['id_matkul']
        matakuliah = request.form['matakuliah']
        rincian_tugas = request.form['rinciantugas']   
        jenis_tugas = request.form['jenistugas']
        deadline = request.form['deadline']
        pengumpulan = request.form['pengumpulan']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "Data Berhasil Ditambahkan"
            sqlstr = "INSERT INTO `task` (`id_matkul`, `matakuliah`, `rincian_tugas`, `jenis_tugas`, `deadline`, `pengumpulan`) VALUES ('"+id_matkul+"','"+matakuliah+"','"+rincian_tugas+"','"+jenis_tugas+"','"+deadline+"','"+pengumpulan+"')"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print('Error in SQL:\n', e)
        finally:
            db.close()
            return redirect(url_for('insert')) 

@application.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    if request.method == 'GET':
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            cur.execute ("SELECT * FROM task where id_matkul=%s", (id,))
            output = cur.fetchall()
            print(output)
            db.commit()
            cur.close()
            
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return render_template('edit.html', kalimat=output)
    elif request.method == 'POST':
        id_matkul = request.form['id_matkul']
        matakuliah = request.form['matakuliah']
        rincian_tugas = request.form['rinciantugas']   
        jenis_tugas = request.form['jenistugas']
        deadline = request.form['deadline']
        pengumpulan = request.form['pengumpulan']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            cur.execute ("UPDATE `task` SET `id_matkul` = %s, `matakuliah` = %s, `rincian_tugas` = %s, `jenis_tugas` = %s, `deadline` = %s, `pengumpulan` = %s WHERE `task`.`id_matkul` = %s",(id_matkul,matakuliah,rincian_tugas,jenis_tugas,deadline,pengumpulan,id,))
            output = cur.fetchall()
            print(output)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('insert'))

    return render_template('insert.html')
    
     #Menghapus data
@application.route('/delete_Matkul/<int:id>', methods=['GET'])
def deleteMatkul(id):
    db = getMysqlConnection()
    if request.method == 'GET':
        cursor = db.cursor()
        cursor.execute("DELETE FROM task WHERE id_matkul=%s", (id, ))
        db.commit()
        cursor.close()

        return redirect(url_for('insert'))
    return render_template('insert.html')






if __name__ == '__main__':
    application.run(debug=True)