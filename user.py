import mysql.connector

conn= mysql.connector.connect(user='root', password='1234', database='pharmacy')
curs=conn.cursor()

class user:
    def __init__(self):
        uid=None

    def signup(self,cust_details): #DONE
        print(cust_details)
        curs.execute("""INSERT INTO customer (cname,phone,email,address,password) VALUES(%s,%s,%s,%s,%s)""",(cust_details['Name'], cust_details['Phone'], cust_details['Email'], cust_details['Address'], cust_details['Password']))
        conn.commit()
        print("Signup Successful!")

    def signin(self,uname,password): #DONE
        try:
            curs.execute("""SELECT password from pharmacy.customer WHERE email=%s""", (uname,))
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


    def placeOrder(self):
        pass

    def previousOrder(self):
        pass

    def updateProfile(self, cid): #DONE    #added uname for condition
        name = input("Enter your Name:")
        password = input("Enter password:")
        phone = input("Enter phone number:")
        email = input("Enter email address:")
        address = input("Enter address:")
        curs.execute(""" UPDATE pharmacy set cname=%s, phone=%s, email=%s, address=%s WHERE cid=%s""",(name,phone,email,address,cid))
        pass

    def getDiscount(self):
        pass

    def fetchDetails(self,name,password,phone,email,address):
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
choice1=int(input("Enter Choice:"))
if choice1==1:
    print("1.Press 1 for Signup")
    print("2.Press 2 for signin")
    choice2=int(input("Enter choice:"))
    if choice2==1:
        name = input("Enter your Name:")
        password = input("Enter password:")
        phone = input("Enter phone number:")
        email = input("Enter email address:")
        address = input("Enter address:")
        obj = customer()
        obj.fetchDetails(name,password,phone,email,address)
    elif choice2==2:
        tf=False
        while tf!=True:
            uname=input("Enter Username(Email):")
            password=input("Enter Password:")
            obj=customer()
            tf=obj.signin(uname,password)
            if tf==True:
                print("Login Successful!")
                curs.execute(""" SELECT cid,cname from pharmacy.customer WHERE email=%s""",(uname,))
                r=curs.fetchall()
                
                print("WELCOME "+r[0][1]+"!")
            else:
                print("Login Unsuccessful!")

#COMPLETED TILL SIGNIN SIGNUP
