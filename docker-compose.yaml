# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

# Basic Airflow cluster configuration for CeleryExecutor with Redis and PostgreSQL.
#
# WARNING: This configuration is for local development. Do not use it in a production deployment.
#
# This configuration supports basic configuration using environment variables or an .env file
# The following variables are supported:
#
# AIRFLOW_IMAGE_NAME           - Docker image name used to run Airflow.
#                                Default: apache/airflow:2.9.2
# AIRFLOW_UID                  - User ID in Airflow containers
#                                Default: 50000
# AIRFLOW_PROJ_DIR             - Base path to which all the files will be volumed.
#                                Default: .
# Those configurations are useful mostly in case of standalone testing/running Airflow in test/try-out mode
#
# _AIRFLOW_WWW_USER_USERNAME   - Username for the administrator account (if requested).
#                                Default: airflow
# _AIRFLOW_WWW_USER_PASSWORD   - Password for the administrator account (if requested).
#                                Default: airflow
# _PIP_ADDITIONAL_REQUIREMENTS - Additional PIP requirements to add when starting all containers.
#                                Use this option ONLY for quick checks. Installing requirements at container
#                                startup is done EVERY TIME the service is started.
#                                A better way is to build a custom image or extend the official image
#                                as described in https://airflow.apache.org/docs/docker-stack/build.html.
#                                Default: ''
#
# Feel free to modify this file to suit your needs.
---
x-airflow-common:
  &airflow-common
  # Use custom image that builds on top of default airflow image (currently; Default: apache/airflow:2.9.2)
  # Image stored on Dockerhub
  image: ${DOCKERHUB_NAMESPACE}/${DOCKERHUB_REPOSITORY}:latest
  # Use the .env file to read the connection params and variables - SWITCH THIS OFF WHEN USING GITHUB ACTIONS
  # env_file:
  #   - .env
  environment:
    &airflow-common-env
    # Set executor to CeleryExecutor 
    AIRFLOW__CORE__EXECUTOR: CeleryExecutor
    # Use SQLAlchemy to connect to Airflow's metadata Postgres database using the psycopg2 driver
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://${METADATA_DATABASE_USERNAME}:${METADATA_DATABASE_PASSWORD}@${POSTGRES_CONN_HOST}:${POSTGRES_CONN_PORT}/${METADATA_DATABASE_NAME}
    # Postgres database backend for storing task results executed by workers
    AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://${CELERY_BACKEND_USERNAME}:${CELERY_BACKEND_PASSWORD}@${POSTGRES_CONN_HOST}:${POSTGRES_CONN_PORT}/${CELERY_BACKEND_NAME}
    # URL for the Redis message broker - handles the communication and task distribution between the scheduler and workers
    AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0
    # Key for encrypting data
    AIRFLOW__CORE__FERNET_KEY: ${FERNET_KEY}
    # New DAGs are paused by default
    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
    # Set to false to remove default DAGs - https://stackoverflow.com/questions/43410836/how-to-remove-default-example-dags-in-airflow
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    # Configure authentication backends. Enable basic & session-based authentication
    AIRFLOW__API__AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth,airflow.api.auth.backend.session'
    # Enable health checks for the scheduler
    AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK: 'true'
    # Setting Airflow Connections and Variables
    # NOTE 1: These will not show up on Airflow UI or using airflow connections/ variables list 
    # However, functions such as Variable.get() will still work as per Airflow docs as long as
    # the variable starts with AIRFLOW_VAR_- https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html#storing-variables-in-environment-variables
    # NOTE 2: Single underscores are used for Airflow to read connections/ variables
    # Connection can be written as URI: 
    # AIRFLOW_CONN_{CONN_ID}='my-conn-type://login:password@host:port/schema?param1=val1&param2=val2'
    # Connection to an external PostgreSQL database needed to store the data from the ELT process
    AIRFLOW_CONN_POSTGRES_DB_YT_ELT: 'postgresql://${ELT_DATABASE_USERNAME}:${ELT_DATABASE_PASSWORD}@${POSTGRES_CONN_HOST}:${POSTGRES_CONN_PORT}/${ELT_DATABASE_NAME}'
    # Variables can be written as follows: 
    # AIRFLOW_VAR_{VARIABLE_NAME}
    AIRFLOW_VAR_API_KEY: ${API_KEY}
    AIRFLOW_VAR_CHANNEL_HANDLE: ${CHANNEL_HANDLE}
    # Postgres databases environment variables - Needed for integration and data quality tests
    ELT_DATABASE_NAME: ${ELT_DATABASE_NAME}
    ELT_DATABASE_USERNAME: ${ELT_DATABASE_USERNAME}
    ELT_DATABASE_PASSWORD: ${ELT_DATABASE_PASSWORD}
    POSTGRES_CONN_HOST: ${POSTGRES_CONN_HOST}
    POSTGRES_CONN_PORT: ${POSTGRES_CONN_PORT}
  volumes:
    - ./config:/opt/airflow/config
    - ./dags:/opt/airflow/dags
    - ./data:/opt/airflow/data
    - ./include:/opt/airflow/include
    - ./logs:/opt/airflow/logs
    - ./plugins:/opt/airflow/plugins
    - ./tests:/opt/airflow/tests
  user: "${AIRFLOW_UID}:0"
  depends_on:
    &airflow-common-depends-on
    redis:
      condition: service_healthy
    postgres:
      condition: service_healthy

