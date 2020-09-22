import re
from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, FollowupAction
from scripts.resume_analysis import calculate_overall_score, python_dev_word_list
from scripts.answer_analysis import answer_score
from scripts.video_analysis import download_answer_video
from scripts.g_sheet import add_candidate_data, fetch_gsheet_data
from templates.quick_reply import add_quick_reply


def job_openings():
    vacancy_sheet, vacancy_data = fetch_gsheet_data(sheet_name='Vacancies')
    data = []
    for item in vacancy_data:
        if item['Vacancies'] != 0:
            job_title = item['Job Title']
            intent = f"{item['Job Title'].lower().split(' ')[0]}_job"
            data = add_quick_reply(data, job_title=job_title, intent=intent)

    return data

def has_already_applied(phone_number, job_title):
    applied_candidates_sheet, applied_candidates_data = fetch_gsheet_data(sheet_name='Candidates-List')
    for item in applied_candidates_data:
        if item['Phone Number'] == phone_number and item['Job Title'] == job_title:
            return 1
    return 0


def save_candidate_data(tracker: Tracker):
    applicant_name = tracker.get_slot("applicant_name")
    phone_number = tracker.get_slot("phone_number")
    job_title = tracker.get_slot("job_title")
    email_id = tracker.get_slot("email_id")
    resume_link = tracker.get_slot("resume_link")
    resume_score = tracker.get_slot("resume_score")
    hr_answer = tracker.get_slot("hr_answer")
    hr_answer_score = tracker.get_slot("hr_answer_score")
    video_link = tracker.get_slot("video_link")

    candidate_data = [applicant_name,phone_number, job_title, email_id, resume_link,
             resume_score, hr_answer, hr_answer_score, video_link]

    if add_candidate_data(candidate_data = candidate_data):
        return "Data Added"

    return "Unable to add data"


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")
        return []

class ActionGreetUser(Action):

    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        gif_url = "https://www.techcodemonk.in/wp-content/uploads/2020/07/giphy.gif"
        text = "Hi I am 𝐈𝐬𝐚𝐚𝐜, the recruitment bot 👋"
        text1 = "I'm here to help you with your job application.<br><br> Ok, so let's get started."
        dispatcher.utter_message(image=gif_url)
        dispatcher.utter_message(text=text)
        dispatcher.utter_message(text=text1)
        return []


class ActionFallback(Action):

    def name(self) -> Text:
        return "action_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = "😕 Oops!I am sorry. I didn't understand you."
        text2 = "I am incredibly bad with conversation because I was only designed for one purpose - " \
                "taking in job applications for TechCodeMonk"
        data = [
            {
                "title": "✅ Yes",
                "payload": "/affirm"
            },
            {
                "title": "❌ No",
                "payload": "/deny"
            }
        ]
        message = {"payload": "quickReplies", "data": data}
        dispatcher.utter_message(text=text)
        dispatcher.utter_message(text=text2)
        dispatcher.utter_message(text="Are you looking for a job?", json_message=message)

        return [AllSlotsReset()]

class ActionAskForJob(Action):

    def name(self) -> Text:
        return "action_ask_for_job"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data = [
            {
                "title": "✅ Yes",
                "payload": "/affirm"
            },
            {
                "title": "❌ No",
                "payload": "/deny"
            }
        ]
        message = {"payload": "quickReplies", "data": data}
        dispatcher.utter_message(text="Are you looking for a job?", json_message=message)

        # dispatcher.utter_message(image="https://i.imgur.com/nGF1K8f.jpg")
        # pdf = {"payload": "pdf_attachment", "url":"https://civilcops-assets.nyc3.digitaloceanspaces.com/cleardekho/invoice.pdf", "title":"PDF"}
        # dispatcher.utter_message(text="attachment", json_message=pdf)

        return []


class ActionShowCompanyInfo(Action):

    def name(self) -> Text:
        return "action_show_company_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        no_problem = "Cool. No problem. 😇"
        company_info = "You can visit our " \
                       "<a href='https://www.techcodemonk.in/' target='_blank'>website</a> to know more."
        dispatcher.utter_message(text=company_info)

        return []

