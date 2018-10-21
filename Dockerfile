FROM python:3.6
MAINTAINER XenonStack

# Creating Application Source Code Directory
RUN mkdir -p /disaster-checklist-backend/

# Setting Home Directory for containers
WORKDIR /disaster-checklist-backend/

# Installing python dependencies
COPY requirements.txt /disaster-checklist-backend/
COPY credentials.json /disaster-checklist-backend/
COPY ./external_libs/ /disaster-checklist-backend/external_libs/
RUN pip install --upgrade pip
RUN pip install invoke
RUN pip install -r requirements.txt
RUN pip install /disaster-checklist-backend/external_libs/disaster_checklist-0.1/

# Copying src code to Container
COPY . /disaster-checklist-backend/app

# Application Environment variables
ENV APP_ENV development

# Exposing Ports
EXPOSE 5000:5000

# Setting Persistent data
VOLUME ["/app-data"]

#RUN cd app && python initial_load.py
# Running Python Application
CMD ["python", "app/app.py"]
#CMD ["python", "-m", "flask", "run"]