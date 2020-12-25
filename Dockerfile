FROM python:3.8.7-slim

COPY --chown=root:root app/ /root/app

WORKDIR /root/app

RUN pip3 install -r requirements.txt
RUN chmod +x run.py

ENV SECRET_KEY testkey

CMD ["python", "run.py"]

# ENV FLASK_APP run.py
#CMD ["flask"]