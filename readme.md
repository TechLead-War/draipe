1. Start the service by -
     pip install -r requirements.txt
     sanic service:app --debug --reload

2. Please do not install the latest version of dependencies, there are several 
   models which won't work with the current code.


________________________________________
PR Guidelines

1. Don't use git commit -m "commit message". Instead, use, "git commit" and 
   mention title as well as message.
2. commits should be squashed and rebase with the commit, there should not 
   be history, small sub-commits or fixup commits.
3. Don't use git add . (please use, git add -u) and verify after adding if 
   all correct files are tracked.