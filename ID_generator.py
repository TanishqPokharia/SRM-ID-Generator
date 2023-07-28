import customtkinter as ct
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import os
from twilio.rest import Client
from fpdf import FPDF
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import zipfile

ct.set_appearance_mode("light")
root=ct.CTk()
root.iconbitmap(r"TPicon.ico")

#classes
class PDF(FPDF):
    def header(self):
        self.image(r"download.png",60,8,80,30)


class response():
    def __init__(self,location,get,getx,gety):

        self.text=f"{get}:"
        self.label=ct.CTkLabel(location,text=self.text,font=('Courier bold',14))
        self.label.place(x=getx,y=gety)
        self.CTkEntry=ct.CTkEntry(location,width=300,border_color="light blue",border_width=3)
        self.CTkEntry.place(x=getx+150,y=gety)


class dropdown():
    def __init__(self,location,text,initial,d_list,getx,gety):
        self.ini=ct.StringVar(value=initial)
        self.text=text
        self.label=ct.CTkLabel(location,text=self.text,font=('Courier bold',14))
        self.label.place(x=getx,y=gety)
        self.CtkOptionMenu=ct.CTkOptionMenu(master=location,values=d_list,variable=self.ini,width=70)
        self.CtkOptionMenu.place(x=getx+150,y=gety)


#functions
source=""
def showimage():
    global source
    fln=filedialog.askopenfilename(initialdir=r"C:\Users\tppok\OneDrive\Desktop",title='Select Image file',filetypes=(("JPG file","*.jpg"),("JPEG file","*.jpeg"),("PNGfile","*.png"),("All files","*.*")))
    source+=fln
    img=Image.open(fln)
    re_img=img.resize((600,600),Image.ANTIALIAS)
    global final
    final=ImageTk.PhotoImage(re_img)
    image_label.configure(image=final)
    image_label.image=final


bf_x=50
def animation():
    global of_x
    global bf_x
    if bf_x!=1100:
        bf_x+=5
        box_frame.place(x=bf_x,y=230)
        box_frame.after(1,animation)


of_x=-900
def animation_otp():
    global of_x
    global bf_x
    if of_x!=50:
        of_x+=5
        otp_frame.place(x=of_x,y=230)
        otp_frame.after(1,animation_otp)


def increase():
    global progress
    if progress<1:
        progress+=0.01
        progressbar.set(progress)
        progressbar.after(50,increase)
        showprogres.configure(text=f"{int(progressbar.get()*100)}%")
        showprogres.place(x=540,y=300)
        if progressbar.get()==1:
            otp_frame.after(1000)
            showprogres.configure(text="")
            load.configure(text="  Done!!!!")
            ct.CTkLabel(otp_frame,text="ID Created!",font=('Courier bold',14)).place(x=420,y=400)
            otp_frame.after(2000,final_animation)


ff_x=-900
def final_animation():
    global ff_x
    global of_x
    if ff_x!=50:
        ff_x+=5
        of_x+=5
        otp_frame.place(x=of_x,y=230)
        final_frame.place(x=ff_x,y=230)
        final_frame.after(1,final_animation)

#create pdf object
pdf=PDF('P','mm','Letter')