class ActionMyBoss(Action):

    def name(self) -> Text:
        return "action_my_boss"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        boss_info = "Kamran has created me."
        boss_linkedin = "You can check his <a href='https://www.linkedin.com/in/skamranahmed/' target='_blank'>LinkedIn</a> for more info."
        dispatcher.utter_message(text=boss_info)
        dispatcher.utter_message(text=boss_linkedin)

        return [AllSlotsReset()]


class ActionShowJobOpenings(Action):

    def name(self) -> Text:
        return "action_show_job_openings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        data = job_openings()
        message = {"payload": "quickReplies", "data": data}
        dispatcher.utter_message(text="These are the job openings we have right now.👇", json_message=message)

        return []


class ActionShowPythonJobDetails(Action):

    def name(self) -> Text:
        return "action_python_job_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message["intent"].get("name")

        dispatcher.utter_message(template="utter_python_job_details")
        return [SlotSet("job_title", intent)]


class ActionShowJavaJobDetails(Action):

    def name(self) -> Text:
        return "action_java_job_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message["intent"].get("name")


        dispatcher.utter_message(template="utter_java_job_details")
        return [SlotSet("job_title", intent)]


class ActionAreYouInterested(Action):

    def name(self) -> Text:
        return "action_are_you_interested"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data = [
            {
                "title": "✅ Yes",
                "payload": "/interested"
            },
            {
                "title": "❌ No",
                "payload": "/not_interested"
            }
        ]
        message = {"payload": "quickReplies", "data": data}
        dispatcher.utter_message(text="Are you interested in this role?", json_message=message)

        return []


class ActionAskName(Action):
    def name(self):
        return "action_ask_name"

    def run(self, dispatcher, tracker, domain):
        great = "Great 👌"
        help_with_details = "Now, please help me with some of your details 😊"
        ask_name = "Your 𝐧𝐚𝐦𝐞?"
        dispatcher.utter_message(text=great)
        dispatcher.utter_message(text=help_with_details)
        dispatcher.utter_message(text=ask_name)

        return []


class FormApplicantName(FormAction):
    def name(self):
        return "form_applicant_name"

    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        return ["applicant_name"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        return {
            "applicant_name": self.from_text()
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], ) -> List[Dict]:
        # after applicant name submission, ask for phone number
        ask_phone_number = "Your 𝐩𝐡𝐨𝐧𝐞 𝐧𝐮𝐦𝐛𝐞𝐫 (with country code)?"
        dispatcher.utter_message(text=ask_phone_number)
        return []


class FormPhoneNumber(FormAction):
    def name(self):
        return "form_phone_number"

    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        return ["phone_number"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        return {
            "phone_number": self.from_text()
        }

    def validate_phone_number(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],) -> Dict[Text, Any]:

        phone_num_pattern = re.compile(r"[+]?[0-9]{12}")
        is_valid_phone_num = phone_num_pattern.search(value)

        if is_valid_phone_num:
            return {"phone_number": value}

        # if phone number is invalid, ask again
        else:
            enter_valid_phone_num = "Please enter a valid 𝐩𝐡𝐨𝐧𝐞 𝐧𝐮𝐦𝐛𝐞𝐫. <br> (for example: +919987456432)"

            dispatcher.utter_message(text=enter_valid_phone_num)
            return {"phone_number": None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],) -> List[Dict]:

        most_recent_state = tracker.current_state()
        sender_id = most_recent_state['sender_id']
        phone_number = tracker.get_slot("phone_number")
        phone_number_converted = '+{}'.format(phone_number)
        sender_id_converted = '{}'.format(sender_id)

        #TODO: Check if user phone number exists in job DB
        phone_number = tracker.get_slot("phone_number")
        job_title = tracker.get_slot("job_title")

        # after phone number submission and previously applied for the same role, prompt this
        if has_already_applied(phone_number=int(phone_number), job_title=job_title):
            dispatcher.utter_message(template="utter_already_applied_for_this_job")
            # data = job_openings()
            # message = {"payload": "quickReplies", "data": data}
            # dispatcher.utter_message(text="These are the job openings we have right now.👇", json_message=message)
            return [FollowupAction("action_show_job_openings"), AllSlotsReset()]

        # after phone number submission and not previously applied for the same role, ask for email id
        else:
            ask_email = "Your 𝐞𝐦𝐚𝐢𝐥? <br> We'll use it to inform you in case you are selected 😊"
            dispatcher.utter_message(text=ask_email)
            return []


