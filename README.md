## Philipposaurus-Bot
### Fun - Moderation - Nonsense Stuff

---

1. Make a `philipposaurus.env`-File with the following variables:
   ```bash
   BOT_TOKEN=
   
   HYPIXEL_API_KEY=
   OSU_API_KEY=
   WOLFRAMALPHA_API_KEY=
   
   BRIDGE_API_URL=https://api.poweredbyfluxi.ml/
   
   POSTGRES_USERNAME=postgres
   POSTGRES_PASSWORD=postgres
   ```
2. Make some docker stuff
    - Create a Docker-network named `main` and `database`
      ```bash
      docker network create --subnet 192.168.0.0/24 main
      docker network create --subnet 192.168.1.0/24 database
      ```
    - Remove the api section and the depends_on section. Your `docker-compose.yml` should now look like this:
      ```yml
      version: "3.7"
      services:
        philipposaurus:
          container_name: philipposaurus
          hostname: main_bot
          build: .
          restart: always
          env_file: philipposaurus.env
          # Removed depends_on section
        networks:
          - database
        volumes:
          - ./philipposaurus:/philipposaurus
      # Removed api service
      networks:
        default:
          external:
            name: main
        database:
          external:
            name: database
      ```
    - Add a `Dockerfile` in which you put following lines:
      ```dockerfile
      FROM python:3.8.0-slim

      WORKDIR /philipposaurus
      
      COPY ./philipposaurus /philipposaurus
      COPY requirements.txt /philipposaurus
      
      RUN apt upgrade
      
      RUN pip install --upgrade pip
      RUN pip install -r requirements.txt
      
      CMD python /philipposaurus/main.py
      ```
3. Now you can start your container for the first time with
   ```bash
   docker-compose up -d --build
   ```
   Congratulations, now you have you own instance of the philipposaurus bot. Now 
   we are going to do some discord specific things...

---

1. First we have to set some channels like the `reaction_role`-Channel
   ```bash
   .set text <role|rule> <channel>
   # To use this command for voice channels you have to be connected to the channel you want to set
   .set voice <public|private>
   ```
2. After this we set some reaction roles
   ```bash
   .set reaction <add|remove> <rule|role> <emoji> <role>
   ```
   Then your bot is running and also has some settings