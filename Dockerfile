FROM pamamu/s2t_main-controller

ARG SHARED_FOLDER
ENV SHARED_FOLDER = $SHARED_FOLDER
ARG TRAINING_NAME
ENV TRAINING_NAME = $TRAINING_NAME

WORKDIR /srv/S2T/S2T_Training

ADD . .

RUN pip install -r requirements.txt

CMD python src/app.py $TRAINING_NAME $SHARED_FOLDER


