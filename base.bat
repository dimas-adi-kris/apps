set PATH=%PATH%;C:\Users\dimas\Anaconda3\Scripts
%windir%\system32\cmd.exe "/K" C:\Users\dimas\Anaconda3\Scripts\activate.bat base

%windir%\system32\cmd.exe "/k" echo set FLASK_APP=run.py 
%windir%\system32\cmd.exe "/k" echo set FLASK_ENV=production 
%windir%\system32\cmd.exe "/k" flask run
