/**
 * Python 재수강 강의 - 자가진단 10문항 (Google Form 자동 생성 스크립트)
 *
 * ── 사용법 ────────────────────────────────────────────────────────
 * 1. https://script.google.com 접속 → [새 프로젝트]
 * 2. 이 파일 내용 전체 복사 → 좌측 코드 영역에 붙여넣기 → 💾 저장
 * 3. 상단에서 함수 [createPythonDiagnosticForm] 선택 → ▶ [실행]
 *    - 처음 실행 시 권한 허용 요청 → [고급] → [프로젝트로 이동] → [허용]
 * 4. 실행 완료 후 [실행 로그] 패널에 두 URL이 표시됩니다:
 *      • 학생용 응답 URL  (단축 후 학생에게 공유)
 *      • 강사용 편집 URL  (질문 손보기, 응답 확인)
 *
 * ── 특징 ──────────────────────────────────────────────────────────
 *  • 퀴즈 모드 ON (자동 채점 + 응답 후 정답·해설 표시)
 *  • 객관식 3문항 (Q1·Q4·Q8) — 자동 채점
 *  • 단답/장문 7문항 — 강사 수동 채점 (정답·해설은 자동 안내)
 *  • 이름 + 이메일 수집 (누가 풀었는지 식별)
 *
 * 출처: docs/02_language/08_python/01_00_python.md
 */

