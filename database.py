from firebase import firebase
firebase = firebase.FirebaseApplication('https://fir-web-learn-e7ad1.firebaseio.com',None)
flag=0
prev_time=''
while True:
    with open('example1.csv', 'r') as csv_file:
        lines = csv_file.readlines()
        if flag == 0:
            prev = str(lines[-2]).split(',')
            prev_time = prev[0]
            flag = 1
        newVal = str(lines[-2]).split(',')
        newVal_time = newVal[0]

        if newVal_time != prev_time:
            if(newVal_time!='Time'):
                firebase.post('parent/', {'Time': newVal[0], 'Count': newVal[1][:-1]})
                print('Posted on Firebase')
            flag = 0
    csv_file.close()
