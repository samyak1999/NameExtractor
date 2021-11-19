from flask import Flask,render_template,request 
import pandas as pd
import regex as re

# ## method 1
# def get_human_names(text):
#     tokens = nltk.tokenize.word_tokenize(text)
#     pos = nltk.pos_tag(tokens)
#     sentt = nltk.ne_chunk(pos, binary = False)
#     person_list = []
#     person = []
#     name = ""
#     for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
#         for leaf in subtree.leaves():
#             person.append(leaf[0])
#         if len(person) > 1: #avoid grabbing lone surnames
#             for part in person:
#                 name += part + ' '
#             if name[:-1] not in person_list:
#                 person_list.append(name[:-1])
#             name = ''
#         person = []

#     return (person_list)

# #method 2
# def extract(text):
#     for sent in nltk.sent_tokenize(text):
#         tokens = nltk.tokenize.word_tokenize(sent)
#         tags = st.tag(tokens)
#         for tag in tags:
#             if tag[1] == "PERSON":
#                 print(tag)                   
# #import en_core_web_sm

# nlp = spacy.load('en_core_web_sm')
# matcher = Matcher(nlp.vocab)


# #method 3
# def extract_name(resume_text):
#     nlp_text = nlp(resume_text.upper())
#     # First name and Last name are always Proper Nouns
#     pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
#     matcher.add('NAME',[pattern])
#     matches = matcher(nlp_text)
#     for match_id, start, end in matches:
#         span = nlp_text[start:end]
#         return span.text


    
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def upload_file():
    if request.method == "POST":
        file_obj=request.files.getlist('file_name')
        ls=[]
        for f in file_obj:
            fileName=f.filename
            human_name=re.findall(r'(?:(?<=^)|(?<=[^A-Za-z.,]))[A-Za-z.,]+(?: [A-Za-z.,]+)*(?:(?=[^A-Za-z.,])|(?=$))', fileName)[0]
            a= [".","pdf","gmail"]
            for x in a:
                if re.search(x,human_name):
                    human_name=human_name.replace(x," ")
            ls.append([human_name,fileName])

        df = pd.DataFrame(ls,columns=['Names','File name'])
        return render_template("upload-file.html", tables=[df.to_html(classes='data',header="true")],msg = "File(s) have been uploaded ")
    return render_template("upload-file.html",msg = "please choose a file ")
if __name__ == '__main__':
    app.run(debug=True)
