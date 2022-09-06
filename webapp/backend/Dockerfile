FROM openjdk:11

RUN wget https://mirrors.estointernet.in/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz
RUN tar -xvf apache-maven-3.6.3-bin.tar.gz
RUN mv apache-maven-3.6.3 /opt/

RUN useradd -ms /bin/bash splinter

WORKDIR /home/splinter
RUN echo "M2_HOME='/opt/apache-maven-3.6.3'" >> /home/splinter/.bashrc
RUN echo 'PATH="$M2_HOME/bin:$PATH"' >> /home/splinter/.bashrc
RUN echo "export PATH" >> /home/splinter/.bashrc
ENV PATH=/opt/apache-maven-3.6.3/bin:$PATH

COPY ./ /home/splinter/app
WORKDIR /home/splinter/app
# RUN echo $PATH
# RUN ls /opt/apache-maven-3.6.3
RUN mvn install
ENTRYPOINT ["java", "-jar", "target/backend-0.0.1-SNAPSHOT.jar"]