function createPythonDiagnosticForm() {
  const form = FormApp.create('Python 재수강 — 사전 자가진단 10문항');

  form.setDescription(
    '본격 강의 전 본인의 Python 문법 이해도를 점검합니다.\n\n' +
    '• 코드 결과를 예측하거나 직접 실행한 결과를 적어주세요.\n' +
    '• 모두 맞히지 않아도 됩니다 — 강사가 어느 챕터에 시간을 더 쓸지 정하는 자료입니다.\n' +
    '• 예상 소요시간: 약 10~15분'
  );
  form.setIsQuiz(true);
  form.setCollectEmail(true);
  form.setShowLinkToRespondAgain(false);

  // ─── 응답자 이름 ────────────────────────────────────────
  form.addTextItem()
      .setTitle('이름 (또는 닉네임)')
      .setHelpText('강사가 결과를 정리할 때 사용합니다.')
      .setRequired(true);

  // ─── Q1: 객관식 ─────────────────────────────────────────
  const q1 = form.addMultipleChoiceItem();
  q1.setTitle('Q1 — 변수와 타입')
    .setHelpText(
      '다음 코드를 실행하면 어떻게 될까요?\n\n' +
      'a = "5"\n' +
      'b = 3\n' +
      'print(a + b)'
    )
    .setPoints(1)
    .setRequired(true)
    .setChoices([
      q1.createChoice('8', false),
      q1.createChoice('"53"', false),
      q1.createChoice('에러', true),                // 정답
      q1.createChoice('"5" + 3', false),
    ])
    .setFeedbackForCorrect(FormApp.createFeedback().setText(
      '정답입니다. TypeError 발생: can only concatenate str (not "int") to str. ' +
      '문자열과 숫자는 + 로 못 더함. int(a) + b 또는 a + str(b) 로 형변환 필요.'
    ).build())
    .setFeedbackForIncorrect(FormApp.createFeedback().setText(
      '정답은 "에러". TypeError 발생. 문자열과 숫자는 + 로 못 더함. ' +
      '→ 챕터 02 변수·타입·연산자 참고'
    ).build());

  // ─── Q2: 장문 ───────────────────────────────────────────
  form.addParagraphTextItem()
      .setTitle('Q2 — == vs is')
      .setHelpText(
        '다음 코드의 출력 두 줄을 적고, 왜 그런지 한 줄로 설명하세요.\n\n' +
        'a = [1, 2, 3]\n' +
        'b = [1, 2, 3]\n' +
        'print(a == b)\n' +
        'print(a is b)'
      )
      .setRequired(true)
      .setPoints(1)
      .setGeneralFeedback(FormApp.createFeedback().setText(
        '모범 답안: True / False\n' +
        '== 는 값이 같은가, is 는 같은 객체(메모리)인가. ' +
        '리스트는 매번 새로 만들어지므로 값은 같아도 서로 다른 객체. ' +
        '→ 챕터 02'
      ).build());

  // ─── Q3: 장문 ───────────────────────────────────────────
  form.addParagraphTextItem()
      .setTitle('Q3 — 문자열 슬라이싱')
      .setHelpText(
        '다음 코드의 출력 두 줄은?\n\n' +
        's = "Hello, World!"\n' +
        'print(s[7:12])\n' +
        'print(s[-6:-1])'
      )
      .setRequired(true)
      .setPoints(1)
      .setGeneralFeedback(FormApp.createFeedback().setText(
        '모범 답안: World / World\n' +
        '음수 인덱스는 뒤에서부터. 위치 7~11과 -6~-2는 같은 글자 묶음. ' +
        '슬라이싱 끝은 항상 불포함. → 챕터 03'
      ).build());

  // ─── Q4: 객관식 ─────────────────────────────────────────
  const q4 = form.addMultipleChoiceItem();
  q4.setTitle('Q4 — 리스트 mutability')
    .setHelpText(
      '다음 코드 실행 후 a의 값은?\n\n' +
      'a = [1, 2, 3]\n' +
      'b = a\n' +
      'b.append(4)\n' +
      'print(a)'
    )
    .setPoints(1)
    .setRequired(true)
    .setChoices([
      q4.createChoice('[1, 2, 3]', false),
      q4.createChoice('[1, 2, 3, 4]', true),       // 정답
      q4.createChoice('에러', false),
    ])
    .setFeedbackForCorrect(FormApp.createFeedback().setText(
      '정답입니다. b = a 는 복사가 아니라 같은 리스트를 두 이름으로 부르는 것. ' +
      'b.append(4) 는 그 객체를 수정 → a도 영향 받음. 복사: b = a.copy() 또는 b = a[:].'
    ).build())
    .setFeedbackForIncorrect(FormApp.createFeedback().setText(
      '정답: [1, 2, 3, 4]. b = a 는 같은 객체를 가리킴(복사 아님). ' +
      '리스트는 mutable이라 b.append(4) 가 a에도 영향. → 챕터 04 (얕은복사 함정)'
    ).build());

  // ─── Q5: 단답 ───────────────────────────────────────────
  form.addParagraphTextItem()
      .setTitle('Q5 — 딕셔너리 KeyError')
      .setHelpText(
        '다음 코드 실행 시 발생하는 에러의 이름은? (예: ValueError)\n\n' +
        'd = {"name": "Alice", "age": 30}\n' +
        'print(d["city"])'
      )
      .setRequired(true)
      .setPoints(1)
      .setGeneralFeedback(FormApp.createFeedback().setText(
        '정답: KeyError\n' +
        '안전한 접근: d.get("city") → None, d.get("city", 기본값). ' +
        '또는 if "city" in d:. → 챕터 05'
      ).build());

  // ─── Q6: 단답 ───────────────────────────────────────────
  form.addParagraphTextItem()
      .setTitle('Q6 — for + range')
      .setHelpText(
        '다음 코드의 출력은? (공백 구분, 한 줄)\n\n' +
        'for i in range(2, 10, 2):\n' +
        '    print(i, end=" ")'
      )
      .setRequired(true)
      .setPoints(1)
      .setGeneralFeedback(FormApp.createFeedback().setText(
        '정답: 2 4 6 8\n' +
        'range(시작, 끝, 간격) — 끝은 불포함. 10은 미포함. → 챕터 06'
      ).build());

  // ─── Q7: 단답 ───────────────────────────────────────────
  form.addParagraphTextItem()
      .setTitle('Q7 — 함수 return')
      .setHelpText(
        'result 에 들어 있는 값은?\n\n' +
        'def add(a, b):\n' +
        '    print(a + b)\n\n' +
        'result = add(3, 4)\n' +
        'print(result)'
      )
      .setRequired(true)
      .setPoints(1)
      .setGeneralFeedback(FormApp.createFeedback().setText(
        '정답: None\n' +
        'print 는 화면 출력만, return 이 없으면 함수는 None 반환. ' +
        '함수를 다른 코드에 쓸 거면 return 필수. → 챕터 07'
      ).build());

  // ─── Q8: 객관식 ─────────────────────────────────────────
  const q8 = form.addMultipleChoiceItem();
  q8.setTitle('Q8 — 가변 기본값 함정')
    .setHelpText(
      '두 번째 호출 결과는?\n\n' +
      'def add_item(item, items=[]):\n' +
      '    items.append(item)\n' +
      '    return items\n\n' +
      'print(add_item("apple"))\n' +
      'print(add_item("banana"))    ← 이 출력은?'
    )
    .setPoints(1)
    .setRequired(true)
    .setChoices([
      q8.createChoice('["banana"]', false),
      q8.createChoice('["apple", "banana"]', true),  // 정답
      q8.createChoice('에러', false),
    ])
    .setFeedbackForCorrect(FormApp.createFeedback().setText(
      '정답입니다. 기본값 리스트는 함수 정의 시 1회만 생성되어 ' +
      '호출 사이에 공유됨. 안전한 패턴: items=None → if items is None: items = []'
    ).build())
    .setFeedbackForIncorrect(FormApp.createFeedback().setText(
      '정답: ["apple", "banana"]. 가변 기본값 함정 — 기본값 리스트가 호출 간 공유. ' +
      '→ 챕터 07 (가변 기본값 함정 ★)'
    ).build());

  // ─── Q9: 단답 ───────────────────────────────────────────
  form.addParagraphTextItem()
      .setTitle('Q9 — 리스트 컴프리헨션')
      .setHelpText(
        '출력은?\n\n' +
        'nums = [1, 2, 3, 4, 5]\n' +
        'result = [x * 2 for x in nums if x % 2 == 0]\n' +
        'print(result)'
      )
      .setRequired(true)
      .setPoints(1)
      .setGeneralFeedback(FormApp.createFeedback().setText(
        '정답: [4, 8]\n' +
        '짝수만 골라(if x % 2 == 0) 2배. ' +
        '컴프리헨션 = [변환식 for 변수 in 반복 if 조건]. → 챕터 08'
      ).build());

  // ─── Q10: 장문 ──────────────────────────────────────────
  form.addParagraphTextItem()
      .setTitle('Q10 — try/except')
      .setHelpText(
        '출력 줄 수와 각 줄의 내용을 적어주세요.\n\n' +
        'try:\n' +
        '    n = int("hello")\n' +
        '    print("OK")\n' +
        'except ValueError:\n' +
        '    print("값 변환 오류")\n' +
        'except Exception:\n' +
        '    print("기타 오류")\n' +
        'finally:\n' +
        '    print("종료")'
      )
      .setRequired(true)
      .setPoints(1)
      .setGeneralFeedback(FormApp.createFeedback().setText(
        '모범 답안: 2줄 — "값 변환 오류" / "종료"\n' +
        'int("hello") → ValueError 발생 → 첫 except 가 잡음 → ' +
        'try 블록 나머지(print("OK"))는 실행 안 됨 → finally 는 항상 실행. → 챕터 08'
      ).build());

  // ─── 마지막: 본인 관심 챕터 (의향 조사, 점수 X) ────────────
  const interest = form.addMultipleChoiceItem();
  interest
    .setTitle('마지막으로 — 본 강의에서 가장 중점적으로 잡고 싶은 부분은?')
    .setHelpText('하나만 선택하셔도 되고, 잘 모르겠으면 마지막 항목으로.')
    .setRequired(false)
    .setChoiceValues([
      '02 변수·타입·연산자 기초',
      '03 문자열 처리',
      '04 리스트·튜플 (mutable/얕은복사)',
      '05 딕셔너리·세트',
      '06 조건문·반복문 (range/enumerate/zip)',
      '07 함수 (return, *args, 스코프)',
      '08 컴프리헨션·파일·예외',
      '09 모듈·클래스·OOP',
      '잘 모르겠음 — 추천해주세요',
    ]);

  // ─── URL 출력 ────────────────────────────────────────────
  const editorUrl = form.getEditUrl();
  const publishedUrl = form.getPublishedUrl();
  const shortUrl = form.shortenFormUrl(publishedUrl);

  Logger.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  Logger.log('✅ Google Form 생성 완료');
  Logger.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  Logger.log('📝 학생용 응답 URL:');
  Logger.log('   ' + publishedUrl);
  Logger.log('🔗 단축 URL: ' + shortUrl);
  Logger.log('');
  Logger.log('✏️  강사용 편집 URL:');
  Logger.log('   ' + editorUrl);
  Logger.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  Logger.log('💡 다음 단계:');
  Logger.log('  1. 편집 URL 열기 → 필요시 문구·디자인 가다듬기');
  Logger.log('  2. 우측 상단 [응답] 탭 → 스프레드시트 아이콘으로 결과 수집');
  Logger.log('  3. 단축 URL을 학생에게 공유');
  Logger.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  return { editorUrl: editorUrl, publishedUrl: publishedUrl, shortUrl: shortUrl };
}
