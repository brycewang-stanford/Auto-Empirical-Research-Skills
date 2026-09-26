# phack: run the demo with nothing installed but Docker
#   docker build -t phack . && docker run --rm -it phack ./demo.sh /out
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY scripts ./scripts
COPY eval ./eval
COPY references ./references
COPY skills ./skills
COPY catalog ./catalog
COPY demo.sh ./
RUN pip install --no-cache-dir -e ".[dev]" && chmod +x demo.sh
ENV PYTHON=python JOBS=2
CMD ["./demo.sh", "/out"]
