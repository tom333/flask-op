FROM gitpod/workspace-full

USER gitpod

RUN python -m pip install poetry
RUN poetry config virtualenvs.create false