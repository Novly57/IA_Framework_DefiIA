# base image
FROM python:3.8

# clone the repository
RUN git clone https://github.com/Novly57/IA_Framework_DefiIA.git

# change working directory to the repository
WORKDIR /IA_Framework_DefiIA

# install all requirements
RUN pip install -r requirements.txt

# expose port 8000
EXPOSE 8000

# run the command
CMD ["bash"]
