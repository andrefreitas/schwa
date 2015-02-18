FROM ubuntu:14.04

# Install Java
RUN apt-get install software-properties-common -y
RUN \
  echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y oracle-java7-installer && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /var/cache/oracle-jdk7-installer

# Install wget
RUN apt-get install wget -y

# Install Scala
RUN wget www.scala-lang.org/files/archive/scala-2.11.5.deb
RUN dpkg -i scala-2.11.5.deb
RUN apt-get update
RUN apt-get install scala -y

# Install curl
RUN apt-get install curl -y

# Install SBT
RUN \
  curl -L -o sbt-0.13.7.deb https://dl.bintray.com/sbt/debian/sbt-0.13.7.deb && \
  dpkg -i sbt-0.13.7.deb && \
  rm sbt-0.13.7.deb && \
  apt-get update && \
  apt-get install sbt

# Install git
RUN apt-get install git -y
WORKDIR /git

# Clone a repository
RUN git clone https://github.com/scala/scala

# Copy schwa code
WORKDIR /schwa
ADD . .


# Default run
CMD ["echo", "hello"]