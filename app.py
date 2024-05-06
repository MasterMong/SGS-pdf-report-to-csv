import PyPDF2
import os

source = input("Enter source folder : ")
folder_name = source
path_source = './source/' + folder_name + '/'
path_des = './des/' + folder_name + '/'
files = os.listdir(path_source)
file_type = '.pdf'
des_allFile = path_des + 'all.csv'

# Filtering only the files.
files = [f for f in files if os.path.isfile(
    path_source+f) and f.endswith(file_type)]
if os.path.exists(path_des) == False:
    os.mkdir(path_des)
if os.path.exists(des_allFile):
    os.remove(des_allFile)
# exit()


def saveToFile(word, des_file):
    print(word)
    f = open(des_file, 'a', encoding='utf-8')
    f.write(word + '\n')
    f.close()
    saveToFileAll(word)


def saveToFileAll(word):
    print(word)
    f = open(des_allFile, 'a', encoding='utf-8')
    f.write(word + '\n')
    f.close()


def saveQuere(word, saveTo):
    saveToFile(word, saveTo)
    return True


des_file = ''


def emptyQuere():
    return 0


for file in files:
    des_file = path_des + file.replace(file_type, '.csv')
    source_file = path_source + file
    current_source_file = open(source_file, 'rb')
    ReadPDF = PyPDF2.PdfFileReader(current_source_file)
    pages = ReadPDF.numPages

    if os.path.exists(des_file):
        os.remove(des_file)
    else:
        f = open(des_file, 'x')
        f.close()

    stu_class = ''
    stu_room = ''
    tigger_class = False
    tigger_room = False
    subject_code = ''

    quere_subject, quere_fullTerm, quere_term, quere_year, quere_stu = '', '', '', '', ''

    for i in range(pages):
        is_newStu = False
        pageObj = ReadPDF.getPage(i)
        text = pageObj.extractText()

        emptyQuere()
        for word in text.split():
            # Class
            if tigger_class:
                stu_class = word
                tigger_class = False
            if tigger_room:
                stu_room = word
                tigger_room = False
            if word == 'ชชชนมชธยมศศกษาปปทรท':
                tigger_class = True
            if word == 'หหองทรท':
                tigger_room = True

            if len(word) == 6:  # Subject
                subject_num = word[1:]
                try:
                    if int(subject_num):
                        # saveToFile('Found : ' + quere_subject, des_file)
                        if quere_stu != '' and quere_fullTerm != '' and quere_subject != '':
                            saveQuere(quere_fullTerm +
                                      ',' +
                                      quere_term +
                                      ',' +
                                      quere_year +
                                      ',' +
                                      stu_class +
                                      ',' +
                                      stu_room +
                                      ',' +
                                      quere_stu +
                                      ',' +
                                      quere_subject,
                                      des_file)
                        quere_subject = word
                except:
                    print('skip subject')

            if len(word) == 6:  # Term
                year = word[:4]
                term = word[5:]
                end = word[4:]
                slash = end[:1]
                if slash == '/':
                    try:
                        if int(year):
                            if int(term):
                                quere_fullTerm = word
                                quere_term = term
                                quere_year = year
                                # saveToFile('Found : ' + quere_fullTerm, des_file)

                    except:
                        print('skip term')

            if len(word) == 5:  # SID
                try:
                    if int(word):
                        quere_stu = word
                        # saveToFile('Found : ' + quere_stu, des_file)
                except:
                    print('skip sid')

    emptyQuere()
    if quere_stu != '' and quere_fullTerm != '' and quere_subject != '':
        saveQuere(quere_fullTerm +
                  ',' +
                  quere_term +
                  ',' +
                  quere_year +
                  ',' +
                  stu_class +
                  ',' +
                  stu_room +
                  ',' +
                  quere_stu +
                  ',' +
                  quere_subject,
                  des_file)
    current_source_file.close()
