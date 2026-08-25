# fridge-recipe-mcp

"냉장고에 있는 재료로 뭘 해먹지?"를 도와주는 개인용 MCP 서버입니다.
회사 업무와는 무관하게, MCP 구조를 계속 손에 익히고 싶어서 만든 놀이용 프로젝트입니다.

## 설계 원칙

이 서버(코드)는 "가진 재료 vs 레시피 필요 재료를 정확히 대조"하는 계산까지만 담당합니다.
"재료가 좀 부족해도 이렇게 대체하면 만들 수 있어요" 같은 창의적인 제안은 이 tool을 호출하는
AI가 담당합니다 — 다른 개인/업무 프로젝트에서도 쓰고 있는 "AI 판단 vs 코드의 정확한 계산 분리"
원칙을 그대로 따릅니다.

## 제공 tool

1. `suggest_recipes` — 가진 재료로 만들 수 있는(또는 근접한) 레시피를 커버리지 순으로 추천
2. `whats_missing` — 특정 레시피 하나에 지금 부족한 재료를 정확히 확인
3. `get_recipe_detail` — 레시피의 재료·조리 순서 조회
4. `list_known_ingredients` — 서버가 아는 재료 목록 조회

## 설치 및 실행

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python mcp
.venv/bin/python fridge_recipe_mcp_server.py
```

Claude Desktop 설정(`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "fridge-recipe": {
      "command": "/절대/경로/.venv/bin/python",
      "args": ["/절대/경로/fridge_recipe_mcp_server.py"]
    }
  }
}
```

## 주의

`RECIPE_DB`는 자취/1인 가구 기준 흔한 집밥 레시피 15종 예시입니다. 자유롭게 추가/수정해서 쓰세요.
