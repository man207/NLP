# NLP

## Tokenizer
regex is used to tokenize texts.

```python
def tokenize(string):
    regex = r"((([\u0621-\u06cc][.])+)[\u0621-\u06cc])|([\u0621-\u06cc]|[\u200C])+|[A-z]+|[(-)]|[\u0621-\u06cc]|((([\u0621-\u06cc][.])+)[\u0621-\u06cc])|([\u06f0-\u06f9]+([.][\u06f0-\u06f9]*)?)|([0-9]+([.][0-9]*)?)"
    matches = re.finditer(regex, string, re.MULTILINE)
    tolist = []
    for i in matches:
        tolist.append(i.group(0))
    return tolist
```
Tokenize unction takes a string and return a list of tokens.
The string is created with reading files with readfile func - The encoding of the file must be utf-8
```python
def readfile(file):
    f = open(file, "r", encoding="UTF-8")
    string = f.read()
    f.close()
    return string
```

## DF & TF

To get term and document ferquency first we read all files and tokenize them. Creating a list containg lists of tokenized texts.
Note that instead of a list to save doc name we could have used a dictionary to save tokenized string with keys with name of respecting files. But since names are sorted it doesn't make any diffrence.
Tokens are saved as set to pervent duplications and are converted to sorted list.
```python
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
```
Empty DF and TF and TF-DF are initiated with respective sizes
```python
tf = np.zeros((len(tokens) , len(tokenized) , 1) , dtype=np.int)
df = [0 for i in tokens]
tf_df = np.zeros((len(tokens) , len(tokenized)))
```
Then search documents for every token, and for every instance of a token increase it's count in TF. and if the token is seen at least once in the document. increase its respective DF by 1.
```python
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
```

then we get an excel file
```python
wb = Workbook()  
sheet1 = wb.add_sheet('Sheet 1') 
for tokenrow , docs in enumerate(tf):
    for doccol , tokennum in enumerate(docs):
        x = tf[tokenrow,doccol] / df[tokenrow]
        tf_df[tokenrow,doccol] = x
        sheet1.write(tokenrow + 1 , doccol + 1 , str(x)) 
for i , j in enumerate(tokens):
    sheet1.write(i + 1 , 0  , str(j)) 
for i , j in enumerate(docnames):
    sheet1.write(0 , i + 1 , str(j)) 
wb.save('xlwt example.xls') 
```

###TODO
- Make this into a lib
- Improve Tokenizer
