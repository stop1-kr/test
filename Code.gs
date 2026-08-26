/**
 * 삼각비의 활용 - 삼각측량과 GPS 학습지  응답 저장용 Google Apps Script
 * ---------------------------------------------------------------
 * 1) 구글 스프레드시트를 새로 만들고, 주소창의 /d/ 와 /edit 사이 문자열을 SHEET_ID 에 붙여 넣습니다.
 * 2) 확장 프로그램 > Apps Script 를 열고 이 코드를 붙여 넣습니다.
 * 3) 배포 > 새 배포 > 유형 [웹 앱]
 *      - 실행 계정      : 나
 *      - 액세스 권한    : 모든 사용자
 *    배포 후 나오는 /exec 로 끝나는 주소를 index.html 의 GAS_URL 에 붙여 넣습니다.
 * ---------------------------------------------------------------
 */

var SHEET_ID   = '여기에_스프레드시트_ID를_붙여넣으세요';
var SHEET_NAME = '응답';

function doGet(e) {
  var p = (e && e.parameter) ? e.parameter : {};
  var out;
  try {
    if (p.action === 'load') {
      out = { ok: true, data: loadRow_(p.sid, p.name) };
    } else {
      out = { ok: true, msg: 'ready' };
    }
  } catch (err) {
    out = { ok: false, error: String(err) };
  }
  var json = JSON.stringify(out);
  if (p.callback) {
    return ContentService.createTextOutput(p.callback + '(' + json + ')')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(json)
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  var out;
  try {
    var body = JSON.parse(e.postData.contents);
    if (!body.sid || !body.name) throw new Error('학번과 이름이 없습니다.');
    saveRow_(body);
    out = { ok: true, msg: '저장 완료' };
  } catch (err) {
    out = { ok: false, error: String(err) };
  }
  return ContentService.createTextOutput(JSON.stringify(out))
    .setMimeType(ContentService.MimeType.JSON);
}

function sheet_() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(['학번', '이름', '저장시각', '응답(JSON)']);
  }
  return sh;
}

function findRow_(sh, sid, name) {
  var v = sh.getDataRange().getValues();
  var a = String(sid).trim(), b = String(name).trim();
  for (var i = 1; i < v.length; i++) {
    if (String(v[i][0]).trim() === a && String(v[i][1]).trim() === b) return i + 1;
  }
  return -1;
}

function saveRow_(b) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var sh = sheet_();
    var r = findRow_(sh, b.sid, b.name);
    var row = [String(b.sid), String(b.name), new Date(), JSON.stringify(b.answers || {})];
    if (r > 0) sh.getRange(r, 1, 1, 4).setValues([row]);
    else sh.appendRow(row);
  } finally {
    lock.releaseLock();
  }
}

function loadRow_(sid, name) {
  if (!sid || !name) return null;
  var sh = sheet_();
  var r = findRow_(sh, sid, name);
  if (r < 0) return null;
  var raw = sh.getRange(r, 4).getValue();
  if (!raw) return null;
  return JSON.parse(raw);
}

/** 응답(JSON) 을 문항별 열로 펼쳐 '정리' 시트에 만듭니다. 채점할 때 한 번 실행하세요. */
function 응답정리() {
  var sh = sheet_();
  var v = sh.getDataRange().getValues();
  var keys = [];
  for (var i = 1; i < v.length; i++) {
    var o = JSON.parse(v[i][3] || '{}');
    for (var k in o) if (keys.indexOf(k) < 0) keys.push(k);
  }
  keys.sort();
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var t = ss.getSheetByName('정리');
  if (t) t.clear(); else t = ss.insertSheet('정리');
  t.appendRow(['학번', '이름', '저장시각'].concat(keys));
  for (var i = 1; i < v.length; i++) {
    var o = JSON.parse(v[i][3] || '{}');
    var row = [v[i][0], v[i][1], v[i][2]];
    for (var j = 0; j < keys.length; j++) row.push(o[keys[j]] || '');
    t.appendRow(row);
  }
}
