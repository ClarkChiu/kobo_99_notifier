FROM    chrome-robot:latest
WORKDIR /kobo_99_notifier

COPY    requirements.txt ./
RUN     pip3 install -r requirements.txt
