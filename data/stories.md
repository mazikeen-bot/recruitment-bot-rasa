## Greet -> Want job -> No
* greet
  - action_greet_user
  - action_ask_for_job
*deny
  - action_show_company_info

## Greet -> Want job -> Yes
* greet
  - action_greet_user
  - action_ask_for_job
*affirm
  - utter_look_for_vacancy
  - action_show_job_openings

## Java Job
* java_job
  - action_java_job_details
  - action_are_you_interested

## Python Job
* python_job
  - action_python_job_details
  - action_are_you_interested

## Interested in job
* interested
  - action_ask_name
  - form_applicant_name
  - form{"name": "form_applicant_name"}
  - form{"name": null}
  - form_phone_number
  - form{"name": "form_phone_number"}
  - form{"name": null}
  - form_email
  - form{"name": "form_email"}
  - form{"name": null}
  - form_resume_link
  - form{"name": "form_resume_link"}
  - form{"name": null}
  - form_hr_question
  - form{"name": "form_hr_question"}
  - form{"name": null}
  - form_why_us
  - form{"name": "form_why_us"}
  - form{"name": null}

## Not interested in job
* not_interested
  - utter_no_problem
  - action_show_job_openings

## boss info
* your_boss
  - action_my_boss
  
## weather details
* ask_about_weather
  - utter_weather

## how many languages
* languages
  - utter_languages

## data privacy
* data_privacy
  - utter_data_privacy

## say goodbye
* goodbye
  - utter_goodbye

## looking for job
* looking_for_job
  - utter_look_for_vacancy
  - action_show_job_openings

## not looking for job
* not_looking_for_job
  - utter_netflix_and_chill

## fallback
*fallback
    -action_fallback
  
## contact
*contact
    - utter_contact

## thank you
*thank_you
    - utter_thankyou
 
## agent be clever
*agent_be_clever
    - utter_agent_be_clever

## sad mood
*mood_unhappy
    - utter_mood_unhappy

## agent fired
*agent_fired
    - utter_agent_fired

## agent hungry
*agent_hungry
    - utter_agent_hungry

## agent residence
*agent_residence
    - utter_agent_residence

## agent hobby
*agent_hobby
    - utter_agent_hobby

## what do you mean
*dialog_what_do_you_mean
    - utter_dialog_what_do_you_mean

## user lonely
*user_lonely
    - utter_user_lonely

## user bored
*user_bored
    - utter_user_bored

## goodnight 1
*agent_goodnight
    - utter_goodnight
    
## goodnight 2
*greetings_goodnight
    - utter_goodnight
    
## agent name
*agent_name
    - utter_agent_name
    
## goodmorning
*greetings_goodmorning
    - utter_greetings_goodmorning

## emotions wow
*emotions_wow
    - utter_emotions_wow
 
## dialog wrong
*dialog_wrong
    - utter_dialog_wrong
    
## user excited
*user_excited
    - utter_user_excited
    
## agent_there
*agent_there
    - utter_agent_there

## appraisal no problem
*appraisal_no_problem
    - utter_appraisal_no_problem

## dialog hug
*dialog_hug
    - utter_dialog_hug

## agent_age
*agent_age
    - utter_agent_age
    
## agent_funny
*agent_funny
    - utter_agent_funny

## greetings_nice_to_meet_you
*greetings_nice_to_meet_you
    - utter_greetings_nice_to_meet_you
    
## greetings_nice_to_see_you
*greetings_nice_to_see_you
    - utter_greetings_nice_to_see_you
    
## agent_ready
*agent_ready
    - utter_agent_ready
    
## user_loves_agent
*user_loves_agent
    - utter_user_loves_agent
       
## dialog_sorry
*dialog_sorry
    - utter_dialog_sorry
    
## agent_beautiful
*agent_beautiful
    - utter_agent_beautiful
    
## agent_origin
*agent_origin
    - utter_agent_origin
    
## agent_birth_date
*agent_birth_date
    - utter_agent_birth_date
    
## agent_real
*agent_real
    - utter_agent_real
    
## emotions_ha_ha
*emotions_ha_ha
    - utter_emotions_ha_ha
    
## dialog_i_do_not_care
*dialog_i_do_not_care
    - utter_dialog_i_do_not_care
    
## user_misses_agent
*user_misses_agent
    - utter_user_misses_agent
    
## agent_boring
*agent_boring
    - utter_agent_boring
    
## appraisal_welcome
*appraisal_welcome
    - utter_appraisal_welcome
    
## agent_answer_my_question
*agent_answer_my_question
    - utter_agent_answer_my_question
    
## greetings_whatsup
*greetings_whatsup
    - utter_greetings_whatsup
    
## user_angry
*user_angry
    - utter_user_angry
    
## user_busy
*user_busy
    - utter_user_busy
    
## agent_annoying
*agent_annoying
    - utter_agent_annoying
    
## greetings_nice_to_talk_to_you
*greetings_nice_to_talk_to_you
    - utter_greetings_nice_to_talk_to_you
    
## agent_busy
*agent_busy
    - utter_agent_busy
    
## greetings_goodevening
*greetings_goodevening
    - utter_greetings_goodevening
    
## agent_crazy
*agent_crazy
    - utter_agent_crazy
    
## agent_sure
*agent_sure
    - utter_agent_sure
    
## agent_marry_user
*agent_marry_user
    - utter_agent_marry_user
    
## agent_can_you_help
*agent_can_you_help
    - utter_agent_can_you_help
    
## appraisal_bad
*appraisal_bad
    - utter_appraisal_bad
    
## greetings_how_are_you
*greetings_how_are_you
    - utter_greetings_how_are_you
    
## agent_happy
*agent_happy
    - utter_agent_happy
    
## mood_great
*mood_great
    - utter_happy

## bot challenge
*bot_challenge
    - utter_iamabot
