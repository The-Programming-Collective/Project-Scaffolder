FROM maven:3.8.5-openjdk-17 as maven_builder

WORKDIR /app

COPY pom.xml .

COPY src ./src

RUN mvn clean package

RUN mv target/*.war target/backend.war


FROM tomcat:10.1.24-jdk17

COPY --from=maven_builder /app/target/backend.war /usr/local/tomcat/webapps/

EXPOSE 8080
