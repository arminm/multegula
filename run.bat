@echo off
call "cmd /c go run multegula.go config bob"

rem de-facto sleep.  Ping an address that doesn't exist and wait 2000ms.
ping 192.0.2.2 -n 1 -w 2000 > nul

call "cmd /c python3 UI/multegulaUI.py -mid"
pause