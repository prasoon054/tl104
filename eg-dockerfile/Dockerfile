FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

ENV INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
ENV LAB_DIRECTORY="/home/labDirectory"
ENV PATH="/home/.evaluationScripts:${PATH}"
ENV TERM=xterm-256color
RUN mkdir -p /home/.evaluationScripts
RUN mkdir -p /home/labDirectory
WORKDIR /home/labDirectory
CMD [ "/bin/bash", "-c", "bash /home/.evaluationScripts/init_activity.sh; while :; do sleep 10; done" ]
