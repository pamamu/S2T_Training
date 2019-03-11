FROM pablomacias/s2t_main-controller

WORKDIR /srv/S2T/S2T_Training

ADD . .

RUN pip install -r requirements.txt

#CMD ["cat", "src/app.py"]


