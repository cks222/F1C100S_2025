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

RUN pip install --upgrade -r requirements.txt

COPY --from=build-stage /ui/dist /app
ENV isProd=false
EXPOSE 1234
CMD ["python", "server.py"]
