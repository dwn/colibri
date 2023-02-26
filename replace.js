function generalInPlaceArrayFunction(arr, func, onlyIndex=-1) { for(const i in arr) if (Array.isArray(arr[i])) generalInPlaceArrayFunction(arr[i], func, onlyIndex); else if (onlyIndex<0 || i==onlyIndex) arr[i] = func(arr[i]); }
function addEscaping(arr, onlyIndex=-1) { generalInPlaceArrayFunction(arr, (s) => { let r = ''; for(const c of s) { r = r.concat('\\',c); } return r; }, onlyIndex); }
function removeEscaping(arr, onlyIndex=-1) { generalInPlaceArrayFunction(arr, (s) => { return s.replaceAll('\\',''); }, onlyIndex); }
function symbolizeWhitespace(arr) { return generalInPlaceArrayFunction(arr, (s) => { return '_🛑_' + s.replace(/\n/g,'_⚠_').replaceAll(' ','_') + '_🛑_'; }); }
function restoreWhitespace(arr) { return generalInPlaceArrayFunction(arr, (s) => { return s.replaceAll('_🛑_','').replaceAll('_🛑','').replaceAll('🛑_','').replaceAll('🛑','').replaceAll('_⚠_','\n').replaceAll('_⚠','\n').replaceAll('⚠_','\n').replaceAll('⚠','\n').replaceAll('_',' '); }); }
function loadReplaceMap(strArrReplacementMap, section) { //Returns arrReplace[numLines][numPairsOnLine][2]
  let r = strArrReplacementMap.split(/\r?\n/g).map(e => e.trim()).filter((line) => { return line; });
  for(const j in r) { r[j] = r[j].split(/\s+/g); for(const i in r[j]) r[j][i] = r[j][i].split(','); }
  for(let iLine = 0, iCurrSection = -1; iLine<r.length; iLine++) { //Populates section
    if (r[iLine].length==1 && r[iLine][0][0]==='====SECTION') {
      iCurrSection++;
      section[r[iLine][0][1]] = { index: iCurrSection, firstLine: iLine }; //Section format {index: N, firstLine: N}
    }
  }
  if (!section.MAIN) section.MAIN = { index: 0, firstLine: -1 };
  addEscaping(r,0); //Arg 0 means only lefthand side of each pair is escaped
  return r;
}
function runReplacementScript(arrPage, iPage=0, arrReplace, section) {
  symbolizeWhitespace(arrPage, iPage)
  addEscaping(arrPage, iPage);
  if (!(section && section.MAIN)) return;
  let iLine = 0;
  let iLineSaved = 0;
  for(iLine=section.MAIN.firstLine+1; iLine<arrReplace.length; iLine++) { //Runs main section
    if (arrReplace[iLine].length==1 && arrReplace[iLine][0][0].split('\\-')[0]==='\\=\\=\\=\\=\\R\\U\\N') { //Potentially jumps to another section
      const numRepetitions=arrReplace[iLine][0][0].split('\\-')[1].replaceAll('\\','');
      if (!numRepetitions) numRepetitions = 1;
      const sectionTitle = arrReplace[iLine][0][1];
      iLineSaved = iLine;
      for(let i=0; i<numRepetitions; i++) { //Loops over section
        const nextSectionTitle = Object.keys(section).find(key => section[key].index==section[sectionTitle].index+1);
        for(iLine=section[sectionTitle].firstLine+1; iLine<section[nextSectionTitle].firstLine; iLine++)
          for(const iPairOnLine of arrReplace[iLine])
            arrPage[iPage] = arrPage[iPage].replaceAll(iPairOnLine[0],iPairOnLine[1]);
      }
      iLine = iLineSaved+1;
    }
    for(const iPairOnLine of arrReplace[iLine]) //Runs main section again
      arrPage[iPage] = arrPage[iPage].replaceAll(iPairOnLine[0],iPairOnLine[1]);
  }
  removeEscaping(arrPage, iPage);
  restoreWhitespace(arrPage, iPage);
}
let url = 'https://dwn.github.io/common/lang/itlani.svg';
let iPage = 0;
let result = { graph: { text: {}, arrReplace: {}, section: {} }, phone: { text: {}, arrReplace: {}, section: {} } };
let data;
fetch(url).then(function(response) {
  response.text().then(function(text) {
    data = text.split('<desc>')[1].split('</desc>')[0];
    try { data = JSON.parse(data); } catch { return result; }

    result.graph.arrReplace = loadReplaceMap(data['grapheme-map'], result.graph.section);
    result.phone.arrReplace = loadReplaceMap(data['phoneme-map'], result.phone.section);

    if (!Array.isArray(result.graph.text = data['user-text'])) result.graph.text = [result.graph.text];
    if (!Array.isArray(result.phone.text = data['user-text'])) result.phone.text = [result.phone.text];

    runReplacementScript(result.graph.text, iPage, result.graph.arrReplace, result.graph.section);
    runReplacementScript(result.phone.text, iPage, result.phone.arrReplace, result.phone.section);

    console.log(result);
  });
});
