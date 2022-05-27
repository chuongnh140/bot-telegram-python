import random
import array
import json
import requests
import subprocess as sb
import os

def genpass ():

    # maximum length of password needed
    # this can be changed to suit your password length
    MAX_LEN = 10

    # declare arrays of the character that we need in out password
    # Represented as chars to enable easy string concatenation
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    LOWCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']

    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']

    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '|', '~', '>',
            '*', '(', ')', '<']


    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOWCASE_CHARACTERS + SYMBOLS


    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOWCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)

    # combine the character randomly selected above
    # at this stage, the password contains only 4 characters but
    # we want a 12-character password
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol


    # now that we are sure we have at least one character from each
    # set of characters, we fill the rest of
    # the password length by selecting randomly from the combined
    # list of character above.
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)

        # convert temporary password into array and shuffle to
        # prevent it from having a consistent pattern
        # where the beginning of the password is predictable
        #'u' Unicode character
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)

    # traverse the temporary password array and append the chars
    # to form the password
    password = ""
    for x in temp_pass_list:
        password = password + x
    return password



def quotes_bot():
    url_quotes = "https://zenquotes.io/api/random"
    response = requests.get(url_quotes)
    json_data = json.loads(response.text)
    return json_data
    


def cve_search(cve):
    cve_search_url = "https://cve.circl.lu/api/cve/"
    response = requests.get(cve_search_url + cve)
    result = json.loads(response.text)   
    return result



def cve_latest():
    cve_latest_url = "https://cve.circl.lu/api/last"
    response = requests.get(cve_latest_url)
    result = json.loads(response.text)
    return result

        
        
def checkOnline(ip):
    cmd_ping = "ping -c 1 {0}  > /dev/null 2>&1".format(ip)
    result = os.system(cmd_ping)
    if result == 0:
        return 0
    else:
        return 1
        
    
    
def port(ip, port):
    cmd = 'nc -zv {0} {1}'.format(ip, port)
    result = sb.getoutput(cmd)
    return result


def trace(ip):
    cmd = "traceroute -n {0}".format(ip)
    result = sb.getoutput(cmd)
    return result