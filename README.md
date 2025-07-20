# To Get Started
## Clone the repo
> Go into anyfolder open a cmd/shell/git bash (I recommend using git bash)

```bash
git clone https://github.com/FakeandrewA/StoryBookGenerator.git
```
```bash
cd StoryBookGenerator
```

## Creating Your feature branch to write your features
> first pull any latest changes(standard procedure to makesure you have the proper baseline)

```bash
git checkout main
```
```bash
git pull origin main
```
> then, to create your feature branch

```bash
git checkout -b feature/some-task-name
```
(follow this naming convention)

> now your are working on our branch any changes made will be saved to this branch
  this will make sure that our main branch is safe
  after some changes or even without changes

```bash
git add --all
```
```bash
git commit -m "your message"
```
```bash
git push origin feature/some-task-name
```
#(note: this should be your branch name)

> now you can see your feature branch in the main repo

## Opening a pull Request
> we will pull and merge the code to test-main branch then do a integration test
  then do a final pull request to main branch , successfuly versioning our project to its next level


# DO THIS
> go to api.together.xyz and create a api key and copy paste it in the .env.example
> then go to groq.com and create a api key and copy paste it in the .env.example
> rename the .env.example -> .env
> then activate the venv
```bash
source venv/Scripts/activate
```
```bash
pip install -r requirements.txt
```

# How To Use This bookGenerator

```python
from .storybookagent.graph import bookGenerator
book = bookGenerator.invoke({"userPrompt":"<prompt>","userId":request.user.id})
```

## returns:
## a dictionary with these attributes
##
## book["userPrompt"] -> str
## book["story"] -> Story object
##                          \___>> book["story"].title -> str
##                           \___>> book["story"].characterDescription -> str
##                            \___>> book["story"].story -> str
##                             \___>> book["story"].oneline -> str
##                              \___>> book["story"].style -> str
##                               \___>> book["story"].numOfScenes -> int
## book["scenes"] -> Scenes object
##                            \___>> book["scenes"].scenes -> list[str]
##                             \___>> book["scenes"].voiceovers -> list[str]
##
## book["grade"] -> str
## book["userId"] -> int 


##### for more details go to storybookagent/schemas.py to read more , also checkout storybookagent