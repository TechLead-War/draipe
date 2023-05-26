1. Start the service by -
     sanic service:app --debug --reload

2. Please do not install the latest version of dependencies, there are several 
   models which won't work with the current code.


________________________________________
PR Guidlines

1. don't use git commit -m "commit message". Instead use, "git commit" and 
   mention title as well as message.
2. commits should be squashed and rebase with the commit, there should not 
   be history, small sub-commits or fixup commits.