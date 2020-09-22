import spacy
import nltk
nltk.download('stopwords')
from pyresparser import ResumeParser
import requests
spacy.load('en_core_web_sm')


internship_word_list = ['intern', 'internship', 'research', 'fellowship']
python_dev_word_list = ['python', 'api', 'aws', 'ec2', 'django', 'flask', 'amazon web services', 'machine learning',
                    'ai', 'artificial intelligence', 'data science', 'database', 'mysql', 'sql']



#  download resume from g-drive link
def download_resume(url, user_email):
    g_drive_file_id = url.split("/d/")[1].split("/")[0]
    gdrive_direct_link = f"https://drive.google.com/uc?id={g_drive_file_id}"

    r = requests.get(gdrive_direct_link)

    if r.status_code == 200 and r.headers['content-type'] == "application/pdf":
        with open(f'{user_email}.pdf', 'wb') as f:
            f.write(r.content)
        return 1
    return 0

def calculate_individual_score(entity_list, lookup_words):
    score = 0
    if entity_list != None:
        for word in lookup_words:
            for entity in entity_list:
                if word in entity.lower():
                    if score >= 5:
                        break
                    score += 1

    return score

def calculate_overall_score(url, user_email, job_domain_word_list):

    if download_resume(url=url, user_email=user_email):
        data = ResumeParser(f'{user_email}.pdf').get_extracted_data()
        experiences = data['experience']
        skills = data['skills']

        job_domain_score = calculate_individual_score(skills, job_domain_word_list)
        job_domain_score += calculate_individual_score(experiences, job_domain_word_list)

        internship_score = calculate_individual_score(skills, internship_word_list)
        internship_score += calculate_individual_score(experiences, internship_word_list)

        out_of_score = 20
        total_score = job_domain_score + internship_score

        resume_score = int(round((total_score / out_of_score) * 100))
        return resume_score

    return -1