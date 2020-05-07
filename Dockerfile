FROM continuumio/anaconda3
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 3502
CMD ["python3","app.py"]
