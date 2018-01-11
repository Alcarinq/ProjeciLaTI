@set CONFIG_FILE=./development.ini
@set PYRAMID_PORT=6001

@title "Pyramid DEV server on port %PYRAMID_PORT% using configuration from %CONFIG_FILE%"
START /High /B CMD /C CALL env\Scripts\pserve --reload %CONFIG_FILE% http_port=%PYRAMID_PORT%

pause