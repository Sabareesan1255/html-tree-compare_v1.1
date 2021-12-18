## Inspiration

- We see a lot of files under the structured document, which is iteratively worked and updated to a final document. Wondered how google sheets can maintain the history of each cell, document changes. Since this problem statement is relevant to the bigger picture, we thought of taking this one.

## What it does

- Given a File A and File B of type HTML, the project will generate a document tree for visualization at tag level, a document comparison window, and the similarity score.

## How we built it
- It's built with help of electron js, python, some plugins.
- Input and visualizations are done with HTML, electron and for comparison, we have used python to generate JSON structure from the HTML.
- Output is generated and displayed on the electron js window.
## Challenges we ran into
- Creating the logical rules for comparing and generating structural nodes
- Visual representation of the HTML tree
- Finding the similarity score
## Accomplishments that we're proud of
- Generating JSON from input HTML
- N level node traversal and retrieval

## What we learned

## What's next for Untitled
- To try to implement for any structured document type and to enhance matching techniques

