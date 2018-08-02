import pymysql
from prettytable import PrettyTable
import datetime

conn= pymysql.connect("localhost","root","1234","pharmacy")
curs=conn.cursor()

class user:   #completed
    def __init__(self):
        uid=None

    def signup(self,cust_details): #DONE
        print(cust_details)
        curs.execute("""INSERT INTO customer (cname,phone,email,address,password) VALUES(%s,%s,%s,%s,%s)""",(cust_details['Name'], cust_details['Phone'], cust_details['Email'], cust_details['Address'], cust_details['Password']))
        conn.commit()
        print("Signup Successful!")

    def signin(self,uname,password): #DONE
        try:
            curs.execute("""SELECT password from pharmacy.customer WHERE email=%s""", (uname))
            passw=curs.fetchall()
            if password==passw[0][0]:
                return True
            else:
                return False
        except Exception as e:
            print("Wrong Details!")
            return False


class customer(user):
    def __init__(self):
        self.cust_details={}


    def placeOrder(self,cid):
        curs.execute("SELECT CONNECTION_ID()")
        conid=curs.fetchall()
        curs.execute("SELECT mid,mname,qty,price FROM pharmacy.medicine")
        rows=curs.fetchall()
        x = PrettyTable(["MedicineID", "Name", "Quantity", "Price"])
        for row in rows:
            x.add_row(row)
        print(x)

        total_cost=0
        wm=True
        while wm!=False:
            medId=int(input("Enter MedicineID of medicine you want to purchase:"))
            quan=int(input("Enter Quantity:"))
            curs.execute("SELECT qty from medicine where mid=%s",medId)
            q=curs.fetchall()
            qold=q[0][0]
            qnew=qold-quan
            curs.execute("UPDATE medicine SET qty=%s WHERE mid=%s",(qnew,medId))
            curs.execute("select price from medicine where mid=%s",medId)
            price=curs.fetchall()
            total_cost=total_cost+quan*price[0][0]
            curs.execute("Insert into orders values(%s,%s,%s,%s,%s)",(conid[0][0],cid,medId,'pending',datetime.datetime.now(),qty))
            conn.commit()
            wmc=input("Want more medicine(Y/N):")
            if wmc=='Y' or wmc=='y':
                wm=True
            else:
                wm=False
        print("Your Total Order Cost is:",total_cost)

    def previousOrder(self):
        pass

    def updateProfile(self, cid):  # DONE    #added uname for condition
        name = input("Enter your Name:")
        password = input("Enter password:")
        phone = input("Enter phone number:")
        email = input("Enter email address:")
        address = input("Enter address:")
        curs.execute(""" UPDATE pharmacy.customer set cname=%s, password=%s, phone=%s, email=%s, address=%s WHERE cid=%s""",
        (name, password, phone, email, address, cid))
        print(curs.rowcount,"record updated successfully!")
        conn.commit()

    def getDiscount(self,totalcost,cid):
        curs.execute(""" SELECT COUNT(*) from (SELECT cid,oid, count(*) AS count FROM pharmacy.orders GROUP BY oid, cid) as t WHERE cid=%s""",cid)
        d=curs.fetchall()
        if(d>=5):
            return 5
        else if(d>=10):
            return 10
        else:
            return 0
    def fetchDetails(self,name,password,phone,email,address): # DONE
        self.cust_details['Name'] = name
        self.cust_details['Password'] = password
        self.cust_details['Phone'] = phone
        self.cust_details['Email'] = email
        self.cust_details['Address'] = address
        print(self.cust_details)
        super().signup(self.cust_details)




#Program Menu
print("1.Press 1 for Customer")
print("2.Press 2 for Admin")
choice1 = int(input("Enter Choice:"))
if choice1 == 1:
    print("1.Press 1 for Signup")
    print("2.Press 2 for signin")
    choice2 = int(input("Enter choice:"))
    if choice2 == 1:
        name = input("Enter your Name:")
        password = input("Enter password:")
        phone = input("Enter phone number:")
        email = input("Enter email address:")
        address = input("Enter address:")
        obj = customer()
        obj.fetchDetails(name, password, phone, email, address)
    elif choice2 == 2:
        tf = False
        while tf != True:
            uname = input("Enter Username(Email):")
            password = input("Enter Password:")
            obj = customer()
            tf = obj.signin(uname, password)
            if tf == True:
                print("Login Successful!")
                curs.execute(""" SELECT cid,cname, address, phone, email from pharmacy.customer WHERE email=%s""",
                             (uname,))
                r = curs.fetchall()
                cid = r[0][0]
                print("WELCOME " + r[0][1] + "!")

                tg = False
                while tg != True:
                    print("1.Press 1 to view profile details.")
                    print("2.Press 2 to update profile details.")
                    print("3.Press 3 to order new items.")
                    print("4.Press 4 to see previous orders.")
                    print("5.Press 5 to log Out.")
                    choice3 = int(input("Enter choice:"))
                    if choice3 == 1:
                        print("Customer Name:", r[0][1])
                        print("Customer ID:", r[0][0])
                        print("Customer address:", r[0][2])
                        print("Customer Email:", r[0][4])
                        print("Customer phone:", r[0][3])
                    elif choice3 == 2:
                        obj.updateProfile(cid)
                    elif choice3 == 3:
                        obj.placeOrder(cid)
                    elif choice3 == 4:
                        pass
                    elif choice3 == 5:
                        tg = True
            else:
                print("Login Unsuccessful!")
curs.close()
conn.close()
