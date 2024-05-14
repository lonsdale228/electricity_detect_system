### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/lonsdale228/electricity_detect_system
   ```
2. create .env file in main folder, or just add following variables in environment:
   
   TG_BOT_TOKEN="1234:ABCD"
   
   DATABASE_URL="postgresql+asyncpg://postgres:1111@db:5432/electricity"
   
   POSTGRES_USER="postgres"
   
   POSTGRES_PASSWORD="1111"
   
   POSTGRES_DB="electricity"
   
4. Run project throw Docker Compose
   ```sh
   sudo docker-compose up -d --build
   ```
5. Enjoy!
   
   Access to map: 0.0.0.0:8001
   Access to API: 0.0.0.0:8000
