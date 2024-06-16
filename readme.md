Better Logged out Reddit
------------------------

A suite of tweaks to make the logged out reddit homepage more bearable.

Blocks domains, subreddits, and keywords.  Simplifies the UI by hiding
most of it.  Blocks ragebait.


## Installing

 - Install the [tampermonkey](https://www.tampermonkey.net/) addon.
   + Create a new script, and paste in the contents of reddit.js
 - Install [ollama](https://ollama.com/)
   + `$ ollama pull llama3`
   + `$ ollama serve`
     - I'm pretty sure you need to do this manually
   + ollama should be running on port 11434 (default)
 - Run python server (in this directory)
   + `$ virtualenv venv`
   + `$ venv/bin/pip install -r requirements.txt`
   + `$ venv/bin/flask --app llm_cache_server run --host=0.0.0.0 --with-threads`
 - Either go to old.reddit.com manually, or install
   [Old Reddit Redirect addon](https://github.com/tom-james-watson/old-reddit-redirect)
