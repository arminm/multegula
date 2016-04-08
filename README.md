# Multegula [![Build Status](https://travis-ci.org/arminm/multegula.svg?branch=master)](https://travis-ci.org/arminm/multegula)

Multiplayer Distributed Brick Gaming  
18-842, Spring 2016, Carnegie Mellon University  
Armin Mahmoudi, Daniel Santoro, Garrett Miller, Lunwen He

Installing:
---------------------------------------------------------
Dependencies Required:  
* Go 1.6 (or greater)  
* Python 3.5.1 (or greater)
* python3-tk
* git (for installation)

#### OS X 10.10 or Newer (using Homebrew):  
```bash
brew install python3 golang git  
mkdir -p ~/go/src/github.com/arminm/  
cd ~/go/src/github.com/arminm/  
git clone https://github.com/arminm/multegula.git
export GOPATH=$HOME/go  
cd multegula/
```

#### Ubuntu Linux 16.04 LTS:  
```bash
sudo apt-get install python3-tk golang git  
mkdir -p ~/go/src/github.com/arminm/  
cd ~/go/src/github.com/arminm/  
git clone https://github.com/arminm/multegula.git  
export GOPATH=$HOME/go
cd multegula/
```

#### Windows 7 or Newer:  
```
Install Go 1.6 - https://golang.org/dl/
Install Python 3.5.1 (includes pip) - https://www.python.org/downloads/
	BE SURE TO CHECK "Add Python 3.5 to PATH"
Open a command prompt and run the following: 
	mkdir C:\Go\src\github.com\arminm\multegula\
Download Multegula and unzip contents of: https://github.com/arminm/multegula/archive/master.zip
	into C:\Go\src\github.com\arminm\multegula\
Click "Allow" on any Windows Firewall notifications upon running.
```

Running:
---------------------------------------------------------
1. ./run.sh (OS X, Linux) or click run.bat (Windows)

Acknowledgements:
---------------------------------------------------------
Dr. Bill Nace, Mayank Shishodia, and the teaching staff of 18-842,
Distributed Systems, at Carnegie Mellon University, Spring 2016.
