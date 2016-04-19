rem ###########################################################
rem #Multegula - run.bat                                      #
rem #Main Driver/Startup Script for Multegula for Windows     #
rem #Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He#
rem ###########################################################

@echo off
START /B CMD /C CALL "cmd /c go run multegula.go -uiport=44444 -gameport=11111"
rem de-facto sleep.  Ping localhost and wait 4s.
ping 127.0.0.1 -n 4 > nul
python.exe UI/multegulaUI.py 44444
pause