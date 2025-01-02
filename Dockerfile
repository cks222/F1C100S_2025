# Stage 1: Build the Vue.js app
FROM node:20 as build-stage
WORKDIR /ui
COPY ./ui /ui
RUN npm install
RUN npm run build

# Stage 2: Set up the Python backend
FROM python:3.9-slim
WORKDIR /app
COPY ./server /app

RUN pip install python-multipart
RUN pip install uvicorn
RUN pip install edge-tts==7.0.0
RUN pip install fastapi==0.115.6
RUN pip install chardet==4.0.0
RUN pip install torch==2.5.1
RUN pip install tokenizers==0.21.0
RUN pip install accelerate==0.31.0
RUN pip install transformers==4.47.0

COPY --from=build-stage /ui/dist /app



EXPOSE 1234
CMD ["python", "server.py"]
