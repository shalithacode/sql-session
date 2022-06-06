from flask import Flask, render_template,request,redirect
import mysql.connector
from mysql.connector.constants import ClientFlag

config = {
    'user': 'root',
    'password': 'toor',
    'host': '34.68.237.227',
    'database': 'my-db' ,
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}
app = Flask(__name__)

@app.route('/',methods =['GET','POST'])
def main():

    cnx = mysql.connector.connect(**config)
    if request.method == 'POST':
        
        query = (f'insert into country_tbl(name,currency,population,gdp) values("{request.form["name"]}","{request.form["currency"]}", "{request.form["population"]}","{request.form["gdp"]}");')
        with cnx.cursor() as cursor:
            cursor.execute(query)
        cnx.commit()
    
    result =[]
    with cnx.cursor() as cursor:
        cursor.execute('select * from country_tbl;')
        result = cursor.fetchall()
        print(len(result))
    cnx.close()

    return render_template('index.html', data = result)


@app.route('/delete',methods =['POST'])
def delete_country():

    cnx = mysql.connector.connect(**config)
    if request.method == 'POST':
        query = (f'DELETE FROM country_tbl WHERE c_id={request.form["custId"]};')
        print(query)
        with cnx.cursor() as cursor:
            cursor.execute(query)
        cnx.commit()
    cnx.close()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
