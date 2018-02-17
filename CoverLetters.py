
from mailmerge import MailMerge
from datetime import date
import comtypes.client
import csv
import os
import shutil

os.chdir("C:\\Users\\Orwic\\coding\\jobsearch\\")
path = os.getcwd() + '\\'

# Ask inputs for business names
focus = input('\nSoftware, Web, or Engineer Template: ').title()
position = input('\nJob Title: ').title()
business = input('\nCompany Name: ').title()
languages = input('\nPrimary Languages used: ')
jobNeeds = input('\nFinish this sentence: I have built the foundational skills that allow'
                 'me the opportunity to work on...')

# set variables dependant on the focus
if focus == 'Software':
    coverLetter = 'Software Developer Cover Letter.docx'
    resume = 'Software Developer.docx'
elif focus == 'Web':
    coverLetter = 'Web Developer Cover Letter.docx'
    resume = 'Web Developer.docx'
elif focus == 'Engineer':
    coverLetter = 'Software Engineer Cover Letter.docx'
    focus = focus + 'ing'
    resume = 'Software Engineer.docx'

docs = [coverLetter,resume]

# Append a Cover letter
document = MailMerge(coverLetter)
document.merge(
    Position=position,
    Focus=focus,
    Business=business,
    Languages=languages,
    JobNeeds=jobNeeds,
    Date='{:%d-%b-%Y}'.format(date.today())
)
document.write('Orwick ' + position + ' Cover.docx')
coverLetter = 'Orwick ' + position + ' Cover.docx'

# Append a Resume
document = MailMerge(resume)
document.merge(Position=position)
document.write('Orwick ' + position + ' Resume.docx')
resume = 'Orwick ' + position + ' Resume.docx'

print('\nApppend Cover Letter and Resume completed')


# Save Cover and Resumes as PDF
def pdf_maker(path, position):
    wdFormatPDF = 17

    inputCoverFile = path + 'Orwick ' + position + ' Cover.docx'
    outputCoverFile = path + 'Orwick ' + position + ' Cover'
    inputResumeFile = path + 'Orwick ' + position + ' Resume.docx'
    outputResumeFile = path + 'Orwick ' + position + ' Resume'

    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(os.path.abspath(inputCoverFile))
    doc.SaveAs(os.path.abspath(outputCoverFile), FileFormat=wdFormatPDF)
    doc2 = word.Documents.Open(os.path.abspath(inputResumeFile))
    doc2.SaveAs(os.path.abspath(outputResumeFile), FileFormat=wdFormatPDF)
    doc.Close()
    doc2.Close()
    word.Quit()
    print('\nPDFs completed')


# Create new folder for company and put all created files in there
def folder_creator(path, business, position):
    if not os.path.exists(path + 'Finished Product\\' + business):
        os.makedirs(path + 'Finished Product\\' + business)

    finalPath = path + 'Finished Product\\' + business

    shutil.move('Orwick ' + position + ' Cover.pdf', finalPath)
    shutil.move('Orwick ' + position + ' Cover.docx', finalPath)
    shutil.move('Orwick ' + position + ' Resume.docx', finalPath)
    shutil.move('Orwick ' + position + ' Resume.pdf', finalPath)
    print('\nCover Letter and Resume organized and filed together')


# Append csv sheet to document who I applied to
def tracking(business, position):
    rows = ['{:%d-%b-%Y}'.format(date.today()), business, position]

    with open(r'Job Tracking.csv', 'a', newline='') as f:
        excel = csv.writer(f)
        excel.writerow(rows)
        print('\nTracking completed')

pdf_maker(path, position)
folder_creator(path, business, position)
tracking(business, position)

print('\n\n******Cover Letter completed******\n\n')