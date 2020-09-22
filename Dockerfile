FROM ubuntu:18.04

ENTRYPOINT []

RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa==1.10.2 && pip3 install --no-cache requests && pip3 install --no-cache gspread && pip3 install --no-cache oauth2client && pip3 install --no-cache pyresparser && pip3 install --no-cache spacy==2.1.9 && pip3 install --no-cache nltk && python3 -m spacy download en_core_web_sm && python3 -m nltk.downloader words && python3 -m nltk.downloader stopwords

ADD . /app/

RUN chmod +x /app/start_services.sh
CMD /app/start_services.sh