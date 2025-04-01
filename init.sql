-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS orders_db CHARACTER SET utf8mb4 COLLATE utf8mb4_slovak_ci;
USE orders_db;
-- Set proper character set and collation
ALTER DATABASE orders_db CHARACTER SET utf8mb4 COLLATE utf8mb4_slovak_ci;
-- Set session variables
SET NAMES utf8mb4;
SET character_set_client = utf8mb4;
SET character_set_connection = utf8mb4;
SET character_set_results = utf8mb4;