services:
  postgres:
    container_name: postgres
    image: postgres:13
    # Use the .env file to read the connection params - SWITCH THIS OFF WHEN USING GITHUB ACTIONS
    # env_file:
    #   - .env
    # Env vars after POSTGRES_PASSWORD are needed for CI-CD workflow - SWITCH THIS ALL ON WHEN USING GITHUB ACTIONS
    environment:
      - POSTGRES_USER=${POSTGRES_CONN_USERNAME}
      - POSTGRES_PASSWORD=${POSTGRES_CONN_PASSWORD}
      - METADATA_DATABASE_NAME=${METADATA_DATABASE_NAME}
      - METADATA_DATABASE_USERNAME=${METADATA_DATABASE_USERNAME}
      - METADATA_DATABASE_PASSWORD=${METADATA_DATABASE_PASSWORD}
      - ELT_DATABASE_NAME=${ELT_DATABASE_NAME}
      - ELT_DATABASE_USERNAME=${ELT_DATABASE_USERNAME}
      - ELT_DATABASE_PASSWORD=${ELT_DATABASE_PASSWORD}
      - CELERY_BACKEND_NAME=${CELERY_BACKEND_NAME}
      - CELERY_BACKEND_USERNAME=${CELERY_BACKEND_USERNAME}
      - CELERY_BACKEND_PASSWORD=${CELERY_BACKEND_PASSWORD}
      - POSTGRES_CONN_HOST=${POSTGRES_CONN_HOST}
      - POSTGRES_CONN_PORT=${POSTGRES_CONN_PORT}
    ports:
      - 5432:5432
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
      - ./docker/postgres/init-multiple-databases.sh:/docker-entrypoint-initdb.d/init-multiple-databases.sh
    # Test connection to 1 of 3 dbs, the metadata db in this case
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "${POSTGRES_CONN_USERNAME}", "-d", "${METADATA_DATABASE_NAME}"]
      interval: 10s
      retries: 5
      start_period: 5s
    restart: always

  redis:
    # Redis is limited to 7.2-bookworm due to licencing change
    # https://redis.io/blog/redis-adopts-dual-source-available-licensing/
    image: redis:7.2-bookworm
    container_name: redis
    expose:
      - 6379
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 30s
      retries: 50
      start_period: 30s
    restart: always

  airflow-webserver:
    <<: *airflow-common
    command: webserver
    container_name: airflow-webserver
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-scheduler:
    <<: *airflow-common
    command: scheduler
    container_name: airflow-scheduler
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8974/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-worker:
    <<: *airflow-common
    command: celery worker
    container_name: airflow-worker
    healthcheck:
      test:
        - "CMD-SHELL"
        - 'celery --app airflow.providers.celery.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}" || celery --app airflow.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}"'
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    environment:
      <<: *airflow-common-env
      # Required to handle warm shutdown of the celery workers properly
      # See https://airflow.apache.org/docs/docker-stack/entrypoint.html#signal-propagation
      DUMB_INIT_SETSID: "0"
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  # airflow-triggerer:
  #   <<: *airflow-common
  #   command: triggerer
  #   container_name: airflow-triggerer
  #   healthcheck:
  #     test: ["CMD-SHELL", 'airflow jobs check --job-type TriggererJob --hostname "$${HOSTNAME}"']
  #     interval: 30s
  #     timeout: 10s
  #     retries: 5
  #     start_period: 30s
  #   restart: always
  #   depends_on:
  #     <<: *airflow-common-depends-on
  #     airflow-init:
  #       condition: service_completed_successfully

  airflow-init:
    <<: *airflow-common
    entrypoint: /bin/bash
    container_name: airflow-init
    command:
      - -c
      - |
        if [[ -z "${AIRFLOW_UID}" ]]; then
          echo
          echo -e "\033[1;33mWARNING!!!: AIRFLOW_UID not set!\e[0m"
          echo "If you are on Linux, you SHOULD follow the instructions below to set "
          echo "AIRFLOW_UID environment variable, otherwise files will be owned by root."
          echo "For other operating systems you can get rid of the warning with manually created .env file:"
          echo "    See: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#setting-the-right-airflow-user"
          echo
        fi
        one_meg=1048576
        mem_available=$$(($$(getconf _PHYS_PAGES) * $$(getconf PAGE_SIZE) / one_meg))
        cpus_available=$$(grep -cE 'cpu[0-9]+' /proc/stat)
        disk_available=$$(df / | tail -1 | awk '{print $$4}')
        warning_resources="false"
        if (( mem_available < 4000 )) ; then
          echo
          echo -e "\033[1;33mWARNING!!!: Not enough memory available for Docker.\e[0m"
          echo "At least 4GB of memory required. You have $$(numfmt --to iec $$((mem_available * one_meg)))"
          echo
          warning_resources="true"
        fi
        if (( cpus_available < 2 )); then
          echo
          echo -e "\033[1;33mWARNING!!!: Not enough CPUS available for Docker.\e[0m"
          echo "At least 2 CPUs recommended. You have $${cpus_available}"
          echo
          warning_resources="true"
        fi
        if (( disk_available < one_meg * 10 )); then
          echo
          echo -e "\033[1;33mWARNING!!!: Not enough Disk space available for Docker.\e[0m"
          echo "At least 10 GBs recommended. You have $$(numfmt --to iec $$((disk_available * 1024 )))"
          echo
          warning_resources="true"
        fi
        if [[ $${warning_resources} == "true" ]]; then
          echo
          echo -e "\033[1;33mWARNING!!!: You have not enough resources to run Airflow (see above)!\e[0m"
          echo "Please follow the instructions to increase amount of resources available:"
          echo "   https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#before-you-begin"
          echo
        fi
        mkdir -p /sources/dags /sources/data /sources/include /sources/logs /sources/tests
        chown -R "${AIRFLOW_UID}:0" /sources/{dags,data,include,logs,tests}
        exec /entrypoint airflow version
    # yamllint enable rule:line-length
    environment:
      <<: *airflow-common-env
      _AIRFLOW_DB_MIGRATE: 'true'
      _AIRFLOW_WWW_USER_CREATE: 'true'
      _AIRFLOW_WWW_USER_USERNAME: ${AIRFLOW_WWW_USER_USERNAME}
      _AIRFLOW_WWW_USER_PASSWORD: ${AIRFLOW_WWW_USER_PASSWORD}
    user: "0:0"
    volumes:
      - .:/sources

  airflow-cli:
    <<: *airflow-common
    profiles:
      - debug
    environment:
      <<: *airflow-common-env
      CONNECTION_CHECK_MAX_COUNT: "0"
    # Workaround for entrypoint issue. See: https://github.com/apache/airflow/issues/16252
    command:
      - bash
      - -c
      - airflow

  # # You can enable flower by adding "--profile flower" option e.g. docker-compose --profile flower up
  # # or by explicitly targeted on the command line e.g. docker-compose up flower.
  # # See: https://docs.docker.com/compose/profiles/
  # flower:
  #   <<: *airflow-common
  #   command: celery flower
  #   container_name: airflow-celery-flower
  #   profiles:
  #     - flower
  #   ports:
  #     - "5555:5555"
  #   healthcheck:
  #     test: ["CMD", "curl", "--fail", "http://localhost:5555/"]
  #     interval: 30s
  #     timeout: 10s
  #     retries: 5
  #     start_period: 30s
  #   restart: always
  #   depends_on:
  #     <<: *airflow-common-depends-on
  #     airflow-init:
  #       condition: service_completed_successfully

volumes:
  postgres-db-volume: