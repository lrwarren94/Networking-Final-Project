=ABProtocol, developed by Lindsey Warren=

System Requirements:-----------------------
	-Python Version 3 or above
	-Git Bash or other ssh client

Installation instructions:-----------------

WINDOWS
	1. Extract the files in the zip to a directory

UNIX CLUSTER
	1. Using Git Bash or similar ssh client, enter 
	   'ssh username@pwc'. Keep this window
	   open. For the purposes of instructions, we'll call this
	   Window 1.
	2. Open a new Git bash or similar ssh client. Extract the
	   files in the zip to a local directory. Execute the follow-
	   ing commands:
		'scp ABProtocol.py username@pwc:~/'
		'scp client.py username@pwc:~/'
		'scp server.py username@pwc:~/'
		'scp ABProtocol.py username@pwc:~/'
		'cd Test\ Files'
		'scp alice.txt username@pwc:~/'
	   You may now close this window.
	3. In Window 1, execute the following commands:
		'mkdir text_files'
		'mv alice.txt text_files'


Run instructions:----------------------------

WINDOWS
	1. Open two command prompt windows. For the purpose of instruc-
	   tions, we'll call these Window 1 and Window 2.
	2. In Window 1, enter 'python server.py'.
		1. Enter an arbitrary receiver port between 1024 and 
		   65535 (inclusive). I used 5555 for testing.
		2. Enter an arbitrary send port. 
		3. Enter '[install_directory]\Test Files' (without the
		   apostrophes).
		4. Enter '1' (without the apostrophes).
	3. In Window 2, enter 'python client.py'.
		1. Enter 'localhost' (without the apostrophes).
		2. Enter the server receiver port you used in Window 1.
		   I used 5555 for testing.
		3. Enter an arbitrary receiver port. This port must be
		   different than the server's receiver port.
		4. Enter an arbitrary send port. This port must be
		   different than the server's send port.
		5. Enter 'alice.txt' (without the apostrophes).
		6. Enter '1' (without the apostrophes).
	4. At this point, the programs in both winows will execute. You
	   can verify that the file has been saved by checking the 
	   install directory for "alice.txt" and opening it manually.

UNIX CLUSTER
	1. Open two Git Bash or similar ssh client windows. For the
	   purposes of instructions, we'll call these Window 1 and Win-
	   dow 2. 
	2. In Window 1, enter 'ssh n001'.
		1. Enter 'ifconfig'. Copy the IP address.
		1. Enter 'python server.py'.
		2. Enter an arbitrary receiver port between 1024 and 
		   65535 (inclusive). I used 5555 for testing.
		3. Enter an arbitrary send port. 
		4. Enter '/home/[username]/text_files' (without the
		   apostrophes).
		5. Enter '1' (without the apostrophes).
	3. In Window 2, enter 'ssh n002'.
		1. Enter 'python client.py'.
		1. Paste the IP address copied earlier and press enter.
		2. Enter the server receiver port you used in Window 1.
		   I used 5555 for testing.
		3. Enter an arbitrary receiver port. This port must be
		   different than the server's receiver port.
		4. Enter an arbitrary send port. This port must be
		   different than the server's send port.
		5. Enter 'alice.txt' (without the apostrophes).
		6. Enter '1' (without the apostrophes).
	4. At this point, the programs in both winows will execute. You
	   can verify that the file has been saved by checking the 
	   install directory for "alice.txt" and opening it manually by
	   executing the command 'cat alice.txt' while in the 
	   '/home/[username]' directory.