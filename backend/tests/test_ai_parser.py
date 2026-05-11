import pytest
import json
from pathlib import Path
from app.services.ai_parser import parse_transaction

_json_path = Path(__file__).parent.parent.parent / "docs/test_frases_ia.json"
with open(_json_path) as f:
    TEST_CASES = json.load(f)["casos_de_teste"]


@pytest.mark.asyncio
@pytest.mark.parametrize("caso", TEST_CASES)
async def test_parse_frase(caso):
    if caso["output_esperado"]["confianca"] == "nenhuma":
        result = await parse_transaction(caso["input"], "test-user")
        assert result["tipo"] is None
        return

    result = await parse_transaction(caso["input"], "test-user")
    expected = caso["output_esperado"]

    assert result["tipo"] == expected["tipo"]
    if expected["valor"] is not None:
        assert abs(result["valor"] - expected["valor"]) < 0.01
    assert result["categoria"] == expected["categoria"]
