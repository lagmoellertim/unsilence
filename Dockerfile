FROM alpine:3.12

# Install requirements
RUN apk add python3 && \
    apk add py3-pip  && \
    pip3 install --upgrade pip && \
    apk add ffmpeg


# Install unsilence
RUN pip3 install unsilence

# Create work directory and run container as user
RUN addgroup -S app && adduser -S app -G app
RUN mkdir /app && chown app:app /app
WORKDIR /app
USER app

# Use unsilence as entrypoint (allows passing arguments directly to unsilence)
ENTRYPOINT ["/usr/bin/unsilence"]
