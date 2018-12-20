import pandas as pd
import csv


# Read in orders from Eventbrite to get signup list of learners
eventbrite_report = input('Enter the name of the EventBrite event report.  ')

orders = pd.read_csv(eventbrite_report, index_col='Order #')

# print(orders[['First Name', 'Last Name', 'Email', 'Department or Center']])

# Read in list of learners who signed in on the etherpad ans thus attended the workshop
signin_file = input('Enter the filename of the etherpad sign-in.  ')

attendees = pd.read_csv(signin_file, delimiter='/', 
                        header=None, names=['name', 'department', 'twitter'])
# print(attendees)

# bring in names_tools for trying to deal with the name differences from the two lists
import name_tools as nt

# make sign-in list using nametool
attendees_list = []
for name in attendees.loc[:,'name']:
    attendees_list.append(nt.split(name))

# make dictionary from sign-in sheet where name is key and department is the value to pair
atnd_dict = {}
departments = []

for i in range(len(attendees_list)):
    atnd_dict.setdefault(attendees_list[i][1] + " " + attendees_list[i][2],[]).append((attendees.iloc[i]['department']).strip())
    departments.append((attendees.iloc[i]['department']).strip())
    
# print(atnd_dict)

# make eb orders list using nametool
orders_list = []
for i in range(len(orders)):
    orders_list.append(nt.split((nt.canonicalize(orders.iloc[i,1] + " " + orders.iloc[i,2]))))

# Make dictionary for orders that has names as keys and  has multiple return values of email and department
eb_dict = {}

for i in range(len(orders_list)):
#    print(orders_list[i][1] + " " + orders_list[i][2])
#    print(orders.iloc[i]['Department or Center'].title())
    eb_dict.setdefault(orders_list[i][1] + " " + orders_list[i][2],[]).append(orders.iloc[i]['Email'])
#    eb_dict.setdefault(orders_list[i][1] + " " + orders_list[i][2],[]).append((orders.iloc[i]['Department or Center']).title())
    eb_dict.setdefault(orders_list[i][1] + " " + orders_list[i][2],[]).append((orders.iloc[i]['Department or Center']))

# learner compare attendee list with orders list

final_list = []
for name_attend in attendees_list:
    found = False
    for name_order in orders_list:
        aname = (name_attend[1] + ' ' + name_attend[2])
        oname =(name_order[1] + ' ' + name_order[2])
        guess = nt.match(aname,oname)

        if guess > .90:
            print(aname, eb_dict[aname][0], eb_dict[aname][1])
            final_list.append([aname, eb_dict[aname][1], eb_dict[aname][0]])
            found = True
    if not found:
        print(aname, atnd_dict[aname][0])
        final_list.append([aname, atnd_dict[aname][0]])
        departments.append(atnd_dict[aname][0])

# write out users file
out = open('final_attendenc.csv', 'w')
wr = csv.writer(out, dialect='excel')
wr.writerow(['name', 'department', 'email'])
for item in final_list:
        wr.writerow(item)       
out.close()

# write out departments file 
out = open('latest_departments.csv', 'w')
wr = csv.writer(out, dialect='excel')
wr.writerow(['department'])
for item in departments:
    wr.writerow([item])       
out.close()

