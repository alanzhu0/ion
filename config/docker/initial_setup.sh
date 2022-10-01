#!/bin/sh
echo "Generating development data..."

echo "Copying create user script..."
cp config/create-users.py .

echo "Creating development users..."
python3 create-users.py -a admin
python3 create-users.py -s student student1 student2 student3 2030student 2029student 2028student 2027student 2026student 2025student 2024student 2023student
python3 create-users.py -t teacher teacher1 teacher2 teacher3

echo "Creating imported users..."
python3 manage.py import_users config/data/outputs/user_import.json

echo "Creating eighth period blocks..."
python3 manage.py dev_create_blocks 12/31/2030

echo "Creating eighth period activities..."
python3 manage.py import_eighth config/data/outputs/eighth_import.json

echo "Data generation complete."