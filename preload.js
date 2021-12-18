let child_process = require("child_process");
let { contextBridge } = require("electron");
const fs = require("fs");
const path = require("path");

// All of the Node.js APIs are available in the preload process.
// It has the same sandbox as a Chrome extension.
window.addEventListener("DOMContentLoaded", () => {
  const replaceText = (selector, text) => {
    const element = document.getElementById(selector);
    if (element) element.innerText = text;
  };

  for (const type of ["chrome", "node", "electron"]) {
    replaceText(`${type}-version`, process.versions[type]);
  }

  if(process.platform=="darwin"){
    document.getElementById("pySelect").selectedIndex = 1;
  }

});

let saveAndProcessJson = (fileContentA, fileContentB, pythonPath) => {
  let savePathA = path.join(__dirname, "./assets/cmpA.html");
  let savePathB = path.join(__dirname, "./assets/cmpB.html");
  let pyScriptPath = path.join(__dirname, "./assets/compareDiff.py");

  let readPathA = path.join(__dirname, "./assets/dataA.json");
  let readPathB = path.join(__dirname, "./assets/dataB.json");

  try {
    fs.unlinkSync(readPathA);
    fs.unlinkSync(readPathB);
    //file removed
  } catch (err) {
    console.error(err);
  }

  fs.writeFileSync(savePathA.toString(), fileContentA, function (err) {
    if (err) throw err;
    console.log("Saved!");
  });
  fs.writeFileSync(savePathB.toString(), fileContentB, function (err) {
    if (err) throw err;
    console.log("Saved!");
  });

  let processCmd = pythonPath + " " + pyScriptPath + " " + savePathA + " " + savePathB + " 0";

  // console.log(processCmd);

  let output = child_process.execSync(processCmd).toString().trim();

  console.log("Done generation");

  retAr = [];

  try {
    let data = fs.readFileSync(readPathA, "utf8");
    // console.log(data);

    retAr.push(JSON.parse(data));

    let data1 = fs.readFileSync(readPathB, "utf8");
    // console.log(data1);
    retAr.push(JSON.parse(data1));
  } catch (err) {
    console.error(err);
  }

  

  return retAr;
};

contextBridge.exposeInMainWorld("api", { saveAndProcessJson });