def create_id():
    global first_name
    global last_name
    global DOB_date
    global DOB_month
    global DOB_year
    global regno
    global programme
    global contact
    global blood
    global srm_mail
    global address_one
    global address_two
    global pdf
    global source
    pdf.add_page()
    pdf.set_font('times','B',22)
    pdf.set_text_color(37,100,190)
    pdf.cell(29,80,"COLLEGE OF ENGINEERING AND TECHNOLOGY",ln=False,border=False)
    pdf.image(r"mus.png",x=0,y=60,w=pdf.w,h=180)
    pdf.image(r"blue.png",x=0,y=240,w=pdf.w)
    pdf.image(source,x=80,y=65,w=50,h=50)
    pdf.set_font('helvetica','B',16)
    pdf.set_text_color(0,0,0)
    pdf.cell(100,230,f"Name   :{first_name.CTkEntry.get()} {last_name.CTkEntry.get()}",ln=False,center=True)
    pdf.cell(180,260,f"DOB                        :{DOB_date.CtkOptionMenu.get()}-{DOB_month.CtkOptionMenu.get()}-{DOB_year.CtkOptionMenu.get()}",ln=False,center=True)
    pdf.cell(180,290,f"Register No.           :{regno.CTkEntry.get()}",ln=False,center=True)
    pdf.cell(180,320,f"Programme            :{programme.CtkOptionMenu.get()}",ln=False,center=True)
    pdf.cell(180,350,f"Contact                   :{contact.CTkEntry.get()}",ln=False,center=True)
    pdf.cell(180,380,f"Blood Grp.              :{blood.CtkOptionMenu.get()}",ln=False,center=True)
    pdf.cell(180,410,f"E-mail ID                 :{srm_mail.CTkEntry.get()}",ln=False,center=True)
    pdf.cell(180,440,f"Address                  :{address_one.CTkEntry.get()},{address_two.CTkEntry.get()}",ln=False,center=True)
    pdf.set_text_color(255,255,255)
    pdf.set_font('times','B',14)
    pdf.cell(60,470,"Kattankulathur Campus",ln=False,center=True)
    pdf.cell(90,480,"Chengalpattu Dt., Tamil Nadu-603203",ln=False,center=True)
    pdf.cell(45,490,"Ph:044-27417777",ln=False,center=True)
    pdf.cell(100,500,"Email:student.services.cet.ktr@srmist.edu.in",ln=False,center=True)
    pdf.cell(65,510,"Website:www.srmist.edu.in",ln=False,center=True)
    pdf.set_font('times','B',20)
    pdf.cell(66,530,"STUDENT - CARD",ln=False,center=True)


def send_otp():
    global contact
    account_sid = "AC08f8d5747cfb0f4453579571f6ea2add"
    auth_token = "41aa2cb7a14e8722e215d53418c77e00"
    verify_sid = "VAeaa3bec02363caacc11b7866c7bc1d21"
    verified_number = contact.CTkEntry.get()
    client = Client(account_sid, auth_token)
    verification = client.verify.v2.services(verify_sid) \
    .verifications \
    .create(to=verified_number, channel="sms")

def otp_verification():
    global contact
    account_sid = "AC08f8d5747cfb0f4453579571f6ea2add"
    auth_token = "41aa2cb7a14e8722e215d53418c77e00"
    verify_sid = "VAeaa3bec02363caacc11b7866c7bc1d21"
    verified_number = contact.CTkEntry.get()
    client = Client(account_sid, auth_token)
    global ask_otp

    verification_check = client.verify.v2.services(verify_sid) \
    .verification_checks \
    .create(to=verified_number, code=ask_otp.CTkEntry.get())
    if (verification_check):
        ct.CTkLabel(otp_frame,text="OTP verified!",font=('Courier bold',14)).place(x=700,y=100)
        progressbar.place(x=365,y=350)
        load.place(x=425,y=300)
        increase()
        create_id()
        download_button.place(x=380,y=100)
        send_to_email_button.place(x=380,y=150)
        ct.CTkButton(final_frame,text="Exit",command=root.quit).place(x=380,y=200)

    else:
        ct.CTkLabel(otp_frame,text="Wrong OTP! Try again",font=('Courier bold',14),fg_color="red").place(x=700,y=100)


def download():
    global pdf
    global first_name
    global last_name
    directory=filedialog.asksaveasfilename(initialdir=r"C:\Users\tppok\OneDrive\Desktop",initialfile=f"{first_name.CTkEntry.get()}_SRM_ID",title="Save ID",filetypes=[("PDF","*.pdf"),("All files","*.*")],defaultextension=".pdf")
    pdf.output(directory)


def sendmail():
    global pdf
    global first_name
    global srm_mail
    f_name=f"{first_name.CTkEntry.get()}_SRM_ID.pdf"
    pdf.output(f_name)
    with zipfile.ZipFile('ID.zip','w',compression=zipfile.ZIP_DEFLATED) as my_zip:
        my_zip.write(f_name)
    mail_id="tppokharia@gmail.com"
    mail_pass="lpcbwdouvkvcobvk"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(mail_id,mail_pass)
    message=MIMEMultipart()
    body_part = MIMEText("Hi! Here is your official SRM ID", 'plain')
    message['Subject']="SRM ID"
    message['From']=mail_id
    message['To']=srm_mail.CTkEntry.get()
    message.attach(body_part)
    with open("ID.zip",'rb') as PDF:
             message.attach(MIMEApplication(PDF.read(), Name='ID.zip'))
    server.sendmail(message['From'], message['To'], message.as_string())
    ct.CTkLabel(final_frame,text="ID has been sent to your email",font=("Courier bold",14)).place(x=370,y=250)


