import re , os
import numpy as np
import xlwt 
from xlwt import Workbook 


#writes any regexiter into file
def writeoutput(iters):
    f = open("ans.txt", "w", encoding="UTF-8")
    s = ""
    for i in iters:
        s = s + i.group(0) + "\n"
    f.write(s)
    f.close()


def readfile(file):
    f = open(file, "r", encoding="UTF-8")
    string = f.read()
    f.close()
    return string

def normalaize(string):
    ye = "ی ۍ ې ے ۓ ێ ؽ ﻱ ؠ ۑ ؾ ؿ ٸ ﻯ ﯼ ي"
    ye = ye.split(" ")
    harake = " َ ُ ِ ّ ً ٌ ٍ"
    harake = harake.split(" ")
    string = string.replace("ك" , "ک")
    for i in ye:
        string = string.replace(i , "ی")
    for i in harake:
        string = string.replace(i , "")
    return string

#tokenizes with  given regex and return list of tokens with repeatation 
def tokenize(string):
    regexes = {
        "link" : r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)",
        "email" : r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        "english_percent" : r"(([0-9]+([.][0-9]+)?)%)",
        "persian_percent" : r"([\u06f0-\u06f9]+([.][\u06f0-\u06f9]+)?)%",
        "username" : r"(@[A-z0-9_.]+)",
        "hashtag" : r"#([A-z\u0621-\u06cc_0-9]+)",
        "persian_word" : r"([\u0621-\u06cc]|[\u200C])+",
        "persian_acronym" : r"((([\u0621-\u06cc][.])+)[\u0621-\u06cc])",
        "english_word" : r"([A-z]+)",
        "persian_punc" : r"([»«،؛؟,])",
        "english_punc" : r"([<>:\"\'{};,.\\/~`&*()%$#@!?%|\--])",
        "english_num" : r"([0-9]+([.][0-9]+)?)",
        "persian_num" : r"([\u06f0-\u06f9]+([.][\u06f0-\u06f9]+)?)",
        "persian_date" : r"([\u06f0-\u06f9]+/[\u06f0-\u06f9]?[\u06f0-\u06f9]/[\u06f0-\u06f9]?[\u06f0-\u06f9])",
        "english_date" : r"([0-9]+/[0-9]?[0-9]/[0-9]?[0-9])",
        "emoji" : r"([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF]|🆔|⭕️|⏰)"
    }
    regex = "|".join([value for value in regexes.values()])
    string = normalaize(string)
    matches = re.finditer(regex, string, re.MULTILINE)
    tolist = []
    for i in matches:
        tolist.append(i.group(0))
    return tolist





#create list of tokens, docs and strings
tokens = set()
tokenized = []
docnames = []
for file in os.listdir("./docs"):
    if file.endswith(".txt"):
        x = tokenize(readfile("./docs/" + file))
        for i in x:
            tokens.add(i)
        tokenized.append(x)
        docnames.append(file)
tokens = list(sorted(tokens))



#create empty tf df and tf-df
tf = np.zeros((len(tokens) , len(tokenized) , 1) , dtype=np.int)
df = [0 for i in tokens]
tf_df = np.zeros((len(tokens) , len(tokenized)))

#get tf and df with list of tokens and tokenized docs
dfTest = False
for tokennum , token in enumerate(tokens):
    for docnum , doc in enumerate(tokenized):
        for i in doc:
            if i == token:
                dfTest = True
                tf[tokennum,docnum] = tf[tokennum,docnum] + 1
        if dfTest:
            pass
            df[tokennum] = df[tokennum] + 1
        dfTest = False

#print tf and df for some reasons
print(tf)
print(df)







wb = Workbook() 
#make an excel files with df-tf   
sheet1 = wb.add_sheet('Sheet 1') 
for tokenrow , docs in enumerate(tf):
    for doccol , tokennum in enumerate(docs):
        x = tf[tokenrow,doccol] / df[tokenrow]
        tf_df[tokenrow,doccol] = x
        sheet1.write(tokenrow + 1 , doccol + 1 , str(x)) 
        sheet1.write(tokenrow + 1 , doccol + 3 + len(tf[0]) , str(tf[tokenrow , doccol]))
    sheet1.write(tokenrow + 1 , doccol + 5 + len(tf[0])  , str(df[tokenrow]))
#this one fils token list
for i , j in enumerate(tokens):
    sheet1.write(i + 1 , 0  , str(j)) 
    
#and this one fills doc list
for i , j in enumerate(docnames):
    sheet1.write(0 , i + 1 , str(j)) 
    sheet1.write(0 , i + 3 + len(tf[0]) , str(j)) 
sheet1.write(0 , 4 +  2 * len(tf[0]) , str("DF")) 
sheet1.write(0 , 2 + len(tf[0]) , str("TF")) 
sheet1.write(0 , 0 , str("TF-DF")) 


#and save
wb.save('xlwt example.xls') 