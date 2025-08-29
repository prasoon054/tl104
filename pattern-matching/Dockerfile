FROM ubuntu:24.04
LABEL "maintainer"="bodhitree"
LABEL version="1.0"
LABEL description="Regex"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y \
&& apt-get install -y man-db manpages-posix nano curl \
&& apt-get install -y python3-pip python3-dev

RUN ln -s /usr/bin/python3 /usr/local/bin/python
 
RUN apt-get install -y nodejs npm
 
WORKDIR /app

RUN npm init -y
RUN npm install puppeteer cssom color

RUN apt-get install -y libnss3
RUN apt-get install -y libatk1.0-0
RUN apt-get install -y libatk-bridge2.0-0
RUN apt-get update
RUN apt-get install -y libcups2
RUN apt-get install -y libxkbcommon-x11-0
RUN apt-get install -y ca-certificates fonts-liberation libappindicator3-1 libasound2t64 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release

RUN apt-get install --reinstall -y locales
# uncomment chosen locale to enable it's generation
RUN sed -i 's/# pl_PL.UTF-8 UTF-8/pl_PL.UTF-8 UTF-8/' /etc/locale.gen
# generate chosen locale
RUN locale-gen pl_PL.UTF-8
# expand the image
# RUN yes | unminimize
# set system-wide locale settings
ENV LANG=pl_PL.UTF-8
ENV LANGUAGE=pl_PL
ENV LC_ALL=pl_PL.UTF-8
 
RUN mkdir /home/.evaluationScripts /home/labDirectory

RUN echo "cd /home/labDirectory" >> /root/.bashrc

ENV INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
ENV LAB_DIRECTORY="/home/labDirectory"
ENV PATH="/home/.evaluationScripts:${PATH}"

COPY .evaluationScripts /home/.evaluationScripts
COPY labDirectory /home/labDirectory

WORKDIR /home/labDirectory

CMD [ "/bin/bash", "-c", "bash /home/.evaluationScripts/init_activity.sh; while :; do sleep 10; done" ]
