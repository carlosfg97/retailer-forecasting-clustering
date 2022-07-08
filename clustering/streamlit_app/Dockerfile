FROM python:3.8

RUN mkdir docker_data

COPY requirements.txt ./requirements.txt
RUN  pip install -r requirements.txt

EXPOSE 8501 
# expose streamlit's standard port 

COPY . .
ENTRYPOINT ["streamlit", "run"]
CMD ["store_type_app.py"]

# docker container ls

# docker build -t streamlit_app . 

# docker run --name clusters_app -v C:\Users\carlo\docker_data:/docker_data -p 8501:8501 streamlit_app

# docker rm -f clusters_app