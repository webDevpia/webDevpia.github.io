# HTML 목업을 이미지로 변환

마크다운 파일 안의 HTML 목업 블록을 Playwright 스크린샷으로 캡처하여 이미지로 교체합니다.

## 입력

$ARGUMENTS 에 대상 마크다운 파일 경로가 전달됩니다. (예: `docs/12_ai_native_javascript/17_통합프로젝트_영화앱.md`)

## 작업 절차

1. **대상 파일 읽기**: 전달된 파일 경로의 마크다운 파일을 Read 도구로 읽습니다.

2. **HTML 목업 블록 찾기**: `<div markdown="0"` 또는 인라인 스타일이 포함된 HTML 블록을 찾습니다. 여러 개가 있으면 사용자에게 어떤 블록을 변환할지 확인합니다.

3. **Jekyll 서버 확인**: `lsof -i :4000` 으로 Jekyll 서버가 실행 중인지 확인합니다. 실행 중이 아니면 사용자에게 `bundle exec jekyll serve` 실행을 요청합니다.

4. **페이지 URL 결정**: 마크다운 frontmatter의 `permalink` 값을 읽어서 `http://localhost:4000{permalink}` URL을 결정합니다.

5. **Playwright로 캡처**:
   - `mcp__plugin_playwright_playwright__browser_navigate` 로 페이지 이동
   - `mcp__plugin_playwright_playwright__browser_evaluate` 로 목업 요소에 임시 id 부여:
     ```javascript
     () => {
       const el = document.querySelector('div[style*="max-width"]');
       if (el) { el.id = 'mockup-capture'; return 'found'; }
       return 'not found';
     }
     ```
   - `mcp__plugin_playwright_playwright__browser_run_code` 로 요소만 스크린샷:
     ```javascript
     async (page) => {
       const el = await page.$('#mockup-capture');
       await el.screenshot({ path: '저장경로', type: 'png', scale: 'device' });
     }
     ```

6. **이미지 저장 경로 결정**:
   - 마크다운 파일이 위치한 디렉토리에 `img/` 폴더를 사용합니다.
   - 파일명에서 이미지명 생성 (예: `17_통합프로젝트_영화앱.md` → `movie-app-mockup.png`)
   - 예시: `docs/12_ai_native_javascript/17_통합프로젝트_영화앱.md`
     → 저장 경로: `docs/12_ai_native_javascript/img/movie-app-mockup.png`
   - `img/` 디렉토리가 없으면 `mkdir -p`로 생성

7. **마크다운 교체**: Edit 도구로 HTML 블록 전체를 이미지 참조로 교체합니다.
   permalink를 사용하는 Jekyll 사이트이므로, 마크다운 파일 기준 상대경로가 아닌 **프로젝트 루트 기준 절대경로**를 사용합니다:
   ```markdown
   ![{적절한 alt 텍스트}](/{마크다운파일디렉토리}/img/{이미지명})
   ```
   예시: 파일이 `docs/12_ai_native_javascript/` 에 있으면:
   ```markdown
   ![영화 검색 앱 완성 화면](/docs/12_ai_native_javascript/img/movie-app-mockup.png)
   ```

8. **빌드 검증**: `bundle exec jekyll build 2>&1 | tail -5` 로 빌드 성공 여부를 확인합니다.

9. **결과 보고**: 캡처된 이미지를 Read 도구로 보여주고, 변환 결과를 요약합니다.

## 주의사항

- HTML 블록의 시작 태그(`<div ...>`)부터 닫는 태그(`</div>`)까지 전체를 교체해야 합니다.
- Kramdown이 HTML 내부를 파싱하지 않도록 `markdown="0"` 속성이 있는 경우 함께 제거합니다.
- 이미지 alt 텍스트는 목업의 제목이나 용도를 반영하여 작성합니다.
- 기존 이미지 파일이 있으면 덮어씁니다.
