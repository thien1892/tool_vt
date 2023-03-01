FROM python:3.9-slim

WORKDIR /app

# ---------
# MS CORE FONTS
# ---------
# from http://askubuntu.com/a/25614
RUN apt-get update
RUN apt-get install -y --no-install-recommends software-properties-common curl wget cabextract xfonts-utils fontconfig
RUN apt-get update


RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections
RUN wget http://ftp.de.debian.org/debian/pool/contrib/m/msttcorefonts/ttf-mscorefonts-installer_3.6_all.deb
RUN dpkg -i ttf-mscorefonts-installer_3.6_all.deb
ADD localfonts.conf /etc/fonts/local.conf
RUN fc-cache -f -v


RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    libreoffice-writer -y \
    libzbar0 \
    libzbar-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]