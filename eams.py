import datetime, os.path, os, tkinter as tk, tkinter.filedialog,tkcalendar as tkc
from tkinter import messagebox

class EAMS: # short for Employees Attendance Management System

    '''creates the first window. the user is asked to choose a name for the object (company/departments) and click a button.
    the button calls the func 'click_install.'''
    def __init__(self):
        self.window_install=tk.Tk()
        self.window_install.geometry("1000x600")

        self.window_install.title(f'Employees Attendance Management System')

        self.label_install=tk.Label(self.window_install,text='what is the department/business name?').grid(row=1,column=0,sticky='W')

        self.textentry_install=tk.Entry(self.window_install,width=134,bg='white')
        self.textentry_install.grid(row=2,column=0,sticky='W')

        self.button_install=tk.Button(self.window_install,text='Enter', width=6,command=self.click_install).grid(row=2,column=2,sticky='E')

        self.window_install.mainloop() #move out of init. make a func just for the mainloop

    '''takes the name entered in the '__init__' window and checks if:
    1) it meets the restrictions- one word of letters or digits only.
    2) it already "exist"- the user is asked if he wishes to use it anyway. if so, the program re-creates the object by retrieving data from its passed use
    3) the object is "new"- the user is asked if he wishes to create it'''
    def click_install(self):

        while True: # the while loop along with break lines are used in order to let the user re-enter data if it raises ecxeptions.
            try:
                self.entered_text_install = self.textentry_install.get() #retrieves the user input in the install window
                self.name=str(self.entered_text_install).lower() #changes the input format to a lowercase string (to overcome case sensitivity)
                if self.name.isalnum()==False: #checks if 'name' doesn't includes only letters and digits and raises an error message if so.
                    raise SyntaxError
            except SyntaxError:
                responed ='the name can only include letters or digits,try again'
                self.message_error = messagebox.showinfo('Employees Attendance Management System', responed)
                break # the iteration breaks in order to let the user re-enter the name to the installation window
            else:
                if any([os.path.isfile(f'{self.name}_employees_details.csv'),os.path.isfile(f'{self.name}_attendance_log.csv')]):#checks if the object was created before in the same folder
                    responed='object already exist. would you like to open it?'
                    self.message_install = messagebox.askyesno('Employees Attendance Management System',responed)
                    if self.message_install:
                        with open(f'{self.name}_employees_details.csv', 'r') as emp_d:
                            self.employees_id_list = ([line.split(',')[2] for line in emp_d.readlines()[1:]]) # retrieves the ids from the existing object
                        self.main_menu()
                        # break #terminates the loop
                else:
                    responed= 'there is no matching object. would you like to create a new one?'
                    self.message_install = messagebox.askyesno('Employees Attendance Management System', responed)
                    if self.message_install == True:
                        with open(f'{self.name}_employees_details.csv','w') as emp_d:  # creates a new employees details file with the object name in it including the headlines
                            emp_d.write('first name,last name,id,phone number,birth date\n')

                        with open(f'{self.name}_attendance_log.csv', 'w') as att_l:  # creates a new employees details file with the object name in it including the headlines
                            att_l.write('first name,last name,id number,time,date\n')

                        self.employees_id_list = []  # creates an empty list that will contain all the ids in the system in the future
                        self.employees_dict = {}  # creates an empty dict. keys=employees ids, values=employee birthdate(datetime object)

                        self.main_menu()
                break

    '''creates the main menu window that contains buttons with all the manipulations that can be done on the object and the reports that can be generated'''
    def main_menu(self):
        self.window_install.destroy()
        self.window_mainmenu = tk.Tk() #creates the main menu window
        self.window_mainmenu.geometry("1000x600")

        self.window_mainmenu.title(f'Employees Attendance Management System - {self.name}')

        # add employees:
        self.button_add_employees_manually = tk.Button(self.window_mainmenu, text='Add employees manually', width=20,command=self.click_add_employees_manually).grid(row=4, column=0)
        self.button_add_employees_from_file = tk.Button(self.window_mainmenu, text='add employees from file', width=20,command=self.click_add_employees_from_file).grid(row=5,column=0)

        # delete employees:
        self.button_delete_employees_manually = tk.Button(self.window_mainmenu, text='Delete employees manually', width=20,command=self.click_delete_employees_manually).grid(row=6,column=0,pady=(10,0))
        self.button_delete_employees_from_file = tk.Button(self.window_mainmenu, text='Delete employees from file',width=20,command=self.click_delete_employees_from_file).grid(row=7,column=0)

        #mark attendance:
        self.button_mark_attendance = tk.Button(self.window_mainmenu, text='mark attendance', width=20,command=self.click_mark_attendance).grid(row=8, column=0,pady=(10,0))

        #generate employees details report:
        self.button_open_all_employees_data = tk.Button(self.window_mainmenu,text='all employees data report', width=20,command=self.click_all_employees_details_report).grid(row=9, column=0, pady=(10,0))

        # generate attendance reports:
        self.button_open_attendance_log = tk.Button(self.window_mainmenu,text='all attendance report', width=20,command=self.click_all_attendance_report).grid(row=10, column=0,pady=(10,0))
        self.button__attendance_report_per_employee = tk.Button(self.window_mainmenu, text='report by employee',width=20,command=self.click_attendance_report_per_employee).grid(row=11, column=0)
        self.button_attendance_report_per_month = tk.Button(self.window_mainmenu, text='monthly report', width=20,command=self.click_attendance_report_per_month).grid(row=12, column=0)
        self.button_late_attendance_report = tk.Button(self.window_mainmenu, text='late attendance report', width=20,command=self.click_late_attendance_report).grid(row=13,column=0)

        #choose new company\department:
        self.button_back_to_install = tk.Button(self.window_mainmenu, text='go back to start page\n(re-choose system name)', width=20,command=self.re_install).grid(row=50,column=0,pady=(10,0))

        self.window_mainmenu.mainloop()

    '''called by the main menu func 'Add employees manually' button.
    creates a window with text boxes where the user can enter the employees data and a button the calls the 'add_employees_manually_click_im_done' func'''
    def click_add_employees_manually(self):
        try:
            with open(f'{self.name}_employees_details.csv', 'a') as emp_d:
                pass
        except PermissionError:
            responed = 'File is running or unaccessible\nclose it and try again'
            self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)

        else:
            self.window_aem = tk.Tk()
            self.window_aem.geometry("1000x600")

            self.window_aem.title(f'Employees Attendance Management System - {self.name} - add employees manually')

            #first name label+entery text box
            self.label_aem_fn = tk.Label(self.window_aem, text='Enter the employees first name').grid(row=1,column=0,sticky='W')
            self.textentry_aem_fn = tk.Entry(self.window_aem, width=134,bg='white')
            self.textentry_aem_fn.grid(row=2, column=0, sticky='W')

            # last name label+entery text box
            self.label_aem_ln = tk.Label(self.window_aem, text='Enter the employees last name').grid(row=3,column=0,sticky='W')
            self.textentry_aem_ln = tk.Entry(self.window_aem, width=134,bg='white')
            self.textentry_aem_ln.grid(row=4, column=0, sticky='W')

            # id label+entery text box
            self.label_aem_id = tk.Label(self.window_aem, text='Enter the employees id number').grid(row=5,column=0,sticky='W')
            self.textentry_aem_id = tk.Entry(self.window_aem, width=134,bg='white')
            self.textentry_aem_id.grid(row=6, column=0, sticky='W')

            # phone number label+entery text box
            self.label_aem_ph = tk.Label(self.window_aem, text='Enter the employees phone number').grid(row=7,column=0,sticky='W')
            self.textentry_aem_ph = tk.Entry(self.window_aem, width=134,bg='white')  # why isn't it the same width as the textbox below?
            self.textentry_aem_ph.grid(row=8, column=0, sticky='W')

            # birthdate label+date entery box
            tk.Label(self.window_aem, text='Choose your Birthdate from the calender').grid(row=9, column=0, sticky='W')

            self.dateentry_aem_birthdate = tkc.DateEntry(self.window_aem, width=134,bg='white') #Date entry is a method of tkcalendar. it lets the user pick a date from  a calender object
            self.dateentry_aem_birthdate.grid(row=11, column=0, sticky="W")

            self.button_all_done = tk.Button(self.window_aem, text='all done', width=20,command=self.add_employees_manually_click_im_done).grid(row=20,column=0,sticky='W')
            self.window_aem.lift()

    '''called by the 'click_add_employees_manually' func 'all done' button.
    checks if the data inserted by the user meets the restrictions, its birthdate has passed and its id isn't already in the employees details file and the file is not open.
    if both terms are True- the employee is added to the employees details csv file, and the user is given an option to enter another employee'''
    def add_employees_manually_click_im_done(self): #birthdate version
        answers=[]
        while True: # the while loop along with break lines are used in order to let the user re-enter data if it raises ecxeptions.
            try:
                alpha_check=[str(self.textentry_aem_fn.get()).lower(),str(self.textentry_aem_ln.get()).lower()] #the input format is changed to lowercase string to overcome case sensitivity issues
                if all([input.isalpha() for input in alpha_check])==False: #checks if the first and last name str each contain only letters, if not an error message pops
                    raise TypeError
            except TypeError:
                responed= 'the first name and last name must contain letters only and consist of one word each'
                self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                self.window_aem.lift()
                break # iteration breaks in order to let the user re-enter the 'wrong' data
            else:
                answers.extend(alpha_check) #adds both variables to a list if both meet the restrictions

            try:
                nums_check = [self.textentry_aem_id.get(),self.textentry_aem_ph.get()]#last ch is a str of the birthdate (numbers only)
                if all([input.isdigit() for input in nums_check]) == False:#digits+positive
                    raise SyntaxError
            except SyntaxError:
                responed = 'the id and phone number must contain numbers only and can\'t be a negative'
                self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                self.window_aem.lift()
                break

            try:
                if str(self.textentry_aem_id.get()) in self.employees_id_list: #checks if the id is already in employees list
                    raise Exception
            except Exception:
                responed = 'The employee is already in the system\n(each id can only be entered once)'
                self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                self.window_aem.lift()
                break
            else:
                answers.extend(nums_check)  # adds both variables to a list if both meet the restrictions

                #date restrictions:
            try:
                birth_date_str= self.dateentry_aem_birthdate.get().replace('.','/')
                birth_date_dt = datetime.datetime.strptime(birth_date_str, '%d/%m/%Y').date()
                date_today=datetime.datetime.now().date()
                self.age=(date_today.year - birth_date_dt.year - ((date_today.month, date_today.day) < (birth_date_dt.month, birth_date_dt.day)))
                if self.age<0:#digits+positive
                    raise ValueError
            except ValueError:
                responed = 'according to the birthdate you entered you haven\'t been born yet'
                self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                self.window_aem.lift()
                break
            else:
                answers.append(birth_date_dt) #adds the variables to the list  with the first and last names if they all meet the restrictions

                break
        if len(answers)==5:
            with open(f'{self.name}_employees_details.csv', 'a') as emp_d:
                emp_d.write(f'{answers[0]},{answers[1]},{answers[2]},{answers[3]},{answers[4]}\n') #adds the user details to the employees details file
                self.employees_id_list.append(answers[2]) #adds the id to the id follow up list
                responed='The employee was added successfully\ndo you wish to enter another one?'
                self.message_success = messagebox.askyesno(f'Employees Attendance Management System-{self.name}', responed)
                self.window_aem.destroy()
                if self.message_success==True:
                    self.click_add_employees_manually() #resets the employee details entery window
                else:
                    self.window_mainmenu.lift() #puts the main menu window on top

    '''called by the main menu 'add employees from file' button.
    if the employees details file is not running, opens a 'select file' window and adds to the employees details file all the 'new' employees from the selected csv file ('new'=employees with ids that aren't already in the employees details file)'''
    def click_add_employees_from_file(self):
        while True: # the while loop along with break lines are used in order to let the user re-enter data if it raises ecxeptions, or enter a new url after a successful process.
            try:
                with open(f'{self.name}_employees_details.csv', 'a') as emp_d:
                    pass
            except PermissionError:
                responed = 'File is running or unaccessible\nclose it and try again'
                self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}',responed)
                break
            else:
                self.directory=tk.filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("csv", "*.csv"), ("all files", "*.*"))) #opens 'select file' window that presents csv files only, and prevents choosing wrong paths
                path = str(self.directory)
                if self.directory!='': #checks if a file was properly chosen in the select file window
                    with open(path, 'r') as user_path:
                        user_path_list=[line for line in user_path.readlines()[1:] if line.split(',')[2] not in self.employees_id_list] #creates a list of all the employees details lines in the path whose ids are not already in the system (line.split(',')[2] is the id in each line).
                    self.employees_id_list.extend([line.split(',')[2] for line in user_path_list]) #adds the new ids from the path to the id follow up list
                    with open(f'{self.name}_employees_details.csv', 'a') as emp_d:
                        emp_d.writelines(user_path_list) #new lines are appended to the employees details file
                    responed = 'The employees from the path were added successfully, would you like to choose another file?'
                    self.message_success = messagebox.askyesno(f'Employees Attendance Management System-{self.name}', responed)
                    if self.message_success == False:
                        self.window_mainmenu.lift()
                        break
                else:
                    break

    '''called by the main menu 'delete employees manually' button.
        creates a window that includes a text box where the user can enter the employees id and a button the calls the 'delete_employees_manually_click_Enter' func'''
    def click_delete_employees_manually(self):
        try:
            with open(f'{self.name}_employees_details.csv', 'a') as emp_d:
                pass
        except PermissionError:
            responed = 'File is running or unaccessible\nclose it and try again'
            self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)

        else:
            self.window_dem = tk.Tk()
            self.window_dem.geometry("1000x600")

            self.window_dem.title(f'Employees Attendance Management System - {self.name} - delete employees manually')

            self.label_dem_id = tk.Label(self.window_dem, text='Enter the employees id number').grid(row=5, column=0,sticky='W')
            self.textentry_dem_id = tk.Entry(self.window_dem, width=134,bg='white')
            self.textentry_dem_id.grid(row=6, column=0, sticky='W')

            self.button_Enter_id = tk.Button(self.window_dem, text='Enter', width=20,command=self.delete_employees_manually_click_Enter).grid(row=20, column=0,sticky='W')
            self.window_dem.lift()

    '''called by the 'click_add_employees_manually' func 'Enter' button.
    checks if the id inserted by the user meets the restrictions and is in the employees list and the employees detail file is not open
    if both terms are True- the employee is deleted from the employees details csv file, and the user is given an option to enter another id'''
    def delete_employees_manually_click_Enter(self):# the while loop along with break lines are used in order to let the user re-enter data if it raises ecxeptions
            while True:
                try:
                    id_input = str(self.textentry_dem_id.get())
                    if id_input.isdigit() == False:  # digits+positive
                        raise SyntaxError
                except SyntaxError:
                    responed = 'the id must contain numbers only and can\'t be a negative'
                    self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                    self.window_dem.lift()
                    break # iteration breaks in order to let the user re-enter the 'wrong' data

                try:
                    if id_input not in self.employees_id_list: #checks if the id is not in employees list
                        raise Exception
                except Exception:
                    responed = 'the employee is not in the system'
                    self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                    self.window_dem.lift()
                    break

                else:
                    with open(f'{self.name}_employees_details.csv', 'r') as emp_d:
                        emp_d_list=emp_d.readlines()
                        for line in emp_d_list[1:]:
                            if line.split(',')[2]== id_input:
                                emp_d_list.remove(line) #removes irrelevent lines from the employees details file
                                self.employees_id_list.remove(id_input) #removes irrelevent lines from the id follow up list
                                break
                    with open(f'{self.name}_employees_details.csv', 'w') as emp_d:
                        emp_d.writelines(emp_d_list)

                        responed = 'The employee was deleted successfully\ndo you wish to enter another one?'
                        self.message_success = messagebox.askyesno(f'Employees Attendance Management System-{self.name}', responed)
                        self.window_dem.destroy()
                        if self.message_success == True:
                            self.click_delete_employees_manually() #resets the employee manually delete window
                        else:
                            self.window_mainmenu.lift()
                        break

    '''called by the main menu 'delete employees from file' button.
    if the employees details file is not running, open a 'select file' window and deletes all the employees from the employees details file whose ids are also in the selected csv file'''
    def click_delete_employees_from_file(self):
        while True: # the while loop along with break lines are used in order to let the user re-enter data if it raises ecxeptions, or enter a new url after a successful process.
            try:
                with open(f'{self.name}_employees_details.csv', 'a') as emp_d:
                    pass
            except PermissionError:
                responed = 'File is running or unaccessible\nclose it and try again'
                self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}',responed)
                break
            else:
                self.directory=tk.filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("csv", "*.csv"), ("all files", "*.*"))) #opens 'select file' window that presents csv files only, and prevents choosing wrong paths
                path = str(self.directory)
                if self.directory != '':#checks if a file was properly chosen in the select file window
                    with open(path, 'r') as user_path:
                        user_path_list = [line for line in user_path.readlines()[1:] if line.split(',')[2] in self.employees_id_list] #creates a list of all the employees details lines in the path whose ids are in the system (line.split(',')[2] is the id in each line).
                        for line in user_path_list:
                            self.employees_id_list.remove(line.split(',')[2]) # removes the ids  that are also in the path from the id follow up list
                        with open(f'{self.name}_employees_details.csv', 'r') as emp_d:
                            emp_d_list= emp_d.readlines()
                            emp_d_new= [emp_d_list[0]]+[line for line in emp_d_list[1:] if line.split(',')[2] in self.employees_id_list] #creates a list of the headers(emp_d_list[0]) and the employees details line which ids are in the follow up list
                        with open(f'{self.name}_employees_details.csv', 'w') as emp_d:
                            emp_d.writelines(emp_d_new)
                    responed = 'The relevant employees from the path were deleted successfully, would you like to choose another file?'
                    self.message_success = messagebox.askyesno(f'Employees Attendance Management System-{self.name}', responed)
                    if self.message_success == False:
                        self.window_mainmenu.lift()
                        break
                else:
                    break

    '''called by the main menu 'go back to start page\n(re-choose system name)' button.
    closes the main menu window and let the user choose a new object'''
    def re_install(self):
        self.window_mainmenu.destroy() #terminates the main menu window
        EAMS() #creates a new object

    '''called by the main menu 'mark attendance' button.
    creates a new window where the user can insert an id and a button that calls the 'mark_attendance_click_Enter' func'''
    def click_mark_attendance(self):

        self.window_ma = tk.Tk()
        self.window_ma.geometry("1000x600")

        self.window_ma.title(f'Employees Attendance Management System - {self.name} - mark attendance')

        self.label_ma_id = tk.Label(self.window_ma, text='Enter the employees id number').grid(row=5, column=0,sticky='W')
        self.textentry_ma_id = tk.Entry(self.window_ma, width=134,bg='white')  # why isn't it the same width as the textbox below?
        self.textentry_ma_id.grid(row=6, column=0, sticky='W')

        self.button_Enter_id = tk.Button(self.window_ma, text='Enter', width=20,command=self.mark_attendance_click_Enter).grid(row=20, column=0,sticky='W')
        self.window_ma.lift()

    '''called by the 'click_mark_attendance' func 'Enter' button.
    checks if the id inserted by the user meets the restrictions and if it's in the employees details list.
    if it's not in the file- the user is asked if he would like to add it and the 'add employees manually' window appears.
    if the id exist in the file- an attendance line is added to the file including his name, id, current time and date'''
    def mark_attendance_click_Enter(self):
        while True: # the while loop along with break lines are used in order to let the user re-enter data if it raises ecxeptions, or enter another id after a successful process.
            try:
                id_input = str(self.textentry_ma_id.get())
                if id_input.isdigit() == False:  # digits+positive
                    raise SyntaxError
            except SyntaxError:
                responed = 'the id must contain numbers only and can\'t be a negative'
                self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                self.window_ma.lift()
                break

            try:
                if id_input not in self.employees_id_list:
                    raise Exception
            except Exception:
                responed = 'the employee is not in the system. do you want to add it?'
                self.message_error = messagebox.askyesno(f'Employees Attendance Management System-{self.name}', responed)
                if self.message_error==True:
                    self.click_add_employees_manually() #reopens the the add employees manually window
                else:
                    self.window_ma.lift()
                break

            else: #all 4 following lines are ment to create current date and time objects in a format that will make excel acknowledge them for their data type
                time_str = datetime.datetime.now().time().strftime('%H:%M:%S')
                time_dt = datetime.datetime.strptime(time_str, '%H:%M:%S').time()

                date_str = datetime.datetime.now().date().strftime('%Y-%m-%d')
                date_dt = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

                with open(f'{self.name}_employees_details.csv', 'r') as emp_d:
                    emp_d_list=emp_d.readlines()
                    for line in emp_d_list:
                        line_list=line.split(',')
                        if line_list[2]==id_input:#line_list[2]=the employees id
                            with open(f'{self.name}_attendance_log.csv', 'a') as att_l:
                                att_l.write(f'{line_list[0]} ,{line_list[1]},{id_input},{time_dt},{date_dt}\n') #line_list[0]=first name, line_list[1]=last name
                                break

                responed = 'The Employee attendance was registered successfully\ndo you wish to enter another one?'
                self.message_success = messagebox.askyesno(f'Employees Attendance Management System-{self.name}', responed)
                self.window_ma.destroy()
                if self.message_success == True:
                    self.click_mark_attendance() #lets the user enter another attendance by re opening the relevant window
                else:
                    self.window_mainmenu.lift()
                break

    '''called by the main menu 'all employees data report' button.
    opens a csv file containing the full employees data list+ their current age (which updates according to the date of the report generation).
    if the file is empty, asks the user if he wants to add files. answering yes calls the 'add_employees_menu' func'''
    def click_all_employees_details_report(self):
        while True:
            try:
                with open(f'{self.name}_employees_details.csv', 'a') as emp_d:
                    pass
                date_today = datetime.datetime.now().date()
                with open(f'{self.name}_employees_details_{date_today}.csv', 'a') as emp_d:
                    pass
            except PermissionError: #checks the file isn't running on the os.
                responed = 'File is running or unaccessible\nclose it and try again'
                self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed) #creates csv file with the current date in its name
                break

            else:
                if len(self.employees_id_list)==0:
                    responed = 'There are no employees in the system yet.\nWould you like to add some?'
                    self.message_error = messagebox.askyesno(f'Employees Attendance Management System-{self.name}', responed)
                    if self.message_error == True:
                        self.add_employees_menu()
                    else:
                        self.window_mainmenu.lift()
                else:
                    with open(f'{self.name}_employees_details.csv', 'r') as emp_d:
                        emp_d_list=emp_d.readlines()
                        emp_d_report=['first name,last name,id,phone number,birth date,age\n']#add age as column header to file
                        date_today = datetime.datetime.now().date()
                        for line in emp_d_list[1:]:
                            line_list=line.split(',')
                            line_list[4]=line_list[4].strip('\n') #remove \n from birthdate if it is still there (it wo'nt after the first run of the func)
                            birth_date_str=line_list[4]
                            birth_date_dt = datetime.datetime.strptime(birth_date_str, '%Y-%m-%d').date() #employees birth date
                            self.age = (date_today.year - birth_date_dt.year - ((date_today.month, date_today.day) < (birth_date_dt.month, birth_date_dt.day))) #calculates employees current age in years
                            line=','.join(line_list)
                            line+=f',{self.age}\n' #add the employee age to the line of details
                            emp_d_report.append(line)
                            with open(f'{self.name}_employees_details_{date_today}.csv', 'w') as emp_d:
                                emp_d.writelines(emp_d_report)

                    os.startfile(f'{self.name}_employees_details_{date_today}.csv') #opens the employees details file
                    responed = 'the report was generated successfully'
                    self.message_success = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                    self.window_mainmenu.lift()
                    break

    '''called by the 'click_all_employees_details_report' func.
    creates a window containing only the add employee buttons from the main menu. each calls the same func as the parallel button in the main menu window'''
    def add_employees_menu(self):
        self.window_add_employees_menu = tk.Tk()
        self.window_add_employees_menu.geometry("1000x600")

        self.window_add_employees_menu.title(f'Employees Attendance Management System - {self.name}')

        # add employees buttons:
        self.button_add_employees_manually = tk.Button(self.window_add_employees_menu, text='Add employees manually', width=20,command=self.click_add_employees_manually).grid(row=4, column=0)
        self.button_add_employees_from_file = tk.Button(self.window_add_employees_menu, text='add employees from file', width=20,command=self.click_add_employees_from_file).grid(row=5,column=0)

        self.window_add_employees_menu.mainloop()# presents window

    '''called by the main menu 'all attendance report' button.
    opens a csv file containing the full attendance log. if the attendance log is empty a message pops'''
    def click_all_attendance_report(self):
        with open(f'{self.name}_attendance_log.csv', 'r') as att_l:
            att_l_all = att_l.readlines()
        if len(att_l_all)==1: #checks if doesn't contain only the headers
            responed = 'No attendance were marked in the system yet.'
            self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
            self.window_mainmenu.lift()
        else:
            os.startfile(f'{self.name}_attendance_log.csv') #opens the attendance log
            responed = 'the report was generated successfully'
            self.message_success = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
            self.window_mainmenu.lift()

    '''called by the main menu 'report by employee' button.
    creates a window where the user can insert an id and a button that calls the 'attendance_report_per_employee_click_Enter' func'''
    def click_attendance_report_per_employee(self):
        with open(f'{self.name}_attendance_log.csv', 'r') as att_l:
            att_l_all = att_l.readlines()
        if len(att_l_all)==1: #checks if doesn't contain only the headers
            responed = 'No attendance were marked in the system yet.'
            self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
            self.window_mainmenu.lift()
        else: #creates a window where the user can insert the employees id number
            self.window_rpe = tk.Tk()
            self.window_rpe.geometry("1000x600")

            self.window_rpe.title(f'Employees Attendance Management System - {self.name} - report by employee')

            self.label_rpe_id = tk.Label(self.window_rpe, text='Enter the employees id number').grid(row=5, column=0,sticky='W')
            self.textentry_rpe_id = tk.Entry(self.window_rpe, width=134,bg='white')  # why isn't it the same width as the textbox below?
            self.textentry_rpe_id.grid(row=6, column=0, sticky='W')

            self.button_Enter_id = tk.Button(self.window_rpe, text='Enter', width=20,command=self.attendance_report_per_employee_click_Enter).grid(row=20, column=0,sticky='W')
            self.window_rpe.lift()

    '''calles by the click_attendance_report_per_employee func 'Enter' button.
    opens a csv file containing the attendance log of all the attendance that have been marked for this praticular employee.
    if the data inserted by the user doesn't meet the restrictions, there aren't any relevant cases or a file with the same name (the name indcludes the  selected id and current date) is already open a message pops'''
    def attendance_report_per_employee_click_Enter(self):  # returns a report of all the attendance of an employee
        while True:
            try:
                id_input = str(self.textentry_rpe_id.get())
                if id_input.isdigit() == False:  # digits+positive
                    raise SyntaxError
            except SyntaxError:
                responed = 'the id must contain numbers only and can\'t be a negative'
                self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                self.window_rpe.lift()
                break
            try:
                date_str_now = datetime.datetime.now().date().strftime('%Y-%m-%d')  # creates a str of current date in a format that meets windows file names restrictions (unlike '/')
                with open(f'{self.name}_employee_id_{id_input}_report_{date_str_now}.csv', 'w'):
                    pass
            except PermissionError:
                responed = 'File is running or unaccessible\nclose it and try again'
                self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}',responed)
                self.window_rpe.lift()
                break
            try:
                if id_input not in self.employees_id_list: #checks if the id entered is in the follow up id list
                    raise Exception
            except Exception:
                responed = 'the employee is not in the system. do you want to add it?'
                self.message_error = messagebox.askyesno(f'Employees Attendance Management System-{self.name}', responed)
                if self.message_error == True:
                    self.click_add_employees_manually() #lets the user enter the employee to the employee details file
                else:
                    self.window_rpe.lift()
                break

            else:
                with open(f'{self.name}_attendance_log.csv', 'r') as att_l:
                    att_l_all=att_l.readlines()

                emp_att_list=[line for line in att_l_all if line.split(',')[2]==id_input or att_l_all.index(line)==0] #creates a list including the attendabce log headers (att_l_all.index(line)==0) and all the line that contain the entered id (line.split(',')[2])
                # date_str_now=datetime.datetime.now().date().strftime('%Y-%m-%d') #creates a str of current date in a format that meets windows file names restrictions (unlike '/')
                with open(f'{self.name}_employee_id_{id_input}_report_{date_str_now}.csv', 'w') as emp_report:
                    emp_report.writelines(emp_att_list) #creates a new file incuding the employee id and current date (in order to prevent overwriting in the future)
                os.startfile(f'{self.name}_employee_id_{id_input}_report_{date_str_now}.csv') #opens the new file


                responed = 'The Employee report was generated successfully\ndo you wish to enter another one?'
                self.message_success = messagebox.askyesno(f'Employees Attendance Management System-{self.name}', responed)
                if self.message_success == True:
                    self.click_attendance_report_per_employee() #resets the id entery window
                else:
                    # self.window_rpe.destroy()
                    self.window_mainmenu.lift()
                break

    '''called by the main menu 'monthly report' button.
    opens a csv file containing the attendance log of all the attendance that have been marked since the beginning of the current month.
    if there were no such cases or a file with the same name (the name indcludes the current date) is already open a message pops'''
    def click_attendance_report_per_month(self):  # returns a report of all the attendance of all employees since the beginning of the month
        while True:
            try:
                date_str_now = datetime.datetime.now().date().strftime('%Y-%m-%d')  # creates a str of current date in a format that meets windows file names restrictions (unlike '/')
                with open(f'{self.name}_last month_report_{date_str_now}.csv', 'w'):
                    pass
            except PermissionError:
                responed = 'File is running or unaccessible\nclose it and try again'
                self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                break
            else:
                with open(f'{self.name}_attendance_log.csv', 'r') as att_l:
                    att_l_all = att_l.readlines()
                emp_att_list = [att_l_all[0]] #att_l_all[0] is the headers line
                str_month_now= str(datetime.datetime.now().month)
                if len(str_month_now) == 1:
                    str_month_now = '0' + str_month_now #zeropades single digit month number string, in order to match the format in the file
                str_year_now= str(datetime.datetime.now().year)
                for line in att_l_all:
                    line_month_str=line.split(',')[-1][5:7] # line.split(',')[-1][5:7] is the month location in the attendance line
                    line_year_str = line.split(',')[-1][:4] # line.split(',')[-1][:4] is the year location in the attendance line
                    if line_month_str == str_month_now and line_year_str == str_year_now:
                        emp_att_list.append(line) #adds lines with the current month and year to the list

                if len(emp_att_list) == 1: #checks if any lines met the condition (equality to 1 means that it contains only the headers
                    responed = 'There were no attendance this last month'
                    self.message_success = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                    self.window_mainmenu.lift()
                else:
                    # date_str_now = datetime.datetime.now().date().strftime('%Y-%m-%d') #creates a str of current date in a format that meets windows file names restrictions (unlike '/')
                    with open(f'{self.name}_last month_report_{date_str_now}.csv', 'w') as emp_report:
                        emp_report.writelines(emp_att_list) #creates a new file incuding the current date (in order to prevent overwriting in the future)
                    os.startfile(f'{self.name}_last month_report_{date_str_now}.csv') #opens the new file
                    responed = 'The monthly report was generated successfully'
                    self.message_success = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                    self.window_mainmenu.lift()
            break

    '''called by the main menu 'late attendance report' button.
    opens a csv file containing the attendance log of all the attendance that have been marked after 9:30.
    if there were no such cases or a file with the same name (the name indcludes the current date) is already open a message pops'''
    def click_late_attendance_report(self):#returns a report of all the attendance of all employees since the beginning of the month
        while True:
            try:
                date_str_now = datetime.datetime.now().date().strftime('%Y-%m-%d')  # creates a str of current date in a format that meets windows file names restrictions (unlike '/')
                with open(f'{self.name}_late_employees_report_{date_str_now}.csv', 'w'):
                    pass
            except PermissionError:
                responed = 'File is running or unaccessible\nclose it and try again'
                self.message_error = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                break
            else:
                with open(f'{self.name}_attendance_log.csv', 'r') as att_l:
                    att_l_all = att_l.readlines()
                emp_att_list = [att_l_all[0]] #att_l_all[0] is the headers line
                due_time_hour=9
                due_time_minutes=30
                due_time=due_time_hour+(due_time_minutes/100) # make the due time a numeric fraction (9.3). this way it can be compared to the data from the line without converting it to a time object
                for line in att_l_all[1:]: #loops through all lines excluding the headers line (index 0)
                    attendance_hour=int(line.split(',')[-2][:2]) # line.split(',')[-2][:2] is the hour location in the attendance line
                    attendance_minutes = int(line.split(',')[-2][3:5]) # line.split(',')[-2][3:5] is the minutes location in the attendance line
                    attendance_time = attendance_hour + (attendance_minutes / 100)  # make the attendance time a fraction

                    if attendance_time>due_time:
                        emp_att_list.append(line) #add line only if the time in it is after 9:30
                if len(emp_att_list) == 1: #checks if any lines met the condition (equality to 1 means that it contains only the headers
                    responed = 'There were no late attendance'
                    self.message_success = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                    self.window_mainmenu.lift()

                else:
                    date_str_now = datetime.datetime.now().date().strftime('%Y-%m-%d') #creates a str of current date in a format that meets windows file names restrictions (unlike '/')
                    with open(f'{self.name}_late_employees_report_{date_str_now}.csv', 'w') as emp_report:
                        emp_report.writelines(emp_att_list) #creates a new file incuding the current date (in order to prevent overwriting in the future)
                    os.startfile(f'{self.name}_late_employees_report_{date_str_now}.csv') #opens the new file
                    responed = 'The late attendance report was generated successfully'
                    self.message_success = messagebox.showinfo(f'Employees Attendance Management System-{self.name}', responed)
                    self.window_mainmenu.lift()
            break



# -----------------------------------------------------------------------------------------------------------------------------------------------------

run=EAMS()
