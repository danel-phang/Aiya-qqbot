@rem ������к����룬���Ҽ��༭�ű� ���Ϊ ����ѡANSI ����
@echo off
@fsutil dirty query "%systemdrive%" 1>nul 2>nul || (mshta vbscript:CreateObject^("Shell.Application"^).ShellExecute^("""cmd.exe""","/c %~s0",,"runas",1^)^(window.close^)&&exit)
@fsutil dirty query "%systemdrive%" 1>nul 2>nul || (echo ���Ҽ����Թ���Ա������С�&timeout /t 7&exit)
set r=0
set te=8640000
set err=��������
cd /d %~dp0


set apipath=".\unidbg-fetch-qsign"
cd /d %apipath%
rem ������api��װ·�������ű��ɷ����κ�λ�ã��������κε�����������
rem ��һ��������ɾ�������У�����start.bat����api.bat������APIĿ¼���ɣ�


set yunzaipath="..\Miao-Yunzai"
set yunzai=node app
set yunzainame=Miao-Yunzai
rem ���������̵İ�װ·����������ʽ�����ڱ���ǰ׺
if not exist %yunzaipath% echo ���棺�Ҳ������̰�װ·�����Ҽ��༭�ű���������



:auto
call :api
title ���-API������%r%��
set /a r+=1
rem ���� ǩ��API ����¼��־



:log
rem ���30��Сѭ��һ��
timeout /t 30 >nul

:api_st
rem ���API�Ƿ�������
for /f "tokens=2 delims=," %%a in ('tasklist /v /fo csv^|find "API����ر�"') do (
  goto api_log_st
)
set err=API���ˡ�����API��
goto bug

:api_log_st
rem �����־�Ƿ��б���
for /f "delims=" %%a in ('findstr "����: emulate RX@" log.txt') do (
  set err=��־��������API��
  goto bug
)
goto log



:bug
rem �ж�����ʱ���Ƿ����600��
call :time %time1% %time%
if %te% GTR 60000 (
    rem API�쳣��������
    call :off API����ر�
) else (
    rem APIƵ���쳣����������
    set err=%err%�������̡�
    call :off API����ر�
    call :off %yunzainame%
    taskkill /f /t /im node.exe
    timeout /t 20 >nul
    call :miao
)
rem ��ת��auto ��ѭ������api
goto :auto





rem ���� ǩ��API����¼��չʾ����ʱ��
:api
call :off API����ر�
if exist log.txt del /f /q log.txt >nul
del /f /q hs_err_pid* >nul 2>nul
rem ɾ����־
set time1=%time%
echo %date%-%time%-%err%
echo.
echo.
>>logs.txt echo %date%-%time%-%err%
start api.bat
exit /b



rem ���� ָ������
:off
for /f "tokens=2 delims=," %%a in ('tasklist /v /fo csv^|find "%1"') do (
  taskkill /pid %%~a
)
timeout /t 3 >nul
exit /b



rem �ӳ�6����������
:miao
PUSHD %yunzaipath%
start cmd /c "timeout /t 6 & %yunzai%"
POPD
exit /b



rem ����ʱ����λΪ����
rem ���� call :time ʱ��1 ʱ��2
rem ��� %te%
:time
@set ta=%1
@set tb=%2
@if %ta:~1,1%==: @set ta=0%ta%
@if %tb:~1,1%==: @set tb=0%tb%
@set /a tc=1%ta:~0,2%*360000+1%ta:~3,2%*6000+1%ta:~6,2%*100+1%ta:~9,2%-36610100
@set /a td=1%tb:~0,2%*360000+1%tb:~3,2%*6000+1%tb:~6,2%*100+1%tb:~9,2%-36610100
@set /a te=td-tc
@if %te:~,1%==- @set /a te+=8640000
@exit /b
