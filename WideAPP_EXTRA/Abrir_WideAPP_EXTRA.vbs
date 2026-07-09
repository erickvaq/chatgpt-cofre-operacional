Option Explicit

Dim fso, shell, appDir, pythonw, mainPy, command

Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

appDir = fso.GetParentFolderName(WScript.ScriptFullName)
pythonw = fso.BuildPath(appDir, ".venv\Scripts\pythonw.exe")
mainPy = fso.BuildPath(appDir, "main.py")

If Not fso.FileExists(pythonw) Then
    pythonw = "pythonw.exe"
End If

command = """" & pythonw & """ """ & mainPy & """"
shell.CurrentDirectory = appDir
shell.Run command, 0, False
