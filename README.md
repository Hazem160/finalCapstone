# Final Capstone project

This is the last project that combines all together the application of lists, functions, string handling and file I/O. As the name might entail, it essentially manages tasks that are being assigned to users that first need to be logged in using simple data handling comparisons of username and password. The initial user that does not require registration is the admin.

Upon successfully logging in, the user can choose to either:
  - registering a user
  - adding a task (assignment is not limited to currently logged-in user)
  - viewing all tasks
  - viewing only the tasks assigned to the current user
  - generating reports 
  - displaying general statistics (number of users and overall tasks).
    
The program does not allow:

  ❌ adding tasks to non-registered users<br>
  ❌ permitting the same username registration<br>
  ❌ unsupported date format (only format allowed is YYYY-MM-DD)
  
# Deployment requirements

It doesn't require any arduous prerequisites for running the program. It only uses Python and text files for saving tasks, users and any changes that may be issued. These are the modules used for the program:
  - os
  - datetime 