#main body
root.title("SRM ID generator -By Tanishq Pokharia")
root.resizable(0,0)
h=800
w=1000
x=(root.winfo_screenwidth()/2)-(w/2)
y=(root.winfo_screenheight()/2)-(h/2)
root.geometry(f"{w}x{h}+{int(x)*2}+{int(y)}")
background_frame=ct.CTkFrame(root,width=w,height=h,fg_color="#FFDB58",bg_color="#FFDB58")
background_frame.place(x=0,y=0)

#creating srm logo
im=Image.open(r"SRM.png")
resized_logo=im.resize((400,400),Image.ANTIALIAS)
logo=ImageTk.PhotoImage(resized_logo)
logo_label=Label(background_frame,image=logo)
logo_label.configure(bg="#FFDB58")
logo_label.place(x=800,y=15)

#creating the first frame
box_frame=ct.CTkFrame(root,width=900,height=540,fg_color="white",border_width=4,border_color="light blue")
box_frame.place(x=50,y=230)

#preparing our entry boxes and dropdown menus
first_name=response(box_frame,"First Name",50,50)
last_name=response(box_frame,"Last Name",50,100)
regno=response(box_frame,"Register Number",50,150)

month=["Jan","Feb","March","April","May","June","July","August","September","October","November","December"]
date=[str(i) for i in range(1,32)]
year=[str(i) for i in range(1990,2024)]
courses=["B.Tech CSE","B.Tech ECE","B.Tech EEE","B.Tech Biotech","B.Tech Mechanical","B.Tech Civil","B.Tech Chemical","B.Tech Aeronatical"]




DOB_date=dropdown(box_frame,"D.O.B:","1",date,50,200)
DOB_month=dropdown(box_frame,"","Jan",month,170,200)
DOB_year=dropdown(box_frame,"","2000",year,280,200)
blood_list=["O+","O-","A+","A-","B+","B-","AB+","AB-"]
blood=dropdown(box_frame,"Blood Group:","A+",blood_list,50,250)
contact=response(box_frame,"Contact Number",50,300)
programme=dropdown(box_frame,"Programme:","B.Tech EEE",courses,50,350)
srm_mail=response(box_frame,"SRM Mail_ID",50,400)
address_one=response(box_frame,"Address Line 1",50,450)
address_two=response(box_frame,"Address Line 2",50,500)

# creating the frame to display the chosen image
image_frame=ct.CTkFrame(box_frame,width=300,height=300,fg_color="white",border_width=5,border_color="light blue")
image_frame.place(x=550,y=50)

#upload photo button
upload=ct.CTkButton(box_frame,text="Upload your photo",command=showimage)
upload.place(x=630,y=400)

image_label=Label(image_frame)
image_label.place(x=0,y=0)

#proceed button
proceed_button=ct.CTkButton(box_frame,text="Proceed->",command=lambda:[animation(),animation_otp(),send_otp()])
proceed_button.place(x=631,y=500)


otp_frame=ct.CTkFrame(root,width=900,height=540,fg_color="white",border_width=4,border_color="light blue")
ask_otp=response(otp_frame,"Enter OTP to proceed",160,100)
label_otp=ct.CTkLabel(otp_frame,text="OTP sent to your mobile number ",font=('Courier bold',14))
label_otp.place(x=350,y=50)

verify_button=ct.CTkButton(otp_frame,text="Verify",command=otp_verification)
verify_button.place(x=390,y=200)

final_frame=ct.CTkFrame(root,width=900,height=540,fg_color="white",border_width=4,border_color="light blue")
download_button=ct.CTkButton(final_frame,text="Download ID",font=("Courier bold",14),command=download)
send_to_email_button=ct.CTkButton(final_frame,text="Send ID to my email",font=("Courier bold",14),command=sendmail)


progressbar=ct.CTkProgressBar(master=otp_frame,progress_color="green")
progressbar.set(0)
progress=0
showprogres = ct.CTkLabel(otp_frame,font=("Courier bold",14),text_color="green")
load=ct.CTkLabel(otp_frame,text="Processing...",font=("Courier bold",14))

#download and send to mail button
download_button.place(x=380,y=100)
send_to_email_button.place(x=380,y=150)

root.mainloop()
