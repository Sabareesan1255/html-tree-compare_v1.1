# Project Name: Group / Classify Documents Comparison Based on Structure 

## Project details
### Project Scope
 - HTML/XML Documents comparision.
 - Node and attribute comparision based on the node level configuration
 - Node, attribute and text comparision
 - Compare and merge documents
 
### S/W Requirements

- python 3.8 or above
- node v12 or above (tested on v12)

### Tech stack

- Electron JS
- python
- javascript/jquery (plugins)

### Pre-requisites

- 1st step is to install the dependencies required for python, the dependencies are available in the `/assets/requirements.txt` in the project folder
- install the dependencies using the command via terminal/cmd `pip install -r <path_to_requirements.txt>`
- navigate to the project directory and open up a terminal/cmd and run the following command to install node dependencies, `npm i`
- once the above are installed, run the following command to open the project. `npm start`

### Process execution

- By now a window will be opened and there will be two textarea's available for inputting the HTML/XML code.
- Once the code is pasted, select the python command relevant to your `OS`, say for windows it will be `python` and for Mac/Linux it will be `python3`. Select the value from the dropdown and click on compare to process.
- Now the JSON creation will run in the backend and the visual/document tree will be displayed along with the comparisons on the screen.
- The tree levels/depth can be controlled using the document levels slider.
- On the comparison end we have tried to compare node-based and child-based traversal and have found the differences.
- Javascript plugin included as an addon features for entire document comparision and merging the documents.

### Troubleshooting

- If any issues are encountered or comparison isn't occurred, it's pretty easy to find the area you can toggle developer tools by `ctrl+shift+i` or `cmd+option+i` on mac.
- The scenario where the process may fail is when python is not configured properly on the system.
