FROM python:3.8

RUN mkdir docker_data

COPY requirements.txt ./requirements.txt
RUN  pip install -r requirements.txt

# COPY /data /data

COPY Dataprep.py .
COPY GetClusters.py .
COPY RunPrepAndClusters.py .

# Make app.sh executable
CMD ["python", "RunPrepAndClusters.py"]