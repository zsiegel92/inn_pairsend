import smtplib
import csv
spreadsheetname = 'Buddy_Spreadsheet.csv'
defaultRecipient = 'zsiegel92@gmail.com'
fromName = 'Zach Siegel'
maxTestEmails = 2


#live = input("send emails? '0', '1', or '-1'")
#live = int(live)
live = -1



#defaultRecipient = 'guthrie.siegman@gmail.com'

if live ==1:
    contvar = input("Sending all emails to real recipients. Type 'yes' to proceed.")
    if contvar!='yes':
        raise inputAbort
elif live ==-1:
    numTestEmails = 0
    print("Sending all emails to default recipient.")
else:
    print("Not sending any emails.")

with open('emailLogin.txt','r') as loginInfo:
    gmail_user = loginInfo.readline()
    gmail_password =loginInfo.readline()

sent_from = gmail_user

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    print('Successfully created SMTP object.')
    server.ehlo()
    print("Successfully ehlo'ed.")
    server.login(gmail_user, gmail_password)
    print("Successfully logged in")
except:
    print('Something went wrong with login.')



with open(spreadsheetname,'r') as csvfile:
    inforeader = csv.reader(csvfile, delimiter=',', quotechar='"')
    headers = next(inforeader)
    for row in inforeader:
        bigEmail, bigPhone, bigFirst, lilFirst, lilLast, lilEmail, lilPhone, lilCity, lilGender, lilJob, lilIdentities, lilExcitementAndFear = row
        subject = "Getting in touch with your chavruta " + lilFirst + " " + lilLast + "!"
        
        greeting = "Hey " + bigFirst + ","
        closer = "Best wishes,\n" + fromName
        intro = "'Chavruta', 'one-to-ones', and 'pair-shares' are each a fundamental part of IfNotNow. We can't organize well unless we support and learn from each other. In the spirit of each of these practices, thank you for agreeing to participate in this project."
        
        main = "Partly based on your stated priorities, and partly at random, we (some hivekeepers) have paired you with " + lilFirst + " " + lilLast + ". Please get in touch with them! If " + lilFirst + " doesn't know something that you know about how IfNotNow does stuff in LA, this can be an oppurtunity to share it. More importantly, though, it's an opportunity to connect."
        
        info = "Here is some information " + lilFirst + " reported on their training sign-up:\n\n"
        for i in range(3,9):
            info = info + headers[i] + ": " + row[i] + "\n"
        
        body = "%s\n\n%s\n\n%s" % (intro,main,info)
        
        email_text ="%s\n\n%s\n%s" % (greeting,body,closer)
        message = 'Subject: {}\n\n{}'.format(subject, email_text)

#        print(message)

        try:
            if live ==1:
#                server.sendmail(sent_from, bigEmail, message)
                print('Email sent to ' + bigEmail + '!')
            elif (live ==-1) & (numTestEmails < maxTestEmails):
                server.sendmail(sent_from, defaultRecipient, message)
                numTestEmails += 1
                print("Test email " + str(numTestEmails) + "/" + str(maxTestEmails) + " sent to " + defaultRecipient + '! (Re-routed from ' + bigEmail + '.)')
            else:
                print('Email not sent to ' + bigEmail + '.')
        except:
            print('Something went wrong with sending.')



try:
    server.close()
except:
    print('Something went wrong with server close.')
