from flask import Flask,render_template,url_for,request,redirect
from flask_mysqldb import MySQL
import math
app=Flask(__name__)
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="root"
app.config["MYSQL_DB"]="users"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

    
	
@app.route("/")
@app.route("/page/<int:page>")
def home(page=1):
    query="select count(*) from customers"
    con=mysql.connection.cursor()
    con.execute(query)
    row=con.fetchone()
    count=row["count(*)"]
    total_page=count//5+(1 if count%5 !=0 else 0)
    offset=(page-1)*5
    nq=f"select * from customers order by id limit 5 offset {offset}"
    con.execute(nq)
    res=con.fetchall()
    return render_template("home.html",data=res,page=page,total_page=total_page)
        
        
        
        

    
@app.route("/deleteuser/<string:id>",methods=["GET","POST"])
def deleteuser(id):
    con=mysql.connection.cursor()
    sql="delete from customers where id=%s;"
    con.execute(sql,[id,])
    mysql.connection.commit()
    con.close
    return redirect(url_for("home"))
@app.route("/addusers.html",methods=['GET','POST'])
def addusers():
    if request.method=='POST':
        name=request.form['name']
        Contact=request.form['Contact']
        Address=request.form['address']
        Amount=request.form['amount']
        con=mysql.connection.cursor()
        sql="insert into customers(Name,Contact,Address,Amount) values(%s,%s,%s,%s);"
        con.execute(sql,[name,Contact,Address,Amount])
        mysql.connection.commit()
        con.close
        return redirect(url_for("home"))
    return render_template("addusers.html")
@app.route("/delete",methods=["GET","POST"])
def delete():
    if request.method=="POST":
        id=request.form['id']
        con=mysql.connection.cursor()
        sql="delete from customers where id=%s;"
        con.execute(sql,[id,])
        mysql.connection.commit()
        con.close
    return redirect(url_for("home"))
    
        
    
@app.route("/edituser.html/<string:id>",methods=["GET","POST"])
def edituser(id):
    if request.method=="POST":
        con=mysql.connection.cursor()
        name=request.form['name']
        Contact=request.form['Contact']
        Address=request.form['address']
        Amount=request.form['amount']
        sql="update customers set Name=%s, Contact=%s, Address=%s, Amount=%s where id=%s;"
        con.execute(sql,[name,Contact,Address,Amount,id])
        mysql.connection.commit()
        con.close
        return redirect(url_for("home")) 
    sql="select*from customers where id=%s"
    con=mysql.connection.cursor()
    con.execute(sql,[id,])
    res=con.fetchone()
    return render_template("edituser.html",data=res)
    
    
    
        
if __name__=='__main__':
    app.run(debug=True)
