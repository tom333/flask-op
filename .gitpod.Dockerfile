FROM gitpod/workspace-full

RUN python -m install poetry
RUN poetry config virtualenvs.create false