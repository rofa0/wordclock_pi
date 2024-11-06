function CreateVenv {
    $PythonVersion = py --version   
	Write-Host "Creating virtual environment with $PythonVersion..." -ForegroundColor green
	py -m venv venv
	venv/Scripts/activate
    py -m pip install --upgrade pip setuptools
	Write-Host ""
}

function InstallRequirements{
	Write-Host "Installing 'requirements.txt'..." -ForegroundColor green
    pip install -r requirements.txt
    Write-Host ""
}


function VenvExists{
	$caption = "Virtual environment already exists!"
	$message = "Do you want to update the virtual environment:"
	[int]$defaultChoice = 0
	$yes = New-Object System.Management.Automation.Host.ChoiceDescription "&Yes", "Delete venv and create new one, update pip"
	$no = New-Object System.Management.Automation.Host.ChoiceDescription "&No", "Continue without changing venv"
	$options = [System.Management.Automation.Host.ChoiceDescription[]]($yes, $no)
	$choiceRTN = $host.ui.PromptForChoice($caption,$message, $options,$defaultChoice)
	if ( $choiceRTN -ne 1 ){
	   # choice was yes --> delete venv, create new venv, update pip
		Get-childItem venv -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
		CreateVenv
		}
	else{venv/Scripts/activate}
}


$ep = Get-ExecutionPolicy

if ($ep -eq 'RemoteSigned'){

    $EnvPath = Join-Path $PSScriptRoot "\venv"
    # check if venv exists
    if (Test-Path -Path $EnvPath){
		VenvExists
		}
    else{
		CreateVenv
		}

    if (Test-Path "requirements.txt" -PathType leaf){
		InstallRequirements
		}
    else{ 
		Write-Host "'requirements.txt' not found!" -ForegroundColor red -BackgroundColor black
		}
	
        
	Write-Host "Done" -ForegroundColor green
} 
else {
    Write-host "Execution Policy does not allow this script to run properly" -ForegroundColor red
    Write-host "If you have the proper permissions," -ForegroundColor red
    Write-Host "Please close powershell," -ForegroundColor red
    Write-host "then right click the powershell icon and run as administrator" -ForegroundColor red
    Write-host "Once in the powershell environment, execute the following:" -ForegroundColor red
    Write-host "Set-ExecutionPolicy RemoteSigned -Force" -ForegroundColor red
}


