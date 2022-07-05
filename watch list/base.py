import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

with open("config.json","r") as f:
    data = json.load(f)
username = data["username"]
print (f'logged in as: {username}')

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

client = gspread.authorize(credentials)

worksheet = client.open("Anime_watch_list").sheet1
al = worksheet.get_all_values()

def update():
    global al 
    al = worksheet.get_all_values()

def compare(value,text):
    if "," in value:
        value = value.split(",")
        for val in value:
            if val.upper() == text.upper():
                return(True)
    elif value.upper() == text.upper():
        return(True)

def getusernum():
    x = al[0]
    count = 0
    for val in x:
        if compare(val,username) == True:
            break
        count += 1
    if count == 0:
        print("user not on data base")
    return(count)

def rfm():
    for x in al:
        if compare(x[2],username) == True:
            if x[usernum] == "FALSE":
                vale = "has not watched"
            elif x[usernum] == "TRUE":
                vale = "has watched"
            print(f'{x[0]},{x[1]},{vale}')

def rfme():
    for x in al:
        if compare(x[2],username) == True:
            if x[usernum] == "FALSE":
                print(f'{x[0]},{x[1]},')

def ma():
    for x in al:
        if compare(x[0],username) == True:
            print(x)

def add():
    count = 1
    for val in al :
        if val[0] == "":
            worksheet.update_cell(count, 1, username)
            anime = str(input("enter name of anime "))
            worksheet.update_cell(count, 2, anime)
            recc = str(input("recomendations "))
            worksheet.update_cell(count, 3, recc)
            have = str(input("have u watched?(y/n) "))
            if have == "y":
                worksheet.update_cell(count, usernum+1, "TRUE")
            elif have == "n":
                worksheet.update_cell(count, usernum+1, "FALSE")
            print("record entered")
            update()
            for val in al:
                if val[1] == anime:
                    print(val)
            break
        count += 1

def maw():
    count = 1
    for val in al:
        if val[usernum] == "FALSE":
            print(f'{count}) {val[1]}')
            count += 1

    choice = int(input("enter choice"))
    count = 1
    num = 1
    for val in al:
        if val[usernum] == "FALSE":
            if choice == count:
                worksheet.update_cell(num, usernum+1, "TRUE")
            count += 1
        num += 1

def fmbm():
    for x in al:
        if compare(x[0],username) == True and compare(x[2],username) == True:
            print(x)

def rd():
    count = 1
    for val in al:
        if val[usernum] == "FALSE":
            print(f'{count}) {val[1]}')
            count += 1

    choice = int(input("enter choice"))
    count = 1
    num = 1
    for val in al:
        if val[usernum] == "FALSE":
            if choice == count:
                worksheet.update_cell(num, usernum+1, "TRUE")
            count += 1
        num += 1

def change():
    global usernum , username
    username = str(input("Enter new name: "))
    data["username"] = username
    with open("config.json","w") as f:
        json.dump(data,f)
    usernum = getusernum()
    print(f'logged in as: {username}')

def main():
    global usernum
    usernum = getusernum()
    while True:
        print('''
1) my anime
2) reccomended for me
3) reccomended for me watched exluded
4) for me by me
5) add new
6) mark as watched
7) reccomend
8) change account
        ''')
        x = int(input("Enter choice "))
        if x == 1:
            ma()
        elif x == 2:
            rfm()
        elif x == 3:
            rfme()
        elif x == 4:
            fmbm()
        elif x == 5:
            add()
        elif x == 6:
            maw()
        elif x == 7:
            rd()
        elif x == 8:
            change()
        update()
main()