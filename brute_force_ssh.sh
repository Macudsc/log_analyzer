#!/bin/bash

# Настройки
HOST="localhost"        # или другой IP
USER="moon"             # существующий пользователь
WRONG_PASSWORD="wrongpassword123"
TRIES=10                # количество попыток

echo "Начинаем $TRIES попыток подключения к $USER@$HOST..."

for i in $(seq 1 $TRIES)
do
    echo "[Попытка $i] Подключение к $HOST..."
    sshpass -p "$WRONG_PASSWORD" ssh -o StrictHostKeyChecking=no -o NumberOfPasswordPrompts=1 $USER@$HOST "echo 'Подключение успешно'; exit"
    
    if [ $? -eq 0 ]; then
        echo "Успешное подключение!"
        break
    else
        echo "Неудачная попытка #$i"
    fi
    
    sleep 1
done

echo "Эксперимент завершён."