function generalInPlaceArrayFunction(arr, func, onlyIndex=-1) { for(const i in arr) if (Array.isArray(arr[i])) generalInPlaceArrayFunction(arr[i], func, onlyIndex); else if (onlyIndex<0 || i==onlyIndex) arr[i] = func(arr[i]); }
function addEscaping(arr, onlyIndex=-1) { generalInPlaceArrayFunction(arr, (s) => { let r = ''; for(const c of s) { r = r.concat('\\',c); } return r; }, onlyIndex); }
function removeEscaping(arr, onlyIndex=-1) { generalInPlaceArrayFunction(arr, (s) => { return s.replaceAll('\\',''); }, onlyIndex); }
function symbolizeWhitespace(arr) { return generalInPlaceArrayFunction(arr, (s) => { return '_🛑_' + s.replace(/\n/g,'_⚠_').replaceAll(' ','_') + '_🛑_'; }); }
function restoreWhitespace(arr) { return generalInPlaceArrayFunction(arr, (s) => { return s.replaceAll('_🛑_','').replaceAll('_🛑','').replaceAll('🛑_','').replaceAll('🛑','').replaceAll('_⚠_','\n').replaceAll('_⚠','\n').replaceAll('⚠_','\n').replaceAll('⚠','\n').replaceAll('_',' '); }); }
function initData(url) { fetch(url).then((res) => { res.text().then((text) => { try { data = JSON.parse(text.split('<desc>')[1].split('</desc>')[0]); } catch {} }); }); }
/////////////////////////////////////////////////
function initReplace_inner(strArrReplacementMap, section) { //Returns arrReplace[numLines][numPairsOnLine][2]
  let r = strArrReplacementMap.split(/\r?\n/g).map(e => e.trim()).filter((line) => { return line; });
  for(const j in r) { r[j] = r[j].split(/\s+/g); for(const i in r[j]) r[j][i] = r[j][i].split(','); }
  for(let iLine = 0, iCurrSection = -1; iLine<r.length; iLine++) { //Populates section
    if (r[iLine].length==1 && r[iLine][0][0]==='====SECTION')
      section[r[iLine][0][1]] = { index: ++iCurrSection, firstLine: iLine }; //Section format {index: N, firstLine: N}
  }
  if (!section.MAIN) section.MAIN = { index: 0, firstLine: -1 };
  addEscaping(r,0); //Arg 0 means only lefthand side of each pair is escaped
  return r;
}
function initReplace(result, data) {
  result.graph.arrReplace = initReplace_inner(data['grapheme-map'], result.graph.section);
  result.phone.arrReplace = initReplace_inner(data['phoneme-map'], result.phone.section);
  result.font.arrCode = data['font-code'].split('\n');
  arrPage = data['user-text'].split('{br}\n');
}
function runReplace_inner(arrPage, iPage=0, arrReplace, section) {
  symbolizeWhitespace(arrPage, iPage)
  addEscaping(arrPage, iPage);
  if (!(section && section.MAIN)) return;
  for(let iLineSaved, iLine=section.MAIN.firstLine+1; iLine<arrReplace.length; iLine++) { //Runs main section
    if (arrReplace[iLine].length==1) {
      const hyphenSplit = arrReplace[iLine][0][0].replaceAll('\\','').split('-');
      if (hyphenSplit[0]==='====RUN') { //Jumps to another section
        const numRepetitions = hyphenSplit[1] || 1;
        const sectionTitle = arrReplace[iLine][0][1];
        iLineSaved = iLine;
        for(let i=0; i<numRepetitions; i++) { //Loops over section
          const nextSectionTitle = Object.keys(section).find(key => section[key].index==section[sectionTitle].index+1);
          for(iLine=section[sectionTitle].firstLine+1; iLine<section[nextSectionTitle].firstLine; iLine++)
            for(const pairOnLine of arrReplace[iLine]) //Runs a line of section
              arrPage[iPage] = arrPage[iPage].replaceAll(pairOnLine[0], pairOnLine[1]);
        }
        iLine = iLineSaved+1;
      }
    }
    for(const pairOnLine of arrReplace[iLine]) //Runs a line of main
      arrPage[iPage] = arrPage[iPage].replaceAll(pairOnLine[0], pairOnLine[1]);
  }
  removeEscaping(arrPage, iPage);
  restoreWhitespace(arrPage, iPage);
}
function runReplace(result, arrPage, iPage=0) {
  result.page = iPage;
  result.text = [arrPage[iPage]];
  result.graph.text = [arrPage[iPage]];
  result.phone.text = [arrPage[iPage]];
  runReplace_inner(result.graph.text, 0, result.graph.arrReplace, result.graph.section);
  runReplace_inner(result.phone.text, 0, result.phone.arrReplace, result.phone.section);
}
let data, arrPage, result = { font: {}, graph: { section: {} }, phone: { section: {} } };
initData('https://dwn.github.io/common/lang/ignota.svg')
setTimeout(() => {
  initReplace(result, data);
  runReplace(result, arrPage, 1);
  console.log(result);
  console.log(data);
}, 2000);
