import json
import unittest
from src.handler import INCOMING_DIR, PROCESSED_DIR, REJECTED_DIR, lambda_handler

class TestFileProcessor(unittest.TestCase):
    def setUp(self):
        for d in (INCOMING_DIR, PROCESSED_DIR, REJECTED_DIR):
            d.mkdir(parents=True, exist_ok=True)
            for f in d.glob("test_*.json"):
                f.unlink()

    def test_valid_file_moves_to_processed(self):
        p = INCOMING_DIR / "test_valid.json"
        p.write_text(json.dumps({"customer_id":"C1","file_type":"claim","records":2}), encoding="utf-8")
        r = lambda_handler({"file_name": p.name})
        self.assertEqual(r["statusCode"], 200)
        self.assertTrue((PROCESSED_DIR / p.name).exists())

    def test_invalid_file_moves_to_rejected(self):
        p = INCOMING_DIR / "test_invalid.json"
        p.write_text(json.dumps({"customer_id":"C2","file_type":"bad","records":-1}), encoding="utf-8")
        r = lambda_handler({"file_name": p.name})
        self.assertEqual(r["statusCode"], 422)
        self.assertTrue((REJECTED_DIR / p.name).exists())

    def test_missing_file_returns_404(self):
        r = lambda_handler({"file_name":"test_missing.json"})
        self.assertEqual(r["statusCode"], 404)

if __name__ == "__main__":
    unittest.main()
