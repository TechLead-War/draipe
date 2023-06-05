1. Start the service by -
    python3 -m venv <myenv>
     pip install -r requirements.txt 
     dbmate -u 'postgres://<db_user>:<db_pass>@localhost:<port>/<db_name>?sslmode=disable' up
     sanic service:app --debug --reload

2. Please do not install the latest version of dependencies, there are several 
   models which won't work with the current code.

3. If you import any dependency in the file, then please use. isort 
   <file_name> this will sorts those imports.
________________________________________
PR Guidelines

1. Don't use git commit -m "commit message". Instead, use, "git commit" and 
   mention title as well as message.
2. commits should be squashed and rebase with the commit, there should not 
   be history, small sub-commits or fixup commits.
3. Don't use git add . (please use, git add -u) and verify after adding if 
   all correct files are tracked.