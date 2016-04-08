@echo off
START /B CMD /C CALL "go run multegula.go config bob"

rem de-facto sleep.  Ping localhost and wait 2s.
ping 127.0.0.1 -n 2 > nul

START /B CMD /C CALL "python3 UI/multegulaUI.py -mid"
pause