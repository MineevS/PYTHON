# The is script for server aiohttp python

# Request demonstration "GET' (Получение информации): (status: Ok [Все хорошо])

Write-Host -Object "Получение информации:" -ForegroundColor Red

    Invoke-WebRequest -Method 'GET' -Uri "http://localhost:8080/labs/"                                                                           # print current content of dict-python.

    # [System.Threading.Thread]::Sleep(1000)                                                                                                     # one second delay.

    # Request demonstration "POST' (Создание):  (status: Created [Создано])


Write-Host -Object "Создание lab1:" -ForegroundColor Yellow

    Invoke-WebRequest -Method 'POST' -Uri "http://localhost:8080/labs"                                                                            # 


Write-Host -Object "Получение информации:" -ForegroundColor Red

    Invoke-WebRequest -Method 'GET' -Uri "http://localhost:8080/labs/"

# Write-Host -Object "Создание labVector:" -ForegroundColor Yellow

    # Invoke-WebRequest -Method 'POST' -Uri "http://localhost:8080/labs/labVector"                                                                  # 


# Write-Host -Object "Создание labString:" -ForegroundColor Yellow

    # $Body = @{"Deadline" = "12.11.2023"; "Dectination" = "Impl Vec 3"; "ListStudy" = "Ivanov I. I."}

    # Invoke-WebRequest -Method 'POST' -Uri "http://localhost:8080/labs/labString" -Body ($Body|ConvertTo-Json) -ContentType "application/json"     # 


Write-Host -Object "Внесение информации в lab1 (Добавление):" -ForegroundColor Green

    $Body = @{"DeadLine" = "12.11.2023"; "Dectination" = "Impl Vec 3"; "ListStudy" = "Ivanov I. I."}

    # Request demonstration "PUT' (Изменение): (status: Accepted [Принято])

    Invoke-WebRequest -Method 'PUT' -Uri "http://localhost:8080/labs/lab1" -Body ($Body|ConvertTo-Json) -ContentType "application/json"           # 


# Write-Host -Object "Получение информации:" -ForegroundColor Red

    # Invoke-WebRequest -Method 'GET' -Uri "http://localhost:8080/labs/"                                                                         # print current content of dict-python.


#Write-Host -Object "Изменение информации в lab1 (Перезапись 1):" -ForegroundColor Green

    #$Body = @{"Deadline" = "12.11.2023"}

    #Invoke-WebRequest -Method 'PUT' -Uri "http://localhost:8080/labs/lab1/" -Body ($Body|ConvertTo-Json) -ContentType "application/json"         # 


# Write-Host -Object "Получение информации:" -ForegroundColor Red

    # Invoke-WebRequest -Method 'GET' -Uri "http://localhost:8080/labs/lab1"                                                                     # print current content of dict-python of lab1.


Write-Host -Object "Изменение информации в lab1 (Перезапись 2):" -ForegroundColor Green

    $Body = @{"ListStudy" = ("Ivanov I. N.", "Sidorov S. D.", "Kolokolcev M. I.")}

    Invoke-WebRequest -Method 'PUT' -Uri "http://localhost:8080/labs/lab1/" -Body ($Body|ConvertTo-Json) -ContentType "application/json"          # 


Write-Host -Object "Попытка получить доступ к несуществующей lab2:" -ForegroundColor Red

    Invoke-WebRequest -Method 'GET' -Uri "http://localhost:8080/labs/lab2"                                                                       # lab2 not find.


Write-Host -Object "Создание lab2:" -ForegroundColor Yellow

    Invoke-WebRequest -Method 'POST' -Uri "http://localhost:8080/labs"                                                                           # lab2 create.

    # Invoke-WebRequest -Method 'GET' -Uri "http://localhost:8080/labs/"                                                                         # print current content of dict-python.


Write-Host -Object "Повторная попытка получить доступ к уже существующей lab2:" -ForegroundColor Red

    Invoke-WebRequest -Method 'GET' -Uri "http://localhost:8080/labs/lab2"                                                                       # 


Write-Host -Object "Удаление информации из lab1:" -ForegroundColor Gray

    # Request demonstration "DELETE' (Удаление):

    $Body = ("Dectination")

    Invoke-WebRequest -Method 'DELETE' -Uri "http://localhost:8080/labs/lab1" -Body  ($Body|ConvertTo-Json) -ContentType "application/json"     # delete field 'Dectination' fron lab1!


Write-Host -Object " Попытка удаление несуществующих полей информации из lab1:" -ForegroundColor Gray

    # Request demonstration "DELETE' (Удаление):

    $Body = ("Dectination")

    Invoke-WebRequest -Method 'DELETE' -Uri "http://localhost:8080/labs/lab1" -Body  ($Body|ConvertTo-Json) -ContentType "application/json"     # 


Write-Host -Object "удаление конкретных данных по ключу из lab1:" -ForegroundColor Gray

    $Body = @{"ListStudy" = ("Ivanov I. I.", "Sidorov S. D.")}

    Invoke-WebRequest -Method 'DELETE' -Uri "http://localhost:8080/labs/lab1" -Body  ($Body|ConvertTo-Json) -ContentType "application/json"     # 


Write-Host -Object "удаление всей lab1:" -ForegroundColor Gray

    Invoke-WebRequest -Method 'DELETE' -Uri "http://localhost:8080/labs/lab1"                                                                   # 


Write-Host -Object "Получение информации:" -ForegroundColor Red

    Invoke-WebRequest -Method 'GET' -Uri "http://localhost:8080/labs/"                                                                          # print current content of dict-python.
