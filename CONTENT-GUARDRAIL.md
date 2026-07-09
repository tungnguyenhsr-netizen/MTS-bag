# MTS WEBSITE — CONTENT-ONLY GUARDRAIL (Hermes Workers)

> Áp dụng cho MỌI worker Hermes được giao sửa website MTS.
> Visual/code (UI/UX, CSS, layout, structure) là việc của **OpenDesign** — KHÔNG phải Hermes.

## HARD RULE (tuyệt đối)
1. **CHỈ được sửa TEXT nội dung** (copywriting) bên trong các element có `lang="vi"` hoặc `lang="en"`.
2. **CẤM đụng vào:**
   - `<style>` block (toàn bộ CSS) — kể cả variable, class, media query.
   - `class="..."` attribute — KHÔNG thêm/sửa/xoá class.
   - `id="..."`, `src="..."`, `href="..."`, `style="..."`, `data-*`, `loading`, `alt` (trừ alt là text content thuần).
   - `<script>` block và mọi JS.
   - Thẻ cấu trúc (`<section>`, `<div>`, `<nav>`, `<footer>`, `<img>`...) — KHÔNG thêm/bớt/sửa tag.
   - Token system (`:root`), design tokens.
3. **ĐƯỢC phép:**
   - Sửa nội dung text trong `<h1..h6>`, `<p>`, `<span>`, `<a>` (phần text, không sửa href), `<div>` thuần text, `<li>`.
   - Đổi từ ngữ, sửa lỗi chính tả, cải thiện copy, thêm/bớt câu — miễn nằm trong element có `lang`.
   - Sửa CẢ 2 bản VI và EN (phải song ngữ, không bỏ 1 bên).
4. **NGUYÊN TẮC SONG NGỮ:** mọi sửa VI phải có bản EN tương đương (và ngược lại). Không được để 1 lang thiếu.
5. **KHÔNG đổi brand:** giữ "Minh Tùng Studio / MTS", MOQ 300, OEM/ODM, TP.HCM. KHÔNG dùng từ cấm (bespoke/tailoring/couture/made-to-measure).
6. **KHÔNG thêm section mới, không xoá section.** Chỉ chỉnh text trong section hiện có.

## CHECKLIST TRƯỚC KHI COMMIT
- [ ] Diff KHÔNG chạm `<style>` / `<script>` / `class=` / `id=` / `src=` / `href=` / `style=`.
- [ ] Chỉ các dòng text (VI + EN) thay đổi.
- [ ] Không element structure thay đổi.
- [ ] Validator script (`validate-content-only.py`) pass với exit 0.

## VI PHẠM = BLOCKED
Nếu worker cần đổi visual/code → **STOP**, báo user: "cần đổi UI/CSS → chuyển sang OpenDesign". Không tự sửa.
