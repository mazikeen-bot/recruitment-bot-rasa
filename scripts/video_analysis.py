import requests

url = "https://drive.google.com/file/d/1Ok5TReoFwQQAp398PjvcWfIqUJOVyBUB/view?usp=sharing"

def download_answer_video(url, user_email):
    g_drive_file_id = url.split("/d/")[1].split("/")[0]
    gdrive_direct_link = f"https://drive.google.com/uc?id={g_drive_file_id}"

    r = requests.get(gdrive_direct_link)
    if r.status_code == 200 and r.headers['content-type'] == "video/mp4":
        # with open(f'{user_email}.mp4', 'wb') as f:
        #     f.write(r.content)
        return 1
    return 0

#  I have not included the video_analysis code because I do not want to make it public as of now.

