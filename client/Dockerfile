FROM python:3.9-buster AS build

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src ./src
COPY app.py ./

FROM python:3.9-slim

WORKDIR /app

COPY --from=build /root/.cache /root/.cache
COPY --from=build /app /app

# re-install python modules from cached wheels
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "app.py"]