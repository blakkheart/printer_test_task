FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app/

RUN apt-get update \
    && apt-get install -y \
    curl \
    libxrender1 \
    libfontconfig \
    libxtst6 \
    xz-utils \
    wkhtmltopdf \
    python3-pip
RUN pip3 install Werkzeug executor gunicorn 

COPY . .
EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "--log-file", "-", "app:application"]




# FROM openlabs/docker-wkhtmltopdf:latest
# FROM python:3.11

# WORKDIR /app/

# # Install dependencies for running web service
# #RUN sudo apt-get update && sudo apt-get install -y python3-pip
# RUN pip3 install Werkzeug executor gunicorn 
# #RUN sudo apt-get install xvfb libfontconfig wkhtmltopdf
# COPY . .
# EXPOSE 80
# #CMD cat /tmp/
# #ENTRYPOINT ["cat", "/tmp/"]
# ENTRYPOINT ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:80", "--log-file", "-", "app:application"]
# CMD ["cat", "/tmp/"]
# # Show the extended help
# #CMD ["gunicorn", "-b", "0.0.0.0:80", "--log-file", "-", "app:application"]