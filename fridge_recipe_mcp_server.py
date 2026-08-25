"""
fridge_recipe_mcp_server.py
----------------------------------
"냉장고에 있는 재료로 뭘 해먹지?"를 도와주는 개인용 MCP 서버입니다.
회사 업무와는 무관하게, MCP 구조를 계속 손에 익히고 싶어서 만든 놀이용 프로젝트입니다.

이 서버(파이썬 코드)가 하는 일은 "가진 재료 vs 레시피 필요 재료를 정확히 대조"하는
계산까지입니다. "재료가 좀 부족해도 이렇게 대체하면 만들 수 있어요" 같은 창의적인
제안은 이 tool을 호출하는 AI가 담당합니다 — 여기서도 다른 프로젝트와 같은 설계 원칙
("AI 판단 vs 코드의 정확한 계산 분리")을 그대로 따릅니다.

제공 기능:
  1) 가진 재료로 만들 수 있는(또는 근접한) 레시피 추천 (suggest_recipes)
  2) 특정 레시피에 지금 부족한 재료 확인 (whats_missing)
  3) 레시피 상세(재료/조리순서) 조회 (get_recipe_detail)
  4) 서버가 아는 재료 목록 조회 (list_known_ingredients)

실행 방법:
  1) pip install mcp
  2) python fridge_recipe_mcp_server.py
  3) Claude Desktop 설정(claude_desktop_config.json)에 등록:
     {
       "mcpServers": {
         "fridge-recipe": {
           "command": "python",
           "args": ["/절대/경로/fridge_recipe_mcp_server.py"]
         }
       }
     }

주의: RECIPE_DB는 자취/1인 가구 기준 흔한 집밥 레시피 15종 예시입니다.
자유롭게 추가/수정해서 쓰세요.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("fridge-recipe")

# required: 없으면 사실상 이 요리라고 부르기 애매한 핵심 재료
# optional: 있으면 좋지만 없어도 만들 수 있는 재료
RECIPE_DB = {
    "김치볶음밥": {
        "required": ["김치", "밥"],
        "optional": ["대파", "계란", "참기름", "스팸", "식용유"],
        "steps": [
            "김치를 잘게 썰어 식용유에 볶는다.",
            "밥을 넣고 김치와 골고루 섞어가며 볶는다.",
            "대파, 스팸 등을 있으면 추가로 볶는다.",
            "불을 끄고 참기름을 둘러 마무리한다. 계란후라이를 올리면 좋다.",
        ],
    },
    "계란찜": {
        "required": ["계란"],
        "optional": ["대파", "새우젓", "당근"],
        "steps": [
            "계란을 풀고 물(계란 부피의 1~1.5배)과 소금(또는 새우젓)을 섞는다.",
            "체에 한번 걸러 곱게 만든다.",
            "약불~중불에서 계속 저어가며 익힌다 (뚝배기면 뚜껑 덮고 약불).",
            "몽글몽글해지면 대파를 넣고 잔열로 마무리한다.",
        ],
    },
    "된장찌개": {
        "required": ["된장", "물"],
        "optional": ["두부", "애호박", "감자", "대파", "양파", "청양고추"],
        "steps": [
            "물에 된장을 풀어 끓인다.",
            "감자, 양파 등 단단한 재료부터 넣고 끓인다.",
            "두부, 애호박을 넣고 한소끔 더 끓인다.",
            "대파, 청양고추를 넣고 마무리한다.",
        ],
    },
    "김치찌개": {
        "required": ["김치"],
        "optional": ["돼지고기", "두부", "대파", "양파", "참치"],
        "steps": [
            "신 김치를 먹기 좋게 썰어 볶는다 (돼지고기 있으면 같이 볶기).",
            "물을 붓고 끓인다.",
            "두부, 양파 등을 넣고 끓인다.",
            "대파를 넣고 마무리한다.",
        ],
    },
    "계란말이": {
        "required": ["계란"],
        "optional": ["대파", "당근", "소금", "식용유"],
        "steps": [
            "계란을 풀고 다진 대파/당근, 소금을 섞는다.",
            "약불로 예열한 팬에 식용유를 두르고 계란물을 얇게 붓는다.",
            "반쯤 익으면 돌돌 말고, 남은 계란물을 부어가며 반복한다.",
            "한 김 식힌 뒤 먹기 좋게 썬다.",
        ],
    },
    "오이무침": {
        "required": ["오이"],
        "optional": ["고춧가루", "식초", "설탕", "마늘", "참기름"],
        "steps": [
            "오이를 얇게 썰어 소금에 절였다가 물기를 짠다.",
            "고춧가루, 식초, 설탕, 다진 마늘을 넣고 무친다.",
            "참기름을 둘러 마무리한다.",
        ],
    },
    "감자채볶음": {
        "required": ["감자"],
        "optional": ["당근", "양파", "식용유", "소금"],
        "steps": [
            "감자를 채 썰어 찬물에 담가 전분기를 뺀다.",
            "식용유에 당근, 양파를 먼저 볶는다.",
            "감자채를 넣고 투명해질 때까지 볶는다.",
            "소금으로 간한다.",
        ],
    },
    "두부조림": {
        "required": ["두부"],
        "optional": ["간장", "대파", "고춧가루", "마늘"],
        "steps": [
            "두부를 도톰하게 썰어 팬에 노릇하게 지진다.",
            "간장, 물, 다진 마늘, 고춧가루로 양념장을 만든다.",
            "두부에 양념장을 붓고 졸인다.",
            "대파를 올려 마무리한다.",
        ],
    },
    "콩나물무침": {
        "required": ["콩나물"],
        "optional": ["대파", "마늘", "참기름", "소금"],
        "steps": [
            "콩나물을 소금물에 삶는다 (뚜껑 열고 삶으면 비린내 줄어듦).",
            "찬물에 헹궈 물기를 짠다.",
            "다진 마늘, 대파, 참기름, 소금을 넣고 무친다.",
        ],
    },
    "어묵볶음": {
        "required": ["어묵"],
        "optional": ["대파", "양파", "간장", "고춧가루"],
        "steps": [
            "어묵을 먹기 좋게 썬다.",
            "식용유에 양파, 어묵을 볶는다.",
            "간장, 약간의 설탕으로 간한다.",
            "대파를 넣고 마무리한다.",
        ],
    },
    "라면": {
        "required": ["라면"],
        "optional": ["계란", "대파", "김치"],
        "steps": [
            "물을 끓이고 면과 스프를 넣는다.",
            "계란, 대파 등 있는 재료를 추가한다.",
            "취향에 맞게 더 끓인다.",
        ],
    },
    "스팸마요덮밥": {
        "required": ["스팸", "밥"],
        "optional": ["계란", "마요네즈", "김가루", "간장"],
        "steps": [
            "스팸을 잘게 썰어 노릇하게 굽는다.",
            "밥 위에 스팸을 올린다.",
            "계란후라이, 마요네즈, 김가루를 올린다.",
            "간장을 살짝 둘러 마무리한다.",
        ],
    },
    "참치김치찌개": {
        "required": ["김치", "참치"],
        "optional": ["두부", "대파", "양파"],
        "steps": [
            "김치를 볶다가 물을 붓고 끓인다.",
            "참치(기름 제거)를 넣고 끓인다.",
            "두부, 대파를 넣고 마무리한다.",
        ],
    },
    "감자전": {
        "required": ["감자"],
        "optional": ["소금", "식용유"],
        "steps": [
            "감자를 강판에 갈아 물을 살짝 따라낸다 (전분은 남기기).",
            "소금으로 간한다.",
            "식용유 두른 팬에 얇게 펴서 노릇하게 굽는다.",
        ],
    },
    "애호박볶음": {
        "required": ["애호박"],
        "optional": ["양파", "새우젓", "식용유", "대파"],
        "steps": [
            "애호박을 반달 모양으로 썬다.",
            "식용유에 애호박, 양파를 볶는다.",
            "새우젓(또는 소금)으로 간한다.",
        ],
    },
}


def _normalize(text: str) -> str:
    return text.strip().replace(" ", "")


def _has_ingredient(owned_norm: set[str], target: str) -> bool:
    """보유 재료 중 target과 정확히 같거나, 서로 부분 문자열로 포함되면 있다고 본다.
    예: 보유 '대파' vs 레시피 요구 '파' 서로 매치."""
    t = _normalize(target)
    return any(t in owned or owned in t for owned in owned_norm)


@mcp.tool()
def suggest_recipes(ingredients: list[str], top_k: int = 5) -> list[dict]:
    """
    가진 재료 목록을 받아, RECIPE_DB의 레시피들과 대조해 만들 수 있는(또는 근접한) 순서로
    추천한다. required 재료 커버리지가 높고 부족한 재료가 적은 순으로 정렬한다.
    """
    owned_norm = {_normalize(i) for i in ingredients if i.strip()}
    results = []
    for name, recipe in RECIPE_DB.items():
        required = recipe["required"]
        optional = recipe.get("optional", [])
        matched_required = [r for r in required if _has_ingredient(owned_norm, r)]
        missing_required = [r for r in required if r not in matched_required]
        matched_optional = [o for o in optional if _has_ingredient(owned_norm, o)]
        coverage = len(matched_required) / len(required) if required else 0.0

        results.append({
            "recipe": name,
            "coverage": round(coverage, 2),
            "ready_to_cook": coverage == 1.0,
            "matched_required": matched_required,
            "missing_required": missing_required,
            "matched_optional": matched_optional,
        })

    results.sort(key=lambda r: (-r["coverage"], len(r["missing_required"]), -len(r["matched_optional"])))
    return results[:top_k]


@mcp.tool()
def whats_missing(recipe_name: str, ingredients: list[str]) -> dict:
    """특정 레시피 하나를 정해두고, 지금 가진 재료로는 뭐가 부족한지 정확히 알려준다."""
    recipe = RECIPE_DB.get(recipe_name)
    if recipe is None:
        return {"ok": False, "error": f"'{recipe_name}' 레시피를 모릅니다.", "known_recipes": list(RECIPE_DB)}

    owned_norm = {_normalize(i) for i in ingredients if i.strip()}
    missing_required = [r for r in recipe["required"] if not _has_ingredient(owned_norm, r)]
    missing_optional = [o for o in recipe.get("optional", []) if not _has_ingredient(owned_norm, o)]

    return {
        "ok": True,
        "recipe": recipe_name,
        "ready_to_cook": not missing_required,
        "missing_required": missing_required,
        "missing_optional": missing_optional,
    }


@mcp.tool()
def get_recipe_detail(recipe_name: str) -> dict:
    """레시피 하나의 필수/선택 재료와 조리 순서를 전부 보여준다."""
    recipe = RECIPE_DB.get(recipe_name)
    if recipe is None:
        return {"ok": False, "error": f"'{recipe_name}' 레시피를 모릅니다.", "known_recipes": list(RECIPE_DB)}
    return {"ok": True, "recipe": recipe_name, **recipe}


@mcp.tool()
def list_known_ingredients() -> list[str]:
    """이 서버가 레시피 매칭에 쓰는 전체 재료 목록(중복 제거, 가나다순)을 보여준다."""
    all_ingredients = set()
    for recipe in RECIPE_DB.values():
        all_ingredients.update(recipe["required"])
        all_ingredients.update(recipe.get("optional", []))
    return sorted(all_ingredients)


if __name__ == "__main__":
    mcp.run()
