docker-compose up -d
docker build -t f1c100s .
docker run -d --network milvus_network -p 1234:1234 f1c100s 