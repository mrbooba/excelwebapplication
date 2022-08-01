FROM python:3.7-slim

# On copie le local vers l'image du container
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --no-cache-dir

WORKDIR app/
# Ajouter les fichiers nécessaires pour faire tourner l'app streamlit
ADD ./app.py /app/app.py 
ADD ./Survey_Results.xlsx /app/Survey_Results.xlsx
ADD ./images/ /app/images/

EXPOSE 8501 

CMD ["streamlit","run","/app/app.py"]