# PRNIoTlet

This project should result in small python scripts, which use a thermo printer to print out different information/images etc.

The main entry point is the prniotlet-server. The server offers the
functionality to print raw data. You have to request a session id before starting to print.

To print all at once, you can use the class PrnIOTlet. This sets up a dummy printer class. When you are finished with composing the print, you can call the final printing, which will send the whole data at once to the print-server.
