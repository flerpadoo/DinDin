import subprocess
import smtplib
import sys
import re

username = 'sendalertfrom@email.com'
password = 'SuperSecretPassword10'
macAddr = '88:19:08:84:c4:a7'

def watchNetworkForHost(macAddress):
    cmd = 'tcpdump -i en0 ether host %s -c 1' % macAddr
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return True

def sendmail(macAddress):
    sent_from = username
    sendTo = ['alertmenow@email.com']
    subject = 'Host Seen: %s' % macAddress
    body = 'The host you have been waiting for is now alive on the network. Better hurry up and get it popped! ;)'
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(username, password)
    email_text = "\nFrom: %s\nTo: %s\nSubject: %s\n%s" %\
        (sent_from, ", ".join(sendTo), subject, body)
    server.sendmail(username, sendTo, email_text)
    server.close()
    print 'Email sent!'

def main():
    if len(sys.argv) != 2:
        sys.exit('You must provide the MAC address of the host you want to alert on.')
    if len(sys.argv) == 2:
        macAddress = sys.argv[1]
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macAddress.lower()):
            if watchNetworkForHost(macAddress):
                sendmail(macAddress)
                sys.exit('Host was found. Email alert has been sent to ' + username)
        else:
            sys.exit('You have provided a bad MAC address. Please check your input and try again.')


main()
