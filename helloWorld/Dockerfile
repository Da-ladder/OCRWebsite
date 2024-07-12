# FOR RUNNING THE HOSTED SERVER
FROM python:3.12.3

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./testBranch /testBranch

WORKDIR /testBranch

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

