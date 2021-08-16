FROM python:alpine3.7
RUN pip install Flask Flask_restful
EXPOSE 5001
COPY productsAPI.py /
ENTRYPOINT [ "python" ]
CMD [ "productsAPI.py" ]