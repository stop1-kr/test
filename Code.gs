/**
 * 삼각비 학습지 - 학생 답안 저장 / 불러오기
 * ------------------------------------------------------------
 * [설치 방법]
 *  1) 구글 스프레드시트를 새로 하나 만든다.
 *  2) 주소창의  .../spreadsheets/d/여기가ID/edit  에서 ID 를 복사해
 *     아래 SHEET_ID 에 붙여넣는다.
 *  3) script.google.com 에서 새 프로젝트를 만들고 이 코드를 붙여넣는다.
 *  4) 배포 > 새 배포 > 유형: 웹 앱
 *       - 실행 사용자      : 나
 *       - 액세스 권한      : 모든 사용자        <-- 반드시 이렇게
 *  5) 배포 후 나온 주소( 끝이 /exec )를 index.html 의
 *     var GAS_URL = "";  안에 붙여넣는다.
 */

var SHEET_ID = "여기에_스프레드시트_ID";
var SHEET_NAME = "responses";

function sheet_() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(["학번", "이름", "저장시각", "답안(JSON)"]);
  }
  return sh;
}

function findRow_(sh, sid, name) {
  var last = sh.getLastRow();
  if (last < 2) return -1;
  var v = sh.getRange(2, 1, last - 1, 2).getValues();
  for (var i = 0; i < v.length; i++) {
    if (String(v[i][0]).trim() === String(sid).trim() &&
        String(v[i][1]).trim() === String(name).trim()) {
      return i + 2;
    }
  }
  return -1;
}

/* 저장 : index.html 의 저장 버튼이 POST 로 보낸다 */
function doPost(e) {
  var out = { ok: false };
  try {
    var body = JSON.parse(e.postData.contents);
    var sh = sheet_();
    var row = findRow_(sh, body.sid, body.name);
    var rec = [body.sid, body.name, new Date(), JSON.stringify(body.data || {})];
    if (row > 0) sh.getRange(row, 1, 1, 4).setValues([rec]);
    else sh.appendRow(rec);
    out.ok = true;
  } catch (err) {
    out.error = String(err);
  }
  return ContentService.createTextOutput(JSON.stringify(out))
                       .setMimeType(ContentService.MimeType.JSON);
}

/* 불러오기 : index.html 의 불러오기 버튼이 JSONP 로 부른다 */
function doGet(e) {
  var res = { found: false, data: {} };
  try {
    var sh = sheet_();
    var row = findRow_(sh, e.parameter.sid, e.parameter.name);
    if (row > 0) {
      res.found = true;
      res.data = JSON.parse(sh.getRange(row, 4).getValue() || "{}");
    }
  } catch (err) {
    res.error = String(err);
  }
  var cb = e.parameter.callback;
  if (cb) {
    return ContentService.createTextOutput(cb + "(" + JSON.stringify(res) + ");")
                         .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(JSON.stringify(res))
                       .setMimeType(ContentService.MimeType.JSON);
}

/* 채점용 : 답안 JSON 을 문항별 열로 펼친 시트를 만든다 */
function 응답정리() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = sheet_();
  var last = sh.getLastRow();
  if (last < 2) return;
  var rows = sh.getRange(2, 1, last - 1, 4).getValues();

  var keys = [];
  var seen = {};
  for (var i = 0; i < rows.length; i++) {
    var o = JSON.parse(rows[i][3] || "{}");
    for (var k in o) { if (!seen[k]) { seen[k] = true; keys.push(k); } }
  }
  keys.sort(function (a, b) { return parseInt(a.substring(1), 10) - parseInt(b.substring(1), 10); });

  var out = ss.getSheetByName("정리");
  if (out) out.clear();
  else out = ss.insertSheet("정리");

  out.appendRow(["학번", "이름", "저장시각"].concat(keys));
  for (var j = 0; j < rows.length; j++) {
    var d = JSON.parse(rows[j][3] || "{}");
    var line = [rows[j][0], rows[j][1], rows[j][2]];
    for (var m = 0; m < keys.length; m++) line.push(d[keys[m]] || "");
    out.appendRow(line);
  }
}
