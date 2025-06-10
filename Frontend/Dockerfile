FROM python:3.9
WORKDIR /code
RUN pip install --no-cache-dir gradio
EXPOSE 7860
COPY ./ /code/app
ENV GRADIO_SERVER_NAME="0.0.0.0"
CMD ["python", "app/main.py"]