CONTAINER_NAME=kobo_99_notifier

sudo docker rmi ${CONTAINER_NAME}
sudo docker build . -t ${CONTAINER_NAME}:latest