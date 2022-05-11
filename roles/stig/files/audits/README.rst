POSIX if-Statements and functions for Bash-based Audits
=======================================================

-a    file exists.
-b    file exists and is a block-special file.
-c    file exists and is a character-special file.
-d    file exists and is a directory.
-e    file exists.
-f    file exists and is a regular file.
-G    file exists and is owned by the effective group ID.
-g    file exists and its SGID bit is set.
-h    file exists and is a symbolic link.
-k    file exists and its sticky bit is set.
-L    file exists and is a symbolic link.
-N    file exists and has been modified since it was last read.
-n    string is not empty.
-O    file exists and is owned by the effective user ID.
-p    file exists and is a named pipe (FIFO).
-r    file exists and is readable.
-s    file exists and has a size greater than zero.
-S    file exists and is a socket.
-t    file descriptor FD is open and refers to a terminal.
-u    file exists and its SUID (set user ID) bit is set.
-w    file exists and is writable.
-x    file exists and is executable.
-z    string is empty.

* calling a func in if:   ``if func; then cmd1; else cmd2; fi (cmd1 executes if func returns 0 (= success))``
* simple string-compare:  ``if [ "$(func)" == "value" ]; then ...; fi``
* contains string:        ``if [[ "$MYVAR" == *"mystring"* ]]; then ...; fi``
* compare on integer:     ``if [ $(func) -le 99 ]; then ...; fi``
