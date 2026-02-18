# Stage 1: Build
FROM docker.io/maven:3.9-eclipse-temurin-25-alpine AS builder

LABEL authors="willian"

WORKDIR /builder

COPY pom.xml .

RUN mvn dependency:go-offline -B

COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Runner
FROM docker.io/eclipse-temurin:25-jre-alpine AS runner

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /builder/target/finfrases-*.jar ./app.jar

EXPOSE 8080

USER appuser

ENTRYPOINT [ "java", "-jar", "app.jar" ]

LABEL org.opencontainers.image.title="FinFrases API" \
    org.opencontainers.image.version="0.0.1"