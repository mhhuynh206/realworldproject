#Sources:
#https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
#https://github.com/ellisju37073/States (Used as template) 
#https://stackoverflow.com/questions/902408/how-to-use-variables-in-sql-statement-in-python
#Worked with Eric Y., and Matthew W.
#Received help also from Eric

from mysql import connector
from flask import Flask, redirect, url_for, request, render_template
import mysql.connector
app = Flask(__name__, static_url_path='')

conn = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='zipcodes',
                               buffered = True)
cursor = conn.cursor()


@app.route('/searchZIP/<searchzip>')
def searchzip(searchzip):

    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [searchzip])
    test = cursor.rowcount
    if test != 1:
        return searchzip + " was not found"
    else:
        searched = cursor.fetchall()
        return 'Success! Here you go: %s' % searched


@app.route('/updatezippop/<updateZIP> <updatePOP>')
def updatezippop(updateZIP, updatePOP):
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [updateZIP])
    test = cursor.rowcount
    if test != 1:
        return updateZIP + " was not found"
    else:
        cursor.execute("UPDATE `zipcodes` SET Population = %s WHERE zip= %s;", [updatePOP,updateZIP])
        cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s and Population=%s", [updateZIP,updatePOP])
        test1 = cursor.rowcount
        if test1 != 1:
            return updateZIP + "  failed to update"
        else:
            return 'Population has been updated successfully for zip: %s' % updateZIP


@app.route('/update',methods = ['POST'])
def update():
       user = request.form['uzip']
       user2 = request.form['upop']
       return redirect(url_for('updatezippop', updateZIP=user, updatePOP=user2))


@app.route('/search', methods=['GET'])
def search():
       user = request.args.get('szip')
       return redirect(url_for('searchzip', searchzip=user))



@app.route('/')
def root():
   return render_template('login.html')


if __name__ == '__main__':
   app.run(debug = True)