class FormEmail(FormAction):
    def name(self):
        return "form_email"

    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        return ["email_id"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        return {
            "email_id": self.from_text()
        }

    def validate_email_id(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], ) -> Dict[Text, Any]:
        intent = tracker.latest_message["intent"].get("name")
        email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        is_valid_email = email_pattern.search(value)

        if is_valid_email:
            extracted_email = is_valid_email.group()
            return {"email_id": extracted_email}

        # if email is invalid, ask again
        else:
            ask_valid_email = "Please enter a valid 𝐞𝐦𝐚𝐢𝐥. <br> (for example: username@gmail.com)"
            dispatcher.utter_message(text=ask_valid_email)
            return {"email_id": None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], ) -> List[Dict]:

        # after valid email submission, ask for resume link
        ask_resume_link = "🔗 Please enter the Google Drive link of your Resume or CV 📄"
        dispatcher.utter_message(text=ask_resume_link)
        return []


class FormResume(FormAction):
    def name(self):
        return "form_resume_link"

    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        return ["resume_link"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        return {
            "resume_link": self.from_text()
        }

    def validate_resume_link(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], ) -> Dict[Text, Any]:

        resume_url = value
        user_email = tracker.get_slot("email_id")
        resume_score = calculate_overall_score(url=resume_url, user_email=user_email, job_domain_word_list=python_dev_word_list)
        print(resume_score)
        # if resume link is invalid, ask again
        if resume_score == -1 or resume_score is None:
            ask_valid_resume_url = "Please enter a valid Google Drive Resume Link. " \
                                   "There seems to be some problem with the Resume link you entered."
            dispatcher.utter_message(text=ask_valid_resume_url)
            return {"resume_link": None}

        else:
            return {"resume_link": resume_url, "resume_score": resume_score}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], ) -> List[Dict]:

        # after valid resume link submission, ask Tell me about yourself
        got_resume = "Cool, I got your resume 📄"
        hr_question = "Now, I would like to know more about you.<br>Could you please tell me something about yourself 👤"
        dispatcher.utter_message(text=got_resume)
        dispatcher.utter_message(text=hr_question)
        return []


class FormHRQuestion(FormAction):
    def name(self):
        return "form_hr_question"

    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        return ["hr_answer"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        return {
            "hr_answer": self.from_text()
        }

    def validate_hr_answer(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], ) -> Dict[Text, Any]:
        if len(value) < 50:
            ask_descriptive_answer = "Please give a descriptive answer with at least 200 characters."
            dispatcher.utter_message(text=ask_descriptive_answer)
            return {"hr_answer": None}

        else:
            answer_text = value
            hr_answer_score = answer_score(answer_text)
            return {"hr_answer": value, "hr_answer_score": hr_answer_score}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], ) -> List[Dict]:

        # after valid resume link submission, ask why us
        why_suitable = "What makes you suitable for this job profile? Why do you want to apply for it?<br><br> 🤔"
        share_video_link = "🔹 Upload your video on Google drive, answering this question and share the link here 🔗 📹 <br>"\
                           "🔹 Video length must be between 30-60 secs"
        dispatcher.utter_message(text=why_suitable)
        dispatcher.utter_message(text=share_video_link)
        return []


class FormWhyUs(FormAction):
    def name(self):
        return "form_why_us"

    @staticmethod
    def required_slots(tracker: "Tracker") -> List[Text]:
        return ["video_link"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
        return {
            "video_link": self.from_text()
        }

    def validate_video_link(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], ) -> Dict[Text, Any]:

        video_link = value
        user_email = tracker.get_slot("email_id")

        if download_answer_video(url=video_link, user_email=user_email):
            return {"video_link": value}
        else:
            ask_valid_link = "Please enter a valid G-drive link for the video."
            dispatcher.utter_message(text=ask_valid_link)
            return {"video_link": None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], ) -> List[Dict]:

        print(save_candidate_data(tracker))

        # after valid video link submission, say we will get in touch
        thanks = "Thank you for filling in the details 😃"
        get_in_touch = "Give me some time to analyse your profile and I will get in touch with you through mail or phone.<br><br>Till then, take care!👋"
        dispatcher.utter_message(text=thanks)
        dispatcher.utter_message(text=get_in_touch)
        return [AllSlotsReset()]

