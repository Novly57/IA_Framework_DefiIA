# base image
FROM python:3.8

# clone the necessary data
COPY ./app.py /MAZeltov/
COPY ./data/features_hotels.csv /MAZeltov/data/
COPY ./data/data.csv /MAZeltov/data/
COPY ./data/test_set.csv /MAZeltov/data/
COPY ./data/target_encoding.csv /MAZeltov/data/
COPY ./data/gradio_model /MAZeltov/data/
COPY ./analysis/train.py /MAZeltov/analysis/
COPY ./analysis/train_catboost.py /MAZeltov/analysis/
COPY ./requirements.txt /MAZeltov/



# change working directory to the repository
WORKDIR /MAZeltov/

RUN mkdir data/submit

# install all requirements
RUN pip install -r requirements.txt

# expose port 8000
EXPOSE 8000

# run the command
CMD ["bash"]
